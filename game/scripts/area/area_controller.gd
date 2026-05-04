extends Node2D
class_name AreaController

const DataLoader = preload("res://game/scripts/core/data_loader.gd")
const GameState = preload("res://game/scripts/core/game_state.gd")
const QuestSystem = preload("res://game/scripts/systems/quest_system.gd")
const CrpgTheme = preload("res://game/scripts/ui/crpg_theme.gd")

@export var area_id: String = "wolfpine_road"
@export var player_speed: float = 260.0

var data_loader: DataLoader
var game_state: GameState
var quest_system: QuestSystem
var area_data: Dictionary = {}
var hotspots_data: Dictionary = {}
var actors_data: Dictionary = {}
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
	data_loader = DataLoader.new()
	game_state = GameState.new()
	quest_system = QuestSystem.new()
	_build_runtime_nodes()
	load_area(area_id)
	_update_quest_tracker()

func _process(delta: float) -> void:
	_update_player_movement(delta)

func _unhandled_input(event: InputEvent) -> void:
	if event is InputEventMouseButton and event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
		if dialogue_panel != null and dialogue_panel.visible:
			return
		move_target = event.position
		has_move_target = true
		_set_debug("Moving to %s" % str(move_target.round()))

func _build_runtime_nodes() -> void:
	background_layer = ColorRect.new()
	background_layer.name = "PlaceholderBackground"
	background_layer.color = Color(0.035, 0.045, 0.035, 1.0)
	background_layer.position = Vector2.ZERO
	background_layer.size = Vector2(1280, 720)
	add_child(background_layer)

	label_layer = Node2D.new()
	label_layer.name = "LabelLayer"
	add_child(label_layer)

	hotspot_layer = Node2D.new()
	hotspot_layer.name = "HotspotLayer"
	add_child(hotspot_layer)

	actor_layer = Node2D.new()
	actor_layer.name = "ActorLayer"
	add_child(actor_layer)

	player_marker = Label.new()
	player_marker.name = "PlayerMarker"
	player_marker.text = "◆ party"
	player_marker.position = Vector2(180, 540)
	player_marker.add_theme_font_size_override("font_size", 18)
	CrpgTheme.apply_label(player_marker, true)
	add_child(player_marker)

	debug_label = Label.new()
	debug_label.name = "DebugLabel"
	debug_label.position = Vector2(24, 24)
	debug_label.custom_minimum_size = Vector2(620, 80)
	debug_label.text = "NG area prototype"
	CrpgTheme.apply_label(debug_label)
	add_child(debug_label)

	_build_quest_panel()
	_build_dialogue_panel()

func _build_quest_panel() -> void:
	quest_panel = PanelContainer.new()
	quest_panel.name = "QuestPanel"
	quest_panel.position = Vector2(900, 24)
	quest_panel.size = Vector2(340, 140)
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
	dialogue_panel.position = Vector2(24, 430)
	dialogue_panel.size = Vector2(760, 260)
	dialogue_panel.visible = false
	CrpgTheme.apply_panel(dialogue_panel)
	add_child(dialogue_panel)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 14)
	margin.add_theme_constant_override("margin_top", 12)
	margin.add_theme_constant_override("margin_right", 14)
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
	dialogue_text_label.custom_minimum_size = Vector2(720, 92)
	dialogue_text_label.fit_content = true
	dialogue_text_label.scroll_active = false
	CrpgTheme.apply_rich_text(dialogue_text_label)
	root.add_child(dialogue_text_label)

	dialogue_choices_box = VBoxContainer.new()
	dialogue_choices_box.name = "Choices"
	dialogue_choices_box.add_theme_constant_override("separation", 4)
	root.add_child(dialogue_choices_box)

func load_area(next_area_id: String) -> void:
	area_id = next_area_id
	var area_path := "res://areas/%s/area.json" % area_id
	area_data = data_loader.load_json_file(area_path)
	if area_data.is_empty():
		_set_debug("Failed to load area: %s" % area_id)
		return

	hotspots_data = data_loader.load_json_file(_to_res_path(String(area_data.get("hotspots", ""))))
	actors_data = data_loader.load_json_file(_to_res_path(String(area_data.get("actors", ""))))
	actor_definitions = _load_actor_definitions()
	_render_area()

func _load_actor_definitions() -> Dictionary:
	var result := {}
	var paths := [
		"res://data/actors/npcs/captain_renna.json",
		"res://data/actors/companions/brannoc.json",
		"res://data/actors/enemies/border_bandit.json"
	]
	for path in paths:
		var actor_data := data_loader.load_json_file(path)
		var actor_id := String(actor_data.get("id", ""))
		if not actor_id.is_empty():
			result[actor_id] = actor_data
	return result

