import bpy, math, random
from pathlib import Path
from mathutils import Vector

ROOT = Path(r"C:\Users\User\Documents\GitHub\NG")
OUT_DIR = ROOT / "assets" / "generated" / "blender_mcp_prototypes" / "wolfpine_shrine_crossing_scene_08"
TEX = OUT_DIR / "textures"
OUT_DIR.mkdir(parents=True, exist_ok=True)
random.seed(8061908)

bpy.ops.object.select_all(action="SELECT")
bpy.ops.object.delete()
scene = bpy.context.scene
try:
    scene.render.engine = "BLENDER_EEVEE_NEXT"
except Exception:
    scene.render.engine = "BLENDER_EEVEE"
try:
    scene.eevee.taa_render_samples = 80
    scene.eevee.use_gtao = True
    scene.eevee.gtao_distance = 3.4
    scene.eevee.gtao_factor = 1.15
except Exception:
    pass
scene.render.resolution_x = 1600
scene.render.resolution_y = 900
scene.render.image_settings.file_format = "PNG"
scene.render.image_settings.color_mode = "RGBA"
scene.view_settings.view_transform = "Standard"
scene.view_settings.look = "Medium High Contrast"
scene.view_settings.exposure = 0.22
scene.view_settings.gamma = 0.96
scene.world.color = (0.16, 0.165, 0.145)

def img_mat(name, filename, rough=.93, tint=(1, 1, 1, 1)):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    bsdf = nodes.get("Principled BSDF")
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = bpy.data.images.load(str(TEX / filename))
    tex.extension = "REPEAT"
    if tint != (1, 1, 1, 1):
        rgb = nodes.new("ShaderNodeRGB")
        rgb.outputs["Color"].default_value = tint
        mix = nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs["Factor"].default_value = 1.0
        mat.node_tree.links.new(tex.outputs["Color"], mix.inputs[6])
        mat.node_tree.links.new(rgb.outputs["Color"], mix.inputs[7])
        mat.node_tree.links.new(mix.outputs[2], bsdf.inputs["Base Color"])
    else:
        mat.node_tree.links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    bsdf.inputs["Roughness"].default_value = rough
    return mat

def flat(name, color, rough=.9, alpha=1):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    bsdf.inputs["Base Color"].default_value = color
    bsdf.inputs["Roughness"].default_value = rough
    if alpha < 1:
        bsdf.inputs["Alpha"].default_value = alpha
        mat.blend_method = "BLEND"
        mat.show_transparent_back = False
    mat.diffuse_color = color
    return mat

mud = img_mat("rutted_clay_mud", "rutted_clay_mud.png", .95, (1.02, .98, .92, 1))
path = img_mat("packed_yellow_path", "packed_yellow_path.png", .94, (.74, .69, .55, 1))
water = img_mat("dark_creek_water", "dark_creek_water.png", .86, (.66, .82, .86, 1))
stone = img_mat("mossy_ashlar_stone", "mossy_ashlar_stone.png", .93, (.97, 1.01, .94, 1))
wood = img_mat("split_weathered_wood", "split_weathered_wood.png", .91, (1.03, .94, .86, 1))
wood_dark = img_mat("dark_split_weathered_wood", "split_weathered_wood.png", .94, (.60, .52, .46, 1))
weeds = img_mat("leaf_litter_weeds", "leaf_litter_weeds.png", .98, (.88, 1.03, .86, 1))
plaster = img_mat("stained_ochre_plaster", "stained_ochre_plaster.png", .94, (1.04, .99, .88, 1))
thatch = img_mat("damp_thatch_straw", "damp_thatch_straw.png", .96, (.92, .88, .72, 1))
canvas = img_mat("mildewed_canvas", "mildewed_canvas.png", .98, (.92, .98, .86, 1))
iron = flat("dull_brown_iron", (.065, .057, .048, 1), .95)
shadow = flat("painted_transparent_shadow", (.022, .018, .014, .18), 1, .18)
dark = flat("deep_recess", (.045, .038, .031, 1), .96)
ember = flat("lantern_ember", (.90, .42, .13, 1), .8)

