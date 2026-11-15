import unreal, os, shutil, filecmp
proj = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
content = os.path.join(proj, "Content")
bk = os.path.join(proj, "Respaldo_20261114_2146")
log = []
def L(s):
    log.append(str(s)); unreal.log("[TLP] " + str(s))

assert os.path.isdir(os.path.join(bk, "TheLastPatch")), "no backup"
EAL = unreal.EditorAssetLibrary

# 1. limpiar restos de _Game
if EAL.does_directory_exist("/Game/_Game"):
    L("delete _Game: %s" % EAL.delete_directory("/Game/_Game"))
g = os.path.join(content, "_Game")
if os.path.isdir(g):
    left = [os.path.join(r, f) for r, _, fs in os.walk(g) for f in fs]
    L("_Game files left on disk: %d" % len(left))
    shutil.rmtree(g, ignore_errors=True)
    L("_Game rmtree -> exists=%s" % os.path.isdir(g))

# 2. copiar TheLastPatch del respaldo
dst = os.path.join(content, "TheLastPatch")
shutil.copytree(os.path.join(bk, "TheLastPatch"), dst, dirs_exist_ok=True)
n = sum(len(fs) for _, _, fs in os.walk(dst))
L("TheLastPatch restored files: %d" % n)

# 3. nivel y config (solo si difieren)
for src, d in [(os.path.join(bk, "L_Puerto.umap"), os.path.join(content, "L_Puerto.umap")),
               (os.path.join(bk, "DefaultEngine.ini"), os.path.join(proj, "Config", "DefaultEngine.ini")),
               (os.path.join(bk, "DefaultGame.ini"), os.path.join(proj, "Config", "DefaultGame.ini"))]:
    if os.path.isfile(src):
        same = os.path.isfile(d) and filecmp.cmp(src, d, shallow=False)
        if not same:
            shutil.copy2(src, d)
        L("%s same=%s" % (os.path.basename(d), same))

# 4. reescanear
ar = unreal.AssetRegistryHelpers.get_asset_registry()
ar.scan_paths_synchronous(["/Game/TheLastPatch", "/Game"], True)
assets = EAL.list_assets("/Game/TheLastPatch", recursive=True)
L("assets in /Game/TheLastPatch: %d" % len(assets))

# 5. abrir L_Puerto y revisar dependencias
les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
L("load L_Puerto: %s" % les.load_level("/Game/L_Puerto"))
opts = unreal.AssetRegistryDependencyOptions(True, True, True, True, True)
def deps(pkg):
    try:
        return ar.get_dependencies(pkg, opts) or []
    except Exception as e:
        return []
missing = set(); seen = set(); stack = ["/Game/L_Puerto"]
while stack:
    p = str(stack.pop())
    if p in seen: continue
    seen.add(p)
    for d in deps(p):
        d = str(d)
        if not d.startswith("/Game"): continue
        if not EAL.does_asset_exist(d):
            missing.add(d)
        else:
            stack.append(d)
L("packages checked: %d" % len(seen))
L("MISSING: %d" % len(missing))
for m in sorted(missing): L("  " + m)
open(os.path.join(proj, "Saved", "tlp_restore2.txt"), "w").write("\n".join(log))
