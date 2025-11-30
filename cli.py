from getpass import getpass
from .bank import Bank, BankError

def ler_float(msg: str) -> float:
    while True:
        try:
            v = float(input(msg).replace(',', '.'))
            if v <= 0:
                print("Valor deve ser positivo.")
                continue
            return round(v, 2)
        except:
            print("Inválido.")

def ler_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except:
            print("Inválido.")

def menu_conta(bank: Bank, numero: int):
    acc = bank.encontrar_conta(numero)
    if not acc:
        print("Conta inválida.")
        return
    while True:
        print("\n--- MENU CONTA ---")
        print("1) Saldo")
        print("2) Depósito")
        print("3) Saque")
        print("4) Transferência")
        print("5) Taxas")
        print("0) Sair")
        op = input("Escolha: ")
        try:
            if op == "1":
                print(f"Saldo: R${acc.saldo:.2f}")
            elif op == "2":
                v = ler_float("Valor: ")
                t = bank.deposito(numero, v)
                print("OK.")
            elif op == "3":
                v = ler_float("Valor: ")
                t = bank.saque(numero, v)
                print("OK.")
            elif op == "4":
                dest = ler_int("Conta destino: ")
                v = ler_float("Valor: ")
                t = bank.transferencia(numero, dest, v)
                print("OK.")
            elif op == "5":
                for t in bank.listar_taxas():
                    print(t)
            elif op == "0":
                break
        except BankError as e:
            print("ERRO:", e)

def menu_principal(bank: Bank):
    while True:
        print("\n=== SISTEMA BANCÁRIO ===")
        print("1) Criar conta")
        print("2) Login")
        print("3) Saldos (gerente)")
        print("0) Sair")
        op = input("Opção: ")
        if op == "1":
            num = ler_int("Número: ")
            nome = input("Nome: ")
            senha = getpass("Senha: ")
            saldo = ler_float("Saldo inicial: ")
            try:
                bank.cadastrar_conta(num, nome, senha, saldo)
                print("Conta criada.")
            except BankError as e:
                print("ERRO:", e)
        elif op == "2":
            num = ler_int("Número: ")
            senha = getpass("Senha: ")
            acc = bank.autenticar(num, senha)
            if acc:
                menu_conta(bank, num)
            else:
                print("Login inválido.")
        elif op == "3":
            s = getpass("Senha gerente: ")
            try:
                print(bank.listar_saldos_gerente(s))
            except BankError as e:
                print("ERRO:", e)
        elif op == "0":
            break