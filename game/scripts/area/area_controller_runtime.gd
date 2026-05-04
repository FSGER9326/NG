extends Node2D
class_name AreaControllerRuntime

const DataLoader = preload("res://game/scripts/core/data_loader.gd")
const GameState = preload("res://game/scripts/core/game_state.gd")
const QuestSystem = preload("res://game/scripts/systems/quest_system.gd")
const CrpgTheme = preload("res://game/scripts/ui/crpg_theme.gd")
const GameLog = preload("res://game/scripts/core/game_log.gd")
const DebugStateDump = preload("res://game/scripts/core/debug_state_dump.gd")

@export var area_id: String = "wolfpine_road"
@export var player_speed: float = 260.0

var data_loader: DataLoader
var game_state: GameState
var quest_system: QuestSystem
var pending_player_profile: Dictionary = {}
var area_data: Dictionary = {}
var hotspots_data: Dictionary = {"hotspots": []}
var actors_data: Dictionary = {"actors": []}
var actor_definitions: Dictionary = {}
var active_dialogue: Dictionary = {}
var active_dialogue_node_id: String = ""

var background_layer: ColorRect
var label_layer: Node2D
var hotspot_layer: Node2D
var actor_layer: Node2D
var player_marker: Label
var move_target: Vector2 = Vector2.ZERO
var has_move_target: bool = false
var debug_label: Label
var quest_panel: PanelContainer
var quest_tracker_label: Label
var dialogue_panel: PanelContainer
var dialogue_speaker_label: Label
var dialogue_text_label: RichTextLabel
var dialogue_choices_box: VBoxContainer

func _ready() -> void:
	if not GameLog.is_started():
		GameLog.start_session("area_runtime")
	else:
		GameLog.info("BOOT", "Area runtime joined existing log session", {"area_id": area_id})
	data_loader = DataLoader.new()
	game_state = GameState.new()
	quest_system = QuestSystem.new()
	if not pending_player_profile.is_empty():
		game_state.apply_player_profile(pending_player_profile)
	_build_runtime_nodes()
	load_area(area_id)
	_update_quest_tracker()
	write_debug_state("state_initial.json")

func setup_player_profile(profile: Dictionary) -> void:
	pending_player_profile = profile.duplicate(true)
	if game_state != null:
		game_state.apply_player_profile(pending_player_profile)
		_update_quest_tracker()
		write_debug_state("state_latest.json")

func _process(delta: float) -> void:
	_update_player_movement(delta)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		if dialogue_panel != null and dialogue_panel.visible:
			GameLog.event("input_ignored", {"reason": "dialogue_open", "position": _vec2_to_array(event.position)})
			return
		move_target = event.position
		has_move_target = true
		GameLog.info("INPUT", "Ground click move target %s" % str(move_target.round()), {"position": _vec2_to_array(move_target)})
		_set_debug("Moving to %s" % str(move_target.round()))

func _build_runtime_nodes() -> void:
	background_layer = ColorRect.new()
	background_layer.name = "PlaceholderBackground"
	background_layer.color = Color(0.035, 0.045, 0.035, 0.82)
	background_layer.position = Vector2.ZERO
	background_layer.size = Vector2(1280, 720)
	background_layer.z_index = -20
	add_child(background_layer)

	label_layer = Node2D.new()
	label_layer.name = "LabelLayer"
	label_layer.z_index = 20
	add_child(label_layer)

	hotspot_layer = Node2D.new()
	hotspot_layer.name = "HotspotLayer"
	hotspot_layer.z_index = 30
	add_child(hotspot_layer)

	actor_layer = Node2D.new()
	actor_layer.name = "ActorLayer"
	actor_layer.z_index = 40
	add_child(actor_layer)

	player_marker = Label.new()
	player_marker.name = "PlayerMarker"
	player_marker.text = "◆ party"
	player_marker.position = Vector2(180, 540)
	player_marker.z_index = 50
	player_marker.add_theme_font_size_override("font_size", 18)
	CrpgTheme.apply_label(player_marker, true)
	add_child(player_marker)

	debug_label = Label.new()
	debug_label.name = "DebugLabel"
	debug_label.position = Vector2(24, 24)
	debug_label.custom_minimum_size = Vector2(620, 80)
	debug_label.z_index = 80
	debug_label.text = "NG area prototype"
	CrpgTheme.apply_label(debug_label)
	add_child(debug_label)

	_build_quest_panel()
	_build_dialogue_panel()
	GameLog.event("runtime_nodes_built", {})

