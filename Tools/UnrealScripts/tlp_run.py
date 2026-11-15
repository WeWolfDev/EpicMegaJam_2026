# Ejecuta tlp_assets.py y deja cualquier error en Saved/TLP_reporte.txt
import os, traceback, unreal
_d = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()), "Scripts")
_rep = os.path.join(unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir()), "Saved", "TLP_reporte.txt")
try:
    exec(open(os.path.join(_d, "tlp_assets.py"), encoding="utf-8").read(), {"__name__": "__main__"})
except Exception:
    with open(_rep, "a", encoding="utf-8") as fh:
        fh.write("ERROR\n" + traceback.format_exc())
    unreal.log_error(traceback.format_exc())
