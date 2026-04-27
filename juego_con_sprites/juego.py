import pygame
import random
from jugador import Jugador
from enemigo import Enemigo
from trampa import TrampaExplosiva
from tienda import Tienda
from mapa import construir_mapa, zona_spawn_jugador, zonas_spawn_enemigo
from sprites import GestorSprites


class Juego:
    """
    Clase principal del juego.
    Ahora incluye:
      - Fondo tipo tilemap (pasto, muros, agua, árboles)
      - Colisiones del jugador con los muros del mapa
      - Sprites de personajes del pack de Kenney
    """

    ANCHO_PANTALLA = 800
    ALTO_PANTALLA  = 600

    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.estado   = "exploracion"
        self.pausado  = False

        # --- Cargar sprites ---
        try:
            self.sprites = GestorSprites("assets/roguelikeChar.png")
            print("Sprites cargados correctamente")
        except Exception as e:
            print(f"No se pudieron cargar los sprites: {e}")
            self.sprites = None

        # --- Construir mapa (prerender en Surface + lista de muros) ---
        self.superficie_mapa, self.muros = construir_mapa()
        print(f"Mapa construido: {len(self.muros)} muros/colisiones")

        # --- Entidades ---
        sx, sy = zona_spawn_jugador()
        self.jugador = Jugador(sx, sy, gestor_sprites=self.sprites)
        self.enemigo = None
        self.turno   = "jugador"
        self.defendiendo = False

        # --- Trampas ---
        self.trampas = []

        # --- Tienda ---
        self.tienda = Tienda()
        self.tienda_abierta = False
        self.opcion_tienda = 0

        # --- UI ---
        self.font = pygame.font.SysFont(None, 28)

    # ------------------------------------------------------------------ #
    # ACTUALIZACIÓN
    # ------------------------------------------------------------------ #

    def actualizar(self):
        if self.pausado:
            return
        if self.estado == "exploracion":
            self._actualizar_exploracion()
        elif self.estado == "combate":
            self._combate()

    def _actualizar_exploracion(self):
        # Mover jugador con colisiones
        self.jugador.mover(self.muros)

        # Chequear si enemigo murió (por trampa u otro)
        if self.enemigo and self.enemigo.vida <= 0:
            xp  = 30 + self.jugador.nivel * 10
            oro = 100
            self.jugador.ganar_xp(xp)
            self.jugador.dinero += oro
            print(f"¡Enemigo destruido! +{xp} XP, +{oro} oro")
            self.enemigo = None

        # Crear enemigo si no hay
        if self.enemigo is None:
            self._spawnear_enemigo()

        # Mover enemigo
        if self.enemigo:
            self.enemigo.mover_hacia(self.jugador, self.muros)
            if self.jugador.rect.colliderect(self.enemigo.rect):
                self.estado = "combate"

        # Trampas
        for trampa in self.trampas[:]:
            if trampa.activa:
                trampa.tiempo -= 1
                if trampa.tiempo <= 0:
                    trampa.explotar(self.enemigo)
            else:
                self.trampas.remove(trampa)

    def _spawnear_enemigo(self):
        """Elige una posición libre del mapa para spawnear el enemigo."""
        zonas = zonas_spawn_enemigo(muros=self.muros, excluir_rect=self.jugador.rect.inflate(120, 120))
        if not zonas:
            return
        px, py = random.choice(zonas)
        tipo = random.choice(["terrestre", "volador"])
        self.enemigo = Enemigo(px, py, tipo=tipo, gestor_sprites=self.sprites)
        vida  = 50 + self.jugador.nivel * 20
        danio = 5  + self.jugador.nivel * 2
        self.enemigo.vida     = vida
        self.enemigo.vida_max = vida
        self.enemigo.danio    = danio

    def _combate(self):
        if not self.enemigo or self.enemigo.vida <= 0:
            self._fin_combate_victoria()
            return
        if self.jugador.vida <= 0:
            self._fin_combate_derrota()
            return
        if self.turno == "enemigo":
            self._turno_enemigo()
            self.turno = "jugador"

    def _turno_enemigo(self):
        if self.defendiendo:
            danio = max(1, self.enemigo.danio - 2)
            self.jugador.recibir_danio(danio)
            self.defendiendo = False
        else:
            self.enemigo.atacar(self.jugador)

    def _fin_combate_victoria(self):
        xp  = 30 + self.jugador.nivel * 10
        oro = 100
        self.jugador.ganar_xp(xp)
        self.jugador.dinero += oro
        print(f"¡Victoria! +{xp} XP, +{oro} oro")
        self.enemigo = None
        self.estado  = "exploracion"

    def _fin_combate_derrota(self):
        print("¡Game Over!")
        self.estado = "game_over"

    # ------------------------------------------------------------------ #
    # EVENTOS
    # ------------------------------------------------------------------ #

    def manejar_eventos(self, evento):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_p:
                self.pausado = not self.pausado
                return
            # Permitir navegación de tienda aunque el juego esté pausado
            if self.tienda_abierta:
                self._manejar_eventos_tienda(evento)
                return
            if self.pausado:
                return
            if self.estado == "combate":
                self._manejar_eventos_combate(evento)
            elif self.estado == "exploracion":
                self._manejar_eventos_exploracion(evento)
            elif self.estado == "game_over":
                if evento.key == pygame.K_r:
                    self.__init__(self.pantalla)

    def _manejar_eventos_combate(self, evento):
        if self.turno != "jugador":
            return
        if evento.key == pygame.K_SPACE:
            self.jugador.atacar(self.enemigo)
            self.turno = "enemigo"
        elif evento.key == pygame.K_d:
            self.defendiendo = True
            self.turno = "enemigo"

    def _manejar_eventos_exploracion(self, evento):
        if evento.key == pygame.K_t:
            self.tienda_abierta = True
            self.pausado = True
            self.opcion_tienda = 0
        elif evento.key == pygame.K_e:
            trampa = TrampaExplosiva(self.jugador.x, self.jugador.y, alcance=100, danio=15)
            self.trampas.append(trampa)
        elif evento.key == pygame.K_u:
            if self.jugador.arma.mejorar(self.jugador):
                print(f"Arma mejorada: daño={self.jugador.arma.danio}")
    
    def _manejar_eventos_tienda(self, evento):
        items = self.tienda.obtener_items()
        if evento.key == pygame.K_UP:
            self.opcion_tienda = (self.opcion_tienda - 1) % len(items)
        elif evento.key == pygame.K_DOWN:
            self.opcion_tienda = (self.opcion_tienda + 1) % len(items)
        elif evento.key == pygame.K_RETURN:
            item = items[self.opcion_tienda]
            # Si es un arma, mejorar la que se tiene
            if item["tipo"] == "arma":
                costo = item["costo"]
                if self.jugador.dinero >= costo:
                    self.jugador.dinero -= costo
                    self.jugador.arma.nivel += 1
                    self.jugador.arma.danio += item["danio"] - 10  # Usar diferencia
                    print(f"¡{self.jugador.arma.nombre} mejorada! Nuevo daño: {self.jugador.arma.danio}")
                else:
                    print("No tienes suficiente dinero")
            else:
                # Otros items se agregan al inventario
                self.tienda.comprar(item["nombre"], self.jugador)
        elif evento.key == pygame.K_ESCAPE:
            self.tienda_abierta = False
            self.pausado = False

    # ------------------------------------------------------------------ #
    # DIBUJADO
    # ------------------------------------------------------------------ #

    def dibujar(self):
        # 1. Fondo del mapa (prerenderizado)
        self.pantalla.blit(self.superficie_mapa, (0, 0))

        # 2. Trampas
        for trampa in self.trampas:
            trampa.dibujar(self.pantalla)

        # 3. Entidades
        if self.enemigo:
            self.enemigo.dibujar(self.pantalla)
        self.jugador.dibujar(self.pantalla)

        # 4. HUD
        self._dibujar_ui()

        if self.estado == "game_over":
            self._dibujar_game_over()
        if self.pausado:
            self._dibujar_pausa()
        if self.tienda_abierta:
            self._dibujar_tienda()

    def _dibujar_ui(self):
        textos = [
            (f"Vida: {self.jugador.vida}/{self.jugador.vida_max}", (10, 10),  (255,  80,  80)),
            (f"Nivel: {self.jugador.nivel}",                       (10, 36),  (255, 255, 255)),
            (f"XP: {self.jugador.xp}/{self.jugador.xp_max}",       (10, 62),  (255, 255,   0)),
            (f"Arma: {self.jugador.arma.nombre} Nv{self.jugador.arma.nivel} | Daño: {self.jugador.arma.danio}",
                                                                   (10, 88),  (200, 200, 200)),
            (f"Dinero: {self.jugador.dinero}",                     (10, 114), (255, 215,   0)),
        ]
        for texto, pos, color in textos:
            surf = self.font.render(texto, True, color)
            # sombra para legibilidad sobre el mapa
            sombra = self.font.render(texto, True, (0, 0, 0))
            self.pantalla.blit(sombra, (pos[0]+1, pos[1]+1))
            self.pantalla.blit(surf, pos)

        # Estado
        color_estado = (255, 60, 60) if self.estado == "combate" else (60, 220, 60)
        s = self.font.render(f"Estado: {self.estado.upper()}", True, color_estado)
        self.pantalla.blit(s, (self.ANCHO_PANTALLA - 220, 10))

        # Controles
        if self.estado == "combate":
            turno_color = (255, 255, 0) if self.turno == "jugador" else (255, 100, 100)
            self.pantalla.blit(
                self.font.render(f"Turno: {self.turno.upper()}", True, turno_color),
                (self.ANCHO_PANTALLA - 220, 36)
            )
            self.pantalla.blit(
                self.font.render("SPACE: Atacar | D: Defender", True, (200, 200, 200)),
                (self.ANCHO_PANTALLA - 280, 62)
            )
        else:
            self.pantalla.blit(
                self.font.render("WASD: Mover | E: Trampa | T: Tienda | U: Mejorar | P: Pausa", True, (200, 200, 200)),
                (self.ANCHO_PANTALLA - 530, 10)
            )

    def _dibujar_game_over(self):
        overlay = pygame.Surface((self.ANCHO_PANTALLA, self.ALTO_PANTALLA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 170))
        self.pantalla.blit(overlay, (0, 0))

        f_grande = pygame.font.SysFont(None, 72)
        f_normal = pygame.font.SysFont(None, 36)
        cx = self.ANCHO_PANTALLA // 2

        self.pantalla.blit(f_grande.render("GAME OVER", True, (255, 60, 60)),
                           (cx - 190, self.ALTO_PANTALLA // 2 - 100))
        self.pantalla.blit(f_normal.render(f"Nivel: {self.jugador.nivel} | XP: {self.jugador.xp}", True, (255, 255, 255)),
                           (cx - 130, self.ALTO_PANTALLA // 2))
        self.pantalla.blit(f_normal.render("Presiona R para reiniciar", True, (200, 200, 200)),
                           (cx - 180, self.ALTO_PANTALLA // 2 + 50))

    def _dibujar_pausa(self):
        overlay = pygame.Surface((self.ANCHO_PANTALLA, self.ALTO_PANTALLA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 140))
        self.pantalla.blit(overlay, (0, 0))

        f_grande = pygame.font.SysFont(None, 72)
        f_normal = pygame.font.SysFont(None, 36)
        cx = self.ANCHO_PANTALLA // 2

        self.pantalla.blit(f_grande.render("PAUSA", True, (255, 255, 255)),
                           (cx - 100, self.ALTO_PANTALLA // 2 - 80))
        self.pantalla.blit(f_normal.render("Presiona P para continuar", True, (200, 200, 200)),
                           (cx - 160, self.ALTO_PANTALLA // 2))

    def _dibujar_tienda(self):
        overlay = pygame.Surface((self.ANCHO_PANTALLA, self.ALTO_PANTALLA), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.pantalla.blit(overlay, (0, 0))

        f_grande = pygame.font.SysFont(None, 48)
        f_normal = pygame.font.SysFont(None, 28)
        f_pequeña = pygame.font.SysFont(None, 20)

        cx = self.ANCHO_PANTALLA // 2
        cy = self.ALTO_PANTALLA // 2

        # Título
        self.pantalla.blit(f_grande.render("TIENDA", True, (255, 215, 0)),
                           (cx - 80, cy - 200))

        # Dinero del jugador
        self.pantalla.blit(f_normal.render(f"Tu dinero: {self.jugador.dinero}", True, (100, 255, 100)),
                           (cx - 100, cy - 150))

        # Arma actual
        arma_info = f"Arma actual: {self.jugador.arma.nombre} Nv{self.jugador.arma.nivel} | Daño: {self.jugador.arma.danio}"
        self.pantalla.blit(f_normal.render(arma_info, True, (255, 200, 100)),
                           (cx - 200, cy - 110))

        # Items disponibles
        items = self.tienda.obtener_items()
        for i, item in enumerate(items):
            color = (255, 255, 0) if i == self.opcion_tienda else (200, 200, 200)
            marca = "> " if i == self.opcion_tienda else "  "
            tipo_marca = " [ARMA]" if item["tipo"] == "arma" else ""
            texto = f"{marca}{item['nombre']}{tipo_marca} - {item['costo']} oro"
            self.pantalla.blit(f_normal.render(texto, True, color),
                               (cx - 150, cy - 50 + i * 40))

        # Controles
        self.pantalla.blit(f_pequeña.render("ARRIBA/ABAJO: Seleccionar | ENTER: Comprar | ESC: Cerrar", True, (200, 200, 200)),
                           (cx - 250, cy + 180))
