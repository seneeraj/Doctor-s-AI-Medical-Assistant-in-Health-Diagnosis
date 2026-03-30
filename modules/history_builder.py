def build_patient_history(name, age, symptoms, report_text):

    history = f"""
    Patient Name: {name}
    Age: {age}

    Symptoms:
    {symptoms}

    Report Summary:
    {report_text[:500]}
    """

    return history