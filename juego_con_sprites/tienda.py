class Tienda:
    """
    Clase que gestiona una tienda donde el jugador puede comprar/vender equipamiento.
    
    Atributos:
        dinero (int): Dinero disponible en la tienda
        inventario (list): Items disponibles para vender
    """
    def __init__(self):
        """Inicializa una tienda con items por defecto."""
        self.dinero = 1000
        self.inventario = [
            {"nombre": "Espada +1", "costo": 50, "tipo": "arma", "danio": 15},
            {"nombre": "Escudo", "costo": 40, "tipo": "defensa", "defensa": 3},
            {"nombre": "Pocima de Vida", "costo": 20, "tipo": "consumible", "vida": 30},
            {"nombre": "Armadura", "costo": 80, "tipo": "defensa", "defensa": 5},
        ]
    
    def obtener_items(self):
        """
        Retorna los items disponibles en la tienda.
        
        Returns:
            list: Lista de items disponibles
        """
        return self.inventario
    
    def comprar(self, item_nombre, jugador):
        """
        El jugador compra un item de la tienda.
        
        Args:
            item_nombre (str): Nombre del item a comprar
            jugador (Jugador): El jugador que compra
            
        Returns:
            bool: True si la compra fue exitosa
        """
        for item in self.inventario:
            if item["nombre"] == item_nombre:
                if jugador.dinero >= item["costo"]:
                    jugador.dinero -= item["costo"]
                    self.dinero += item["costo"]
                    jugador.inventario.agregar(item)
                    print(f"¡Compra exitosa! {item_nombre}")
                    return True
                else:
                    print("¡No tienes dinero suficiente!")
                    return False
        
        print("Item no encontrado en la tienda")
        return False
    
    def vender(self, item, jugador):
        """
        El jugador vende un item a la tienda.
        
        Args:
            item (dict): Item a vender
            jugador (Jugador): El jugador que vende
            
        Returns:
            bool: True si la venta fue exitosa
        """
        if jugador.inventario.remover(item):
            precio_venta = item.get("costo", 10) // 2
            jugador.dinero += precio_venta
            self.dinero -= precio_venta
            print(f"¡Venta exitosa! Ganaste {precio_venta} monedas")
            return True
        return False
    
    def info(self):
        """Retorna información de la tienda."""
        return {
            "dinero": self.dinero,
            "items_disponibles": len(self.inventario)
        }
