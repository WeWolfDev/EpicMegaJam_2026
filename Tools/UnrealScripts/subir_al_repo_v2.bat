@echo off
setlocal
rem ==========================================================================
rem  The Last Patch - sube el proyecto a WeWolfDev/EpicMegaJam_2026
rem  en una rama nueva (main no se toca) y deja listo el Pull Request.
rem  Requisitos: Git para Windows (trae Git LFS) y permiso de escritura en el repo.
rem  Cierra Unreal antes de correrlo (todo debe estar guardado).
rem ==========================================================================

set "SRC=C:\Users\crod3\OneDrive\Documentos\Unreal Projects\The_Last_Patch"
set "DST=C:\Proyectos\EpicMegaJam_2026"
set "RAMA=nivel-puerto-crod3"
set "REPO=https://github.com/WeWolfDev/EpicMegaJam_2026.git"

where git >nul 2>nul || (echo [ERROR] No encuentro Git. Instala Git para Windows: https://git-scm.com & pause & exit /b 1)
git lfs version >nul 2>nul || (echo [ERROR] No encuentro Git LFS. Reinstala Git para Windows con LFS. & pause & exit /b 1)
git lfs install >nul

echo.
echo === 1. Clon limpio fuera de OneDrive: %DST%
if not exist "%DST%\.git" (
    git clone "%REPO%" "%DST%" || (echo [ERROR] No se pudo clonar. Revisa tu acceso al repo. & pause & exit /b 1)
)
cd /d "%DST%"
git config core.longpaths true
git fetch origin
git checkout main && git pull origin main
git lfs pull

echo.
echo === 2. Rama %RAMA%
git checkout -B %RAMA%

echo.
echo === 3. Revisando locks de LFS (si alguien tiene un archivo bloqueado, no lo pises)
git lfs locks

echo.
echo === 4. Copiando el proyecto
copy /Y "%SRC%\The_Last_Patch.uproject" "%DST%\" >nul
robocopy "%SRC%\Config" "%DST%\Config" /E /NFL /NDL /NJH /NJS /NP
for %%F in (TheLastPatch OneMoreCast Characters LevelPrototyping Input ThirdPerson) do (
    robocopy "%SRC%\Content\%%F" "%DST%\Content\%%F" /E /NFL /NDL /NJH /NJS /NP
)
copy /Y "%SRC%\Content\L_Puerto.umap" "%DST%\Content\" >nul
robocopy "%SRC%\Scripts" "%DST%\Tools\UnrealScripts" /E /NFL /NDL /NJH /NJS /NP

echo.
echo === 5. Commit y push
git add -A
git status --short | find /c /v ""
git commit -m "Nivel L_Puerto completo: puzzles, Toto y Paco, final, pausa, enemigos y tramos de plataformas" -m "Incluye el proyecto Unreal 5.8 (The_Last_Patch.uproject + Config), el nivel L_Puerto, los Blueprints de TheLastPatch (vidas con quesos, enemigos que persiguen y se aplastan, charlas, final y pausa), la mecanica OneMoreCast (cana con quitar poder) y las piezas de la plantilla Third Person que usa el nivel." -m "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>" -m "Claude-Session: https://claude.ai/code/session_01TkhZh7XwZTSwc2FBejcWBS"
git push -u origin %RAMA% || (echo [ERROR] El push fallo. Copia el mensaje de arriba y pasamelo. & pause & exit /b 1)

echo.
echo ==========================================================================
echo  Listo. Abre este enlace para crear el Pull Request hacia main:
echo  https://github.com/WeWolfDev/EpicMegaJam_2026/compare/main...%RAMA%?expand=1
echo ==========================================================================
start "" "https://github.com/WeWolfDev/EpicMegaJam_2026/compare/main...%RAMA%?expand=1"
pause
