from .conta import Conta

class ContaCorrente(Conta):
    TAXAS = {
        "deposito": (0.50, 0.00),
        "saque": (1.00, 0.01),
        "transferencia": (2.00, 0.02)
    }

    def calcular_taxa(self, tipo: str, valor: float) -> float:
        fixa, percentual = self.TAXAS[tipo]
        return fixa + (percentual * valor)
