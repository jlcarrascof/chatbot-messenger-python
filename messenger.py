import requests
import os
from dotenv import load_dotenv

load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GRAPH_API_URL = "https://graph.facebook.com/v18.0/me/messages"

def send_text_message(recipient_id, text):
    """
    Envía un mensaje de texto simple a un usuario de Messenger.
    
    Args:
        recipient_id: El sender.id del usuario al que responderemos
        text: El texto del mensaje a enviar
    """
    payload = {
        "recipient": {"id": recipient_id},
        "message":   {"text": text}
    }

    response = requests.post(
        url=GRAPH_API_URL,
        params={"access_token": PAGE_ACCESS_TOKEN},
        json=payload
    )

    if response.status_code != 200:
        print(f"Error enviando mensaje: {response.status_code} - {response.text}")
    else:
        print(f"Mensaje enviado a {recipient_id}: {text}")

    return response