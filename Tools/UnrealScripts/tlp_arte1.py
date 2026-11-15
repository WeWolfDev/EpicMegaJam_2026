# Importa banderas, queso, jaula, bote y Paco
import unreal, os, zipfile
LOG=[]
def log(*a):
    s=" ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] "+s)
proj=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()); SA=os.path.join(proj,"SourceArt")
DL=r"C:\Users\crod3\Downloads"
# 1. sacar los FBX grandes de los zip de Descargas
for zipn,folder in (("Checkpoitn rojo.zip","Bandera_Roja"),("Checkpoint verde.zip","Bandera_Verde"),("Botesito.zip","Bote")):
    zp=os.path.join(DL,zipn)
    with zipfile.ZipFile(zp) as z:
        for n in z.namelist():
            if n.endswith(".fbx"):
                dst=os.path.join(SA,folder,os.path.basename(n))
                if not os.path.exists(dst):
                    with z.open(n) as src, open(dst,"wb") as out: out.write(src.read())
                log("fbx",folder,os.path.getsize(dst))
for cv in ("Interchange.FeatureFlags.Import.FBX false",):
    unreal.SystemLibrary.execute_console_command(None,cv)
at=unreal.AssetToolsHelpers.get_asset_tools(); EAL=unreal.EditorAssetLibrary; mel=unreal.MaterialEditingLibrary
def imp(fn,dest,opts=None,name=None):
    t=unreal.AssetImportTask(); t.filename=fn; t.destination_path=dest; t.automated=True; t.save=True; t.replace_existing=True
    if name: t.destination_name=name
    if opts: t.options=opts
    at.import_asset_tasks([t]); return [p for p in t.get_editor_property("imported_object_paths")]
def sm_ui():
    o=unreal.FbxImportUI(); o.import_mesh=True; o.import_materials=False; o.import_textures=False; o.import_as_skeletal=False
    o.automated_import_should_detect_type=False; o.mesh_type_to_import=unreal.FBXImportType.FBXIT_STATIC_MESH
    o.static_mesh_import_data.set_editor_property("combine_meshes",True)
    return o
def tex(png,dest,name,normal=False):
    p=imp(png,dest,name=name); t=unreal.load_asset(dest+"/"+name)
    if normal and t:
        t.set_editor_property("compression_settings",unreal.TextureCompressionSettings.TC_NORMALMAP); t.set_editor_property("srgb",False); EAL.save_loaded_asset(t)
    return t
def material(dest,name,bc,nm=None,skel=False):
    path=dest+"/"+name
    m=unreal.load_asset(path) if EAL.does_asset_exist(path) else at.create_asset(name,dest,unreal.Material,unreal.MaterialFactoryNew())
    mel.delete_all_material_expressions(m)
    a=mel.create_material_expression(m,unreal.MaterialExpressionTextureSample,-400,0); a.texture=bc
    mel.connect_material_property(a,"RGB",unreal.MaterialProperty.MP_BASE_COLOR)
    if nm:
        b=mel.create_material_expression(m,unreal.MaterialExpressionTextureSample,-400,300); b.texture=nm; b.sampler_type=unreal.MaterialSamplerType.SAMPLERTYPE_NORMAL
        mel.connect_material_property(b,"RGB",unreal.MaterialProperty.MP_NORMAL)
    r=mel.create_material_expression(m,unreal.MaterialExpressionConstant,-400,500); r.r=0.75
    mel.connect_material_property(r,"",unreal.MaterialProperty.MP_ROUGHNESS)
    if skel: m.set_editor_property("used_with_skeletal_mesh",True); m.set_editor_property("used_with_morph_targets",True)
    mel.recompile_material(m); EAL.save_loaded_asset(m); return m
def setmat(mesh,m):
    if isinstance(mesh,unreal.StaticMesh):
        for i in range(len(mesh.get_editor_property("static_materials"))): mesh.set_material(i,m)
    else:
        mats=mesh.get_editor_property("materials")
        for s in mats: s.set_editor_property("material_interface",m)
        mesh.set_editor_property("materials",mats)
    EAL.save_loaded_asset(mesh)
def first(dest,cls):
    for a in EAL.list_assets(dest,recursive=False):
        o=unreal.load_asset(a.split(".")[0])
        if isinstance(o,cls): return o
ROOT="/Game/TheLastPatch/Props"
props=(("Bandera_Roja","SM_Bandera_Roja","Meshy_AI_red_cheese_flag_20261115_image-to-3d-texture"),
       ("Bandera_Verde","SM_Bandera_Verde","Meshy_AI_cheese_flag_20261115_image-to-3d-texture"),
       ("Bote","SM_Bote","Meshy_AI_retro_wooden_fishing_boat_3d_20261115_image-to-3d-texture"),
       ("Queso","SM_Queso","Meshy_AI_retro_cheese_collectible_3d_20261115_texture"),
       ("Jaula","SM_Jaula","Meshy_AI_retro_stylized_cage_3d_20261115_texture"))
for folder,name,base in props:
    dest=f"{ROOT}/{folder}"
    imp(os.path.join(SA,folder,base+".fbx"),dest,sm_ui(),name)
    sm=unreal.load_asset(dest+"/"+name)
    bc=tex(os.path.join(SA,folder,base+".png"),dest,"T_"+folder+"_BC")
    npng=os.path.join(SA,folder,base+"_normal.png")
    nm=tex(npng,dest,"T_"+folder+"_N",True) if os.path.exists(npng) else None
    m=material(dest,"M_"+folder,bc,nm)
    if sm:
        setmat(sm,m); b=sm.get_bounds(); log(name,"origen",b.origin,"ext",b.box_extent)
    else: log("NO SE IMPORTO",name)
# Paco
PD="/Game/TheLastPatch/Personajes/Paco"; PS=os.path.join(SA,"Paco")
o=unreal.FbxImportUI(); o.import_mesh=True; o.import_materials=False; o.import_textures=False; o.import_as_skeletal=True
o.automated_import_should_detect_type=False; o.mesh_type_to_import=unreal.FBXImportType.FBXIT_SKELETAL_MESH; o.import_animations=False
o.skeletal_mesh_import_data.set_editor_property("import_morph_targets",True)
imp(os.path.join(PS,"SK_Paco.fbx"),PD,o)
skm=first(PD,unreal.SkeletalMesh); skel=first(PD,unreal.Skeleton); log("paco",skm,skel)
for f in sorted(os.listdir(os.path.join(PS,"Animations"))):
    a=unreal.FbxImportUI(); a.import_mesh=False; a.import_materials=False; a.import_textures=False; a.import_as_skeletal=True
    a.automated_import_should_detect_type=False; a.mesh_type_to_import=unreal.FBXImportType.FBXIT_ANIMATION; a.skeleton=skel; a.import_animations=True
    imp(os.path.join(PS,"Animations",f),PD+"/Anims",a,f[:-4])
log("anims paco",EAL.list_assets(PD+"/Anims"))
bc=tex(os.path.join(PS,"Textures","T_Paco_BaseColor.png"),PD,"T_Paco_BaseColor"); nm=tex(os.path.join(PS,"Textures","T_Paco_Normal.png"),PD,"T_Paco_Normal",True)
if skm: setmat(skm,material(PD,"M_Paco",bc,nm,True)); b=skm.get_bounds(); log("paco bounds",b.origin,b.box_extent)
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_arte1.txt"),"w").write("\n".join(str(x) for x in LOG))
