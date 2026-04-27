import pygame
from entidad import Entidad
from arma import Arma
from inventario import Inventario

class Enemigo(Entidad):
    """
    Clase que representa un enemigo del juego.
    Soporta sprites desde el spritesheet de Kenney.
    """
    def __init__(self, x, y, tipo="terrestre", gestor_sprites=None):
        super().__init__(x, y, 50)
        self.tipo = tipo
        self.danio = 5

        if tipo == "volador":
            self.velocidad = 4
            self.defensa = 0
            self.sprite = gestor_sprites.enemigo_volador if gestor_sprites else None
        else:
            self.velocidad = 2
            self.defensa = 2
            self.sprite = gestor_sprites.enemigo_terrestre if gestor_sprites else None

    def dibujar(self, pantalla):
        """Dibuja el enemigo con sprite o fallback."""
        if self.sprite:
            pantalla.blit(self.sprite, self.rect.topleft)
        else:
            color = (255, 100, 100) if self.tipo == "volador" else (200, 0, 0)
            pygame.draw.rect(pantalla, color, self.rect)
        self.dibujar_barra_vida(pantalla)

    def mover_hacia(self, jugador, muros=None):
        """Mueve el enemigo hacia el jugador con colisiones."""
        if muros is None:
            muros = []

        v = self.velocidad

        # --- Mover en X y resolver colisiones ---
        x_anterior = self.x
        if self.x < jugador.x:
            self.x += v
        elif self.x > jugador.x:
            self.x -= v
        
        self.rect.x = self.x
        for muro in muros:
            if self.rect.colliderect(muro):
                self.x = x_anterior  # Revertir movimiento en X
                self.rect.x = self.x
                break

        # --- Mover en Y y resolver colisiones ---
        y_anterior = self.y
        if self.y < jugador.y:
            self.y += v
        elif self.y > jugador.y:
            self.y -= v
        
        self.rect.y = self.y
        for muro in muros:
            if self.rect.colliderect(muro):
                self.y = y_anterior  # Revertir movimiento en Y
                self.rect.y = self.y
                break
    def atacar(self, jugador):
        danio = self.danio - self.defensa if jugador.defendiendo else self.danio
        jugador.recibir_danio(danio)
