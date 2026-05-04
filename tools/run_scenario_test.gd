extends SceneTree

const GameLog = preload("res://game/scripts/core/game_log.gd")

func _initialize() -> void:
	GameLog.start_session("scenario_test")
	var scenario_path := _normalize_res_path(_get_scenario_path())
	GameLog.info("SCENARIO", "Loading scenario: %s" % scenario_path, {"scenario_path": scenario_path})

	var scenario := _load_json(scenario_path)
	if scenario.is_empty():
		GameLog.error("SCENARIO", "Could not load scenario: %s" % scenario_path)
		quit(1)
		return

	var target_scene_path := _get_target_scene_path(scenario)
	var target_scene := load(target_scene_path)
	if target_scene == null:
		GameLog.error("SCENARIO", "Could not load target scene: %s" % target_scene_path)
		quit(1)
		return

	var target_instance = target_scene.instantiate()
	if target_instance == null:
		GameLog.error("SCENARIO", "Could not instantiate target scene: %s" % target_scene_path)
		quit(1)
		return
	if not target_instance.has_method("run_debug_action"):
		GameLog.error("SCENARIO", "Target scene does not expose run_debug_action().", {"target_scene": target_scene_path})
		quit(1)
		return

	root.add_child(target_instance)
	await process_frame
	await process_frame

	var success := await _run_steps(target_instance, scenario.get("steps", []))

	if target_instance.has_method("write_debug_state"):
		target_instance.write_debug_state("state_after_scenario.json")

	if success:
		GameLog.info("SCENARIO", "Scenario passed: %s" % String(scenario.get("id", scenario_path)))
		quit(0)
	else:
		GameLog.error("SCENARIO", "Scenario failed: %s" % String(scenario.get("id", scenario_path)))
		quit(1)

func _run_steps(target_instance: Node, steps: Variant) -> bool:
	if typeof(steps) != TYPE_ARRAY:
		GameLog.error("SCENARIO", "Scenario steps must be a list")
		return false
	var step_index := 0
	for step in steps:
		step_index += 1
		if typeof(step) != TYPE_DICTIONARY:
			GameLog.error("SCENARIO", "Invalid step at index %s" % step_index, {"step_index": step_index})
			return false
		GameLog.info("SCENARIO", "Step %s: %s" % [step_index, String(step.get("type", ""))], {"step_index": step_index, "step": step})
		if not target_instance.run_debug_action(step):
			GameLog.error("SCENARIO", "Step failed: %s" % step_index, {"step_index": step_index, "step": step})
			return false
		await process_frame
		await process_frame
	return true

func _get_target_scene_path(scenario: Dictionary) -> String:
	var root_scene := String(scenario.get("root_scene", "area"))
	match root_scene:
		"main":
			return "res://game/scenes/main.tscn"
		"area":
			return "res://game/scenes/area/area_scene.tscn"
		_:
			if root_scene.begins_with("res://"):
				return root_scene
			GameLog.warning("SCENARIO", "Unknown root_scene, defaulting to area scene: %s" % root_scene)
			return "res://game/scenes/area/area_scene.tscn"

func _get_scenario_path() -> String:
	var args := OS.get_cmdline_args()
	for index in range(args.size()):
		if args[index] == "--scenario" and index + 1 < args.size():
			return args[index + 1]
	return "res://tests/scenarios/wolfpine_missing_caravan.json"

func _normalize_res_path(path: String) -> String:
	var normalized := path.replace("\\", "/")
	if normalized.begins_with("res://"):
		return normalized
	return "res://%s" % normalized

func _load_json(path: String) -> Dictionary:
	if not FileAccess.file_exists(path):
		GameLog.error("SCENARIO", "Missing JSON file: %s" % path)
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		GameLog.error("SCENARIO", "Could not open JSON file: %s" % path)
		return {}
	var parsed: Variant = JSON.parse_string(file.get_as_text())
	file.close()
	if typeof(parsed) != TYPE_DICTIONARY:
		GameLog.error("SCENARIO", "Scenario root must be object: %s" % path)
		return {}
	return parsed
