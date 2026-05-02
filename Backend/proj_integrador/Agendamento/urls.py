from django.urls import path
from Usuario import views

urlpatterns = [
    path('agendamento/', views.agendamento, name='agendamento'),
]