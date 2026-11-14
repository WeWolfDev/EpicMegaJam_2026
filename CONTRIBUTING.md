# Guía para trabajar en el repo

## 1. Configuración inicial (una vez por computadora)

1. Instala Git para Windows (git-scm.com). Git LFS viene incluido.
2. Abre PowerShell o Git Bash y ejecuta:
   ```
   git lfs version
   git lfs install
   ```
3. Clona el repo en una ruta corta y fuera de OneDrive:
   ```
   git clone https://github.com/WeWolfDev/EpicMegaJam_2026.git C:\Proyectos\EpicMegaJam_2026
   ```
4. Usa la misma versión exacta de Unreal Engine que el resto del equipo.
5. (Recomendado) Instala el plugin de Git para Unreal de Project Borealis (UEGitPlugin) para ver y tomar locks desde el editor.

## 2. Ciclo de cada cambio

```
git pull
git lfs lock "Content/_Game/Ruta/Al/Asset.uasset"
# editar en Unreal y guardar
git add -A
git commit -m "Descripción clara del cambio"
git push
git lfs unlock "Content/_Game/Ruta/Al/Asset.uasset"
```

- Ver quién tiene bloqueado qué: `git lfs locks`
- Antes de editar un `.uasset` o `.umap`, revisa que nadie lo tenga bloqueado.
- **Nadie se va a dormir con archivos bloqueados.**

## 3. Reglas del equipo

- `main` siempre abre y siempre se puede jugar. No subas nada que rompa el proyecto.
- Commits pequeños y frecuentes. Haz `git pull` antes de empezar cualquier cosa.
- Cada asset tiene un dueño. Si necesitas tocar algo ajeno, pídelo en Discord (`#locks`).
- No muevas ni renombres carpetas o assets sin avisar. Si lo haces, ejecuta "Fix Up Redirectors" antes del commit.
- Tus pruebas van en `Content/Developers/<tu-nombre>/`.
- No subas Starter Content ni paquetes de Fab que no se vayan a usar: gastan la cuota de LFS.

## 4. Estructura de carpetas

```
Content/
  _Game/
    Core/  Characters/  Forms/  Levels/
    Props/  UI/  Audio/  VFX/  Materials/
  Developers/<nombre>/
```

Prefijos: `BP_` Blueprint, `WBP_` Widget, `AC_` Componente, `BPI_` Interfaz, `DA_` Data Asset, `SM_`/`SK_` Mesh, `T_` Textura, `M_`/`MI_` Material, `L_` Nivel.

## 5. Si algo sale mal

- **Los assets se ven como archivos de texto pequeños:** falta LFS. Ejecuta `git lfs install` y luego `git lfs pull`.
- **`git push` rechazado por lock:** alguien más tiene ese archivo. Pregunta en Discord.
- **Conflicto en un `.uasset`:** no se puede fusionar. Decide con tu compañero qué versión se queda (`git checkout --theirs` o `--ours`).
