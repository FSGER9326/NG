
import bpy, math, random
from pathlib import Path
from mathutils import Vector

ROOT = Path(r"C:\Users\User\Documents\GitHub\NG")
OUT_DIR = ROOT / "assets" / "generated" / "blender_mcp_prototypes" / "wolfpine_supply_yard_scene_07"
TEX = ROOT / "assets" / "generated" / "blender_mcp_prototypes" / "wolfpine_supply_yard_scene_05" / "textures"
OUT_DIR.mkdir(parents=True, exist_ok=True)
random.seed(70619)

bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete()
scene=bpy.context.scene
try: scene.render.engine='BLENDER_EEVEE_NEXT'
except Exception: scene.render.engine='BLENDER_EEVEE'
try:
    scene.eevee.taa_render_samples=128; scene.eevee.use_gtao=True; scene.eevee.gtao_distance=3.2; scene.eevee.gtao_factor=1.05
except Exception: pass
scene.render.resolution_x=1600; scene.render.resolution_y=900; scene.render.film_transparent=False
scene.render.image_settings.file_format='PNG'; scene.render.image_settings.color_mode='RGBA'
scene.view_settings.view_transform='Standard'; scene.view_settings.look='Medium High Contrast'; scene.view_settings.exposure=.42; scene.view_settings.gamma=.94
scene.world.color=(0.18,0.19,0.17)

def img_mat(name, filename, rough=.9, darken=1.0):
    m=bpy.data.materials.new(name); m.use_nodes=True
    nodes=m.node_tree.nodes; bsdf=nodes.get('Principled BSDF')
    tex=nodes.new('ShaderNodeTexImage'); tex.image=bpy.data.images.load(str(TEX/filename)); tex.extension='REPEAT'
    if darken != 1.0:
        rgb=nodes.new('ShaderNodeRGB'); rgb.outputs['Color'].default_value=(darken,darken,darken,1)
        mix=nodes.new('ShaderNodeMix'); mix.data_type='RGBA'; mix.blend_type='MULTIPLY'; mix.inputs['Factor'].default_value=1.0
        m.node_tree.links.new(tex.outputs['Color'], mix.inputs[6]); m.node_tree.links.new(rgb.outputs['Color'], mix.inputs[7]); m.node_tree.links.new(mix.outputs[2], bsdf.inputs['Base Color'])
    else:
        m.node_tree.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
    bsdf.inputs['Roughness'].default_value=rough
    return m

def flat(name, color, rough=.9, alpha=1):
    m=bpy.data.materials.new(name); m.use_nodes=True; bsdf=m.node_tree.nodes.get('Principled BSDF')
    bsdf.inputs['Base Color'].default_value=color; bsdf.inputs['Roughness'].default_value=rough
    if alpha<1: bsdf.inputs['Alpha'].default_value=alpha; m.blend_method='BLEND'; m.show_transparent_back=False
    m.diffuse_color=color; return m

mud=img_mat('mud_texture_real','mud_flecked.png',.93,1.08)
dirt=img_mat('packed_dirt_real','packed_dirt_streaked.png',.93,1.12)
grass=img_mat('moss_grass_real','dark_grass_moss.png',.95,1.16)
stone=img_mat('worn_stone_real','worn_stone.png',.91,1.04)
wood=img_mat('weathered_wood_real','weathered_plank_wood.png',.90,1.05)
wood_dark=img_mat('dark_weathered_wood_real','weathered_plank_wood.png',.92,.72)
roof=img_mat('mossy_roof_real','mossy_slate_roof.png',.94,.96)
plaster=img_mat('dirty_plaster_real','dirty_plaster.png',.93,1.05)
sack=img_mat('sackcloth_real','sackcloth_weave.png',.96,1.02)
parch=img_mat('parchment_real','damp_parchment.png',.92,1.04)
iron=flat('dull_black_iron',(0.070,0.068,0.062,1),.95)
shadow=flat('transparent_soft_shadow',(0.026,0.021,0.016,.16),1,.16)
wax=flat('muted_wax',(0.28,.05,.042,1),.9)
dark=flat('near_black_recess',(0.050,0.044,0.036,1),.95)

