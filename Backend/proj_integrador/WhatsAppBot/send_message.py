import os
import requests
from http.client import responses

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')

def enviar_mensagem(to, message, phone_number_id):
    url = f"https://graph.facebook.com/v22.0/{phone_number_id}/messages"

    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        print("Mensagem enviada com sucesso!")
    else:
        print(f"Erro ao enviar mensagem para {to}. Resposta do servidor: {response.text} ({response.status_code})")