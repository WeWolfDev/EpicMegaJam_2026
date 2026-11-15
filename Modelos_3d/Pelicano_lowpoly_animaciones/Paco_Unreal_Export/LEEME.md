# Paco (pelícano) — exportación para Unreal

Generado a partir del modelo estático de `Pelicano_lowpoly_animaciones`. Todos los archivos comparten unidades (cm), ejes (Z arriba, personaje mirando a +X) y escala 1.

## Qué traía el archivo original

Una sola malla estática de 668 018 vértices y 1 336 552 triángulos, sin esqueleto, pesos, morph targets ni animaciones. Un material con color base y normales a 4096 px, y metálico y rugosidad a 2048 px. Medía 1,90 unidades de alto, centrada en el origen, con Z arriba y mirando a −Y, en A-pose simétrica.

## Archivos

| Archivo | Contenido |
|---|---|
| `SK_Paco.fbx` | Personaje en A-pose con esqueleto, pesos, material y 9 morph targets. 58442 triángulos, 37 huesos, máx. 4 influencias por vértice. |
| `Animations/A_Paco_*.fbx` | 7 archivos: 6 clips y la pose de referencia. Cada uno incluye la misma malla, esqueleto y pesos, y las 9 curvas de morph targets. |
| `Textures/` | `T_Paco_BaseColor`, `T_Paco_Normal`, `T_Paco_Metallic` y `T_Paco_Roughness`. El color base lleva una muestra de color oscuro añadida en una esquina libre, para el interior del pico. |
| `Preview_Paco.mp4` | Vista previa de los clips en el orden de la secuencia, con primer plano de la cara; los bucles se repiten 5 veces. |
| `Expresiones_MorphTargets.png` | Cada morph target al 100 %. |

## Clips

Todos a 30 fps. En los bucles, el último frame es idéntico al primero (huesos y morphs).

| Clip | Frames | Duración | Bucle | Expresión | Fotogramas clave |
|---|---|---|---|---|---|
| `A_Paco_RefPose` | 1 | — | — | Neutra | Pose de referencia |
| `A_Paco_Trapped_Idle` | 120 | 4,0 s | Sí | `Eyes_Wide` 0,45–1, `Eyes_Sad` 0,4–1, pico entreabierto llamando (`jaw`), buche inquieto, `Pouch_Slack` al asomarse | Agita las alas del 4 al 62; se asoma al hueco del 62 al 108; mira a los lados al principio y al final; parpadeo en el 110 |
| `A_Paco_Freed_Celebrate` | 75 | 2,5 s | No | `Eyes_Wide` 1 → `Eyes_Happy` 1 + `Pouch_Puff` 1 + `Beak_Smile` 1, pico abierto | Sorpresa en el 6; se mira el ala izquierda en el 19 y la derecha en el 27; se agacha en el 33; despega en el 38; punto más alto en el 43; aterriza en el 48 |
| `A_Paco_Idle` | 120 | 4,0 s | Sí | `Lid_Heavy` 0,55–0,8; parpadeos lentos en el 14 y el 104 | Se acomoda las plumas del ala izquierda del 34 al 90 |
| `A_Paco_Talk` | 60 | 2,0 s | Sí | `jaw` abre 3 veces por ciclo, `Eyes_Happy` 0,35–0,8, `Beak_Smile` 0,6, buche a ritmo | Gesticula con el ala derecha |
| `A_Paco_Wave` | 60 | 2,0 s | No | `Beak_Smile` 1, `Eyes_Happy` 0,8 | Ala derecha arriba en el 12; saluda del 12 al 46; vuelve al reposo en el 60 |
| `A_Paco_Point` | 60 | 2,0 s | No | `Lid_Heavy` 0,2, `Beak_Smile` 0,5–0,8, `Eyes_Happy` al mirar al jugador | **Punto máximo del señalamiento en el 18**; mira al jugador en el 32; baja el ala desde el 44 |

- **Dirección de `A_Paco_Point`:** señala con el ala derecha hacia (0,45, −0,88, 0,12), es decir, unos 63° a su derecha y ligeramente hacia arriba. Gira el actor en el nivel para que apunte al acceso. Para mantener el señalamiento, pausa el clip entre los frames 18 y 44.
- **`A_Paco_Sit_Idle`:** no está hecho. Tu tabla no lo lista y Paco no se sienta en tu descripción.
- El salto de la celebración despega y aterriza en el mismo punto; los pies están en el aire del frame 39 al 47 (hasta 11,5 cm).

## Esqueleto

