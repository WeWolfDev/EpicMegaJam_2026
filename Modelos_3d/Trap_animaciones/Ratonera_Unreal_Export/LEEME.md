# Ratonera araña — exportación para Unreal Engine 5

Malla reducida, rig, expresiones y cuatro animaciones en el sitio hechas a partir de `Meshy_AI_trampoculus_cheese_3d_…fbx`. Todo se verificó reimportando cada FBX en Blender. **No se probó en Unreal.**

## Contenido

| Archivo | Qué es |
|---|---|
| `SK_Ratonera.fbx` | Malla con esqueleto, material y 7 morph targets, en pose de referencia |
| `Animations/Trap_Idle.fbx` | Bucle, 90 frames (3,0 s) |
| `Animations/Trap_Walk.fbx` | Bucle, 24 frames (0,8 s) |
| `Animations/Trap_Attack_Snap.fbx` | Una vez, 24 frames (0,8 s) |
| `Animations/Trap_Dead.fbx` | Una vez, 54 frames (1,8 s); mantener el último frame |
| `Textures/T_Ratonera_BaseColor.png` | Color original (4096 px) |
| `Textures/T_Ratonera_Normal.png` | Normales horneadas desde la malla original (2048 px) |
| `Textures/T_Ratonera_AO.png` | Oclusión ambiental horneada (2048 px); no va dentro del FBX |
| `Textures/T_Ratonera_Metallic.png`, `T_Ratonera_Roughness.png` | Originales (2048 px) |
| `Preview_Ratonera.mp4` | Cada clip (bucles ×5) y la secuencia de transiciones |
| `Expresiones_MorphTargets.png` | Cada morph target al 100 % |

Todos los FBX comparten malla, esqueleto, jerarquía, pose de referencia, pesos, unidades (cm), ejes (Z arriba, frente a +X) y 30 fps. Cada clip trae las 7 curvas de morph con el nombre exacto del morph target.

## Qué traía el modelo

- Una sola malla fusionada de **679 860 triángulos** (339 876 vértices), un material y 4 texturas. Sin rig ni animaciones.
- Cuerpo, mandíbula, resorte, manija, ojos y patas estaban soldados en una pieza; no había partes separadas.
- **Solo 3 patas:** dos a la izquierda y una a la derecha, más el muñón de la cadera delantera derecha.
- La barra de mandíbula cuelga de un solo pasador lateral, no de dos.

## Cambios en la malla (acordados contigo)

- **Reducción:** de 679 860 a **14 837 triángulos** (7 815 vértices), contando 738 vértices de piezas auxiliares para las expresiones. Es una reducción automática, no una retopología manual.
- **Patas:** quité la pata derecha suelta y copié en espejo las dos izquierdas. Ahora tiene 4 patas simétricas. Las derechas comparten textura con las izquierdas.
- **Cortes:** separé mandíbula, manija, resorte y los tres globos oculares del cuerpo para que se muevan sin estirar la madera, y tapé los huecos de la mandíbula y la manija.
- **Escala:** 80 cm de alto con la manija, 98 cm de largo total (el cuerpo de madera mide unos 76 cm) y 108 cm de ancho con las patas.
- `root` está en el suelo, en (0, 0, 0), bajo el centro de las patas.

## Esqueleto (22 huesos)

- `root` → `body`
- Patas: `leg_fl_01` → `leg_fl_02` → `leg_fl_03` (cadera, rodilla, tobillo), y lo mismo para `fr`, `bl`, `br`.
- `jaw_bar`: bisagra bajo el frente del cuerpo; gira sobre el eje Y.
- `spring_01`, `spring_02`, `spring_03`: tres tramos del resorte, de derecha a izquierda.
- `handle`: pivote de la manija en los soportes del resorte.
- `eye_l`, `eye_c`, `eye_r`: centro de cada globo ocular.
- Máximo 2 influencias por vértice. Mandíbula, manija y ojos van al 100 % a su hueso.

Rangos que usé: mandíbula de +36° (abierta) a −22° (cerrada); manija de −14° a +128° (tumbada hacia delante); ojos hasta ±16°.

## Morph targets

`Blink`, `Eyes_Wide`, `Eyes_Angry`, `Eyes_Squint`, `Eyes_Dizzy`, `Pupil_Small`, `Pupil_Large`.

