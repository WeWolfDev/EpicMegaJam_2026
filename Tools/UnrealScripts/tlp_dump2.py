import unreal, os
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
rows=[]
for a in eas.get_all_level_actors():
    v=a.get_actor_location(); o,e=a.get_actor_bounds(False)
    rows.append(f"{a.get_folder_path()}|{a.get_actor_label()}|{a.get_class().get_name()}|{v.x:.0f},{v.y:.0f},{v.z:.0f}|ext {e.x:.0f},{e.y:.0f},{e.z:.0f}|hid={a.get_editor_property('hidden')}|{','.join(str(t) for t in a.tags)}")
rows.sort()
w=unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
rows.insert(0,"MAPA "+w.get_path_name())
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_dump2.txt"),"w",encoding="utf-8").write("\n".join(rows))
