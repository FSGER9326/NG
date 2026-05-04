extends Node2D

const DataLoader = preload("res://game/scripts/core/data_loader.gd")

var data_loader: DataLoader

func _ready() -> void:
	print("NG booting...")
	data_loader = DataLoader.new()
	var load_result := data_loader.load_bootstrap_data()
	print("Loaded bootstrap data: %s" % str(load_result))
