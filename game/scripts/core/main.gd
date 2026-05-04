extends Node2D

const DataLoader = preload("res://game/scripts/core/data_loader.gd")
const AreaScene = preload("res://game/scenes/area/area_scene.tscn")
const CrpgTheme = preload("res://game/scripts/ui/crpg_theme.gd")
const GameLog = preload("res://game/scripts/core/game_log.gd")

var data_loader: DataLoader
var current_area: Node2D
var menu_root: Control
var character_creator_root: Control
var character_name_edit: LineEdit
var origin_options: OptionButton
var archetype_options: OptionButton
var player_profile: Dictionary = {
	"name": "Wanderer",
	"origin": "Border Drifter",
	"archetype": "Mercenary"
}

func _ready() -> void:
	GameLog.start_session("main_menu")
	GameLog.info("BOOT", "NG booting")
	data_loader = DataLoader.new()
	var load_result := data_loader.load_bootstrap_data()
	GameLog.info("BOOT", "Loaded bootstrap data", {"keys": load_result.keys()})
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
	var load_button := _make_menu_button("Load Game (coming soon)", _on_load_game_pressed)
	load_button.disabled = true
	root.add_child(load_button)
	var save_button := _make_menu_button("Save Game (in-game soon)", _on_save_game_pressed)
	save_button.disabled = true
	root.add_child(save_button)
	root.add_child(_make_menu_button("Quit", _on_quit_pressed))

	root.add_child(_spacer(14))
	var note := Label.new()
	note.text = "Current build: Wolfpine Road vertical-slice prototype"
	note.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	CrpgTheme.apply_label(note)
	root.add_child(note)
	GameLog.info("MENU", "Main menu shown")

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
	panel.position = Vector2(320, 90)
	panel.size = Vector2(640, 540)
	CrpgTheme.apply_panel(panel)
	character_creator_root.add_child(panel)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_top", 22)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_bottom", 22)
	panel.add_child(margin)

	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 10)
	margin.add_child(root)

	var title := Label.new()
	title.text = "Create Your Character"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	CrpgTheme.apply_label(title, true)
	title.add_theme_font_size_override("font_size", 26)
	root.add_child(title)

	var intro := Label.new()
	intro.text = "This is a first-pass creator. It stores a simple profile now; attributes, portraits, classes, and party setup will expand later."
	intro.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	CrpgTheme.apply_label(intro)
	root.add_child(intro)

	root.add_child(_spacer(10))

	var name_label := Label.new()
	name_label.text = "Name"
	CrpgTheme.apply_label(name_label, true)
	root.add_child(name_label)

	character_name_edit = LineEdit.new()
	character_name_edit.name = "CharacterName"
	character_name_edit.text = String(player_profile.get("name", "Wanderer"))
	root.add_child(character_name_edit)

	var origin_label := Label.new()
	origin_label.text = "Origin"
	CrpgTheme.apply_label(origin_label, true)
	root.add_child(origin_label)

	origin_options = OptionButton.new()
	origin_options.name = "OriginOptions"
	for origin in ["Border Drifter", "Failed Squire", "Village Outcast", "Caravan Guard"]:
		origin_options.add_item(origin)
	origin_options.select(0)
	root.add_child(origin_options)

	var archetype_label := Label.new()
	archetype_label.text = "Archetype"
	CrpgTheme.apply_label(archetype_label, true)
	root.add_child(archetype_label)

	archetype_options = OptionButton.new()
	archetype_options.name = "ArchetypeOptions"
	for archetype in ["Mercenary", "Scout", "Hedge Knight", "Cunning Speaker"]:
		archetype_options.add_item(archetype)
	archetype_options.select(0)
	root.add_child(archetype_options)

	root.add_child(_spacer(12))

	var buttons := HBoxContainer.new()
	buttons.add_theme_constant_override("separation", 10)
	root.add_child(buttons)

	var back_button := Button.new()
	back_button.text = "Back"
	CrpgTheme.apply_button(back_button)
	back_button.pressed.connect(_show_main_menu)
	buttons.add_child(back_button)

	var start_button := Button.new()
	start_button.text = "Start Journey"
	CrpgTheme.apply_button(start_button)
	start_button.pressed.connect(_start_new_game_from_creator.bind(character_name_edit, origin_options, archetype_options))
	buttons.add_child(start_button)
	GameLog.info("MENU", "Character creator shown")

func _start_new_game_from_creator(name_edit: LineEdit, selected_origin_options: OptionButton, selected_archetype_options: OptionButton) -> void:
	var character_name := name_edit.text.strip_edges()
	if character_name.is_empty():
		character_name = "Wanderer"
	player_profile = {
		"name": character_name,
		"origin": selected_origin_options.get_item_text(selected_origin_options.selected),
		"archetype": selected_archetype_options.get_item_text(selected_archetype_options.selected)
	}
	GameLog.info("CHARACTER", "Created player profile", player_profile)
	_start_game()

