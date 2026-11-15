# Reorganiza el contenido propio a Content/_Game segun CONTRIBUTING.md del equipo.
# 1) respaldo  2) mover carpetas  3) arreglar redirectores  4) abrir el nivel movido
import unreal, os, shutil, time
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] " + s)
proj = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
content = os.path.join(proj, "Content")
out = os.path.join(proj, "Saved", "tlp_reorg.txt")
def dump(): open(out, "w", encoding="utf-8").write("\n".join(LOG))

eal = unreal.EditorAssetLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)

# 0. guardar todo
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

# 1. respaldo (fuera de Content para que Unreal no lo lea)
bk = os.path.join(proj, "Respaldo_" + time.strftime("%Y%m%d_%H%M"))
os.makedirs(bk, exist_ok=True)
shutil.copytree(os.path.join(content, "TheLastPatch"), os.path.join(bk, "TheLastPatch"), dirs_exist_ok=True)
shutil.copy2(os.path.join(content, "L_Puerto.umap"), bk)
for f in ("DefaultEngine.ini", "DefaultGame.ini"):
    shutil.copy2(os.path.join(proj, "Config", f), bk)
log("respaldo en", bk)
dump()

# 2. salir del nivel para poder moverlo
les.load_level("/Game/ThirdPerson/Lvl_ThirdPerson")
log("nivel temporal cargado")

moves = [
    ("/Game/TheLastPatch/Blueprints", "/Game/_Game/Core/Blueprints"),
    ("/Game/TheLastPatch/Blockout",   "/Game/_Game/Materials/Blockout"),
    ("/Game/TheLastPatch/Materiales", "/Game/_Game/Materials/Materiales"),
    ("/Game/TheLastPatch/Texturas",   "/Game/_Game/Materials/Texturas"),
    ("/Game/TheLastPatch/Senaletica", "/Game/_Game/Props/Senaletica"),
    ("/Game/TheLastPatch/UI",         "/Game/_Game/UI"),
    ("/Game/TheLastPatch/Personajes", "/Game/_Game/Characters"),
]
for src, dst in moves:
    if not eal.does_directory_exist(src):
        log("no existe", src); continue
    ok = eal.rename_directory(src, dst)
    log("mover", src, "->", dst, ok)
ok = eal.rename_asset("/Game/L_Puerto", "/Game/_Game/Levels/L_Puerto")
log("mover nivel /Game/L_Puerto -> /Game/_Game/Levels/L_Puerto", ok)
dump()

# 3. arreglar redirectores
ar = unreal.AssetRegistryHelpers.get_asset_registry()
flt = unreal.ARFilter(package_paths=["/Game"], recursive_paths=True,
                      class_paths=[unreal.TopLevelAssetPath("/Script/CoreUObject", "ObjectRedirector")])
reds = ar.get_assets(flt)
objs = [r.get_asset() for r in reds]
objs = [o for o in objs if o]
log("redirectores encontrados", len(objs))
if objs:
    at.fixup_referencers(objs)
reds2 = ar.get_assets(flt)
log("redirectores restantes", len(reds2), [str(r.package_name) for r in reds2][:10])
if eal.does_directory_exist("/Game/TheLastPatch"):
    left = eal.list_assets("/Game/TheLastPatch", True, False)
    log("quedan en /Game/TheLastPatch:", left)
    if not left:
        eal.delete_directory("/Game/TheLastPatch"); log("carpeta vieja borrada")
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)

# 4. volver al nivel
les.load_level("/Game/_Game/Levels/L_Puerto")
log("nivel abierto en su nueva ruta")
dump()
