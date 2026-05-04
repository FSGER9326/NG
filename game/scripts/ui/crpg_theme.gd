extends RefCounted
class_name CrpgTheme

static func panel_style() -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.08, 0.075, 0.055, 0.92)
	style.border_color = Color(0.55, 0.43, 0.24, 1.0)
	style.set_border_width_all(2)
	style.set_corner_radius_all(4)
	style.content_margin_left = 12
	style.content_margin_top = 10
	style.content_margin_right = 12
	style.content_margin_bottom = 10
	return style

static func panel_dark_style() -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.045, 0.048, 0.04, 0.84)
	style.border_color = Color(0.22, 0.18, 0.10, 1.0)
	style.set_border_width_all(1)
	style.set_corner_radius_all(3)
	style.content_margin_left = 10
	style.content_margin_top = 8
	style.content_margin_right = 10
	style.content_margin_bottom = 8
	return style

static func button_normal_style() -> StyleBoxFlat:
	var style := StyleBoxFlat.new()
	style.bg_color = Color(0.15, 0.13, 0.09, 0.92)
	style.border_color = Color(0.42, 0.32, 0.18, 1.0)
	style.set_border_width_all(1)
	style.set_corner_radius_all(3)
	style.content_margin_left = 8
	style.content_margin_top = 6
	style.content_margin_right = 8
	style.content_margin_bottom = 6
	return style

static func button_hover_style() -> StyleBoxFlat:
	var style := button_normal_style()
	style.bg_color = Color(0.23, 0.18, 0.11, 0.96)
	style.border_color = Color(0.78, 0.62, 0.34, 1.0)
	return style

static func button_pressed_style() -> StyleBoxFlat:
	var style := button_normal_style()
	style.bg_color = Color(0.10, 0.085, 0.06, 1.0)
	style.border_color = Color(0.90, 0.72, 0.38, 1.0)
	return style

static func apply_panel(control: Control) -> void:
	control.add_theme_stylebox_override("panel", panel_style())

static func apply_dark_panel(control: Control) -> void:
	control.add_theme_stylebox_override("panel", panel_dark_style())

static func apply_button(button: Button) -> void:
	button.add_theme_stylebox_override("normal", button_normal_style())
	button.add_theme_stylebox_override("hover", button_hover_style())
	button.add_theme_stylebox_override("pressed", button_pressed_style())
	button.add_theme_color_override("font_color", Color(0.88, 0.82, 0.68, 1.0))
	button.add_theme_color_override("font_hover_color", Color(1.0, 0.92, 0.68, 1.0))
	button.add_theme_color_override("font_pressed_color", Color(1.0, 0.80, 0.42, 1.0))

static func apply_label(label: Label, is_title: bool = false) -> void:
	label.add_theme_color_override("font_color", Color(0.86, 0.80, 0.66, 1.0))
	if is_title:
		label.add_theme_color_override("font_color", Color(0.95, 0.83, 0.48, 1.0))
		label.add_theme_font_size_override("font_size", 18)

static func apply_rich_text(label: RichTextLabel) -> void:
	label.add_theme_color_override("default_color", Color(0.86, 0.80, 0.68, 1.0))
	label.add_theme_color_override("font_selected_color", Color(1.0, 0.93, 0.70, 1.0))
