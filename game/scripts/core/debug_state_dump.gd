extends RefCounted
class_name DebugStateDump

static func from_area_controller(area_controller: Node) -> Dictionary:
	var data := {
		"area_id": "",
		"player_position": [],
		"move_target": [],
		"has_move_target": false,
		"active_dialogue_node_id": "",
		"quest_stages": {},
		"active_quest_ids": [],
		"flags": {},
		"faction_reputation": {},
		"hotspot_ids": [],
		"actor_ids": []
	}

	data["area_id"] = String(area_controller.get("area_id"))

	var player_marker: Node = area_controller.get("player_marker")
	if player_marker != null and player_marker is Node2D:
		data["player_position"] = _vec2_to_array((player_marker as Node2D).position)

	data["move_target"] = _vec2_to_array(area_controller.get("move_target"))
	data["has_move_target"] = bool(area_controller.get("has_move_target"))
	data["active_dialogue_node_id"] = String(area_controller.get("active_dialogue_node_id"))

	var game_state = area_controller.get("game_state")
	if game_state != null:
		data["quest_stages"] = game_state.quest_stages.duplicate(true)
		data["active_quest_ids"] = game_state.active_quest_ids.duplicate(true)
		data["flags"] = game_state.flags.duplicate(true)
		data["faction_reputation"] = game_state.faction_reputation.duplicate(true)

	var hotspots_data: Dictionary = area_controller.get("hotspots_data")
	for hotspot in hotspots_data.get("hotspots", []):
		if typeof(hotspot) == TYPE_DICTIONARY:
			data["hotspot_ids"].append(String(hotspot.get("id", "")))

	var actors_data: Dictionary = area_controller.get("actors_data")
	for actor in actors_data.get("actors", []):
		if typeof(actor) == TYPE_DICTIONARY:
			data["actor_ids"].append(String(actor.get("actor_id", "")))

	return data

static func _vec2_to_array(value: Variant) -> Array:
	if value is Vector2:
		return [value.x, value.y]
	return []
