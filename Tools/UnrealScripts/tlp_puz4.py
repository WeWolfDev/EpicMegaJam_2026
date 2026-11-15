import unreal, os
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
out=[]
for a in eas.get_all_level_actors():
    l=a.get_actor_label()
    if l.startswith("TLP_Mover"):
        out.append(f"{l} vaiven={a.get_editor_property('Vaiven')} pieza={a.get_editor_property('Pieza').get_actor_label()} destino={a.get_editor_property('Destino').get_actor_label()}")
    if l=="BO_Ascensor_Plataforma":
        out.append(f"{l} mobility={a.root_component.mobility} parent={a.get_attach_parent_actor()}")
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_puz4.txt"),"w").write("\n".join(out))
