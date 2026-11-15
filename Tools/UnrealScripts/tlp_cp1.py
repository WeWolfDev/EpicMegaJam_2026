# Crea los Blueprints de checkpoint, agua y punto de reaparicion. Escribe Saved/TLP_cp1.txt
import os, traceback, unreal
PROJ = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
OUT = os.path.join(PROJ, "Saved", "TLP_cp1.txt")
P = "/Game/TheLastPatch/Blueprints"
L = []
def w(*a):
    L.append(" ".join(str(x) for x in a)); open(OUT, "w", encoding="utf-8").write("\n".join(L))
tools = unreal.AssetToolsHelpers.get_asset_tools()
eal = unreal.EditorAssetLibrary
def make(name, parent):
    path = P + "/" + name
    if eal.does_asset_exist(path):
        return unreal.load_asset(path)
    f = unreal.BlueprintFactory(); f.set_editor_property("parent_class", parent)
    bp = tools.create_asset(name, P, unreal.Blueprint, f)
    unreal.BlueprintEditorLibrary.compile_blueprint(bp)
    eal.save_loaded_asset(bp)
    return bp
try:
    for n, par in [("BP_TLP_Respawn", unreal.TargetPoint), ("BP_TLP_Checkpoint", unreal.TriggerBox), ("BP_TLP_Agua", unreal.TriggerBox)]:
        w("ok", make(n, par).get_path_name())
    unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([unreal.load_asset(P + "/BP_TLP_Checkpoint")])
    w("editor abierto")
except Exception:
    w("ERROR", traceback.format_exc())
