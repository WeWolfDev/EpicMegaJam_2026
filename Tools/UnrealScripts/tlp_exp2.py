import unreal, os
proj = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
out = os.path.join(proj, "Saved", "exp"); os.makedirs(out, exist_ok=True)
for a in unreal.EditorAssetLibrary.list_assets("/Game/TheLastPatch/Blueprints", recursive=False):
    p = a.split(".")[0]; o = unreal.load_asset(p)
    if not isinstance(o, unreal.Blueprint): continue
    t = unreal.AssetExportTask(); t.object = o; t.filename = os.path.join(out, p.split("/")[-1] + ".t3d")
    t.automated = True; t.prompt = False; t.replace_identical = True
    unreal.Exporter.run_asset_export_task(t)
