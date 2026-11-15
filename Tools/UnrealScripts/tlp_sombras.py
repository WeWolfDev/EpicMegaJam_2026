# Arreglo de sombras y del piso de la plantilla. Escribe Saved/TLP_sombras.txt
import os, traceback, unreal
PROJ = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
OUT = os.path.join(PROJ, "Saved", "TLP_sombras.txt")
L = []
def w(*a):
    L.append(" ".join(str(x) for x in a))
    open(OUT, "w", encoding="utf-8").write("\n".join(L))
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

def setp(obj, prop, val):
    try:
        obj.set_editor_property(prop, val); w("  ", prop, "=", val)
    except Exception as e:
        w("  aviso", prop, e)

try:
    with unreal.ScopedEditorTransaction("TLP sombras 3"):
        for a in actors.get_all_level_actors():
            lab = a.get_actor_label()
            if isinstance(a, unreal.DirectionalLight):
                w("Sol:", lab)
                lc = a.light_component
                setp(lc, "cast_cloud_shadows", False)          # sin manchas de nubes en el suelo
                setp(lc, "cast_shadows", True)
                # sol mas alto y desde el oeste: las sombras caen hacia el este, lejos del muelle
                a.set_actor_rotation(unreal.Rotator(roll=0.0, pitch=-50.0, yaw=300.0), False)
                w("  rotacion pitch -50 yaw 300")
            if isinstance(a, unreal.VolumetricCloud):
                w("Nubes:", lab)
                try:
                    a.volumetric_cloud_component.set_editor_property("shadow_tracing_distance", 0.0)
                except Exception as e:
                    w("  aviso nubes", e)
            if lab == "Floor" and isinstance(a, unreal.StaticMeshActor):
                # piso de la plantilla: invisible y 10 cm bajo el agua (sigue atrapando caidas)
                c = a.static_mesh_component
                c.set_visibility(False)
                c.set_cast_shadow(False)
                loc = a.get_actor_location()
                o, e = a.get_actor_bounds(False)
                top = o.z + e.z
                a.set_actor_location(unreal.Vector(loc.x, loc.y, loc.z + (-70.0 - top)), False, False)
                w("Floor oculto y bajado bajo el agua")
            if lab == "SM_SkySphere":
                c = a.static_mesh_component
                c.set_cast_shadow(False)
                w("SkySphere sin sombra")
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    w("nivel guardado")
except Exception:
    w("ERROR", traceback.format_exc())
w("FIN")
