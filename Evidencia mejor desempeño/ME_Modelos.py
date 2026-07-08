# Autor: Alejandro Salas
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# Documentacion: Esta Clase establece la Base del Producto y define dos Funciones claves para poder Modificar los Productos. Por un tema de nomenclatura con el Inventario JSON no modifique las Variables base como: "cod", "prod", "precio", "despedida", "stock".

class Producto():

    def __init__(self, cod, prod, precio: float, despedida: str, stock: int = 0):
        self.codigo = cod
        self.nombre = prod
        self.precio = precio
        self.despedida = despedida
        self.stock = stock
        self.coordenada = None

    def Actualizar_Precio(self, precio_actualizado: float):
        self.precio = precio_actualizado

    def Actualizar_Stock(self, cantidad: int):
        self.stock += cantidad

# Documentacion: Esta otra Clase establece el Metodo de Pago mediante una Funcion que permite realizar las 
# transacciones de los Clientes para que el dinero cobre sentido.

class Tarjeta():

    def __init__(self, id, fondos: float):
        self.id = id
        self.fondos = fondos
        self.gasto_total = 0.0

    def Descontar_Fondos(self, monto: float): # Nota: Si genera fallos entonces quitar la especificacion "float".
        if self.fondos >= monto:
            self.fondos -= monto
            self.gasto_total += monto
            return True
        return False
    
# Nota: En este Proyecto este Metodo de Pago lo defino como "Transaccion" para evitar malinterpretaciones en el 
# Modulo de Venta. Por ende es comun que en ves de definir id de la "Tarjeta" como "Numero de Tarjeta", lo hago como "Numero de Cuenta".