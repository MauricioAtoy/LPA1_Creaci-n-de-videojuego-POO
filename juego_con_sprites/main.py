"""
Videojuego 2D - Juego de Rol (RPG)

Un pequeño juego RPG desarrollado con Pygame.
El jugador controla un personaje que debe explorar, combatir enemigos,
y tratar de sobrevivir el mayor tiempo posible.

Controles:
    - WASD: Mover al jugador
    - SPACE: Atacar (en combate)
    - D: Defender (en combate)
    - E: Colocar trampa (en exploración)
    - R: Reiniciar (cuando pierdes)
"""

import pygame
from juego import Juego

# Inicializar Pygame
pygame.init()

# Constantes
ANCHO = 800
ALTO = 600
FPS = 60

# Crear pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Videojuego 2D - RPG POO")

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Crear instancia del juego
juego = Juego(pantalla)

# Loop principal del juego
ejecutando = True
while ejecutando:
    clock.tick(FPS)

    # Procesar eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        juego.manejar_eventos(evento)

    # Actualizar lógica del juego
    juego.actualizar()
    
    # Dibujar
    juego.dibujar()
    
    # Actualizar pantalla
    pygame.display.flip()

# Salir
pygame.quit()
print("Juego finalizado")
