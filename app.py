from flask import Flask, request, jsonify
from dotenv import load_dotenv
from messenger import send_text_message, send_buttons_message
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

@app.route("/", methods=["GET"])
def home():
    return "Bot is running ✓", 200

@app.route("/webhook", methods=["GET"])
def verify_webhook():
    mode      = request.args.get("hub.mode")
    token     = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == VERIFY_TOKEN and challenge:
        return challenge, 200
    return "Invalid token", 403

@app.route("/webhook", methods=["POST"])
def receive_message():
    data = request.get_json()

    if data.get("object") != "page":
        return "Not a page event", 400

    for entry in data.get("entry", []):
        for event in entry.get("messaging", []):
            sender_id = event.get("sender", {}).get("id")
            # Detect message text
            message   = event.get("message", {})
            text      = message.get("text")

            # Detect postback (button pressed)
            postback = event.get("postback", {})
            payload = postback.get("payload")

            if sender_id: 
                # Case 1: The user sent a text message.

                if text:
                    # Instead of just echoing, we will show them our menu buttons!

                    send_buttons_message(sender_id, "What would you like to do?", [
                        {"type": "postback", "title": "View lessons", "payload": "VIEW_LESSONS"},
                        {"type": "postback", "title": "Take a quiz", "payload": "START_QUIZ"},
                        {"type": "postback", "title": "Contact us", "payload": "CONTACT"} 
                    ])

                    # Case 2: The user pressed one of our buttons
                elif payload:
                    if payload == "VIEW_LESSONS":
                        send_text_message(sender_id, "Here are your available lessons 📚")
                    elif payload == "START_QUIZ":
                        send_text_message(sender_id, "Starting quiz! 🎯")
                    elif payload == "CONTACT":
                        send_text_message(sender_id, "We'll be in touch shortly! 📩")
 
    return jsonify({"status": "ok"}), 200

if __name__ == "__main__":
    app.run(debug=True, port=5000)