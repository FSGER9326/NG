extends RefCounted
class_name DialogueConditionEvaluator

const GameLog = preload("res://game/scripts/core/game_log.gd")

var game_state: GameState

func setup(state: GameState) -> void:
	game_state = state

func passes_data_conditions(data: Dictionary) -> bool:
	return passes_conditions(data.get("conditions", []))

func passes_conditions(conditions: Variant) -> bool:
	if conditions == null:
		return true
	if typeof(conditions) != TYPE_ARRAY:
		GameLog.warning("DIALOGUE", "Conditions field is not a list", {"conditions": conditions})
		return false
	for condition in conditions:
		if not passes_condition(condition):
			return false
	return true

func passes_condition(condition: Variant) -> bool:
	if game_state == null:
		GameLog.warning("DIALOGUE", "Condition evaluator has no game state", {"condition": condition})
		return false
	if typeof(condition) != TYPE_DICTIONARY:
		GameLog.warning("DIALOGUE", "Condition is not an object", {"condition": condition})
		return false
	var condition_type := String(condition.get("type", ""))
	match condition_type:
		"flag":
			return _passes_flag_condition(condition)
		"quest_stage":
			return _passes_quest_stage_condition(condition)
		"skill_check":
			return _passes_skill_check_condition(condition)
		"not":
			return not passes_condition(condition.get("condition", {}))
		"all":
			return passes_conditions(condition.get("conditions", []))
		"any":
			return _passes_any_condition(condition.get("conditions", []))
		_:
			GameLog.warning("DIALOGUE", "Unknown condition type: %s" % condition_type, {"condition": condition})
			return false

func _passes_flag_condition(condition: Dictionary) -> bool:
	var flag_id := String(condition.get("flag_id", ""))
	var expected := bool(condition.get("value", true))
	var actual := game_state.has_flag(flag_id)
	GameLog.event("condition_checked", {
		"type": "flag",
		"flag_id": flag_id,
		"expected": expected,
		"actual": actual,
		"passed": actual == expected
	})
	return actual == expected

func _passes_quest_stage_condition(condition: Dictionary) -> bool:
	var quest_id := String(condition.get("quest_id", ""))
	var expected_stage := String(condition.get("stage", ""))
	var actual_stage := game_state.get_quest_stage(quest_id)
	GameLog.event("condition_checked", {
		"type": "quest_stage",
		"quest_id": quest_id,
		"expected": expected_stage,
		"actual": actual_stage,
		"passed": actual_stage == expected_stage
	})
	return actual_stage == expected_stage

func _passes_skill_check_condition(condition: Dictionary) -> bool:
	var skill_id := String(condition.get("skill_id", ""))
	var difficulty := int(condition.get("difficulty", 0))
	if skill_id.is_empty():
		GameLog.warning("DIALOGUE", "skill_check condition missing skill_id", {"condition": condition})
		return false
	var actual := game_state.get_party_skill(skill_id)
	var passed := actual >= difficulty
	GameLog.event("condition_checked", {
		"type": "skill_check",
		"skill_id": skill_id,
		"difficulty": difficulty,
		"actual": actual,
		"passed": passed
	})
	return passed

func _passes_any_condition(conditions: Variant) -> bool:
	if typeof(conditions) != TYPE_ARRAY:
		GameLog.warning("DIALOGUE", "any condition missing conditions list", {"conditions": conditions})
		return false
	for condition in conditions:
		if passes_condition(condition):
			return true
	return false
