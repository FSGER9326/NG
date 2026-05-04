extends SceneTree

const GameLog = preload("res://game/scripts/core/game_log.gd")
const DebugStateDump = preload("res://game/scripts/core/debug_state_dump.gd")

func _initialize() -> void:
	GameLog.start_session("scenario_test")
	var scenario_path := _get_scenario_path()
	GameLog.info("SCENARIO", "Loading scenario: %s" % scenario_path, {"scenario_path": scenario_path})

	var scenario := _load_json(scenario_path)
	if scenario.is_empty():
		GameLog.error("SCENARIO", "Could not load scenario: %s" % scenario_path)
		quit(1)
		return

	var area_scene := load("res://game/scenes/area/area_scene.tscn")
	if area_scene == null:
		GameLog.error("SCENARIO", "Could not load area scene")
		quit(1)
		return

	var area_instance = area_scene.instantiate()
	if area_instance == null:
		GameLog.error("SCENARIO", "Could not instantiate area scene")
		quit(1)
		return

	root.add_child(area_instance)
	await process_frame
	await process_frame

	var success := true
	var step_index := 0
	for step in scenario.get("steps", []):
		step_index += 1
		if typeof(step) != TYPE_DICTIONARY:
			GameLog.error("SCENARIO", "Invalid step at index %s" % step_index, {"step_index": step_index})
			success = false
			break
		GameLog.info("SCENARIO", "Step %s: %s" % [step_index, String(step.get("type", ""))], {"step_index": step_index, "step": step})
		if not area_instance.run_debug_action(step):
			GameLog.error("SCENARIO", "Step failed: %s" % step_index, {"step_index": step_index, "step": step})
			success = false
			break
		await process_frame

	if area_instance.has_method("write_debug_state"):
		area_instance.write_debug_state("state_after_scenario.json")
	else:
		GameLog.write_state_dump("state_after_scenario.json", DebugStateDump.from_area_controller(area_instance))

	if success:
		GameLog.info("SCENARIO", "Scenario passed: %s" % String(scenario.get("id", scenario_path)))
		quit(0)
	else:
		GameLog.error("SCENARIO", "Scenario failed: %s" % String(scenario.get("id", scenario_path)))
		quit(1)

func _get_scenario_path() -> String:
	var args := OS.get_cmdline_args()
	for index in range(args.size()):
		if args[index] == "--scenario" and index + 1 < args.size():
			return args[index + 1]
	return "res://tests/scenarios/wolfpine_missing_caravan.json"

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
