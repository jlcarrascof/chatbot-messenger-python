# NotebookLM Reference: Sprint 2 - Postback Buttons (Lectures 10-11)

This document contains a comprehensive summary of the concepts, API structures, constraints, and implementation details for **Sprint 2: Postback Buttons**. This file is structured to be uploaded to NotebookLM for generating study guides, summaries, or interactive quizzes.

---

## 1. Core Concept: Interactive Messages vs. Plain Text

In Facebook Messenger Platform, messages generally fall into two categories:
* **Plain Text Messages:** Simple strings of text sent to the user using the standard `"text"` payload inside the `"message"` object.
* **Structured Messages (Templates):** Rich, interactive visual elements (e.g., buttons, generic carrusels, media, receipts) enclosed within the `"attachment"` payload of type `"template"`.

### Why Use Templates and Buttons?
* **Reduced Friction:** Users don't need to type responses. They can simply tap options.
* **Guided Navigation:** Allows the bot to offer a menu of actions (e.g., viewing lessons, starting quizzes, contacting support).
* **Controlled Input:** Prevents natural language processing (NLP) errors by guiding users down specific conversation paths.

---

## 2. Structure of the Button Template Payload

To send a button template message, the JSON payload sent via `POST` to Meta's Graph API (`/me/messages`) must have the following structure:

```json
{
  "recipient": {
    "id": "<RECIPIENT_ID>"
  },
  "message": {
    "attachment": {
      "type": "template",
      "payload": {
        "template_type": "button",
        "text": "What would you like to do?",
        "buttons": [
          {
            "type": "postback",
            "title": "View lessons",
            "payload": "VIEW_LESSONS"
          },
          {
            "type": "postback",
            "title": "Take a quiz",
            "payload": "START_QUIZ"
          }
        ]
      }
    }
  }
}
```

### Key Components:
1. **`recipient`**: Specifies the target user ID.
2. **`attachment`**: Notifies the Messenger platform that this is a non-text media or template element.
3. **`type: "template"`**: Tells the platform that we are using a structured layout.
4. **`template_type: "button"`**: Specifies that the layout is a button template.
5. **`text`**: The header or prompt message (placed directly above the buttons).
6. **`buttons`**: An array of button objects. In this sprint, we use `postback` buttons.

---

## 3. Postback Button Mechanics

### How Postbacks Work:
1. When a user presses a postback button, **nothing** appears in the user's chat window as a sent message.
2. Instead, Facebook's servers capture the tap event and send an HTTP `POST` webhook request back to our Flask server (`/webhook`).
3. This payload does **not** contain a `"message"` key. It contains a `"postback"` key:
   ```json
   {
     "sender": { "id": "999" },
     "postback": {
       "payload": "START_QUIZ",
       "title": "Take a quiz"
     }
   }
   ```
4. Our Flask webhook checks if the event contains a `"postback"` block, reads the custom `"payload"` value, and handles it accordingly.

---

## 4. Meta API Postback Constraints (Lecture 11)

Meta enforces strict physical limits on the button template API. Violating these rules results in a `400 Bad Request` error:

| Feature / Attribute | Constraint / Limit |
| :--- | :--- |
| **Number of Buttons** | **Maximum 3 buttons** per template message. |
| **Button Title (`title`)** | **Maximum 20 characters** (including spaces/emojis). |
| **Button Payload (`payload`)** | **Maximum 1000 characters**. |
| **Header Text (`text`)** | **Maximum 640 characters**. |
| **Testing Environment** | Postback buttons **do not work** in Meta's quick test console. A real Messenger page inbox or test account is required. |

---

## 5. Implementation Highlights

### Code Architecture:
* **`messenger.py`** contains the low-level functions communicating with Meta's Graph API:
  * `send_text_message(recipient_id, text)`
  * `send_buttons_message(recipient_id, text, buttons)`
* **`app.py`** contains the Flask routing logic to parse incoming JSON, differentiate text from postback payloads, and dispatch the correct responses.
