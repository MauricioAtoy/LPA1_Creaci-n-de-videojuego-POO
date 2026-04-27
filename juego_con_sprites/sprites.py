import pygame

# Constantes del spritesheet (roguelikeChar)
TILE_SIZE = 16
MARGIN = 1  # 1px entre tiles

# Índices de personajes en el spritesheet (col, fila)
SPRITE_JUGADOR = (0, 0)       # Personaje principal (torso)
SPRITE_ENEMIGO_T = (6, 0)     # Enemigo terrestre
SPRITE_ENEMIGO_V = (7, 0)     # Enemigo volador


def cargar_spritesheet(ruta):
    """Carga el spritesheet y devuelve la superficie."""
    sheet = pygame.image.load(ruta).convert_alpha()
    return sheet


def get_tile(sheet, col, fila, escala=40):
    """
    Extrae un tile del spritesheet y lo escala.
    
    Args:
        sheet: Surface del spritesheet
        col: Columna del tile (0-indexed)
        fila: Fila del tile (0-indexed)
        escala: Tamaño final en píxeles (el juego usa 40x40)
    
    Returns:
        pygame.Surface con el tile escalado
    """
    x = col * (TILE_SIZE + MARGIN)
    y = fila * (TILE_SIZE + MARGIN)
    tile = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    tile.blit(sheet, (0, 0), (x, y, TILE_SIZE, TILE_SIZE))
    return pygame.transform.scale(tile, (escala, escala))


class GestorSprites:
    """
    Gestiona la carga y acceso a todos los sprites del juego.
    Carga el spritesheet una sola vez y provee acceso a cada sprite.
    """
    
    def __init__(self, ruta_sheet="assets/roguelikeChar.png"):
        self.sheet = cargar_spritesheet(ruta_sheet)
        self.escala = 40  # mismo tamaño que el rect de las entidades
        
        # Cachear sprites usados frecuentemente
        self._cache = {}
    
    def obtener(self, col, fila):
        """Devuelve un sprite escalado, usando caché."""
        key = (col, fila)
        if key not in self._cache:
            self._cache[key] = get_tile(self.sheet, col, fila, self.escala)
        return self._cache[key]
    
    @property
    def jugador(self):
        return self.obtener(*SPRITE_JUGADOR)
    
    @property
    def enemigo_terrestre(self):
        return self.obtener(*SPRITE_ENEMIGO_T)
    
    @property
    def enemigo_volador(self):
        return self.obtener(*SPRITE_ENEMIGO_V)
