from typing import List

from .bot.dtos import UsuarioContextoDTO, AgendamentoDTO
from .helper import MensagemBOT, Conversation
from .enum import Status
from .send_message import enviar_mensagem

conversations = {}

def processar_mensagem(mensagemDoUsuario: str, bot_telefone: str, usuario_telefone: str):
    if usuario_telefone not in conversations:
        conversations[usuario_telefone] = {
            'state': Status.INICIAL,
            'usuario': UsuarioContextoDTO(wa_id=usuario_telefone),
            'agendamento': AgendamentoDTO(usuario_wa_id=usuario_telefone)
        }

    conv = conversations[usuario_telefone]
    agendamentos = buscarAgendamentosDisponiveisNoPeriodo(20)

    match conv["state"]:
        # case Status.IDLE:
        #     enviar_mensagem(usuario_telefone, MensagemBOT.IDLE, bot_telefone)
        #     gerenciar_menu_principal(usuario_telefone, bot_telefone, mensagemDoUsuario, agendamentos)
#
        case Status.INICIAL:
            gerenciar_status_inicial(usuario_telefone, bot_telefone)

        case Status.VALIDANDO_USUARIO:
            gerenciar_validacao_usuario(usuario_telefone, bot_telefone)

        case Status.SOLICITACAO_PARA_CRIAR_CONTA:
            gerenciar_solicitacao_para_criar_conta(usuario_telefone, bot_telefone)

#         case Status.AGUARDANDO_OPCAO_MENU:
#             gerenciar_menu_principal(usuario_telefone, bot_telefone, mensagemDoUsuario, agendamentos)
#
#         case Status.AGENDAMENTO:
#             gerenciar_agendamento(usuario_telefone, bot_telefone, mensagemDoUsuario, agendamentos)
#
#         case Status.CONFIRMANDO_AGENDAMENTO:
#             gerenciar_confirmacao_agendamento(usuario_telefone, bot_telefone, mensagemDoUsuario)
#
#         case Status.CANCELAMENTO:
#             gerenciar_cancelamento(usuario_telefone, bot_telefone, mensagemDoUsuario)
#
#         case Status.CONFIRMANDO_CANCELAMENTO:
#             gerenciar_confirmar_cancelamento(usuario_telefone, bot_telefone, mensagemDoUsuario)
#
#
def gerenciar_status_inicial(usuario_telefone: str, bot_telefone: str) -> None:
    enviar_mensagem(usuario_telefone, MensagemBOT.SOLICITAR_CPF, bot_telefone)
    set_state(usuario_telefone, Status.VALIDANDO_USUARIO)

def gerenciar_validacao_usuario(usuario_telefone: str, bot_telefone: str, mensagemDoUsuario: str) -> None:
    cpfValido: bool = validarCPF(mensagemDoUsuario)
    conv = get_conversation(usuario_telefone)

    if not cpfValido:
        enviar_mensagem(usuario_telefone, MensagemBOT.CPF_INVALIDO, bot_telefone)
        set_state(usuario_telefone, Status.VALIDANDO_USUARIO)

    usuarioExiste: bool = checarSeUsuarioExistePorCPF(mensagemDoUsuario)

    if usuarioExiste:
        enviar_mensagem(usuario_telefone, MensagemBOT.MENU_PRINCIPAL, bot_telefone)
        set_state(usuario_telefone, Status.AGUARDANDO_OPCAO_MENU)

    else:
        enviar_mensagem(usuario_telefone, MensagemBOT.CPF_NAO_CADASTRADO, bot_telefone)
        conv['usuario'].cpf = cpfValido
        set_state(usuario_telefone, Status.SOLICITACAO_PARA_CRIAR_CONTA)

def gerenciar_solicitacao_para_criar_conta(usuario_telefone: str, bot_telefone: str, mensagemDoUsuario: str) -> None:
    mensagem = mensagemDoUsuario.strip().lower()
    conv = get_conversation(usuario_telefone)

    if mensagem == "sim":
        enviar_mensagem(usuario_telefone, MensagemBOT.MENU_PRINCIPAL, bot_telefone)
        set_state(usuario_telefone, Status.AGUARDANDO_OPCAO_MENU)

    elif mensagem == "não":
        enviar_mensagem(usuario_telefone,MensagemBOT.SAIR_NAO_CRIOU_CONTA, bot_telefone)
        set_state(usuario_telefone, Status.INICIAL)



# def gerenciar_menu_principal(usuario_telefone: str, bot_telefone: str, mensagemDoUsuario: str, agendamentos: List[int]) -> None:
#             enviar_mensagem(usuario_telefone, MensagemBOT.MENU_PRINCIPAL, bot_telefone)
#
#             if mensagemDoUsuario == "1":
#                 datasDisponiveis = MensagemBOT.informarDatasDisponiveis(agendamentos)
#                 enviar_mensagem(usuario_telefone, datasDisponiveis, bot_telefone)
#                 set_state(usuario_telefone, Status.AGENDAMENTO)
#
#             elif mensagemDoUsuario == "2":
#                 agendamentosDoUsuario = buscarAgendamentosPorCPF(cpf)
#
#                 if not agendamentosDoUsuario:
#                     enviar_mensagem(usuario_telefone, MensagemBOT.SEM_AGENDAMENTOS, bot_telefone)
#                     return
#
#                 msg = MensagemBOT.selecionar_agendamento(agendamentosDoUsuario)
#                 enviar_mensagem(usuario_telefone, msg, bot_telefone)
#
#                 conv = get_conversation(usuario_telefone)
#                 conv.data["agendamentos"] = agendamentosDoUsuario
#
#                 set_state(usuario_telefone, Status.CANCELAMENTO)
#
#             elif mensagemDoUsuario == "3":
#                 agendamentosDoUsuario = buscarAgendamentosPorCPF(cpf)
#                 enviar_mensagem(usuario_telefone, MensagemBOT.listar_agendamentos(agendamentosDoUsuario), bot_telefone)
#                 set_state(usuario_telefone, Status.IDLE)
#
#             elif mensagemDoUsuario == "4":
#                 conv = get_conversation(usuario_telefone)
#
#                 conv.data.clear()
#                 enviar_mensagem(usuario_telefone,MensagemBOT.SAIR, bot_telefone)
#                 set_state(usuario_telefone, Status.IDLE)


