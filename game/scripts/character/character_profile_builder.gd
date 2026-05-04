extends RefCounted
class_name CharacterProfileBuilder

const GameLog = preload("res://game/scripts/core/game_log.gd")

static func build_profile(character_name: String, ancestry: Dictionary, background: Dictionary, character_class: Dictionary, trait: Dictionary, creation_data: Dictionary) -> Dictionary:
	var clean_name := character_name.strip_edges()
	if clean_name.is_empty():
		clean_name = "Wanderer"

	var profile := {
		"name": clean_name,
		"ancestry": String(ancestry.get("name", "")),
		"ancestry_id": String(ancestry.get("id", "")),
		"background": String(background.get("name", "")),
		"background_id": String(background.get("id", "")),
		"class": String(character_class.get("name", "")),
		"class_id": String(character_class.get("id", "")),
		"trait": String(trait.get("name", "")),
		"trait_id": String(trait.get("id", "")),
		"origin": String(background.get("name", "")),
		"archetype": String(character_class.get("name", "")),
		"tags": [],
		"attributes": _dictionary_int_copy(creation_data.get("base_attributes", {})),
		"skills": _dictionary_int_copy(creation_data.get("base_skills", {})),
		"compatibility_warnings": []
	}

	var chosen := [ancestry, background, character_class, trait]
	for item in chosen:
		_apply_item(profile, item)
	for item in chosen:
		_check_item_compatibility(profile, item)

	GameLog.info("CHARACTER", "Built character profile", {
		"name": clean_name,
		"ancestry": profile["ancestry"],
		"background": profile["background"],
		"class": profile["class"],
		"trait": profile["trait"],
		"tags": profile["tags"],
		"warnings": profile["compatibility_warnings"]
	})
	return profile

static func is_item_available(existing_tags: Array, item: Dictionary) -> bool:
	for blocked_tag in item.get("blocked_by_tags", []):
		if existing_tags.has(String(blocked_tag)):
			return false
	var required := item.get("requires_any_tags", [])
	if typeof(required) == TYPE_ARRAY and not required.is_empty():
		for tag in required:
			if existing_tags.has(String(tag)):
				return true
		return false
	return true

static func _apply_item(profile: Dictionary, item: Dictionary) -> void:
	for tag in item.get("tags", []):
		var tag_id := String(tag)
		if not tag_id.is_empty() and not profile["tags"].has(tag_id):
			profile["tags"].append(tag_id)
	var modifiers: Dictionary = item.get("modifiers", {})
	_add_modifiers(profile["attributes"], modifiers.get("attributes", {}))
	_add_modifiers(profile["skills"], modifiers.get("skills", {}))

static func _check_item_compatibility(profile: Dictionary, item: Dictionary) -> void:
	var item_name := String(item.get("name", item.get("id", "unknown")))
	for blocked_tag in item.get("blocked_by_tags", []):
		var tag_id := String(blocked_tag)
		if profile["tags"].has(tag_id):
			profile["compatibility_warnings"].append("%s conflicts with tag %s" % [item_name, tag_id])
	var required := item.get("requires_any_tags", [])
	if typeof(required) == TYPE_ARRAY and not required.is_empty():
		for tag in required:
			if profile["tags"].has(String(tag)):
				return
		profile["compatibility_warnings"].append("%s is missing one required theme tag" % item_name)

static func _add_modifiers(target: Dictionary, modifiers: Variant) -> void:
	if typeof(modifiers) != TYPE_DICTIONARY:
		return
	for key in modifiers.keys():
		var stat_id := String(key)
		target[stat_id] = int(target.get(stat_id, 0)) + int(modifiers[key])

static func _dictionary_int_copy(value: Variant) -> Dictionary:
	var result := {}
	if typeof(value) != TYPE_DICTIONARY:
		return result
	for key in value.keys():
		result[String(key)] = int(value[key])
	return result