def bevel(obj, width=.012, seg=2):
    if width:
        mod = obj.modifiers.new("soft_bevel", "BEVEL")
        mod.width = width
        mod.segments = seg
    obj.modifiers.new("weighted_normals", "WEIGHTED_NORMAL")
    return obj

def cube(name, loc, dims, mat, rz=0, bw=.012):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dims
    obj.rotation_euler[2] = math.radians(rz)
    obj.data.materials.append(mat)
    bevel(obj, bw, 2)
    return obj

def cyl(name, loc, radius, depth, mat, verts=24, rz=0, bw=.006, scale=(1, 1, 1)):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=radius, depth=depth, location=loc)
    obj = bpy.context.object
    obj.name = name
    obj.rotation_euler[2] = math.radians(rz)
    obj.scale = scale
    obj.data.materials.append(mat)
    bevel(obj, bw, 2)
    return obj

def blob(name, center, rx, ry, mat, rz=0, points=30, z=.018, wobble=.18):
    verts = [(0, 0, 0)]
    for i in range(points):
        a = math.tau * i / points
        wob = 1 + random.uniform(-wobble, wobble)
        verts.append((math.cos(a) * rx * wob, math.sin(a) * ry * wob, 0))
    mesh = bpy.data.meshes.new(name + "_mesh")
    mesh.from_pydata(verts, [], [tuple([0] + list(range(1, points + 1)))])
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    obj.location = (center[0], center[1], z)
    obj.rotation_euler[2] = math.radians(rz)
    obj.data.materials.append(mat)
    return obj

def sh(name, loc, rx, ry, rz=0):
    return blob(name, loc, rx, ry, shadow, rz, 28, .010, .12)

# Terrain base.
cols, rows = 42, 28
sx, sy = 23.0, 15.0
verts, faces = [], []
for j in range(rows + 1):
    for i in range(cols + 1):
        x = -sx / 2 + sx * i / cols
        y = -sy / 2 + sy * j / rows
        z = -0.045 + random.uniform(-.006, .006)
        verts.append((x, y, z))
for j in range(rows):
    for i in range(cols):
        a = j * (cols + 1) + i
        faces.append((a, a + 1, a + cols + 2, a + cols + 1))
mesh = bpy.data.meshes.new("crossing_ground_mesh")
mesh.from_pydata(verts, [], faces)
mesh.update()
ground = bpy.data.objects.new("continuous_muddy_ground", mesh)
bpy.context.collection.objects.link(ground)
ground.data.materials.append(mud)

# Creek, banks, and walkable path.
blob("diagonal_dark_creek", (-.20, .20), 5.45, .58, water, -18, 42, .021, .10)
blob("near_bank_wet_mud", (-.45, -.18), 5.25, .18, mud, -18, 34, .031, .13)
blob("far_bank_wet_mud", (.05, .61), 5.10, .16, mud, -18, 34, .031, .13)
for name, x, y, rx, ry, rz in [
    ("lower_left_path", -3.55, -1.95, 2.75, .82, -17),
    ("bridge_approach", -.74, -.91, 2.30, .58, -17),
    ("upper_right_path", 2.65, .98, 2.85, .70, -17),
    ("shrine_forecourt", 3.55, 1.80, 1.35, .70, -8),
]:
    blob(name, (x, y), rx, ry, path, rz, 38, .035, .15)
for i, (x, y, rx, ry) in enumerate([(-2.9, -1.75, 1.1, .035), (-1.5, -1.28, 1.2, .032), (.45, -.62, 1.1, .03), (2.25, .42, 1.25, .035), (3.85, 1.34, .70, .035)]):
    blob("muddy_foot_rut_%02d" % i, (x, y), rx, ry, flat("rut_dark_%02d" % i, (.068, .052, .038, 1)), -17, 18, .045, .08)

