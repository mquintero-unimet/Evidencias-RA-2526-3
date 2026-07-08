# Autor: Alejandro Salas
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# Documentacion: Importar la libreria "string" me permite generar las coordenadas de los productos automaticamente para que el Catalogo se adapte a cualquier producto sin necesidad de modificarla.

import string

# Documentacion: Esta Clase es el Mecanismo Principal de la Maquina Expendedora que establece la Matriz Principal mediante el cual muestra el Catalogo y busca los Productos para que las otras Clases puedan ejercer sus funciones.

class Catalogo():

    def __init__(self, filas: int = 4, columnas: int = 4):
        self.filas = filas
        self.columnas = columnas
        self.matriz_de_productos = {}

    def Constructor_de_la_Matriz(self, lista_de_objetos: list): # Nota: Si genera fallos entonces quitar la especificacion "list".
        self.matriz_de_productos.clear()
        letras = string.ascii_uppercase
        idx = 0
        
        while len(lista_de_objetos) > self.filas * self.columnas:
            self.filas += 1

        for r in range(self.filas):
            for k in range(1, self.columnas + 1):
                if idx < len(lista_de_objetos):
                    prod = lista_de_objetos[idx]
                    coordenada_alterna = (f"{letras[r]}{k}")
                    prod.coordenada = coordenada_alterna
                    self.matriz_de_productos[coordenada_alterna] = prod
                    idx += 1

    def Mostrar_Catalogo(self):
        print("\n" + "=" * 50)
        print("          MÁQUINA EXPENDEDORA F-18F") # Nota: Es una referencia a un avion ;).
        print("=" * 50)

        for coordenada_alterna, prod in self.matriz_de_productos.items():
            if prod.stock > 0:
                print(f"[{coordenada_alterna}] {prod.codigo:<7} - {prod.nombre:<25} | ${prod.precio:.2f} | Stock: {prod.stock}")
            else:
                print(f"[{coordenada_alterna}] {prod.codigo:<7} - {prod.nombre:<25} | AGOTADO")
        print("=" * 50)

    def Buscar_Producto(self, serie):
        if serie.upper() in self.matriz_de_productos:
            return self.matriz_de_productos[serie.upper()]
        for prod in self.matriz_de_productos.values():
            if prod.codigo.lower() == serie.lower():
                return prod
        return None