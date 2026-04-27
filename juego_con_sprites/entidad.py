import pygame

class Entidad:
    """
    Clase base para todas las entidades del juego (Jugador, Enemigo, etc).
    """
    def __init__(self, x, y, vida):
        self.x = x
        self.y = y
        self.vida = vida
        self.vida_max = vida
        self.rect = pygame.Rect(x, y, 40, 40)
        self.vivo = True
        self.turno = "jugador"
        self.defendiendo = False

    def recibir_danio(self, cantidad):
        self.vida -= cantidad
        if self.vida <= 0:
            self.vivo = False

    def dibujar_barra_vida(self, pantalla):
        ancho = 40
        alto = 5
        porcentaje = max(0, self.vida / self.vida_max)
        pygame.draw.rect(pantalla, (255, 0, 0),   (self.x, self.y - 10, ancho, alto))
        pygame.draw.rect(pantalla, (0, 255, 0),   (self.x, self.y - 10, int(ancho * porcentaje), alto))
