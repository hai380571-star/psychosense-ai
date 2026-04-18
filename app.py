import os
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# 1. API Initialization Check
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("CRITICAL: GEMINI_API_KEY ki value khali mili hai! Render Settings check karo.")
else:
    print(f"SUCCESS: API Key mil gayi hai (Starts with: {api_key[:5]}...)")
    genai.configure(api_key=api_key)

model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_msg = data.get("message", "")
        print(f"DEBUG: User ne kaha -> {user_msg}")

        # Safety checking for API configuration
        if not api_key:
            return jsonify({"reply": "Backend Error: API Key nahi mili."})

        prompt = f"Respond as PsychoSense (Coach) in the user's language. No emojis. User: {user_msg}"
        
        # Gemini API Call
        response = model.generate_content(prompt)
        
        if response and response.text:
            print(f"DEBUG: AI ka jawab -> {response.text[:20]}...")
            return jsonify({"reply": response.text.strip()})
        else:
            return jsonify({"reply": "AI ne khali jawab diya. Key check karo."})

    except Exception as e:
        # Ye line Render ke logs mein ERROR dikhayegi
        print(f"ERROR OCCURRED: {str(e)}")
        return jsonify({"reply": f"Asli Error: {str(e)[:50]}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
