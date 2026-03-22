from enum import Enum

class Status(str, Enum):
    IDLE = 'idle'
    AGUARDANDO_CPF = 'solicitar_cpf'
    AGUARDANDO_OPCAO_MENU = 'aguardando_opcao'
    AGUARDANDO_DATA = 'aguardando_data'
    AGUARDANDO_HORA = 'aguardando_hora'
    AGUARDANDO_CONFIRMACAO = 'aguardando_confirmacao'