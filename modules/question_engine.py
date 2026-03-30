from modules.followup_questions import followup_db

def get_followup_questions(symptoms_list):

    questions = []

    for symptom in symptoms_list:
        if symptom in followup_db:
            questions.extend(followup_db[symptom])

    return questions