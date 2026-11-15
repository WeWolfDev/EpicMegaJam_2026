# Arregla el control del personaje y quita sombras costosas. Escribe Saved/TLP_fix.txt
import os, unreal
PROJ = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
OUT = os.path.join(PROJ, "Saved", "TLP_fix.txt")
L = []
def w(*a): L.append(" ".join(str(x) for x in a))
eal = unreal.EditorAssetLibrary
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

try:
    # 1. GameMode: usar el PlayerController de la plantilla (agrega los controles de Enhanced Input)
    gm_bp = unreal.load_asset("/Game/TheLastPatch/Blueprints/BP_TheLastPatchGameMode")
    pc_bp = unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController")
    ch_bp = unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")
    cdo = unreal.get_default_object(gm_bp.generated_class())
    cdo.set_editor_property("player_controller_class", pc_bp.generated_class())
    cdo.set_editor_property("default_pawn_class", ch_bp.generated_class())
    eal.save_loaded_asset(gm_bp, only_if_is_dirty=False)
    w("GameMode player_controller_class ->", cdo.get_editor_property("player_controller_class").get_name())

    # 2. El nivel usa este GameMode
    world = unreal.EditorLevelLibrary.get_editor_world()
    ws = world.get_world_settings()
    ws.set_editor_property("default_game_mode", gm_bp.generated_class())
    w("WorldSettings GameMode ->", ws.get_editor_property("default_game_mode").get_name())

    # 3. Luces decorativas sin sombras (7 luces estacionarias se encimaban en el escenario)
    n = 0
    with unreal.ScopedEditorTransaction("TLP sombras"):
        for a in actors.get_all_level_actors():
            lab = a.get_actor_label()
            if isinstance(a, unreal.Light) and lab.startswith(("BO_Foco_", "BO_Brillo_", "BO_Faro_")):
                a.light_component.set_editor_property("cast_shadows", False)
                n += 1
    w("luces sin sombra:", n)

    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    w("nivel guardado")
except Exception as e:
    import traceback
    w("ERROR", traceback.format_exc())

open(OUT, "w", encoding="utf-8").write("\n".join(L))
unreal.log("TLP fix listo")
