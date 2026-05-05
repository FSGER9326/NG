extends Node2D

const DataLoader = preload("res://game/scripts/core/data_loader.gd")
const AreaScene = preload("res://game/scenes/area/area_scene.tscn")
const CrpgTheme = preload("res://game/scripts/ui/crpg_theme.gd")
const GameLog = preload("res://game/scripts/core/game_log.gd")
const SaveSystem = preload("res://game/scripts/core/save_system.gd")
const CharacterProfileBuilder = preload("res://game/scripts/character/character_profile_builder.gd")

const CHARACTER_CREATION_PATH := "res://data/character_creation/character_creation.json"

var data_loader: DataLoader
var save_system: SaveSystem
var current_area: Node2D
var menu_root: Control
var character_creator_root: Control
var character_name_edit: LineEdit
var ancestry_options: OptionButton
var origin_options: OptionButton
var archetype_options: OptionButton
var trait_options: OptionButton
var compatibility_warning_label: Label
var start_journey_button: Button
var character_creation_data: Dictionary = {}
var player_profile: Dictionary = {
	"name": "Wanderer",
	"origin": "Border Drifter",
	"archetype": "Mercenary",
	"ancestry": "Border Human",
	"trait": "Steady Under Fire",
	"tags": []
}

func _ready() -> void:
	GameLog.start_session("main_menu")
	GameLog.info("BOOT", "NG booting")
	data_loader = DataLoader.new()
	save_system = SaveSystem.new()
	var load_result := data_loader.load_bootstrap_data()
	character_creation_data = data_loader.load_json_file(CHARACTER_CREATION_PATH)
	GameLog.info("BOOT", "Loaded bootstrap data", {"keys": load_result.keys(), "has_character_creation": not character_creation_data.is_empty()})
	_show_main_menu()

func _show_main_menu() -> void:
	_clear_current_screen()
	menu_root = _make_fullscreen_control("MainMenu")
	add_child(menu_root)

	var background := ColorRect.new()
	background.name = "MenuBackground"
	background.color = Color(0.025, 0.028, 0.024, 1.0)
	background.position = Vector2.ZERO
	background.size = menu_root.size
	menu_root.add_child(background)

	var panel := PanelContainer.new()
	panel.name = "MenuPanel"
	panel.position = Vector2(410, 120)
	panel.size = Vector2(460, 460)
	CrpgTheme.apply_panel(panel)
	menu_root.add_child(panel)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_top", 22)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_bottom", 22)
	panel.add_child(margin)

	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 12)
	margin.add_child(root)

	var title := Label.new()
	title.text = "NG"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	CrpgTheme.apply_label(title, true)
	title.add_theme_font_size_override("font_size", 34)
	root.add_child(title)

	var subtitle := Label.new()
	subtitle.text = "A low-fantasy party CRPG prototype"
	subtitle.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	CrpgTheme.apply_label(subtitle)
	root.add_child(subtitle)

	root.add_child(_spacer(18))
	root.add_child(_make_menu_button("New Game", _show_character_creator))
	var load_button := _make_menu_button("Load Game", _on_load_game_pressed)
	load_button.disabled = not save_system.has_save()
	root.add_child(load_button)
	var save_button := _make_menu_button("Save Game (available in-game)", _on_save_game_pressed)
	save_button.disabled = true
	root.add_child(save_button)
	root.add_child(_make_menu_button("Quit", _on_quit_pressed))

	root.add_child(_spacer(14))
	var note := Label.new()
	note.text = "Current build: Wolfpine Road vertical-slice prototype"
	note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	CrpgTheme.apply_label(note)
	root.add_child(note)
	GameLog.info("MENU", "Main menu shown", {"has_save": save_system.has_save()})

