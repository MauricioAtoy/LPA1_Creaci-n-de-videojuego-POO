import pygame

# Tamaño de cada tile del mapa (en píxeles en pantalla)
TILE_PX = 40

# Colores estilo 1-bit (paleta oscura como el 1-Bit Pack de Kenney)
COLOR_PASTO    = (58,  90,  48)   # verde oscuro
COLOR_TIERRA   = (101, 67,  33)   # marrón
COLOR_PASTO2   = (70, 110,  55)   # verde claro (variación)
COLOR_MURO     = (60,  50,  40)   # marrón muy oscuro
COLOR_AGUA     = (30,  80, 120)   # azul oscuro
COLOR_CAMINO   = (120, 100,  70)  # beige oscuro
COLOR_ARBOL_T  = (20,  60,  20)   # verde muy oscuro (tronco/sombra)
COLOR_ARBOL_C  = (40, 120,  40)   # verde (copa)
COLOR_BORDE_M  = (40,  35,  30)   # borde de muro

# Tipos de tiles
T_PASTO  = 0   # caminar OK
T_MURO   = 1   # colisión - pared/edificio
T_AGUA   = 2   # colisión - agua
T_CAMINO = 3   # caminar OK
T_ARBOL  = 4   # colisión - árbol

# ¿Bloquea el paso?
COLISIONA = {
    T_PASTO:  False,
    T_MURO:   True,
    T_AGUA:   True,
    T_CAMINO: False,
    T_ARBOL:  True,
}

# Mapa 20x15 tiles (800x600 px con tiles de 40px)
# Leyenda: 0=pasto, 1=muro, 2=agua, 3=camino, 4=árbol
MAPA_DATA = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,4,0,0,0,0,3,3,3,3,0,0,0,4,0,0,0,1],
    [1,0,0,0,0,1,1,0,3,0,0,3,0,1,1,0,0,0,0,1],
    [1,4,0,0,0,1,1,0,3,0,0,3,0,1,1,0,0,4,0,1],
    [1,0,0,0,0,0,0,0,3,0,0,3,0,0,0,0,0,0,0,1],
    [1,0,2,2,0,0,0,0,3,3,3,3,0,0,0,0,2,2,0,1],
    [1,0,2,2,0,4,0,0,0,0,0,0,0,0,4,0,2,2,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,1],
    [1,4,0,0,1,1,0,3,0,0,0,0,3,0,1,1,0,0,4,1],
    [1,0,0,0,1,1,0,3,0,0,0,0,3,0,1,1,0,0,0,1],
    [1,0,0,0,0,0,0,3,0,0,0,0,3,0,0,0,0,0,0,1],
    [1,0,4,0,0,0,0,3,3,3,3,3,3,0,0,0,0,4,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]

FILAS  = len(MAPA_DATA)
COLS   = len(MAPA_DATA[0])
ANCHO  = COLS * TILE_PX   # 800
ALTO   = FILAS * TILE_PX  # 600


def _dibujar_arbol(surface, px, py):
    """Dibuja un árbol estilo pixel art en la posición dada."""
    # Tronco
    pygame.draw.rect(surface, COLOR_TIERRA,
                     (px + 16, py + 28, 8, 12))
    # Sombra de copa
    pygame.draw.circle(surface, COLOR_ARBOL_T,
                       (px + 20, py + 22), 14)
    # Copa
    pygame.draw.circle(surface, COLOR_ARBOL_C,
                       (px + 20, py + 20), 13)
    # Brillo
    pygame.draw.circle(surface, (60, 160, 60),
                       (px + 16, py + 14), 5)


def _dibujar_agua(surface, px, py):
    """Dibuja tile de agua con efecto."""
    pygame.draw.rect(surface, COLOR_AGUA, (px, py, TILE_PX, TILE_PX))
    # Ondas
    for oy in [10, 24]:
        pygame.draw.line(surface, (40, 100, 150),
                         (px+4, py+oy), (px+16, py+oy), 2)
        pygame.draw.line(surface, (40, 100, 150),
                         (px+20, py+oy), (px+32, py+oy), 2)


