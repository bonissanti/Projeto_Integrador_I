def processar_mensagem(message, phone_number_id):
    print(f"Mensagem recebida: {message}")
    print(f"ID do número de telefone: {phone_number_id}")

    message_type = message.get("type")

    if message_type == "text":
        mensagem_texto = message.get("text", {}).get("body")
        from_number = message.get("from")

        print(f"Mensagem de texto: {mensagem_texto} recebida de {from_number}")

        enviar_mensagem(phone_number_id, from_number, "Tu vai apanhar em Cálculo II")
