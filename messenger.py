import requests
import os
from dotenv import load_dotenv

load_dotenv()

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
GRAPH_API_URL = "https://graph.facebook.com/v18.0/me/messages"

def send_text_message(recipient_id, text):
    """
    Sends a plain text message to a Messenger user.

    Args:
        recipient_id: The sender.id of the user to reply to
        text: The text content of the message to send
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
        print(f"Error sending message: {response.status_code} - {response.text}")
    else:
        print(f"Message sent to {recipient_id}: {text}")

    return response 

def send_buttons_message(recipient_id, text, buttons):
    """
    Sends a template message with postback buttons to a Messenger user.

    Args:
        recipient_id: The sender.id of the user to reply to
        text: Text to display above the buttons (max 640 characters)
        buttons: A list of dicts representing the buttons (max 3 buttons)
    """
    payload = {
        "recipient": {"id": recipient_id},
        "message": {
            "attachment": {
                "type": "template",
                "payload": {
                    "template_type": "button",
                    "text": text,
                    "buttons": buttons
                }
            }
        }
    }

    response = requests.post(
        url=GRAPH_API_URL,
        params={"access_token": PAGE_ACCESS_TOKEN},
        json=payload
    )

    if response.status_code != 200:
        print(f"Error sending buttons message: {response.status_code} - {response.text}")
    else:
        print(f"Buttons message sent to {recipient_id}")

    return response
