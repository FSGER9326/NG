extends RefCounted
class_name QuestSystem

const GameLog = preload("res://game/scripts/core/game_log.gd")

var quest_states: Dictionary = {}

func start_quest(quest_id: String, start_stage: String = "accepted") -> void:
	var old_stage := get_stage(quest_id)
	quest_states[quest_id] = start_stage
	GameLog.info("QUEST_SYSTEM", "%s %s -> %s" % [quest_id, old_stage, start_stage], {
		"quest_id": quest_id,
		"from": old_stage,
		"to": start_stage,
		"operation": "start_quest"
	})

func set_stage(quest_id: String, stage_id: String) -> void:
	var old_stage := get_stage(quest_id)
	quest_states[quest_id] = stage_id
	GameLog.info("QUEST_SYSTEM", "%s %s -> %s" % [quest_id, old_stage, stage_id], {
		"quest_id": quest_id,
		"from": old_stage,
		"to": stage_id,
		"operation": "set_stage"
	})

func get_stage(quest_id: String) -> String:
	return String(quest_states.get(quest_id, "not_started"))

func is_started(quest_id: String) -> bool:
	return quest_states.has(quest_id) and get_stage(quest_id) != "not_started"

func to_debug_dict() -> Dictionary:
	return quest_states.duplicate(true)
