extends preload("res://game/scripts/core/main_runtime_v2.gd")

const PortraitCatalog = preload("res://game/scripts/character/portrait_catalog.gd")

const PORTRAITS_PATH := "res://data/character_creation/portraits.json"

var portrait_options: OptionButton
var portrait_summary_label: Label
var profile_preview_label: Label
var portrait_data: Dictionary = {}
var portrait_manually_selected := false

func _ready() -> void:
	GameLog.start_session("main_menu")
	GameLog.info("BOOT", "NG booting")
	data_loader = DataLoader.new()
	save_system = SaveSystem.new()
	var load_result := data_loader.load_bootstrap_data()
	character_creation_data = data_loader.load_json_file(CHARACTER_CREATION_PATH)
	portrait_data = data_loader.load_json_file(PORTRAITS_PATH)
	GameLog.info("BOOT", "Loaded bootstrap data", {
		"keys": load_result.keys(),
		"has_character_creation": not character_creation_data.is_empty(),
		"has_portraits": not portrait_data.is_empty()
	})
	_show_main_menu()

func _show_character_creator() -> void:
	_clear_current_screen()
	portrait_manually_selected = false
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
	panel.position = Vector2(290, 10)
	panel.size = Vector2(700, 715)
	CrpgTheme.apply_panel(panel)
	character_creator_root.add_child(panel)

	var margin := MarginContainer.new()
	margin.add_theme_constant_override("margin_left", 24)
	margin.add_theme_constant_override("margin_top", 14)
	margin.add_theme_constant_override("margin_right", 24)
	margin.add_theme_constant_override("margin_bottom", 14)
	panel.add_child(margin)

	var root := VBoxContainer.new()
	root.add_theme_constant_override("separation", 5)
	margin.add_child(root)

	var title := Label.new()
	title.text = "Create Your Character"
	title.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	CrpgTheme.apply_label(title, true)
	title.add_theme_font_size_override("font_size", 23)
	root.add_child(title)

	var intro := Label.new()
	intro.text = "Choose a name, ancestry, background, class, trait, and portrait. The preview shows the profile that will enter Wolfpine Road."
	intro.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	CrpgTheme.apply_label(intro)
	root.add_child(intro)

	root.add_child(_make_form_label("Name"))
	character_name_edit = LineEdit.new()
	character_name_edit.name = "CharacterName"
	character_name_edit.text = String(player_profile.get("name", "Wanderer"))
	character_name_edit.text_changed.connect(_on_creator_text_changed)
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

	root.add_child(_make_form_label("Portrait"))
	portrait_options = OptionButton.new()
	portrait_options.name = "PortraitOptions"
	_populate_portrait_options()
	_select_portrait_for_current_background(false)
	portrait_options.item_selected.connect(_on_portrait_selection_changed)
	root.add_child(portrait_options)

	portrait_summary_label = Label.new()
	portrait_summary_label.name = "PortraitSummary"
	portrait_summary_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	portrait_summary_label.custom_minimum_size = Vector2(640, 44)
	CrpgTheme.apply_label(portrait_summary_label)
	root.add_child(portrait_summary_label)

	profile_preview_label = Label.new()
	profile_preview_label.name = "ProfilePreview"
	profile_preview_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	profile_preview_label.custom_minimum_size = Vector2(640, 92)
	CrpgTheme.apply_label(profile_preview_label)
	root.add_child(profile_preview_label)

	compatibility_warning_label = Label.new()
	compatibility_warning_label.name = "CompatibilityWarning"
	compatibility_warning_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
	compatibility_warning_label.custom_minimum_size = Vector2(640, 44)
	CrpgTheme.apply_label(compatibility_warning_label)
	root.add_child(compatibility_warning_label)

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
	start_journey_button.pressed.connect(_start_new_game_from_creator.bind(character_name_edit, ancestry_options, origin_options, archetype_options, trait_options, portrait_options))
	buttons.add_child(start_journey_button)
	_refresh_trait_options(String(player_profile.get("trait", "Steady Under Fire")))
	_update_portrait_summary()
	_update_creator_compatibility()
	_update_profile_preview()
	GameLog.info("MENU", "Character creator shown", {"portrait_count": PortraitCatalog.get_portraits(portrait_data).size()})

