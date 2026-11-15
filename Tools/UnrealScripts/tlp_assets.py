# The Last Patch - importa Assets_Mapa, crea materiales y los aplica al blockout.
# Ejecutar en Unreal 5.8:  exec(open(r"<proyecto>/Scripts/tlp_assets.py", encoding="utf-8").read())
# Escribe un reporte en Saved/TLP_reporte.txt

import os, glob, math, traceback
import unreal

PROJ = unreal.Paths.convert_relative_path_to_full(unreal.Paths.project_dir())
SRC = os.path.join(PROJ, "Content", "EpicMegaJam_2026", "Assets_Mapa")
REPORT = os.path.join(PROJ, "Saved", "TLP_reporte.txt")
open(REPORT, "w", encoding="utf-8").write("")

def log(*a):
    s = " ".join(str(x) for x in a)
    unreal.log("TLP " + s)
    with open(REPORT, "a", encoding="utf-8") as fh:
        fh.write(s + "\n")
M = 100.0

tools = unreal.AssetToolsHelpers.get_asset_tools()
eal = unreal.EditorAssetLibrary
mel = unreal.MaterialEditingLibrary
actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)

DST = {
    "og": "/Game/TheLastPatch/Texturas/OG",
    "ue": "/Game/TheLastPatch/Texturas/UE",
    "s_ue": "/Game/TheLastPatch/Senaletica/UE",
    "s_og": "/Game/TheLastPatch/Senaletica/OG",
    "ui": "/Game/TheLastPatch/UI",
}
MAT_DIR = "/Game/TheLastPatch/Materiales"


# ------------------------------------------------------------------ 1. importar texturas
def import_folder(src_dir, dst, pattern="*.png"):
    files = sorted(glob.glob(os.path.join(src_dir, pattern)))
    tasks = []
    for f in files:
        t = unreal.AssetImportTask()
        t.set_editor_property("filename", f)
        t.set_editor_property("destination_path", dst)
        t.set_editor_property("automated", True)
        t.set_editor_property("replace_existing", True)
        t.set_editor_property("save", False)
        tasks.append(t)
    if tasks:
        tools.import_asset_tasks(tasks)
    out = {}
    for f in files:
        name = os.path.splitext(os.path.basename(f))[0]
        a = unreal.load_asset(dst + "/" + name)
        if a:
            out[name] = a
        else:
            log("ERROR no se importo", f)
    log("importadas", len(out), "de", len(files), "->", dst)
    return out


def setp(obj, prop, val):
    try:
        obj.set_editor_property(prop, val)
    except Exception as e:
        log("aviso", obj.get_name(), prop, e)


