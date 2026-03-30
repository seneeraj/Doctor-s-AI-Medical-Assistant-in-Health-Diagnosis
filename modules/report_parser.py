import fitz  # PyMuPDF
import re

def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")

    for page in pdf:
        text += page.get_text()

    return text


def extract_medical_entities(text):
    text = text.lower()

    data = {}

    # -----------------------------
    # BLOOD SUGAR
    # -----------------------------
    glucose_match = re.search(r'glucose[:\s]+(\d+)', text)
    if glucose_match:
        glucose_value = int(glucose_match.group(1))
        data["glucose"] = glucose_value

    # -----------------------------
    # HEMOGLOBIN
    # -----------------------------
    hb_match = re.search(r'hemoglobin[:\s]+(\d+)', text)
    if hb_match:
        hb_value = int(hb_match.group(1))
        data["hemoglobin"] = hb_value

    # -----------------------------
    # GENERIC FLAGS
    # -----------------------------
    if "infection" in text:
        data["infection"] = True

    if "fracture" in text:
        data["fracture"] = True

    return data