func _show_character_creator() -> void:
	_clear_current_screen()
	character_creator_root = _make_fullscreen_control("CharacterCreator")
	add_child(character_creator_root)

	var background := ColorRect.new()
	background.name = "CreatorBackground"
	background.color = Color(0.026, 0.030, 0.026, 1.0)
	background.position = Vector2.ZERO
	background.size = character_creator_root.size
	character_creator_root.add_child(background)

	var panel := PanelContainer.new()
	panel.name = "CreatorPanel"
	panel.position = Vector2(300, 28)
	panel.size = Vector2(680, 675)
	CrpgTheme.apply_panel(panel)
	character_creator_root.add_child(panel)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_top", 22)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_bottom", 22)
	panel.add_child(margin)

	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 8)
	margin.add_child(root)

	var title := Label.new()
	title.text = "Create Your Character"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	CrpgTheme.apply_label(title, true)
	title.add_theme_font_size_override("font_size", 26)
	root.add_child(title)

	var intro := Label.new()
	intro.text = "Choose a name, ancestry, background, class, and trait. These choices build tags for passive checks and NPC reactions."
	intro.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	CrpgTheme.apply_label(intro)
	root.add_child(intro)

	root.add_child(_spacer(6))
	root.add_child(_make_form_label("Name"))

	character_name_edit = LineEdit.new()
	character_name_edit.name = "CharacterName"
	character_name_edit.text = String(player_profile.get("name", "Wanderer"))
	root.add_child(character_name_edit)

	root.add_child(_make_form_label("Ancestry"))
	ancestry_options = OptionButton.new()
	ancestry_options.name = "AncestryOptions"
	_populate_option_button(ancestry_options, character_creation_data.get("ancestries", []), ["Border Human"])
	_select_option_by_text(ancestry_options, String(player_profile.get("ancestry", "Border Human")), "ancestry")
	ancestry_options.item_selected.connect(_on_creator_selection_changed)
	root.add_child(ancestry_options)

	root.add_child(_make_form_label("Background"))
	origin_options = OptionButton.new()
	origin_options.name = "OriginOptions"
	_populate_option_button(origin_options, character_creation_data.get("backgrounds", []), ["Border Drifter", "Failed Squire", "Village Outcast", "Caravan Guard"])
	_select_option_by_text(origin_options, String(player_profile.get("origin", "Border Drifter")), "origin")
	origin_options.item_selected.connect(_on_creator_selection_changed)
	root.add_child(origin_options)

	root.add_child(_make_form_label("Class"))
	archetype_options = OptionButton.new()
	archetype_options.name = "ArchetypeOptions"
	_populate_option_button(archetype_options, character_creation_data.get("classes", []), ["Mercenary", "Scout", "Hedge Knight", "Cunning Speaker"])
	_select_option_by_text(archetype_options, String(player_profile.get("archetype", "Mercenary")), "archetype")
	archetype_options.item_selected.connect(_on_creator_selection_changed)
	root.add_child(archetype_options)

	root.add_child(_make_form_label("Trait"))
	trait_options = OptionButton.new()
	trait_options.name = "TraitOptions"
	_populate_option_button(trait_options, character_creation_data.get("traits", []), ["Steady Under Fire"])
	_select_option_by_text(trait_options, String(player_profile.get("trait", "Steady Under Fire")), "trait")
	trait_options.item_selected.connect(_on_creator_selection_changed)
	root.add_child(trait_options)

	compatibility_warning_label = Label.new()
	compatibility_warning_label.name = "CompatibilityWarning"
	compatibility_warning_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	compatibility_warning_label.custom_minimum_size = Vector2(620, 56)
	CrpgTheme.apply_label(compatibility_warning_label)
	root.add_child(compatibility_warning_label)

	root.add_child(_spacer(8))
	var buttons := HBoxContainer.new()
	buttons.add_theme_constant_override("separation", 10)
	root.add_child(buttons)

	var back_button := Button.new()
	back_button.text = "Back"
	CrpgTheme.apply_button(back_button)
	back_button.pressed.connect(_show_main_menu)
	buttons.add_child(back_button)

	start_journey_button = Button.new()
	start_journey_button.text = "Start Journey"
	CrpgTheme.apply_button(start_journey_button)
	start_journey_button.pressed.connect(_start_new_game_from_creator.bind(character_name_edit, ancestry_options, origin_options, archetype_options, trait_options))
	buttons.add_child(start_journey_button)
	_refresh_trait_options(String(player_profile.get("trait", "Steady Under Fire")))
	_update_creator_compatibility()
	GameLog.info("MENU", "Character creator shown")