- Raíz única `root` en el suelo y `pelvis` separada. Nombres del UE5 Mannequin: `spine_01`–`03`, `clavicle_*`, `upperarm_*`, `lowerarm_*`, `hand_*`, `thigh_*`, `calf_*`, `foot_*`, `ball_*`.
- Cuello: `neck_01`, `neck_02`, `neck_03` y `head`.
- Pico: `jaw` para la mandíbula inferior, y `pouch_01`–`pouch_03` para el buche.
- Alas: `hand_*` más `wing_feather_l_01`–`03` y `wing_feather_r_01`–`03`. No hay huesos de dedos porque las alas son cerradas.
- Cola: `tail_01` y `tail_02`, que mueven el faldón trasero del abrigo.

## Morph targets

`Blink`, `Eyes_Wide`, `Eyes_Squint`, `Eyes_Sad`, `Eyes_Happy`, `Lid_Heavy`, `Beak_Smile`, `Pouch_Puff`, `Pouch_Slack`.

- Los de ojos giran los párpados alrededor de cada globo ocular.
- El modelo ya trae los párpados a media altura, así que `Lid_Heavy` los baja un poco más y `Eyes_Wide` los sube.

## Importación en Unreal

1. Importa `SK_Paco.fbx` como Skeletal Mesh creando un Skeleton nuevo, con **Import Morph Targets** activado, Import Uniform Scale en 1 y sin "Force Front XAxis".
2. Importa los FBX de `Animations/` eligiendo ese Skeleton y desmarcando "Import Mesh". Las curvas de morph llegan con el mismo nombre que cada morph target y se reproducen solas.
3. Marca como bucle: Trapped_Idle, Idle y Talk.
4. Si las texturas no se asignan solas, conéctalas al material `M_Paco`: color base, normales, metálico y rugosidad.
5. Comprueba que mida 165 unidades de alto y mire a +X.

## Validación realizada

Comprobado reimportando cada FBX en Blender y midiendo la malla deformada en cada frame:

- Mismos 37 huesos, jerarquía, pose de referencia y malla en los 8 archivos; mismas unidades y ejes.
- Las 9 curvas de morph están en los 7 archivos de animación con el nombre exacto.
- Escala de huesos constante (desviación máxima 0,00001) y `root` inmóvil en todos los clips; el cuello se curva sin estirarse.
- Altura en pose de referencia: 165,0 cm.
- Pies: en Trapped_Idle, Idle, Talk, Wave y Point las suelas quedan entre −0,01 y 0,03 cm del suelo y se desplazan como máximo 0,03 cm. En Celebrate la puntera baja 0,6 cm bajo el suelo al despegar y al aterrizar.

| Clip | Radio máximo respecto a `root` | Extensión lateral (Y) | Altura máxima |
|---|---|---|---|
| RefPose | 55 cm | −54 a 54 cm | 165 cm |
| Trapped_Idle | 68 cm | −64 a 63 cm | 187 cm |
| Freed_Celebrate | 79 cm | −72 a 72 cm | 199 cm |
| Idle | 50 cm | −37 a 38 cm | 163 cm |
| Talk | 64 cm | −52 a 38 cm | 164 cm |
| Wave | 67 cm | −63 a 37 cm | 188 cm |
| Point | 91 cm | −91 a 37 cm | 164 cm |

## Limitaciones y cambios respecto a lo pedido

- **Radio de 60 cm:** solo Idle lo cumple. Las alas miden unos 84 cm desde el hombro, y la propia A-pose ya llega a 55 cm; Trapped_Idle, Talk y Wave lo superan por poco, y Celebrate y Point por más.
- **Topología:** la malla es una reducción automática (de 1 336 552 a 58442 triángulos) con más densidad en la cabeza y los ojos. No es una retopología manual.
- **Pico:** el original venía cerrado y fusionado. Lo abrí por la línea de la boca y uní los bordes con una membrana oscura, así que al abrir se ve un interior oscuro sin lengua ni paladar modelados. Lo usé hasta 20° de apertura.
- **`Eyes_Wide`:** bajo los párpados no hay globo ocular modelado, así que la apertura extra es moderada y deja una franja oscura bajo el párpado.
- **`Beak_Smile`:** el pico es rígido; el efecto es sutil.
- **Cola:** el modelo no tiene plumas de cola visibles; los huesos de cola mueven el faldón del abrigo.
- **Muñecas de las alas:** el antebrazo gira hasta unos 100° en algún frame de Celebrate y de Point; la mitad se reparte en el antebrazo y la otra mitad en la muñeca, bajo el puño de la manga.
- **Intersecciones:** las revisé solo visualmente; no medí cruces entre alas, abrigo, buche y pecho.
- **Unreal:** no pude abrir Unreal. La importación, los morph targets, la escala y las transiciones Trapped_Idle → Freed_Celebrate → Idle → Talk → Point → Idle quedan por comprobar en el motor.