def cfg(tex, kind):
    if kind == "pixel":
        setp(tex, "filter", unreal.TextureFilter.TF_NEAREST)
        setp(tex, "mip_gen_settings", unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
    elif kind == "normal":
        setp(tex, "compression_settings", unreal.TextureCompressionSettings.TC_NORMALMAP)
        setp(tex, "srgb", False)
    elif kind == "masks":
        setp(tex, "compression_settings", unreal.TextureCompressionSettings.TC_MASKS)
        setp(tex, "srgb", False)
    elif kind == "ui":
        setp(tex, "compression_settings", unreal.TextureCompressionSettings.TC_EDITOR_ICON)
        setp(tex, "lod_group", unreal.TextureGroup.TEXTUREGROUP_UI)
        setp(tex, "mip_gen_settings", unreal.TextureMipGenSettings.TMGS_NO_MIPMAPS)
    eal.save_loaded_asset(tex)


TEX_OG = import_folder(os.path.join(SRC, "Texturas", "OG_LowPoly"), DST["og"])
for t in TEX_OG.values():
    cfg(t, "pixel")
TEX_UE = import_folder(os.path.join(SRC, "Texturas", "UE_Pulido"), DST["ue"])
for n, t in TEX_UE.items():
    cfg(t, "normal" if n.endswith("_N") else "masks" if n.endswith("_ORM") else "color")
SEN_UE = import_folder(os.path.join(SRC, "Senaletica", "UE_Pulido"), DST["s_ue"])
for t in SEN_UE.values():
    cfg(t, "color")
SEN_OG = import_folder(os.path.join(SRC, "Senaletica", "OG_LowPoly"), DST["s_og"])
for t in SEN_OG.values():
    cfg(t, "pixel")
UI = import_folder(os.path.join(SRC, "UI"), DST["ui"])
for t in UI.values():
    cfg(t, "ui")


# ------------------------------------------------------------------ 2. materiales maestros
def E(mat, cls, x, y):
    return mel.create_material_expression(mat, cls, x, y)


def link(a, out, b, inp):
    ok = mel.connect_material_expressions(a, out, b, inp)
    if not ok:
        log("aviso: no conecto", a.get_name(), out, "->", b.get_name(), inp)
    return ok


def new_material(name):
    path = MAT_DIR + "/" + name
    if eal.does_asset_exist(path):
        eal.delete_asset(path)  # se rehace limpio (las instancias se vuelven a apuntar abajo)
    return tools.create_asset(name, MAT_DIR, unreal.Material, unreal.MaterialFactoryNew())


def triplanar_coords(mat):
    """Proyeccion en espacio mundo: 1 repeticion cada 'Escala_cm' (200 por defecto)."""
    wp = E(mat, unreal.MaterialExpressionWorldPosition, -1800, 0)
    sc = E(mat, unreal.MaterialExpressionScalarParameter, -1800, 150)
    sc.set_editor_property("parameter_name", "Escala_cm")
    sc.set_editor_property("default_value", 200.0)
    div = E(mat, unreal.MaterialExpressionDivide, -1600, 50)
    link(wp, "", div, "A")
    link(sc, "", div, "B")
    masks = {}
    for i, (key, r, g, b) in enumerate([("xy", True, True, False), ("xz", True, False, True), ("yz", False, True, True)]):
        m = E(mat, unreal.MaterialExpressionComponentMask, -1400, i * 120)
        m.set_editor_property("r", r); m.set_editor_property("g", g); m.set_editor_property("b", b)
        link(div, "", m, "")
        masks[key] = m
    nws = E(mat, unreal.MaterialExpressionVertexNormalWS, -1400, 450)
    ab = E(mat, unreal.MaterialExpressionAbs, -1250, 450)
    link(nws, "", ab, "")
    nx = E(mat, unreal.MaterialExpressionComponentMask, -1100, 420)
    nx.set_editor_property("r", True)
    nz = E(mat, unreal.MaterialExpressionComponentMask, -1100, 500)
    nz.set_editor_property("b", True)
    link(ab, "", nx, "")
    link(ab, "", nz, "")
    return masks, nx, nz


def triplanar_sample(mat, coords, pname, tex, stype, y):
    masks, nx, nz = coords
    s = {}
    for i, key in enumerate(["xy", "xz", "yz"]):
        t = E(mat, unreal.MaterialExpressionTextureSampleParameter2D, -900, y + i * 220)
        t.set_editor_property("parameter_name", pname)
        t.set_editor_property("texture", tex)
        t.set_editor_property("sampler_type", stype)
        link(masks[key], "", t, "UVs")
        s[key] = t
    l1 = E(mat, unreal.MaterialExpressionLinearInterpolate, -600, y)
    link(s["xz"], "RGB", l1, "A")
    link(s["yz"], "RGB", l1, "B")
    link(nx, "", l1, "Alpha")
    l2 = E(mat, unreal.MaterialExpressionLinearInterpolate, -450, y)
    link(l1, "", l2, "A")
    link(s["xy"], "RGB", l2, "B")
    link(nz, "", l2, "Alpha")
    return l2


def any_tex(d, suffix):
    for n, t in sorted(d.items()):
        if n.endswith(suffix):
            return t


ST = unreal.MaterialSamplerType
MP = unreal.MaterialProperty

# M_TLP_OG: pixel art plano, sin PBR
m_og = new_material("M_TLP_OG")
c = triplanar_coords(m_og)
bc = triplanar_sample(m_og, c, "Textura", any_tex(TEX_OG, "_64"), ST.SAMPLERTYPE_COLOR, 0)
mel.connect_material_property(bc, "", MP.MP_BASE_COLOR)
r1 = E(m_og, unreal.MaterialExpressionConstant, -300, 300); r1.set_editor_property("r", 1.0)
mel.connect_material_property(r1, "", MP.MP_ROUGHNESS)
s0 = E(m_og, unreal.MaterialExpressionConstant, -300, 380); s0.set_editor_property("r", 0.0)
mel.connect_material_property(s0, "", MP.MP_SPECULAR)
mel.recompile_material(m_og); eal.save_loaded_asset(m_og)
log("material M_TLP_OG listo")

# M_TLP_UE: PBR con BC + N + ORM
m_ue = new_material("M_TLP_UE")
c = triplanar_coords(m_ue)
bc = triplanar_sample(m_ue, c, "BC", any_tex(TEX_UE, "_BC"), ST.SAMPLERTYPE_COLOR, 0)
nn = triplanar_sample(m_ue, c, "N", any_tex(TEX_UE, "_N"), ST.SAMPLERTYPE_NORMAL, 800)
orm = triplanar_sample(m_ue, c, "ORM", any_tex(TEX_UE, "_ORM"), ST.SAMPLERTYPE_MASKS, 1600)
mel.connect_material_property(bc, "", MP.MP_BASE_COLOR)
mel.connect_material_property(nn, "", MP.MP_NORMAL)
for i, (ch, prop) in enumerate([("r", MP.MP_AMBIENT_OCCLUSION), ("g", MP.MP_ROUGHNESS), ("b", MP.MP_METALLIC)]):
    mk = E(m_ue, unreal.MaterialExpressionComponentMask, -250, 1600 + i * 100)
    mk.set_editor_property(ch, True)
    link(orm, "", mk, "")
    mel.connect_material_property(mk, "", prop)
mel.recompile_material(m_ue); eal.save_loaded_asset(m_ue)
log("material M_TLP_UE listo")

# M_TLP_Senal: carteles (UV del objeto), algo emisivo para que lo comercial brille
m_s = new_material("M_TLP_Senal")
tx = E(m_s, unreal.MaterialExpressionTextureSampleParameter2D, -700, 0)
tx.set_editor_property("parameter_name", "Textura")
tx.set_editor_property("texture", any_tex(SEN_UE, ""))
mel.connect_material_property(tx, "RGB", MP.MP_BASE_COLOR)
br = E(m_s, unreal.MaterialExpressionScalarParameter, -700, 250)
br.set_editor_property("parameter_name", "Brillo"); br.set_editor_property("default_value", 0.3)
mu = E(m_s, unreal.MaterialExpressionMultiply, -400, 150)
link(tx, "RGB", mu, "A"); link(br, "", mu, "B")
mel.connect_material_property(mu, "", MP.MP_EMISSIVE_COLOR)
rg = E(m_s, unreal.MaterialExpressionConstant, -400, 300); rg.set_editor_property("r", 0.3)
mel.connect_material_property(rg, "", MP.MP_ROUGHNESS)
mel.recompile_material(m_s); eal.save_loaded_asset(m_s)
log("material M_TLP_Senal listo")


# ------------------------------------------------------------------ 3. instancias
def instance(name, parent, textures, scalars=None):
    path = MAT_DIR + "/" + name
    if eal.does_asset_exist(path):
        mi = unreal.load_asset(path)
    else:
        mi = tools.create_asset(name, MAT_DIR, unreal.MaterialInstanceConstant,
                                unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(mi, parent)
    for p, t in textures.items():
        mel.set_material_instance_texture_parameter_value(mi, p, t)
    for p, v in (scalars or {}).items():
        mel.set_material_instance_scalar_parameter_value(mi, p, v)
    mel.update_material_instance(mi)
    eal.save_loaded_asset(mi)
    return mi


MI_OG, MI_UE, MI_S, MI_SOG = {}, {}, {}, {}
for n, t in TEX_OG.items():                       # T_OG_MaderaMuelle_64 -> MaderaMuelle
    key = n[len("T_OG_"):-len("_64")]
    MI_OG[key] = instance("MI_OG_" + key, m_og, {"Textura": t})
for n, t in TEX_UE.items():
    if n.endswith("_BC"):
        key = n[len("T_UE_"):-len("_BC")]
        tx = {"BC": t}
        if ("T_UE_%s_N" % key) in TEX_UE: tx["N"] = TEX_UE["T_UE_%s_N" % key]
        if ("T_UE_%s_ORM" % key) in TEX_UE: tx["ORM"] = TEX_UE["T_UE_%s_ORM" % key]
        MI_UE[key] = instance("MI_UE_" + key, m_ue, tx)
for n, t in SEN_UE.items():                       # T_Senal_X -> X
    key = n[len("T_Senal_"):]
    MI_S[key] = instance("MI_Senal_" + key, m_s, {"Textura": t})
for n, t in SEN_OG.items():
    key = n[len("T_OG_Senal_"):]
    MI_SOG[key] = instance("MI_OG_Senal_" + key, m_s, {"Textura": t}, {"Brillo": 0.0})
log("instancias OG", len(MI_OG), "UE", len(MI_UE), "senal", len(MI_S), "senal OG", len(MI_SOG))


# ------------------------------------------------------------------ 4. aplicar al blockout
POSTERS = ["Poster_Sale", "Poster_Hot", "Poster_4K", "Poster_Vip", "Poster_Ya",
           "Poster_Menos80", "Poster_New", "Poster_Top", "Poster_MasXP", "Poster_Dlc"]
_pi = [0]
def next_poster():
    k = POSTERS[_pi[0] % len(POSTERS)]; _pi[0] += 1
    return MI_S.get(k)


def pick(label, cur):
    L = label
    if L == "Agua": return MI_UE.get("Agua")
    if L.endswith("_Poste") and L.startswith("Anuncio"): return MI_UE.get("PanelComercial")
    if L in ("Valla_Publicitaria", "Anuncio_Faro"): return MI_S.get("Valla_RemakeUltraHD")
    if L.startswith("Anuncio_Corredor_S_0") or L.startswith("Anuncio_Corredor_N_2"): return MI_S.get("Valla_MegaOferta")
    if L.startswith("Anuncio_"): return next_poster()
    if L == "Caja_OG": return MI_SOG.get("CajaOG_Cara")
    if L in ("Caja_Comercial", "Caja_Anuncio_Alt"): return MI_S.get("CajaComercial_Cara")
    if L in ("Mural", "Mural_Final"): return MI_S.get("Mural_Antiguo")
    if L == "Ascensor_Marca": return MI_S.get("Cartel_AccesoVIP")
    if L.startswith("Cortina"): return MI_UE.get("Telon")
    if L == "Logo_Estudio": return MI_S.get("Banda_PresentacionExclusiva")
    if L == "Expositor_Acolchado": return MI_UE.get("Acolchado")
    if L == "Escenario": return MI_UE.get("PisoEscenario")
    if L.startswith("Cinta_Obra"): return MI_S.get("Barrera_Precaucion")
    if L.startswith("Cono_Obra"): return MI_UE.get("Precaucion")
    if L.startswith("Grua_Marca"): return MI_UE.get("ContenedorMarca")
    if L.startswith("Grua_"): return MI_UE.get("MetalGrua")
    if L == "Faro": return MI_UE.get("EstucoFaro")
    if L.startswith(("Bolardo", "Barril", "Pasarela_Poste", "Muelle_Alto_Soporte", "Farol_")) and "Luz" not in L:
        return MI_OG.get("MaderaOscura")
    if cur == "MI_OG_Madera": return MI_OG.get("MaderaMuelle")
    if cur == "MI_Comercial":
        if L in ("Patio", "Corredor", "Orilla_A", "Hueco_Valla"): return MI_UE.get("ConcretoMuelle")
        return MI_UE.get("PanelComercial")
    if cur == "MI_Suelo": return MI_UE.get("ConcretoMuelle")
    if cur == "MI_Anuncio": return MI_UE.get("ContenedorMarca")
    return None


changed, kept = 0, []
with unreal.ScopedEditorTransaction("TLP materiales"):
    for a in actors.get_all_level_actors():
        lab = a.get_actor_label()
        if not lab.startswith("BO_") or not isinstance(a, unreal.StaticMeshActor):
            continue
        comp = a.static_mesh_component
        cur_m = comp.get_material(0)
        cur = cur_m.get_name() if cur_m else ""
        new = pick(lab[3:], cur)
        if new:
            comp.set_material(0, new)
            changed += 1
        else:
            kept.append(lab[3:])
log("actores con material nuevo:", changed)
log("sin cambio (se quedan con color de blockout):", ", ".join(sorted(set(kept))))


# ------------------------------------------------------------------ 5. senaletica nueva
CUBE = unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
CYL = unreal.load_asset("/Engine/BasicShapes/Cylinder.Cylinder")

def clear(prefix):
    for a in actors.get_all_level_actors():
        if a.get_actor_label().startswith(prefix):
            actors.destroy_actor(a)

def piece(name, x0, x1, y0, y1, z_top, h, mi, mesh=CUBE, tags=None, hidden=False):
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, z_top - h / 2
    a = actors.spawn_actor_from_class(unreal.StaticMeshActor, unreal.Vector(cx * M, cy * M, cz * M))
    a.static_mesh_component.set_static_mesh(mesh)
    if mi: a.static_mesh_component.set_material(0, mi)
    a.set_actor_scale3d(unreal.Vector(x1 - x0, y1 - y0, h))
    a.set_actor_label("BO_" + name)
    a.set_folder_path("Blockout/Senaletica")
    if tags: a.set_editor_property("tags", [unreal.Name(t) for t in tags])
    if hidden: a.set_actor_hidden_in_game(True)
    return a

def sign(name, key, x0, x1, y0, y1, z_top, h, tags=None, hidden=False):
    piece("Senal_" + name, x0, x1, y0, y1, z_top, h, MI_S.get(key), tags=tags, hidden=hidden)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    piece("Senal_" + name + "_Poste", cx - 0.08, cx + 0.08, cy - 0.08, cy + 0.08, z_top - h, z_top - h,
          MI_OG.get("MaderaOscura"), mesh=CYL, tags=tags, hidden=hidden)

with unreal.ScopedEditorTransaction("TLP senaletica"):
    clear("BO_Senal_")
    sign("Zona_0", "Zona_0", 3, 7, 12, 12.1, 3.0, 1.0)                     # mira al sur, al llegar
    sign("Zona_1", "Zona_1", 16.2, 16.3, 37, 41, 3.0, 1.0)                 # entrada del patio
    sign("Zona_2", "Zona_2", 56.2, 56.3, 39, 43, 3.0, 1.0)                 # entrada del corredor
    sign("Zona_3", "Zona_3", 86.2, 86.3, 40, 44, 3.0, 1.0)                 # orilla A
    sign("Zona_4", "Zona_4", 42.9, 43.0, 12.5, 16.5, 3.0, 1.0)             # entrada del escenario
    sign("Zona_5", "Zona_5", 3, 7, 0.6, 0.7, 3.0, 1.0, tags=["Restore_Final"], hidden=True)
    sign("PuenteCerrado", "PuenteCerrado", 95, 97, 33.6, 33.7, 2.4, 2.0)
    sign("Flecha_Corredor", "Flecha_Derecha", 50, 51, 43.6, 43.7, 6.5, 1.0)
    sign("Flecha_Pasarela", "Flecha_Izquierda", 62, 63, 12.3, 12.4, 1.8, 1.0)
log("senaletica nueva colocada en Blockout/Senaletica")


# ------------------------------------------------------------------ 6. guardar
try:
    eal.save_directory("/Game/TheLastPatch", only_if_is_dirty=True, recursive=True)
    unreal.get_editor_subsystem(unreal.LevelEditorSubsystem).save_current_level()
    log("guardado: assets de /Game/TheLastPatch y el nivel")
except Exception as e:
    log("aviso al guardar:", e)

log("FIN")
