# Miguel Castro y Emiliana Diaz

import hashlib
import json
import matplotlib.pyplot as plt


# Representa un producto individual dentro de la máquina expendedora, guardando sus datos de identificación, costo, disponibilidad y mensaje.
class Producto:
    
    # Inicializa un nuevo objeto Producto con sus valores iniciales
    def __init__(self, idPosicion, cod, nombre, precio, stock, despedida):
        self.idPosicion = idPosicion
        self.cod = cod
        self.nombre = nombre
        self.precio = float(precio)
        self.stock = int(stock)
        self.despedida = despedida

    # Retorna el precio del producto.    
    def GetPrecio(self):
        return self.precio

    # Verifica si quedan unidades disponibles del producto en el inventario. Returns: True si hay stock, False si está agotado.  
    def CheckStock(self):
        return self.stock > 0
    
# Representa a un cliente del sistema que posee una tarjeta y un saldo disponible.
class Usuario:

    # Inicializa una cuenta de usuario vinculada a una tarjeta de pago.
    def __init__(self, hashTarjeta, saldo):
        self.hashTarjeta = str(hashTarjeta)
        self.saldo = float(saldo)

    # Compara si el saldo actual de la tarjeta es suficiente para cubrir un costo. Returns: True si el saldo alcanza, False si es insuficiente.
    def ValidarSaldo(self, monto):
        return self.saldo >= monto

# Gestiona la estructura que organiza todos los productos de la máquina expendedora.
class Catalogo:
    
    # Crea el catálogo cargando los productos desde el archivo y los organiza en un diccionario utilizando sus coordenadas en la máquina como clave.
    def __init__(self):
        self.matriz = {}
        lista_de_productos = cargar_productos()

        for prod in lista_de_productos:
            self.matriz[prod.idPosicion] = prod

    # Muestra en la pantalla de la terminal la lista completa de productos del catálogo, incluyendo su coordenada, nombre, precio y cantidad disponible.
    def DisplayCatalogo(self):
        print("Catalogo:")
        for posicion, prod in self.matriz.items():
            print(f"[{posicion}] {prod.nombre} - Precio: ${prod.precio} (Stock: {prod.stock})") 

# Modela los datos y el proceso de una transacción individual realizada por un usuario.
class Venta:

    # Crea el registro de una transacción con su identificador único, producto y monto.
    def __init__(self, idVenta, idProducto, monto, hashTarjeta=""):
        self.idVenta = int(idVenta)
        self.idProducto = str(idProducto)
        self.monto = float(monto)
        self.hashTarjeta = str(hashTarjeta)
    
    # Verifica el saldo del usuario, descuenta una unidad del inventario del producto, resta el costo del saldo de la tarjeta y muestra los mensajes de éxito en pantalla.
    def procesar_pago(self, usuario: Usuario, producto: Producto):
        if usuario.ValidarSaldo(producto.precio):
            producto.stock -=1
            usuario.saldo -= producto.precio
            print("¡Compra procesada con exito!")
            print(f"Dispensando: {producto.nombre}")
            print(f"Mensaje de la marca: ¡{producto.despedida}!")
            print(f"Su nuevo saldo es: ${usuario.saldo:.2f}")
            return True
        else:
            print("Error: Saldo insuficiente en la tarjeta.")
            return False
        
# Contiene las herramientas especiales para el mantenimiento y reabastecimiento de la máquina.
class Administracion:

    # Inicializa el módulo de control administrativo.
    def __init__(self, idRestock=1):
        self.idRestock = idRestock

    # Suma unidades adicionales al stock de un producto que ya existe en el catálogo.
    def recargar_catalogo(self, catalogo: Catalogo, idPosicion, cantidad):
        if idPosicion in catalogo.matriz:
            catalogo.matriz[idPosicion].stock += int(cantidad)
            print(f"Stock actualizado: Nuevo stock de {catalogo.matriz[idPosicion].nombre}: {catalogo.matriz[idPosicion].stock}")
        else:
            print("Error: La coordenada ingresada no existe en el catálogo.")

    # Reemplaza el producto de una coordenada o introduce uno nuevo en el catálogo.
    def cambiar_producto(self, catalogo: Catalogo, posicion, nuevo_producto):
        catalogo.matriz[posicion] = nuevo_producto
        print(f"¡Catálogo actualizado! Ahora en la posición [{posicion}] está: {nuevo_producto.nombre}")