# Densify the ground with painted decals and scatter.
for i in range(210):
    x = random.uniform(-7.9, 7.8)
    y = random.uniform(-4.7, 4.4)
    creekish = abs((y - .18) - .32 * x) < .50
    pathish = abs((y + 1.0) - .32 * x) < .92 or (x > 2.4 and y > 1.0)
    if creekish:
        mat = random.choice([stone, weeds, mud])
        rx, ry, z = random.uniform(.03, .20), random.uniform(.012, .055), .048
    elif pathish:
        mat = random.choice([path, mud, stone])
        rx, ry, z = random.uniform(.035, .17), random.uniform(.012, .06), .049
    else:
        mat = random.choice([weeds, mud, stone])
        rx, ry, z = random.uniform(.05, .38), random.uniform(.014, .13), .033
    blob("ground_detail_%03d" % i, (x, y), rx, ry, mat, random.uniform(-70, 70), random.randint(10, 18), z, .22)

# Stone bridge: low, playable, silhouette readable.
for i, x in enumerate([-1.20, -.60, 0, .60, 1.20]):
    cube("bridge_slab_%02d" % i, (x, -.25 + x * .32, .105), (.64, .44, .10), wood, -18 + random.uniform(-2, 2), .010)
cube("bridge_left_low_curb", (-.18, -.76, .185), (2.95, .055, .080), wood_dark, -18, .005)
cube("bridge_right_low_curb", (.18, .24, .185), (2.95, .055, .080), wood_dark, -18, .005)
for i, x in enumerate([-1.35, -.45, .45, 1.35]):
    cube("bridge_short_post_%02d" % i, (x, -.74 + x * .32, .31), (.055, .060, .32), wood_dark, -18, .004)
    cube("bridge_far_short_post_%02d" % i, (x, .24 + x * .32, .31), (.055, .060, .28), wood_dark, -18, .004)
for x in [-1.40, -.78, -.16, .46, 1.08]:
    sh("bridge_slab_shadow_%s" % str(x).replace(".", "_"), (x, -.36 + x * .32, .01), .44, .18, -18)

# Shrine and ruin cluster.
cube("shrine_stone_plinth", (3.38, 2.05, .19), (1.20, .68, .30), stone, -8, .014)
cube("shrine_back_wall", (3.52, 2.38, .82), (1.10, .14, 1.10), plaster, -8, .010)
cube("shrine_inner_shadow", (3.54, 2.31, .76), (.58, .035, .62), dark, -8, .002)
cube("shrine_roof_left", (3.18, 2.34, 1.42), (.78, .46, .10), thatch, -22, .009)
cube("shrine_roof_right", (3.83, 2.30, 1.40), (.72, .42, .10), thatch, 7, .009)
for i, x in enumerate([3.02, 4.03]):
    cyl("shrine_column_%02d" % i, (x, 2.22, .68), .075, 1.0, stone, 18, 0, .008, (1, .85, 1))
cube("offering_stone", (3.42, 1.74, .36), (.46, .25, .18), stone, -8, .006)
for i, (x, y, z) in enumerate([(3.20, 1.68, .50), (3.65, 1.73, .47), (3.48, 1.56, .44)]):
    cyl("small_candle_%02d" % i, (x, y, z), .025, .09, ember, 12, 0, .002)
sh("shrine_deep_shadow", (3.40, 1.88, .012), .95, .40, -8)

# Ruined low walls and broken stones.
for i, (x, y, dx, rz) in enumerate([(-4.0, 1.55, 1.45, -12), (-5.25, 1.15, .78, 8), (4.92, 2.72, 1.10, 14), (5.72, 2.35, .62, -7)]):
    cube("broken_wall_%02d" % i, (x, y, .22), (dx, .16, .30), stone, rz, .012)
    for n in range(3):
        cube("wall_fallen_stone_%02d_%02d" % (i, n), (x + random.uniform(-dx*.45, dx*.45), y + random.uniform(-.38, .38), .06), (random.uniform(.16, .38), random.uniform(.09, .18), random.uniform(.055, .11)), stone, random.uniform(-35, 35), .006)

