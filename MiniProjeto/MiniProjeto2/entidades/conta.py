from abc import ABC, abstractmethod
from datetime import datetime
from utilitarios.exceptions import SaldoInsuficienteError

class Conta(ABC):
    _total_contas = 0
    def __init__(self, numero: int, cliente):
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0.0
        self._historico = []
        Conta._total_contas += 1

    @property
    def saldo(self):
        return self._saldo
    
    @classmethod
    def get_total_contas(cls):
        return cls._total_contas
    
    def depositar(self, valor: float):
        if valor > 0:
            self._saldo += valor
            self._historico.append((datetime.now(), f"Depósito de R${valor:.2f}"))
            print(f"Depósito de R${valor:.2f} realizado com sucesso.\nNovo saldo: R${self._saldo:.2f}")
        else:
            print("Valor de depósito inválido.")
        
    @abstractmethod
    def sacar(self, valor: float):
        pass

    def extrato(self):
        print(f"Extrato da conta Nº {self._numero} --- Cliente: {self._cliente.nome}")
        print(f"Saldo atual: R${self._saldo:.2f}")
        print("Histórico de transações:")
        if not self._historico:
            print("Nenhuma transação realizada.")
        for data, transacao in self._historico:
            print(f"-- {data.strftime('%d/%m/%Y %H:%M:%S')}: {transacao}")
        print("-" * 20 + "\n")

class ContaCorrente(Conta):
    def __init__(self, numero: int, cliente, limite: float = 500.0):
        super().__init__(numero, cliente)
        self.limite = limite

    def sacar(self, valor: float):
        if valor <= 0:
            print("Valor de saque inválido.")
            return
        saldo_disponivel = self._saldo + self.limite
        if valor > saldo_disponivel:
            raise SaldoInsuficienteError(saldo_disponivel, valor, "Saque e limite insuficientes.")
        self._saldo -= valor
        self._historico.append((datetime.now(), f"Saque de R${valor:.2f}"))
        print(f"Saque de R${valor:.2f} realizado com sucesso.\nNovo saldo: R${self._saldo:.2f}")

class ContaPoupanca(Conta):
    def __init__(self, numero: int, cliente):
        super().__init__(numero, cliente)
    
    def sacar(self, valor: float):
        if valor <= 0:
            print("Valor de saque inválido.")
            return
        if valor > self._saldo:
            raise SaldoInsuficienteError(self._saldo, valor, "Saldo insuficiente para saque.")
        self._saldo -= valor
        self._historico.append((datetime.now(), f"Saque de R${valor:.2f}"))
        print(f"Saque de R${valor:.2f} realizado com sucesso.\nNovo saldo: R${self._saldo:.2f}")