from .send_message import enviar_mensagem

def processar_mensagem(message, from_phone_number, to_phone_number):
    print(f"Mensagem recebida: {message}")
    print(f"ID do número de telefone: {from_phone_number}")

    message_type = message.get("type")

    if message_type == "text":
        mensagem_texto = message.get("text", {}).get("body")

        print(f"Mensagem de texto: {mensagem_texto} recebida de {to_phone_number}")

        enviar_mensagem(to_phone_number, "Tu vai apanhar em Cálculo II", from_phone_number)
