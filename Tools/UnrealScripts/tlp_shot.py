# Coloca la camara del viewport y toma capturas del nivel en Saved/Screenshots
import unreal
ues = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
M = 100.0
views = {
    "general": ((50, -30, 35), (53, 24, 0)),
    "muelle": ((5, -4, 4), (5, 20, 1.5)),
    "ascensor": ((18, 26, 4), (34, 38, 3)),
    "corredor": ((58, 41, 3), (80, 42, 2)),
    "escenario": ((40, 10, 3.5), (22, 10, 1.5)),
}
_q = list(views.items())

def _shot(i):
    name, (p, t) = _q[i]
    loc = unreal.Vector(p[0] * M, p[1] * M, p[2] * M)
    rot = unreal.MathLibrary.find_look_at_rotation(loc, unreal.Vector(t[0] * M, t[1] * M, t[2] * M))
    ues.set_level_viewport_camera_info(loc, rot)
    unreal.SystemLibrary.execute_console_command(None, "HighResShot 1280x720 filename=TLP_%s" % name)

_state = {"i": 0, "t": 0.0}
def _tick(dt):
    _state["t"] += dt
    if _state["t"] < 1.5:
        return
    _state["t"] = 0.0
    if _state["i"] < len(_q):
        _shot(_state["i"])
        _state["i"] += 1
    else:
        unreal.unregister_slate_post_tick_callback(_h)
        unreal.log("TLP capturas listas")

_h = unreal.register_slate_post_tick_callback(_tick)
