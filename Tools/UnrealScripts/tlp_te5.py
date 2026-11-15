# Pasada automatica en PIE: golpe de enemigo, todos los saltos de los 5 tramos, plataforma movil
import unreal, os, json
JUMPS = json.loads(r'''[{"st": "S1", "name": "zona->p", "sx": 1585, "y": 3400, "sz": 76, "vx": 391.43125, "T": 0.9937888198757764, "lo": 1904.0, "hi": 2184.0, "tz": 0}, {"st": "S1", "name": "p->up", "sx": 2169.0, "y": 3400, "sz": 76, "vx": 379.65996397921583, "T": 0.8644577546711426, "lo": 2427.2, "hi": 2667.2, "tz": 63}, {"st": "S1", "name": "up->isla", "sx": 2652.2, "y": 3400, "sz": 139, "vx": 354.9870834043843, "T": 1.0958145188535489, "lo": 2971.2, "hi": 3971.2, "tz": 0}, {"st": "S1", "name": "isla->check", "sx": 3956.2, "y": 3400, "sz": 76, "vx": 391.43125, "T": 0.9937888198757764, "lo": 4275.2, "hi": 4695.2, "tz": 0}, {"st": "S1", "skip": 1, "name": "check->mx"}, {"st": "S1", "skip": 1, "name": "mx->s"}, {"st": "S1", "name": "s->p", "sx": 6327.8, "y": 3400, "sz": 76, "vx": 235.05999999999946, "T": 0.9937888198757764, "lo": 6491.4, "hi": 6651.4, "tz": 0}, {"st": "S1", "name": "p->zona", "sx": 6636.4, "y": 3400, "sz": 76, "vx": 235.06000000000037, "T": 0.9937888198757764, "lo": 6800.0, "hi": 7200.0, "tz": 0}, {"st": "S2", "name": "zona->p", "sx": 9785.0, "y": 4150, "sz": 576, "vx": 391.43125, "T": 0.9937888198757764, "lo": 10104.0, "hi": 10384.0, "tz": 500}, {"st": "S2", "skip": 1, "name": "p->my"}, {"st": "S2", "skip": 1, "name": "my->isla"}, {"st": "S2", "name": "isla->fr", "sx": 12277.0, "y": 4150, "sz": 576, "vx": 391.43125, "T": 0.9937888198757764, "lo": 12596.0, "hi": 13166.0, "tz": 500}, {"st": "S2", "name": "fr->check", "sx": 13151.0, "y": 4150, "sz": 576, "vx": 391.43125, "T": 0.9937888198757764, "lo": 13470.0, "hi": 13890.0, "tz": 500}, {"st": "S2", "name": "check->L", "sx": 13875.0, "y": 4150, "sz": 576, "vx": 436.7125, "T": 0.9937888198757764, "lo": 14239.0, "hi": 14559.0, "tz": 500}, {"st": "S2", "name": "L->up", "sx": 14544.0, "y": 4150, "sz": 576, "vx": 379.6599639792169, "T": 0.8644577546711426, "lo": 14802.2, "hi": 15042.2, "tz": 563}, {"st": "S2", "name": "up->p", "sx": 15027.2, "y": 4150, "sz": 639, "vx": 164.6264006327784, "T": 1.0958145188535489, "lo": 15137.6, "hi": 15297.6, "tz": 500}, {"st": "S2", "name": "p->zona", "sx": 15282.6, "y": 4150, "sz": 576, "vx": 185.9783566150625, "T": 0.9700053451563241, "lo": 15393.0, "hi": 15793.0, "tz": 513}, {"st": "S3", "name": "zona->s", "sx": 19385.0, "y": 4200, "sz": 76, "vx": 360.8412499999985, "T": 0.9937888198757764, "lo": 19673.6, "hi": 19843.6, "tz": 0}, {"st": "S3", "name": "s->L", "sx": 19828.6, "y": 4200, "sz": 76, "vx": 436.7125, "T": 0.9937888198757764, "lo": 20192.6, "hi": 20512.6, "tz": 0}, {"st": "S3", "name": "L->pel", "sx": 20497.6, "y": 4200, "sz": 76, "vx": 391.43125, "T": 0.9937888198757764, "lo": 20816.6, "hi": 21376.6, "tz": 0}, {"st": "S3", "name": "pel->isla", "sx": 21361.6, "y": 4200, "sz": 76, "vx": 391.43125, "T": 0.9937888198757764, "lo": 21680.6, "hi": 22680.6, "tz": 0}, {"st": "S3", "name": "isla->check", "sx": 22665.6, "y": 4200, "sz": 76, "vx": 391.43125, "T": 0.9937888198757764, "lo": 22984.6, "hi": 23404.6, "tz": 0}, {"st": "S3", "name": "check->up", "sx": 23389.6, "y": 4200, "sz": 76, "vx": 379.6599639792169, "T": 0.8644577546711426, "lo": 23647.8, "hi": 23887.8, "tz": 63}, {"st": "S3", "name": "up->s", "sx": 23872.8, "y": 4200, "sz": 139, "vx": 327.2451622334491, "T": 1.0958145188535489, "lo": 24161.399999999998, "hi": 24331.399999999998, "tz": 0}, {"st": "S3", "name": "s->zona", "sx": 24316.399999999998, "y": 4200, "sz": 76, "vx": 355.8100000000022, "T": 0.9937888198757764, "lo": 24600.0, "hi": 25000.0, "tz": 0}, {"st": "S4", "name": "zona->p", "sx": 24615.0, "y": 1000, "sz": 76, "vx": -226.909375, "T": 0.9937888198757764, "lo": 24299.5, "hi": 24459.5, "tz": 0}, {"st": "S4", "skip": 1, "name": "p->my"}, {"st": "S4", "skip": 1, "name": "my->L"}, {"st": "S4", "name": "L->check", "sx": 23250.0, "y": 1000, "sz": 76, "vx": -436.7125, "T": 0.9937888198757764, "lo": 22466.0, "hi": 22886.0, "tz": 0}, {"st": "S4", "name": "check->isla", "sx": 22481.0, "y": 1000, "sz": 76, "vx": -391.43125, "T": 0.9937888198757764, "lo": 21162.0, "hi": 22162.0, "tz": 0}, {"st": "S4", "name": "isla->fr", "sx": 21177.0, "y": 1000, "sz": 76, "vx": -391.43125, "T": 0.9937888198757764, "lo": 20288.0, "hi": 20858.0, "tz": 0}, {"st": "S4", "name": "fr->p", "sx": 20303.0, "y": 1000, "sz": 76, "vx": -391.43125, "T": 0.9937888198757764, "lo": 19704.0, "hi": 19984.0, "tz": 0}, {"st": "S4", "name": "p->zona", "sx": 19719.0, "y": 1000, "sz": 76, "vx": -391.43125, "T": 0.9937888198757764, "lo": 19000.0, "hi": 19400.0, "tz": 0}, {"st": "S5", "name": "zona->p", "sx": 15015.0, "y": 1000, "sz": 76, "vx": -255.68812499999854, "T": 0.9937888198757764, "lo": 14670.900000000001, "hi": 14830.900000000001, "tz": 0}, {"st": "S5", "name": "p->up", "sx": 14685.900000000001, "y": 1000, "sz": 76, "vx": -293.94148947933866, "T": 0.8644577546711426, "lo": 14261.800000000001, "hi": 14501.800000000001, "tz": 63}, {"st": "S5", "name": "up->s", "sx": 14276.800000000001, "y": 1000, "sz": 139, "vx": -299.5032410625172, "T": 1.0958145188535489, "lo": 13848.6, "hi": 14018.6, "tz": 0}, {"st": "S5", "name": "s->fr", "sx": 13863.6, "y": 1000, "sz": 76, "vx": -360.84125000000034, "T": 0.9937888198757764, "lo": 13005.0, "hi": 13575.0, "tz": 0}, {"st": "S5", "name": "fr->check", "sx": 13020.0, "y": 1000, "sz": 76, "vx": -391.43125, "T": 0.9937888198757764, "lo": 12281.0, "hi": 12701.0, "tz": 0}, {"st": "S5", "name": "check->isla", "sx": 12296.0, "y": 1000, "sz": 76, "vx": -391.43125, "T": 0.9937888198757764, "lo": 10977.0, "hi": 11977.0, "tz": 0}, {"st": "S5", "skip": 1, "name": "isla->my"}, {"st": "S5", "skip": 1, "name": "my->L"}, {"st": "S5", "name": "L->zona", "sx": 9764.0, "y": 1000, "sz": 76, "vx": -436.7125, "T": 0.9937888198757764, "lo": 9000.0, "hi": 9400.0, "tz": 0}]''')
out = os.path.join(unreal.Paths.project_saved_dir(), "tlp_te3.txt")
ST = {"t": 0.0, "i": -1, "phase": "golpe0", "t0": 0.0, "res": [], "h": None}
def W(*a): open(out, "a", encoding="utf-8").write(" ".join(str(x) for x in a) + "\n")
def world(): return unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
def tick(dt):
    try:
        w = world()
        if w is None: return
        S = ST; S["t"] = unreal.GameplayStatics.get_time_seconds(w)
        pc = unreal.GameplayStatics.get_player_character(w, 0)
        if pc is None: return
        acts = unreal.GameplayStatics.get_all_actors_of_class(w, unreal.Actor)
        byc = lambda n: [a for a in acts if a.get_class().get_name() == n]
        resp = byc("BP_TLP_Respawn_C")[0]
        vid = lambda: resp.get_editor_property("Vidas")
        if S["phase"] == "golpe0":
            ens = byc("BP_TLP_Enemigo_C"); e1 = min(ens, key=lambda a: (a.get_actor_location().x - 500) ** 2 + (a.get_actor_location().y - 2750) ** 2)
            v = e1.get_actor_location(); S["v0"] = vid(); pc.set_actor_location(unreal.Vector(v.x, v.y - 150, 76), False, True)
            S["phase"] = "golpe1"; S["t0"] = S["t"]
        elif S["phase"] == "golpe1" and S["t"] - S["t0"] > 4.0:
            p = pc.get_actor_location(); W("GOLPE LATERAL: vidas %s -> %s, raton vuelve a (%.0f,%.0f)" % (S["v0"], vid(), p.x, p.y))
            for a in byc("BP_TLP_Enemigo_C") + byc("BP_TLP_Peligro_C") + [x for x in acts if x.get_actor_label().startswith("TLP_Puerta_Escenario_Este")]: a.set_actor_enable_collision(False)
            pc.get_component_by_class(unreal.CharacterMovementComponent).set_editor_property("braking_deceleration_falling", 0.0)
            S["phase"] = "next"
        elif S["phase"] == "next":
            S["i"] += 1
            if S["i"] >= len(JUMPS): S["phase"] = "movil0"; return
            j = JUMPS[S["i"]]
            if j.get("skip"): S["res"].append((j["st"], j["name"], "MOVIL")); return
            pc.set_actor_location(unreal.Vector(j["sx"], j["y"], j["sz"]), False, True)
            S["phase"] = "launch"; S["t0"] = S["t"]
        elif S["phase"] == "launch" and S["t"] - S["t0"] > 0.25:
            j = JUMPS[S["i"]]; pc.launch_character(unreal.Vector(j["vx"], 0, 560), True, True); S["phase"] = "air"; S["t0"] = S["t"]
        elif S["phase"] == "air" and S["t"] - S["t0"] > JUMPS[S["i"]]["T"] + 0.2:
            j = JUMPS[S["i"]]; p = pc.get_actor_location()
            ok = (j["lo"] - 30 <= p.x <= j["hi"] + 30) and p.z > j["tz"] + 40
            S["res"].append((j["st"], j["name"], "OK" if ok else "FALLA x=%.0f z=%.0f (plat %.0f..%.0f z%.0f) vx=%.0f" % (p.x, p.z, j["lo"], j["hi"], j["tz"], j["vx"])))
            S["phase"] = "next"
        elif S["phase"] == "movil0":
            m = [a for a in acts if a.get_actor_label() == "TLP_Plat_S1_movil_1"][0]; v = m.get_actor_location()
            pc.set_actor_location(unreal.Vector(v.x, v.y, v.z + 105), False, True); S["m"] = m; S["mx0"] = v.x; S["phase"] = "movil1"; S["t0"] = S["t"]
        elif S["phase"] == "movil1" and S["t"] - S["t0"] > 2.5:
            v = S["m"].get_actor_location(); p = pc.get_actor_location()
            W("PLATAFORMA MOVIL: se movio %.0f cm; raton encima: dx=%.0f z=%.0f (%s)" % (v.x - S["mx0"], p.x - v.x, p.z, "LO LLEVA" if abs(p.x - v.x) < 120 and p.z > v.z + 40 else "NO LO LLEVA"))
            cur = None
            for st, n, r in S["res"]:
                if st != cur: cur = st; W("--", st)
                W("  ", n, r)
            W("RESUMEN: %d saltos OK, %d fallan, %d con plataforma movil (no probados)" % (sum(r == "OK" for _, _, r in S["res"]), sum(r.startswith("FALLA") for _, _, r in S["res"]), sum(r == "MOVIL" for _, _, r in S["res"])))
            W("vidas al final", vid()); S["phase"] = "fin"
            unreal.unregister_slate_post_tick_callback(S["h"])
    except Exception as ex:
        W("ERROR", ex); unreal.unregister_slate_post_tick_callback(ST["h"])
open(out, "w").write("")
ST["h"] = unreal.register_slate_post_tick_callback(tick)
