# PIE: STEP='tronco' / 'tabla' / 'rep'
import unreal, os
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
L = {a.get_actor_label(): a for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor)}
pc = unreal.GameplayStatics.get_player_character(w, 0)
out = os.path.join(unreal.Paths.project_saved_dir(), "tlp_test_obs.txt")
s = globals().get("STEP", "rep")
if s == "tronco":
    v = L["TLP_Obs_Tronco_Pasarela_0"].get_actor_location()
    pc.set_actor_location(unreal.Vector(v.x, v.y, 80), False, True)
    open(out, "a").write(f"-> al tronco {v.y:.0f}\n")
elif s == "tabla":
    pc.set_actor_location(unreal.Vector(6700, 1000, 90), False, True)
    open(out, "a").write("-> a la tabla 1\n")
else:
    r = next(a for a in L.values() if a.get_class().get_name().startswith("BP_TLP_Respawn"))
    p = pc.get_actor_location()
    t = L["TLP_Obs_Tabla_1"]
    open(out, "a").write(f"vidas={r.get_editor_property('Vidas')} raton=({p.x:.0f},{p.y:.0f},{p.z:.0f}) tabla1_oculta={t.get_editor_property('hidden')}\n")
