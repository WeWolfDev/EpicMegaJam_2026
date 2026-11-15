import unreal, os
LOG=[]
bel=unreal.BlueprintEditorLibrary; at=unreal.AssetToolsHelpers.get_asset_tools(); mel=unreal.MaterialEditingLibrary
BPDIR="/Game/TheLastPatch/Blueprints"; name="BP_TLP_Enemigo"; path=f"{BPDIR}/{name}"
if unreal.EditorAssetLibrary.does_asset_exist(path): bp=unreal.load_asset(path)
else:
    f=unreal.BlueprintFactory(); f.set_editor_property("parent_class",unreal.StaticMeshActor); bp=at.create_asset(name,BPDIR,unreal.Blueprint,f)
def T(k): return bel.get_struct_type(unreal.Vector.static_struct()) if k=="vec" else bel.get_basic_type_by_name(k)
for v,t in (("Inicio","vec"),("Muerto","bool"),("Velocidad","real"),("RadioVision","real"),("RadioCasa","real")):
    try:
        ok=bel.add_member_variable(bp,v,T(t)); bel.set_blueprint_variable_instance_editable(bp,v,True)
    except Exception as ex: ok=f"ERROR {ex}"
    LOG.append(f"{v} {ok}")
bel.compile_blueprint(bp); unreal.EditorAssetLibrary.save_loaded_asset(bp)
parent=unreal.load_asset("/Game/TheLastPatch/Blockout/M_Blockout")
for n,c,r in (("MI_Enemigo",(0.75,0.05,0.85),0.35),("MI_Movil",(0.1,0.75,0.95),0.3)):
    p="/Game/TheLastPatch/Blockout/"+n
    mi=unreal.load_asset(p) if unreal.EditorAssetLibrary.does_asset_exist(p) else at.create_asset(n,"/Game/TheLastPatch/Blockout",unreal.MaterialInstanceConstant,unreal.MaterialInstanceConstantFactoryNew())
    mel.set_material_instance_parent(mi,parent); mel.set_material_instance_vector_parameter_value(mi,"Color",unreal.LinearColor(*c,1.0))
    mel.set_material_instance_scalar_parameter_value(mi,"Roughness",r); mel.update_material_instance(mi); unreal.EditorAssetLibrary.save_loaded_asset(mi); LOG.append(n)
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
ch=[a for a in eas.get_all_level_actors() if a.get_actor_label()=="TLP_Raton_Jugador"][0]
cm=ch.get_component_by_class(unreal.CharacterMovementComponent)
LOG.append("salto jz=%s gs=%s walk=%s air=%s" % tuple(cm.get_editor_property(k) for k in ("jump_z_velocity","gravity_scale","max_walk_speed","air_control")))
LOG.append("jumpmax=%s" % ch.get_editor_property("jump_max_count"))
for n in ("BO_Agua","BO_Trigger_Agua","BO_Limite_N","BO_Checkpoint_1","BO_Checkpoint_1_Marca"):
    a=[x for x in eas.get_all_level_actors() if x.get_actor_label()==n]
    LOG.append(f"{n} scale {a[0].get_actor_scale3d() if a else None}")
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_en1.txt"),"w").write("\n".join(str(x) for x in LOG))
