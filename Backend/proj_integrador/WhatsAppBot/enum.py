from enum import Enum

class Status(str, Enum):
    SAIR = "Sair"
    INICIAL = "inicial"
    IDLE = "idle"
    VALIDANDO_USUARIO = "solicitar_cpf"
    SOLICITACAO_PARA_CRIAR_CONTA = "criando_conta"
    AGUARDANDO_OPCAO_MENU = "aguardando_opcao"
    DEFININDO_DATA = "agendamento"
    CANCELAMENTO = "cancelamento"
    CONFIRMANDO_AGENDAMENTO = "confirmando_agendamento"
    CONFIRMANDO_CANCELAMENTO = "aguardando_cancelamento"

class LocalAtendimento(str, Enum):
    A_DOMICILIO = "A Domicílio"
    SALAO = "No Salão"