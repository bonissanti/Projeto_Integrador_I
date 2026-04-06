from Agendamento.models import Appointment
from WhatsAppBot.engine import set_state
from WhatsAppBot.enum import Status
from WhatsAppBot.helper import MensagemBOT, Conversation
from WhatsAppBot.send_message import enviar_mensagem

FILLERS = [
    'meu nome é',
    'me chamo',
    'pode me chamar de',
    'sou o',
    'sou a',
    'sou',
    'olá',
    'oi',
]

def extrair_nome(texto: str) -> str | None:
    for filler in FILLERS:
        texto = texto.replace(filler, '').strip()

    nome = texto.strip().title()
    palavras = nome.split()

    if len(palavras) == 0 or len(palavras) > 5:
        return None
    if any(char.isdigit() for char in nome):
        return None


def opcao_cancelar(conv: Conversation, usuario_telefone: str, bot_telefone: str, mensagem_do_usuario: str) -> None:
    agendamentos_do_usuario: list[Appointment] = Appointment.objects.buscar_agendamentos_por_numero_telefone(
        mensagem_do_usuario)

    if not agendamentos_do_usuario:
        enviar_mensagem(usuario_telefone, MensagemBOT.SEM_AGENDAMENTOS, bot_telefone)
        return

    msg = MensagemBOT.selecionar_agendamento(agendamentos_do_usuario)

    enviar_mensagem(usuario_telefone, msg, bot_telefone)
    conv.data["agendamentos"] = agendamentos_do_usuario
    set_state(usuario_telefone, Status.CANCELAMENTO)


def opcao_consultar(usuario_telefone: str, bot_telefone: str, mensagem_do_usuario: str) -> None:
    agendamentos_do_usuario: list[Appointment] = Appointment.objects.buscar_agendamentos_por_numero_telefone(mensagem_do_usuario)
    enviar_mensagem(usuario_telefone, MensagemBOT.listar_agendamentos(agendamentos_do_usuario), bot_telefone)
    set_state(usuario_telefone, Status.IDLE)


def opcao_agendar(conv: Conversation, usuario_telefone: str, bot_telefone: str, mensagem_do_usuario: str) -> None:
    agendamentos = conv.data["agendamento"].datas_disponiveis
    datas_disponiveis = MensagemBOT.informarDatasDisponiveis(agendamentos)
    enviar_mensagem(usuario_telefone, datas_disponiveis, bot_telefone)
    set_state(usuario_telefone, Status.DEFININDO_DATA)


def opcao_sair(conv: Conversation, usuario_telefone: str, bot_telefone: str) -> None:
    conv.data.clear()
    enviar_mensagem(usuario_telefone, MensagemBOT.SAIR, bot_telefone)
    set_state(usuario_telefone, Status.IDLE)
