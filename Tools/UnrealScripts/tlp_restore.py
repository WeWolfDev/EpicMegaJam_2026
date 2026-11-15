# Restaura TheLastPatch + L_Puerto desde el respaldo de las 21:46
import unreal, os, shutil
L = []
def log(*a):
    s = " ".join(str(x) for x in a); L.append(s); unreal.log("[TLP] " + s)
proj = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
content = os.path.join(proj, "Content")
bk = os.path.join(proj, "Respaldo_20261114_2146")
out = os.path.join(proj, "Saved", "tlp_restore.txt")
def dump(): open(out, "w", encoding="utf-8").write("\n".join(L))
eal = unreal.EditorAssetLibrary
aes = unreal.get_editor_subsystem(unreal.AssetEditorSubsystem)
les = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)

assert os.path.isdir(os.path.join(bk, "TheLastPatch")) and os.path.isfile(os.path.join(bk, "L_Puerto.umap")), "falta el respaldo"
les.load_level("/Game/ThirdPerson/Lvl_ThirdPerson")

for root in ("/Game/_Game", "/Game/TheLastPatch"):
    if eal.does_directory_exist(root):
        for p in eal.list_assets(root, True, False):
            a = unreal.load_asset(p)
            if a:
                try: aes.close_all_editors_for_asset(a)
                except Exception: pass
        ok = eal.delete_directory(root)
        log("borrar", root, ok)
dump()

for d in ("_Game", "TheLastPatch"):
    full = os.path.join(content, d)
    if os.path.isdir(full):
        rest = [os.path.join(r, f) for r, _, fs in os.walk(full) for f in fs]
        log("en disco quedan", d, len(rest), rest[:5])
        if rest:
            dump(); raise SystemExit("no se pudo borrar todo; me detengo sin copiar")
        shutil.rmtree(full, ignore_errors=True)

shutil.copytree(os.path.join(bk, "TheLastPatch"), os.path.join(content, "TheLastPatch"))
shutil.copy2(os.path.join(bk, "L_Puerto.umap"), os.path.join(content, "L_Puerto.umap"))
log("respaldo copiado")
ar = unreal.AssetRegistryHelpers.get_asset_registry()
ar.scan_paths_synchronous(["/Game/TheLastPatch", "/Game"], True, True)
lp = unreal.find_package("/Game/L_Puerto") if hasattr(unreal, "find_package") else None
if lp:
    unreal.EditorLoadingAndSavingUtils.reload_packages([lp])
    log("L_Puerto recargado")
les.load_level("/Game/L_Puerto")
log("L_Puerto abierto")
dump()

# verificacion
opts = unreal.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True)
pk = {p.split(".")[0] for r in ("/Game/TheLastPatch", "/Game/OneMoreCast") for p in eal.list_assets(r, True, False)}
pk.add("/Game/L_Puerto")
rotas = {}
for p in pk:
    for d in ar.get_dependencies(unreal.Name(p), opts) or []:
        d = str(d)
        if d.startswith("/Game/") and not eal.does_asset_exist(d):
            rotas.setdefault(d, []).append(p)
log("paquetes revisados", len(pk), "| referencias rotas", len(rotas))
for d, u in list(rotas.items())[:20]:
    log("  rota", d, "<-", u[:2])
log("_Game existe:", eal.does_directory_exist("/Game/_Game"))
dump()
