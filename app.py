from flask import Flask, request, jsonify, render_template_string
from openai import OpenAI
import os, random

app = Flask(__name__)

# ===== OPENAI =====
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ===== MEMORY =====
memory = {"lazy": 0, "success": 0}
history = []
last_reply = ""
CREATOR = "Abdul Hai"

# ===== NO REPEAT =====
def pick(options):
    global last_reply
    random.shuffle(options)
    for opt in options:
        if opt != last_reply:
            last_reply = opt
            return opt
    return options[0]

# ===== ANALYZE =====
def analyze(text):
    t = (text or "").lower()

    if any(w in t for w in ["kal", "baad me", "nahi karunga"]):
        memory["lazy"] += 1
        return "STRICT"

    elif any(w in t for w in ["done", "kar liya", "complete"]):
        memory["success"] += 1
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
- Short replies (1–2 lines)
- Human tone
- If user repeats/avoids, point it out
"""

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=80
    )

    return res.choices[0].message.content.strip()

# ===== MAIN REPLY =====
def reply(mode, msg):
    global history
    m = (msg or "").lower()

    history.append(m)
    if len(history) > 5:
        history.pop(0)

    # creator fix
    if any(x in m for x in ["creator", "kisne banaya", "who made you"]):
        return "Mujhe " + CREATOR + " ne banaya hai"

    # try AI
    try:
        return ai_reply(mode, msg)

    except Exception as e:
        print("AI ERROR:", e)

        # SAFE fallback (never breaks)
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
