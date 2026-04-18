import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# API Setup
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

# Model initialization
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        
        # Identity Logic
        prompt = f"You are PsychoSense AI by Abdul Hai. Respond in the user's language. No emojis. User: {user_msg}"
        
        response = model.generate_content(prompt)
        
        if response.text:
            return jsonify({"reply": response.text.strip()})
        else:
            return jsonify({"reply": "AI ne kuch nahi kaha."})

    except Exception as e:
        return jsonify({"reply": f"Technical issue: {str(e)[:50]}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
