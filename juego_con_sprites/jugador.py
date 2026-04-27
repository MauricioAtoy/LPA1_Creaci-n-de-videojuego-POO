import pygame
from entidad import Entidad
from arma import Arma
from inventario import Inventario


class Jugador(Entidad):
    """
    Clase que representa al jugador del juego.
    Ahora soporta sprites y colisión con muros del mapa.
    """
    def __init__(self, x, y, gestor_sprites=None):
        super().__init__(x, y, 100)
        self.velocidad = 4
        self.arma = Arma("Espada", 10)
        self.xp = 0
        self.xp_max = 100
        self.nivel = 1
        self.dinero = 100
        self.inventario = Inventario()
        
        # Sprite: se asigna desde GestorSprites al iniciar el juego
        self.sprite = gestor_sprites.jugador if gestor_sprites else None

    def mover(self, muros=None):
        """
        Mueve al jugador con WASD y resuelve colisiones contra muros.
        
        Args:
            muros: lista de pygame.Rect que bloquean el paso
        """
        if muros is None:
            muros = []
        
        teclas = pygame.key.get_pressed()
        dx = 0
        dy = 0

        if teclas[pygame.K_w]: dy -= self.velocidad
        if teclas[pygame.K_s]: dy += self.velocidad
        if teclas[pygame.K_a]: dx -= self.velocidad
        if teclas[pygame.K_d]: dx += self.velocidad

        # --- Mover en X y resolver colisiones ---
        self.rect.x += dx
        for muro in muros:
            if self.rect.colliderect(muro):
                if dx > 0:
                    self.rect.right = muro.left
                elif dx < 0:
                    self.rect.left = muro.right

        # --- Mover en Y y resolver colisiones ---
        self.rect.y += dy
        for muro in muros:
            if self.rect.colliderect(muro):
                if dy > 0:
                    self.rect.bottom = muro.top
                elif dy < 0:
                    self.rect.top = muro.bottom

        # Sincronizar x, y con el rect
        self.x = self.rect.x
        self.y = self.rect.y

    def atacar(self, enemigo):
        enemigo.recibir_danio(self.arma.danio)

    def dibujar(self, pantalla):
        """Dibuja el jugador con sprite o fallback de rectángulo."""
        if self.sprite:
            pantalla.blit(self.sprite, self.rect.topleft)
        else:
            pygame.draw.rect(pantalla, (0, 200, 0), self.rect)
        self.dibujar_barra_vida(pantalla)

    def ganar_xp(self, cantidad):
        self.xp += cantidad
        while self.xp >= self.xp_max:
            self.xp -= self.xp_max
            self.subir_nivel()

    def subir_nivel(self):
        self.nivel += 1
        self.xp_max += 50
        self.vida_max += 20
        self.vida = self.vida_max
        self.arma.danio += 2
        print(f"¡Subiste al nivel {self.nivel}!")
