extends RefCounted
class_name GameLog

static var _started: bool = false
static var _start_msec: int = 0
static var _log_dir: String = ""

static func start_session(session_name: String = "manual") -> void:
	_start_msec = Time.get_ticks_msec()
	_log_dir = _resolve_log_dir()
	_ensure_dir(_log_dir)
	_write_file(_path("game.log"), "")
	_write_file(_path("actions.jsonl"), "")
	_started = true
	info("BOOT", "NG log session started: %s" % session_name, {"session": session_name, "log_dir": _log_dir})

static func info(category: String, message: String, data: Dictionary = {}) -> void:
	_ensure_started()
	var elapsed := _elapsed_seconds()
	var line := "[%08.3f] %s: %s" % [elapsed, category, message]
	_append_file(_path("game.log"), line + "\n")
	print(line)
	var event_data := data.duplicate(true)
	event_data["category"] = category
	event_data["message"] = message
	event("log", event_data)

static func warning(category: String, message: String, data: Dictionary = {}) -> void:
	var payload := data.duplicate(true)
	payload["level"] = "warning"
	info(category, "WARNING: %s" % message, payload)

static func error(category: String, message: String, data: Dictionary = {}) -> void:
	var payload := data.duplicate(true)
	payload["level"] = "error"
	info(category, "ERROR: %s" % message, payload)

static func event(event_type: String, data: Dictionary = {}) -> void:
	_ensure_started()
	var payload := data.duplicate(true)
	payload["time"] = _elapsed_seconds()
	payload["type"] = event_type
	_append_file(_path("actions.jsonl"), JSON.stringify(payload) + "\n")

static func write_state_dump(file_name: String, data: Dictionary) -> void:
	_ensure_started()
	_write_file(_path(file_name), JSON.stringify(data, "  "))
	info("STATE", "Wrote state dump: %s" % file_name, {"file": file_name})

static func get_log_dir() -> String:
	_ensure_started()
	return _log_dir

static func _ensure_started() -> void:
	if not _started:
		start_session("auto")

static func _resolve_log_dir() -> String:
	var env_dir := OS.get_environment("NG_DEBUG_DIR")
	if not env_dir.is_empty():
		return env_dir.replace("\\", "/")
	return ProjectSettings.globalize_path("user://logs/latest")

static func _path(file_name: String) -> String:
	return "%s/%s" % [_log_dir, file_name]

static func _ensure_dir(path: String) -> void:
	DirAccess.make_dir_recursive_absolute(path)

static func _write_file(path: String, text: String) -> void:
	var file := FileAccess.open(path, FileAccess.WRITE)
	if file == null:
		push_warning("Could not write file: %s" % path)
		return
	file.store_string(text)
	file.close()

static func _append_file(path: String, text: String) -> void:
	if not FileAccess.file_exists(path):
		_write_file(path, "")
	var file := FileAccess.open(path, FileAccess.READ_WRITE)
	if file == null:
		push_warning("Could not append file: %s" % path)
		return
	file.seek_end()
	file.store_string(text)
	file.close()

static func _elapsed_seconds() -> float:
	if _start_msec <= 0:
		return 0.0
	return float(Time.get_ticks_msec() - _start_msec) / 1000.0
