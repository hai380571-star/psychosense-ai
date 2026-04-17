from flask import Flask, request, jsonify, render_template_string
import random

app = Flask(__name__)

memory = {"lazy": 0, "success": 0}
last_mode = None
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
    global last_mode
    m = (msg or "").lower()

    # creator
    if any(x in m for x in ["creator", "kisne banaya", "who made you"]):
        return f"Mujhe {CREATOR} ne banaya hai"

    # savage level
    savage = memory["lazy"]

    # direct reactions
    if "hi" in m or "hello" in m:
        return random.choice([
            "Haan bol, kya chal raha hai?",
            "Aaj kya scene hai?",
        ])

    if "nhi" in m or "kuch nhi" in m:
        return random.choice([
            "Har baar 'kuch nahi' ke peeche kuch hota hai",
            "Tu avoid kar raha hai bas bol nahi raha",
        ])

    if "chal bhag" in m or "abe" in m:
        return random.choice([
            "Attitude aa raha hai, par reason bhi hoga",
            "Bhag sakta hai, par problem wahi rahegi",
        ])

    # mode behavior
    if mode == "STRICT":
        if savage > 3:
            return random.choice([
                "Tu sirf delay nahi kar raha, ye tera pattern ban gaya hai",
                "Sach bol, tu khud ko hi ignore kar raha hai",
            ])
        return random.choice([
            "Tu avoid kar raha hai, start kar abhi",
            "Bahane kam, action zyada",
        ])

    elif mode == "SOFT":
        return random.choice([
            "Good, tu effort daal raha hai",
            "Nice, consistency aa rahi hai",
        ])

    elif mode == "FUN":
        return random.choice([
            "Chal thoda chill karte hain",
            "Mood halka kar raha hai tu",
        ])

    # neutral
    return random.choice([
        "Seedha bol, kya chal raha hai?",
        "Tu clearly bol nahi raha abhi",
        "Andar kuch to chal raha hai",
        "Main sun raha hoon, bol",
    ])


HTML = '''
<!DOCTYPE html>
<html>
<head>
<title>PsychoSense AI</title>
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
'''

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
