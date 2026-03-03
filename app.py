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

    if data.get("object") != "page":
        return "Not a page event", 400

    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            sender_id = event.get("sender", {}).get("id")
            message   = event.get("message", {})
            text      = message.get("text")

            if text:
                print(f"Mensaje de {sender_id}: {text}")

    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)