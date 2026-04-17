import random

def reply(mode, msg):
    global last_mode
    m = (msg or "").lower()

    # 🔥 direct understanding (real AI feel)
    if any(x in m for x in ["hi", "hii", "hello"]):
        return random.choice([
            "Haan bol, kya chal raha hai?",
            "Hi... aaj kya scene hai?",
        ])

    if any(x in m for x in ["nhi", "kuch nhi"]):
        return random.choice([
            "Har baar 'kuch nahi' ke peeche kuch hota hai",
            "Tu avoid kar raha hai bas bol nahi raha",
        ])

    if any(x in m for x in ["chal bhag", "abe", "jaa"]):
        return random.choice([
            "Attitude aa raha hai... par reason bhi hoga",
            "Theek hai bhag ja, par problem wahi rahegi",
        ])

    if "kya karu" in m:
        return "Jo tu avoid kar raha hai wahi kar — wahi answer hai"

    if "creator" in m:
        return f"Mujhe {CREATOR} ne banaya hai"

    # 🔥 mode continuity (real AI feel)
    if last_mode == mode:
        if mode == "STRICT":
            return random.choice([
                "Abhi bhi wahi pattern repeat ho raha hai",
                "Tu consciously delay kar raha hai",
            ])

        elif mode == "SOFT":
            return random.choice([
                "Consistency dikh rahi hai, accha hai",
                "Ye flow maintain kar, rukna mat",
            ])

    # 🔥 normal behavior
    if mode == "STRICT":
        res = random.choice([
            "Sach bol — tu avoid kar raha hai",
            "Action lena padega, warna kuch change nahi hoga",
        ])

    elif mode == "SOFT":
        res = random.choice([
            "Good — tu effort daal raha hai",
            "Nice progress, aise hi chal",
        ])

    elif mode == "FUN":
        res = random.choice([
            "Chal thoda fun bhi zaroori hai",
            "Mood halka kar raha hai tu 😏",
        ])

    else:
        res = random.choice([
            "Seedha bol — kya chal raha hai?",
            "Tu clearly express nahi kar raha abhi",
            "Main sun raha hoon, bol",
        ])

    last_mode = mode
    return res
