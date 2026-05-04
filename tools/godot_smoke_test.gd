extends SceneTree

func _initialize() -> void:
	print("NG Godot smoke test starting...")
	var main_scene: PackedScene = load("res://game/scenes/main.tscn")
	if main_scene == null:
		push_error("Could not load main scene: res://game/scenes/main.tscn")
		quit(1)
		return

	var area_scene: PackedScene = load("res://game/scenes/area/area_scene.tscn")
	if area_scene == null:
		push_error("Could not load area scene: res://game/scenes/area/area_scene.tscn")
		quit(1)
		return

	var area_instance: Node = area_scene.instantiate()
	if area_instance == null:
		push_error("Could not instantiate area scene.")
		quit(1)
		return

	root.add_child(area_instance)
	await process_frame
	await process_frame

	if not area_instance.has_method("load_area"):
		push_error("Area scene instance does not expose load_area().")
		quit(1)
		return

	area_instance.call("load_area", "wolfpine_road")
	await process_frame

	print("NG Godot smoke test passed.")
	quit(0)
