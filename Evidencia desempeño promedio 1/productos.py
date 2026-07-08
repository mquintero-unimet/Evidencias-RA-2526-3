class Producto:
    def __init__(self, codigo, nombre, precio, stock_actual):
        self.codigo = codigo
        self.nombre = nombre
        self.precio = precio
        self.stock_actual = stock_actual
        self.stock_colocado_restock = 0
        self.cantidad_vendida = 0
        self.mensaje_despedida = ""

    def actualizar_precio(self, nuevo_precio: float):
        self.precio = nuevo_precio

    def descontar_stock(self, cantidad: int):
        self.stock_actual -= cantidad