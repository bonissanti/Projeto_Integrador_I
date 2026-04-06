from datetime import datetime
from django.db import models
from Agendamento.models import Appointment, Customer, AppointmentxService, Service


class AppointmentsManager(models.Manager[Appointment]):
    def buscar_agendamentos_disponiveis_no_periodo(self, total_dias: int = 20) -> list[datetime]:
        hoje = datetime.now()

        if hoje.hour >= 10:
            data_inicio = hoje + datetime.timedelta(days=1)
        else:
            data_inicio = hoje

        data_final = data_inicio + datetime.timedelta(days=total_dias)

        dias_ocupados = Appointment.objects.filter(
            date__range=[data_inicio, data_final],
        ).values_list('date', flat=True).distinct()

        possiveis_dias = [data_inicio + datetime.timedelta(days=i) for i in range(total_dias)]
        dias_disponiveis = [dia for dia in possiveis_dias if dia not in dias_ocupados]
        return dias_disponiveis

    def buscar_agendamentos_por_numero_telefone(self, numero_telefone: str) -> list['Appointment']:
        query = Appointment.objects.filter(customer__phone=numero_telefone)
        return list(query)

    def marcar_agendamento(self, customer: Customer, date: datetime, time: datetime.time, services: list[Service]) -> 'Appointment':
        appointment = Appointment.objects.create(
            customer=customer,
            date=date,
            time=time,
            status='scheduled'
        )

        for service in services:
            AppointmentxService.objects.create(
                appointment=appointment,
                service=service,
                applied_price=service.price
            )

        return appointment

    def cancelar_agendamento(self, appointment: Appointment) -> Appointment:
        appointment.status = 'cancelled'
        appointment.save(update_fields=['status'])
        return appointment

    def checar_se_data_esta_em_uso(self, agendamento: Appointment) -> bool:
        return Appointment.objects.filter(date=agendamento.date, status='scheduled').exists()


class CustomerManager(models.Manager[Customer]):
    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)

    def checar_se_usuario_existe_por_telefone(self, numero_telefone: str) -> bool:
        return Customer.objects.filter(phone=numero_telefone).exists()

    def cadastrar_usuario(self, nome: str, email: str, numero_telefone: str) -> 'Customer':
        return Customer.objects.create(name=nome, email=email, phone=numero_telefone)

    def editar_usuario(self, numero_telefone_atual: str, nome: str | None, email: str | None, novo_numero_telefone: str | None) -> int:
        return Customer.objects.filter(phone=numero_telefone_atual).update(name=nome, email=email, phone=novo_numero_telefone)

    def deletar_usuario(self, numero_telefone: str) -> int:
        linhas_alteradas = Customer.objects.filter(phone=numero_telefone).update(deleted=True)
        return linhas_alteradas > 0

    def buscar_usuario_por_telefone(self, numero_telefone: str) -> Customer | None:
        return Customer.objects.filter(phone=numero_telefone).first()

    def buscar_usuarios_nao_deletados(self) -> list[Customer]:
        return Customer.objects.filter(deleted=False)

