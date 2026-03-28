import datetime
import random
from typing import List

from Backend.proj_integrador.WhatsAppBot.enum import LocalAtendimento


def buscarAgendamentosDisponiveisNoPeriodoMock(total_dias: int)-> List[datetime]:
    disponiveis = []
    hoje = datetime.date.today()

    for i in range(total_dias):
        data_atual = hoje + datetime.timedelta(days=i)

        if random.choice([True, False]):
            agendamento = {
                "data": data_atual.strftime("%d/%m/%Y"),
                "horario": "10:00",
                "local": random.choice(list(LocalAtendimento)),
            }
            disponiveis.append(agendamento)
    return disponiveis


def checarSeUsuarioExistePorCPFMock(cpfUsuario: str):
    return random.choice([True, False])

def buscarAgendamentosPorCPFMock(cpf: str) -> List[datetime]:
    agendamentoDoUsuario = []
    hoje = datetime.date.today()
    agendamentosMarcados = random.randint(1, 3)

    for i in range(agendamentosMarcados):
        data_atual = hoje + datetime.timedelta(days=i)

        if random.choice([True, False]):
            agendamento = {
                "data": data_atual.strftime("%d/%m/%Y"),
                "horario": "10:00",
                "local": random.choice(list(LocalAtendimento)),
            }
            agendamentoDoUsuario.append(agendamento)
    return agendamentoDoUsuario
