# Autor: Alejandro Salas
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# Documentacion: Esta Clase sostiene el Inventario de la Maquina Expendedora mediante su unica Funcion que permite Añadir Productos.

class Modulo_de_Restock():
    
    def Iniciar_Restock(self, catalogo):
        print("\n=========== MENU DE RESTOCK ===========")
        coordenada = input("[SOLICITUD] Ingrese la Coordenada del Producto que desea Reponer [Ejemplo: B1]: ").upper()
        producto = catalogo.Buscar_Producto(coordenada)

        if not producto:
            print("[ERROR] La Coordenada ingresada no concuerda con las del Sistema.")
            return
        
        while True:
            try:
                cantidad = int(input(f"¿Cuantas unidades de '{producto.nombre}' desea Añadir?: "))
                if cantidad < 0:
                    print("[ERROR] Por favor ingrese un numero Positivo.")
                    continue
                producto.Actualizar_Stock(cantidad)
                print(f"[EXITO] Inventario Actualizado. Nuevo Stock de {producto.nombre}: {producto.stock}")
                break
            except ValueError:
                print("[ERROR] Debe ingresar un numero Entero valido.")

# Nota: Considero que la creacion de un Inventario Local es vital para evitar una dependencia total del GITHUB.