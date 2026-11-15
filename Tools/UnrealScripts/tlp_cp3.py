# Restaura los conos BO_Checkpoint_N_Marca (tlp_cp2 los convirtio en triggers por error)
import unreal
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
cone = unreal.load_asset("/Engine/BasicShapes/Cone.Cone")
mi = unreal.load_asset("/Game/TheLastPatch/Blockout/MI_Personaje")
out = []
for a in eas.get_all_level_actors():
    lab = a.get_actor_label()
    if lab.startswith("BO_Checkpoint_") and lab.endswith("_Marca"):
        loc = a.get_actor_location()
        folder = a.get_folder_path()
        tags = list(a.tags)
        eas.destroy_actor(a)
        n = eas.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(loc.x, loc.y, 50), unreal.Rotator(0, 0, 0))
        c = n.static_mesh_component
        c.set_static_mesh(cone)
        c.set_material(0, mi)
        c.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
        n.set_actor_scale3d(unreal.Vector(0.8, 0.8, 1.0))
        n.set_actor_label(lab)
        n.set_folder_path(folder)
        n.tags = tags
        out.append(lab)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.log("[TLP] conos restaurados: " + ", ".join(out))
import os
open(os.path.join(unreal.Paths.project_saved_dir(), "tlp_cp3.txt"), "w").write("\n".join(out))
