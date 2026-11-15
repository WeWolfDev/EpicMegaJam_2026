# Menú principal — The Last Patch

El juego comienza en /Game/L_MainMenu. Para probar el menú desde el editor, abrir ese nivel y pulsar Play. L_Puerto sigue disponible para pruebas directas de jugabilidad.

Interfaz: /Game/TheLastPatch/MainMenu/WBP_MainMenu. Inicio: BP_MainMenuBoot; reglas sin personaje ni HUD de partida: BP_MainMenuMode.

Distribución: logo con la silueta del ratón arriba a la izquierda; botones START, SETTINGS y EXIT debajo; monograma TLP discreto arriba a la derecha; fondo obtenido de una captura aérea real del nivel completo, desplazado a la derecha. Sombras transparentes y sombreado lateral mejoran la lectura. Entrada con deslizamiento y opacidad, flotación leve del logo, zoom muy lento del fondo, escala suave al seleccionar y fundido al iniciar.

START carga /Game/L_Puerto y devuelve el control al personaje. SETTINGS ofrece volumen de música y calidad gráfica baja/media/alta con aplicación inmediata. BACK vuelve al menú. EXIT termina el juego; en el editor, termina la sesión de Play.

La música utiliza la pista existente, sin duplicarla, con la clase SC_TLP_Music y la mezcla SM_TLP_Music para el volumen. El volumen del menú se inicia en 80%; la calidad utiliza GameUserSettings y sus preferencias guardadas.

Arte original entregado: tres botones de madera. Arte generado con la herramienta de imágenes integrada: logo, monograma y plantilla vacía de botón para BACK y las opciones gráficas. PNG y especificaciones en SourceArt/MainMenu; prompts exactos en prompts.json. Se conserva el estilo de madera, metal oxidado, arpillera y tonos queso/olivo/rosa.

El fondo es una imagen del estado actual del puerto. Si cambia sustancialmente la geometría, actualizar T_Menu_Background desde una nueva captura. La ampliación del agua para capturar el fondo se revirtió antes de guardar L_Puerto.

Verificación: carga visible del menú, animaciones en ejecución, apertura/cierre de ajustes, volumen, selección de calidad, START con llegada a L_Puerto y presencia del ratón y los corazones, EXIT con cierre de Play. Copia previa del mapa, configuraciones y pista de música en work/main_menu/backup del chat. No se modificó la lógica de la caña, el personaje ni los puzles.
