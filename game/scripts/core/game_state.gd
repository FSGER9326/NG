extends RefCounted
class_name GameState

var flags: Dictionary = {}
var faction_reputation: Dictionary = {}
var party_member_ids: Array[String] = []
var active_quest_ids: Array[String] = []
var quest_stages: Dictionary = {}

func set_flag(flag_id: String, value: bool = true) -> void:
	flags[flag_id] = value

func has_flag(flag_id: String) -> bool:
	return bool(flags.get(flag_id, false))

func modify_reputation(faction_id: String, amount: int) -> void:
	faction_reputation[faction_id] = int(faction_reputation.get(faction_id, 0)) + amount

func start_quest(quest_id: String, stage_id: String = "accepted") -> void:
	if not active_quest_ids.has(quest_id):
		active_quest_ids.append(quest_id)
	set_quest_stage(quest_id, stage_id)

func set_quest_stage(quest_id: String, stage_id: String) -> void:
	quest_stages[quest_id] = stage_id
	if stage_id != "not_started" and not active_quest_ids.has(quest_id):
		active_quest_ids.append(quest_id)

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
