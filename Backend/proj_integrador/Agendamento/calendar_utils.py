import logging
import os
from datetime import timedelta

from django.conf import settings
from google.oauth2 import service_account
from googleapiclient.discovery import build

logger = logging.getLogger(__name__)

CREDENTIALS_FILE = os.path.join(settings.BASE_DIR, 'calendar_credentials.json')
CALENDAR_ID = 'agendatrancistabot@gmail.com'
TEMPO_PROCEDIMENTO = 2  # TODO: puxar da tabela Service


def criar_evento_google_calendar(agendamento):
    """Cria evento no Google Calendar a partir de um Appointment. Retorna o ID do evento ou None."""
    if not os.path.exists(CREDENTIALS_FILE):
        logger.warning(
            "calendar_credentials.json não encontrado em %s. Pulei integração com Google Calendar.",
            CREDENTIALS_FILE,
        )
        return None

    try:
        credentials = service_account.Credentials.from_service_account_file(
            CREDENTIALS_FILE,
            scopes=['https://www.googleapis.com/auth/calendar'],
        )
        service = build('calendar', 'v3', credentials=credentials)
    except Exception:
        logger.exception("Falha ao inicializar cliente do Google Calendar.")
        return None

    inicio = agendamento.scheduled_at
    fim = inicio + timedelta(hours=TEMPO_PROCEDIMENTO)

    event_data = {
        'summary': f'Trança - {agendamento.customer.name}',
        'description': f'Telefone: {agendamento.customer.phone}\nServiço agendado via Bot.',
        'start': {'dateTime': inicio.isoformat(), 'timeZone': 'America/Sao_Paulo'},
        'end': {'dateTime': fim.isoformat(), 'timeZone': 'America/Sao_Paulo'},
    }

    try:
        evento_criado = service.events().insert(calendarId=CALENDAR_ID, body=event_data).execute()
        logger.info("Evento Google Calendar criado com ID: %s", evento_criado.get('id'))
        return evento_criado.get('id')
    except Exception:
        logger.exception("Erro ao criar evento no Google Calendar.")
        return None
