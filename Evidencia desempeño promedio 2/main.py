# Miguel Castro y Emiliana Diaz

import json
import hashlib
import matplotlib.pyplot as plt
from clases import *

# Controla el flujo de ejecución de la máquina expendedora. Inicia los componentes, carga las bases de datos en memoria y mantiene activo el bucle del menú.
def main():

    maquina = Catalogo()
    clientes = cargar_usuarios()
    admin_sistema = Administracion()
    control_ventas = Reporte()
    contador_ventas = 0

    while True:
        print("Maquina expendedora:")
        print("1. Mostrar catalogo")
        print("2. Comprar producto")
        print("3. Salir")
        opcion = input("Seleccione una opcion: ")

        # Opcion 1: Muestra el catalogo de productos disponible.
        if opcion == "1":
            maquina.DisplayCatalogo()

        # Opcion 2: Flujo integral de compra
        elif opcion == "2": 
            maquina.DisplayCatalogo()
            posicion = input("Ingrese la coordenada del producto: ").upper()
            
            if posicion in maquina.matriz:
                producto = maquina.matriz[posicion]

                if producto.CheckStock():
                    print(f"Producto seleccionado: {producto.nombre} - Precio: ${producto.precio}")
                    tarjeta_ingresada = input("Ingrese el numero de su tarjeta: ")

                    if tarjeta_ingresada in clientes:
                        usuario = clientes[tarjeta_ingresada]
                        contador_ventas += 1
                        nueva_venta = Venta(contador_ventas, producto.cod, producto.precio, usuario.hashTarjeta)

                        compra_exitosa = nueva_venta.procesar_pago(usuario, producto)
                        if compra_exitosa:
                            control_ventas.AgregarVenta(nueva_venta)
                            guardar_inventario(maquina)
                    else:
                        print("Error: Tarjeta no registrada o inválida.")

                else:
                    print("Error: Lo sentimos, este producto se encuentra agotado.")

            else:
                print("Error: Coordenada inválida. Revise el catálogo.")

        # Opcion 3: Apaga la maquina expendedora.
        elif opcion == "3":
            print("Apagando máquina... ¡Hasta luego!")
            break

        # Opcion RS: Menu tecnico de restock y administracion.
        elif opcion == "RS":
            print("Operacion de Restock:")
            print("1. Actualizar inventario")
            print("2. Cambiar o incluir producto nuevo")
            sub_opcion = input("Seleccione una opcion: ")

            # # Sub-opción 1: Recargar unidades de productos ya existentes.
            if sub_opcion == "1":
                maquina.DisplayCatalogo()
                pos = input("Ingrese la coordenada a recargar: ").upper()
                cant = input("Ingrese la cantidad de unidades a añadir: ")
                admin_sistema.recargar_catalogo(maquina, pos, cant)
                guardar_inventario(maquina)

            # Sub-opción 2: Reemplaza o registra un producto completamente diferente.
            elif sub_opcion == "2":
                maquina.DisplayCatalogo()
                pos = input("Ingrese la coordenada donde ubicar el producto: ").upper()
                cod = input("Ingrese el código del nuevo producto: ")
                nom = input("Ingrese el nombre del nuevo producto: ")
                pre = input("Ingrese el precio: ")
                stk = input("Ingrese el stock inicial: ")
                des = input("Ingrese el mensaje de despedida de la marca: ")

                nuevo_prod = Producto(pos, cod, nom, pre, stk, des)
                admin_sistema.cambiar_producto(maquina, pos, nuevo_prod)
                guardar_inventario(maquina)

        # Opcion RP: Calculos contables y genera las graficas PNGs.
        elif opcion == "RP":
            print("Generando reporte...")
            control_ventas.GenerarReporte()
            control_ventas.graficar_todo(maquina, clientes)

        else:
            print("Opción inválida. Intente de nuevo.")

# # Arranca el bloque de control del hilo principal del script de Python.
if __name__ == "__main__":
    main()