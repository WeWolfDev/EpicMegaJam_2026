# Obstaculos paso 1: Blueprints BP_TLP_Peligro y BP_TLP_TablaFragil + materiales
import unreal, os
LOG = []
def log(*a):
    s = " ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] " + s)
bel = unreal.BlueprintEditorLibrary
at = unreal.AssetToolsHelpers.get_asset_tools()
mel = unreal.MaterialEditingLibrary
BPDIR = "/Game/TheLastPatch/Blueprints"

def make_bp(name, parent):
    path = f"{BPDIR}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(path):
        return unreal.load_asset(path)
    f = unreal.BlueprintFactory(); f.set_editor_property("parent_class", parent)
    return at.create_asset(name, BPDIR, unreal.Blueprint, f)

def T(k):
    return bel.get_struct_type(unreal.Vector.static_struct()) if k == "vec" else bel.get_basic_type_by_name(k)

specs = {
    "BP_TLP_Peligro": [("Mueve", "bool"), ("PuntoB", "vec"), ("Periodo", "real"), ("Desfase", "real"),
                       ("Intermitente", "bool"), ("FraccionEncendido", "real"), ("Activo", "bool"), ("Inicio", "vec")],
    "BP_TLP_TablaFragil": [("Retraso", "real"), ("Reaparece", "real"), ("Cayendo", "bool")],
}
for name, vars_ in specs.items():
    bp = make_bp(name, unreal.StaticMeshActor)
    for v, t in vars_:
        ok = bel.add_member_variable(bp, v, T(t))
        try: bel.set_blueprint_variable_instance_editable(bp, v, True)
        except Exception as ex: log("editable ERROR", v, ex)
        log(name, v, ok)
    bel.compile_blueprint(bp)
    unreal.EditorAssetLibrary.save_loaded_asset(bp)

parent = unreal.load_asset("/Game/TheLastPatch/Blockout/M_Blockout")
def mi(name, color, rough):
    path = "/Game/TheLastPatch/Blockout/" + name
    m = unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else \
        at.create_asset(name, "/Game/TheLastPatch/Blockout", unreal.MaterialInstanceConstant, unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(m, parent)
    mel.set_material_instance_vector_parameter_value(m, "Color", unreal.LinearColor(*color, 1.0))
    mel.set_material_instance_scalar_parameter_value(m, "Roughness", rough)
    mel.update_material_instance(m)
    unreal.EditorAssetLibrary.save_loaded_asset(m)
    log("material", name)
mi("MI_Peligro", (0.85, 0.05, 0.05), 0.4)
mi("MI_Electrico", (1.0, 0.85, 0.05), 0.2)
mi("MI_Fragil", (0.75, 0.55, 0.30), 0.9)
mi("MI_Base_Electrica", (0.08, 0.08, 0.10), 0.6)
open(os.path.join(unreal.Paths.project_saved_dir(), "tlp_obs1.txt"), "w").write("\n".join(LOG))
