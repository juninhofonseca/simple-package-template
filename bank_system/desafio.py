import textwrap
from datetime import datetime
from abc import abstractmethod, ABC


class Transacao(ABC):

    @property
    @abstractmethod
    def valor(self):
        pass

    @property
    @abstractmethod
    def data(self):
        pass

    @abstractmethod
    def registrar(self, conta):
        pass


class Deposito(Transacao):
    @property
    def valor(self):
        return self._valor

    @property
    def data(self):
        return self._data

    def __init__(self, valor):
        self._valor = valor
        self._data = datetime.now()

    def registrar(self, conta):
        conta._saldo += self._valor
        conta._historico.append(
            f"Depósito de R$ {self._valor} em {self._data.strftime('%d/%m/%Y %H:%M:%S')}")


class Historico:
    def __init__(self):
        self._transacoes = []

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def obter_extrato(self):
        return self._transacoes


class cliente:
    def __init__(self, endereco):
        self._endereco = endereco
        self._contas = []

    @property
    def contas(self):
        return self._contas

    @property
    def endereco(self):
        return self._endereco

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)
        conta._historico.append(transacao)

    def adicionar_conta(self, conta):
        self._contas.append(conta)


class PessoaFisica(cliente):
    def __init__(self, nome, cpf, data_nascimento, endereco):
        super().__init__(endereco)
        self._nome = nome
        self._cpf = cpf
        self._data_nascimento = data_nascimento
        self._contas = []

    @property
    def nome(self):
        return self._nome

    @property
    def cpf(self):
        return self._cpf

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def __str__(self):
        return f"Nome: {self._nome}, CPF: {self._cpf}, Data de Nascimento: {self._data_nascimento}, Endereço: {self._endereco}"


class Conta:
    def __init__(self, saldo, numero, agencia, cliente, historico=None):
        self._saldo = saldo
        self._numero = numero
        self._agencia = agencia
        self._cliente = cliente
        self._historico = historico

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    @classmethod
    def nova_conta(self, cliente, numero, agencia):
        return self(0, numero, agencia, cliente, historico=Historico())

    def sacar(self, valor):

        return True

    def depositar(self):
        return True


class ContaCorrente(Conta):
    def __init__(self, saldo, numero, agencia, cliente, historico, limite=500, limite_saques=3):
        super().__init__(saldo, numero, agencia, cliente, historico)
        self._limite = limite
        self._limite_saques = limite_saques
        self._numero_saques = 0

    def sacar(self, valor):
        if self._numero_saques >= self._limite_saques:
            print("Limite de saques atingido.")
            return False
        if valor > self._saldo:
            print("Saldo insuficiente.")
            return False
        self._saldo -= valor
        self._historico.adicionar_transacao(f"Saque de R$ {valor:.2f}")
        self._numero_saques += 1
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Valor de depósito inválido.")
            return False
        self._saldo += valor
        self._historico.adicionar_transacao(f"Depósito de R$ {valor:.2f}")
        return True


def listar_contas(lista_contas):
    print("Listar contas")
    for conta in lista_contas:
        print(f"""Agência: {conta['agencia']}
Número da conta: {conta['numero']}
Titular: {conta['cliente']['nome']}""")
        print("==========================================")


def cadastrar_cliente(nome, cpf, data_nascimento, endereco, lista_clientes):
    if not obter_cliente(cpf, lista_clientes):
        return PessoaFisica(nome, cpf, data_nascimento, endereco)


def obter_cliente(cpf, lista_clientes):
    for cliente in lista_clientes:
        if cliente.cpf == cpf:
            return cliente
    return None


def criar_conta(agencia, numero, cliente):
    return ContaCorrente.nova_conta(cliente=cliente, numero=numero, agencia=agencia)


def obter_conta(agencia, numero, lista_contas):
    for conta in lista_contas:
        if conta.agencia == agencia and conta.numero == numero:
            return conta


def validar_conta(lista_contas):
    agencia = input("Informe a agência:  ")
    numero = int(input("Informe o Número da Conta:  "))
    conta = obter_conta(agencia, numero, lista_contas)

    if not conta:
        print("Conta não encontrada.")
        return None
    return conta


def deposito(valor, saldo, extrato, /):  # deprecate
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo
    saldo += valor
    extrato += f"Depósito: R$ {valor:.2f}\n"
    print(f"Depósito realizado com sucesso.")
    print(extrato)
    return saldo, extrato