# Helpers.
def bevel(o,w=.012,s=2):
    if w>0:
        b=o.modifiers.new('soft_edges','BEVEL'); b.width=w; b.segments=s
    o.modifiers.new('weighted_normals','WEIGHTED_NORMAL'); return o

def cube(name,loc,dims,ma,rz=0,bw=.012):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o=bpy.context.object; o.name=name; o.dimensions=dims; o.rotation_euler[2]=math.radians(rz); o.data.materials.append(ma); bevel(o,bw,2); return o

def cyl(name,loc,r,depth,ma,verts=32,scale=(1,1,1),bw=.006,rz=0):
    bpy.ops.mesh.primitive_cylinder_add(vertices=verts, radius=r, depth=depth, location=loc); o=bpy.context.object; o.name=name; o.scale=scale; o.rotation_euler[2]=math.radians(rz); o.data.materials.append(ma); bevel(o,bw,2); return o

def blob(name,center,rx,ry,ma,rz=0,points=26,z=.018):
    verts=[(0,0,0)]
    for i in range(points):
        a=math.tau*i/points; wob=random.uniform(.80,1.16); verts.append((math.cos(a)*rx*wob, math.sin(a)*ry*wob, 0))
    mesh=bpy.data.meshes.new(name+'_mesh'); mesh.from_pydata(verts,[],[tuple([0]+list(range(1,points+1)))]); mesh.update()
    o=bpy.data.objects.new(name,mesh); bpy.context.collection.objects.link(o); o.location=(center[0],center[1],z); o.rotation_euler[2]=math.radians(rz); o.data.materials.append(ma); return o

def sh(name,loc,rx,ry,rz=0): return blob(name,loc,rx,ry,shadow,rz,30,.012)

# Ground.
cols,rows=36,24; sx,sy=16.4,10.4; verts=[]; faces=[]
for j in range(rows+1):
    for i in range(cols+1):
        x=-sx/2+sx*i/cols; y=-sy/2+sy*j/rows; z=-.038+random.uniform(-.004,.004); verts.append((x,y,z))
for j in range(rows):
    for i in range(cols):
        a=j*(cols+1)+i; faces.append((a,a+1,a+cols+2,a+cols+1))
mesh=bpy.data.meshes.new('ground_mesh'); mesh.from_pydata(verts,[],faces); mesh.update(); ground=bpy.data.objects.new('continuous_textured_mud_ground',mesh); bpy.context.collection.objects.link(ground); ground.data.materials.append(mud)
for name,x,y,rx,ry,rz in [('path_left',-3.95,-.86,2.7,.58,-17),('path_center',-.75,-.24,3.7,.94,-16),('path_right',2.70,.48,2.7,.58,-16)]: blob(name,(x,y),rx,ry,dirt,rz,34,.020)
for i,(x,y,rx,ry,rz) in enumerate([(-3.4,-1.05,1.35,.040,-17),(-2.0,-.65,1.62,.038,-17),(-.24,-.14,1.78,.040,-17),(1.38,.35,1.34,.037,-17),(2.82,.72,1.04,.034,-17)]): blob(f'dark_wagon_rut_{i}',(x,y),rx,ry,flat('rut_mat_'+str(i),(0.060,0.045,0.034,1)),rz,18,.034)
for i in range(155):
    x=random.uniform(-7.2,7.2); y=random.uniform(-3.9,3.8); pathish=abs((y+.08)-(.20*x))<1.25
    if pathish: ma=random.choice([stone,dirt,mud]); rx=random.uniform(.035,.16); ry=random.uniform(.012,.060); z=.034
    else: ma=random.choice([grass,mud,stone]); rx=random.uniform(.05,.36); ry=random.uniform(.016,.12); z=.024
    blob(f'ground_mark_{i:03d}',(x,y),rx,ry,ma,random.uniform(-65,65),random.randint(10,18),z)

