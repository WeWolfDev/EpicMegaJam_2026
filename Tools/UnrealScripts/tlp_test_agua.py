# Prueba en PIE: paso 1 lanza al raton sobre agua abierta; paso 2 (STEP=2) reporta donde quedo
import unreal, os
w = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_game_world()
out = os.path.join(unreal.Paths.project_saved_dir(), "tlp_test_agua.txt")
pc = unreal.GameplayStatics.get_player_character(w, 0)
step = globals().get("STEP", 1)
if step == 1:
    found = None
    for x in range(-1500, 12000, 300):
        for y in range(-1500, 7000, 300):
            hit = unreal.SystemLibrary.line_trace_single(w, unreal.Vector(x, y, 3000), unreal.Vector(x, y, -500),
                    unreal.TraceTypeQuery.TRACE_TYPE_QUERY1, False, [pc], unreal.DrawDebugTrace.NONE, True)
            if hit:
                t = hit.to_tuple()
                if t[0] and t[4].z < -50 and t[4].z > -100:
                    found = unreal.Vector(x, y, 250)
                    break
        if found:
            break
    pc.set_actor_location(found, False, True)
    open(out, "w").write(f"lanzado a {found}\n")
else:
    open(out, "a").write(f"ahora en {pc.get_actor_location()}\n")