func _build_quest_panel() -> void:
	quest_panel = PanelContainer.new()
	quest_panel.name = "QuestPanel"
	quest_panel.position = Vector2(900, 24)
	quest_panel.size = Vector2(340, 170)
	quest_panel.z_index = 80
	CrpgTheme.apply_dark_panel(quest_panel)
	add_child(quest_panel)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 10)
	margin.add_theme_constant_override("margin_top", 8)
	margin.add_theme_constant_override("margin_right", 10)
	margin.add_theme_constant_override("margin_bottom", 8)
	quest_panel.add_child(margin)

	quest_tracker_label = Label.new()
	quest_tracker_label.name = "QuestTracker"
	quest_tracker_label.text = "Quests: none"
	CrpgTheme.apply_label(quest_tracker_label)
	margin.add_child(quest_tracker_label)

func _build_dialogue_panel() -> void:
	dialogue_panel = PanelContainer.new()
	dialogue_panel.name = "DialoguePanel"
	dialogue_panel.position = Vector2(24, 420)
	dialogue_panel.size = Vector2(820, 270)
	dialogue_panel.z_index = 90
	dialogue_panel.visible = false
	CrpgTheme.apply_panel(dialogue_panel)
	add_child(dialogue_panel)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 14)
	margin.add_theme_constant_override("margin_top", 12)
	margin.add_theme_constant_override("margin_right", 12)
	margin.add_theme_constant_override("margin_bottom", 12)
	dialogue_panel.add_child(margin)

	var root := VBoxContainer.new()
	root.name = "DialogueRoot"
	root.add_theme_constant_override("separation", 8)
	margin.add_child(root)

	dialogue_speaker_label = Label.new()
	dialogue_speaker_label.name = "Speaker"
	dialogue_speaker_label.text = "Speaker"
	CrpgTheme.apply_label(dialogue_speaker_label, true)
	root.add_child(dialogue_speaker_label)

	dialogue_text_label = RichTextLabel.new()
	dialogue_text_label.name = "Text"
	dialogue_text_label.custom_minimum_size = Vector2(780, 90)
	dialogue_text_label.fit_content = true
	dialogue_text_label.scroll_active = false
	CrpgTheme.apply_rich_text(dialogue_text_label)
	root.add_child(dialogue_text_label)

	dialogue_choices_box = VBoxContainer.new()
	dialogue_choices_box.name = "Choices"
	dialogue_choices_box.add_theme_constant_override("separation", 4)
	root.add_child(dialogue_choices_box)

func load_area(next_area_id: String, entry_id: String = "south_road") -> void:
	area_id = next_area_id
	var area_path := "res://areas/%s/area.json" % area_id
	GameLog.info("AREA", "Loading area: %s" % area_id, {"area_id": area_id, "entry_id": entry_id, "path": area_path})
	area_data = data_loader.load_json_file(area_path)
	if area_data.is_empty():
		GameLog.error("AREA", "Failed to load area: %s" % area_id, {"area_id": area_id})
		_set_debug("Failed to load area: %s" % area_id)
		return

	hotspots_data = _load_optional_json_path(String(area_data.get("hotspots", "")), {"area_id": area_id, "hotspots": []})
	actors_data = _load_optional_json_path(String(area_data.get("actors", "")), {"area_id": area_id, "actors": []})
	actor_definitions = _load_actor_definitions()
	_render_area(entry_id)
	GameLog.info("AREA", "Area loaded: %s" % area_id, {
		"area_id": area_id,
		"entry_id": entry_id,
		"hotspot_count": hotspots_data.get("hotspots", []).size(),
		"actor_count": actors_data.get("actors", []).size()
	})
	write_debug_state("state_latest.json")

func _load_optional_json_path(path: String, fallback: Dictionary) -> Dictionary:
	if path.is_empty():
		return fallback.duplicate(true)
	var loaded := data_loader.load_json_file(_to_res_path(path))
	if loaded.is_empty():
		return fallback.duplicate(true)
	return loaded

func _load_actor_definitions() -> Dictionary:
	var result := {}
	for path in [
		"res://data/actors/npcs/captain_renna.json",
		"res://data/actors/companions/brannoc.json",
		"res://data/actors/enemies/border_bandit.json"
	]:
		var actor_data := data_loader.load_json_file(path)
		var actor_id := String(actor_data.get("id", ""))
		if not actor_id.is_empty():
			result[actor_id] = actor_data
			GameLog.event("actor_definition_loaded", {"actor_id": actor_id, "path": path})
	return result

