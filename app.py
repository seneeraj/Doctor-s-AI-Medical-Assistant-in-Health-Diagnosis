import streamlit as st
import matplotlib.pyplot as plt
from datetime import date, datetime



# -----------------------------
# RESET FUNCTION (ADD HERE)
# -----------------------------
def reset_app():
    st.session_state.name = ""
    st.session_state.dob = date.today()
    st.session_state.gender = "Male"
    st.session_state.father_name = ""

    st.session_state.selected_symptoms = []
    st.session_state.symptom_version += 1

    # Clear dynamic answers
    for key in list(st.session_state.keys()):
        if key.startswith("question_"):
            del st.session_state[key]            

# -----------------------------
# MODULES
# -----------------------------
from modules.medical_reasoning import generate_diagnosis
from modules.risk_scoring import calculate_risk
from modules.emergency_detection import detect_emergency
from modules.question_engine import get_followup_questions
from modules.report_parser import extract_text_from_pdf, extract_medical_entities
from modules.llm_engine import generate_doctor_explanation, summarize_report
from modules.database import (
    init_db,
    save_record,
    get_patient_history,
    get_all_patients,
    get_patient_by_id
)
from modules.symptom_database import symptom_db

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Doctor's Medical Diagnosis Assistant", layout="wide")
st.title("🩺 Doctor's AI Medical Assistant in Health Diagnosis")

init_db()

col1, col2 = st.columns([8, 2])

with col2:
    if st.button("🔄 Refresh/Next Case"):
        reset_app()
        st.rerun()


# -----------------------------
# SESSION STATE
# -----------------------------
defaults = {
    "name": "",
    "dob": date.today(),
    "gender": "Male",
    "father_name": "",
    "selected_symptoms": [],
    "symptom_version": 0
}

for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:

    st.title("🧑 Patient Panel")

    patient_type = st.radio("Patient Type", ["New Patient", "Existing Patient"])

    if patient_type == "Existing Patient":

        patients = get_all_patients()

        if patients:
            patient_map = {f"{name} ({pid[:6]}...)": pid for pid, name in patients}

            search = st.text_input("🔍 Search Patient")

            filtered = {
                k: v for k, v in patient_map.items()
                if not search or search.lower() in k.lower()
            }

            if filtered:
                selected_label = st.selectbox("Select Patient", list(filtered.keys()))
                selected_id = filtered[selected_label]

                data = get_patient_by_id(selected_id)

                if data:
                    st.session_state.name = data[0]
                    st.session_state.dob = datetime.strptime(data[1], "%Y-%m-%d").date()
                    st.session_state.gender = data[2]
                    st.session_state.father_name = data[3]

                    st.success("✅ Patient Loaded")

    st.text_input("Name", key="name")
    st.date_input("DOB", key="dob", min_value=date(1900,1,1), max_value=date.today())
    st.selectbox("Gender", ["Male","Female","Other"], key="gender")
    st.text_input("Father Name", key="father_name")

# -----------------------------
# DASHBOARD
# -----------------------------
st.subheader("📊 Clinical Dashboard")

left, right = st.columns([1.2, 2])

# -----------------------------
# HISTORY
# -----------------------------
history = get_patient_history(
    st.session_state.name,
    str(st.session_state.dob),
    st.session_state.gender,
    st.session_state.father_name
)

with left:
    st.markdown("### 📜 Patient History")

    if history:
        for r in history[::-1]:
            symptoms, _, diagnosis, risk, priority, time = r

            with st.expander(f"{time} | {priority}"):
                st.write("Symptoms:", symptoms)

                for d in diagnosis:
                    st.write(f"- {d['disease']} ({d['score']}%)")
    else:
        st.info("No history")

# -----------------------------
# GRAPH (PRIMARY vs SECONDARY)
# -----------------------------
with right:
    st.markdown("### 📊 Disease Frequency (Primary vs Secondary)")

    if history:

        primary_counts = {}
        secondary_counts = {}

        for r in history:
            diagnosis_list = sorted(r[2], key=lambda x: x["score"], reverse=True)

            if not diagnosis_list:
                continue

            # Primary
            primary = diagnosis_list[0]["disease"]
            primary_counts[primary] = primary_counts.get(primary, 0) + 1

            # Secondary
            for d in diagnosis_list[1:3]:
                disease = d["disease"]
                secondary_counts[disease] = secondary_counts.get(disease, 0) + 1

        all_diseases = list(set(primary_counts) | set(secondary_counts))

        all_diseases = sorted(
            all_diseases,
            key=lambda d: primary_counts.get(d, 0),
            reverse=True
        )

        primary_vals = [primary_counts.get(d, 0) for d in all_diseases]
        secondary_vals = [secondary_counts.get(d, 0) for d in all_diseases]

        fig, ax = plt.subplots(figsize=(6, 4))

        ax.bar(all_diseases, primary_vals, label="Primary")
        ax.bar(all_diseases, secondary_vals, bottom=primary_vals, label="Secondary")

        ax.set_title("Diagnosis Distribution")
        ax.set_xlabel("Disease")
        ax.set_ylabel("Count")

        plt.xticks(rotation=25)
        ax.legend()

        st.pyplot(fig)

    else:
        st.info("No history available")

