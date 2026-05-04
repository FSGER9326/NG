extends RefCounted
class_name SaveSystem

const GameLog = preload("res://game/scripts/core/game_log.gd")

const SAVE_VERSION := 1
const DEFAULT_SAVE_PATH := "user://ng_save_slot_1.json"

func has_save(path: String = DEFAULT_SAVE_PATH) -> bool:
	return FileAccess.file_exists(path)

func write_save(data: Dictionary, path: String = DEFAULT_SAVE_PATH) -> bool:
	var save_data := data.duplicate(true)
	save_data["save_version"] = SAVE_VERSION
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		GameLog.error("SAVE", "Could not open save file for writing: %s" % path, {"path": path})
		return false
	file.store_string(JSON.stringify(save_data, "\t"))
	file.close()
	GameLog.info("SAVE", "Wrote save file: %s" % path, {"path": path, "save_version": SAVE_VERSION})
	return true

func read_save(path: String = DEFAULT_SAVE_PATH) -> Dictionary:
	if not FileAccess.file_exists(path):
		GameLog.warning("SAVE", "Save file does not exist: %s" % path, {"path": path})
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		GameLog.error("SAVE", "Could not open save file for reading: %s" % path, {"path": path})
		return {}
	var text := file.get_as_text()
	file.close()
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		GameLog.error("SAVE", "Save file root must be an object: %s" % path, {"path": path})
		return {}
	var save_version := int(parsed.get("save_version", 0))
	if save_version != SAVE_VERSION:
		GameLog.warning("SAVE", "Save version mismatch", {"path": path, "expected": SAVE_VERSION, "actual": save_version})
	GameLog.info("SAVE", "Read save file: %s" % path, {"path": path, "save_version": save_version})
	return parsed
