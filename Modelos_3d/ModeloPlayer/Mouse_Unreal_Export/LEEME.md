# Ratón explorador — exportación para Unreal

Generado a partir de los dos modelos de Meshy (personaje y personaje con caña). Todos los archivos comparten unidades (cm), ejes (Z arriba, personaje mirando a +X) y escala 1.

## Archivos

| Archivo | Contenido |
|---|---|
| `SK_Mouse.fbx` | Personaje en pose de referencia (A-pose) con esqueleto, pesos y material. 42162 triángulos, 50 huesos, máx. 4 influencias por vértice. |
| `Animations/A_Mouse_*.fbx` | 14 clips. Cada uno incluye la misma malla, esqueleto, jerarquía, pose de referencia y pesos que `SK_Mouse.fbx`. |
| `SM_FishingRod.fbx` | Caña como objeto separado, sin línea ni anzuelo. Origen en la empuñadura. Incluye `SOCKET_LineTip` en la punta. |
| `SM_FishingHook.fbx` | Flotador con anzuelo, separado. Origen en el punto donde se ata la línea; cuelga hacia −Z. |
| `Textures/` | Color base, normal, metálico y rugosidad del personaje (`T_Mouse_*`) y de la caña (`T_FishingRod_*`). |
| `Preview_Animaciones.mp4` | Vista previa de todos los clips desde cámara de tercera persona y de perfil; los bucles se repiten 5 veces. |

## Clips

| Clip | Frames | Duración | FPS | Bucle | Velocidad recomendada | Notas |
|---|---|---|---|---|---|---|
| `A_Mouse_Idle.fbx` | 120 | 4.00 s | 30 | Sí | — | Reposo sin caña. |
| `A_Mouse_Idle_Rod.fbx` | 120 | 4.00 s | 30 | Sí | — | Reposo con caña: mano delante de la cintura, codo algo flexionado. |
| `A_Mouse_Walk_Rod.fbx` | 18 | 0.60 s | 30 | Sí | 72 cm/s | Caminar in-place con caña. |
| `A_Mouse_Run_Rod.fbx` | 12 | 0.40 s | 30 | Sí | 224 cm/s | Correr in-place con caña. |
| `A_Mouse_Jump_Start_Rod.fbx` | 12 | 0.40 s | 30 | No | — | Preparación y despegue. Aplicar el impulso del salto en el frame 9. |
| `A_Mouse_Jump_Fall_Rod.fbx` | 16 | 0.53 s | 30 | Sí | — | Caída / en el aire. |
| `A_Mouse_Jump_Land_Rod.fbx` | 18 | 0.60 s | 30 | No | — | Aterrizaje y vuelta al reposo con caña. Impacto en el frame 5. |
| `A_Mouse_Aim_Enter.fbx` | 10 | 0.33 s | 30 | No | — | Del reposo con caña a la postura de apuntado. |
| `A_Mouse_Cast_Charge.fbx` | 14 | 0.47 s | 30 | No | — | Del apuntado a la carga completa. |
| `A_Mouse_Cast_ChargeHold.fbx` | 40 | 1.33 s | 30 | Sí | — | Carga mantenida mientras se sostiene el clic. |
| `A_Mouse_Cast_Throw.fbx` | 12 | 0.40 s | 30 | No | — | Lanzamiento desde la pose de carga. **Liberar el anzuelo en el frame 6 (0,20 s).** |
| `A_Mouse_Cast_Recover.fbx` | 20 | 0.67 s | 30 | No | — | Del final del lanzamiento al reposo con caña. |
| `A_Mouse_Wave.fbx` | 58 | 1.93 s | 30 | No | — | Saludo con la mano izquierda, sin caña. |
| `A_Mouse_Death.fbx` | 32 | 1.07 s | 30 | No | — | Muerte: tropieza, cae de espaldas y queda tumbado. Sin bucle: mantener el último frame. Impacto en el frame 15. |

- En los bucles, el último frame es idéntico al primero.
- Ningún clip tiene root motion: `root` permanece en el origen y no hay escala animada. El desplazamiento lo aporta la cápsula.
- Velocidades: caminar 72 cm/s (zancada 43 cm, ciclo 0,60 s); correr 224 cm/s (zancada 89 cm, ciclo 0,40 s). Si cambias la velocidad en el juego, ajusta el play rate en la misma proporción.
- La muerte no tiene root motion: `root` se queda en el origen y el cuerpo acaba tumbado hacia atrás, entre X = −117 y X = +35 cm. Desactiva la colisión de la cápsula al morir si estorba.
- En la muerte la caña sigue en la mano y queda apoyada en el suelo a la derecha; si prefieres que caiga suelta, desacóplala del socket al empezar el clip.
- Los clips de salto llevan la caña en la mano; el saludo usa la mano izquierda para poder combinarse con la caña.

## Personaje y esqueleto