func _start_new_game_from_creator(name_edit: LineEdit, selected_ancestry_options: OptionButton, selected_origin_options: OptionButton, selected_archetype_options: OptionButton, selected_trait_options: OptionButton, selected_portrait_options: OptionButton = null) -> void:
	var character_name := name_edit.text.strip_edges()
	if character_name.is_empty():
		character_name = "Wanderer"
	var ancestry_name := selected_ancestry_options.get_item_text(selected_ancestry_options.selected)
	var background_name := selected_origin_options.get_item_text(selected_origin_options.selected)
	var archetype_name := selected_archetype_options.get_item_text(selected_archetype_options.selected)
	var trait_name := selected_trait_options.get_item_text(selected_trait_options.selected)
	var built_profile := _build_player_profile(character_name, ancestry_name, background_name, archetype_name, trait_name)
	if selected_portrait_options != null:
		built_profile = PortraitCatalog.apply_to_profile(built_profile, _get_selected_portrait())
	var warnings: Array = built_profile.get("compatibility_warnings", [])
	if not warnings.is_empty():
		_show_creator_warnings(warnings)
		GameLog.warning("CHARACTER", "Blocked incompatible player profile", {"warnings": warnings, "profile": built_profile})
		return
	player_profile = built_profile
	GameLog.info("CHARACTER", "Created player profile", player_profile)
	_start_game()

func _on_creator_selection_changed(_selected_index: int = -1) -> void:
	_refresh_trait_options(_get_selected_option_text(trait_options))
	_select_portrait_for_current_background(true)
	_update_creator_compatibility(_selected_index)
	_update_profile_preview()

func _on_creator_text_changed(_new_text: String) -> void:
	_update_creator_compatibility()
	_update_profile_preview()

func _on_portrait_selection_changed(_selected_index: int = -1) -> void:
	portrait_manually_selected = true
	_update_portrait_summary()
	_update_profile_preview()

func _populate_portrait_options() -> void:
	if portrait_options == null:
		return
	portrait_options.clear()
	var portraits := PortraitCatalog.get_portraits(portrait_data)
	if portraits.is_empty():
		portrait_options.add_item("Weathered Drifter")
		portrait_options.select(0)
		return
	for portrait_data_item in portraits:
		portrait_options.add_item(PortraitCatalog.get_display_name(portrait_data_item))
	portrait_options.select(0)

func _select_portrait_for_current_background(respect_manual_selection: bool = true) -> void:
	if portrait_options == null:
		return
	if respect_manual_selection and portrait_manually_selected:
		_update_portrait_summary()
		return
	var background_data := _find_option_by_name(character_creation_data.get("backgrounds", []), _get_selected_option_text(origin_options))
	var default_profile := CharacterProfileBuilder.build_profile(
		"Wanderer",
		_find_option_by_name(character_creation_data.get("ancestries", []), _get_selected_option_text(ancestry_options)),
		background_data,
		_find_option_by_name(character_creation_data.get("classes", []), _get_selected_option_text(archetype_options)),
		_find_option_by_name(character_creation_data.get("traits", []), _get_selected_option_text(trait_options)),
		character_creation_data
	)
	var wanted_name := String(default_profile.get("portrait", ""))
	if wanted_name.is_empty() or not _select_option_by_text(portrait_options, wanted_name, "portrait"):
		portrait_options.select(0)
	_update_portrait_summary()

func _get_selected_portrait() -> Dictionary:
	if portrait_options == null or portrait_options.get_item_count() == 0:
		return PortraitCatalog.get_default_portrait(portrait_data)
	var portrait_name := portrait_options.get_item_text(portrait_options.selected)
	var portrait_data_item := PortraitCatalog.find_by_name(portrait_data, portrait_name)
	if portrait_data_item.is_empty():
		return PortraitCatalog.get_default_portrait(portrait_data)
	return portrait_data_item

func _update_portrait_summary() -> void:
	if portrait_summary_label == null:
		return
	var portrait_data_item := _get_selected_portrait()
	if portrait_data_item.is_empty():
		portrait_summary_label.text = "Portrait: Weathered Drifter\nNo portrait metadata loaded."
		return
	portrait_summary_label.text = "%s\n%s" % [PortraitCatalog.get_display_name(portrait_data_item), PortraitCatalog.get_summary(portrait_data_item)]

