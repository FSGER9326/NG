$ErrorActionPreference = "Stop"

$blender = "C:\Program Files\Blender Foundation\Blender 5.1\blender.exe"
$scriptDir = Join-Path $env:USERPROFILE ".codex\mcp\blender-mcp"
$scriptPath = Join-Path $scriptDir "start_blender_mcp.py"

if (!(Test-Path -LiteralPath $blender)) {
    throw "Blender executable not found: $blender"
}

New-Item -ItemType Directory -Force -Path $scriptDir | Out-Null

@'
import bpy

try:
    bpy.ops.preferences.addon_enable(module="addon")
except Exception as exc:
    print("Addon enable skipped/failed:", exc)

try:
    prefs = bpy.context.preferences.addons["addon"].preferences
    prefs.telemetry_consent = False
except Exception as exc:
    print("Telemetry preference skipped:", exc)

bpy.context.scene.blendermcp_port = 9876
if not bpy.context.scene.blendermcp_server_running:
    bpy.ops.blendermcp.start_server()
print("Blender MCP socket server requested on port 9876")
'@ | Set-Content -LiteralPath $scriptPath -Encoding UTF8

Start-Process -FilePath $blender -ArgumentList @("--python", $scriptPath) -WorkingDirectory (Resolve-Path ".").Path
Start-Sleep -Seconds 5

$connection = Get-NetTCPConnection -LocalPort 9876 -State Listen -ErrorAction SilentlyContinue
if ($connection) {
    Write-Output "Blender MCP is listening on 127.0.0.1:9876"
} else {
    Write-Warning "Blender started, but port 9876 is not listening yet. In Blender, open the BlenderMCP sidebar and click Connect to MCP server."
}
