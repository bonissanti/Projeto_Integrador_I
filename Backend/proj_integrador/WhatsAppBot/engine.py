from .helper import MensagemBOT, Conversation
from .enum import Status
from .send_message import enviar_mensagem

conversations = {}

def processar_mensagem(mensagemDoUsuario: str, bot_telefone: str, usuario_telefone: str):
    if usuario_telefone not in conversations:
        conversations[usuario_telefone] = {
            'state': Status.IDLE,
            'data': {}
        }

    conv = conversations[usuario_telefone]

    match conv["state"]:
        case Status.IDLE:
            enviar_mensagem(usuario_telefone, MensagemBOT.SOLICITAR_CPF, bot_telefone)
            set_state(usuario_telefone, Status.AGUARDANDO_CPF)

        case Status.AGUARDANDO_CPF:
            cpfValido: bool = validarCPF(mensagemDoUsuario)

            if not cpfValido:
                enviar_mensagem(usuario_telefone, MensagemBOT.CPF_INVALIDO, bot_telefone)
                set_state(usuario_telefone, Status.C)

            usuarioExiste: bool = checarSeUsuarioExistePorCPF(mensagemDoUsuario)

            if usuarioExiste:
                enviar_mensagem(usuario_telefone, MensagemBOT.MENU_PRINCIPAL, bot_telefone)
                set_state(usuario_telefone, Status.AGUARDANDO_OPCAO_MENU)

            else:
                enviar_mensagem(usuario_telefone, MensagemBOT.CPF_NAO_CADASTRADO, bot_telefone)
                set_state(usuario_telefone, Status.AGUARDANDO_CPF)





def get_conversation(phone: str) -> Conversation:
    if phone not in conversations:
        conversations[phone] = Conversation()
    return conversations[phone]

def set_state(phone: str, new_state: Status):
    conv = get_conversation(phone)
    conv.state = new_state