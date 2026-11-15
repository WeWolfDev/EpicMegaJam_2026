# Agrega la variable Vidas (int, 3) a BP_TLP_Respawn y abre BP_TLP_Agua y BP_TLP_HUD
import unreal, os
LOG=[]
bel = unreal.BlueprintEditorLibrary
bp = unreal.load_asset("/Game/TheLastPatch/Blueprints/BP_TLP_Respawn")
try:
    t = bel.get_basic_type_by_name("int")
    ok = bel.add_member_variable(bp, "Vidas", t)
    LOG.append(f"add_member_variable: {ok}")
except Exception as ex:
    LOG.append(f"add var ERROR {ex}")
bel.compile_blueprint(bp)
cdo = unreal.get_default_object(bp.generated_class())
try:
    cdo.set_editor_property("Vidas", 3)
    LOG.append(f"Vidas por defecto = {cdo.get_editor_property('Vidas')}")
except Exception as ex:
    LOG.append(f"default ERROR {ex}")
unreal.EditorAssetLibrary.save_loaded_asset(bp)
unreal.load_asset("/Game/OneMoreCast/Fusion/BP_FusionTestRig")
ae = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
ae.open_editor_for_assets([unreal.load_asset("/Game/TheLastPatch/Blueprints/BP_TLP_Agua")])
open(os.path.join(unreal.Paths.project_saved_dir(), "tlp_vidas.txt"), "w").write("\n".join(LOG))
