extends RefCounted
class_name DataLoader

const GameLog = preload("res://game/scripts/core/game_log.gd")

const BOOTSTRAP_FILES := {
	"area": "res://areas/wolfpine_road/area.json",
	"npc": "res://data/actors/npcs/captain_renna.json",
	"companion": "res://data/actors/companions/brannoc.json",
	"enemy": "res://data/actors/enemies/border_bandit.json",
	"item": "res://data/items/weapons/border_iron_sword.json",
	"quest": "res://data/quests/main/missing_caravan.json",
	"factions": "res://data/factions/factions.json"
}

func load_json_file(path: String) -> Dictionary:
	if path.is_empty():
		GameLog.error("DATA", "Missing JSON path argument")
		return {}
	if not FileAccess.file_exists(path):
		GameLog.error("DATA", "Missing JSON file: %s" % path, {"path": path})
		push_error("Missing JSON file: %s" % path)
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	if file == null:
		GameLog.error("DATA", "Could not open JSON file: %s" % path, {"path": path})
		return {}
	var text := file.get_as_text()
	file.close()
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		GameLog.error("DATA", "JSON root must be object: %s" % path, {"path": path})
		push_error("JSON root must be object: %s" % path)
		return {}
	GameLog.event("json_loaded", {"path": path})
	return parsed

func load_bootstrap_data() -> Dictionary:
	var result := {}
	GameLog.info("DATA", "Loading bootstrap data", {"count": BOOTSTRAP_FILES.size()})
	for key in BOOTSTRAP_FILES.keys():
		result[key] = load_json_file(BOOTSTRAP_FILES[key])
	GameLog.info("DATA", "Bootstrap data loaded", {"keys": result.keys()})
	return result