func _start_new_game_from_creator(name_edit: LineEdit, selected_ancestry_options: OptionButton, selected_origin_options: OptionButton, selected_archetype_options: OptionButton, selected_trait_options: OptionButton) -> void:
	var character_name := name_edit.text.strip_edges()
	if character_name.is_empty():
		character_name = "Wanderer"
	var ancestry_name := selected_ancestry_options.get_item_text(selected_ancestry_options.selected)
	var background_name := selected_origin_options.get_item_text(selected_origin_options.selected)
	var archetype_name := selected_archetype_options.get_item_text(selected_archetype_options.selected)
	var trait_name := selected_trait_options.get_item_text(selected_trait_options.selected)
	var built_profile := _build_player_profile(character_name, ancestry_name, background_name, archetype_name, trait_name)
	var warnings: Array = built_profile.get("compatibility_warnings", [])
	if not warnings.is_empty():
		_show_creator_warnings(warnings)
		GameLog.warning("CHARACTER", "Blocked incompatible player profile", {"warnings": warnings, "profile": built_profile})
		return
	player_profile = built_profile
	GameLog.info("CHARACTER", "Created player profile", player_profile)
	_start_game()

func _build_player_profile(character_name: String, ancestry_name: String, background_name: String, archetype_name: String, trait_name: String) -> Dictionary:
	if character_creation_data.is_empty():
		return {
			"name": character_name,
			"ancestry": ancestry_name,
			"origin": background_name,
			"archetype": archetype_name,
			"background": background_name,
			"class": archetype_name,
			"trait": trait_name,
			"tags": [],
			"compatibility_warnings": []
		}
	var ancestry := _find_option_by_name(character_creation_data.get("ancestries", []), ancestry_name)
	var background := _find_option_by_name(character_creation_data.get("backgrounds", []), background_name)
	var character_class := _find_option_by_name(character_creation_data.get("classes", []), archetype_name)
	var trait_data := _find_option_by_name(character_creation_data.get("traits", []), trait_name)
	return CharacterProfileBuilder.build_profile(character_name, ancestry, background, character_class, trait_data, character_creation_data)

func _update_creator_compatibility(_selected_index: int = -1) -> void:
	if compatibility_warning_label == null or start_journey_button == null:
		return
	if ancestry_options == null or origin_options == null or archetype_options == null or trait_options == null:
		return
	var preview_name := character_name_edit.text.strip_edges() if character_name_edit != null else "Wanderer"
	if preview_name.is_empty():
		preview_name = "Wanderer"
	var preview_profile := _build_player_profile(
		preview_name,
		ancestry_options.get_item_text(ancestry_options.selected),
		origin_options.get_item_text(origin_options.selected),
		archetype_options.get_item_text(archetype_options.selected),
		trait_options.get_item_text(trait_options.selected)
	)
	var warnings: Array = preview_profile.get("compatibility_warnings", [])
	if warnings.is_empty():
		var unavailable_trait_explanations := _get_unavailable_trait_explanations()
		if unavailable_trait_explanations.is_empty():
			compatibility_warning_label.text = "Theme check: coherent."
		else:
			compatibility_warning_label.text = "Theme check: coherent.\nUnavailable traits for this build:\n- %s" % "\n- ".join(unavailable_trait_explanations)
		start_journey_button.disabled = false
	else:
		_show_creator_warnings(warnings)

func _show_creator_warnings(warnings: Array) -> void:
	if compatibility_warning_label != null:
		compatibility_warning_label.text = "Theme conflict:\n- %s" % "\n- ".join(warnings)
	if start_journey_button != null:
		start_journey_button.disabled = true

func _on_creator_selection_changed(_selected_index: int = -1) -> void:
	_refresh_trait_options(_get_selected_option_text(trait_options))
	_update_creator_compatibility(_selected_index)

