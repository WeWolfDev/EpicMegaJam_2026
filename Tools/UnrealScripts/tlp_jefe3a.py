# Variables nuevas del jefe + BPs de bandera y NPC animado
import unreal, os
LOG=[]
bel=unreal.BlueprintEditorLibrary; at=unreal.AssetToolsHelpers.get_asset_tools()
BPD="/Game/TheLastPatch/Blueprints"
def make(name,parent):
    p=f"{BPD}/{name}"
    if unreal.EditorAssetLibrary.does_asset_exist(p): return unreal.load_asset(p)
    f=unreal.BlueprintFactory(); f.set_editor_property("parent_class",parent); return at.create_asset(name,BPD,unreal.Blueprint,f)
def C(n): return unreal.load_asset(n).generated_class()
META=C(f"{BPD}/BP_TLP_Meta")
def T(k):
    if k=="vec": return bel.get_struct_type(unreal.Vector.static_struct())
    if isinstance(k,str): return bel.get_basic_type_by_name(k)
    return bel.get_object_reference_type(k)
A=unreal.Actor
specs={
 "BP_TLP_Jefe":(unreal.TextRenderActor,[("BaseA","vec"),("BaseB","vec"),("S","real"),("Puerta",A),("MetaP3",META),("PuertaAbierta","vec"),("PuertaCerrada","vec")]),
 "BP_TLP_Bandera":(unreal.StaticMeshActor,[("MallaVerde",unreal.StaticMesh),("Pasado","bool"),("Radio","real")]),
 "BP_TLP_NPCAnim":(unreal.Actor,[("Personaje",unreal.SkeletalMeshActor),("Meta",META),("AnimAntes",unreal.AnimationAsset),("AnimLiberado",unreal.AnimationAsset),("AnimDespues",unreal.AnimationAsset),("Liberado","bool"),("Despues","bool"),("T","real")]),
}
for name,(parent,vs) in specs.items():
    bp=make(name,parent)
    for v,t in vs:
        try:
            ok=bel.add_member_variable(bp,v,T(t)); bel.set_blueprint_variable_instance_editable(bp,v,True)
        except Exception as ex: ok=f"ERROR {ex}"
        LOG.append(f"{name}.{v} {ok}")
    bel.compile_blueprint(bp); unreal.EditorAssetLibrary.save_loaded_asset(bp)
cdo=unreal.get_default_object(C(f"{BPD}/BP_TLP_Bandera")); cdo.set_editor_property("Radio",300.0)
unreal.EditorAssetLibrary.save_asset(f"{BPD}/BP_TLP_Bandera")
open(r"C:/Proyectos/EpicMegaJam_2026/Saved/tlp_jefe3a.txt","w").write("\n".join(LOG))
