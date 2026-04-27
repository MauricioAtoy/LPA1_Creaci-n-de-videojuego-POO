import pygame

class TrampaExplosiva:
    """
    Clase que representa una trampa explosiva colocada en el mapa.
    
    Atributos:
        x (int): Posición X
        y (int): Posición Y
        alcance (int): Radio de explosión en píxeles
        danio (int): Daño que causa la explosión
        activa (bool): Si la trampa está activa
        tiempo (int): Contador de tiempo antes de explotar automáticamente
    """
    def __init__(self, x, y, alcance, danio):
        """
        Inicializa una trampa explosiva.
        
        Args:
            x (int): Posición inicial X
            y (int): Posición inicial Y
            alcance (int): Radio de explosión
            danio (int): Daño de la explosión
        """
        self.x = x
        self.y = y
        self.alcance = alcance
        self.danio = danio
        self.activa = True
        self.tiempo = 30  # 0.5 segundos a 60 FPS

    def dibujar(self, pantalla):
        """Dibuja la trampa en pantalla."""
        if self.activa:
            color = (255, 200, 0)  # Amarillo para trampa activa
            # Parpadeante si está a punto de explotar
            if self.tiempo < 10:
                if self.tiempo % 2 == 0:
                    color = (255, 100, 0)
        else:
            color = (100, 100, 100)  # Gris para trampa desactivada
        
        # Dibujar la trampa como un cuadrado
        rect = pygame.Rect(self.x - 10, self.y - 10, 30, 30)
        pygame.draw.rect(pantalla, color, rect)
        pygame.draw.rect(pantalla, (200, 150, 0), rect, 2)  # Borde
        
        # Dibujar "X" indicador
        pygame.draw.line(pantalla, (0, 0, 0), (self.x - 5, self.y - 5), (self.x + 5, self.y + 5), 2)
        pygame.draw.line(pantalla, (0, 0, 0), (self.x + 5, self.y - 5), (self.x - 5, self.y + 5), 2)

    def explotar(self, enemigo):
        """
        Explota la trampa si el enemigo está en rango.
        
        Args:
            enemigo (Enemigo): El enemigo a verificar
        """
        if not self.activa or enemigo is None:
            return

        # Calcular distancia entre trampa y enemigo
        distancia = ((self.x - enemigo.x)**2 + (self.y - enemigo.y)**2) ** 0.5

        # Si está en rango, causar daño
        if distancia <= self.alcance:
            enemigo.recibir_danio(self.danio)
            print("¡Trampa explotó!")

        self.activa = False