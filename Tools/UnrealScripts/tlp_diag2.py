# Diagnostico de sombras/planos grandes y del raton. Escribe Saved/TLP_diag2.txt
import os, traceback, unreal
PROJ = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
OUT = os.path.join(PROJ, "Saved", "TLP_diag2.txt")
L = []
def w(*a):
    L.append(" ".join(str(x) for x in a))
    open(OUT, "w", encoding="utf-8").write("\n".join(L))
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
try:
    for a in actors.get_all_level_actors():
        o, e = a.get_actor_bounds(False)
        if max(e.x, e.y) > 1500 and not isinstance(a, (unreal.Light, unreal.TriggerBox)):
            mats = []
            for c in a.get_components_by_class(unreal.PrimitiveComponent):
                try:
                    mats += [m.get_name() for m in c.get_materials() if m]
                except Exception:
                    pass
                cs = c.get_editor_property("cast_shadow")
            w("GRANDE", a.get_actor_label(), a.get_class().get_name(), "origen", o, "extent", e, "mats", mats[:3])
    r = [a for a in actors.get_all_level_actors() if a.get_actor_label() == "TLP_Raton_Jugador"]
    if r:
        ch = r[0]
        m = ch.mesh
        w("RATON loc", ch.get_actor_location(), "mesh rel", m.get_relative_location())
        w("RATON capsula", ch.capsule_component.get_unscaled_capsule_half_height(), ch.capsule_component.get_unscaled_capsule_radius())
        mesh = m.get_skeletal_mesh_asset()
        b = mesh.get_bounds()
        w("RATON bounds origin", b.origin, "extent", b.box_extent)
        w("RATON materiales", [ (s.get_editor_property("material_slot_name"), s.get_editor_property("material_interface")) for s in mesh.get_editor_property("materials")])
        mi = mesh.get_editor_property("materials")[0].get_editor_property("material_interface")
        if mi:
            par = mi.get_base_material()
            w("RATON material base", par.get_name(), "blend", par.get_editor_property("blend_mode"), "two_sided", par.get_editor_property("two_sided"))
except Exception:
    w("ERROR", traceback.format_exc())
w("FIN")
