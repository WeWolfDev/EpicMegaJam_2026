import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
A={a.get_actor_label():a for a in unreal.GameplayStatics.get_all_actors_of_class(w,unreal.Actor)}
pc=unreal.GameplayStatics.get_player_character(w,0); J=A['TLP_Jefe_Controlador']; lo=A['TLP_Jefe_Lobo']
cm=unreal.GameplayStatics.get_player_camera_manager(w,0)
s=f"pc={pc.get_actor_location()} est={J.get_editor_property('Estado')} lobo={lo.get_actor_location()} rot={lo.get_actor_rotation()} hid={lo.get_editor_property('hidden')} rev={A['BO_Finale_Reveal'].get_editor_property('Resuelto')} cam={cm.get_camera_location()} camrot={cm.get_camera_rotation()}"
open(r'C:/Proyectos/EpicMegaJam_2026/Saved/chk2.txt','w').write(s)
