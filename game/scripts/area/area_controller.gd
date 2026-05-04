extends Node2D
class_name AreaController

const DataLoader = preload("res://game/scripts/core/data_loader.gd")

@export var area_id: String = "wolfpine_road"

var data_loader: DataLoader
var area_data: Dictionary = {}
var hotspots_data: Dictionary = {}
var actors_data: Dictionary = {}

var background_layer: ColorRect
var label_layer: Node2D
var hotspot_layer: Node2D
var actor_layer: Node2D
var debug_label: Label

func _ready() -> void:
	data_loader = DataLoader.new()
	_build_runtime_nodes()
	load_area(area_id)

func _build_runtime_nodes() -> void:
	background_layer = ColorRect.new()
	background_layer.name = "PlaceholderBackground"
	background_layer.color = Color(0.12, 0.14, 0.12, 1.0)
	background_layer.position = Vector2.ZERO
	background_layer.size = Vector2(1280, 720)
	add_child(background_layer)

	label_layer = Node2D.new()
	label_layer.name = "LabelLayer"
	add_child(label_layer)

	hotspot_layer = Node2D.new()
	hotspot_layer.name = "HotspotLayer"
	add_child(hotspot_layer)

	actor_layer = Node2D.new()
	actor_layer.name = "ActorLayer"
	add_child(actor_layer)

	debug_label = Label.new()
	debug_label.name = "DebugLabel"
	debug_label.position = Vector2(24, 24)
	debug_label.text = "NG area prototype"
	add_child(debug_label)

func load_area(next_area_id: String) -> void:
	area_id = next_area_id
	var area_path := "res://areas/%s/area.json" % area_id
	area_data = data_loader.load_json_file(area_path)
	if area_data.is_empty():
		_set_debug("Failed to load area: %s" % area_id)
		return

	hotspots_data = data_loader.load_json_file(_to_res_path(String(area_data.get("hotspots", ""))))
	actors_data = data_loader.load_json_file(_to_res_path(String(area_data.get("actors", ""))))
	_render_area()

func _render_area() -> void:
	_clear_layer(label_layer)
	_clear_layer(hotspot_layer)
	_clear_layer(actor_layer)

	var area_name := String(area_data.get("name", area_id))
	var description := String(area_data.get("description", ""))
	_set_debug("Loaded %s\n%s" % [area_name, description])
	_draw_area_title(area_name)
	_draw_hotspots()
	_draw_actors()

func _draw_area_title(area_name: String) -> void:
	var title := Label.new()
	title.name = "AreaTitle"
	title.text = area_name
	title.position = Vector2(24, 64)
	label_layer.add_child(title)

func _draw_hotspots() -> void:
	for hotspot in hotspots_data.get("hotspots", []):
		if typeof(hotspot) != TYPE_DICTIONARY:
			continue
		var marker := Button.new()
		marker.name = "Hotspot_%s" % String(hotspot.get("id", "unknown"))
		marker.text = String(hotspot.get("name", "Hotspot"))
		var pos := _array_to_vec2(hotspot.get("position", [0, 0]))
		marker.position = pos
		marker.size = Vector2(170, 32)
		marker.pressed.connect(_on_hotspot_pressed.bind(hotspot))
		hotspot_layer.add_child(marker)

func _draw_actors() -> void:
	for actor in actors_data.get("actors", []):
		if typeof(actor) != TYPE_DICTIONARY:
			continue
		var marker := Label.new()
		var actor_id := String(actor.get("actor_id", "unknown_actor"))
		marker.name = "Actor_%s" % actor_id
		marker.text = "@ %s" % actor_id
		marker.position = _array_to_vec2(actor.get("position", [0, 0]))
		actor_layer.add_child(marker)

func _on_hotspot_pressed(hotspot: Dictionary) -> void:
	var hotspot_type := String(hotspot.get("type", "inspect"))
	if hotspot_type == "exit":
		var target_area := String(hotspot.get("target_area", ""))
		_set_debug("Exit hotspot selected: %s -> %s" % [String(hotspot.get("name", "Exit")), target_area])
	else:
		_set_debug("Inspect: %s\n%s" % [String(hotspot.get("name", "Hotspot")), String(hotspot.get("description", ""))])

func _set_debug(text: String) -> void:
	if debug_label != null:
		debug_label.text = text
	print(text)

func _clear_layer(layer: Node) -> void:
	for child in layer.get_children():
		child.queue_free()

func _to_res_path(path: String) -> String:
	if path.is_empty():
		return ""
	if path.begins_with("res://"):
		return path
	return "res://%s" % path

func _array_to_vec2(value: Variant) -> Vector2:
	if typeof(value) == TYPE_ARRAY and value.size() >= 2:
		return Vector2(float(value[0]), float(value[1]))
	return Vector2.ZERO
