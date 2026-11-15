import unreal, os
proj = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
out = os.path.join(proj, "Saved", "exp"); os.makedirs(out, exist_ok=True)
log=[]
for p in ["/Game/OneMoreCast/Fusion/BP_FusionTestRig", "/Game/OneMoreCast/Fusion/BP_FusionObject", "/Game/OneMoreCast/Fusion/BPC_SketchInventory", "/Game/TheLastPatch/Blueprints/BP_TLP_Mover"]:
    a = unreal.load_asset(p)
    t = unreal.AssetExportTask()
    t.object = a; t.filename = os.path.join(out, p.split("/")[-1] + ".t3d")
    t.automated = True; t.prompt = False; t.replace_identical = True
    ok = unreal.Exporter.run_asset_export_task(t)
    log.append("%s %s %s" % (p, ok, os.path.getsize(t.filename) if os.path.exists(t.filename) else -1))
open(os.path.join(proj, "Saved", "tlp_exp1.txt"), "w").write("\n".join(log))
