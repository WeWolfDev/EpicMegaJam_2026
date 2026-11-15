# Abre un Blueprint y deja su grafico (.t3d) en el portapapeles. Usar: BP='...'; F='...'; exec(...)
import unreal, subprocess, os
d = r'C:\Users\crod3\OneDrive\Documentos\Unreal Projects\The_Last_Patch\Scripts'
txt = open(os.path.join(d, F), encoding='utf-8').read()
subprocess.run('clip', input=txt.encode('ascii'), shell=True)
unreal.get_editor_subsystem(unreal.AssetEditorSubsystem).open_editor_for_assets([unreal.load_asset(BP)])
