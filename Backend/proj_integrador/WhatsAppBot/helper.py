from dataclasses import dataclass, field
from xmlrpc.client import DateTime

from Agendamento.models import Appointment
from .bot_enums import Status

class MensagemBOT:
    DATA_EM_USO = "Opa, esta data já está ocupada, por favor, informe uma outra opção."
    BOAS_VINDAS = "Olá, obrigada pelo seu contato. Por favor, para prosseguirmos, informe seu nome e sobrenome 🙂"
    INFORMAR_ENDERECO = "Por favor, informe seu endereço com Rua, Número, complemento (se houver), CEP e bairro:"
    NUMERO_NAO_CADASTRADO = "Você não possui cadastro. Gostaria de criar uma conta?\nDigite um dos valores abaixo:\n\n1 - Sim\n2 - Não"
    SOLICITAR_DADOS_CADASTRO = "Por favor, informe o seu email\n"
    MENU_PRINCIPAL = "O que deseja fazer?\nDigite um dos valores abaixo:\n\n1 - Agendar\n2 - Cancelar agendamento\n3 - Consultar agendamentos\n4 - Sair"
    OPCAO_INVALIDA = "Opção inválida. Por favor, escolha uma das opções disponíveis."
    EMAIL_INVALIDO = "Opa, parece que o email informado não é válido, revise e tente novamente!"
    NOME_NAO_INFORMADO = "Opa! Esse nome me parece incorreto, por favor, informe seu nome novamente."
    LOCAL_ATENDIMENTO = "Em qual local deseja ser atendido(a)?\nDigite um dos valores abaixo:\n\n1 - Em sua residência (preço: R$YYY)\n2 - Em meu salão (preço: R$XXX)"
    AGENDAMENTO_CONFIRMADO = "Agendamento confirmado! ✅\n"
    CANCELAMENTO_CONFIRMADO = "Agendamento cancelado! ❌"
    CANCELAMENTO_ABORTADO = "Cancelamento abortado! ✅"
    SAIR = "OK! Operação cancelada! Caso deseje iniciar uma nova conversa posteriormente, digite 'Oi' para reiniciarmos 😀"
    SEM_AGENDAMENTOS = "Você não possui agendamentos."
    IDLE = "Deseja fazer algo mais?\n1 - Agendar\n2 - Cancelar agendamento\n3 - Consultar agendamentos\n4 - Sair"

    @staticmethod
    def informarDatasDisponiveis(datas: list[dict]) -> str:
        lista = "\n".join(
            f"{i + 1} - {d['data']} às {d['horario']}"
            for i, d in enumerate(datas)
        )
        return f"Estas são minhas datas disponíveis nos próximos 20 dias:\n{lista}\n\nEscolha uma opção:"

    @staticmethod
    def confirmar_agendamento(nome: str, agendamento: dict, endereco: str) -> str:
        return f"Ok, {nome}, posso confirmar o agendamento para:\n\n📅 {agendamento['data']} às {agendamento['horario']}\n🏠 Local: {endereco}\n\n1 - Sim\n2 - Não"

    @staticmethod
    def listar_agendamentos(agendamentos: list[Appointment]) -> str:
        if not agendamentos:
            return MensagemBOT.SEM_AGENDAMENTOS
        lista = "\n".join(f"{i+1} - {a.date} às {a.time}" for i, a in enumerate(agendamentos))
        return f"Seus agendamentos:\n{lista}"

    @staticmethod
    def selecionar_agendamento(agendamentos: list[Appointment]) -> str:
        if not agendamentos:
            return MensagemBOT.SEM_AGENDAMENTOS
        lista = "\n".join(f"{i+1} - {a.date} às {a.time}" for i, a in enumerate(agendamentos))
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