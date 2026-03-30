def calculate_risk(symptoms_list, answers, report_data, alerts):

    score = 0

    # -----------------------------
    # BASE SYMPTOM RISK
    # -----------------------------
    if "chest pain" in symptoms_list:
        score += 20

    if "breathlessness" in symptoms_list:
        score += 20

    if "dizziness" in symptoms_list:
        score += 10

    if "fever" in symptoms_list:
        score += 10

    # -----------------------------
    # FOLLOW-UP ANSWERS
    # -----------------------------
    for q, ans in answers.items():

        if "spread to arm" in q.lower() and ans == "Yes":
            score += 30

        if "fever" in q.lower() and isinstance(ans, (int, float)):
            if ans >= 103:
                score += 20

    # -----------------------------
    # REPORT DATA
    # -----------------------------
    if "glucose" in report_data:
        if report_data["glucose"] > 180:
            score += 20

    if "hemoglobin" in report_data:
        if report_data["hemoglobin"] < 10:
            score += 20

    # -----------------------------
    # EMERGENCY ALERT BONUS
    # -----------------------------
    if alerts:
        score += 30

    # -----------------------------
    # LIMIT SCORE
    # -----------------------------
    score = min(score, 100)

    # -----------------------------
    # PRIORITY LEVEL
    # -----------------------------
    if score >= 80:
        priority = "Critical"
    elif score >= 60:
        priority = "High"
    elif score >= 30:
        priority = "Medium"
    else:
        priority = "Low"

    return score, priority