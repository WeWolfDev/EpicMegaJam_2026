import unreal, os
out = os.path.join(unreal.Paths.project_saved_dir(), "tlp_te4.txt")
CASES = [("S4 isla->fr", 21177, 1000, 76, -391), ("S2 isla->fr", 12277, 4150, 576, 391)]
ST = {"t": 0.0, "c": -1, "phase": "next", "t0": 0.0, "h": None, "last": 0.0}
def W(*a): open(out, "a", encoding="utf-8").write(" ".join(str(x) for x in a) + "\n")
def tick(dt):
    try:
        w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
        if w is None: return
        S = ST; S["t"] += dt
        pc = unreal.GameplayStatics.get_player_character(w, 0)
        if S["phase"] == "next":
            S["c"] += 1
            if S["c"] >= len(CASES):
                unreal.unregister_slate_post_tick_callback(S["h"]); W("FIN"); return
            n, x, y, z, vx = CASES[S["c"]]; W("==", n)
            for a in unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor):
                cn = a.get_class().get_name()
                if cn in ("BP_TLP_Enemigo_C", "BP_TLP_Peligro_C"): a.set_actor_enable_collision(False)
                if cn == "BP_TLP_TablaFragil_C":
                    v = a.get_actor_location()
                    if abs(v.x - (x + vx)) < 500 and abs(v.y - y) < 100:
                        c = a.static_mesh_component
                        W("  tabla", a.get_actor_label(), "(%.0f,%.0f,%.0f)" % (v.x, v.y, v.z), "esc", a.get_actor_scale3d().x, a.get_actor_scale3d().z, "oculta", a.get_editor_property("hidden"), "col", a.get_actor_enable_collision(), c.get_collision_profile_name(), c.get_collision_enabled(), "cay", a.get_editor_property("Cayendo"))
            pc.get_component_by_class(unreal.CharacterMovementComponent).set_editor_property("braking_deceleration_falling", 0.0)
            pc.set_actor_location(unreal.Vector(x, y, z), False, True); S["phase"] = "launch"; S["t0"] = S["t"]
        elif S["phase"] == "launch" and S["t"] - S["t0"] > 0.25:
            pc.launch_character(unreal.Vector(CASES[S["c"]][4], 0, 560), True, True); S["phase"] = "air"; S["t0"] = S["t"]; S["last"] = -1
        elif S["phase"] == "air":
            e = S["t"] - S["t0"]
            if e - S["last"] >= 0.1:
                S["last"] = e; p = pc.get_actor_location(); W("  t=%.2f dt=%.3f (%.0f,%.0f,%.0f)" % (e, dt, p.x, p.y, p.z))
            if e > 2.2: S["phase"] = "next"
    except Exception as ex:
        W("ERROR", ex); unreal.unregister_slate_post_tick_callback(ST["h"])
open(out, "w").write("")
ST["h"] = unreal.register_slate_post_tick_callback(tick)
