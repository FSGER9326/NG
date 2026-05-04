extends Node2D

const DataLoader = preload("res://game/scripts/core/data_loader.gd")
const AreaScene = preload("res://game/scenes/area/area_scene.tscn")

var data_loader: DataLoader
var current_area: Node2D

func _ready() -> void:
	print("NG booting...")
	data_loader = DataLoader.new()
	var load_result := data_loader.load_bootstrap_data()
	print("Loaded bootstrap data keys: %s" % str(load_result.keys()))
	_load_start_area()

func _load_start_area() -> void:
	current_area = AreaScene.instantiate()
	current_area.name = "CurrentArea"
	add_child(current_area)
