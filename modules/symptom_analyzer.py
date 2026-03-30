def analyze_symptoms(symptoms_list):
    
    results = []

    if "fever" in symptoms_list and "cough" in symptoms_list:
        results.append("Flu or Viral Infection")

    if "chest pain" in symptoms_list:
        results.append("Cardiac Issue")

    if "fatigue" in symptoms_list:
        results.append("Anemia or Diabetes")

    return results