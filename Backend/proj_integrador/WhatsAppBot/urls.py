from django.urls import path
from . import views

urlpatterns = [
    path('webhook', views.verificar_webhook, name='verificar_webhook'),
    path('webhook', views.processar_webhook, name='processar_webhook'),
]