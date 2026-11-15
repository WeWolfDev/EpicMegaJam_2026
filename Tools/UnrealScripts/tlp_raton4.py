# Paso 4: el jugador es el raton. Coloca un BP_ThirdPersonCharacter con la malla y animaciones del raton
# en el PlayerStart y lo posee el jugador 0. Escribe Saved/TLP_raton4.txt
import os, traceback, unreal
PROJ = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
OUT = os.path.join(PROJ, "Saved", "TLP_raton4.txt")
DST = "/Game/TheLastPatch/Personajes/Raton"
L = []
def w(*a):
    L.append(" ".join(str(x) for x in a))
    open(OUT, "w", encoding="utf-8").write("\n".join(L))

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
try:
    mouse = unreal.load_asset(DST + "/Meshy_AI_rigged_retro_mouse_20261114_character_ue5_mannequin")
    abp = unreal.load_asset(DST + "/Anims/ABP_Unarmed_Raton")
    w("abp:", abp)
    char_bp = unreal.load_asset("/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter")

    # quitar uno anterior si existe
    for a in actors.get_all_level_actors():
        if a.get_actor_label() == "TLP_Raton_Jugador":
            actors.destroy_actor(a)

    ps = [a for a in actors.get_all_level_actors() if isinstance(a, unreal.PlayerStart)][0]
    loc = ps.get_actor_location()
    rot = ps.get_actor_rotation()

    HALF = 72.0   # media altura de la capsula para un raton de ~140 cm
    with unreal.ScopedEditorTransaction("TLP raton jugador"):
        ch = actors.spawn_actor_from_class(char_bp.generated_class(), unreal.Vector(loc.x, loc.y, loc.z + 10), rot)
        ch.set_actor_label("TLP_Raton_Jugador")
        ch.set_folder_path("Personajes")
        ch.set_editor_property("auto_possess_player", unreal.AutoReceiveInput.PLAYER0)
        cap = ch.capsule_component
        cap.set_capsule_size(34.0, HALF)
        mesh = ch.mesh
        mesh.set_skeletal_mesh_asset(mouse)
        mesh.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_BLUEPRINT)
        mesh.set_editor_property("anim_class", abp.generated_class())
        mesh.set_relative_location(unreal.Vector(0, 0, -HALF), False, False)
        mesh.set_relative_rotation(unreal.Rotator(roll=0.0, pitch=0.0, yaw=-90.0), False, False)
    w("colocado en", ch.get_actor_location(), "auto possess PLAYER0")
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    w("nivel guardado")
except Exception:
    w("ERROR", traceback.format_exc())
w("FIN")