# -----------------------------
# SYMPTOMS
# -----------------------------
st.subheader("🧾 Symptoms")

search = st.text_input("🔍 Search symptom").lower()

cols = st.columns(3)
i = 0

for category, symptoms in symptom_db.items():

    filtered = [s for s in symptoms if not search or search in s.lower()]

    if not filtered:
        continue

    with cols[i]:
        st.markdown(f"### {category}")

        for s in filtered:
            key = f"{s}_{st.session_state.symptom_version}"

            checked = st.checkbox(s, key=key, value=(s in st.session_state.selected_symptoms))

            if checked and s not in st.session_state.selected_symptoms:
                st.session_state.selected_symptoms.append(s)

            elif not checked and s in st.session_state.selected_symptoms:
                st.session_state.selected_symptoms.remove(s)

    i = (i + 1) % 3

if st.button("🧹 Clear"):
    st.session_state.selected_symptoms = []
    st.session_state.symptom_version += 1
    st.rerun()

# -----------------------------
# QUESTIONS
# -----------------------------
st.subheader("🧠 Additional Questions")

answers = {}
questions = get_followup_questions(st.session_state.selected_symptoms)

for q in questions:
    if q["type"] == "yesno":
        answers[q["question"]] = st.radio(q["question"], ["Yes","No","Not Sure"], horizontal=True)
    elif q["type"] == "mcq":
        answers[q["question"]] = st.selectbox(q["question"], q["options"])
    elif q["type"] == "number":
        answers[q["question"]] = st.number_input(q["question"], min_value=0.0)
    else:
        answers[q["question"]] = st.text_input(q["question"])

# -----------------------------
# REPORT UPLOAD
# -----------------------------
st.subheader("📄 Upload Reports")

uploaded_files = st.file_uploader("Upload PDFs", type=["pdf"], accept_multiple_files=True)

report_data = {}

if uploaded_files:
    combined = ""

    for f in uploaded_files:
        combined += extract_text_from_pdf(f)

    report_data = extract_medical_entities(combined)
    st.success(f"{len(uploaded_files)} reports processed")

# -----------------------------
# ANALYZE
# -----------------------------

def reset_app():
    st.session_state.name = ""
    st.session_state.dob = date.today()
    st.session_state.gender = "Male"
    st.session_state.father_name = ""

    st.session_state.selected_symptoms = []
    st.session_state.symptom_version += 1

    # Clear dynamic answers (important)
    for key in list(st.session_state.keys()):
        if key.startswith("question_"):
            del st.session_state[key]





if st.button("🔍 Analyze"):

    if not st.session_state.name:
        st.error("Enter patient name")
        st.stop()

    if not st.session_state.selected_symptoms:
        st.error("Select symptoms")
        st.stop()

    diagnosis = generate_diagnosis(
        st.session_state.selected_symptoms,
        report_data,
        answers
    )

    alerts = detect_emergency(
        st.session_state.selected_symptoms,
        answers,
        report_data
    )

    risk, priority = calculate_risk(
        st.session_state.selected_symptoms,
        answers,
        report_data,
        alerts
    )

    pid = save_record(
        st.session_state.name,
        str(st.session_state.dob),
        st.session_state.gender,
        st.session_state.father_name,
        st.session_state.selected_symptoms,
        report_data,
        diagnosis,
        risk,
        priority
    )

    st.success(f"Saved | Patient ID: {pid}")

    st.metric("Risk", risk)
    st.metric("Priority", priority)

    if alerts:
        st.error("🚨 Emergency Detected")

    st.subheader("🧠 Diagnosis")
    for d in diagnosis:
        st.write(f"{d['disease']} ({d['score']}%)")

    st.subheader("🧠 AI Explanation")
    st.write(generate_doctor_explanation(
        st.session_state.selected_symptoms,
        report_data,
        diagnosis
    ))

    st.subheader("📄 Report Summary")
    st.write(summarize_report(report_data))
    
    
st.markdown("---")
st.subheader("⚠️ Disclaimer")
st.error("⚠️ This report is AI-generated report. and should not be used as a substitute for professional medical advice. Please consult a qualified doctor.")

