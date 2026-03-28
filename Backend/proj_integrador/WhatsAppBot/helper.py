from dataclasses import dataclass, field

from Backend.proj_integrador.WhatsAppBot.enum import Status

class MensagemBOT:
    SOLICITAR_CPF = "Olá! Obrigada pelo seu contato! Para darmos andamento em nosso serviço, por favor, preciso que me informe seu CPF:"
    CPF_INVALIDO = "CPF inválido. Por favor, tente novamente:"
    CPF_NAO_CADASTRADO = "Você não possui cadastro. Gostaria de criar uma conta?\nDigite um dos valores abaixo:\n\n1 - Sim\n2 - Não"
    SOLICITAR_DADOS_CADASTRO = "Por favor, informe:\n- Nome completo\n- Telefone"
    MENU_PRINCIPAL = "O que deseja fazer?\nDigite um dos valores abaixo:\n\n1 - Agendar\n2 - Cancelar agendamento\n3 - Consultar agendamentos\n4 - Sair"
    OPCAO_INVALIDA = "Opção inválida. Por favor, escolha uma das opções disponíveis."
    LOCAL_ATENDIMENTO = "Em qual local deseja ser atendido(a)?\nDigite um dos valores abaixo:\n\n1 - Em minha residência (preço: R$YYY)\n2 - Em outro local (preço: R$XXX)"
    AGENDAMENTO_CONFIRMADO = "Agendamento confirmado! ✅"
    CANCELAMENTO_CONFIRMADO = "Agendamento cancelado! ✅"
    CANCELAMENTO_ABORTADO = "Cancelamento abortado! ✅"
    SAIR = "OK! Operação cancelada! Caso deseje iniciar uma nova conversa posteriormente, digite 'Oi' para reiniciarmos 😀"
    SEM_AGENDAMENTOS = "Você não possui agendamentos."
    IDLE = "Deseja fazer algo mais?\n1 - Agendar\n2 - Cancelar agendamento\n3 - Consultar agendamentos\n4 - Sair"

    @staticmethod
    def informarDatasDisponiveis(datas: list) -> str:
        lista = "\n".join(f"{i + 1} - {d}" for i, d in enumerate(datas))
        return f"Estas são minhas datas disponíveis nos próximos 20 dias:\n{lista}\n\nEscolha uma opção:"

    @staticmethod
    def confirmar_agendamento(nome, data, horario, local_atendimento) -> str:
        return f"Ok, {nome}, posso confirmar o agendamento para:\n\n📅 {data} às {horario}\n🏠 Local: {local_atendimento}\n\n1 - Sim\n2 - Não"

    @staticmethod
    def listar_agendamentos(agendamentos: list) -> str:
        if not agendamentos:
            return MensagemBOT.SEM_AGENDAMENTOS
        lista = "\n".join(f"{i+1} - {a['data']} às {a['horario']}" for i, a in enumerate(agendamentos))
        return f"Seus agendamentos:\n{lista}"

    @staticmethod
    def selecionar_agendamento(agendamentos: list) -> str:
        if not agendamentos:
            return MensagemBOT.SEM_AGENDAMENTOS
        lista = "\n".join(f"{i+1} - {a['data']} às {a['horario']}" for i, a in enumerate(agendamentos))
        return f"Qual agendamento deseja cancelar?\n{lista}"

    @staticmethod
    def confirmar_cancelamento(agendamento) -> str:
        return f"Cancelar este agendamento?\n📅 {agendamento['data']} às {agendamento['horario']}\n\n1 - Sim\n2 - Não"

    @staticmethod
    def criar_conta_com_cpf_informado_previamente(cpf: str) -> str:
        return f"Deseja criar uma conta com o CPF {cpf}, informado anteriormente?"


@dataclass
class Conversation:
    state: Status = Status.IDLE
    data: dict = field(default_factory=dict)

conversations: dict[str, Conversation] = {}