# Camp/travel props.
for i, (x, y, z, rz) in enumerate([(-3.40, -2.32, .15, -12), (-3.00, -2.10, .12, 8), (-2.72, -2.46, .10, 18)]):
    cube("camp_crate_%02d" % i, (x, y, z), (.38, .32, .26), wood, rz, .008)
cube("folded_canvas", (-2.25, -2.18, .08), (.72, .34, .08), canvas, -22, .006)
for i, (x, y, r) in enumerate([(-2.58, -2.78, .18), (-2.18, -2.66, .13), (-1.98, -2.88, .11)]):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16, ring_count=8, radius=.34, location=(x, y, r))
    s = bpy.context.object
    s.name = "travel_sack_%02d" % i
    s.scale = (.28, .20, .17)
    s.rotation_euler[2] = math.radians(random.uniform(-20, 20))
    s.data.materials.append(canvas)
    bevel(s, .002, 1)
sh("camp_shadow", (-2.72, -2.36, .012), 1.05, .46, -18)

# Barrels with slimmer profile.
def barrel(prefix, x, y, sc=.36, rz=0):
    seg = 32
    rings = [(.05, .26), (.16, .35), (.40, .43), (.74, .47), (1.03, .44), (1.28, .35), (1.40, .26)]
    verts, faces, mi = [], [], []
    for z, r in rings:
        for ii in range(seg):
            a = math.tau * ii / seg
            verts.append((math.cos(a) * r * sc, math.sin(a) * r * sc, z * sc))
    for rr in range(len(rings) - 1):
        for ii in range(seg):
            faces.append((rr * seg + ii, rr * seg + (ii + 1) % seg, (rr + 1) * seg + (ii + 1) % seg, (rr + 1) * seg + ii))
            mi.append(0 if ii % 6 else 1)
    top = len(verts); verts.append((0, 0, rings[-1][0] * sc))
    bottom = len(verts); verts.append((0, 0, rings[0][0] * sc))
    for ii in range(seg):
        faces.append(((len(rings) - 1) * seg + ii, (len(rings) - 1) * seg + (ii + 1) % seg, top)); mi.append(0)
        faces.append((ii, bottom, (ii + 1) % seg)); mi.append(1)
    mesh = bpy.data.meshes.new(prefix + "_mesh")
    mesh.from_pydata(verts, [], faces); mesh.update()
    obj = bpy.data.objects.new(prefix, mesh); bpy.context.collection.objects.link(obj)
    obj.location = (x, y, 0); obj.rotation_euler[2] = math.radians(rz)
    obj.data.materials.append(wood); obj.data.materials.append(wood_dark)
    for p, idx in zip(obj.data.polygons, mi):
        p.material_index = idx
        p.use_smooth = True
    bevel(obj, .006, 2)
    for k, (z, r) in enumerate([(.28, .40), (.74, .47), (1.18, .37)]):
        bpy.ops.mesh.primitive_torus_add(major_radius=r * sc, minor_radius=.009 * sc, major_segments=48, minor_segments=8, location=(x, y, z * sc))
        h = bpy.context.object
        h.name = prefix + "_hoop_%02d" % k
        h.data.materials.append(iron)
    sh(prefix + "_shadow", (x + .02, y - .05, .01), .26 * sc, .20 * sc, rz)

barrel("bridge_supply_barrel", -1.58, -.92, .39, -10)
barrel("shrine_side_barrel", 4.62, 1.36, .31, 12)

# Broken wheel and poles for readable prop silhouettes.
cyl("broken_wheel_outer", (-4.05, -2.36, .20), .31, .035, wood_dark, 40, -14, .004, (1, 1, .35))
bpy.context.object.rotation_euler[1] = math.radians(90)
for i in range(6):
    spoke = cube("wheel_spoke_%02d" % i, (-4.05, -2.36, .20), (.55, .025, .025), wood, i * 30 - 14, .002)
    spoke.rotation_euler[1] = math.radians(90)
