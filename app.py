import os
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# 1. API Setup
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-pro')
chat_history = [] 

SYSTEM_INSTRUCTION = (
    "Identity: You are PsychoSense AI, created by Abdul Hai. "
    "Behavior: Professional, firm, and observant psychology coach. "
    "Language: Hinglish. "
    "Rules: 1. Strict NO EMOJI policy. 2. Never repeat phrases. "
    "3. Keep responses brief. 4. Be blunt but helpful."
)

def remove_emojis(text):
    return re.sub(r'[^\x00-\x7f]', r'', text)

@app.route('/')
def home():
    return "PsychoSense 2.1 is Running!"

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    global chat_history
    if not user_input:
        return jsonify({"reply": "Kuch toh bol!"})
    try:
        context = "\n".join(chat_history[-5:])
        full_prompt = f"{SYSTEM_INSTRUCTION}\nContext:\n{context}\nUser: {user_input}\nPsychoSense:"
        response = model.generate_content(full_prompt)
        reply = remove_emojis(response.text).strip()
        chat_history.append(f"User: {user_input}")
        chat_history.append(f"AI: {reply}")
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "System busy hai, phir se try kar."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
