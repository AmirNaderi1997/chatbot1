from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# 🔐 Store your API key securely
API_KEY = ""
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = ""
    payload = {}  # define upfront so it's always in scope

    try:
        data = request.get_json()
        user_message = data.get("message", "")

        # Build Gemini payload
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": user_message}]
                }
            ]
        }

        headers = {"Content-Type": "application/json"}
        response = requests.post(
            f"{GEMINI_URL}?key={API_KEY}",
            json=payload,
            headers=headers
        )

        # Check if Gemini returned success
        if response.status_code == 200:
            result = response.json()
            reply = result["candidates"][0]["content"]["parts"][0]["text"]
        else:
            print("Gemini error response:", response.text)
            reply = f"Error: {response.status_code}"

    except Exception as e:
        print("Exception in /chat:", str(e))
        reply = "Sorry, something went wrong."

    return jsonify({"reply": reply})



if __name__ == "__main__":
    app.run(debug=True)
