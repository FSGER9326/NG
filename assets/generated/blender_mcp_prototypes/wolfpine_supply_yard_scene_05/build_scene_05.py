
import bpy, math, random
from pathlib import Path
from mathutils import Vector

ROOT = Path(r"C:\Users\User\Documents\GitHub\NG")
OUT_DIR = ROOT / "assets" / "generated" / "blender_mcp_prototypes" / "wolfpine_supply_yard_scene_05"
TEX = OUT_DIR / "textures"
random.seed(90519)

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
scene=bpy.context.scene
try: scene.render.engine='BLENDER_EEVEE_NEXT'
except Exception: scene.render.engine='BLENDER_EEVEE'
try:
    scene.eevee.taa_render_samples=96; scene.eevee.use_gtao=True; scene.eevee.gtao_distance=4.4; scene.eevee.gtao_factor=1.7
except Exception: pass
scene.render.resolution_x=1600; scene.render.resolution_y=900; scene.render.film_transparent=False
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
scene.view_settings.view_transform='Standard'; scene.view_settings.look='Medium High Contrast'; scene.view_settings.exposure=-0.04
scene.world.color=(0.050,0.058,0.050)

# Materials.
def img_mat(name, filename, tint=(1,1,1,1), rough=.9, alpha=1.0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    nodes=m.node_tree.nodes; bsdf=nodes.get('Principled BSDF')
    tex=nodes.new('ShaderNodeTexImage'); tex.image=bpy.data.images.load(str(TEX/filename)); tex.extension='REPEAT'
    if tint != (1,1,1,1):
        mix=nodes.new('ShaderNodeMix'); mix.data_type='RGBA'; mix.factor_mode='UNIFORM'; mix.inputs['Factor'].default_value=.22; mix.inputs[6].default_value=tint
        m.node_tree.links.new(tex.outputs['Color'], mix.inputs[7]); m.node_tree.links.new(mix.outputs[2], bsdf.inputs['Base Color'])
    else:
        m.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value=rough
    if alpha < 1:
        bsdf.inputs['Alpha'].default_value=alpha; m.blend_method='BLEND'; m.show_transparent_back=False
    m.diffuse_color=tint
    return m

def flat_mat(name, color, rough=.9, alpha=1.0):
    m=bpy.data.materials.new(name); m.use_nodes=True; bsdf=m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value=color; bsdf.inputs['Roughness'].default_value=rough
    if alpha<1: bsdf.inputs['Alpha'].default_value=alpha; m.blend_method='BLEND'; m.show_transparent_back=False
    m.diffuse_color=color; return m

mud=img_mat('mud_flecked_texture','mud_flecked.png',(0.82,0.78,0.68,1))
dirt=img_mat('packed_dirt_texture','packed_dirt_streaked.png',(0.95,0.91,0.78,1))
grass=img_mat('dark_grass_moss_texture','dark_grass_moss.png',(0.82,0.95,0.78,1))
stone=img_mat('worn_stone_texture','worn_stone.png',(0.90,0.90,0.86,1))
wood=img_mat('weathered_plank_wood_texture','weathered_plank_wood.png',(0.95,0.90,0.82,1))
wood_dark=img_mat('dark_weathered_plank_wood_texture','weathered_plank_wood.png',(0.45,0.36,0.28,1))
roof=img_mat('mossy_slate_roof_texture','mossy_slate_roof.png',(0.82,0.95,0.82,1))
plaster=img_mat('dirty_plaster_texture','dirty_plaster.png',(1.0,0.94,0.84,1))
sack=img_mat('sackcloth_weave_texture','sackcloth_weave.png',(0.95,0.90,0.78,1))
parch=img_mat('damp_parchment_texture','damp_parchment.png',(1,1,1,1))
iron=flat_mat('dull_black_iron',(0.048,0.047,0.044,1),.95)
shadow=flat_mat('transparent_soft_shadow',(0.018,0.016,0.013,.24),1,.24)
seal_red=flat_mat('muted_red_wax',(0.31,.065,.052,1),.9)

# Helpers.
def bevel(o,w=.014,s=2):
    if w>0:
        b=o.modifiers.new('soft_edges','BEVEL'); b.width=w; b.segments=s
    o.modifiers.new('weighted_normals','WEIGHTED_NORMAL'); return o

def cube(name,loc,dims,ma,rz=0,bw=.014):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o=bpy.context.object; o.name=name; o.dimensions=dims; o.rotation_euler[2]=math.radians(rz); o.data.materials.append(ma); bevel(o,bw,2); return o

def cyl(name,loc,r,depth,ma,verts=32,scale=(1,1,1),bw=.006,rz=0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc); o=bpy.context.object; o.name=name; o.scale=scale; o.rotation_euler[2]=math.radians(rz); o.data.materials.append(ma); bevel(o,bw,2); return o

def irregular_blob(name, center, rx, ry, ma, rz=0, points=26, z=.018):
    verts=[(0,0,0)]; faces=[]
    for i in range(points):
        a=math.tau*i/points; wob=random.uniform(.78,1.18)
        verts.append((math.cos(a)*rx*wob, math.sin(a)*ry*wob, 0))
    faces=[tuple([0]+list(range(1,points+1)))]
    mesh=bpy.data.meshes.new(name+'_mesh'); mesh.from_pydata(verts,[],faces); mesh.update()
    o=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(o); o.location=(center[0],center[1],z); o.rotation_euler[2]=math.radians(rz); o.data.materials.append(ma); return o

def sh(name,loc,rx,ry,rz=0): return irregular_blob(name, loc, rx, ry, shadow, rz, 30, .012)

# Terrain: wide, non-stage background.
cols,rows=34,24; sx,sy=16.2,10.3; verts=[]; faces=[]
for j in range(rows+1):
    for i in range(cols+1):
        x=-sx/2+sx*i/cols; y=-sy/2+sy*j/rows; z=-.038+random.uniform(-.004,.004); verts.append((x,y,z))
for j in range(rows):
    for i in range(cols):
        a=j*(cols+1)+i; faces.append((a,a+1,a+cols+2,a+cols+1))
mesh=bpy.data.meshes.new('textured_yard_ground_mesh'); mesh.from_pydata(verts,[],faces); mesh.update(); ground=bpy.data.objects.new('textured_yard_ground',mesh); bpy.context.collection.objects.link(ground); ground.data.materials.append(mud)

# Path and ground layers.
for name,x,y,rx,ry,rz in [('path_west',-3.85,-.86,2.7,.60,-17),('path_center',-.65,-.22,3.7,1.00,-16),('path_east',2.92,.54,2.9,.62,-16)]: irregular_blob(name,(x,y),rx,ry,dirt,rz,34,.020)
for i,(x,y,rx,ry,rz) in enumerate([(-3.35,-1.05,1.40,.045,-17),(-1.9,-.66,1.65,.042,-17),(-.20,-.15,1.85,.045,-17),(1.55,.37,1.40,.040,-17),(3.05,.73,1.10,.038,-17)]): irregular_blob(f'wagon_rut_dark_{i}',(x,y),rx,ry,flat_mat('wet_rut_'+str(i),(0.085,0.064,0.048,1)),rz,18,.033)
for i in range(165):
    pathish = random.random()<.55
    x=random.uniform(-7.2,7.2); y=random.uniform(-4.0,3.8)
    if pathish:
        ma=random.choice([stone,dirt,mud]); rx=random.uniform(.04,.18); ry=random.uniform(.015,.07); z=.034
    else:
        ma=random.choice([grass,mud,stone]); rx=random.uniform(.05,.42); ry=random.uniform(.018,.14); z=.024
    irregular_blob(f'surface_decal_{i:03d}',(x,y),rx,ry,ma,random.uniform(-65,65),random.randint(10,18),z)

# Storehouse facade across rear left: gives scene IE-like architectural context.
cube('storehouse_stone_foundation',(-2.10,2.20,.18),(3.8,.25,.36),stone,0,.012)
cube('storehouse_plaster_wall',(-2.10,2.08,.95),(3.65,.18,1.20),plaster,0,.012)
for i,x in enumerate([-3.68,-2.70,-1.72,-.74]): cube(f'storehouse_vertical_timber_{i}',(x,1.965,.95),(.12,.16,1.28),wood_dark,0,.006)
for i,z in enumerate([.55,1.17]): cube(f'storehouse_horizontal_beam_{i}',(-2.10,1.955,z),(3.82,.15,.12),wood_dark,0,.006)
cube('storehouse_heavy_door',(-.98,1.88,.58),(.58,.10,.90),wood_dark,0,.008)
for i,x in enumerate([-3.15,-2.28]):
    cube(f'small_shutter_window_{i}',(x,1.875,.98),(.42,.08,.30),wood,0,.006)
    cube(f'dark_window_slit_{i}',(x,1.82,.98),(.24,.025,.16),flat_mat('dark_window_'+str(i),(0.028,0.024,0.020,1)),0,.002)
cube('storehouse_mossy_roof',(-2.10,1.82,1.62),(4.20,.78,.13),roof,0,.012)
sh('storehouse_cast_shadow',(-2.1,1.25,.01),2.3,.36,-2)

# Fence continuation to the right, lower priority than facade.
for i,x in enumerate([.25,.95,1.65,2.35,3.05,3.75,4.45,5.15,5.85,6.55]): cube(f'right_fence_post_{i}',(x,2.38,.38),(.065,.080,random.uniform(.54,.74)),wood_dark,random.uniform(-5,5),.006)
for z in [.43,.64]: cube('right_fence_rail_'+str(z),(3.45,2.38,z),(6.70,.064,.070),wood,0,.006)
sh('right_fence_shadow',(3.3,1.86,.01),3.4,.21,-5)

# Notice board in front of storehouse, smaller and textured.
for i,x in enumerate([-4.42,-3.90]): cube(f'notice_post_{i}',(x,.88,.48),(.070,.080,.95),wood_dark,-2+i*3,.006)
cube('weathered_notice_board',(-4.16,.83,.82),(.78,.080,.48),wood,0,.009)
for i,(x,z,dx,dz,rz) in enumerate([(-4.33,.90,.16,.12,-5),(-4.12,.76,.22,.15,2),(-3.92,.94,.15,.11,6),(-4.20,1.02,.12,.09,-3)]): cube(f'notice_parchment_{i}',(x,.766,z),(dx,.010,dz),parch,rz,.002)
for i,(x,z) in enumerate([(-4.02,.85),(-4.30,.98)]): cyl(f'wax_seal_{i}',(x,.757,z),.022,.008,seal_red,12,(1,.35,1),.001)

# Barrels, crates, sacks with image textures.
def barrel(prefix,x,y,sc=.45,rz=0):
    seg=30; rings=[(.08,.31),(.18,.39),(.38,.47),(.72,.54),(1.04,.56),(1.36,.50),(1.58,.40),(1.68,.31)]
    verts=[]; faces=[]; mi=[]
    for z,r in rings:
        for ii in range(seg):
            a=math.tau*ii/seg; verts.append((math.cos(a)*r*sc,math.sin(a)*r*sc,z*sc))
    for rr in range(len(rings)-1):
        for ii in range(seg): faces.append((rr*seg+ii,rr*seg+(ii+1)%seg,(rr+1)*seg+(ii+1)%seg,(rr+1)*seg+ii)); mi.append(0 if ii%5 not in (0,1) else 1)
    top=len(verts); verts.append((0,0,rings[-1][0]*sc)); bottom=len(verts); verts.append((0,0,rings[0][0]*sc))
    for ii in range(seg): faces.append(((len(rings)-1)*seg+ii,(len(rings)-1)*seg+(ii+1)%seg,top)); mi.append(2); faces.append((ii,bottom,(ii+1)%seg)); mi.append(1)
    mesh=bpy.data.meshes.new(prefix+'_mesh'); mesh.from_pydata(verts,[],faces); mesh.update(); body=bpy.data.objects.new(prefix+'_body',mesh); bpy.context.collection.objects.link(body); body.location=(x,y,0); body.rotation_euler[2]=math.radians(rz)
    for m in (wood,wood_dark,wood): body.data.materials.append(m)
    for p,idx in zip(body.data.polygons,mi): p.material_index=idx; p.use_smooth=True
    bevel(body,.006,2)
    for k,(z,r) in enumerate([(.36,.475),(.92,.555),(1.43,.455)]):
        bpy.ops.mesh.primitive_torus_add(major_radius=r*sc,minor_radius=.010*sc,major_segments=48,minor_segments=8,location=(x,y,z*sc)); h=bpy.context.object; h.name=f'{prefix}_iron_hoop_{k}'; h.rotation_euler[2]=math.radians(rz); h.data.materials.append(iron)
    sh(prefix+'_shadow',(x+.02,y-.032,.010),.29*sc,.21*sc,rz)

barrel('front_supply_barrel',-.90,-.93,.47,-8); barrel('back_storehouse_barrel',-2.20,.65,.36,9); barrel('right_small_barrel',2.85,.28,.36,13)
sh('supply_cluster_shadow',(.74,-.58,.01),.78,.40,-12)
for i,(loc,dims,rz) in enumerate([((.32,-.66,.17),(.42,.36,.30),-8),((.85,-.54,.15),(.34,.30,.26),4),((.64,-.93,.12),(.30,.27,.21),15),((1.20,-.82,.11),(.30,.24,.20),-11)]):
    cube(f'textured_crate_{i}',loc,dims,wood,rz,.009); cube(f'textured_crate_band_{i}',(loc[0],loc[1]-.01,loc[2]+dims[2]*.10),(dims[0]*1.02,.012,.024),wood_dark,rz,.001)
for i,(x,y,z,a,b,c,rz) in enumerate([(1.38,-.86,.12,.28,.21,.18,5),(1.58,-.55,.13,.26,.20,.20,-13),(1.83,-.72,.10,.22,.18,.16,18),(.98,-1.13,.09,.20,.16,.14,-8)]):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.35,location=(x,y,z)); s=bpy.context.object; s.name=f'textured_sack_{i}'; s.scale=(a,b,c); s.rotation_euler[2]=math.radians(rz); s.data.materials.append(sack); bevel(s,.002,1)

