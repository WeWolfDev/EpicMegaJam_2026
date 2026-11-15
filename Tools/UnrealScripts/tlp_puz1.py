# Puzzles paso 1: crea BP_TLP_Mover y BP_TLP_Meta con sus variables
import unreal, os
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] " + s)

bel = unreal.BlueprintEditorLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
BPDIR = "/Game/TheLastPatch/Blueprints"

def make_bp(name, parent):
    path = f"{BPDIR}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.load_asset(path)
    f = unreal.BlueprintFactory(); f.set_editor_property("parent_class", parent)
    return at.create_asset(name, BPDIR, unreal.Blueprint, f)

def T(kind, arg=None):
    if kind == "obj":
        return bel.get_object_reference_type(arg)
    if kind == "struct":
        return bel.get_struct_type(arg)
    return bel.get_basic_type_by_name(kind)

fusion = unreal.load_asset("/Game/OneMoreCast/Fusion/BP_FusionObject").generated_class()

specs = {
    "BP_TLP_Mover": (unreal.Actor, [
        ("Receptor", ("obj", fusion)), ("Destino", ("obj", unreal.Actor)), ("Pieza", ("obj", unreal.Actor)),
        ("Vaiven", ("bool",)), ("Velocidad", ("real",)), ("Duracion", ("real",)),
        ("Activo", ("bool",)), ("Alpha", ("real",)), ("Inicio", ("struct", unreal.Vector.static_struct())),
    ]),
    "BP_TLP_Meta": (unreal.TriggerBox, [
        ("TagAnuncios", ("name",)), ("TagRestaurar", ("name",)), ("Resuelto", ("bool",)), ("Mensaje", ("string",)),
    ]),
}
for name, (parent, vars_) in specs.items():
    bp = make_bp(name, parent)
    for vname, t in vars_:
        try:
            ok = bel.add_member_variable(bp, vname, T(*t))
            try:
                bel.set_blueprint_variable_instance_editable(bp, vname, True)
            except Exception as ex:
                log("  instance editable ERROR", vname, ex)
            log(name, vname, ok)
        except Exception as ex:
            log(name, vname, "ERROR", ex)
    bel.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)

cdo = unreal.get_default_object(unreal.load_asset(f"{BPDIR}/BP_TLP_Mover").generated_class())
for k, v in (("Velocidad", 0.6), ("Duracion", 2.5)):
    try: cdo.set_editor_property(k, v); log("defecto", k, v)
    except Exception as ex: log("defecto ERROR", k, ex)
unreal.EditorAssetLibrary.save_asset(f"{BPDIR}/BP_TLP_Mover")
open(os.path.join(unreal.Paths.project_saved_dir(), "tlp_puz1.txt"), "w").write("\n".join(LOG))
