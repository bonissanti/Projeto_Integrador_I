import json

from django.shortcuts import render

# Create your views here.
def get_request_data(request):
    if request.method == 'POST':
        return request.POST
    try:
        return json.loads(request.body)
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON")
        return None


@csrf_exempt
def agendamento(request):