func _render_area(entry_id: String = "south_road") -> void:
	_clear_layer(label_layer)
	_clear_layer(hotspot_layer)
	_clear_layer(actor_layer)
	_hide_dialogue()

	var area_name := String(area_data.get("name", area_id))
	var description := String(area_data.get("description", ""))
	_set_debug("Loaded %s\n%s" % [area_name, description])
	_draw_area_title(area_name)
	_draw_hotspots()
	_draw_actors()
	_place_player_at_entry(entry_id)
	GameLog.event("area_rendered", {"area_id": area_id, "area_name": area_name, "entry_id": entry_id})

func _draw_area_title(area_name: String) -> void:
	var title := Label.new()
	title.name = "AreaTitle"
	title.text = area_name
	title.position = Vector2(24, 92)
	CrpgTheme.apply_label(title, true)
	label_layer.add_child(title)

func _draw_hotspots() -> void:
	for hotspot in hotspots_data.get("hotspots", []):
		if typeof(hotspot) != TYPE_DICTIONARY:
			continue
		var marker := Button.new()
		marker.name = "Hotspot_%s" % String(hotspot.get("id", "unknown"))
		marker.text = String(hotspot.get("name", "Hotspot"))
		marker.position = _array_to_vec2(hotspot.get("position", [0, 0]))
		marker.size = Vector2(180, 34)
		CrpgTheme.apply_button(marker)
		marker.pressed.connect(_on_hotspot_pressed.bind(hotspot))
		hotspot_layer.add_child(marker)
		GameLog.event("hotspot_placed", {"hotspot_id": String(hotspot.get("id", "")), "position": _vec2_to_array(marker.position)})

func _draw_actors() -> void:
	for actor in actors_data.get("actors", []):
		if typeof(actor) != TYPE_DICTIONARY:
			continue
		var actor_id := String(actor.get("actor_id", "unknown_actor"))
		var marker := Button.new()
		marker.name = "Actor_%s" % actor_id
		marker.text = "@ %s" % actor_id
		marker.position = _array_to_vec2(actor.get("position", [0, 0]))
		marker.size = Vector2(190, 34)
		CrpgTheme.apply_button(marker)
		marker.pressed.connect(_on_actor_pressed.bind(actor_id))
		actor_layer.add_child(marker)
		GameLog.event("actor_placed", {"actor_id": actor_id, "position": _vec2_to_array(marker.position)})

func _place_player_at_entry(entry_id: String) -> void:
	var entries: Dictionary = area_data.get("entry_points", {})
	var chosen_entry := entry_id
	if not entries.has(chosen_entry):
		chosen_entry = String(entries.keys()[0]) if not entries.is_empty() else ""
	if not chosen_entry.is_empty() and entries.has(chosen_entry):
		player_marker.position = _array_to_vec2(entries[chosen_entry])
		move_target = player_marker.position
		has_move_target = false
		GameLog.info("AREA", "Player placed at entry %s" % chosen_entry, {"entry_id": chosen_entry, "position": _vec2_to_array(player_marker.position)})

func _update_player_movement(delta: float) -> void:
	if not has_move_target:
		return
	var offset := move_target - player_marker.position
	var distance := offset.length()
	if distance <= 4.0:
		player_marker.position = move_target
		has_move_target = false
		GameLog.info("MOVE", "Party reached %s" % str(move_target.round()), {"position": _vec2_to_array(move_target)})
		_set_debug("Party reached %s" % str(move_target.round()))
		return
	player_marker.position += offset.normalized() * min(player_speed * delta, distance)

func _on_hotspot_pressed(hotspot: Dictionary) -> void:
	var hotspot_id := String(hotspot.get("id", "unknown"))
	var hotspot_type := String(hotspot.get("type", "inspect"))
	GameLog.info("HOTSPOT", "Clicked %s" % hotspot_id, {"hotspot_id": hotspot_id, "hotspot_type": hotspot_type})
	if hotspot_type == "exit":
		var target_area := String(hotspot.get("target_area", ""))
		var target_entry := String(hotspot.get("target_entry", "south_road"))
		if target_area.is_empty():
			GameLog.error("AREA", "Exit hotspot missing target_area", {"hotspot_id": hotspot_id})
			_set_debug("Exit has no target area: %s" % hotspot_id)
			return
		_set_debug("Travelling: %s -> %s" % [String(hotspot.get("name", "Exit")), target_area])
		GameLog.event("area_exit_selected", {"hotspot_id": hotspot_id, "target_area": target_area, "target_entry": target_entry})
		load_area(target_area, target_entry)
		return

	_set_debug("Inspect: %s\n%s" % [String(hotspot.get("name", "Hotspot")), String(hotspot.get("description", ""))])
	_apply_effects(hotspot.get("effects", []), "hotspot:%s" % hotspot_id)