def construir_mapa(surface=None):
    """
    Renderiza el mapa en una Surface y devuelve la lista de rects de muros.
    
    Args:
        surface: Si se pasa, dibuja directamente en ella.
                 Si no, crea una Surface nueva (para prerender).
    
    Returns:
        (surface_mapa, lista_muros)
        lista_muros: lista de pygame.Rect con todos los tiles que colisionan
    """
    if surface is None:
        surface = pygame.Surface((ANCHO, ALTO))
    
    muros = []
    
    for fila, fila_data in enumerate(MAPA_DATA):
        for col, tipo in enumerate(fila_data):
            px = col * TILE_PX
            py = fila * TILE_PX
            rect = pygame.Rect(px, py, TILE_PX, TILE_PX)
            
            # Dibujar tile según tipo
            if tipo == T_PASTO:
                # Alternar dos tonos para dar textura
                color = COLOR_PASTO if (col + fila) % 2 == 0 else COLOR_PASTO2
                pygame.draw.rect(surface, color, rect)
                
            elif tipo == T_MURO:
                pygame.draw.rect(surface, COLOR_MURO, rect)
                pygame.draw.rect(surface, COLOR_BORDE_M, rect, 2)
                muros.append(rect.copy())
                
            elif tipo == T_AGUA:
                _dibujar_agua(surface, px, py)
                muros.append(rect.copy())
                
            elif tipo == T_CAMINO:
                pygame.draw.rect(surface, COLOR_CAMINO, rect)
                # Borde sutil
                pygame.draw.rect(surface, (100, 82, 55), rect, 1)
                
            elif tipo == T_ARBOL:
                # Fondo de pasto primero
                color = COLOR_PASTO if (col + fila) % 2 == 0 else COLOR_PASTO2
                pygame.draw.rect(surface, color, rect)
                _dibujar_arbol(surface, px, py)
                muros.append(rect.copy())
    
    return surface, muros


def zona_spawn_jugador():
    """Devuelve una posición segura de spawn para el jugador (en píxeles)."""
    return (TILE_PX * 1 + 4, TILE_PX * 1 + 4)  # esquina interior segura


def zonas_spawn_enemigo(muros=None, excluir_rect=None):
    """
    Devuelve lista de posiciones seguras para spawnear enemigos.
    Evita tiles con colisión, muros, la zona del jugador y los bordes.
    """
    if muros is None:
        muros = []
    
    posiciones = []
    enemigo_size = 40  # tamaño del rect del enemigo
    
    for fila, fila_data in enumerate(MAPA_DATA):
        for col, tipo in enumerate(fila_data):
            # Solo en tiles walkables (no colisionan)
            if not COLISIONA[tipo]:
                # Evitar bordes - aumentado para tener espacio seguro
                if fila <= 2 or fila >= FILAS - 3 or col <= 2 or col >= COLS - 3:
                    continue
                
                # Verificar también que tiles adyacentes no sean muros
                es_seguro = True
                for df in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        nf = fila + df
                        nc = col + dc
                        if 0 <= nf < FILAS and 0 <= nc < COLS:
                            if COLISIONA[MAPA_DATA[nf][nc]]:
                                es_seguro = False
                                break
                    if not es_seguro:
                        break
                
                if not es_seguro:
                    continue
                
                px = col * TILE_PX + TILE_PX // 2  # Centro del tile
                py = fila * TILE_PX + TILE_PX // 2
                
                # Crear rect del enemigo para verificar colisiones
                rect_enemigo = pygame.Rect(px - enemigo_size // 2, py - enemigo_size // 2, enemigo_size, enemigo_size)
                
                # Evitar muros (verificación adicional)
                colisiona_muro = False
                for muro in muros:
                    if rect_enemigo.colliderect(muro):
                        colisiona_muro = True
                        break
                if colisiona_muro:
                    continue
                
                # Evitar zona del jugador
                if excluir_rect:
                    if rect_enemigo.colliderect(excluir_rect):
                        continue
                
                posiciones.append((px, py))
    return posiciones
