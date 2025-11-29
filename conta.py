from abc import ABC, abstractmethod

class Conta(ABC):
    def __init__(self, numero: int, nome: str, senha: str, saldo: float = 0):
        self._numero = numero
        self._nome = nome
        self._senha = senha
        self._saldo = saldo
        self._ativa = True

    @property
    def numero(self):
        return self._numero

    @property
    def nome(self):
        return self._nome

    @property
    def ativa(self):
        return self._ativa

    @property
    def saldo(self):
        return self._saldo

    def _depositar(self, valor):
        self._saldo += valor

    def _sacar(self, valor):
        self._saldo -= valor

    @abstractmethod
    def calcular_taxa(self, tipo: str, valor: float) -> float:
        pass

    def verificar_senha(self, senha: str) -> bool:
        return self._senha == senha

    def desativar(self):
        self._ativa = False