func _on_actor_pressed(actor_id: String) -> void:
	GameLog.info("ACTOR", "Clicked %s" % actor_id, {"actor_id": actor_id})
	var actor_data: Dictionary = actor_definitions.get(actor_id, {})
	if actor_data.is_empty():
		_set_debug("Actor selected: %s" % actor_id)
		GameLog.warning("ACTOR", "Actor has no definition: %s" % actor_id, {"actor_id": actor_id})
		return
	var dialogue_path := String(actor_data.get("dialogue", ""))
	if dialogue_path.is_empty():
		_set_debug("Actor has no dialogue: %s" % actor_id)
		return
	_start_dialogue(actor_data, dialogue_path)

func _start_dialogue(actor_data: Dictionary, dialogue_path: String) -> void:
	active_dialogue = data_loader.load_json_file(_to_res_path(dialogue_path))
	if active_dialogue.is_empty():
		_set_debug("Failed to load dialogue: %s" % dialogue_path)
		GameLog.error("DIALOGUE", "Failed to load dialogue: %s" % dialogue_path, {"dialogue_path": dialogue_path})
		return
	active_dialogue_node_id = String(active_dialogue.get("start_node", "start"))
	dialogue_speaker_label.text = String(actor_data.get("name", active_dialogue.get("speaker", "Speaker")))
	dialogue_panel.visible = true
	_show_dialogue_node(active_dialogue_node_id)

func _show_dialogue_node(node_id: String) -> void:
	var nodes: Dictionary = active_dialogue.get("nodes", {})
	if not nodes.has(node_id):
		GameLog.error("DIALOGUE", "Dialogue node missing: %s" % node_id, {"node_id": node_id})
		_hide_dialogue()
		return
	active_dialogue_node_id = node_id
	var node: Dictionary = nodes[node_id]
	if not _passes_conditions(node):
		GameLog.warning("DIALOGUE", "Blocked node because conditions failed: %s" % node_id, {"node_id": node_id})
		_hide_dialogue()
		return
	dialogue_text_label.text = String(node.get("text", ""))
	_clear_layer(dialogue_choices_box)
	var choices := _get_visible_choices(node.get("choices", []))
	GameLog.info("DIALOGUE", "Entered node %s" % node_id, {"node_id": node_id, "visible_choice_count": choices.size()})
	_apply_effects(node.get("effects", []), "dialogue:%s" % node_id)

	if choices.is_empty():
		var close_button := Button.new()
		close_button.text = "Continue"
		CrpgTheme.apply_button(close_button)
		close_button.pressed.connect(_hide_dialogue)
		dialogue_choices_box.add_child(close_button)
		return

	for choice in choices:
		var choice_button := Button.new()
		choice_button.text = String(choice.get("text", "..."))
		CrpgTheme.apply_button(choice_button)
		choice_button.pressed.connect(_on_dialogue_choice_pressed.bind(choice))
		dialogue_choices_box.add_child(choice_button)

func _on_dialogue_choice_pressed(choice: Dictionary) -> void:
	if not _passes_conditions(choice):
		GameLog.warning("DIALOGUE_CHOICE", "Choice conditions failed: %s" % String(choice.get("text", "...")), {"choice": choice})
		return
	var next_node := String(choice.get("next", "end"))
	GameLog.info("DIALOGUE_CHOICE", "%s -> %s" % [String(choice.get("text", "...")), next_node], {"choice_text": String(choice.get("text", "...")), "next": next_node})
	if next_node == "end":
		_hide_dialogue()
		return
	_show_dialogue_node(next_node)

func _apply_effects(effects: Variant, source: String) -> void:
	if typeof(effects) != TYPE_ARRAY:
		return
	for effect in effects:
		_apply_effect(effect, source)
	_update_quest_tracker()
	write_debug_state("state_latest.json")

