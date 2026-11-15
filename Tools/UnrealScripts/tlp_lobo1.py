# Importa el lobo (SK, lentes, textura, 9 clips) en /Game/TheLastPatch/Personajes/Lobo
import unreal, os
LOG=[]
def log(*a):
    s=" ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] "+s)
proj=unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
SRC=os.path.join(proj,"SourceArt","Lobo"); DST="/Game/TheLastPatch/Personajes/Lobo"
log("proyecto",proj)
for cv in ("Interchange.FeatureFlags.Import.FBX false","Interchange.FeatureFlags.Import.FBX 0"):
    unreal.SystemLibrary.execute_console_command(None,cv)
at=unreal.AssetToolsHelpers.get_asset_tools(); EAL=unreal.EditorAssetLibrary
def task(fn,dest,opts=None,name=None):
    t=unreal.AssetImportTask(); t.filename=fn; t.destination_path=dest; t.automated=True; t.save=True; t.replace_existing=True
    if name: t.destination_name=name
    if opts: t.options=opts
    return t
def ui(mesh_type,skel=None,import_mesh=True,anim=False):
    o=unreal.FbxImportUI(); o.import_mesh=import_mesh; o.import_materials=False; o.import_textures=False
    o.automated_import_should_detect_type=False; o.mesh_type_to_import=mesh_type
    if mesh_type==unreal.FBXImportType.FBXIT_SKELETAL_MESH:
        o.import_as_skeletal=True; o.import_animations=anim
        sm=o.skeletal_mesh_import_data; sm.set_editor_property("import_morph_targets",True)
        if skel: o.skeleton=skel
    if anim:
        ad=o.anim_sequence_import_data
        for k,v in (("import_custom_attribute",True),("import_meshes_in_bone_hierarchy",False)):
            try: ad.set_editor_property(k,v)
            except Exception as ex: log("animopt",k,ex)
    if mesh_type==unreal.FBXImportType.FBXIT_STATIC_MESH:
        o.import_as_skeletal=False
    return o
# 1. textura
at.import_asset_tasks([task(os.path.join(SRC,"T_Lobo_BaseColor.png"),DST)])
# 2. malla esqueletica
at.import_asset_tasks([task(os.path.join(SRC,"SK_Lobo.fbx"),DST,ui(unreal.FBXImportType.FBXIT_SKELETAL_MESH))])
assets=EAL.list_assets(DST,recursive=False); log("tras SK:",assets)
skm=None; skel=None
for a in assets:
    o=unreal.load_asset(a.split(".")[0])
    if isinstance(o,unreal.SkeletalMesh) and skm is None: skm=o
    if isinstance(o,unreal.Skeleton): skel=o
log("skm",skm,"skel",skel)
if skm:
    try: log("morphs",[m.get_name() for m in skm.get_editor_property("morph_targets")])
    except Exception as ex: log("morphs?",ex)
    b=skm.get_bounds(); log("bounds",b.box_extent,b.origin)
# 3. lentes
at.import_asset_tasks([task(os.path.join(SRC,"SM_Lobo_Glasses.fbx"),DST,ui(unreal.FBXImportType.FBXIT_STATIC_MESH))])
# 4. clips
AD=os.path.join(SRC,"Animations")
loops=("Idle_Smug","Talk","Launched_Tumble","Land_Stuck_Loop","Defeated_Loop")
for f in sorted(os.listdir(AD)):
    if not f.endswith(".fbx") or "RefPose" in f: continue
    o=ui(unreal.FBXImportType.FBXIT_ANIMATION,skel,import_mesh=False,anim=True); o.skeleton=skel; o.import_animations=True
    at.import_asset_tasks([task(os.path.join(AD,f),DST+"/Anims",o,f[:-4])])
anims=EAL.list_assets(DST+"/Anims",recursive=False); log("anims",len(anims),anims)
# 5. material con la textura
tex=unreal.load_asset(DST+"/T_Lobo_BaseColor")
mpath=DST+"/MI_Lobo"
parent=unreal.load_asset("/Game/TheLastPatch/Materiales/M_TLP_OG") or unreal.load_asset("/Game/TheLastPatch/Blockout/M_Blockout")
log("padre material",parent)
if skm and tex:
    mf=unreal.MaterialFactoryNew(); mpath=DST+"/M_Lobo"
    m=unreal.load_asset(mpath) if EAL.does_asset_exist(mpath) else at.create_asset("M_Lobo",DST,unreal.Material,mf)
    mel=unreal.MaterialEditingLibrary
    mel.delete_all_material_expressions(m)
    ts=mel.create_material_expression(m,unreal.MaterialExpressionTextureSample,-300,0); ts.texture=tex
    mel.connect_material_property(ts,"RGB",unreal.MaterialProperty.MP_BASE_COLOR)
    r=mel.create_material_expression(m,unreal.MaterialExpressionConstant,-300,200); r.r=0.8
    mel.connect_material_property(r,"",unreal.MaterialProperty.MP_ROUGHNESS)
    m.set_editor_property("used_with_skeletal_mesh",True); m.set_editor_property("used_with_morph_targets",True)
    mel.recompile_material(m); EAL.save_loaded_asset(m)
    mats=skm.get_editor_property("materials")
    for sm in mats: sm.set_editor_property("material_interface",m)
    skm.set_editor_property("materials",mats); EAL.save_loaded_asset(skm)
    log("material asignado a",len(mats),"slots")
    # socket de lentes
    try:
        s=unreal.SkeletalMeshSocket(); s.set_editor_property("socket_name","GlassesSocket"); s.set_editor_property("bone_name","GlassesSocket")
        log("socket listo")
    except Exception as ex: log("socket",ex)
open(os.path.join(proj,"Saved","tlp_lobo1.txt"),"w").write("\n".join(LOG))