Los ojos son esferas rígidas con la pupila pintada, así que los morphs usan piezas pequeñas añadidas (párpados, pupilas, discos y cruces) que en reposo quedan ocultas dentro de cada ojo. `Eyes_Wide` no abre los aros: empuja los globos hacia fuera. `Eyes_Dizzy` muestra una cruz en cada ojo.

## Clips

| Clip | Frames | Duración | Bucle | Expresión | Extensión máxima desde `root` |
|---|---|---|---|---|---|
| `Trap_Idle` | 90 | 3,0 s | Sí | `Eyes_Squint` 0,35; un parpadeo en los frames 40–55; los tres ojos giran por separado | 58 cm |
| `Trap_Walk` | 24 | 0,8 s | Sí | `Eyes_Angry` 0,55; ojos fijos al frente | 63 cm |
| `Trap_Attack_Snap` | 24 | 0,8 s | No | `Eyes_Wide` (4–9) → `Eyes_Angry` y `Pupil_Small` (12–18) | 75 cm (hacia +X) |
| `Trap_Dead` | 54 | 1,8 s | No | `Eyes_Wide` y `Pupil_Small` (2–18) → `Eyes_Dizzy` (desde 24) | 66 cm durante la caída; 59 cm al final |

### Trap_Idle

- Agachada 5 cm, el cuerpo sube y baja 1 cm, la mandíbula se balancea entreabierta y el resorte vibra.
- Las cuatro patas quedan apoyadas todo el clip.

### Trap_Walk

- **Velocidad recomendada: 130 cm/s a play rate 1,0.**
- Rango de play rate estimado: 0,7 a 1,3 (91 a 169 cm/s). Es una estimación mía, no una prueba en Unreal.
- Trote en diagonal: delantera izquierda con trasera derecha, y al revés. Cada pata da 2 pasos por bucle, con zancada de 26 cm y levantamiento de 6,5 cm.
- El cuerpo oscila ±0,6 cm y su posición media es 0: no avanza dentro del clip.
- La mandíbula queda a 9 cm del suelo como mínimo.

### Trap_Attack_Snap

| Frame | Qué ocurre |
|---|---|
| 0–9 | Anticipación (0,3 s): se alza de delante, abre la mandíbula al máximo y echa atrás la manija |
| **9** | **Sin retorno:** empieza a lanzarse. Pon el aviso al jugador antes de este frame |
| **12** | **Impacto:** la mandíbula se cierra (0,4 s). Sonido, daño y pantalla de pérdida |
| 12–16 | La manija salta hacia delante y el resorte vibra |
| 16–24 | Vuelve atrás |
| 24 | Pose idéntica al frame 0 de `Trap_Idle` |

- El cuerpo se adelanta 16 cm y la mandíbula llega a 73 cm de `root` en +X. `root` no se mueve.
- El frame 0 también coincide exactamente con el frame 0 de `Trap_Idle`.

### Trap_Dead

| Frame | Qué ocurre |
|---|---|
| 1–4 | La trampa se dispara sola: la mandíbula se cierra y la manija se tumba hacia delante |
| **3** | **Desactiva la colisión de ataque** a partir de aquí |
| 3–14 | Salta hacia atrás agitando las patas; toca el suelo en el 14 |
| 19–30 | Vuelca sobre su costado |
| **30** | **Impacto contra el suelo** (sonido y polvo) |
| 30–42 | Rebote pequeño y asentamiento |
| 54 | Pose final |

- **Cae hacia atrás y sobre su lado derecho (−Y).** El cuerpo termina 13 cm atrás y 14 cm a la derecha de `root`.
- La pose final ocupa de X = −52 a 41 cm y de Y = −45 a 33 cm, con 77 cm de alto. Se apoya en las patas derechas encogidas y en el borde superior derecho del cuerpo, y no atraviesa el suelo.

## Importar en Unreal

1. Arrastra `SK_Ratonera.fbx` al Content Browser.
   - Skeletal Mesh: activado. Skeleton: ninguno (crea uno nuevo; renómbralo `SK_Ratonera_Skeleton`).
   - **Import Morph Targets: activado.**
   - Import Uniform Scale: 1,0. Convert Scene: activado. Force Front XAxis: desactivado.
   - Import Animations: desactivado en este archivo.
