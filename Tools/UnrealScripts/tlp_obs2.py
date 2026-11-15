import unreal
bel = unreal.BlueprintEditorLibrary
bp = unreal.load_asset("/Game/TheLastPatch/Blueprints/BP_TLP_TablaFragil")
for v in ("ZonaOffset", "ZonaExtent"):
    bel.add_member_variable(bp, v, bel.get_struct_type(unreal.Vector.static_struct()))
    bel.set_blueprint_variable_instance_editable(bp, v, True)
bel.compile_blueprint(bp)
