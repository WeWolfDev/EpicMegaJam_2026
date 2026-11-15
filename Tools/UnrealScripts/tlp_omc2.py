# Integra One More Cast (cana + fusion + raton con animaciones corregidas) en L_Puerto
import unreal, os
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] " + s)

ar = unreal.AssetRegistryHelpers.get_asset_registry()
ar.scan_paths_synchronous(["/Game/OneMoreCast"], True)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

def ld(p):
    a = unreal.load_asset(p)
    log("cargar", p, "OK" if a else "FALLO")
    return a

sk = ld("/Game/OneMoreCast/Player/RetroMouse/SK_RetroMouse_Game")
abp = ld("/Game/OneMoreCast/Player/RetroMouse/CorrectedAnimations/Fixed_ABP_Unarmed")
rig = ld("/Game/OneMoreCast/Fusion/BP_FusionTestRig")
fobj = ld("/Game/OneMoreCast/Fusion/BP_FusionObject")
ld("/Game/OneMoreCast/Fusion/FishingRod/BP_FishingRod")
ld("/Game/OneMoreCast/Fusion/UI/WBP_FishingAim")

actors = eas.get_all_level_actors()
by_label = {a.get_actor_label(): a for a in actors}

# ---- 1. Raton jugador: malla + animaciones corregidas
ply = by_label.get("TLP_Raton_Jugador")
if ply and sk and abp:
    mesh = ply.get_component_by_class(unreal.SkeletalMeshComponent)
    cap = ply.get_component_by_class(unreal.CapsuleComponent)
    log("antes: malla", mesh.get_editor_property("skeletal_mesh_asset") if hasattr(mesh, "skeletal_mesh_asset") else mesh.skeletal_mesh,
        "rel", mesh.get_editor_property("relative_location"), "capsula", cap.get_scaled_capsule_half_height(), cap.get_scaled_capsule_radius())
    mesh.set_skeletal_mesh_asset(sk) if hasattr(mesh, "set_skeletal_mesh_asset") else mesh.set_skeletal_mesh(sk)
    mesh.set_editor_property("animation_mode", unreal.AnimationMode.ANIMATION_BLUEPRINT)
    mesh.set_editor_property("anim_class", abp.generated_class())
    b = sk.get_bounds()
    min_z = b.origin.z - b.box_extent.z
    h = b.box_extent.z * 2
    half = cap.get_unscaled_capsule_half_height()
    z = -half - min_z
    loc = mesh.get_editor_property("relative_location")
    mesh.set_editor_property("relative_location", unreal.Vector(loc.x, loc.y, z))
    log("malla nueva: alto", round(h), "cm, min_z", round(min_z, 1), "-> mesh z", round(z, 1),
        "rot", mesh.get_editor_property("relative_rotation"))
    # sockets / huesos de mano
    names = [str(n) for n in mesh.get_all_socket_names()]
    log("hand_r existe:", "hand_r" in names, "| huesos con 'hand':", [n for n in names if "hand" in n.lower()][:8])
else:
    log("NO pude cambiar el raton", ply, sk, abp)

# ---- 2. Controlador de la mecanica
for a in actors:
    if rig and a.get_class() == rig.generated_class():
        eas.destroy_actor(a)
ps = next((a for a in actors if isinstance(a, unreal.PlayerStart)), None)
r = eas.spawn_actor_from_class(rig.generated_class(), ps.get_actor_location() if ps else unreal.Vector(0, 0, 100), unreal.Rotator(0, 0, 0))
r.set_actor_label("OMC_FusionRig"); r.set_folder_path("TLP/Logica")
log("Rig colocado")

# ---- 3. Fuentes y receptores en los puntos con tag del blockout
for a in eas.get_all_level_actors():
    if fobj and a.get_class() == fobj.generated_class():
        eas.destroy_actor(a)
spots = []
for a in eas.get_all_level_actors():
    tags = [str(t) for t in a.tags]
    for t in tags:
        if t.startswith(("Source_", "Receiver_")):
            spots.append((a, t, tags))
for a, t, tags in spots:
    kind, sk_name = t.split("_", 1)          # Source/Receiver, Bounce/Pull
    o, e = a.get_actor_bounds(False)
    loc = unreal.Vector(o.x, o.y, o.z + e.z)  # encima de la pieza
    n = eas.spawn_actor_from_class(fobj.generated_class(), loc, a.get_actor_rotation())
    lab = "OMC_" + kind + "_" + sk_name + "_" + a.get_actor_label().replace("BO_", "")
    n.set_actor_label(lab); n.set_folder_path("TLP/Fusion")
    n.tags = [unreal.Name(x) for x in tags]
    res = []
    for prop, val in (("IsSource", kind == "Source"), ("SketchType", sk_name)):
        try:
            cur = n.get_editor_property(prop)
            if isinstance(cur, unreal.Name) or isinstance(val, str) and not isinstance(cur, str):
                val = unreal.Name(val)
            n.set_editor_property(prop, val)
            res.append(f"{prop}={n.get_editor_property(prop)}")
        except Exception as ex:
            res.append(f"{prop}: ERROR {ex}")
    pass
    log(lab, loc, res)

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
log("Nivel guardado")
open(os.path.join(unreal.Paths.project_saved_dir(), "tlp_omc.txt"), "w", encoding="utf-8").write("\n".join(LOG))
