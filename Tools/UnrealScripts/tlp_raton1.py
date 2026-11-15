# Paso 1: sombras + extraer el modelo del raton desde el zip. Escribe Saved/TLP_raton1.txt
import os, zipfile, traceback, unreal
PROJ = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
OUT = os.path.join(PROJ, "Saved", "TLP_raton1.txt")
ZIP = r"C:\Users\crod3\Downloads\EpicMegaJam_2026.zip"
DEST = os.path.join(PROJ, "Imports", "Raton")
L = []
def w(*a): L.append(" ".join(str(x) for x in a))
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

# --- sombras
try:
    with unreal.ScopedEditorTransaction("TLP sombras 2"):
        for a in actors.get_all_level_actors():
            lab = a.get_actor_label()
            if lab.startswith("BO_Limite_") or lab == "BO_Agua":
                c = a.static_mesh_component
                c.set_cast_shadow(False)
                if lab.startswith("BO_Limite_"):
                    c.set_visibility(False)          # invisibles tambien en el editor; la colision sigue
                w("sin sombra:", lab)
            if isinstance(a, unreal.DirectionalLight):
                a.set_actor_rotation(unreal.Rotator(roll=0.0, pitch=-42.0, yaw=225.0), False)
                w("sol a -42 grados")
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    w("nivel guardado")
except Exception:
    w("ERROR sombras", traceback.format_exc())

# --- zip
try:
    z = zipfile.ZipFile(ZIP)
    names = z.namelist()
    w("entradas en zip:", len(names))
    keys = ("retro_mouse", "Player_lowpoly", "Lobo_lowpoly", "Foca_lowpoly")
    hits = [n for n in names if any(k in n for k in keys)]
    for n in hits:
        w("ZIP", n, z.getinfo(n).file_size)
    os.makedirs(DEST, exist_ok=True)
    for n in hits:
        if n.endswith("/") or "retro_mouse" not in n and "Player_lowpoly" not in n:
            continue
        base = os.path.basename(n)
        if not base:
            continue
        target = os.path.join(DEST, base)
        with z.open(n) as src, open(target, "wb") as dst:
            dst.write(src.read())
        w("extraido ->", target)
except Exception:
    w("ERROR zip", traceback.format_exc())

open(OUT, "w", encoding="utf-8").write("\n".join(L))
unreal.log("TLP raton1 listo")
