extends Node2D
class_name IsoPlaceholderMap

const TILE_W := 96.0
const TILE_H := 48.0
const ORIGIN := Vector2(640, 150)

func _ready() -> void:
	z_index = -10
	queue_redraw()

func _draw() -> void:
	_draw_ground_plate()
	_draw_road()
	_draw_forest_edges()
	_draw_old_shrine()
	_draw_wagon_ruts()
	_draw_vignette()

func _iso_to_screen(x: float, y: float) -> Vector2:
	return ORIGIN + Vector2((x - y) * TILE_W * 0.5, (x + y) * TILE_H * 0.5)

func _diamond(center: Vector2, w: float = TILE_W, h: float = TILE_H) -> PackedVector2Array:
	return PackedVector2Array([
		center + Vector2(0, -h * 0.5),
		center + Vector2(w * 0.5, 0),
		center + Vector2(0, h * 0.5),
		center + Vector2(-w * 0.5, 0)
	])

func _draw_ground_plate() -> void:
	for x in range(-6, 7):
		for y in range(-4, 9):
			var center := _iso_to_screen(x, y)
			var tone := 0.02 * float((x + y) % 3)
			var color := Color(0.16 + tone, 0.19 + tone, 0.15 + tone, 1.0)
			draw_colored_polygon(_diamond(center), color)
			draw_polyline(_diamond(center), Color(0.08, 0.10, 0.08, 0.32), 1.0, true)

func _draw_road() -> void:
	var road_points := PackedVector2Array([
		_iso_to_screen(-6, 7),
		_iso_to_screen(-4, 7.8),
		_iso_to_screen(-1, 6.8),
		_iso_to_screen(2, 6.1),
		_iso_to_screen(5.6, 4.3),
		_iso_to_screen(6.2, 3.0),
		_iso_to_screen(3.2, 4.5),
		_iso_to_screen(0.2, 5.0),
		_iso_to_screen(-3.6, 6.2),
		_iso_to_screen(-6.4, 6.1)
	])
	draw_colored_polygon(road_points, Color(0.25, 0.22, 0.16, 0.95))
	draw_polyline(road_points, Color(0.10, 0.08, 0.05, 0.45), 2.0, true)

func _draw_forest_edges() -> void:
	for i in range(11):
		_draw_pine(_iso_to_screen(-6.0 + i * 0.9, 1.1 + sin(i) * 0.25), 1.0 + float(i % 3) * 0.15)
	for i in range(9):
		_draw_pine(_iso_to_screen(3.5 + float(i) * 0.35, 0.5 + float(i) * 0.7), 0.9 + float(i % 2) * 0.2)

func _draw_pine(base: Vector2, scale: float) -> void:
	var trunk_h := 22.0 * scale
	var crown_h := 56.0 * scale
	draw_rect(Rect2(base + Vector2(-3 * scale, -trunk_h), Vector2(6 * scale, trunk_h)), Color(0.16, 0.10, 0.06, 1.0))
	for layer in range(3):
		var y := base.y - trunk_h - float(layer) * crown_h * 0.25
		var w := (42.0 - float(layer) * 8.0) * scale
		var h := 34.0 * scale
		var tri := PackedVector2Array([
			Vector2(base.x, y - h),
			Vector2(base.x + w * 0.5, y),
			Vector2(base.x - w * 0.5, y)
		])
		draw_colored_polygon(tri, Color(0.06, 0.13 + float(layer) * 0.015, 0.08, 0.98))

func _draw_old_shrine() -> void:
	var p := Vector2(650, 355)
	draw_colored_polygon(PackedVector2Array([
		p + Vector2(-32, 18), p + Vector2(0, 0), p + Vector2(38, 16), p + Vector2(5, 34)
	]), Color(0.26, 0.25, 0.22, 1.0))
	draw_rect(Rect2(p + Vector2(-10, -44), Vector2(22, 46)), Color(0.30, 0.29, 0.25, 1.0))
	draw_rect(Rect2(p + Vector2(-18, -54), Vector2(38, 12)), Color(0.18, 0.17, 0.15, 1.0))
	draw_line(p + Vector2(-4, -26), p + Vector2(9, -12), Color(0.10, 0.09, 0.08, 0.9), 3.0)
	draw_line(p + Vector2(9, -26), p + Vector2(-5, -12), Color(0.10, 0.09, 0.08, 0.9), 3.0)

func _draw_wagon_ruts() -> void:
	var a := _iso_to_screen(-0.5, 6.2)
	var b := _iso_to_screen(3.4, 4.7)
	var c := _iso_to_screen(-0.1, 6.55)
	var d := _iso_to_screen(3.8, 5.05)
	draw_line(a, b, Color(0.08, 0.06, 0.04, 0.55), 3.0)
	draw_line(c, d, Color(0.08, 0.06, 0.04, 0.55), 3.0)

func _draw_vignette() -> void:
	draw_rect(Rect2(Vector2.ZERO, Vector2(1280, 720)), Color(0.02, 0.03, 0.025, 0.18), false, 32.0)
