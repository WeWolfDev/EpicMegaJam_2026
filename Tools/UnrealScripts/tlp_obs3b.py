# Obstaculos paso 3: coloca peligros, tablas fragiles y corta la pasarela
import unreal, os
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] " + s)
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
BPD = "/Game/TheLastPatch/Blueprints"
pel_c = unreal.load_asset(f"{BPD}/BP_TLP_Peligro").generated_class()
tab_c = unreal.load_asset(f"{BPD}/BP_TLP_TablaFragil").generated_class()
CUBE = unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
CYL = unreal.load_asset("/Engine/BasicShapes/Cylinder.Cylinder")
MB = "/Game/TheLastPatch/Blockout/"
M = {n: unreal.load_asset(MB + n) for n in ("MI_Peligro", "MI_Electrico", "MI_Fragil", "MI_Base_Electrica")}
V = unreal.Vector
def R(pitch=0, yaw=0): return unreal.Rotator(roll=0, pitch=pitch, yaw=yaw)

# limpiar lo de una corrida anterior
for a in eas.get_all_level_actors():
    if a.get_class() in (pel_c, tab_c) or a.get_actor_label().startswith("TLP_Obs_"):
        eas.destroy_actor(a)
L = {a.get_actor_label(): a for a in eas.get_all_level_actors()}

def setup_mesh(a, mesh, mat, scale, overlap):
    c = a.static_mesh_component
    c.set_mobility(unreal.ComponentMobility.MOVABLE)
    c.set_static_mesh(mesh); c.set_material(0, mat)
    a.set_actor_scale3d(scale)
    if overlap:
        c.set_collision_profile_name("OverlapAllDynamic")
        c.set_editor_property("generate_overlap_events", True)

def peligro(label, mesh, mat, loc, scale, rot=R(), mueve=False, puntob=V(0, 0, 0), periodo=3.0,
            desfase=0.0, intermitente=False, fraccion=0.5):
    a = eas.spawn_actor_from_class(pel_c, loc, rot)
    setup_mesh(a, mesh, mat, scale, True)
    for k, v in (("Mueve", mueve), ("PuntoB", puntob), ("Periodo", periodo), ("Desfase", desfase),
                 ("Intermitente", intermitente), ("FraccionEncendido", fraccion), ("Activo", not intermitente)):
        a.set_editor_property(k, v)
    a.set_actor_label("TLP_Obs_" + label); a.set_folder_path("TLP/Obstaculos")
    log("peligro", label, loc)
    return a

def deco(label, mesh, mat, loc, scale):
    a = eas.spawn_actor_from_class(unreal.StaticMeshActor, loc, R())
    a.static_mesh_component.set_static_mesh(mesh); a.static_mesh_component.set_material(0, mat)
    a.set_actor_scale3d(scale)
    a.static_mesh_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    a.set_actor_label("TLP_Obs_" + label); a.set_folder_path("TLP/Obstaculos")

# 1. Barril en el paso muelle -> patio (x 10-16, y 32-36)
peligro("Barril_Paso", CYL, M["MI_Peligro"], V(1300, 3260, 40), V(0.8, 0.8, 1.4), R(pitch=90),
        mueve=True, puntob=V(0, 280, 0), periodo=3.5)
# 2. Gato de seguridad patrullando el patio
peligro("Gato_Patio", CUBE, M["MI_Peligro"], V(1800, 3700, 40), V(1.0, 0.6, 0.8),
        mueve=True, puntob=V(1100, 0, 0), periodo=7.0)
# 3. Troncos que barren la pasarela 3->4 (y 8-12)
for i, (x, d) in enumerate(((5000, 0.0), (5800, 1.2), (7800, 0.6))):
    peligro(f"Tronco_Pasarela_{i}", CYL, M["MI_Peligro"], V(x, 850, 40), V(0.8, 0.8, 1.4), R(pitch=90),
            mueve=True, puntob=V(0, 300, 0), periodo=2.4, desfase=d)
# 4. Letreros electrificados en el corredor (y 38-46)
for i, (x, d) in enumerate(((6000, 0.0), (6600, 1.5))):
    peligro(f"Electrico_{i}", CUBE, M["MI_Electrico"], V(x, 4200, 5), V(1.5, 7.8, 0.1),
            intermitente=True, periodo=3.0, desfase=d, fraccion=0.5)
    deco(f"Base_Electrica_{i}", CUBE, M["MI_Base_Electrica"], V(x, 4200, 1), V(1.6, 7.9, 0.02))

# 5. Cortar la pasarela 3->4 (x 42-86) y poner 3 tablas fragiles en x 64-70
p = L.get("BO_Pasarela_3_4")
if p:
    z = p.get_actor_location().z; sy = p.get_actor_scale3d().y; sz = p.get_actor_scale3d().z
    mat = p.static_mesh_component.get_material(0)
    p.set_actor_location(V(5300, 1000, z), False, False); p.set_actor_scale3d(V(22, sy, sz))
    b = eas.spawn_actor_from_class(unreal.StaticMeshActor, V(7800, 1000, z), R())
    b.static_mesh_component.set_static_mesh(CUBE); b.static_mesh_component.set_material(0, mat)
    b.set_actor_scale3d(V(16, sy, sz)); b.set_actor_label("TLP_Obs_Pasarela_Tramo_B"); b.set_folder_path(p.get_folder_path())
    for a in eas.get_all_level_actors():
        if a.get_actor_label().startswith("BO_Pasarela_Poste") and 6350 < a.get_actor_location().x < 7050:
            eas.destroy_actor(a); log("poste quitado", a)
    for i, x in enumerate((6500, 6700, 6900)):
        t = eas.spawn_actor_from_class(tab_c, V(x, 1000, z), R())
        setup_mesh(t, CUBE, M["MI_Fragil"], V(1.9, sy, sz), False)
        t.set_editor_property("Retraso", 0.5); t.set_editor_property("Reaparece", 3.0)
        t.set_editor_property("ZonaOffset", V(0, 0, -z + 72))
        t.set_editor_property("ZonaExtent", V(100, sy * 50 + 20, 40))
        t.set_actor_label(f"TLP_Obs_Tabla_{i}"); t.set_folder_path("TLP/Obstaculos")
        log("tabla", i, x, "z", z)
else:
    log("NO encontre BO_Pasarela_3_4")

unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
log("Nivel guardado")
open(os.path.join(unreal.Paths.project_saved_dir(), "tlp_obs3.txt"), "w", encoding="utf-8").write("\n".join(LOG))