func _get_creator_preview_profile() -> Dictionary:
	if character_name_edit == null or ancestry_options == null or origin_options == null or archetype_options == null or trait_options == null:
		return {}
	var preview_name := character_name_edit.text.strip_edges()
	if preview_name.is_empty():
		preview_name = "Wanderer"
	var preview_profile := _build_player_profile(
		preview_name,
		_get_selected_option_text(ancestry_options),
		_get_selected_option_text(origin_options),
		_get_selected_option_text(archetype_options),
		_get_selected_option_text(trait_options)
	)
	if portrait_options != null:
		preview_profile = PortraitCatalog.apply_to_profile(preview_profile, _get_selected_portrait())
	return preview_profile

func _update_profile_preview() -> void:
	if profile_preview_label == null:
		return
	var preview_profile := _get_creator_preview_profile()
	if preview_profile.is_empty():
		profile_preview_label.text = "Profile preview unavailable."
		return
	profile_preview_label.text = "Profile preview: %s\nAttributes: %s\nSkills: %s\nTags: %s" % [
		_profile_identity_line(preview_profile),
		_format_score_summary(preview_profile.get("attributes", {})),
		_format_score_summary(preview_profile.get("skills", {})),
		_format_tag_preview(preview_profile.get("tags", []))
	]

func _profile_identity_line(preview_profile: Dictionary) -> String:
	return "%s — %s / %s / %s / %s" % [
		String(preview_profile.get("name", "Wanderer")),
		String(preview_profile.get("ancestry", "Unknown ancestry")),
		String(preview_profile.get("background", "Unknown background")),
		String(preview_profile.get("class", "Unknown class")),
		String(preview_profile.get("trait", "Unknown trait"))
	]

func _format_score_summary(value: Variant) -> String:
	if typeof(value) != TYPE_DICTIONARY:
		return "none"
	var source: Dictionary = value
	var keys := source.keys()
	keys.sort()
	var pieces: Array[String] = []
	for key in keys:
		var label := String(key).replace("_", " ").capitalize()
		pieces.append("%s %d" % [label, int(source[key])])
	if pieces.is_empty():
		return "none"
	return ", ".join(pieces)

func _format_tag_preview(value: Variant) -> String:
	if typeof(value) != TYPE_ARRAY:
		return "none"
	var labels: Array[String] = []
	for tag_id in value:
		labels.append(CharacterProfileBuilder.format_tag(String(tag_id)))
		if labels.size() >= 6:
			break
	if labels.is_empty():
		return "none"
	return ", ".join(labels)

func run_debug_action(action: Dictionary) -> bool:
	var action_type := String(action.get("type", ""))
	if action_type == "select_portrait":
		var portrait_ok := _select_option_by_text(portrait_options, String(action.get("portrait", "")), "portrait")
		portrait_manually_selected = portrait_ok
		_update_portrait_summary()
		_update_profile_preview()
		return portrait_ok
	if action_type == "assert_creator_preview_contains":
		return _assert_creator_preview_contains(String(action.get("text", "")))
	return super.run_debug_action(action)

func _assert_creator_preview_contains(expected_text: String) -> bool:
	if profile_preview_label == null:
		GameLog.error("ASSERT", "Creator profile preview label is missing")
		return false
	var actual_text := profile_preview_label.text
	if not actual_text.contains(expected_text):
		GameLog.error("ASSERT", "Creator profile preview mismatch: expected text containing %s got %s" % [expected_text, actual_text], {"expected": expected_text, "actual": actual_text})
		return false
	GameLog.info("ASSERT", "Creator profile preview contains: %s" % expected_text)
	return true

func _press_menu_button(button: String) -> bool:
	if button == "start_journey":
		if character_name_edit == null or ancestry_options == null or origin_options == null or archetype_options == null or trait_options == null or portrait_options == null:
			GameLog.error("ASSERT", "Cannot start journey; character creator controls are missing")
			return false
		_start_new_game_from_creator(character_name_edit, ancestry_options, origin_options, archetype_options, trait_options, portrait_options)
		return true
	return super._press_menu_button(button)

func _assert_player_profile(action: Dictionary) -> bool:
	for key in ["name", "ancestry", "origin", "archetype", "background", "class", "trait", "portrait_id", "portrait"]:
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

func _clear_current_screen() -> void:
	super._clear_current_screen()
	portrait_options = null
	portrait_summary_label = null
	profile_preview_label = null