func _refresh_trait_options(preferred_trait: String = "") -> void:
	if trait_options == null:
		return
	var traits: Array = character_creation_data.get("traits", [])
	if traits.is_empty():
		return
	var wanted_trait := preferred_trait
	if wanted_trait.is_empty():
		wanted_trait = _get_selected_option_text(trait_options)
	trait_options.clear()
	var base_tags := _collect_creator_base_tags()
	var first_enabled_index := -1
	var preferred_index := -1
	for trait_data in traits:
		if typeof(trait_data) != TYPE_DICTIONARY:
			continue
		var trait_name := String(trait_data.get("name", "Unnamed"))
		var index := trait_options.get_item_count()
		trait_options.add_item(trait_name)
		var is_available := CharacterProfileBuilder.is_item_available(base_tags, trait_data)
		trait_options.set_item_disabled(index, not is_available)
		if is_available and first_enabled_index == -1:
			first_enabled_index = index
		if is_available and trait_name == wanted_trait:
			preferred_index = index
	if preferred_index != -1:
		trait_options.select(preferred_index)
	elif first_enabled_index != -1:
		trait_options.select(first_enabled_index)
	elif trait_options.get_item_count() > 0:
		trait_options.select(0)

func _collect_creator_base_tags() -> Array:
	var tags: Array = []
	if character_creation_data.is_empty() or ancestry_options == null or origin_options == null or archetype_options == null:
		return tags
	var ancestry := _find_option_by_name(character_creation_data.get("ancestries", []), _get_selected_option_text(ancestry_options))
	var background := _find_option_by_name(character_creation_data.get("backgrounds", []), _get_selected_option_text(origin_options))
	var character_class := _find_option_by_name(character_creation_data.get("classes", []), _get_selected_option_text(archetype_options))
	for item in [ancestry, background, character_class]:
		for tag in item.get("tags", []):
			var tag_id := String(tag)
			if not tag_id.is_empty() and not tags.has(tag_id):
				tags.append(tag_id)
	return tags

func _get_unavailable_trait_explanations() -> Array[String]:
	var result: Array[String] = []
	if character_creation_data.is_empty():
		return result
	var traits: Array = character_creation_data.get("traits", [])
	if traits.is_empty():
		return result
	var base_tags := _collect_creator_base_tags()
	for trait_data in traits:
		if typeof(trait_data) != TYPE_DICTIONARY:
			continue
		var reasons := CharacterProfileBuilder.get_item_unavailable_reasons(base_tags, trait_data)
		if not reasons.is_empty():
			result.append(" ".join(reasons))
	return result

func _start_game() -> void:
	_clear_current_screen()
	GameLog.info("GAME", "Instantiating area scene", {"scene": "res://game/scenes/area/area_scene.tscn"})
	current_area = AreaScene.instantiate()
	if current_area == null:
		GameLog.error("GAME", "Failed to instantiate area scene")
		return
	current_area.name = "CurrentArea"
	if current_area.has_method("setup_player_profile"):
		current_area.setup_player_profile(player_profile)
	add_child(current_area)
	GameLog.info("AREA", "Area loaded", {"area_id": String(current_area.get("area_id")), "source": "new_game"})
	if current_area.has_method("write_debug_state"):
		current_area.write_debug_state("state_latest.json")
	GameLog.info("GAME", "Started new game", {"player_profile": player_profile, "area_id": String(current_area.get("area_id"))})

func _start_game_from_save(save_data: Dictionary) -> bool:
	if save_data.is_empty():
		GameLog.error("SAVE", "Cannot start game from empty save data")
		return false
	_clear_current_screen()
	player_profile = _dictionary_from(save_data.get("player_profile", player_profile))
	GameLog.info("SAVE", "Instantiating area scene from save", {"area_id": String(save_data.get("area_id", ""))})
	current_area = AreaScene.instantiate()
	if current_area == null:
		GameLog.error("SAVE", "Failed to instantiate area scene from save")
		return false
	current_area.name = "CurrentArea"
	if current_area.has_method("setup_player_profile"):
		current_area.setup_player_profile(player_profile)
	add_child(current_area)
	_apply_save_to_current_area(save_data)
	GameLog.info("AREA", "Area loaded", {"area_id": String(current_area.get("area_id")), "source": "save"})
	GameLog.info("SAVE", "Started game from save", {"player_profile": player_profile, "area_id": String(save_data.get("area_id", ""))})
	return true

