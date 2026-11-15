import unreal, os
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
L={a.get_actor_label():a for a in eas.get_all_level_actors()}
L["TLP_Charla_Ascensor"].set_editor_property("Meta",L["BO_Goal_P1"])
L["TLP_Charla_Escenario"].set_editor_property("Meta",L["BO_Finale_Reveal"])
cam=L["BO_Cam_Final"]; cam.set_actor_location(unreal.Vector(500,950,240),False,False)
cam.set_actor_rotation(unreal.MathLibrary.find_look_at_rotation(cam.get_actor_location(),unreal.Vector(500,235,110)),False)
unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_fin3.txt"),"w").write("ok "+str(cam.get_actor_location()))