# Architectural anchor: smaller, more complete storehouse facade.
cube('storehouse_stone_foundation',(-2.25,2.12,.18),(3.35,.22,.34),stone,0,.010)
cube('storehouse_plaster_wall',(-2.25,2.02,.86),(3.22,.16,1.04),plaster,0,.010)
for i,x in enumerate([-3.70,-2.75,-1.80,-.86]): cube(f'storehouse_timber_{i}',(x,1.925,.86),(.10,.13,1.10),wood_dark,0,.005)
for i,z in enumerate([.50,1.05]): cube(f'storehouse_beam_{i}',(-2.25,1.915,z),(3.40,.13,.10),wood_dark,0,.005)
cube('storehouse_heavy_door',(-1.03,1.85,.52),(.48,.085,.78),wood_dark,0,.006)
cube('door_worn_threshold',(-1.03,1.78,.12),(.60,.12,.08),stone,0,.004)
for i,x in enumerate([-3.16,-2.30]): cube(f'shutter_window_{i}',(x,1.84,.88),(.34,.065,.25),wood,0,.004); cube(f'black_window_{i}',(x,1.807,.88),(.19,.018,.13),dark,0,.001)
cube('storehouse_mossy_roof',(-2.25,1.76,1.44),(3.75,.64,.11),roof,0,.010)
sh('storehouse_shadow',(-2.3,1.25,.01),2.05,.32,-2)

# Fence right.
for i,x in enumerate([.05,.75,1.45,2.15,2.85,3.55,4.25,4.95,5.65,6.35]): cube(f'fence_post_{i}',(x,2.35,.36),(.058,.075,random.uniform(.50,.68)),wood_dark,random.uniform(-5,5),.005)
for z in [.42,.61]: cube('fence_rail_'+str(z),(3.15,2.34,z),(6.55,.058,.062),wood,0,.005)
sh('fence_shadow',(3.15,1.85,.01),3.2,.18,-5)

# Notice board.
for i,x in enumerate([-4.38,-3.88]): cube(f'notice_post_{i}',(x,.82,.46),(.064,.070,.90),wood_dark,-2+i*3,.005)
cube('notice_board',(-4.13,.78,.78),(.72,.070,.44),wood,0,.007)
for i,(x,z,dx,dz,rz) in enumerate([(-4.28,.86,.15,.11,-5),(-4.10,.73,.20,.13,2),(-3.92,.88,.14,.10,6),(-4.17,.96,.11,.08,-3)]): cube(f'notice_note_{i}',(x,.718,z),(dx,.008,dz),parch,rz,.001)
for i,(x,z) in enumerate([(-4.02,.81),(-4.27,.93)]): cyl(f'wax_{i}',(x,.710,z),.019,.007,wax,12,(1,.35,1),.001)

# Props.
def barrel(prefix,x,y,sc=.43,rz=0):
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
        bpy.ops.mesh.primitive_torus_add(major_radius=r*sc,minor_radius=.010*sc,major_segments=48,minor_segments=8,location=(x,y,z*sc)); h=bpy.context.object; h.name=f'{prefix}_hoop_{k}'; h.rotation_euler[2]=math.radians(rz); h.data.materials.append(iron)
    sh(prefix+'_shadow',(x+.02,y-.032,.010),.29*sc,.21*sc,rz)