func _start_game() -> void:
	_clear_current_screen()
	current_area = AreaScene.instantiate()
	current_area.name = "CurrentArea"
	add_child(current_area)
	GameLog.info("GAME", "Started new game", {"player_profile": player_profile})

func run_debug_action(action: Dictionary) -> bool:
	var action_type := String(action.get("type", ""))
	GameLog.info("SCENARIO", "Running main action %s" % action_type, {"action": action})
	match action_type:
		"assert_screen":
			return _assert_screen(String(action.get("screen", "")))
		"press_menu":
			var button := String(action.get("button", ""))
			if button == "new_game":
				_show_character_creator()
				return true
			if button == "start_journey":
				if character_name_edit == null or origin_options == null or archetype_options == null:
					GameLog.error("ASSERT", "Cannot start journey; character creator controls are missing")
					return false
				_start_new_game_from_creator(character_name_edit, origin_options, archetype_options)
				return true
			GameLog.error("SCENARIO", "Unknown menu button: %s" % button, {"button": button})
			return false
		"set_character_name":
			if character_name_edit == null:
				GameLog.error("SCENARIO", "Cannot set character name; creator is not open")
				return false
			character_name_edit.text = String(action.get("name", "Wanderer"))
			return true
		"select_origin":
			return _select_option_by_text(origin_options, String(action.get("origin", "")), "origin")
		"select_archetype":
			return _select_option_by_text(archetype_options, String(action.get("archetype", "")), "archetype")
		"assert_player_profile":
			return _assert_player_profile(action)
		"assert_area":
			if current_area == null:
				GameLog.error("ASSERT", "No current area is loaded")
				return false
			var expected_area := String(action.get("area_id", ""))
			var actual_area := String(current_area.get("area_id"))
			if actual_area != expected_area:
				GameLog.error("ASSERT", "Area mismatch: expected %s got %s" % [expected_area, actual_area], {"expected": expected_area, "actual": actual_area})
				return false
			GameLog.info("ASSERT", "Area OK: %s" % expected_area)
			return true
		_:
			if current_area != null and current_area.has_method("run_debug_action"):
				return current_area.run_debug_action(action)
			GameLog.error("SCENARIO", "Unknown main action type: %s" % action_type, {"action": action})
			return false

func write_debug_state(file_name: String = "state_latest.json") -> void:
	var data := {
		"screen": _get_current_screen(),
		"player_profile": player_profile.duplicate(true),
		"has_current_area": current_area != null,
		"current_area_id": String(current_area.get("area_id")) if current_area != null else ""
	}
	GameLog.write_state_dump(file_name, data)

func _assert_screen(expected_screen: String) -> bool:
	var actual_screen := _get_current_screen()
	if actual_screen != expected_screen:
		GameLog.error("ASSERT", "Screen mismatch: expected %s got %s" % [expected_screen, actual_screen], {"expected": expected_screen, "actual": actual_screen})
		return false
	GameLog.info("ASSERT", "Screen OK: %s" % expected_screen)
	return true

func _get_current_screen() -> String:
	if current_area != null:
		return "game"
	if character_creator_root != null:
		return "character_creator"
	if menu_root != null:
		return "main_menu"
	return "unknown"

func _assert_player_profile(action: Dictionary) -> bool:
	for key in ["name", "origin", "archetype"]:
		if action.has(key):
			var expected := String(action[key])
			var actual := String(player_profile.get(key, ""))
			if actual != expected:
				GameLog.error("ASSERT", "Player profile mismatch for %s: expected %s got %s" % [key, expected, actual], {"key": key, "expected": expected, "actual": actual})
				return false
	GameLog.info("ASSERT", "Player profile OK", {"player_profile": player_profile})
	return true

func _select_option_by_text(option_button: OptionButton, text: String, label: String) -> bool:
	if option_button == null:
		GameLog.error("SCENARIO", "Cannot select %s; control is missing" % label)
		return false
	for index in range(option_button.item_count):
		if option_button.get_item_text(index) == text:
			option_button.select(index)
			GameLog.info("SCENARIO", "Selected %s: %s" % [label, text])
			return true
	GameLog.error("SCENARIO", "Could not find %s option: %s" % [label, text])
	return false

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
	origin_options = null
	archetype_options = null

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
	GameLog.info("MENU", "Load Game pressed, but saves are not implemented yet")

func _on_save_game_pressed() -> void:
	GameLog.info("MENU", "Save Game pressed, but saves are not implemented yet")

func _on_quit_pressed() -> void:
	GameLog.info("MENU", "Quit pressed")
	get_tree().quit()
