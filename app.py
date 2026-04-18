import os
from flask import Flask, request, jsonify, render_template
from google import genai

app = Flask(__name__)

# 1. New SDK Client Setup
# Render ke Environment Variables se key lega
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.json
        user_message = data.get("message")

        # 2. New Method for Gemini 1.5 Flash
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=user_message,
            config={
                "system_instruction": "You are PsychoSense AI by Abdul Hai. Respond in the user's language. NO EMOJIS."
            }
        )

        return jsonify({"reply": response.text.strip()})

    except Exception as e:
        return jsonify({"reply": f"Audit Error: {str(e)[:50]}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
