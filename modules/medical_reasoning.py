# -----------------------------
# 🧠 WEIGHTED + RULE-BASED ENGINE
# -----------------------------

def generate_diagnosis(symptoms, report_data=None, answers=None):

    symptoms = [s.lower() for s in symptoms]

    # -----------------------------
    # 📚 DISEASE KNOWLEDGE BASE
    # -----------------------------
    disease_db = {
        "Flu": {
            "symptoms": {
                "fever": 3,
                "fatigue": 2,
                "headache": 2,
                "cough": 3,
                "body pain": 2
            },
            "required": ["fever"],
            "negative": {}
        },

        "Diabetes": {
            "symptoms": {
                "fatigue": 2,
                "weight loss": 2,
                "blurred vision": 3,
                "frequent urination": 3,
                "excessive thirst": 3
            },
            "required": ["frequent urination", "excessive thirst"],
            "negative": {
                "fever": 3   # ❗ critical penalty
            }
        },

        "Migraine": {
            "symptoms": {
                "headache": 3,
                "dizziness": 2,
                "nausea": 2,
                "sensitivity to light": 3
            },
            "required": ["headache"],
            "negative": {}
        },

        "Heart Disease": {
            "symptoms": {
                "chest pain": 4,
                "shortness of breath": 3,
                "fatigue": 1
            },
            "required": ["chest pain"],
            "negative": {
                "fever": 2
            }
        },

        "Gastric Issue": {
            "symptoms": {
                "abdominal pain": 3,
                "bloating": 2,
                "nausea": 2,
                "loss of appetite": 2
            },
            "required": [],
            "negative": {}
        }
    }

    results = []

    # -----------------------------
    # 🧠 SCORING ENGINE
    # -----------------------------
    for disease, data in disease_db.items():

        score = 0
        max_score = sum(data["symptoms"].values())

        # ✅ Add symptom weights
        for s in symptoms:
            if s in data["symptoms"]:
                score += data["symptoms"][s]

        # ❗ Apply negative penalties
        for s in symptoms:
            if s in data["negative"]:
                score -= data["negative"][s]

        # ⚠️ Required symptom check
        if data["required"]:
            if not any(req in symptoms for req in data["required"]):
                score *= 0.4  # heavy penalty

        # Avoid negative score
        score = max(score, 0)

        # Normalize %
        if max_score > 0:
            probability = int((score / max_score) * 100)
        else:
            probability = 0

        # Cap unrealistic confidence
        probability = min(probability, 85)

        results.append({
            "disease": disease,
            "score": probability
        })

    # -----------------------------
    # SORT + TOP 5
    # -----------------------------
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results[:5]