func _build_save_data() -> Dictionary:
	var save_data := {
		"player_profile": player_profile.duplicate(true),
		"area_id": "",
		"player_position": [],
		"game_state": {}
	}
	if current_area == null:
		return save_data
	save_data["area_id"] = String(current_area.get("area_id"))
	var player_marker: Node = current_area.get("player_marker")
	if player_marker != null and player_marker is Node2D:
		save_data["player_position"] = _vec2_to_array((player_marker as Node2D).position)
	var area_game_state = current_area.get("game_state")
	if area_game_state != null and area_game_state.has_method("to_debug_dict"):
		save_data["game_state"] = area_game_state.to_debug_dict()
	return save_data

func _apply_save_to_current_area(save_data: Dictionary) -> void:
	if current_area == null:
		return
	var target_area_id := String(save_data.get("area_id", "wolfpine_road"))
	if target_area_id.is_empty():
		target_area_id = "wolfpine_road"
	if current_area.has_method("load_area"):
		current_area.load_area(target_area_id, "south_road")
	var area_game_state = current_area.get("game_state")
	var game_state_data := _dictionary_from(save_data.get("game_state", {}))
	if area_game_state != null and area_game_state.has_method("apply_save_data"):
		area_game_state.apply_save_data(game_state_data)
	elif area_game_state != null and area_game_state.has_method("apply_player_profile"):
		area_game_state.apply_player_profile(player_profile)
	var quest_system = current_area.get("quest_system")
	if quest_system != null:
		quest_system.quest_states = _dictionary_from(game_state_data.get("quest_stages", {}))
	var player_marker: Node = current_area.get("player_marker")
	var player_position := _array_to_vec2(save_data.get("player_position", []))
	if player_marker != null and player_marker is Node2D and player_position != Vector2.ZERO:
		(player_marker as Node2D).position = player_position
		current_area.set("move_target", player_position)
		current_area.set("has_move_target", false)
	if current_area.has_method("_update_quest_tracker"):
		current_area.call("_update_quest_tracker")
	if current_area.has_method("write_debug_state"):
		current_area.write_debug_state("state_latest.json")

func run_debug_action(action: Dictionary) -> bool:
	var action_type := String(action.get("type", ""))
	GameLog.info("SCENARIO", "Running main action %s" % action_type, {"action": action})
	match action_type:
		"assert_screen":
			return _assert_screen(String(action.get("screen", "")))
		"press_menu":
			return _press_menu_button(String(action.get("button", "")))
		"save_game":
			return _save_game()
		"load_game":
			return _load_game()
		"set_character_name":
			if character_name_edit == null:
				GameLog.error("SCENARIO", "Cannot set character name; creator is not open")
				return false
			character_name_edit.text = String(action.get("name", "Wanderer"))
			return true
		"select_ancestry":
			var ancestry_ok := _select_option_by_text(ancestry_options, String(action.get("ancestry", "")), "ancestry")
			_refresh_trait_options(_get_selected_option_text(trait_options))
			_update_creator_compatibility()
			return ancestry_ok
		"select_origin":
			var origin_ok := _select_option_by_text(origin_options, String(action.get("origin", "")), "origin")
			_refresh_trait_options(_get_selected_option_text(trait_options))
			_update_creator_compatibility()
			return origin_ok
		"select_archetype":
			var archetype_ok := _select_option_by_text(archetype_options, String(action.get("archetype", "")), "archetype")
			_refresh_trait_options(_get_selected_option_text(trait_options))
			_update_creator_compatibility()
			return archetype_ok
		"select_trait":
			var trait_ok := _select_option_by_text(trait_options, String(action.get("trait", "")), "trait")
			_update_creator_compatibility()
			return trait_ok
		"assert_trait_available":
			return _assert_trait_availability(String(action.get("trait", "")), true)
		"assert_trait_unavailable":
			return _assert_trait_availability(String(action.get("trait", "")), false)
		"assert_creator_warning_contains":
			return _assert_creator_warning_contains(String(action.get("text", "")))
		"assert_player_profile":
			return _assert_player_profile(action)
		"assert_area":
			return _assert_area(String(action.get("area_id", "")))
		_:
			if current_area == null:
				_start_game()
			if current_area != null and current_area.has_method("run_debug_action"):
				return current_area.run_debug_action(action)
			GameLog.error("SCENARIO", "Unknown main action type: %s" % action_type, {"action": action})
			return false

