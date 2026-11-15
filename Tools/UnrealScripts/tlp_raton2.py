# Paso 2: importar el raton, crear IK Rigs + Retargeter y retargetear el AnimBP de la plantilla.
# Escribe Saved/TLP_raton2.txt
import os, traceback, unreal
PROJ = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
OUT = os.path.join(PROJ, "Saved", "TLP_raton2.txt")
SRC = os.path.join(PROJ, "Imports", "Raton")
DST = "/Game/TheLastPatch/Personajes/Raton"
L = []
def w(*a):
    L.append(" ".join(str(x) for x in a))
    open(OUT, "w", encoding="utf-8").write("\n".join(L))

tools = unreal.AssetToolsHelpers.get_asset_tools()
eal = unreal.EditorAssetLibrary
ar = unreal.AssetRegistryHelpers.get_asset_registry()

def find(path, cls_name):
    out = []
    for d in ar.get_assets_by_path(path, recursive=True):
        if str(d.asset_class_path.asset_name) == cls_name:
            out.append(unreal.load_asset(str(d.package_name)))
    return out

def step(name, fn):
    try:
        r = fn()
        w("OK", name, r if r is not None else "")
        return r
    except Exception:
        w("ERROR", name, traceback.format_exc())
        return None

# 1. importar el personaje (y su textura)
def do_import():
    if not find(DST, "SkeletalMesh"):
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", os.path.join(SRC, "Meshy_AI_rigged_retro_mouse_20261114_character_ue5_mannequin.fbx"))
        t.set_editor_property("destination_path", DST)
        t.set_editor_property("automated", True)
        t.set_editor_property("replace_existing", True)
        t.set_editor_property("save", True)
        tools.import_asset_tasks([t])
        w("importados:", list(t.get_editor_property("imported_object_paths")))
    t2 = unreal.AssetImportTask()
    t2.set_editor_property("filename", os.path.join(SRC, "Meshy_AI_rigged_retro_mouse_20261114_animated_ue5_mannequin_Wave_One_Hand.png"))
    t2.set_editor_property("destination_path", DST)
    t2.set_editor_property("destination_name", "T_Raton_BaseColor")
    t2.set_editor_property("automated", True)
    t2.set_editor_property("replace_existing", True)
    t2.set_editor_property("save", True)
    tools.import_asset_tasks([t2])
    for d in ar.get_assets_by_path(DST, recursive=True):
        w("  asset:", d.package_name, d.asset_class_path.asset_name)
step("importar", do_import)

meshes = find(DST, "SkeletalMesh")
mouse = meshes[0] if meshes else None
w("malla raton:", mouse.get_path_name() if mouse else None)
manny = unreal.load_asset("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple")
abp = unreal.load_asset("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed")
w("manny:", manny is not None, "abp_unarmed:", abp is not None)

def bounds():
    b = mouse.get_bounds()
    w("bounds raton (cm): extent", b.box_extent, "origin", b.origin)
    b2 = manny.get_bounds()
    w("bounds manny (cm): extent", b2.box_extent)
if mouse: step("medidas", bounds)

# 2. IK Rigs con definicion automatica
def make_rig(name, mesh):
    path = DST + "/" + name
    rig = unreal.load_asset(path) if eal.does_asset_exist(path) else \
        tools.create_asset(name, DST, unreal.IKRigDefinition, unreal.IKRigDefinitionFactory())
    c = unreal.IKRigController.get_controller(rig)
    c.set_skeletal_mesh(mesh)
    ok = c.apply_auto_generated_retarget_definition()
    w("  auto retarget def", name, ok, "chains:", [ch.get_editor_property("chain_name") for ch in c.get_retarget_chains()])
    eal.save_loaded_asset(rig)
    return rig
rig_m = step("IK_Manny", lambda: make_rig("IK_Manny_TLP", manny))
rig_r = step("IK_Raton", lambda: make_rig("IK_Raton", mouse)) if mouse else None

# 3. Retargeter
def make_rtg():
    path = DST + "/RTG_Manny_a_Raton"
    rtg = unreal.load_asset(path) if eal.does_asset_exist(path) else \
        tools.create_asset("RTG_Manny_a_Raton", DST, unreal.IKRetargeter, unreal.IKRetargetFactory())
    c = unreal.IKRetargeterController.get_controller(rtg)
    c.set_ik_rig(unreal.RetargetSourceOrTarget.SOURCE, rig_m)
    c.set_ik_rig(unreal.RetargetSourceOrTarget.TARGET, rig_r)
    try:
        c.auto_map_chains(unreal.AutoMapChainType.FUZZY, True)
    except Exception as e:
        w("  auto_map_chains aviso", e)
    for side in (unreal.RetargetSourceOrTarget.SOURCE, unreal.RetargetSourceOrTarget.TARGET):
        try:
            c.auto_align_all_bones(side)
        except Exception as e:
            w("  auto_align aviso", e)
    eal.save_loaded_asset(rtg)
    return rtg
rtg = step("RTG", make_rtg) if (rig_m and rig_r) else None

# 4. Duplicar y retargetear el AnimBP de la plantilla (con sus animaciones)
def retarget():
    res = unreal.IKRetargetBatchOperation.duplicate_and_retarget(
        [eal.find_asset_data(abp.get_path_name())], manny, mouse, rtg, "", "", "", "_Raton", True)
    names = [str(getattr(a, "package_name", a)) for a in res]
    for n in names:
        w("  nuevo:", n)
    return len(names)
if rtg:
    step("retarget ABP", retarget)

w("FIN")