func _apply_effect(effect: Variant, source: String) -> void:
	if typeof(effect) != TYPE_DICTIONARY:
		return
	var effect_type := String(effect.get("type", ""))
	GameLog.event("effect_applied", {"effect_type": effect_type, "source": source, "effect": effect})
	match effect_type:
		"start_quest":
			var quest_id := String(effect.get("quest_id", ""))
			var stage := String(effect.get("stage", "accepted"))
			if not quest_id.is_empty():
				quest_system.start_quest(quest_id, stage)
				game_state.start_quest(quest_id, stage)
				_set_debug("Quest started: %s -> %s" % [quest_id, stage])
		"set_quest_stage":
			var quest_id := String(effect.get("quest_id", ""))
			var stage := String(effect.get("stage", ""))
			if not quest_id.is_empty() and not stage.is_empty():
				quest_system.set_stage(quest_id, stage)
				game_state.set_quest_stage(quest_id, stage)
				_set_debug("Quest updated: %s -> %s" % [quest_id, stage])
		"set_flag":
			var flag_id := String(effect.get("flag_id", ""))
			if not flag_id.is_empty():
				game_state.set_flag(flag_id, bool(effect.get("value", true)))
				_set_debug("Flag set: %s from %s" % [flag_id, source])
		"add_party_member":
			var actor_id := String(effect.get("actor_id", ""))
			if not actor_id.is_empty() and not game_state.party_member_ids.has(actor_id):
				game_state.party_member_ids.append(actor_id)
				GameLog.info("PARTY", "Added party member: %s" % actor_id, {"actor_id": actor_id})
				_set_debug("Companion joined: %s" % actor_id)
		_:
			GameLog.warning("EFFECT", "Unhandled effect: %s" % effect_type, {"source": source, "effect": effect})

func _get_visible_choices(choices: Variant) -> Array:
	var visible: Array = []
	if typeof(choices) != TYPE_ARRAY:
		return visible
	for choice in choices:
		if typeof(choice) == TYPE_DICTIONARY and _passes_conditions(choice):
			visible.append(choice)
	return visible

func _passes_conditions(data: Dictionary) -> bool:
	return _passes_condition_list(data.get("conditions", []))

func _passes_condition_list(conditions: Variant) -> bool:
	if conditions == null:
		return true
	if typeof(conditions) != TYPE_ARRAY:
		GameLog.warning("DIALOGUE", "Conditions field is not a list", {"conditions": conditions})
		return false
	for condition in conditions:
		if not _passes_condition(condition):
			return false
	return true

func _passes_condition(condition: Variant) -> bool:
	if typeof(condition) != TYPE_DICTIONARY:
		return false
	var condition_type := String(condition.get("type", ""))
	match condition_type:
		"flag":
			return game_state.has_flag(String(condition.get("flag_id", ""))) == bool(condition.get("value", true))
		"quest_stage":
			return game_state.get_quest_stage(String(condition.get("quest_id", ""))) == String(condition.get("stage", ""))
		"skill_check":
			return game_state.get_party_skill(String(condition.get("skill_id", ""))) >= int(condition.get("difficulty", 0))
		"attribute_check":
			return game_state.get_player_attribute(String(condition.get("attribute_id", ""))) >= int(condition.get("difficulty", 0))
		"player_tag":
			var tag_id := String(condition.get("tag", ""))
			var expected_tag := bool(condition.get("value", true))
			return game_state.has_player_tag(tag_id) == expected_tag
		"party_member":
			var actor_id := String(condition.get("actor_id", ""))
			var expected := bool(condition.get("value", true))
			return game_state.party_member_ids.has(actor_id) == expected
		"not":
			return not _passes_condition(condition.get("condition", {}))
		"all":
			return _passes_condition_list(condition.get("conditions", []))
		"any":
			for item in condition.get("conditions", []):
				if _passes_condition(item):
					return true
			return false
		_:
			GameLog.warning("DIALOGUE", "Unknown condition type: %s" % condition_type, {"condition": condition})
			return false

func _update_quest_tracker() -> void:
	if quest_tracker_label == null or game_state == null:
		return
	var text := game_state.get_debug_summary()
	if not game_state.party_member_ids.is_empty():
		text += "\nParty:"
		for actor_id in game_state.party_member_ids:
			text += "\n- %s" % actor_id
	quest_tracker_label.text = text

func _hide_dialogue() -> void:
	if dialogue_panel != null:
		dialogue_panel.visible = false
	if not active_dialogue_node_id.is_empty():
		GameLog.info("DIALOGUE", "Closed dialogue", {"last_node": active_dialogue_node_id})
	active_dialogue = {}
	active_dialogue_node_id = ""

