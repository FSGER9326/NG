extends RefCounted
class_name GameState

const GameLog = preload("res://game/scripts/core/game_log.gd")

var flags: Dictionary = {}
var faction_reputation: Dictionary = {}
var party_member_ids: Array[String] = []
var player_profile: Dictionary = {}
var player_tags: Array[String] = []
var player_attributes: Dictionary = {
	"might": 1,
	"finesse": 1,
	"resolve": 1,
	"wits": 1,
	"presence": 1,
	"occult": 0
}
var party_skills: Dictionary = {
	"perception": 2,
	"survival": 1,
	"resolve": 1,
	"lore": 1,
	"stealth": 1,
	"athletics": 0,
	"medicine": 0,
	"streetwise": 0,
	"arcana": 0,
	"command": 0
}
var active_quest_ids: Array[String] = []
var quest_stages: Dictionary = {}

func apply_player_profile(profile: Dictionary) -> void:
	player_profile = profile.duplicate(true)
	player_tags.clear()
	for tag in profile.get("tags", []):
		var tag_id := String(tag)
		if not tag_id.is_empty() and not player_tags.has(tag_id):
			player_tags.append(tag_id)
	var profile_attributes: Dictionary = profile.get("attributes", {})
	for key in profile_attributes.keys():
		player_attributes[String(key)] = int(profile_attributes[key])
	var profile_skills: Dictionary = profile.get("skills", {})
	for key in profile_skills.keys():
		party_skills[String(key)] = int(profile_skills[key])
	GameLog.info("CHARACTER", "Applied player profile to game state", {
		"name": String(profile.get("name", "")),
		"tag_count": player_tags.size(),
		"tags": player_tags,
		"attributes": player_attributes,
		"skills": party_skills
	})

func has_player_tag(tag_id: String) -> bool:
	return player_tags.has(tag_id)

func get_player_attribute(attribute_id: String) -> int:
	return int(player_attributes.get(attribute_id, 0))

func set_flag(flag_id: String, value: bool = true) -> void:
	var old_value := bool(flags.get(flag_id, false))
	flags[flag_id] = value
	GameLog.info("FLAG", "%s %s -> %s" % [flag_id, old_value, value], {
		"flag_id": flag_id,
		"from": old_value,
		"to": value
	})

func has_flag(flag_id: String) -> bool:
	return bool(flags.get(flag_id, false))

func set_party_skill(skill_id: String, value: int) -> void:
	if skill_id.is_empty():
		GameLog.warning("SKILL", "Ignored empty skill id", {"value": value})
		return
	var old_value := get_party_skill(skill_id)
	party_skills[skill_id] = value
	GameLog.info("SKILL", "%s %s -> %s" % [skill_id, old_value, value], {
		"skill_id": skill_id,
		"from": old_value,
		"to": value
	})

func get_party_skill(skill_id: String) -> int:
	return int(party_skills.get(skill_id, 0))

func modify_reputation(faction_id: String, amount: int) -> void:
	var old_value := int(faction_reputation.get(faction_id, 0))
	var new_value := old_value + amount
	faction_reputation[faction_id] = new_value
	GameLog.info("FACTION", "%s reputation %s -> %s" % [faction_id, old_value, new_value], {
		"faction_id": faction_id,
		"from": old_value,
		"to": new_value,
		"amount": amount
	})

func start_quest(quest_id: String, stage_id: String = "accepted") -> void:
	if not active_quest_ids.has(quest_id):
		active_quest_ids.append(quest_id)
		GameLog.info("QUEST", "Quest activated: %s" % quest_id, {"quest_id": quest_id})
	if get_quest_stage(quest_id) == "not_started":
		set_quest_stage(quest_id, stage_id)
	else:
		GameLog.info("QUEST", "Quest already has progress; start_quest did not overwrite %s" % quest_id, {
			"quest_id": quest_id,
			"existing_stage": get_quest_stage(quest_id),
			"requested_stage": stage_id
		})

func set_quest_stage(quest_id: String, stage_id: String) -> void:
	var old_stage := get_quest_stage(quest_id)
	quest_stages[quest_id] = stage_id
	if stage_id != "not_started" and not active_quest_ids.has(quest_id):
		active_quest_ids.append(quest_id)
	GameLog.info("QUEST", "%s %s -> %s" % [quest_id, old_stage, stage_id], {
		"quest_id": quest_id,
		"from": old_stage,
		"to": stage_id
	})

func get_quest_stage(quest_id: String) -> String:
	return String(quest_stages.get(quest_id, "not_started"))

func is_quest_started(quest_id: String) -> bool:
	return get_quest_stage(quest_id) != "not_started"

func get_debug_summary() -> String:
	var lines: Array[String] = []
	if active_quest_ids.is_empty():
		lines.append("Quests: none")
	else:
		lines.append("Quests:")
		for quest_id in active_quest_ids:
			lines.append("- %s: %s" % [quest_id, get_quest_stage(quest_id)])
	if not player_tags.is_empty():
		lines.append("Tags: %s" % ", ".join(player_tags.slice(0, min(4, player_tags.size()))))
	return "\n".join(lines)

func to_debug_dict() -> Dictionary:
	return {
		"flags": flags.duplicate(true),
		"faction_reputation": faction_reputation.duplicate(true),
		"party_member_ids": party_member_ids.duplicate(true),
		"player_profile": player_profile.duplicate(true),
		"player_tags": player_tags.duplicate(true),
		"player_attributes": player_attributes.duplicate(true),
		"party_skills": party_skills.duplicate(true),
		"active_quest_ids": active_quest_ids.duplicate(true),
		"quest_stages": quest_stages.duplicate(true)
	}

func apply_save_data(data: Dictionary) -> void:
	flags = _dictionary_from(data.get("flags", {}))
	faction_reputation = _dictionary_from(data.get("faction_reputation", {}))
	party_skills = _dictionary_from(data.get("party_skills", party_skills))
	quest_stages = _dictionary_from(data.get("quest_stages", {}))
	party_member_ids = _string_array_from(data.get("party_member_ids", []))
	active_quest_ids = _string_array_from(data.get("active_quest_ids", []))
	player_profile = _dictionary_from(data.get("player_profile", {}))
	player_tags = _string_array_from(data.get("player_tags", []))
	player_attributes = _dictionary_from(data.get("player_attributes", player_attributes))
	GameLog.info("SAVE", "Applied game-state save data", {
		"flag_count": flags.size(),
		"quest_count": active_quest_ids.size(),
		"skill_count": party_skills.size(),
		"tag_count": player_tags.size()
	})

func _dictionary_from(value: Variant) -> Dictionary:
	if typeof(value) == TYPE_DICTIONARY:
		return value.duplicate(true)
	return {}

func _string_array_from(value: Variant) -> Array[String]:
	var result: Array[String] = []
	if typeof(value) != TYPE_ARRAY:
		return result
	for item in value:
		result.append(String(item))
	return result
