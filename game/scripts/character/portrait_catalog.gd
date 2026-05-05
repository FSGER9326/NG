extends RefCounted
class_name PortraitCatalog

const DEFAULT_PORTRAIT_ID := "portrait_weathered_drifter_01"

static func get_portraits(portrait_data: Dictionary) -> Array:
	var source: Variant = portrait_data.get("portraits", [])
	var result: Array = []
	if typeof(source) != TYPE_ARRAY:
		return result
	for portrait in source:
		if typeof(portrait) == TYPE_DICTIONARY:
			result.append(portrait)
	return result

static func find_by_id(portrait_data: Dictionary, portrait_id: String) -> Dictionary:
	for portrait in get_portraits(portrait_data):
		if String(portrait.get("id", "")) == portrait_id:
			return portrait
	return {}

static func find_by_name(portrait_data: Dictionary, portrait_name: String) -> Dictionary:
	for portrait in get_portraits(portrait_data):
		if String(portrait.get("name", "")) == portrait_name:
			return portrait
	return {}

static func get_default_portrait(portrait_data: Dictionary, fallback_id: String = DEFAULT_PORTRAIT_ID) -> Dictionary:
	var explicit := find_by_id(portrait_data, fallback_id)
	if not explicit.is_empty():
		return explicit
	var portraits := get_portraits(portrait_data)
	if portraits.is_empty():
		return {}
	return portraits[0]

static func get_display_name(portrait: Dictionary) -> String:
	return String(portrait.get("name", "Unnamed Portrait"))

static func get_summary(portrait: Dictionary) -> String:
	return String(portrait.get("summary", "No portrait summary available."))

static func apply_to_profile(profile: Dictionary, portrait: Dictionary) -> Dictionary:
	if portrait.is_empty():
		return profile
	var result := profile.duplicate(true)
	var portrait_id := String(portrait.get("id", ""))
	var portrait_name := get_display_name(portrait)
	if not portrait_id.is_empty():
		result["portrait_id"] = portrait_id
	if not portrait_name.is_empty():
		result["portrait"] = portrait_name
	return result
