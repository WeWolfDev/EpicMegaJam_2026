# Fin paso 1: crea BP_TLP_Vida, BP_TLP_Charla, BP_TLP_Final, BP_TLP_Pausa y MI_Queso
import unreal, os
LOG=[]
def log(*a):
    s=" ".join(str(x) for x in a); LOG.append(s); unreal.log("[TLP] "+s)
bel=unreal.BlueprintEditorLibrary; at=unreal.AssetToolsHelpers.get_asset_tools(); mel=unreal.MaterialEditingLibrary
BPDIR="/Game/TheLastPatch/Blueprints"
def make_bp(name,parent):
    path=f"{BPDIR}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(path): return unreal.load_asset(path)
    f=unreal.BlueprintFactory(); f.set_editor_property("parent_class",parent)
    return at.create_asset(name,BPDIR,unreal.Blueprint,f)
def cls(p): return unreal.load_asset(p).generated_class()
FUS=cls("/Game/OneMoreCast/Fusion/BP_FusionObject"); META=cls(f"{BPDIR}/BP_TLP_Meta")
def T(k):
    if k=="vec": return bel.get_struct_type(unreal.Vector.static_struct())
    if isinstance(k,str): return bel.get_basic_type_by_name(k)
    return bel.get_object_reference_type(k)
A=unreal.Actor
specs={
 "BP_TLP_Vida":(unreal.StaticMeshActor,[("Recogido","bool"),("Inicio","vec")]),
 "BP_TLP_Charla":(unreal.TextRenderActor,[("TextoAntes","string"),("TextoDespues","string"),("Meta",META),("Radio","real")]),
 "BP_TLP_Final":(unreal.Actor,[("Plataforma",FUS),("Revelacion",META),("Mascota",A),("Destino",A),("Camara",A),("Toto",A),("Paco",A),
     ("PuntoRaton",A),("PuntoToto",A),("PuntoPaco",A),("Estado","int"),("T","real"),("Inicio","vec"),("Fin","bool")]),
 "BP_TLP_Pausa":(unreal.Actor,[("Pausado","bool"),("FinJuego","bool")]),
}
for name,(parent,vars_) in specs.items():
    bp=make_bp(name,parent)
    for v,t in vars_:
        try:
            ok=bel.add_member_variable(bp,v,T(t))
            bel.set_blueprint_variable_instance_editable(bp,v,True)
        except Exception as ex: ok=f"ERROR {ex}"
        log(name,v,ok)
    bel.compile_blueprint(bp); unreal.EditorAssetLibrary.save_loaded_asset(bp)
cdo=unreal.get_default_object(cls(f"{BPDIR}/BP_TLP_Charla"))
try: cdo.set_editor_property("Radio",700.0)
except Exception as ex: log("radio",ex)
path="/Game/TheLastPatch/Blockout/MI_Queso"
mq=unreal.load_asset(path) if unreal.EditorAssetLibrary.does_asset_exist(path) else at.create_asset("MI_Queso","/Game/TheLastPatch/Blockout",unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
mel.set_material_instance_parent(mq,unreal.load_asset("/Game/TheLastPatch/Blockout/M_Blockout"))
mel.set_material_instance_vector_parameter_value(mq,"Color",unreal.LinearColor(1.0,0.78,0.12,1.0))
mel.set_material_instance_scalar_parameter_value(mq,"Roughness",0.5)
mel.update_material_instance(mq); unreal.EditorAssetLibrary.save_loaded_asset(mq)
log("MI_Queso ok")
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_fin1.txt"),"w").write("\n".join(LOG))
