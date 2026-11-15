# PIE: pone al raton frente a la fuente Rebote (trampolin OG) mirando hacia ella
import unreal
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
pc = unreal.GameplayStatics.get_player_character(w, 0)
ctl = unreal.GameplayStatics.get_player_controller(w, 0)
pc.set_actor_location(unreal.Vector(2200, 2050, 150), False, True)
ctl.set_control_rotation(unreal.Rotator(pitch=-15, yaw=90, roll=0))
pc.set_actor_rotation(unreal.Rotator(roll=0, pitch=0, yaw=90), True)