# Encargado de acumular el historial de transacciones, calcular ganancias y generar gráficas estadísticas sobre el rendimiento de la máquina
class Reporte:

    # Inicializa los contenedores vacíos para registrar las ventas y los totales de dinero.
    def __init__(self):
        self.ventas = []
        self.totalVendido = 0
        self.dineroTotal = 0.0

    # Añade un objeto de tipo Venta al historial de la sesión y actualiza los contadores globales.
    def AgregarVenta(self, nueva_venta: Venta):
        self.ventas.append(nueva_venta)
        self.totalVendido += 1
        self.dineroTotal += nueva_venta.monto

    # Muestra en consola el resumen de cuentas: total de productos vendidos, dinero recaudado y el desglose línea por línea de cada transacción realizada.
    def GenerarReporte (self):
        print("Reporte de ventas totales:")
        print(f"Total de productos dispensados: {self.totalVendido}")
        print(f"Dinero total recaudado: ${self.dineroTotal:.2f}")
        print("Historial de transacciones:")

        if not self.ventas:
            print("No se han realizado ventas todavía.")
        else:
            for v in self.ventas:
                print(f"- Venta ID: {v.idVenta} | Código Producto: {v.idProducto} | Monto: ${v.monto:.2f}")

    # Utiliza la libreria matplotlib para construir y guardar en archivos PNG tres graficas.
    def graficar_todo(self, catalogo: Catalogo, clientes: dict):
        # Grafico de barras: Stock Inicial (Cargado) vs Ventas por Producto.
        nombres_productos = []
        cargas_totales = []
        ventas_totales = []

        for prod in catalogo.matriz.values():
            nombres_productos.append(prod.nombre)

            vendidos = sum(1 for v in self.ventas if v.idProducto == prod.cod)
            ventas_totales.append(vendidos)

            cargas_totales.append(prod.stock + vendidos)

        x = range(len(nombres_productos))
        plt.figure(figsize=(10, 5))
        plt.bar([i - 0.2 for i in x], cargas_totales, width=0.4, label='Cargado (Stock Inicial)', color='lightblue')
        plt.bar([i + 0.2 for i in x], ventas_totales, width=0.4, label='Vendido', color='orange')
        plt.xticks(x, nombres_productos, rotation=15)
        plt.ylabel('Cantidad de Unidades')
        plt.title('Inventario: Cantidad Cargada vs Vendida por Producto')
        plt.legend()
        plt.tight_layout()
        plt.savefig('reporte_productos_barras.png')
        plt.close()

        # Grafico circular: Distribución de Gastos Totales por Tarjeta de Usuario.
        usuarios_ids = []
        compras_usuarios = []

        for usr in clientes.values():
            monto_comprado = sum(v.monto for v in self.ventas if hasattr(v, 'hashTarjeta') and v.hashTarjeta == usr.hashTarjeta)
            if monto_comprado > 0:
                usuarios_ids.append(f"Tarj: {usr.hashTarjeta[-4:]}")
                compras_usuarios.append(monto_comprado)

        if compras_usuarios:
            plt.figure(figsize=(6, 6))
            plt.pie(compras_usuarios, labels=usuarios_ids, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#6bcae2','#b19cd9','#99ff99'])
            plt.title('Distribución de Gastos Totales por Usuario ($)')
            plt.tight_layout()
            plt.savefig('reporte_usuarios_circular.png')
            plt.close()

        # Grafico de lineas: Progreso temporal de los ingresos acumulados.
        if self.ventas:
            historico_ventas = []
            acumulado = 0
            for v in self.ventas:
                acumulado += v.monto
                historico_ventas.append(acumulado)

            plt.figure(figsize=(10, 4))
            plt.plot(range(1, len(historico_ventas) + 1), historico_ventas, marker='o', color='green', linestyle='-')
            plt.xlabel('Número de Transacción')
            plt.ylabel('Ingresos Acumulados ($)')
            plt.title('Evolución Temporal de las Ingresos Totales')
            plt.grid(True, linestyle='--', alpha=0.6)
            plt.tight_layout()
            plt.savefig('reporte_ingresos_linea.png')
            plt.close()

        print("¡Gráficas generadas y guardadas exitosamente en archivos PNG!")

# Lee la información de productos_api.json, cruza los datos con las coordenadas y stocks de inventario.txt. Construye la lista de objetos de tipo Producto.
def cargar_productos():
    with open("productos_api.json", "r", encoding="utf-8") as archivo_json:
        lista_api = json.load(archivo_json)

    datos_productos_api = {prod_api["cod"]: prod_api for prod_api in lista_api}
    productos_cargados = []

    with open("inventario.txt", "r", encoding="utf-8") as archivo_txt:
        for linea in archivo_txt:
            partes = linea.strip().split(",")
            if len(partes) == 3:
                idPosicion = partes[0]
                cod = partes[1]
                stock = int(partes[2])

                if cod in datos_productos_api:
                    info_api = datos_productos_api[cod]
                    nombre = info_api["prod"]
                    precio = info_api["precio"]
                    despedida = info_api["despedida"]

                    nuevo_producto = Producto(idPosicion, cod, nombre, precio, stock, despedida)
                    productos_cargados.append(nuevo_producto)
                    
    return productos_cargados

# Abre el archivo inventario.txt en modo de escritura ("w") y guarda el stock actual de cada producto, manteniendo los datos actualizados de forma permanente.
def guardar_inventario(catalogo: Catalogo):
    with open("inventario.txt", "w", encoding="utf-8") as archivo_txt:
        for posicion, prod in catalogo.matriz.items():
            archivo_txt.write(f"{posicion},{prod.cod},{prod.stock}\n")

# Lee las cuentas de los usuarios desde tarjetas_api.json y construye un diccionario donde la clave es el número de la tarjeta y el valor es el objeto Usuario.
def cargar_usuarios():
    with open("tarjetas_api.json", "r", encoding="utf-8") as archivo_json:
        lista_usuarios = json.load(archivo_json)

    usuarios_cargados = {}
    for usr in lista_usuarios:
        valores = list(usr.values())
        codigo_tarjeta = str(valores[0])
        saldo_tarjeta = float(valores[1])
        usuarios_cargados[codigo_tarjeta] = Usuario(codigo_tarjeta, saldo_tarjeta)
        
    return usuarios_cargados