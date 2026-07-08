from gestor_archivos import GestorArchivos
from tarjeta import Tarjeta
from producto import Producto

class MaquinaExpendedora:
    def __init__(self):
        self.inventario = {} # dict de Productos
        self.tarjetas_validas = {} # dict de Tarjetas
        self.total_dinero_cobrado = 0.0
        self.total_productos_vendidos = 0
        self.gestor = GestorArchivos()

    def iniciar_maquina(self):
        pass

    def mostrar_catalogo(self):
        pass

    def procesar_venta(self, coordenada: str):
        pass

    def realizar_restock(self, coordenada: str):
        pass

    def generar_reporte(self):
        pass