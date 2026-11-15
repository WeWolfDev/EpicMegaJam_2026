# Diagnostico: control del personaje y rendimiento. Escribe Saved/TLP_diag.txt
import os, collections, traceback, unreal

PROJ = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
OUT = os.path.join(PROJ, "Saved", "TLP_diag.txt")
L = []
def w(*a): L.append(" ".join(str(x) for x in a))

def safe(fn, label):
    try:
        fn()
    except Exception as e:
        w("ERROR", label, e)

actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
world = unreal.EditorLevelLibrary.get_editor_world()

def gm():
    ws = world.get_world_settings()
    ov = ws.get_editor_property("default_game_mode")
    w("WorldSettings GameMode override:", ov.get_path_name() if ov else None)
    maps = unreal.get_default_object(unreal.GameMapsSettings)
    for p in ["editor_startup_map", "game_default_map", "global_default_game_mode"]:
        safe(lambda p=p: w("GameMapsSettings", p, maps.get_editor_property(p)), p)
    for path in ["/Game/TheLastPatch/Blueprints/BP_TheLastPatchGameMode",
                 "/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode"]:
        bp = unreal.load_asset(path)
        if not bp:
            w("no existe", path); continue
        cdo = unreal.get_default_object(bp.generated_class())
        for p in ["default_pawn_class", "player_controller_class", "hud_class"]:
            safe(lambda p=p: w(path.rsplit('/', 1)[1], p, cdo.get_editor_property(p)), p)
safe(gm, "gamemode")

def ps():
    for a in actors.get_all_level_actors():
        if isinstance(a, unreal.PlayerStart):
            w("PlayerStart", a.get_actor_label(), a.get_actor_location())
        if isinstance(a, unreal.Pawn) or "Character" in a.get_class().get_name():
            w("Pawn en nivel", a.get_actor_label(), a.get_class().get_name(),
              "auto_possess", a.get_editor_property("auto_possess_player"))
safe(ps, "playerstart")

def counts():
    c = collections.Counter(a.get_class().get_name() for a in actors.get_all_level_actors())
    w("ACTORES total", sum(c.values()))
    for k, v in c.most_common(25):
        w("  ", k, v)
    lights = [a for a in actors.get_all_level_actors() if isinstance(a, unreal.Light)]
    for l in lights:
        comp = l.light_component
        w("LUZ", l.get_actor_label(), l.get_class().get_name(), "mov", comp.get_editor_property("mobility"),
          "sombras", comp.get_editor_property("cast_shadows"))
    for cls in [unreal.ExponentialHeightFog, unreal.SkyLight, unreal.PostProcessVolume]:
        w("hay", cls.__name__, len([a for a in actors.get_all_level_actors() if isinstance(a, cls)]))
safe(counts, "counts")

def rendering():
    r = unreal.get_default_object(unreal.RendererSettings)
    for p in ["dynamic_global_illumination_method", "reflection_method", "shadow_map_method",
              "generate_mesh_distance_fields", "virtual_textures", "anti_aliasing_method",
              "default_feature_anti_aliasing", "support_hardware_ray_tracing", "nanite"]:
        safe(lambda p=p: w("Render", p, r.get_editor_property(p)), p)
safe(rendering, "render")

def assets():
    ar = unreal.AssetRegistryHelpers.get_asset_registry()
    for root in ["/Game/EpicMegaJam_2026", "/Game/TheLastPatch"]:
        data = ar.get_assets_by_path(root, recursive=True)
        c = collections.Counter(str(d.asset_class_path.asset_name) for d in data)
        w("ASSETS", root, sum(c.values()), dict(c))
safe(assets, "assets")

def dirty():
    pk = unreal.EditorLoadingAndSavingUtils.get_dirty_content_packages()
    w("paquetes sin guardar:", len(pk))
    for p in pk[:40]:
        w("  ", p.get_name())
safe(dirty, "dirty")

open(OUT, "w", encoding="utf-8").write("\n".join(L))
unreal.log("TLP diag listo")
