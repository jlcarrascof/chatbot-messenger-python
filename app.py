from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os

# Carga las variables del archivo .env
load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "Bot activo ✓", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN and challenge:
        return challenge, 200
    return "Token inválido", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()

    # Verificamos que sea un evento de página
    if data.get("object") != "page":
        return "Not a page event", 400

    # Iteramos sobre entry (puede haber varios)
    for entry in data.get("entry", []):

        # Iteramos sobre messaging (puede haber varios)
        for event in entry.get("messaging", []):

            sender_id = event.get("sender", {}).get("id")
            message   = event.get("message", {})
            text      = message.get("text")

            # Solo procesamos si hay texto (no postbacks, no reads)
            if text:
                print(f"Mensaje de {sender_id}: {text}")

    return jsonify({"status": "ok"}), 200