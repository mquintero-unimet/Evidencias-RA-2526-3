class Tarjeta:
    def __init__(self, hash_numero, saldo):
        self.hash_numero = hash_numero
        self.saldo = saldo
        self.dinero_gastado = 0.0

    def verificar_saldo(self, monto: float) -> bool:
        return self.saldo >= monto

    def descontar_saldo(self, monto: float):
        self.saldo -= monto
        self.dinero_gastado += monto