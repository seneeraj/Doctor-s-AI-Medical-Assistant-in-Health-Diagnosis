def detect_emergency(symptoms_list, answers, report_data):

    alerts = []

    # -----------------------------
    # ❤️ HEART ATTACK
    # -----------------------------
    if "chest pain" in symptoms_list and "breathlessness" in symptoms_list:
        for q, ans in answers.items():
            if "spread to arm" in q.lower() and ans == "Yes":
                alerts.append({
                    "type": "Heart Attack Risk",
                    "message": "Chest pain with radiation to arm and breathlessness detected.",
                    "action": "Seek immediate emergency medical care (call ambulance)."
                })

    # -----------------------------
    # 🧠 STROKE
    # -----------------------------
    if "dizziness" in symptoms_list:
        for q, ans in answers.items():
            if "one-sided" in str(ans).lower():
                alerts.append({
                    "type": "Stroke Risk",
                    "message": "One-sided neurological symptoms detected.",
                    "action": "Immediate neurological evaluation required."
                })

    # -----------------------------
    # 🌡️ HIGH FEVER
    # -----------------------------
    for q, ans in answers.items():
        if "fever" in q.lower() and isinstance(ans, (int, float)):
            if ans >= 103:
                alerts.append({
                    "type": "High Fever Risk",
                    "message": "Very high fever detected.",
                    "action": "Consult doctor urgently."
                })

    # -----------------------------
    # 🫁 RESPIRATORY DISTRESS
    # -----------------------------
    if "breathlessness" in symptoms_list:
        alerts.append({
            "type": "Respiratory Risk",
            "message": "Breathing difficulty detected.",
            "action": "Seek medical evaluation immediately."
        })

    return alerts