# Diagnostico tras la reorganizacion: guarda pendientes y busca referencias rotas
import unreal, os
eal = unreal.EditorAssetLibrary
ar = unreal.AssetRegistryHelpers.get_asset_registry()
L = []
unreal.EditorLoadingAndSavingUtils.save_dirty_packages(True, True)
opts = unreal.AssetRegistryDependencyOptions(include_soft_package_references=True, include_hard_package_references=True)
roots = ["/Game/_Game", "/Game/TheLastPatch", "/Game/OneMoreCast"]
pk = set()
for r in roots:
    if eal.does_directory_exist(r):
        for p in eal.list_assets(r, True, False):
            pk.add(p.split(".")[0])
pk.add("/Game/L_Puerto")
rotas = {}
for p in sorted(pk):
    deps = ar.get_dependencies(unreal.Name(p), opts) or []
    for d in deps:
        d = str(d)
        if d.startswith("/Game/") and not eal.does_asset_exist(d):
            rotas.setdefault(d, []).append(p)
L.append(f"paquetes revisados: {len(pk)}")
L.append(f"dependencias rotas: {len(rotas)}")
for d, users in sorted(rotas.items()):
    L.append(f"  {d}  <- {len(users)}: {users[:3]}")
left = eal.list_assets("/Game/TheLastPatch", True, False) if eal.does_directory_exist("/Game/TheLastPatch") else []
L.append(f"quedan en /Game/TheLastPatch: {len(left)}")
for a in left[:80]:
    d = ar.get_asset_by_object_path(a)
    L.append(f"  {a} [{d.asset_class_path.asset_name if d else '?'}]")
open(os.path.join(unreal.Paths.project_saved_dir(), "tlp_diag3.txt"), "w", encoding="utf-8").write("\n".join(L))
