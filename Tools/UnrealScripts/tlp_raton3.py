# Paso 3: retargetear ABP_Unarmed al raton (con sus animaciones). Escribe Saved/TLP_raton3.txt
import os, traceback, unreal
PROJ = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
OUT = os.path.join(PROJ, "Saved", "TLP_raton3.txt")
DST = "/Game/TheLastPatch/Personajes/Raton"
L = []
def w(*a):
    L.append(" ".join(str(x) for x in a))
    open(OUT, "w", encoding="utf-8").write("\n".join(L))

eal = unreal.EditorAssetLibrary
fn = unreal.IKRetargetBatchOperation.duplicate_and_retarget
w("DOC:", fn.__doc__)
try:
    mouse = unreal.load_asset(DST + "/Meshy_AI_rigged_retro_mouse_20261114_character_ue5_mannequin")
    manny = unreal.load_asset("/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple")
    rtg = unreal.load_asset(DST + "/RTG_Manny_a_Raton")
    abp = eal.find_asset_data("/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed")
    kw = dict(assets_to_retarget=[abp], source_mesh=manny, target_mesh=mouse, ik_retarget_asset=rtg,
              search="", replace="", prefix="", suffix="_Raton", include_referenced_assets=True)
    doc = fn.__doc__ or ""
    if "target_path" in doc:
        kw["target_path"] = DST + "/Anims"
    res = fn(**kw)
    for a in res:
        w("nuevo:", getattr(a, "package_name", a))
except Exception:
    w("ERROR", traceback.format_exc())
w("FIN")
