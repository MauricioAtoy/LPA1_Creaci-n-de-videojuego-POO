class Arma:
    """
    Clase que representa un arma del juego.
    
    Atributos:
        nombre (str): Nombre del arma
        danio (int): Daño que causa el arma
        nivel (int): Nivel de mejora del arma
    """
    def __init__(self, nombre, danio):
        """
        Inicializa un arma.
        
        Args:
            nombre (str): Nombre del arma
            danio (int): Daño base del arma
        """
        self.nombre = nombre
        self.danio = danio
        self.nivel = 1

    def mejorar(self, jugador):
        """Mejora el arma, aumentando nivel y daño. Requiere 300 de oro.
        
        Args:
            jugador (Jugador): El jugador que mejora el arma
            
        Returns:
            bool: True si se mejoró, False si no hay suficiente dinero
        """
        costo = 300
        if jugador.dinero < costo:
            print(f"No tienes suficiente dinero. Necesitas {costo}, tienes {jugador.dinero}")
            return False
        
        jugador.dinero -= costo
        self.nivel += 1
        self.danio += 5
        print(f"¡Arma mejorada! Costo: {costo} de oro. Nuevo daño: {self.danio}")
        return True