2. Importa las texturas de `Textures/` y conéctalas en el material `M_Ratonera`. Desactiva sRGB en Metallic, Roughness y AO; Normal como Normalmap. Conecta `T_Ratonera_AO` al pin Ambient Occlusion.
3. Arrastra los 4 FBX de `Animations/`.
   - Skeleton: `SK_Ratonera_Skeleton`. Import Animations: activado. Import Mesh: desactivado.
   - **Import Morph Target Curves** (o «Import Custom Attribute»): activado.
   - Import Uniform Scale: 1,0.
4. En `Trap_Idle` y `Trap_Walk` activa Loop. En todos, deja Root Motion desactivado.
5. Comprueba la escala: la ratonera debe medir 80 cm de alto junto al ratón de 150 cm.
6. Comprueba los morphs: abre la malla, pestaña Morph Target Previewer, y mueve cada deslizador. En cada animación, la pestaña Curves debe listar las 7 curvas.

## Animation Blueprint

Variables (las fija el Blueprint del actor): `Speed` (float, cm/s), `bAttack` (bool), `bDead` (bool).

- **Idle:** `Trap_Idle` en bucle.
- **Walk:** `Trap_Walk` en bucle, con **Play Rate = Speed / 130**, limitado entre 0,7 y 1,3.
- **Attack:** `Trap_Attack_Snap` sin bucle.
- **Dead:** `Trap_Dead` sin bucle; al terminar se queda en el último frame.

Transiciones:

- Idle → Walk si Speed > 10; Walk → Idle si Speed < 10. Mezcla de 0,15 s.
- Idle o Walk → Attack si `bAttack`. Mezcla de 0,05 s.
- Attack → Idle al terminar (regla automática por tiempo restante). Sin mezcla: la pose final es la del Idle.
- Cualquiera → Dead si `bDead`. Mezcla de 0,05–0,1 s. Sin salida.

Añade Anim Notifies en `Trap_Attack_Snap` (frames 9 y 12) y `Trap_Dead` (frames 3, 14 y 30) para los eventos de las tablas.

## Lo que no se cumple del prompt

- **Velocidad del walk:** sincroniza a 130 cm/s, no a 180 cm/s. Por encima de unos 169 cm/s las patas patinarán.
- **Parpadeo en el walk:** el bucle dura 0,8 s y no incluye parpadeo. Si lo quieres, anima la curva `Blink` desde el Animation Blueprint cada 3–5 s.
- **Radio de 60 cm en la muerte:** la pose final queda a 59 cm, pero durante el salto las patas llegan a 66 cm.
- **Idle → Walk:** el primer frame del walk no coincide con el Idle (las patas difieren hasta 14 cm); necesita la mezcla de 0,15 s.
- **Apoyo de las patas:** las puntas bajan hasta 0,3 cm bajo el suelo (0,5 cm en el ataque) y se deslizan hasta 0,7 cm durante el apoyo al caminar.
- **Ataque:** en el impacto, las patas traseras quedan estiradas al límite y les faltan 1–2 cm para alcanzar su punto de apoyo.
- **Muerte:** entre los frames 2 y 3 el cuerpo sube 10 cm de golpe (es el disparo). La estabilidad de la pose final es una estimación geométrica, no una simulación.
- **Ojos:** cada globo es un casquete con un anillo añadido por detrás. Con giros de más de unos 20° o con `Eyes_Wide` se ve una franja lisa del color del ojo junto al aro.
- **Mandíbula cerrada:** a −22° los dientes quedan delante de la parte baja de los ojos.
- **Resorte:** es un casquete abierto por debajo. Lo uso con giros de hasta 26° y 3 cm de compresión; con más, se vería el hueco.
- **Topología:** la malla reducida no tiene bucles de articulación. Las patas se doblan con mezclas de 2 huesos en cada unión.
- **Normales:** el mapa se horneó antes de copiar las patas en espejo; las patas derechas reutilizan el de las izquierdas.
- **Intersecciones:** las revisé solo visualmente. En la pose final de la muerte, las patas encogidas pueden cruzarse entre sí y con el borde del cuerpo.
- **Unreal:** no pude abrir Unreal. La importación, la escala, los morph targets y las mezclas del Animation Blueprint quedan por comprobar en el motor.