#
# def gerenciar_agendamento(usuario_telefone: str, bot_telefone: str, mensagemDoUsuario: str, agendamentos: List[int]) -> None:
#     mensagem = mensagemDoUsuario.strip()
#
#     if not mensagem.isdigit():
#         enviar_mensagem(usuario_telefone, MensagemBOT.OPCAO_INVALIDA, bot_telefone)
#         return
#
#     indice = int(mensagem)
#
#     if indice < 1 or indice > 20:
#         enviar_mensagem(usuario_telefone, MensagemBOT.OPCAO_INVALIDA, bot_telefone)
#         return
#
#     if indice not in agendamentos:
#         enviar_mensagem(usuario_telefone, MensagemBOT.OPCAO_INVALIDA, bot_telefone)
#         return
#
#     data = agendamentos[indice]
#
#     conv = get_conversation(usuario_telefone)
#     conv.data["data"] = data
#
#     msg = MensagemBOT.confirmar_agendamento(data)
#     enviar_mensagem(usuario_telefone, msg, bot_telefone)
#
#     set_state(usuario_telefone, Status.CONFIRMANDO_AGENDAMENTO)
#
#
# def gerenciar_confirmacao_agendamento(usuario_telefone: str, bot_telefone: str, mensagemDoUsuario: str) -> None:
#     mensagem = mensagemDoUsuario.strip().lower()
#
#     conv = get_conversation(usuario_telefone)
#     data = conv.data.get("data")
#
#     if mensagem == "sim":
#         marcar_agendamento(data, hora, cpf, usuario_telefone)
#         enviar_mensagem(usuario_telefone, MensagemBOT.AGENDAMENTO_CONFIRMADO, bot_telefone)
#         set_state(usuario_telefone, Status.IDLE)
#
#     elif mensagem == "não":
#         enviar_mensagem(usuario_telefone, MensagemBOT.CANCELAMENTO_CONFIRMADO, bot_telefone)
#         set_state(usuario_telefone, Status.IDLE)
#
#     else:
#         enviar_mensagem(usuario_telefone,MensagemBOT.OPCAO_INVALIDA, bot_telefone)
#
#
# def gerenciar_cancelamento(usuario_telefone: str, bot_telefone: str, mensagemDoUsuario: str) -> None:
#     mensagem = mensagemDoUsuario.strip()
#
#     if not mensagem.isdigit():
#         enviar_mensagem(usuario_telefone, MensagemBOT.OPCAO_INVALIDA, bot_telefone)
#         return
#
#     indice = int(mensagem)
#
#     conv = get_conversation(usuario_telefone)
#     agendamentos = conv.data.get("agendamentos", [])
#
#     if indice < 1 or indice > len(agendamentos):
#         enviar_mensagem(usuario_telefone, MensagemBOT.OPCAO_INVALIDA, bot_telefone)
#         return
#
#     agendamento = agendamentos[indice - 1]
#     conv.data["agendamento_para_cancelar"] = agendamento
#
#     msg = MensagemBOT.confirmar_cancelamento(agendamento)
#     enviar_mensagem(usuario_telefone, msg, bot_telefone)
#     set_state(usuario_telefone, Status.CONFIRMANDO_CANCELAMENTO)
#
#
# def gerenciar_confirmar_cancelamento(usuario_telefone: str, bot_telefone: str, mensagemDoUsuario: str) -> None:
#     mensagem = mensagemDoUsuario.strip().lower()
#
#     conv = get_conversation(usuario_telefone)
#     agendamento = conv.data.get("agendamento_para_cancelar")
#
#     if mensagem == "sim":
#         MensagemBOT.cancelar_agendamento(agendamento)
#         enviar_mensagem(usuario_telefone, MensagemBOT.CANCELAMENTO_CONFIRMADO, bot_telefone)
#         set_state(usuario_telefone, Status.IDLE)
#
#     elif mensagem == "não":
#         enviar_mensagem(usuario_telefone, MensagemBOT.CANCELAMENTO_ABORTADO, bot_telefone)
#         set_state(usuario_telefone, Status.IDLE)
#
#     else:
#         enviar_mensagem(usuario_telefone,MensagemBOT.OPCAO_INVALIDA, bot_telefone)
#
# def reset_conversation(phone: str):
#     conv = get_conversation(phone)
#     conv.state = Status.IDLE
#     conv.data.clear()

def get_conversation(phone: str) -> Conversation:
    if phone not in conversations:
        conversations[phone] = Conversation()
    return conversations[phone]

def set_state(phone: str, new_state: Status):
    conv = get_conversation(phone)
    conv.state = new_state