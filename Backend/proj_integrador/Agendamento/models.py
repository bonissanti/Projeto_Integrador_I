from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    duration = models.IntegerField(help_text="Duração em minutos")

    def __str__(self):
        return self.name
class Appointment(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Agendado'),
        ('completed', 'Concluído'),
        ('canceled', 'Cancelado'),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    google_event_id = models.CharField(max_length=255, blank=True, null=True)

class AppointmentxService(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    applied_price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"{self.appointment.customer.name} - {self.service.name} at {self.appointment.date} {self.appointment.time}"
