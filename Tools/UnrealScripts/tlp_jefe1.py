# Crea BP_TLP_Foco y BP_TLP_Jefe con sus variables
import unreal, os
LOG=[]
bel=unreal.BlueprintEditorLibrary; at=unreal.AssetToolsHelpers.get_asset_tools()
BPD="/Game/TheLastPatch/Blueprints"
def make(name,parent):
    p=f"{BPD}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(p): return unreal.load_asset(p)
    f=unreal.BlueprintFactory(); f.set_editor_property("parent_class",parent); return at.create_asset(name,BPD,unreal.Blueprint,f)
def C(n): return unreal.load_asset(n).generated_class()
FUS=C("/Game/OneMoreCast/Fusion/BP_FusionObject"); META=C(f"{BPD}/BP_TLP_Meta"); FIN=C(f"{BPD}/BP_TLP_Final")
def T(k):
    if k=="vec": return bel.get_struct_type(unreal.Vector.static_struct())
    if isinstance(k,str): return bel.get_basic_type_by_name(k)
    return bel.get_object_reference_type(k)
A=unreal.Actor
specs={
 "BP_TLP_Foco":(unreal.StaticMeshActor,[("Activo","bool"),("Periodo","real"),("Desfase","real"),("Sombra",A),("Apuntado","bool"),("Golpeo","bool"),("Objetivo","vec"),("MinXY","vec"),("MaxXY","vec")]),
 "BP_TLP_Jefe":(unreal.TextRenderActor,[("Estado","int"),("Fase","int"),("Golpes","int"),("T","real"),("TL","real"),("Lado","bool"),("AnimIdle","bool"),("Inicio","vec"),("Linea","string"),
     ("Lobo",unreal.SkeletalMeshActor),("Barra",unreal.TextRenderActor),("Revelacion",META),("PlatA",FUS),("PlatB",FUS),("Palanca",FUS),
     ("FocoJefe",A),("PuntoA",A),("PuntoB",A),("PuntoPodio",A),("Expositor",A),("Final",FIN)]),
}
for name,(parent,vs) in specs.items():
    bp=make(name,parent)
    for v,t in vs:
        try:
            ok=bel.add_member_variable(bp,v,T(t)); bel.set_blueprint_variable_instance_editable(bp,v,True)
        except Exception as ex: ok=f"ERROR {ex}"
        LOG.append(f"{name}.{v} {ok}")
    bel.compile_blueprint(bp); unreal.EditorAssetLibrary.save_loaded_asset(bp)
cdo=unreal.get_default_object(C(f"{BPD}/BP_TLP_Foco")); cdo.set_editor_property("Periodo",3.2)
unreal.EditorAssetLibrary.save_asset(f"{BPD}/BP_TLP_Foco")
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_jefe1.txt"),"w").write("\n".join(LOG))