func _render_area() -> void:
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
	_place_player_at_entry("south_road")

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
		var pos := _array_to_vec2(hotspot.get("position", [0, 0]))
		marker.position = pos
		marker.size = Vector2(180, 34)
		CrpgTheme.apply_button(marker)
		marker.pressed.connect(_on_hotspot_pressed.bind(hotspot))
		hotspot_layer.add_child(marker)

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

func _place_player_at_entry(entry_id: String) -> void:
	var entries: Dictionary = area_data.get("entry_points", {})
	if entries.has(entry_id):
		player_marker.position = _array_to_vec2(entries[entry_id])
		move_target = player_marker.position
		has_move_target = false

func _update_player_movement(delta: float) -> void:
	if not has_move_target:
		return
	var current := player_marker.position
	var offset := move_target - current
	var distance := offset.length()
	if distance <= 4.0:
		player_marker.position = move_target
		has_move_target = false
		_set_debug("Party reached %s" % str(move_target.round()))
		return
	player_marker.position = current + offset.normalized() * min(player_speed * delta, distance)

func _on_hotspot_pressed(hotspot: Dictionary) -> void:
	var hotspot_type := String(hotspot.get("type", "inspect"))
	if hotspot_type == "exit":
		var target_area := String(hotspot.get("target_area", ""))
		_set_debug("Exit hotspot selected: %s -> %s" % [String(hotspot.get("name", "Exit")), target_area])
	else:
		_set_debug("Inspect: %s\n%s" % [String(hotspot.get("name", "Hotspot")), String(hotspot.get("description", ""))])
		_apply_effects(hotspot.get("effects", []), "hotspot:%s" % String(hotspot.get("id", "unknown")))

func _on_actor_pressed(actor_id: String) -> void:
	var actor_data: Dictionary = actor_definitions.get(actor_id, {})
	if actor_data.is_empty():
		_set_debug("Actor selected: %s" % actor_id)
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
		return
	active_dialogue_node_id = String(active_dialogue.get("start_node", "start"))
	dialogue_speaker_label.text = String(actor_data.get("name", active_dialogue.get("speaker", "Speaker")))
	dialogue_panel.visible = true
	_show_dialogue_node(active_dialogue_node_id)

func _show_dialogue_node(node_id: String) -> void:
	var nodes: Dictionary = active_dialogue.get("nodes", {})
	if not nodes.has(node_id):
		_set_debug("Dialogue node missing: %s" % node_id)
		_hide_dialogue()
		return
	active_dialogue_node_id = node_id
	var node: Dictionary = nodes[node_id]
	dialogue_text_label.text = String(node.get("text", ""))
	_clear_layer(dialogue_choices_box)
	_apply_effects(node.get("effects", []), "dialogue:%s" % node_id)

	var choices: Array = node.get("choices", [])
	if choices.is_empty():
		var close_button := Button.new()
		close_button.text = "Continue"
		CrpgTheme.apply_button(close_button)
		close_button.pressed.connect(_hide_dialogue)
		dialogue_choices_box.add_child(close_button)
		return

	for choice in choices:
		if typeof(choice) != TYPE_DICTIONARY:
			continue
		var choice_button := Button.new()
		choice_button.text = String(choice.get("text", "..."))
		CrpgTheme.apply_button(choice_button)
		choice_button.pressed.connect(_on_dialogue_choice_pressed.bind(choice))
		dialogue_choices_box.add_child(choice_button)

func _on_dialogue_choice_pressed(choice: Dictionary) -> void:
	var next_node := String(choice.get("next", "end"))
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

func _apply_effect(effect: Variant, source: String) -> void:
	if typeof(effect) != TYPE_DICTIONARY:
		return
	var effect_type := String(effect.get("type", ""))
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
		_:
			_set_debug("Unhandled effect: %s from %s" % [effect_type, source])

func _update_quest_tracker() -> void:
	if quest_tracker_label != null and game_state != null:
		quest_tracker_label.text = game_state.get_debug_summary()

func _hide_dialogue() -> void:
	if dialogue_panel != null:
		dialogue_panel.visible = false
	active_dialogue = {}
	active_dialogue_node_id = ""

func _set_debug(text: String) -> void:
	if debug_label != null:
		debug_label.text = text
	print(text)

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
