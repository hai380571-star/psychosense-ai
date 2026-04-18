from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
import random

app = Flask(__name__)

# ===== CONFIG =====
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash-latest")

# ===== MEMORY =====
memory = {"lazy": 0, "success": 0}

# ===== ANALYZE =====
def analyze(text):
    t = text.lower()

    if "nahi" in t or "kal" in t:
        memory["lazy"] += 1
        return "STRICT"
    elif "done" in t or "kiya" in t:
        memory["success"] += 1
        return "SOFT"
    else:
        return "NEUTRAL"

# ===== LOCAL RESPONSE =====
def local_reply(mode):
    if mode == "STRICT":
        return random.choice([
            "Seedha bol, kya issue hai.",
            "Avoid karne se kuch solve nahi hoga.",
            "Focus kar—problem kya hai exactly?",
            "Repeat se kuch nahi badlega.",
        ])
    elif mode == "SOFT":
        return random.choice([
            "Good. Tu effort daal raha hai.",
            "Nice, continue kar.",
            "Sahi direction me ja raha hai tu.",
        ])
    else:
        return random.choice([
            "Thoda clear bol—problem kya hai?",
            "Context de, tab hi help kar paunga.",
        ])

# ===== ROUTES =====
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("msg")

    mode = analyze(user_msg)

    try:
        # ===== AI RESPONSE =====
        prompt = f"""
        You are PsychoSense, created by Abdul Hai.
        Tone: {mode}
        User: {user_msg}

        Reply in Hinglish, short, human-like, slightly psychological.
        """

        response = model.generate_content(prompt)
        ai_reply = response.text.strip()

    except Exception as e:
        ai_reply = f"Technical issue: {str(e)}"

    # fallback if AI fails
    if not ai_reply:
        ai_reply = local_reply(mode)

    return jsonify({
        "reply": ai_reply,
        "mode": mode
    })

# ===== RUN =====
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