- Altura: 150 cm incluyendo la pluma del sombrero. Suelas en Z = 0.
- Raíz única `root` en el suelo, `pelvis` separada.
- Cadena: `spine_01`–`spine_03`, `neck_01`, `head`, `clavicle_*`, `upperarm_*`, `lowerarm_*`, `hand_*`, `thigh_*`, `calf_*`, `foot_*`, `ball_*` (dedos del pie).
- Extras: `tail_01`–`tail_04`, `ear_l`, `ear_r`, dedos de la mano (`thumb`, `index`, `middle`, `ring`, `pinky`, `_01`/`_02`).
- `FishingGrip`: hueso hijo de `hand_r` en el centro de la palma, en (4, −28.5, 50) cm en pose de referencia, sin rotación respecto al mundo.

## Caña

- Acopla `SM_FishingRod` al hueso `FishingGrip` (o a un socket creado sobre él) con transformación relativa cero y escala 1.
- Longitud total 108 cm: 17 cm por detrás de la empuñadura y 91 cm por delante.
- `SOCKET_LineTip` está en (90.6, 7.5, 6.9) cm respecto al origen de la caña: úsalo como origen de la línea.

## Importación en Unreal

1. Importa `SK_Mouse.fbx` como Skeletal Mesh con escala 1 y sin "Force Front XAxis". Los archivos ya están en cm y con Z arriba.
2. Importa los clips de `Animations/` eligiendo el esqueleto de `SK_Mouse` y desmarcando "Import Mesh".
3. Marca como bucle: Idle, Idle_Rod, Walk_Rod, Run_Rod, Jump_Fall_Rod y Cast_ChargeHold.
4. Importa `SM_FishingRod.fbx` y `SM_FishingHook.fbx` como Static Mesh.
5. Comprueba que el personaje mida 150 unidades de alto y mire a +X.

## Validación realizada

Comprobado reimportando cada FBX en Blender y midiendo la malla deformada en cada frame:

- Mismos huesos, jerarquía, pose de referencia y malla en los 15 archivos del personaje.
- Mismas unidades y ejes en los 17 FBX.
- Escala de huesos constante (desviación máxima 0,00002) y `root` inmóvil en todos los clips.
- Pelvis sin desplazamiento horizontal acumulado en caminar y correr.

| Clip | Punto más bajo de las suelas | Holgura mínima caña–cuerpo | Pies |
|---|---|---|---|
| `A_Mouse_Idle` | -0.21 cm | — | desplazamiento máximo de las suelas 0.12 cm |
| `A_Mouse_Idle_Rod` | -0.21 cm | 6.4 cm | desplazamiento máximo de las suelas 0.12 cm |
| `A_Mouse_Walk_Rod` | -0.87 cm | 4.3 cm | deslizamiento medio en apoyo 0.20 cm/frame (máx. 0.61) sobre 2.41 cm/frame |
| `A_Mouse_Run_Rod` | -0.89 cm | 3.9 cm | deslizamiento medio en apoyo 0.27 cm/frame (máx. 0.86) sobre 7.46 cm/frame |
| `A_Mouse_Jump_Start_Rod` | -0.42 cm | 3.4 cm |  |
| `A_Mouse_Jump_Fall_Rod` | 0.96 cm | 7.0 cm |  |
| `A_Mouse_Jump_Land_Rod` | -0.43 cm | 2.9 cm |  |
| `A_Mouse_Aim_Enter` | -0.24 cm | 4.1 cm | desplazamiento máximo de las suelas 0.36 cm |
| `A_Mouse_Cast_Charge` | -0.26 cm | 3.7 cm | desplazamiento máximo de las suelas 0.14 cm |
| `A_Mouse_Cast_ChargeHold` | -0.27 cm | 5.5 cm | desplazamiento máximo de las suelas 0.06 cm |
| `A_Mouse_Cast_Throw` | -0.31 cm | 5.8 cm | desplazamiento máximo de las suelas 0.49 cm |
| `A_Mouse_Cast_Recover` | -0.30 cm | 4.1 cm | desplazamiento máximo de las suelas 0.59 cm |
| `A_Mouse_Wave` | -0.18 cm | — | desplazamiento máximo de las suelas 0.00 cm |
| `A_Mouse_Death` | −2,2 cm (cuerpo, en el impacto) | 6.3 cm | parte de pie y acaba tumbado; el cuerpo descansa a −1,6 cm en el último frame |

## Limitaciones

- **Topología:** la malla es una reducción automática de la malla de Meshy (de 1,17 M a 42162 triángulos), no una retopología manual con bucles en las articulaciones.
- **Dedos de las manos:** los puños vienen modelados como una pieza cerrada, así que los huesos de los dedos están en el esqueleto pero sin pesos. La caña se sujeta con el puño cerrado.
- **Bolso:** el puño derecho estaba fusionado con el bolso en el modelo original; se separó y queda una pequeña marca en la solapa.
- **Suelas:** en caminar y correr la puntera o el talón bajan hasta 0,9 cm por debajo del suelo durante el rodado del pie.
- **Deslizamiento:** en apoyo los pies siguen la velocidad recomendada con un error medio del 8 % al caminar y del 4 % al correr.
- **Lanzamiento:** se resolvió como lanzamiento lateral, porque el sombrero y las orejas no dejan pasar la caña por encima del hombro. La muñeca gira hasta 40° en la carga.
- **Unreal:** no se pudo abrir Unreal en este entorno. Escala, ejes y esqueleto están verificados en los FBX, pero la importación, las transiciones idle → caminar → correr → idle y el acople de la caña al socket quedan por comprobar en el motor.
