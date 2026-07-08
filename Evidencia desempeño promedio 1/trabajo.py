import json
import os
import hashlib

class Producto:
    """Clase que representa un producto en la máquina expendedora."""
    def __init__(self, codigo: str, nombre: str, precio: float, stock_actual: int):
        self.codigo = codigo[:5] 
        self.nombre = nombre
        self.precio = precio
        self.stock_actual = stock_actual
        self.stock_colocado_restock = stock_actual 
        self.cantidad_vendida = 0
        self.mensaje_despedida = f"¡Gracias por comprar {self.nombre}!"

    def actualizar_precio(self, nuevo_precio: float):
        """Actualiza el precio del producto."""
        self.precio = nuevo_precio

    def descontar_stock(self, cantidad: int):
        """Descuenta el inventario tras una venta."""
        if self.stock_actual >= cantidad:
            self.stock_actual -= cantidad
            self.cantidad_vendida += cantidad

    def to_dict(self):
        """Convierte el objeto a diccionario para guardarlo en JSON."""
        return {
            "codigo": self.codigo,
            "nombre": self.nombre,
            "precio": self.precio,
            "stock_actual": self.stock_actual,
            "stock_colocado_restock": self.stock_colocado_restock,
            "cantidad_vendida": self.cantidad_vendida,
            "mensaje_despedida": self.mensaje_despedida
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Construye un objeto Producto desde un diccionario."""
        prod = cls(data["codigo"], data["nombre"], data["precio"], data["stock_actual"])
        prod.stock_colocado_restock = data.get("stock_colocado_restock", data["stock_actual"])
        prod.cantidad_vendida = data.get("cantidad_vendida", 0)
        prod.mensaje_despedida = data.get("mensaje_despedida", f"¡Gracias por comprar {prod.nombre}!")
        return prod


class Tarjeta:
    """Clase para manejar las tarjetas prepagadas usando su hash."""
    def __init__(self, hash_numero: str, saldo: float):
        self.hash_numero = hash_numero
        self.saldo = saldo
        self.dinero_gastado = 0.0

    def verificar_saldo(self, monto: float) -> bool:
        """Verifica si hay saldo suficiente."""
        return self.saldo >= monto

    def descontar_saldo(self, monto: float):
        """Resta el saldo y suma al dinero gastado por el usuario."""
        self.saldo -= monto
        self.dinero_gastado += monto


class GestorArchivos:
    """Maneja la lectura y escritura de archivos locales."""
    ARCHIVO_INVENTARIO = 'inventario_local.json'

    def cargar_inventario_local(self) -> dict:
        """Carga el inventario desde el archivo JSON."""
        if not os.path.exists(self.ARCHIVO_INVENTARIO):
            return {}
        try:
            with open(self.ARCHIVO_INVENTARIO, 'r', encoding='utf-8') as f:
                datos = json.load(f)
                return {coord: Producto.from_dict(prod) for coord, prod in datos.items()}
        except Exception:
            return {}

    def guardar_inventario_local(self, inventario: dict):
        """Guarda el inventario actual en el archivo JSON."""
        datos = {coord: prod.to_dict() for coord, prod in inventario.items()}
        with open(self.ARCHIVO_INVENTARIO, 'w', encoding='utf-8') as f:
            json.dump(datos, f, indent=4)

    def escribir_reporte_txt(self, contenido: str):
        """Guarda el reporte en un archivo de texto."""
        with open('reporte_ventas.txt', 'w', encoding='utf-8') as f:
            f.write(contenido)


class MaquinaExpendedora:
    """Clase principal que maneja los módulos de Catálogo, Venta, Restock y Reporte."""
    def __init__(self):
        self.inventario = {}  
        self.tarjetas_validas = {}  
        self.total_dinero_cobrado = 0.0
        self.total_productos_vendidos = 0
        self.historico_ventas = [] 
        self.gestor = GestorArchivos()

    def obtener_hash(self, texto: str) -> str:
        """Genera un hash seguro usando hashlib."""
        return hashlib.sha256(texto.encode('utf-8')).hexdigest()

    def iniciar_maquina(self):
        """Carga datos locales y actualiza precios/tarjetas simulando el repositorio."""
        self.inventario = self.gestor.cargar_inventario_local()
        if not self.inventario:
            print("Inventario local no encontrado. Asumiendo máquina vacía.")
        
        
        try:
            if os.path.exists("github_productos.json"):
                with open("github_productos.json", 'r', encoding='utf-8') as f:
                    datos_nube = json.load(f)
                    for coord, datos in datos_nube.items():
                        if coord in self.inventario:
                            self.inventario[coord].actualizar_precio(datos['precio'])
        except Exception:
            print("No se pudo revisar precios en el repositorio.")

        try:
            if os.path.exists("github_tarjetas.json"):
                with open("github_tarjetas.json", 'r', encoding='utf-8') as f:
                    tarjetas_nube = json.load(f)
                    for num_tarjeta, saldo in tarjetas_nube.items():
                        hash_t = self.obtener_hash(num_tarjeta)
                        self.tarjetas_validas[hash_t] = Tarjeta(hash_t, saldo)
            else:
                # Tarjetas por defecto si no existe el archivo simulado
                tarjetas_prueba = ["1234567890", "9876543210", "1223334444", "4444333221", "1010101010"]
                for t in tarjetas_prueba:
                    self.tarjetas_validas[self.obtener_hash(t)] = Tarjeta(self.obtener_hash(t), 100.0)
        except Exception:
            pass

    def mostrar_catalogo(self):
        """Módulo 1: Imprime el catálogo en formato de matriz."""
        if not self.inventario:
            print("\n[La máquina no tiene productos configurados]")
            return

        filas = sorted(list(set(int(coord[1:]) for coord in self.inventario.keys())))
        columnas = sorted(list(set(coord[0].upper() for coord in self.inventario.keys())))

        print("\n--- CATÁLOGO ---")
        print("   " + "      ".join(columnas))
        for f in filas:
            fila_str = f"{f}  "
            for c in columnas:
                coord = f"{c}{f}"
                if coord in self.inventario and self.inventario[coord].stock_actual > 0:
                    fila_str += f"{self.inventario[coord].codigo:<7}"
                else:
                    fila_str += "       "
            print(fila_str)

    def procesar_venta(self, coordenada: str):
        """Módulo 2: Maneja la lógica de venta de un producto."""
        coordenada = coordenada.upper()
        if coordenada not in self.inventario or self.inventario[coordenada].stock_actual <= 0:
            print("Producto inválido o agotado.")
            return

        producto = self.inventario[coordenada]
        print(f"Precio de {producto.nombre}: ${producto.precio:.2f}")

        num_tarjeta = input("Introduzca número de tarjeta (Enter cancela): ").strip()
        if not num_tarjeta:
            print("Venta cancelada.")
            return

        hash_t = self.obtener_hash(num_tarjeta)
        if hash_t not in self.tarjetas_validas:
            print("Tarjeta inválida o no registrada.")
            return

        tarjeta = self.tarjetas_validas[hash_t]
        conf = input(f"¿Confirmar compra de {producto.nombre}? (S/N): ").upper()
        
        if conf == 'S':
            if tarjeta.verificar_saldo(producto.precio):
                tarjeta.descontar_saldo(producto.precio)
                producto.descontar_stock(1)
                
                self.total_dinero_cobrado += producto.precio
                self.total_productos_vendidos += 1
                self.historico_ventas.append(self.total_dinero_cobrado)
                
                self.gestor.guardar_inventario_local(self.inventario)
                print(f"Dispensando {producto.nombre}...")
                print(producto.mensaje_despedida)
            else:
                print("Saldo insuficiente en la tarjeta.")
        else:
            print("Venta cancelada.")

    def realizar_restock(self):
        """Módulo 3: Permite actualizar existencias o cambiar un producto."""
        print("\n--- RESTOCK ---")
        print("1. Actualizar existencia de inventario")
        print("2. Cambiar producto")
        op = input("Opción: ").strip()
        if op not in ['1', '2']:
            print("Opción no válida.")
            return

        coord = input("Introduzca coordenada (ej. A1): ").upper()

        if op == '1':
            if coord in self.inventario:
                try:
                    cant = int(input("Cantidad a añadir: "))
                    self.inventario[coord].stock_actual += cant
                    self.inventario[coord].stock_colocado_restock += cant
                    print(f"Stock actualizado a {self.inventario[coord].stock_actual}.")
                except ValueError:
                    print("Error: Ingrese un número entero válido.")
            else:
                print("Coordenada vacía. Use la opción 2 para crear el producto primero.")
        
        elif op == '2':
            cod = input("Nuevo código (5 letras max): ")[:5]
            nom = input("Nombre completo del producto: ")
            try:
                prec = float(input("Precio: "))
                stk = int(input("Existencia inicial: "))
            except ValueError:
                print("Error: Formato de precio o cantidad inválido.")
                return
                
            self.inventario[coord] = Producto(cod, nom, prec, stk)
            print(f"Producto {cod} asignado a la coordenada {coord}.")

        self.gestor.guardar_inventario_local(self.inventario)

    def generar_reporte(self):
        """Módulo 4: Genera el txt de reporte con representaciones visuales (ASCII)."""
        txt = "--- REPORTE DE VENTAS ---\n\nPRODUCTOS:\n"
        for c, p in self.inventario.items():
            txt += f"- {p.nombre} ({p.codigo}): Colocados {p.stock_colocado_restock}, Vendidos {p.cantidad_vendida}\n"
        
        txt += f"\nTOTALES:\nProductos vendidos: {self.total_productos_vendidos}\nDinero cobrado: ${self.total_dinero_cobrado:.2f}\n"
        txt += "\nUSUARIOS (TARJETAS):\n"
        
        usuarios_activos = [t for t in self.tarjetas_validas.values() if t.dinero_gastado > 0]
        for t in usuarios_activos:
            txt += f"- Hash {t.hash_numero[:10]}... gastó: ${t.dinero_gastado:.2f}\n"
        
        txt += f"\nTotal usuarios registrados: {len(self.tarjetas_validas)}\n"

        # Alternativa sin Matplotlib: Gráficos ASCII en el archivo de texto
        txt += "\n" + "="*30 + "\n"
        txt += "REPRESENTACIÓN VISUAL (ASCII)\n"
        txt += "="*30 + "\n\n"

        if self.inventario:
            txt += "[GRÁFICO DE BARRAS: STOCK vs VENDIDO]\n"
            for c, p in self.inventario.items():
                bar_stock = "█" * p.stock_colocado_restock
                bar_vend = "▓" * p.cantidad_vendida
                txt += f"{p.codigo:<7} | Colocados: {bar_stock} ({p.stock_colocado_restock})\n"
                txt += f"        | Vendidos : {bar_vend} ({p.cantidad_vendida})\n\n"

        if self.historico_ventas:
            txt += "[HISTÓRICO DE CRECIMIENTO DE VENTAS ($)]\n"
            for i, venta in enumerate(self.historico_ventas, 1):
                # Escalamos para que la barra no sea inmensa si el monto es alto
                escala = int(venta / 5) 
                bar_dinero = "■" * escala
                txt += f"Venta {i:<2} | {bar_dinero} (${venta:.2f})\n"

        self.gestor.escribir_reporte_txt(txt)
        print("Reporte generado exitosamente con gráficos ASCII en 'reporte_ventas.txt'.")

    def run(self):
        """Bucle principal que mantiene la máquina en funcionamiento."""
        self.iniciar_maquina()
        while True:
            self.mostrar_catalogo()
            cmd = input("\nCoordenada (ej. A1), 'RS' (Restock), 'RP' (Reporte), 'Q' (Salir): ").upper()
            
            if cmd == 'Q':
                print("Apagando...")
                break
            elif cmd == 'RS':
                self.realizar_restock()
            elif cmd == 'RP':
                self.generar_reporte()
            elif len(cmd) >= 2:
                self.procesar_venta(cmd)
            else:
                print("Comando no reconocido.")

if __name__ == "__main__":
    app = MaquinaExpendedora()
    app.run()