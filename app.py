@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "").lower()

    if not msg:
        return jsonify({"reply": "Kuch to bol 😄", "mode": "error"})

    # simple intelligence
    if "hi" in msg or "hello" in msg:
        reply = "Hello 👀 main PsychoSense hoon, tum kya soch rahe ho?"
    
    elif "sad" in msg or "dukhi" in msg:
        reply = "Hmm… lagta hai mood heavy hai. Kya hua?"
    
    elif "happy" in msg:
        reply = "Nice 😄 good energy! Kya accha hua aaj?"
    
    else:
        reply = "Interesting… thoda aur detail me bata"

    return jsonify({
        "reply": reply,
        "mode": "psycho-basic"
    })
