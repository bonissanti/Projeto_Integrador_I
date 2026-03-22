from enum import Enum

class Status(str, Enum):
    INICIAL = 'inicial'
    IDLE = 'idle'
    VALIDANDO_USUARIO = 'solicitar_cpf'
    SOLICITACAO_PARA_CRIAR_CONTA = 'criando_conta'
    AGUARDANDO_OPCAO_MENU = 'aguardando_opcao'
    AGENDAMENTO = 'agendamento'
    CANCELAMENTO = 'cancelamento'
    CONFIRMANDO_AGENDAMENTO = 'confirmando_agendamento'
    CONFIRMANDO_CANCELAMENTO = 'aguardando_cancelamento'