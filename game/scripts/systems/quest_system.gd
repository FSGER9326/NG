extends RefCounted
class_name QuestSystem

var quest_states: Dictionary = {}

func start_quest(quest_id: String, start_stage: String = "accepted") -> void:
	quest_states[quest_id] = start_stage

func set_stage(quest_id: String, stage_id: String) -> void:
	quest_states[quest_id] = stage_id

func get_stage(quest_id: String) -> String:
	return String(quest_states.get(quest_id, "not_started"))

func is_started(quest_id: String) -> bool:
	return quest_states.has(quest_id) and get_stage(quest_id) != "not_started"
