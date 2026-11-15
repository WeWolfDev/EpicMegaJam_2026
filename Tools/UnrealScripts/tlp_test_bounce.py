# PIE: STEP=1 vuelve hibrido el ascensor y deja caer al raton encima; STEP=2 reporta altura
import unreal, os
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
L = {a.get_actor_label(): a for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor)}
pc = unreal.GameplayStatics.get_player_character(w, 0)
out = os.path.join(unreal.Paths.project_saved_dir(), "tlp_test_bounce.txt")
r = L["OMC_Receiver_Bounce_Ascensor_Plataforma"]
if globals().get("STEP", 1) == 1:
    r.set_editor_property("VersionState", unreal.Name("Hybrid"))
    v = r.get_actor_location()
    pc.set_actor_location(unreal.Vector(v.x, v.y, v.z + 150), False, True)
    open(out, "w").write(f"receptor en z={v.z:.0f}\n")
else:
    p = pc.get_actor_location(); vz = pc.get_velocity().z
    open(out, "a").write(f"raton z={p.z:.0f} vz={vz:.0f}\n")
