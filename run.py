from sistema_bancario.bank import Bank
from sistema_bancario.cli import menu_principal

if __name__ == "__main__":
    bank = Bank()
    menu_principal(bank)