for i in range(8):
    log = cyl("bank_branch_%02d" % i, (-.25 + i * .18, .92 + random.uniform(-.05, .05), .08 + (i % 2) * .04), .026, .42, wood_dark, 10, 0, .003)
    log.rotation_euler[1] = math.radians(86)
    log.rotation_euler[2] = math.radians(-19 + i * 3)

# Foreground occluders, kept at edge of play space.
for i, (x, y, z, dx, rz) in enumerate([(-6.6, -3.95, .90, 1.45, -22), (5.80, -3.55, .80, 1.15, 16), (-4.85, -4.25, .70, .86, 10)]):
    cube("foreground_branch_%02d" % i, (x, y, z), (dx, .060, .045), wood_dark, rz, .010)
    for n in range(9):
        cube("foreground_leaf_%02d_%02d" % (i, n), (x + (n - 4) * dx / 11, y - .035, z - .055 - (n % 3) * .025), (.20, .026, .020), weeds, rz + random.uniform(-48, 48), .002)

# Fence fragment and signpost for gameplay readability.
for i, x in enumerate([-.10, .55, 1.20]):
    cube("small_fence_post_%02d" % i, (x, 2.72, .36), (.06, .08, .62), wood_dark, random.uniform(-4, 4), .005)
for z in [.46, .64]:
    cube("small_fence_rail_%s" % z, (.55, 2.72, z), (1.50, .055, .055), wood, 0, .004)
cube("weathered_signpost", (-5.75, -.65, .54), (.07, .07, .95), wood_dark, -6, .004)
cube("weathered_signboard", (-5.63, -.72, .82), (.62, .06, .24), wood, -6, .004)

# Lighting/camera.
bpy.ops.object.light_add(type="AREA", location=(-4.5, -5.0, 7.8))
key = bpy.context.object
key.name = "large_overcast_key"
key.data.energy = 1120
key.data.size = 9.5
bpy.ops.object.light_add(type="AREA", location=(4.7, -2.6, 3.9))
fill = bpy.context.object
fill.name = "cool_water_fill"
fill.data.energy = 120
fill.data.size = 8.0
fill.data.color = (.68, .78, 1.0)
bpy.ops.object.light_add(type="POINT", location=(3.36, 1.68, .72))
lamp = bpy.context.object
lamp.name = "tiny_shrine_candle_warmth"
lamp.data.energy = 22
lamp.data.color = (1.0, .48, .18)

bpy.ops.object.camera_add()
cam = bpy.context.object
cam.name = "IE_shrine_crossing_camera"
cam.data.type = "ORTHO"
cam.data.ortho_scale = 8.15
cam.location = (5.85, -7.70, 5.25)
direction = Vector((.88, .34, .40)) - cam.location
cam.rotation_euler = direction.to_track_quat("-Z", "Y").to_euler()
scene.camera = cam

for name, loc in [
    ("HOTSPOT_shrine_offering", (3.42, 1.74, .35)),
    ("HOTSPOT_camp_supplies", (-2.80, -2.35, .2)),
    ("HOTSPOT_weathered_sign", (-5.65, -.70, .2)),
    ("WALKABLE_bridge_crossing", (-.05, -.25, .06)),
    ("OCCLUDER_foreground_branches", (0, -3.90, .8)),
]:
    bpy.ops.object.empty_add(type="PLAIN_AXES", location=loc)
    bpy.context.object.name = name

raw = OUT_DIR / "wolfpine_shrine_crossing_scene_08_raw.png"
blend = OUT_DIR / "wolfpine_shrine_crossing_scene_08.blend"
scene.render.filepath = str(raw)
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(blend))
print("WROTE", raw)
print("WROTE", blend)
print("OBJECTS", len(scene.objects))
bpy.ops.wm.quit_blender()
