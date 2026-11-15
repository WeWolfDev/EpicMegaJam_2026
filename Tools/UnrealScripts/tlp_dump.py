import unreal, os
eas = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
rows=[]
for a in eas.get_all_level_actors():
    v=a.get_actor_location(); b=a.get_actor_bounds(False)
    tags=",".join(str(t) for t in a.tags)
    rows.append(f"{a.get_folder_path()}|{a.get_actor_label()}|{a.get_class().get_name()}|{v.x:.0f},{v.y:.0f},{v.z:.0f}|ext {b[1].x:.0f},{b[1].y:.0f},{b[1].z:.0f}|hid={a.get_editor_property('hidden')}|{tags}")
rows.sort()
open(os.path.join(unreal.Paths.project_saved_dir(),"tlp_dump.txt"),"w",encoding="utf-8").write("\n".join(rows))
