# Autor: Alejandro Salas
#- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -#

# Documentacion: Esta Clase es el Motor de Venta que permite ejecutar todas las transacciones y con ello a su ves mobilizar todo el sistema. Adicionalmente, tiene una funcion para Solicitar el "Numero de Cuenta" o "Numero de Tarjeta".

class Modulo_de_Venta():

    def __init__(self):
        self.historial_de_ventas = []

    def Iniciar_Ventas(self, producto, diccionario_de_tarjetas):
        if producto.stock <= 0:
            print("[ERROR] Producto Agotado.")
            return
        
        print(f"[INFORMACION] Producto seleccionado: {producto.nombre} || Precio: ${producto.precio:.2f}")

        tarjeta = self.Solicitar_Tarjeta(diccionario_de_tarjetas)

        if not tarjeta:
            print("[ERROR] Transaccion Invalida, revise el Numero de Cuenta ingresado.")
            return
        if tarjeta.Descontar_Fondos(producto.precio):
            producto.Actualizar_Stock(-1)
            self.historial_de_ventas.append({
                "Producto": producto.nombre,
                "Precio": producto.precio,
                "Numero de Cuenta": tarjeta.id
            })
            print(f"[EXITO] ¡Transaccion Exitosa! Fondo Resultante: ${tarjeta.fondos:.2f}")
            print(f"[AGRADECIMIENTO] Mensaje: {producto.despedida}")
        else:
            print("[ERROR] Fondos Insuficientes, consulte su Disponibilidad Bancaria antes de realizar otra compra.")

    def Solicitar_Tarjeta(self, diccionario_de_tarjetas):
        cuenta = input("[SOLICITUD] Ingrese su Numero de Tarjeta (10 dígitos): ")
        
        respaldo_de_numeros_de_cuentas = { # Nota: Mapeo de Respaldo para evitar inconvenientes.
            "1234567890": 971972920886152672,
            "9876543210": 868325932658092573,
            "1223334444": 5045008721928864229,
            "4444333221": 4352731616153219794,
            "1010101010": 4414288896857671194
        }
        
        id_a_buscar = respaldo_de_numeros_de_cuentas.get(cuenta)
        
        if id_a_buscar in diccionario_de_tarjetas:
            return diccionario_de_tarjetas[id_a_buscar]
        return None