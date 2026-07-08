#Jorge Kriger 32560571
#José Páez 32538298

import json
import requests

class maquina:
    def __init__(self):
        self.producto= {}
        self.tarjeta= {}
        self.dinero_ganado= 0.0
        self.ventas= 0

    def obtener(self):
        url= "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/productos.json"
        try:
            print("Conectando con la base de datos...")
            res = requests.get(url)
            if res.status_code == 200:
                datos = res.json()
                print("Datos cargados con exito \n")
                return datos
            else:
                print("no se pudo conectar")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión a la red: {e}")
            return None

    def cargar(self):
        try:
            with open("inventario.txt", "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split(",")
                    if len(partes) == 5:
                        coordenada, codigo, nombre, precio, stock = partes
                        self.producto[coordenada] = {
                            "codigo": codigo,
                            "nombre": nombre,
                            "precio": float(precio),
                            "stock": int(stock)
                        }
            print("Inventario local cargado con éxito.")
        except FileNotFoundError:
            print("Archivo no encontrado")
            self.producto = {}

    def iniciar(self):
        self.cargar()
        datos_api= self.obtener()
        if datos_api and isinstance(datos_api, list):
            print("Sincronizando precios con GitHub...")
            for prod_remoto in datos_api:
                cod_remoto = prod_remoto["cod"]
                precio_nuevo = float(prod_remoto["precio"])
                despedida_nueva = prod_remoto.get("despedida")
                for coord, info_local in self.producto.items():
                    if info_local["codigo"] == cod_remoto:
                        info_local["precio"] = precio_nuevo
                        info_local["despedida"] = despedida_nueva

    def matriz(self):
        if not self.producto:
            print("====LA MAQUINA ESTA VACIA====")
            return
        columna= set()
        fila= set()
        for coordenada in self.producto.keys():
            columna.add(coordenada[0])
            fila.add(coordenada[1:])
        columna_ordenada = sorted(list(columna))
        fila_ordenada = sorted(list(fila), key=int)
        print("\n     " + "      ".join(columna_ordenada))
        print("   " + "-------" * len(columna_ordenada))
        for fil in fila_ordenada:
            linea_impresion = f"{fil} | "
            for col in columna_ordenada:
                coordenada_actual = f"{col}{fil}"
                if coordenada_actual in self.producto:
                    item = self.producto[coordenada_actual]
                    if item["stock"] <= 0:
                        linea_impresion += "     " + "  "
                    else:
                        linea_impresion += f"{item['codigo']}  "
                else:
                    linea_impresion += "     " + "  "
                    
            print(linea_impresion)
        print("\n")

    def obtener_tarjetas(self):
        url_tarjeta= "https://raw.githubusercontent.com/FernandoSapient/BPTSP05_2526-3/refs/heads/main/clientes.json"
        try:
            print("Conectando con la base de datos...")
            res2= requests.get(url_tarjeta)
            if res2.status_code == 200:
                print("Conexion exitosa")
                return res2.json()
            else:
                print("No se pudo conectar con exito...")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error de conexión a la red: {e}")
            return None

    def actualizar_informacion(self):
        try:
            with open("inventario.txt", "w", encoding="utf-8") as f:
                for coordenada, info in self.producto.items():
                    linea = f"{coordenada},{info['codigo']},{info['nombre']},{info['precio']},{info['stock']}\n"
                    f.write(linea)
        except Exception as e:
            print(f"Error al escribir en el archivo: {e}")

    def transaccion(self):
        opcion= input("ingrese el codigo de lo que desea comprar (Ejm: A1) o escriba VOLVER para ir un paso atras: ").strip().upper()
        if opcion == "VOLVER":
            return
        if opcion not in self.producto:
            print("El producto seleccionado no se encuentra")
            return 
        opcion_producto= self.producto[opcion]
        if opcion_producto["stock"] <=0:
            print("El producto seleccionado se encuntra agotado")
            return
        tarjeta= input("ingrese su tarjeta de cliente: ").strip()
        diccionario_tarjetas_fijas = {
            "1234567890": 971972920886152672,
            "9876543210": 868325932658092573,
            "1223334444": 504500872192886429,
            "4444333221": 435273161615321974,
            "1010101010": 441428889685767119
        }
        if tarjeta in diccionario_tarjetas_fijas:
            hash_tarjeta = diccionario_tarjetas_fijas[tarjeta]
        else:
            hash_tarjeta = hash(tarjeta)
        clientes = self.obtener_tarjetas()
        if not clientes:
            print("El Usuario no fue encontrado")
            return
        cuenta_encontrada = None
        for cuenta in clientes:
            if cuenta["id"] == hash_tarjeta:
                cuenta_encontrada = cuenta
                break
        if not cuenta_encontrada:
            print("No se a encontrado")
            return
        saldo_cliente = float(cuenta_encontrada["saldo"])
        precio_producto = opcion_producto["precio"]
        if saldo_cliente < precio_producto:
            print("No se tiene el dinero sufiente para hacer la compra")
            return
        nuevo_saldo = saldo_cliente - precio_producto
        self.producto[opcion]["stock"] -= 1
        self.dinero_ganado += precio_producto
        self.ventas += 1
        self.actualizar_informacion()
        print("\n========================================")
        print("============¡COMPRA EXITOSA!============")
        print(f"====={opcion_producto['despedida']}=====")
        print(f"   Saldo restante en cuenta: ${nuevo_saldo:.2f}")
        print("========================================\n")

    def restock(self):
        opcion3= input("Ingresa la coordenada que desea modificar (Ejm: A1) o escriba VOLVER para dar un paso atras: ").strip().upper()
        if opcion3 == "VOLVER":
            return
        if not opcion3 in self.producto:
            print("No se encuentra dentro del inventario")
            return 
        producto_actual = self.producto[opcion3]
        print(f"\n Producto seleccionado: {producto_actual['nombre']}")
        print(f"   Stock actual en máquina: {producto_actual['stock']} unidades")
        try:
            cantidad_cambiante= int(input("Ingresa la cantidad a modificar en la coordenada: ").strip())
            if cantidad_cambiante <=0:
                print("No se pudo procesar el cambio \n")
                return
        except ValueError:
            print("No se pudo entrar")
            return
        self.producto[opcion3]["stock"] += cantidad_cambiante
        self.actualizar_informacion()
        print("\n========================================")
        print("=========ACTUALIZACION EXCITOSA=========")
        print(f"{producto_actual['nombre']} ahora tiene: {self.producto[opcion3]['stock']} unidades.")
        print("========================================\n")

def main_maquina():
    mi_expendedora = maquina()
    mi_expendedora.iniciar()
    while True:
        mi_expendedora.matriz()
        print("---MENU OPERATIVO---")
        print("[1] Comprar un producto")
        print("[RS] Entrar a modo Restock")
        print("[SALIR] Apagar la maquina")
        opcion2 = input("Seleccione una opción: ").strip().upper()
        if opcion2 == "1":
            mi_expendedora.transaccion()
        elif opcion2 == "SALIR":
            print("Apagando maquina expendedora. ¡Feliz dia!")
            break
        elif opcion2 == "RS":
            print("Entrando al modo Restock...")
            mi_expendedora.restock()
        else:
            print("Opcion invalida. Intente de nuevo.\n")
if __name__ == "__main__":
    main_maquina() 