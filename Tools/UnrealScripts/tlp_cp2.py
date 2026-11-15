# The Last Patch - paso 2: checkpoints/agua en el nivel, saltos, camara y HUD base
import unreal

LOG = []
def log(*a):
    s = " ".join(str(x) for x in a)
    LOG.append(s)
    unreal.log("[TLP] " + s)

eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
BPDIR = "/Game/TheLastPatch/Blueprints"

def cls(name):
    bp = unreal.load_asset(f"{BPDIR}/{name}")
    return bp.generated_class() if bp else None

actors = eas.get_all_level_actors()
by_label = {a.get_actor_label(): a for a in actors}

# ---------- 1. Respawn ----------
c_resp = cls("BP_TLP_Respawn")
for a in actors:
    if a.get_class() == c_resp:
        eas.destroy_actor(a)
ps = next((a for a in actors if isinstance(a, unreal.PlayerStart)), None)
ps_loc = ps.get_actor_location() if ps else unreal.Vector(500, 300, 130)
resp = eas.spawn_actor_from_class(c_resp, ps_loc, unreal.Rotator(0, 0, 0))
resp.set_actor_label("TLP_Respawn")
resp.set_folder_path("TLP/Logica")
log("Respawn en", ps_loc)

def box_extent(a):
    bc = a.get_component_by_class(unreal.BoxComponent)
    return bc.get_editor_property("box_extent") if bc else unreal.Vector(40, 40, 40)

def replace(old, new_cls, label, extent=None, loc=None, scale=None):
    loc = loc or old.get_actor_location()
    rot = old.get_actor_rotation()
    scl = scale or old.get_actor_scale3d()
    ext = extent or box_extent(old)
    tags = list(old.tags)
    folder = old.get_folder_path()
    eas.destroy_actor(old)
    n = eas.spawn_actor_from_class(new_cls, loc, rot)
    n.set_actor_scale3d(scl)
    bc = n.get_component_by_class(unreal.BoxComponent)
    bc.set_editor_property("box_extent", ext)
    n.tags = tags
    n.set_actor_label(label)
    n.set_folder_path(folder if str(folder) != "None" else "TLP/Logica")
    return n

# ---------- 2. Checkpoints ----------
c_cp = cls("BP_TLP_Checkpoint")
for lab in sorted(l for l in by_label if l.startswith("BO_Checkpoint")):
    old = by_label[lab]
    loc = old.get_actor_location()
    ext = box_extent(old)
    sc = old.get_actor_scale3d()
    half_h = ext.z * sc.z
    # el centro del trigger es donde reaparece el raton: lo dejo ~1 m sobre el suelo
    ground = loc.z - half_h
    new_loc = unreal.Vector(loc.x, loc.y, max(loc.z, ground + 100))
    n = replace(old, c_cp, lab, loc=new_loc)
    log("Checkpoint", lab, "suelo~", round(ground), "centro", new_loc, "ext", ext, "scale", sc)

# ---------- 3. Agua ----------
c_ag = cls("BP_TLP_Agua")
agua_vis = by_label.get("BO_Agua")
if agua_vis:
    o, e = agua_vis.get_actor_bounds(False)
    cx, cy, hx, hy = o.x, o.y, e.x, e.y
else:
    cx, cy, hx, hy = 0, 0, 20000, 20000
# Suelo oculto con tope en z=-70: si el raton esta ahi, toca el trigger (-65..-20 cm)
zc, hz = -42.5, 22.5
old = by_label.get("BO_Trigger_Agua")
if old:
    n = replace(old, c_ag, "BO_Trigger_Agua", extent=unreal.Vector(hx, hy, hz),
                loc=unreal.Vector(cx, cy, zc), scale=unreal.Vector(1, 1, 1))
else:
    n = eas.spawn_actor_from_class(c_ag, unreal.Vector(cx, cy, zc), unreal.Rotator(0, 0, 0))
    n.get_component_by_class(unreal.BoxComponent).set_editor_property("box_extent", unreal.Vector(hx, hy, hz))
    n.set_actor_label("BO_Trigger_Agua")
    n.set_folder_path("TLP/Logica")
log("Agua trigger centro", (cx, cy, zc), "extent", (hx, hy, hz))

# ---------- 4. Saltos y camara ----------
ply = by_label.get("TLP_Raton_Jugador")
if ply:
    cm = ply.get_component_by_class(unreal.CharacterMovementComponent)
    # altura de salto = v^2 / (2 * 980 * gravedad) = 560^2 / (2*980*1.15) ~ 1.39 m
    for k, v in {
        "jump_z_velocity": 560.0,
        "gravity_scale": 1.15,
        "air_control": 0.7,
        "air_control_boost_multiplier": 2.0,
        "braking_deceleration_falling": 700.0,
        "falling_lateral_friction": 0.0,
        "max_walk_speed": 450.0,
        "max_acceleration": 2400.0,
        "braking_deceleration_walking": 2400.0,
        "ledge_check_threshold": 8.0,
        "perch_radius_threshold": 4.0,
    }.items():
        try:
            cm.set_editor_property(k, v)
        except Exception as ex:
            log("CM no pude", k, ex)
    ply.set_editor_property("jump_max_hold_time", 0.0)
    ply.set_editor_property("jump_max_count", 1)
    arm = ply.get_component_by_class(unreal.SpringArmComponent)
    if arm:
        arm.set_editor_property("target_arm_length", 330.0)
        arm.set_editor_property("target_offset", unreal.Vector(0, 0, 40))
        arm.set_editor_property("enable_camera_lag", True)
        arm.set_editor_property("camera_lag_speed", 12.0)
    log("Jugador ajustado: salto ~1.39 m, air control 0.7, camara 330 cm")
else:
    log("NO encontre TLP_Raton_Jugador")

# ---------- 5. HUD ----------
at = unreal.AssetToolsHelpers.get_asset_tools()
hud_path = f"{BPDIR}/BP_TLP_HUD"
if not unreal.EditorAssetLibrary.does_asset_exist(hud_path):
    f = unreal.BlueprintFactory()
    f.set_editor_property("parent_class", unreal.HUD)
    at.create_asset("BP_TLP_HUD", BPDIR, unreal.Blueprint, f)
hud_bp = unreal.load_asset(hud_path)
unreal.EditorAssetLibrary.save_asset(hud_path)

gm_bp = None
for p in unreal.EditorAssetLibrary.list_assets("/Game", True, False):
    if p.split(".")[-1] == "BP_ThirdPersonGameMode":
        gm_bp = unreal.load_asset(p)
        break
if gm_bp:
    cdo = unreal.get_default_object(gm_bp.generated_class())
    cdo.set_editor_property("hud_class", hud_bp.generated_class())
    unreal.BlueprintEditorLibrary.compile_blueprint(gm_bp)
    unreal.EditorAssetLibrary.save_loaded_asset(gm_bp)
    log("GameMode HUD =", cdo.get_editor_property("hud_class"))
else:
    log("NO encontre BP_ThirdPersonGameMode")

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([hud_bp])
log("Nivel guardado")

import os
out = os.path.join(unreal.Paths.project_saved_dir(), "tlp_cp2.txt")
open(out, "w", encoding="utf-8").write("\n".join(LOG))
