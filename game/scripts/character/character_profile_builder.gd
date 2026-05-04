extends RefCounted
class_name CharacterProfileBuilder

const GameLog = preload("res://game/scripts/core/game_log.gd")

const TAG_LABELS := {
	"ancestry.elf": "elf ancestry",
	"ancestry.human": "human ancestry",
	"ancestry.dwarf": "dwarf ancestry",
	"ancestry.halfling": "halfling ancestry",
	"age.young": "young character",
	"appearance.fair": "fair appearance",
	"frame.slender": "slender frame",
	"frame.stout": "stout frame",
	"frame.small": "small frame",
	"frame.brawny": "brawny frame",
	"frame.work_hardened": "work-hardened body",
	"class.mage": "mage training",
	"combat.fragile": "fragile arcane training",
	"combat.veteran": "veteran combat history",
	"combat.martial": "martial training",
	"training.martial": "martial background",
	"background.veteran": "war veteran background",
	"background.caravan_guard": "caravan guard background",
	"background.laborer": "laborer background",
	"background.cloister": "cloister education",
	"labor.heavy": "heavy labor history",
	"education.formal": "formal education",
	"social.sheltered": "sheltered upbringing",
	"social.noble": "noble standing",
	"reputation.untrustworthy": "untrustworthy reputation",
	"magic.arcane": "arcane training",
	"occult.marked": "occult mark",
	"temperament.calm": "calm temperament"
}

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
		"portrait_id": _portrait_id_for_background(background),
		"portrait": _portrait_name_for_background(background),
		"tags": [],
		"attributes": _dictionary_int_copy(creation_data.get("base_attributes", {})),
		"skills": _dictionary_int_copy(creation_data.get("base_skills", {})),
		"compatibility_warnings": []
	}

	var context_tags: Array = []
	for item in [ancestry, background, character_class, trait]:
		for reason in get_item_unavailable_reasons(context_tags, item):
			profile["compatibility_warnings"].append(reason)
		_apply_item(profile, item)
		context_tags = profile["tags"].duplicate()

	GameLog.info("CHARACTER", "Built character profile", {
		"name": clean_name,
		"ancestry": profile["ancestry"],
		"background": profile["background"],
		"class": profile["class"],
		"trait": profile["trait"],
		"portrait_id": profile["portrait_id"],
		"tags": profile["tags"],
		"warnings": profile["compatibility_warnings"]
	})
	return profile

static func is_item_available(existing_tags: Array, item: Dictionary) -> bool:
	return get_item_unavailable_reasons(existing_tags, item).is_empty()

static func get_item_unavailable_reasons(existing_tags: Array, item: Dictionary) -> Array[String]:
	var reasons: Array[String] = []
	var item_name := String(item.get("name", item.get("id", "unknown")))
	var blocked_matches := _matching_tags(existing_tags, item.get("blocked_by_tags", []))
	if not blocked_matches.is_empty():
		reasons.append("%s conflicts with %s." % [item_name, _format_tag_list(blocked_matches)])
	var required := item.get("requires_any_tags", [])
	if typeof(required) == TYPE_ARRAY and not required.is_empty():
		var required_matches := _matching_tags(existing_tags, required)
		if required_matches.is_empty():
			reasons.append("%s needs one of these themes: %s." % [item_name, _format_tag_list(required)])
	return reasons

static func _apply_item(profile: Dictionary, item: Dictionary) -> void:
	for tag in item.get("tags", []):
		var tag_id := String(tag)
		if not tag_id.is_empty() and not profile["tags"].has(tag_id):
			profile["tags"].append(tag_id)
	var modifiers: Dictionary = item.get("modifiers", {})
	_add_modifiers(profile["attributes"], modifiers.get("attributes", {}))
	_add_modifiers(profile["skills"], modifiers.get("skills", {}))

static func _matching_tags(existing_tags: Array, query_tags: Variant) -> Array[String]:
	var result: Array[String] = []
	if typeof(query_tags) != TYPE_ARRAY:
		return result
	for tag in query_tags:
		var tag_id := String(tag)
		if existing_tags.has(tag_id) and not result.has(tag_id):
			result.append(tag_id)
	return result

static func _format_tag_list(tags: Variant) -> String:
	if typeof(tags) != TYPE_ARRAY:
		return "unknown themes"
	var labels: Array[String] = []
	for tag in tags:
		labels.append(format_tag(String(tag)))
	if labels.is_empty():
		return "unknown themes"
	return ", ".join(labels)

static func format_tag(tag_id: String) -> String:
	return String(TAG_LABELS.get(tag_id, tag_id.replace(".", " ").replace("_", " ")))

static func _portrait_id_for_background(background: Dictionary) -> String:
	var explicit_id := String(background.get("portrait_id", ""))
	if not explicit_id.is_empty():
		return explicit_id
	match String(background.get("id", "")):
		"background_failed_squire":
			return "portrait_disgraced_squire_01"
		"background_village_outcast":
			return "portrait_village_outcast_01"
		"background_caravan_guard":
			return "portrait_caravan_guard_01"
		_:
			return "portrait_weathered_drifter_01"

static func _portrait_name_for_background(background: Dictionary) -> String:
	match _portrait_id_for_background(background):
		"portrait_disgraced_squire_01":
			return "Disgraced Squire"
		"portrait_village_outcast_01":
			return "Village Outcast"
		"portrait_caravan_guard_01":
			return "Caravan Guard"
		_:
			return "Weathered Drifter"

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
