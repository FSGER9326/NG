extends RefCounted
class_name GameState

const GameLog = preload("res://game/scripts/core/game_log.gd")

var flags: Dictionary = {}
var faction_reputation: Dictionary = {}
var party_member_ids: Array[String] = []
var active_quest_ids: Array[String] = []
var quest_stages: Dictionary = {}

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
	return "\n".join(lines)

func to_debug_dict() -> Dictionary:
	return {
		"flags": flags.duplicate(true),
		"faction_reputation": faction_reputation.duplicate(true),
		"party_member_ids": party_member_ids.duplicate(true),
		"active_quest_ids": active_quest_ids.duplicate(true),
		"quest_stages": quest_stages.duplicate(true)
	}
