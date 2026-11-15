# Cierra los extremos este y oeste del escenario del jefe
import unreal
eas=unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
V=unreal.Vector
for a in eas.get_all_level_actors():
    if a.get_actor_label().startswith("TLP3_Muro"): eas.destroy_actor(a)
L={a.get_actor_label():a for a in eas.get_all_level_actors()}
L["BO_Nueva mascota"].set_is_temporarily_hidden_in_editor(False)
ref=L["BO_Muro_N"]; mesh=ref.static_mesh_component.static_mesh; mat=ref.static_mesh_component.get_material(0)
def wall(n,x0,x1,y0,y1,z0,z1):
    a=eas.spawn_actor_from_class(unreal.StaticMeshActor,V((x0+x1)/2,(y0+y1)/2,(z0+z1)/2),unreal.Rotator(0,0,0))
    c=a.static_mesh_component; c.set_static_mesh(mesh); c.set_material(0,mat)
    # el cubo basico mide 100 con pivote al centro
    me=mesh.get_bounds().box_extent; a.set_actor_scale3d(V((x1-x0)/(2*me.x),(y1-y0)/(2*me.y),(z1-z0)/(2*me.z)))
    o,e=a.get_actor_bounds(False); l=a.get_actor_location()
    a.set_actor_location(V(l.x+((x0+x1)/2-o.x),l.y+((y0+y1)/2-o.y),l.z+((z0+z1)/2-o.z)),False,False)
    a.set_actor_label("TLP3_Muro_"+n); a.set_folder_path("TLP/Jefe")
wall("Oeste",6760,6800,-50,2050,0,650)
wall("Este_S",9400,9440,-50,785,0,650)
wall("Este_N",9400,9440,1215,2050,0,650)
wall("Este_Dintel",9400,9440,785,1215,420,650)
open(r'C:/Proyectos/EpicMegaJam_2026/Saved/tlp_jefe3c.txt','w').write(f"mesh={mesh.get_name()} ok")
