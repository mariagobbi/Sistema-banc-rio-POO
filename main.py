from models.banco import Banco

banco = Banco()

while True:
    print("\n=== SISTEMA BANCÁRIO ===")
    print("1) Criar conta")
    print("2) Login")
    print("3) Listar saldos (gerente)")
    print("0) Sair")
    op = input("Opção: ")

    if op == "1":
        banco.cadastrar_conta()

    elif op == "2":
        conta = banco.autenticar()
        if conta:
            while True:
                print("\n--- MENU DA CONTA ---")
                print("1) Saldo")
                print("2) Depósito")
                print("3) Saque")
                print("4) Transferência")
                print("0) Sair")
                op2 = input("Opção: ")

                if op2 == "1":
                    banco.ver_saldo(conta)
                elif op2 == "2":
                    banco.deposito(conta)
                elif op2 == "3":
                    banco.saque(conta)
                elif op2 == "4":
                    banco.transferencia(conta)
                elif op2 == "0":
                    break
                else:
                    print("Opção inválida.")

    elif op == "3":
        banco.listar_saldos()

    elif op == "0":
        print("Encerrando...")
        break

    else:
        print("Opção inválida.")