# Firewood and foreground clutter.
sh('firewood_shadow',(-1.16,.96,.01),.38,.17,-6)
for i in range(12):
    x=-1.48+(i%6)*.14; z=.080+(i//6)*.078; y=.97+(i%2)*.027
    log=cyl(f'firewood_log_{i}',(x,y,z),.028,.40,wood,10,bw=.003); log.rotation_euler[1]=math.radians(86); log.rotation_euler[2]=math.radians(-11+i*2.4)
cube('discarded_plank',(2.30,-1.08,.050),(.76,.050,.038),wood_dark,16,.005); cube('discarded_branch',(2.10,-.99,.042),(.50,.028,.028),grass,-8,.003)

# Foreground branch occluders at edges.
for i,(x,y,z,dx,rz) in enumerate([(-5.8,-2.88,1.10,1.10,-18),(5.8,-2.70,.94,.95,21)]):
    cube(f'foreground_branch_{i}',(x,y,z),(dx,.060,.045),wood_dark,rz,.012)
    for n in range(8): cube(f'foreground_needles_{i}_{n}',(x+(n-3.5)*.10,y-.030,z-.050-(n%2)*.020),(.18,.023,.023),grass,rz+35-(n%3)*24,.003)

# Lighting and camera.
bpy.ops.object.light_add(type='AREA',location=(-4.8,-5.2,7.5)); key=bpy.context.object; key.name='soft_upper_left_overcast'; key.data.energy=720; key.data.size=8.0
bpy.ops.object.light_add(type='POINT',location=(-1.1,1.3,1.6)); glow=bpy.context.object; glow.name='subtle_warm_storehouse_bounce'; glow.data.energy=18; glow.data.color=(1,.62,.34)
bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='IE_area_plate_camera'; cam.data.type='ORTHO'; cam.data.ortho_scale=6.80; cam.location=(5.05,-7.05,4.75); direction=Vector((0,0,.52))-cam.location; cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler(); scene.camera=cam
for name,loc in [('HOTSPOT_notice_board',(-4.16,.83,.2)),('HOTSPOT_supply_cluster',(.80,-.65,.2)),('HOTSPOT_storehouse_door',(-.98,1.88,.2)),('WALKABLE_path_center',(-.35,-.12,.05)),('OCCLUDER_foreground_branches',(0,-2.80,1.0))]: bpy.ops.object.empty_add(type='PLAIN_AXES',location=loc); bpy.context.object.name=name

scene.render.filepath=str(OUT_DIR/'wolfpine_supply_yard_scene_05_raw.png')
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=str(OUT_DIR/'wolfpine_supply_yard_scene_05.blend'))
print(f"WROTE {OUT_DIR / 'wolfpine_supply_yard_scene_05_raw.png'}")
print(f"WROTE {OUT_DIR / 'wolfpine_supply_yard_scene_05.blend'}")
print(f"OBJECTS {len(bpy.context.scene.objects)}")
