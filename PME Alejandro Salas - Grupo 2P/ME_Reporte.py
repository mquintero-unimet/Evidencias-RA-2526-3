# Autor: Alejandro Salas
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# Documentacion: Con ayuda de la IA instale "matplotlib" y me guie para hacer el Reporte de Inventario. Tambien importe "os" para manejar el directorio de los reportes y "datetime" para mostrar la fecha y hora en el reporte de texto.

import os
import matplotlib.pyplot as plt # Nota: "pip install matplotlib" para que el grafico funcione.
from datetime import datetime

# Documentacion: Mediante esta Clase se construyen los Reportes de Venta y Stock con una Funcion que genera un Archivo de Texto y otra Funcion que genera un Grafico de Barras.

class Modulo_de_Reporte():

    def __init__(self):
        self.registro_de_reportes = "Reportes"

    def Generar_Reporte(self, historial_de_ventas: list, catalogo): # Nota: Si genera fallos entonces quitar la especificacion "list".
        print("\n=========== GENERANDO REPORTE ===========")

        if not os.path.exists(self.registro_de_reportes):
            try:
                os.makedirs(self.registro_de_reportes)
                print(f"[INFORMACION] Se ha creado la carpeta '{self.registro_de_reportes}' para organizar los reportes")
            except Exception as x:
                print(f"[ERROR] No se pudo crear la carpeta de reportes: {x}")
                return
            
        self.Generar_txt(historial_de_ventas)
        self.Generar_Grafico(catalogo)

    def Generar_txt(self, historial: list): # Nota: Si genera fallos entonces quitar la especificacion "list".
        txt = os.path.join(self.registro_de_reportes, "Reporte_de_Ventas.txt")
        ingreso_total = sum(y["Precio"] for y in historial)

        try:
            with open(txt, "w", encoding = "utf-8") as z:
                z.write("========================================\n")
                z.write("          REPORTE DE VENTAS\n")
                z.write("========================================\n")
                z.write(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                z.write("-" * 40 + "\n")
                if not historial:
                    z.write("No se realizaron ventas en este turno.\n")
                else:
                    for v in historial:
                        z.write(f"- {v['Producto']:<25} | ${v['Precio']:.2f}\n")
                z.write("-" * 40 + "\n")
                z.write(f"TOTAL INGRESOS: ${ingreso_total:.2f}\n")
                z.write("========================================\n")
            print(f"[EXITO] Reporte escrito guardado en: {txt}")
        except Exception as x:
            print(f"[ERROR] No se pudo generar el Archivo de Texto: {x}")

    def Generar_Grafico(self, catalogo):
        grafico = os.path.join(self.registro_de_reportes, "Grafico_de_Stock.png")

        try:
            nombres = []
            stocks = []
            for prod in catalogo.matriz_de_productos.values():
                nombres.append(prod.codigo)
                stocks.append(prod.stock)

            plt.figure(figsize = (10, 6))
            plt.bar(nombres, stocks, color = 'skyblue', edgecolor = 'navy')
            plt.title("Stock Actual de Productos en la Maquina Expendedora")
            plt.xlabel("Codigo de Producto")
            plt.ylabel("Unidades Disponibles")
            plt.xticks(rotation = 45)
            plt.grid(axis = 'y', linestyle = '--', alpha = 0.7)
            plt.tight_layout()
            plt.savefig(grafico)
            plt.close()
            print(f"[INFORMACION] Grafico de Stock guardado en: {grafico}")
        except ImportError:
            print("[AVISO] Matplotlib no esta Instalado. No se pudo generar el Grafico del Bono.")
            return
        except Exception as x:
            print(f"[ERROR] No se pudo generar el Grafico de Barras: {x}")

# Nota: Numero de Cuenta = Numero de Trajeta || Transaccion = Operacion (Ventas).