barrel('front_barrel',-.90,-.93,.45,-8); barrel('back_barrel',-2.18,.62,.34,9); barrel('right_barrel',2.80,.25,.34,13)
sh('supply_shadow',(.73,-.60,.01),.73,.38,-12)
for i,(loc,dims,rz) in enumerate([((.32,-.66,.17),(.40,.34,.29),-8),((.82,-.55,.15),(.32,.29,.25),4),((.62,-.93,.12),(.29,.26,.20),15),((1.17,-.82,.11),(.28,.23,.19),-11)]): cube(f'crate_{i}',loc,dims,wood,rz,.008); cube(f'crate_band_{i}',(loc[0],loc[1]-.01,loc[2]+dims[2]*.10),(dims[0]*1.02,.010,.022),wood_dark,rz,.001)
for i,(x,y,z,a,b,c,rz) in enumerate([(1.36,-.86,.12,.27,.20,.17,5),(1.55,-.55,.13,.25,.19,.19,-13),(1.80,-.72,.10,.21,.17,.15,18),(.98,-1.13,.09,.19,.15,.13,-8)]):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=16,ring_count=8,radius=.35,location=(x,y,z)); s=bpy.context.object; s.name=f'sack_{i}'; s.scale=(a,b,c); s.rotation_euler[2]=math.radians(rz); s.data.materials.append(sack); bevel(s,.002,1)
sh('firewood_shadow',(-1.16,.96,.01),.36,.16,-6)
for i in range(12):
    x=-1.48+(i%6)*.135; z=.078+(i//6)*.076; y=.97+(i%2)*.026
    log=cyl(f'firewood_{i}',(x,y,z),.027,.37,wood,10,bw=.003); log.rotation_euler[1]=math.radians(86); log.rotation_euler[2]=math.radians(-11+i*2.4)
cube('discarded_plank',(2.28,-1.07,.048),(.72,.045,.035),wood_dark,16,.004); cube('discarded_branch',(2.08,-.98,.040),(.48,.026,.026),grass,-8,.003)
for i,(x,y,z,dx,rz) in enumerate([(-5.75,-2.86,1.06,1.05,-18),(5.70,-2.68,.92,.90,21)]):
    cube(f'foreground_branch_{i}',(x,y,z),(dx,.055,.040),wood_dark,rz,.010)
    for n in range(8): cube(f'foreground_needles_{i}_{n}',(x+(n-3.5)*.10,y-.028,z-.047-(n%2)*.018),(.17,.021,.021),grass,rz+35-(n%3)*24,.003)

# Lighting/camera.
bpy.ops.object.light_add(type='AREA',location=(-4.8,-5.2,7.5)); key=bpy.context.object; key.name='soft_upper_left_daylight'; key.data.energy=1150; key.data.size=8.5
bpy.ops.object.light_add(type='AREA',location=(3.8,-1.8,4.2)); rim=bpy.context.object; rim.name='cool_open_sky_fill'; rim.data.energy=145; rim.data.size=10.0; rim.data.color=(.70,.78,1.0)
bpy.ops.object.light_add(type='POINT',location=(-1.1,1.2,1.6)); fill=bpy.context.object; fill.name='warm_storehouse_bounce'; fill.data.energy=34; fill.data.color=(1,.60,.33)
bpy.ops.object.camera_add(); cam=bpy.context.object; cam.name='IE_area_plate_camera'; cam.data.type='ORTHO'; cam.data.ortho_scale=6.80; cam.location=(5.05,-7.05,4.75); direction=Vector((0,0,.52))-cam.location; cam.rotation_euler=direction.to_track_quat('-Z','Y').to_euler(); scene.camera=cam
for name,loc in [('HOTSPOT_notice_board',(-4.13,.78,.2)),('HOTSPOT_supply_cluster',(.80,-.65,.2)),('HOTSPOT_storehouse_door',(-1.03,1.85,.2)),('WALKABLE_path_center',(-.35,-.12,.05)),('OCCLUDER_foreground_branches',(0,-2.80,1.0))]: bpy.ops.object.empty_add(type='PLAIN_AXES',location=loc); bpy.context.object.name=name
scene.render.filepath=str(OUT_DIR/'wolfpine_supply_yard_scene_07_raw.png'); bpy.ops.render.render(write_still=True); bpy.ops.wm.save_as_mainfile(filepath=str(OUT_DIR/'wolfpine_supply_yard_scene_07.blend'))
print(f"WROTE {OUT_DIR / 'wolfpine_supply_yard_scene_07_raw.png'}")
print(f"WROTE {OUT_DIR / 'wolfpine_supply_yard_scene_07.blend'}")
print(f"OBJECTS {len(bpy.context.scene.objects)}")
