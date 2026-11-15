import unreal
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
pc=unreal.GameplayStatics.get_player_character(w,0); pc.set_actor_location(unreal.Vector(9000,1000,120),False,True)
pc.set_actor_rotation(unreal.Rotator(0,0,180),False)
