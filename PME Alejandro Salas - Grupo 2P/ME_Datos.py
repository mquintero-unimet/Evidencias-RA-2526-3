# Autor: Alejandro Salas
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# Documentacion: Nuevamente con ayuda de la IA instale "requests" para que pueda enlazar los datos del GITHUB con el Proyecto y a su vez definir los Datos para el Inventario Local. Adicionalmente me guie de ella para construir las Funciones Principales de la Central de Datos.

import json
import requests # Nota: "pip install requests" para manejar peticiones https.
import os

# Documentacion General: Esta es la Central de Datos del programa definidas en dos Clases importantes: ClientesAPI y Gestionador_de_Datos. Ambas permiten que el Sistema pueda obtener datos del GITHUB, suministrar la informacion necesaria para el Inventario Local y gestionar la Base de Datos del Sistema.
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# Documentacion: Mediante esta Clase se establece el enlace directo con el directorio de GITHUB.

class ClienteAPI():

    @staticmethod
    def Obtener_Datos(url):
        try:
            respuesta = requests.get(url, timeout = 10)
            respuesta.raise_for_status()
            return respuesta.json()
        except requests.exceptions.RequestException:
            return None

# Documentacion: Y por otro lado esta Clase trabaja directamente con la anterior para acceder a los Datos que nos suministra el directorio de GITHUB, obteniendo asi Datos Claves como los Productos y Tarjetas para que los respectivos Modulos puedan operar correctamente.
        
class Gestionador_de_Datos():

    def __init__(self):
        self.url_productos = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/main/productos.json"
        self.url_clientes = "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/main/clientes.json"
        self.inventario_local = "ME_Inventario_Local.json"

    def Iniciar_Nube(self):
        return ClienteAPI.Obtener_Datos(self.url_productos), ClienteAPI.Obtener_Datos(self.url_clientes)

    def Cargar_Inventario_Local(self):
        if not os.path.exists(self.inventario_local):
            return []
        try:
            with open(self.inventario_local, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def Guardar_Inventario_Local(self, lista_productos: list): # Nota: Si genera fallos entonces quitar la especificacion "list".
        try:
            with open(self.inventario_local, 'w', encoding ='utf-8') as f:
                json.dump(lista_productos, f, indent = 4, ensure_ascii = False)
        except Exception as x:
            print(f"[ERROR] No se pudo guardar Inventario Local: {x}")

# Nota: Esta ultima Clase a su vez tiene las Funciones necesarias para suministrar los Datos para el Inventario Local, por lo que trabaja a la par del Modulo_de_restock.