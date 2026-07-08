# Autor: Alejandro Salas
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# Documentacion: Importamos todos los Modulos para el Cerebro del Sistema.

from ME_Modelos import Producto, Tarjeta
from ME_Reporte import Modulo_de_Reporte
from ME_Restock import Modulo_de_Restock
from ME_Venta import Modulo_de_Venta
from ME_Catalogo import Catalogo
from ME_Datos import Gestionador_de_Datos

# Documentacion: Esta Clase es practicamente el Cerebro del Sistema y se encarga de enlazar cada Modulo del Proyecto para operar de manera eficiente. Tambien lleva a cabo Funciones vitales como el Inicio, el Menu y la Salida del Programa.

class Maquina_Expendedora_F18F():

    def __init__(self):
        self.gestor = Gestionador_de_Datos()
        self.catalogo = Catalogo()
        self.venta = Modulo_de_Venta()
        self.restock = Modulo_de_Restock()
        self.reporte = Modulo_de_Reporte()
        
        self.lista_de_productos = []
        self.diccionario_de_tarjetas = {}

    def Iniciar_Sistema(self):
        print("[CENTRAL] Iniciando sistema...")
        Datos_API_prod, Datos_API_cli = self.gestor.Iniciar_Nube()
        Datos_Locales = self.gestor.Cargar_Inventario_Local()
        Lista_Principal = Datos_Locales if Datos_Locales else (Datos_API_prod if Datos_API_prod else [])

        for Item in Lista_Principal:
            precio = Item.get("precio", 0.0)
            if Datos_API_prod:
                for API_Item in Datos_API_prod:
                    if API_Item["cod"] == Item["cod"]:
                        precio = API_Item["precio"]
                        break
            
            Producto_Item = Producto(
                Item["cod"], Item["prod"], precio, 
                Item["despedida"], Item.get("stock", 0)
            )
            self.lista_de_productos.append(Producto_Item)
        
        self.catalogo.Constructor_de_la_Matriz(self.lista_de_productos)

        if Datos_API_cli:
            for cli in Datos_API_cli:
                self.diccionario_de_tarjetas[cli["id"]] = Tarjeta(cli["id"], cli["saldo"])

        self.Loop_Menu()

    def Loop_Menu(self):
        while True:
            self.catalogo.Mostrar_Catalogo()
            Inicio = input("\n[SOLICITUD] Por favor Ingrese el Codigo del Producto o su Coordenada, 'RESTOCK', 'REPORTE' o 'SALIR': ").strip()

            if Inicio.upper() == 'SALIR':
                self.Guardado_y_salida()
                break
            elif Inicio.upper() == 'RESTOCK':
                self.restock.Iniciar_Restock(self.catalogo)
            elif Inicio.upper() == 'REPORTE':
                self.reporte.Generar_Reporte(self.venta.historial_de_ventas, self.catalogo)
            else:
                Producto = self.catalogo.Buscar_Producto(Inicio)
                if Producto:
                    self.venta.Iniciar_Ventas(Producto, self.diccionario_de_tarjetas)
                else:
                    print("[ERROR] El Producto o la Coordenada Ingresada no existe")

    def Guardado_y_salida(self):
        Datos_a_guardar = []

        for prod in self.lista_de_productos:
            Datos_a_guardar.append({
                "cod": prod.codigo,
                "prod": prod.nombre,
                "precio": prod.precio,
                "despedida": prod.despedida,
                "stock": prod.stock
            })
        self.gestor.Guardar_Inventario_Local(Datos_a_guardar)
        print("[CENTRAL] Inventario Guardado... Apagando sistema...")

if __name__ == "__main__":
    Maquina = Maquina_Expendedora_F18F()
    Maquina.Iniciar_Sistema()

# Nota: El uso de "__name__ == '__main__'" es para asegurar que el bloque de codigo solo se ejecute cuando el archivo se ejecute directamente.
