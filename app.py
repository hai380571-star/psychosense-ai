from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

memory = {"lazy": 0, "success": 0}
CREATOR = "Abdul Hai"

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


def reply(mode, msg):
    m = (msg or "").lower()

    if "creator" in m or "kisne banaya" in m:
        return f"Mujhe {CREATOR} ne banaya hai"

    if mode == "STRICT":
        return random.choice([
            "Sach bol - tu avoid kar raha hai. Abhi start kar.",
            "Bahane kam, action zyada. Start kar abhi.",
        ])

    elif mode == "SOFT":
        return random.choice([
            "Good. Tu effort daal raha hai.",
            "Nice. Aise hi continue kar.",
        ])

    elif mode == "FUN":
        return random.choice([
            "Bakchodi mode ON. Bol kya kare?",
            "Chal thoda masti karte hain 😏",
        ])

    # NEUTRAL (improved)
    return random.choice([
        "Hmmm... thoda aur detail me bata",
        "Itna short nahi, clearly bol",
        "Andar kya chal raha hai sach me?",
        "Tu kuch chhupa raha hai kya?"
    ])


HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>PsychoSense</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
body {
    margin:0;
    font-family:sans-serif;
    background:#0f172a;
    color:white;
    display:flex;
    flex-direction:column;
    height:100vh;
}

.header {
    padding:12px;
    background:#020617;
}

#chat {
    flex:1;
    overflow-y:auto;
    padding:10px;
    display:flex;
    flex-direction:column;
}

.msg {
    padding:10px;
    margin:6px;
    border-radius:12px;
    max-width:75%;
}

.user {
    background:#22c55e;
    margin-left:auto;
}

.bot {
    background:#1e293b;
}

.footer {
    display:flex;
    padding:10px;
    background:#020617;
}

input {
    flex:1;
    padding:12px;
    border-radius:20px;
    border:none;
}

button {
    margin-left:5px;
    padding:10px;
    background:#22c55e;
    color:white;
    border:none;
    border-radius:20px;
}
</style>
</head>

<body>

<div class="header">
<b>PsychoSense</b><br>
<small>AI Behavioral Mirror</small>
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

        // ❌ mode remove kar diya
        addMsg(data.reply,"bot");

    } catch(err){
        typing.remove();
        addMsg("Server error","bot");
    }
}
</script>

</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user = data.get("message") or ""

    if not user:
        return jsonify({"reply": "Kuch to bol", "mode": "error"})

    mode = analyze(user)
    res = reply(mode, user)

    return jsonify({"reply": res})


if __name__ == "__main__":
    app.run(debug=True)