# def saque(*, saldo, valor, extrato, limite, numero_saques, LIMITE_SAQUES):
    if numero_saques >= LIMITE_SAQUES:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, numero_saques, extrato
    if valor <= 0:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, numero_saques, extrato
    if valor > saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, numero_saques, extrato
    if valor > limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, numero_saques, extrato

    saldo -= valor
    numero_saques += 1
    extrato += f"Saque: R$ {valor:.2f}\n"
    print(
        f"Saque realizado com sucesso. Número de saques hoje: {numero_saques}/{LIMITE_SAQUES}")
    print(extrato)
    return saldo, numero_saques, extrato


def obter_extrato(saldo, /, *, extrato):  # deprecate
    global EXTRATO_PADRAO
    print("Não foram realizadas movimentações." if extrato ==
          EXTRATO_PADRAO else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


def menu():
    menu = """\n
================ MENU ================
[1]\tDepositar
[2]\tSacar
[3]\tExtrato
[4]\tCadastrar Cliente
[5]\tCriar uma Conta
[6]\tListar Clientes
[7]\tListar Contas

[0]\tSair
=> """
    return input(textwrap.dedent(menu))


def main():
    # saldo = 0
    # limite = 500
    # extrato = EXTRATO_PADRAO
    # numero_saques = 0
    # LIMITE_SAQUES = 3
    lista_clientes = []
    lista_contas = []

    while True:

        opcao = menu()

        if opcao == "1":  # Depósito
            conta = validar_conta(lista_contas)
            if not conta:
                continue
            valor = float(input("Informe o valor do depósito: "))
            if conta.depositar(valor):
                print("Depósito realizado com sucesso!")
            else:
                print("Falha ao realizar depósito.")

        elif opcao == "2":  # Saque
            conta = validar_conta(lista_contas)
            if not conta:
                continue

            valor = float(input("Informe o valor do saque: "))
            if conta.sacar(valor):
                print("Saque realizado com sucesso!")
            else:
                print("Falha ao realizar saque.")
        elif opcao == "3":  # Extrato
            conta = validar_conta(lista_contas)
            if not conta:
                continue
            print("Extrato:")
            for transacao in conta.historico.obter_extrato():
                print(transacao)
            print(f"Saldo atual: R$ {conta.saldo:.2f}")
        elif opcao == "4":  # Cadastrar Cliente
            cpf = int(input("Informe o CPF do cliente: "))
            if obter_cliente(cpf, lista_clientes):
                print("Já existe um cliente com esse CPF!")
                continue
            cliente = cadastrar_cliente(
                nome=input("Informe o nome: "),
                cpf=cpf,
                data_nascimento=input("Informe a data de nascimento: "),
                endereco=input("Informe o endereço: "),
                lista_clientes=lista_clientes)                    
            if cliente:
                lista_clientes.append(cliente)
                print("Cliente criado com sucesso!")
        elif opcao == "5":  # Criar Conta
            numero = len(lista_contas) + 1
            agencia = "0001"
            cpf = int(input("Informe o CPF do cliente: "))
            cliente = obter_cliente(cpf, lista_clientes)
            if cliente:
                conta = criar_conta(agencia, numero, cliente)
                if conta:
                    lista_contas.append(conta)
                    cliente.adicionar_conta(conta)
                print("Conta criada com sucesso!")
            else:
                print("Cliente não encontrado, por favor verifique o CPF informado.")
        elif opcao == "6":  # Listar Clientes
            print("\n================ LISTA DE CLIENTES ================")
            for cliente in lista_clientes:
                for clientes in lista_clientes:
                    print(
                        f"Nome: {cliente.nome}\tCPF: {cliente.cpf}\tData de Nascimento: {cliente.data_nascimento}\tEndereço: {cliente.endereco}"
                    )
            print("================================================")
        elif opcao == "7":  # Listar Contas
            print("\n================ LISTA DE CONTAS ================")
            for conta in lista_contas:
                print(
                    f"Agência: {conta.agencia}\tC/C: {conta.numero}\tTitular: {conta.cliente.nome}\tSaldo: R$ {conta.saldo:.2f}")
            print("================================================")
        elif opcao == "0":  # Sair
            print("Obrigado por usar nosso sistema bancário!")
            break
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")


if __name__ == "__main__":
    main()

