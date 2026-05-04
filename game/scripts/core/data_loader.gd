extends RefCounted
class_name DataLoader

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
	if not FileAccess.file_exists(path):
		push_error("Missing JSON file: %s" % path)
		return {}
	var file := FileAccess.open(path, FileAccess.READ)
	var text := file.get_as_text()
	var parsed: Variant = JSON.parse_string(text)
	if typeof(parsed) != TYPE_DICTIONARY:
		push_error("JSON root must be object: %s" % path)
		return {}
	return parsed

func load_bootstrap_data() -> Dictionary:
	var result := {}
	for key in BOOTSTRAP_FILES.keys():
		result[key] = load_json_file(BOOTSTRAP_FILES[key])
	return result
