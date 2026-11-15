# Fija Velocidad y Duracion en cada movedor del nivel
import unreal, os
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
mc = unreal.load_asset("/Game/TheLastPatch/Blueprints/BP_TLP_Mover").generated_class()
out = []
for a in eas.get_all_level_actors():
    if a.get_class() == mc:
        out.append(f"{a.get_actor_label()} antes: vel={a.get_editor_property('Velocidad')} dur={a.get_editor_property('Duracion')}")
        a.set_editor_property("Velocidad", 0.6)
        a.set_editor_property("Duracion", 2.5)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
open(os.path.join(unreal.Paths.project_saved_dir(), "tlp_puz3.txt"), "w").write("\n".join(out))
