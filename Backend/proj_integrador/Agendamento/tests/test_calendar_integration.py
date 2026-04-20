from datetime import datetime, timedelta
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from Agendamento.models import Appointment, Customer


class IntegracaoCalendarTest(TestCase):
    def setUp(self):
        self.cliente = Customer.objects.create(
            name="Cliente de Teste",
            email="teste@example.com",
            phone="11988887777",
        )

    def _futuro(self, hora=14):
        base = datetime.now() + timedelta(days=2)
        return timezone.make_aware(base.replace(hour=hora, minute=0, second=0, microsecond=0))

    @patch('Agendamento.calendar_utils.criar_evento_google_calendar')
    def test_agendamento_confirmado_chama_google_calendar(self, mock_google_calendar):
        mock_google_calendar.return_value = 'id_falso_do_google_123'

        agendamento = Appointment(
            customer=self.cliente,
            scheduled_at=self._futuro(14),
            status='scheduled',
        )
        agendamento.save()

        mock_google_calendar.assert_called_once_with(agendamento)
        self.assertEqual(agendamento.google_event_id, 'id_falso_do_google_123')

    @patch('Agendamento.calendar_utils.criar_evento_google_calendar')
    def test_agendamento_cancelado_nao_chama_google(self, mock_google_calendar):
        agendamento = Appointment(
            customer=self.cliente,
            scheduled_at=self._futuro(15),
            status='canceled',
        )
        agendamento.save()

        mock_google_calendar.assert_not_called()
