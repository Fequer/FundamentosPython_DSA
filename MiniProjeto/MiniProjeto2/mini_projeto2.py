from utilitarios.exceptions import SaldoInsuficienteError, ContaInexistenteError
from operacoes.banco import Banco

def menu_principal():
    print("\n=== Bem-vindo ao Sistema Bancário ===\n")
    print("1. Adicionar Cliente")
    print("2. Criar Conta")
    print("3. Acessar Conta")
    print("4. Sair\n")
    return input("Escolha uma opção: ")

def menu_conta(banco):
    try:
        numero_conta = int(input("Digite o número da conta: "))
        conta = banco.buscar_conta(numero_conta)
        while True:
            print(f"\n=== Operações para Conta Nº {numero_conta} ===\n")
            print(f"Cliente: {conta._cliente.nome} || Saldo: R${conta.saldo:.2f}\n")
            print("1. Depositar")
            print("2. Sacar")
            print("3. Ver Extrato")
            print("4. Voltar ao Menu Principal\n")
            opcao = input("Escolha uma opção: ")
            if opcao == '1':
                valor = float(input("Digite o valor a ser depositado: "))
                conta.depositar(valor)
            elif opcao == '2':
                try:
                    valor = float(input("Digite o valor para saque: "))
                    conta.sacar(valor)
                except SaldoInsuficienteError as e:
                    print(f"Erro na operação: {e}")
            elif opcao == '3':
                conta.extrato()
            elif opcao == '4':
                break
            else:
                print("Opção inválida. Tente novamente.")
    except ContaInexistenteError as e:
        print(f"Erro: {e}")
    except ValueError:
        print("Erro: Entrada inválida. Por favor, digite um número.")

def main():
    banco = Banco("Banco Digital")
    while True:
        opcao = menu_principal()
        if opcao == '1':
            nome = input("Digite o nome do cliente: ")
            cpf = input("Digite o CPF do cliente: ")
            banco.adicionar_cliente(nome, cpf)
        elif opcao == '2':
            cpf = input("Digite o CPF do cliente para criar a conta: ")
            cliente = banco._clientes.get(cpf)
            if cliente:
                tipo = input("Digite o tipo de conta (corrente/poupanca): ")
                banco.criar_conta(cliente, tipo)
            else:
                print("Cliente não encontrado. Por favor, cadastre o cliente primeiro.")
        elif opcao == '3':
            menu_conta(banco)
        elif opcao == '4':
            print("\nSaindo do sistema. Até logo!\n")
            break
        else:
            print("\nOpção inválida. Tente novamente.\n")

if __name__ == "__main__":
    main()