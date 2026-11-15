# PIE: STEP=1 activa receptores de Traccion y lleva al raton a la meta P1; STEP=2 reporta
import unreal, os
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
acts = unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor)
L = {a.get_actor_label(): a for a in acts}
out = os.path.join(unreal.Paths.project_saved_dir(), "tlp_test_puz.txt")
step = globals().get("STEP", 1)
pc = unreal.GameplayStatics.get_player_character(w, 0)
if step == 1:
    for r in ("OMC_Receiver_Pull_Valla_Publicitaria", "OMC_Receiver_Pull_Grua_Plataforma", "OMC_Receiver_Pull_Panel_Cierre"):
        L[r].set_editor_property("VersionState", unreal.Name("Hybrid"))
    g = L["BO_Goal_P1"]
    pc.set_actor_location(g.get_actor_location(), False, True)
    open(out, "w").write("paso 1 ok\n")
else:
    lines = []
    for n in ("BO_Ascensor_Plataforma", "BO_Valla_Publicitaria", "BO_Grua_Plataforma", "BO_Panel_Cierre"):
        v = L[n].get_actor_location(); lines.append(f"{n}: {v.x:.0f},{v.y:.0f},{v.z:.0f}")
    for n in ("BO_Jaula_Toto", "BO_Taller_Mesa", "BO_Anuncio_Patio_1"):
        a = L.get(n)
        if a: lines.append(f"{n}: oculto={a.get_editor_property("hidden")} colision={a.get_actor_enable_collision()}")
    open(out, "a").write("\n".join(lines) + "\n")