func write_debug_state(file_name: String = "state_latest.json") -> void:
	GameLog.write_state_dump(file_name, DebugStateDump.from_area_controller(self))

func run_debug_action(action: Dictionary) -> bool:
	var action_type := String(action.get("type", ""))
	GameLog.info("SCENARIO", "Running action %s" % action_type, {"action": action})
	match action_type:
		"load_area":
			load_area(String(action.get("area_id", area_id)), String(action.get("entry_id", "south_road")))
			return true
		"click_actor":
			_on_actor_pressed(String(action.get("actor_id", "")))
			return true
		"choose_dialogue":
			return choose_dialogue_by_text(String(action.get("text", "")))
		"click_hotspot":
			return click_hotspot_by_id(String(action.get("hotspot_id", "")))
		"assert_area":
			return _assert_equal("Area", String(action.get("area_id", "")), area_id)
		"assert_quest_stage":
			return _assert_equal("Quest stage", String(action.get("stage", "")), game_state.get_quest_stage(String(action.get("quest_id", ""))))
		"assert_flag":
			var flag_id := String(action.get("flag_id", ""))
			var expected_flag := bool(action.get("value", true))
			var actual_flag := game_state.has_flag(flag_id)
			if actual_flag != expected_flag:
				GameLog.error("ASSERT", "Flag mismatch: %s expected %s got %s" % [flag_id, expected_flag, actual_flag])
				return false
			return true
		"assert_party_member":
			var actor_id := String(action.get("actor_id", ""))
			if not game_state.party_member_ids.has(actor_id):
				GameLog.error("ASSERT", "Party member missing: %s" % actor_id)
				return false
			return true
		"assert_player_tag":
			var tag_id := String(action.get("tag", ""))
			var expected_tag := bool(action.get("value", true))
			var actual_tag := game_state.has_player_tag(tag_id)
			if actual_tag != expected_tag:
				GameLog.error("ASSERT", "Player tag mismatch: %s expected %s got %s" % [tag_id, expected_tag, actual_tag])
				return false
			return true
		_:
			GameLog.error("SCENARIO", "Unknown action type: %s" % action_type, {"action": action})
			return false

func _assert_equal(label: String, expected: String, actual: String) -> bool:
	if expected != actual:
		GameLog.error("ASSERT", "%s mismatch: expected %s got %s" % [label, expected, actual])
		return false
	GameLog.info("ASSERT", "%s OK: %s" % [label, expected])
	return true

func choose_dialogue_by_text(choice_text: String) -> bool:
	var nodes: Dictionary = active_dialogue.get("nodes", {})
	if active_dialogue_node_id.is_empty() or not nodes.has(active_dialogue_node_id):
		GameLog.error("SCENARIO", "No active dialogue node for choice: %s" % choice_text)
		return false
	var node: Dictionary = nodes[active_dialogue_node_id]
	for choice in _get_visible_choices(node.get("choices", [])):
		if String(choice.get("text", "")) == choice_text:
			_on_dialogue_choice_pressed(choice)
			return true
	GameLog.error("SCENARIO", "Visible choice text not found: %s" % choice_text, {"node_id": active_dialogue_node_id})
	return false

func click_hotspot_by_id(hotspot_id: String) -> bool:
	for hotspot in hotspots_data.get("hotspots", []):
		if typeof(hotspot) == TYPE_DICTIONARY and String(hotspot.get("id", "")) == hotspot_id:
			_on_hotspot_pressed(hotspot)
			return true
	GameLog.error("SCENARIO", "Hotspot not found: %s" % hotspot_id)
	return false

func _set_debug(text: String) -> void:
	if debug_label != null:
		debug_label.text = text
	GameLog.info("DEBUG", text)

func _clear_layer(layer: Node) -> void:
	for child in layer.get_children():
		child.queue_free()

func _to_res_path(path: String) -> String:
	if path.is_empty():
		return ""
	if path.begins_with("res://"):
		return path
	return "res://%s" % path

func _array_to_vec2(value: Variant) -> Vector2:
	if typeof(value) == TYPE_ARRAY and value.size() >= 2:
		return Vector2(float(value[0]), float(value[1]))
	return Vector2.ZERO

func _vec2_to_array(value: Vector2) -> Array:
	return [value.x, value.y]
