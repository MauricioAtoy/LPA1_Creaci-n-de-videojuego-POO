class Inventario:
    """
    Clase que gestiona los items del jugador.
    
    Atributos:
        items (list): Lista de items en el inventario
        max_items (int): Número máximo de items que se pueden llevar
    """
    def __init__(self, max_items=10):
        """
        Inicializa un inventario vacío.
        
        Args:
            max_items (int): Capacidad máxima del inventario
        """
        self.items = []
        self.max_items = max_items
    
    def agregar(self, item):
        """
        Agrega un item al inventario si hay espacio.
        
        Args:
            item (dict): Item a agregar
            
        Returns:
            bool: True si se agregó, False si está lleno
        """
        if len(self.items) < self.max_items:
            self.items.append(item)
            print(f"Item agregado: {item.get('nombre', 'Desconocido')}")
            return True
        print("¡Inventario lleno!")
        return False
    
    def remover(self, item):
        """
        Remueve un item del inventario.
        
        Args:
            item (dict): Item a remover
            
        Returns:
            bool: True si se removió, False si no estaba
        """
        if item in self.items:
            self.items.remove(item)
            print(f"Item removido: {item.get('nombre', 'Desconocido')}")
            return True
        return False
    
    def usar(self, item):
        """
        Usa un item (consumible o equipo).
        
        Args:
            item (dict): Item a usar
            
        Returns:
            bool: True si se usó, False si no estaba
        """
        if item in self.items:
            self.remover(item)
            print(f"Item usado: {item.get('nombre', 'Desconocido')}")
            return True
        return False
    
    def listar(self):
        """
        Lista todos los items en el inventario.
        
        Returns:
            list: Lista de items
        """
        return self.items
    
    def contar_espacio(self):
        """
        Retorna el espacio disponible en el inventario.
        
        Returns:
            int: Espacio libre
        """
        return self.max_items - len(self.items)