func _press_menu_button(button: String) -> bool:
	if button == "new_game":
		_show_character_creator()
		return true
	if button == "start_journey":
		if character_name_edit == null or ancestry_options == null or origin_options == null or archetype_options == null or trait_options == null:
			GameLog.error("ASSERT", "Cannot start journey; character creator controls are missing")
			return false
		_start_new_game_from_creator(character_name_edit, ancestry_options, origin_options, archetype_options, trait_options)
		return true
	if button == "load_game":
		return _load_game()
	GameLog.error("SCENARIO", "Unknown menu button: %s" % button, {"button": button})
	return false

func write_debug_state(file_name: String = "state_latest.json") -> void:
	var state_data := {
		"screen": _get_current_screen(),
		"player_profile": player_profile.duplicate(true),
		"has_current_area": current_area != null,
		"current_area_id": String(current_area.get("area_id")) if current_area != null else "",
		"has_save": save_system.has_save() if save_system != null else false
	}
	GameLog.write_state_dump(file_name, state_data)

func _save_game() -> bool:
	if current_area == null:
		GameLog.warning("SAVE", "Cannot save without an active area")
		return false
	return save_system.write_save(_build_save_data())

func _load_game() -> bool:
	var save_data := save_system.read_save()
	if save_data.is_empty():
		return false
	return _start_game_from_save(save_data)

func _assert_screen(expected_screen: String) -> bool:
	var actual_screen := _get_current_screen()
	if actual_screen != expected_screen:
		GameLog.error("ASSERT", "Screen mismatch: expected %s got %s" % [expected_screen, actual_screen], {"expected": expected_screen, "actual": actual_screen})
		return false
	GameLog.info("ASSERT", "Screen OK: %s" % expected_screen)
	return true

func _assert_area(expected_area: String) -> bool:
	if current_area == null:
		GameLog.error("ASSERT", "No current area is loaded")
		return false
	var actual_area := String(current_area.get("area_id"))
	if actual_area != expected_area:
		GameLog.error("ASSERT", "Area mismatch: expected %s got %s" % [expected_area, actual_area], {"expected": expected_area, "actual": actual_area})
		return false
	GameLog.info("ASSERT", "Area OK: %s" % expected_area)
	return true

func _assert_creator_warning_contains(expected_text: String) -> bool:
	if compatibility_warning_label == null:
		GameLog.error("ASSERT", "Creator warning label is missing")
		return false
	var actual_text := compatibility_warning_label.text
	if not actual_text.contains(expected_text):
		GameLog.error("ASSERT", "Creator warning mismatch: expected text containing %s got %s" % [expected_text, actual_text], {"expected": expected_text, "actual": actual_text})
		return false
	GameLog.info("ASSERT", "Creator warning contains: %s" % expected_text)
	return true

func _assert_trait_availability(trait_name: String, expected_available: bool) -> bool:
	if trait_options == null:
		GameLog.error("ASSERT", "Trait options are missing")
		return false
	for index in range(trait_options.get_item_count()):
		if trait_options.get_item_text(index) == trait_name:
			var actual_available := not trait_options.is_item_disabled(index)
			if actual_available != expected_available:
				GameLog.error("ASSERT", "Trait availability mismatch for %s: expected %s got %s" % [trait_name, expected_available, actual_available])
				return false
			GameLog.info("ASSERT", "Trait availability OK: %s -> %s" % [trait_name, actual_available])
			return true
	GameLog.error("ASSERT", "Trait option not found: %s" % trait_name)
	return false

func _get_current_screen() -> String:
	if current_area != null:
		return "game"
	if character_creator_root != null:
		return "character_creator"
	if menu_root != null:
		return "main_menu"
	return "unknown"

