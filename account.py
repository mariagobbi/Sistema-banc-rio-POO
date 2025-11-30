from __future__ import annotations
from dataclasses import dataclass, field
from decimal import Decimal, ROUND_HALF_UP

def _round_money(value: float) -> float:
    d = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return float(d)

@dataclass
class Account:
    numero: int
    nome: str
    _senha: str
    saldo: float = field(default=0.0)
    ativa: bool = field(default=True)

    def autenticar(self, senha: str) -> bool:
        return self.ativa and senha == self._senha

    def creditar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Valor de crédito deve ser positivo.")
        self.saldo = _round_money(self.saldo + valor)

    def debitar(self, valor: float) -> None:
        if valor <= 0:
            raise ValueError("Valor de débito deve ser positivo.")
        if self.saldo < valor:
            raise ValueError("Saldo insuficiente.")
        self.saldo = _round_money(self.saldo - valor)

    def alterar_senha(self, senha_atual: str, nova_senha: str) -> bool:
        if self._senha != senha_atual:
            return False
        self._senha = nova_senha
        return True

    def desativar(self):
        self.ativa = False

    def ativar(self):
        self.ativa = True

    def __repr__(self):
        status = "ativa" if self.ativa else "inativa"
        return f"<Account {self.numero} {self.nome} saldo=R${self.saldo:.2f} {status}>"
