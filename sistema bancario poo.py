import textwrap
from datetime import datetime

class Usuario:
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

    def __str__(self):
        return f"{self.nome} ({self.cpf})"


class Conta:
    LIMITE_SAQUES = 3

    def __init__(self, agencia, numero, usuario):
        self.agencia = agencia
        self.numero = numero
        self.usuario = usuario
        self.saldo = 0
        self.limite = 500
        self.extrato = ""
        self.numero_saques = 0

    def depositar(self, valor):
        if valor > 0:
            self.saldo += valor
            self.extrato += f"Depósito:\tR$ {valor:.2f}\n"
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

    def sacar(self, valor):
        excedeu_saldo = valor > self.saldo
        excedeu_limite = valor > self.limite
        excedeu_saques = self.numero_saques >= Conta.LIMITE_SAQUES

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Saldo insuficiente. @@@")
        elif excedeu_limite:
            print("\n@@@ Operação falhou! O valor excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques atingido. @@@")
        elif valor > 0:
            self.saldo -= valor
            self.extrato += f"Saque:\t\tR$ {valor:.2f}\n"
            self.numero_saques += 1
            print("\n=== Saque realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! Valor inválido. @@@")

    def exibir_extrato(self):
        print("\n================ EXTRATO ================")
        print("Não foram realizadas movimentações." if not self.extrato else self.extrato)
        print(f"\nSaldo:\t\tR$ {self.saldo:.2f}")
        print("==========================================")

    def __str__(self):
        return f"Agência: {self.agencia} | Conta: {self.numero} | Titular: {self.usuario.nome}"


class Banco:
    def __init__(self):
        self.usuarios = []
        self.contas = []
        self.agencia_padrao = "0001"

    def menu(self):
        opcoes = """
        ================ MENU ================
        [d]  Depositar
        [s]  Sacar
        [e]  Extrato
        [nc] Nova conta
        [lc] Listar contas
        [nu] Novo usuário
        [q]  Sair
        => """
        return input(textwrap.dedent(opcoes))

    def criar_usuario(self):
        cpf = input("Informe o CPF (somente números): ")
        if self.filtrar_usuario(cpf):
            print("\n@@@ Já existe usuário com esse CPF! @@@")
            return

        nome = input("Informe o nome completo: ")
        data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
        endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

        usuario = Usuario(nome, data_nascimento, cpf, endereco)
        self.usuarios.append(usuario)
        print("\n=== Usuário criado com sucesso! ===")

    def filtrar_usuario(self, cpf):
        for usuario in self.usuarios:
            if usuario.cpf == cpf:
                return usuario
        return None

    def criar_conta(self):
        cpf = input("Informe o CPF do usuário: ")
        usuario = self.filtrar_usuario(cpf)
        if not usuario:
            print("\n@@@ Usuário não encontrado. @@@")
            return

        numero_conta = len(self.contas) + 1
        conta = Conta(self.agencia_padrao, numero_conta, usuario)
        usuario.adicionar_conta(conta)
        self.contas.append(conta)
        print("\n=== Conta criada com sucesso! ===")

    def listar_contas(self):
        for conta in self.contas:
            print("=" * 50)
            print(conta)

    def executar(self):
        while True:
            opcao = self.menu()

            if opcao == "d":
                cpf = input("CPF do titular: ")
                usuario = self.filtrar_usuario(cpf)
                if usuario and usuario.contas:
                    conta = usuario.contas[0]
                    valor = float(input("Informe o valor do depósito: "))
                    conta.depositar(valor)
                else:
                    print("\n@@@ Usuário/conta não encontrada. @@@")

            elif opcao == "s":
                cpf = input("CPF do titular: ")
                usuario = self.filtrar_usuario(cpf)
                if usuario and usuario.contas:
                    conta = usuario.contas[0]
                    valor = float(input("Informe o valor do saque: "))
                    conta.sacar(valor)
                else:
                    print("\n@@@ Usuário/conta não encontrada. @@@")

            elif opcao == "e":
                cpf = input("CPF do titular: ")
                usuario = self.filtrar_usuario(cpf)
                if usuario and usuario.contas:
                    usuario.contas[0].exibir_extrato()
                else:
                    print("\n@@@ Usuário/conta não encontrada. @@@")

            elif opcao == "nu":
                self.criar_usuario()

            elif opcao == "nc":
                self.criar_conta()

            elif opcao == "lc":
                self.listar_contas()

            elif opcao == "q":
                print("\nSaindo...")
                break

            else:
                print("\n@@@ Opção inválida! @@@")


if __name__ == "__main__":
    banco = Banco()
    banco.executar()
