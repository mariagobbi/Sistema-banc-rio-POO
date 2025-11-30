from typing import Dict, List, Optional
from .account import Account
from .transaction import Transaction
from decimal import Decimal, ROUND_HALF_UP

class BankError(Exception):
    pass

class Bank:
    def __init__(self, gerente_senha: str = "gerente123") -> None:
        self._accounts: Dict[int, Account] = {}
        self._taxas = [
            (0.50, 0.00),
            (1.00, 0.01),
            (2.00, 0.02),
        ]
        self.transactions: List[Transaction] = []
        self.gerente_senha = gerente_senha

    @staticmethod
    def _round_money(value: float) -> float:
        d = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        return float(d)

    def calcular_taxa(self, indice: int, valor: float) -> float:
        fixa, perc = self._taxas[indice]
        return self._round_money(fixa + perc * valor)

    def listar_taxas(self) -> List[Dict]:
        nomes = ["Depósito", "Saque", "Transferência"]
        return [{"servico": nomes[i], "taxa_fixa": t[0], "percentual": t[1]} for i, t in enumerate(self._taxas)]

    def cadastrar_conta(self, numero: int, nome: str, senha: str, saldo_inicial: float) -> Account:
        if numero in self._accounts:
            raise BankError("Já existe uma conta com esse número.")
        if saldo_inicial < 0:
            raise BankError("Saldo inicial não pode ser negativo.")
        acc = Account(numero, nome.strip(), senha, self._round_money(saldo_inicial), True)
        self._accounts[numero] = acc
        return acc

    def encontrar_conta(self, numero: int) -> Optional[Account]:
        acc = self._accounts.get(numero)
        return acc if acc and acc.ativa else None

    def autenticar(self, numero: int, senha: str) -> Optional[Account]:
        acc = self._accounts.get(numero)
        return acc if acc and acc.autenticar(senha) else None

    def deposito(self, numero: int, valor: float) -> Transaction:
        acc = self.encontrar_conta(numero)
        if not acc:
            raise BankError("Conta não encontrada/ativa.")
        taxa = self.calcular_taxa(0, valor)
        liquido = valor - taxa
        if liquido <= 0:
            raise BankError("Valor muito baixo frente à taxa.")
        acc.creditar(liquido)
        tr = Transaction.create("DEPÓSITO", numero, None, valor, taxa, acc.saldo, None)
        self.transactions.append(tr)
        return tr

    def saque(self, numero: int, valor: float) -> Transaction:
        acc = self.encontrar_conta(numero)
        if not acc:
            raise BankError("Conta não encontrada/ativa.")
        taxa = self.calcular_taxa(1, valor)
        total = valor + taxa
        if acc.saldo < total:
            raise BankError("Saldo insuficiente.")
        acc.debitar(total)
        tr = Transaction.create("SAQUE", numero, None, valor, taxa, acc.saldo, None)
        self.transactions.append(tr)
        return tr

    def transferencia(self, origem: int, destino: int, valor: float) -> Transaction:
        if origem == destino:
            raise BankError("Não pode transferir para a mesma conta.")
        acc_o = self.encontrar_conta(origem)
        acc_d = self.encontrar_conta(destino)
        if not acc_o or not acc_d:
            raise BankError("Conta de origem ou destino inválida.")
        taxa = self.calcular_taxa(2, valor)
        total = valor + taxa
        if acc_o.saldo < total:
            raise BankError("Saldo insuficiente.")
        acc_o.debitar(total)
        acc_d.creditar(valor)
        tr = Transaction.create("TRANSFERÊNCIA", origem, destino, valor, taxa, acc_o.saldo, acc_d.saldo)
        self.transactions.append(tr)
        return tr

    def listar_saldos_gerente(self, senha: str):
        if senha != self.gerente_senha:
            raise BankError("Senha incorreta.")
        return [{"numero": a.numero, "titular": a.nome, "saldo": a.saldo, "ativa": a.ativa} for a in self._accounts.values()]