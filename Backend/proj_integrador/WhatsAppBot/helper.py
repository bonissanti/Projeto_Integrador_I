from dataclasses import dataclass, field

from Backend.proj_integrador.WhatsAppBot.enum import Status


class MensagemBOT:
    SOLICITAR_CPF = "Olá! Obrigada pelo seu contato! Para darmos andamento em nosso serviço, por favor, preciso que me informe seu CPF:"
    CPF_INVALIDO = "CPF inválido. Por favor, tente novamente:"
    CPF_NAO_CADASTRADO = "Você não possui cadastro. Gostaria de criar uma conta?\n1 - Sim\n2 - Não"
    SOLICITAR_DADOS_CADASTRO = "Por favor, informe:\n- Nome completo\n- Telefone"
    MENU_PRINCIPAL = "O que deseja fazer?\n1 - Agendar\n2 - Cancelar agendamento\n3 - Consultar agendamentos"
    OPCAO_INVALIDA = "Opção inválida. Por favor, escolha uma das opções disponíveis."
    AGENDAMENTO_CONFIRMADO = "Agendamento confirmado! ✅"
    CANCELAMENTO_CONFIRMADO = "Agendamento cancelado! ✅"
    SEM_AGENDAMENTOS = "Você não possui agendamentos."

    @staticmethod
    def datas_disponiveis(datas: list) -> str:
        lista = "\n".join(f"{i + 1} - {d}" for i, d in enumerate(datas))
        return f"Estas são minhas datas disponíveis nos próximos 30 dias:\n{lista}\n\nEscolha uma opção:"

    @staticmethod
    def confirmar_agendamento(data, horario) -> str:
        return f"Confirmar agendamento?\n📅 {data} às {horario}\n\n1 - Sim\n2 - Não"

    @staticmethod
    def listar_agendamentos(agendamentos: list) -> str:
        if not agendamentos:
            return MensagemBOT.SEM_AGENDAMENTOS
        lista = "\n".join(f"{i+1} - {a['data']} às {a['horario']}" for i, a in enumerate(agendamentos))
        return f"Seus agendamentos:\n{lista}"

    @staticmethod
    def confirmar_cancelamento(agendamento) -> str:
        return f"Cancelar este agendamento?\n📅 {agendamento['data']} às {agendamento['horario']}\n\n1 - Sim\n2 - Não"


@dataclass
class Conversation:
    state: Status = Status.IDLE
    data: dict = field(default_factory=dict)

conversations: dict[str, Conversation] = {}