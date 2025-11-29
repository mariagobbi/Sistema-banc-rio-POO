def ler_float_positivo(msg: str) -> float:
    while True:
        try:
            v = float(input(msg).replace(',', '.'))
            if v <= 0:
                print("Valor deve ser positivo.")
                continue
            return round(v, 2)
        except ValueError:
            print("Entrada inválida.")

def ler_int(msg: str) -> int:
    while True:
        try:
            return int(input(msg))
        except ValueError:
            print("Digite um número inteiro.")
