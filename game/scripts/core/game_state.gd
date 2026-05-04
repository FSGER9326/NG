extends RefCounted
class_name GameState

var flags: Dictionary = {}
var faction_reputation: Dictionary = {}
var party_member_ids: Array[String] = []
var active_quest_ids: Array[String] = []

func set_flag(flag_id: String, value: bool = true) -> void:
	flags[flag_id] = value

func has_flag(flag_id: String) -> bool:
	return bool(flags.get(flag_id, false))

func modify_reputation(faction_id: String, amount: int) -> void:
	faction_reputation[faction_id] = int(faction_reputation.get(faction_id, 0)) + amount
