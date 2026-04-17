import os
import re
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# 1. API Setup (Render Environment Variable)
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# 2. Memory & Behavior Setup
# Yahan 'Abdul Hai' as creator fixed hai aur 'No Emoji' rule strict hai.
model = genai.GenerativeModel('gemini-pro')
chat_history = [] # Memory storage

SYSTEM_INSTRUCTION = (
    "Identity: You are PsychoSense AI, created by Abdul Hai. "
    "Behavior: Professional, firm, and observant psychology coach. "
    "Language: Hinglish. "
    "Rules: 1. Strict NO EMOJI policy. 2. Never repeat phrases. "
    "3. Keep responses brief and logic-driven. 4. Be blunt but helpful."
)

# Emojis hatane ka function (Fallback filter)
def remove_emojis(text):
    return re.sub(r'[^\x00-\x7f]', r'', text)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("message")
    global chat_history

    if not user_input:
        return jsonify({"reply": "Kuch likh tabhi toh observe karunga."})

    try:
        # 3. Contextual Memory (Last 5 chats yaad rakhega)
        context = "\n".join(chat_history[-5:])
        full_prompt = f"{SYSTEM_INSTRUCTION}\nContext:\n{context}\nUser: {user_input}\nPsychoSense:"

        response = model.generate_content(full_prompt)
        
        # 4. Clean & Filter Output
        reply = remove_emojis(response.text).strip()
        
        # History update
        chat_history.append(f"User: {user_input}")
        chat_history.append(f"AI: {reply}")

        return jsonify({"reply": reply})

    except Exception as e:
        # 5. Fallback (System Crash nahi hoga)
        print(f"Error: {e}")
        return jsonify({"reply": "System overload ho raha hai. Seedha point pe baat kar dobara."})

if __name__ == "__main__":
    # Render dynamic port support
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
        return "SOFT"

    elif any(w in t for w in ["masti", "bakchodi", "fun"]):
        return "FUN"

    return "NEUTRAL"

# ===== AI REPLY =====
def ai_reply(mode, msg):
    prompt = f"""
You are PsychoSense, a psychological AI created by Abdul Hai.

Mode: {mode}

User message: {msg}

User stats:
Lazy: {memory['lazy']}
Success: {memory['success']}

Rules:
- No emojis
- Short replies (1-2 lines)
- Human tone
- If user avoids or repeats, point it out
"""

    response = model.generate_content(prompt)
    return response.text.strip()

# ===== MAIN REPLY =====
def reply(mode, msg):
    global history
    m = (msg or "").lower()

    history.append(m)
    if len(history) > 5:
        history.pop(0)

    # creator
    if any(x in m for x in ["creator", "kisne banaya", "who made you"]):
        return "Mujhe " + CREATOR + " ne banaya hai"

    try:
        return ai_reply(mode, msg)

    except Exception as e:
        print("AI ERROR:", e)

        # fallback
        if mode == "STRICT":
            return pick([
                "Tu delay kar raha hai, start kar",
                "Action le warna same rahega",
            ])
        elif mode == "SOFT":
            return pick([
                "Good, continue kar",
                "Progress ho raha hai",
            ])
        elif mode == "FUN":
            return pick([
                "Chal thoda chill karte hain",
                "Mood halka kar",
            ])
        else:
            return pick([
                "Seedha bol, kya chal raha hai",
                "Tu clearly bol nahi raha",
            ])

# ===== UI =====
HTML = """
<!DOCTYPE html>
<html>
<head>
<title>PsychoSense AI</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
body {margin:0;font-family:sans-serif;background:#0f172a;color:white;display:flex;flex-direction:column;height:100vh;}
.header {padding:12px;background:#020617;}
#chat {flex:1;overflow-y:auto;padding:10px;display:flex;flex-direction:column;}
.msg {padding:10px;margin:6px;border-radius:12px;max-width:75%;}
.user {background:#22c55e;margin-left:auto;}
.bot {background:#1e293b;}
.footer {display:flex;padding:10px;background:#020617;}
input {flex:1;padding:12px;border-radius:20px;border:none;}
button {margin-left:5px;padding:10px;background:#22c55e;color:white;border:none;border-radius:20px;}
</style>
</head>

<body>

<div class="header">
<b>PsychoSense AI</b><br>
<small>Created by Abdul Hai</small>
</div>

<div id="chat"></div>

<div class="footer">
<input id="input" placeholder="Type your thoughts...">
<button onclick="send()">Send</button>
</div>

<script>
let chat = document.getElementById("chat");

function addMsg(text, type){
    let div = document.createElement("div");
    div.className = "msg " + type;
    div.innerHTML = text;
    chat.appendChild(div);
    chat.scrollTop = chat.scrollHeight;
}

async function send(){
    let input = document.getElementById("input");
    let msg = input.value;
    if(!msg) return;

    addMsg(msg,"user");
    input.value="";

    let typing = document.createElement("div");
    typing.className = "msg bot";
    typing.innerHTML = "Typing...";
    chat.appendChild(typing);

    try {
        let res = await fetch("/chat",{
            method:"POST",
            headers:{"Content-Type":"application/json"},
            body:JSON.stringify({ message: msg })
        });

        let data = await res.json();

        typing.remove();
        addMsg(data.reply,"bot");

    } catch(err){
        typing.remove();
        addMsg("Server error","bot");
    }
}
</script>

</body>
</html>
"""

# ===== ROUTES =====
@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user = data.get("message") or ""

    if not user:
        return jsonify({"reply": "Say something"})

    mode = analyze(user)
    res = reply(mode, user)

    return jsonify({"reply": res})

if __name__ == "__main__":
    app.run()