func _assert_player_profile(action: Dictionary) -> bool:
	for key in ["name", "ancestry", "origin", "archetype", "background", "class", "trait"]:
		if action.has(key):
			var expected := String(action[key])
			var actual := String(player_profile.get(key, ""))
			if actual != expected:
				GameLog.error("ASSERT", "Player profile mismatch for %s: expected %s got %s" % [key, expected, actual], {"key": key, "expected": expected, "actual": actual})
				return false
	if action.has("tag") and not player_profile.get("tags", []).has(String(action.get("tag", ""))):
		GameLog.error("ASSERT", "Player profile missing tag: %s" % String(action.get("tag", "")), {"player_profile": player_profile})
		return false
	GameLog.info("ASSERT", "Player profile OK", {"player_profile": player_profile})
	return true

func _select_option_by_text(option_button: OptionButton, text: String, label: String) -> bool:
	if option_button == null:
		GameLog.error("SCENARIO", "Cannot select %s; control is missing" % label)
		return false
	for index in range(option_button.get_item_count()):
		if option_button.get_item_text(index) == text:
			if option_button.is_item_disabled(index):
				GameLog.warning("SCENARIO", "Cannot select disabled %s option: %s" % [label, text])
				return false
			option_button.select(index)
			GameLog.info("SCENARIO", "Selected %s: %s" % [label, text])
			return true
	GameLog.error("SCENARIO", "Could not find %s option: %s" % [label, text])
	return false

func _get_selected_option_text(option_button: OptionButton) -> String:
	if option_button == null or option_button.get_item_count() == 0:
		return ""
	return option_button.get_item_text(option_button.selected)

func _populate_option_button(option_button: OptionButton, data_items: Variant, fallback_names: Array) -> void:
	if typeof(data_items) == TYPE_ARRAY and not data_items.is_empty():
		for item in data_items:
			if typeof(item) == TYPE_DICTIONARY:
				option_button.add_item(String(item.get("name", "Unnamed")))
	else:
		for item_name in fallback_names:
			option_button.add_item(String(item_name))
	option_button.select(0)

func _find_option_by_name(items: Variant, option_name: String) -> Dictionary:
	if typeof(items) == TYPE_ARRAY:
		for item in items:
			if typeof(item) == TYPE_DICTIONARY and String(item.get("name", "")) == option_name:
				return item
		for item in items:
			if typeof(item) == TYPE_DICTIONARY:
				return item
	return {}

func _make_form_label(text: String) -> Label:
	var label := Label.new()
	label.text = text
	CrpgTheme.apply_label(label, true)
	return label

func _make_fullscreen_control(control_name: String) -> Control:
	var control := Control.new()
	control.name = control_name
	control.position = Vector2.ZERO
	control.size = get_viewport_rect().size
	control.set_anchors_preset(Control.PRESET_FULL_RECT)
	return control

func _clear_current_screen() -> void:
	for child in get_children():
		child.queue_free()
	current_area = null
	menu_root = null
	character_creator_root = null
	character_name_edit = null
	ancestry_options = null
	origin_options = null
	archetype_options = null
	trait_options = null
	compatibility_warning_label = null
	start_journey_button = null

func _make_menu_button(text: String, callback: Callable) -> Button:
	var button := Button.new()
	button.text = text
	button.custom_minimum_size = Vector2(260, 42)
	CrpgTheme.apply_button(button)
	button.pressed.connect(callback)
	return button

func _spacer(height: int) -> Control:
	var spacer := Control.new()
	spacer.custom_minimum_size = Vector2(1, height)
	return spacer

func _on_load_game_pressed() -> void:
	if not _load_game():
		GameLog.warning("MENU", "Load Game pressed, but no valid save was loaded")

func _on_save_game_pressed() -> void:
	if not _save_game():
		GameLog.warning("MENU", "Save Game pressed, but no game was saved")

func _on_quit_pressed() -> void:
	GameLog.info("MENU", "Quit pressed")
	get_tree().quit()

func _dictionary_from(value: Variant) -> Dictionary:
	if typeof(value) == TYPE_DICTIONARY:
		return value.duplicate(true)
	return {}

func _array_to_vec2(value: Variant) -> Vector2:
	if typeof(value) == TYPE_ARRAY and value.size() >= 2:
		return Vector2(float(value[0]), float(value[1]))
	return Vector2.ZERO

func _vec2_to_array(value: Vector2) -> Array:
	return [value.x, value.y]
