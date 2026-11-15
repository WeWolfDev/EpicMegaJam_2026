import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
pc=unreal.GameplayStatics.get_player_character(w,0); pc.set_actor_location(unreal.Vector(8250,1500,120),False,True)
pc.get_controller().set_control_rotation(unreal.Rotator(0,-12,-140))
