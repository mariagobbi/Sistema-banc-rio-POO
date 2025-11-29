from typing import List, Optional
from datetime import datetime
from .conta_corrente import ContaCorrente
from getpass import getpass
from utils.leitor import ler_float_positivo, ler_int

class Banco:

    GERENTE_SENHA = "gerente123"

    def __init__(self):
        self.contas: List[ContaCorrente] = []
        self.transacoes: List[List] = []

    def encontrar_conta(self, numero: int) -> Optional[ContaCorrente]:
        for c in self.contas:
            if c.numero == numero and c.ativa:
                return c
        return None

    def cadastrar_conta(self):
        print("\n=== CADASTRO DE CONTA ===")
        numero = ler_int("Número da conta: ")
        if self.encontrar_conta(numero):
            print("Conta já existe.")
            return

        nome = input("Nome do titular: ")
        senha = getpass("Senha: ")
        saldo = ler_float_positivo("Saldo inicial: R$ ")

        conta = ContaCorrente(numero, nome, senha, saldo)
        self.contas.append(conta)
        print(f"Conta criada com sucesso! Número: {numero}")

    def autenticar(self):
        print("\n=== LOGIN ===")
        numero = ler_int("Número da conta: ")
        senha = getpass("Senha: ")

        conta = self.encontrar_conta(numero)
        if not conta or not conta.verificar_senha(senha):
            print("Credenciais inválidas.")
            return None

        print(f"Bem-vindo(a), {conta.nome}!")
        return conta

    def ver_saldo(self, conta):
        print(f"Saldo atual: R${conta.saldo:.2f}")

    def deposito(self, conta):
        print("\n=== DEPÓSITO ===")
        valor = ler_float_positivo("Valor do depósito: R$ ")
        taxa = conta.calcular_taxa("deposito", valor)
        total = valor - taxa

        if total <= 0:
            print("Valor muito baixo para cobrir a taxa.")
            return

        conta._depositar(total)
        self.transacoes.append([datetime.now().isoformat(), "DEPÓSITO", conta.numero, None, valor, taxa])
        print(f"Depósito realizado! Líquido: R${total:.2f}")

    def saque(self, conta):
        print("\n=== SAQUE ===")
        valor = ler_float_positivo("Valor do saque: R$ ")
        taxa = conta.calcular_taxa("saque", valor)
        total = valor + taxa

        if conta.saldo < total:
            print("Saldo insuficiente.")
            return

        conta._sacar(total)
        self.transacoes.append([datetime.now().isoformat(), "SAQUE", conta.numero, None, valor, taxa])
        print(f"Saque realizado! Total debitado: R${total:.2f}")

    def transferencia(self, origem):
        print("\n=== TRANSFERÊNCIA ===")
        destino_num = ler_int("Conta destino: ")
        destino = self.encontrar_conta(destino_num)

        if not destino or destino.numero == origem.numero:
            print("Conta destino inválida.")
            return

        valor = ler_float_positivo("Valor: R$ ")
        taxa = origem.calcular_taxa("transferencia", valor)
        total = valor + taxa

        if origem.saldo < total:
            print("Saldo insuficiente.")
            return

        origem._sacar(total)
        destino._depositar(valor)

        self.transacoes.append([datetime.now().isoformat(), "TRANSFERÊNCIA", origem.numero, destino.numero, valor, taxa])
        print("Transferência realizada com sucesso.")

    def listar_saldos(self):
        print("\n=== LISTA DE SALDOS ===")
        senha = getpass("Senha do gerente: ")

        if senha != self.GERENTE_SENHA:
            print("Senha incorreta.")
            return

        print(f"{'Conta':>6} | {'Titular':<20} | Saldo")
        print("-" * 40)
        for c in self.contas:
            print(f"{c.numero:>6} | {c.nome:<20} | R${c.saldo:.2f}")
