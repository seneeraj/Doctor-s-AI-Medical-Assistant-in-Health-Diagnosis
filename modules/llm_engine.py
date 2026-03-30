from openai import OpenAI

client = OpenAI()

def generate_doctor_explanation(symptoms, report_data, diagnosis):

    prompt = f"""
You are a medical assistant helping a doctor.

Patient symptoms:
{symptoms}

Medical report data:
{report_data}

Top predicted conditions:
{diagnosis}

Tasks:
1. Explain the possible conditions in simple clinical language
2. Justify reasoning
3. Suggest next steps (tests / doctor visit)
4. Keep it clear and professional
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
    
def summarize_report(report_data):

    if not report_data:
        return "No significant findings from uploaded report."

    summary = "Medical Report Summary:\n\n"

    for key, value in report_data.items():

        if key == "glucose":
            if value > 140:
                summary += f"- Elevated glucose level ({value}) suggesting possible diabetes.\n"
            else:
                summary += f"- Normal glucose level ({value}).\n"

        elif key == "hemoglobin":
            if value < 12:
                summary += f"- Low hemoglobin ({value}) suggesting anemia.\n"
            else:
                summary += f"- Normal hemoglobin ({value}).\n"

        elif key == "infection":
            summary += "- Signs of infection detected.\n"

        elif key == "fracture":
            summary += "- Possible fracture indicated in report.\n"

        else:
            summary += f"- {key}: {value}\n"

    return summary