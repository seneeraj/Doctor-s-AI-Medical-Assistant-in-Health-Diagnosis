README

# 🩺 Doctor's AI Medical Assistant in Health Diagnosis

An intelligent, AI-powered clinical decision support system that assists in preliminary diagnosis, risk assessment, and patient history tracking using symptoms, medical reports, and contextual reasoning.

---

## 🚀 Features

### 🧑 Patient Management

* New & Existing patient handling
* Unique Patient ID generation
* Auto-fill patient details from database
* Patient history tracking across visits

### 🧾 Symptom-Based Diagnosis

* Structured symptom selection (50+ symptoms)
* Intelligent follow-up questions
* Rule-based + weighted diagnosis engine

### 📄 Medical Report Analysis

* Upload multiple medical reports (PDF)
* Automatic text extraction
* Medical entity detection

### 🧠 AI Clinical Reasoning

* Multi-factor diagnosis:

  * Symptoms
  * Follow-up answers
  * Medical reports
* Primary vs Secondary disease classification

### ⚠️ Emergency Detection

* Identifies red-flag conditions
* Generates alert signals for critical cases

### 📊 Risk Scoring System

* Risk Score (numeric)
* Priority Levels:

  * Low
  * Medium
  * High
  * Critical

### 📈 Dashboard & Analytics

* Patient history view
* Disease frequency visualization
* Primary vs Secondary diagnosis chart

### 🤖 AI Doctor Explanation

* Natural language explanation of diagnosis
* Auto-generated report summary

---

## 🖥️ Tech Stack

* **Frontend:** Streamlit
* **Backend Logic:** Python
* **Database:** SQLite
* **Visualization:** Matplotlib
* **AI/Logic:**

  * Rule-based reasoning engine
  * LLM integration (optional/local/OpenAI)

---

## 📁 Project Structure

```
ai_medical_assistant/
│
├── app.py
├── patients.db
│
├── modules/
│   ├── medical_reasoning.py
│   ├── risk_scoring.py
│   ├── emergency_detection.py
│   ├── question_engine.py
│   ├── report_parser.py
│   ├── llm_engine.py
│   ├── database.py
│   └── symptom_database.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/ai-medical-assistant.git
cd ai-medical-assistant
```

### 2️⃣ Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run app.py
```

---

## 🧠 How It Works

1. Enter patient details or load existing patient
2. Select symptoms
3. Answer follow-up questions
4. Upload medical reports (optional)
5. Click **Analyze**

➡️ System performs:

* Diagnosis prediction
* Risk scoring
* Emergency detection
* AI explanation generation

---

## 📊 Example Outputs

* Diagnosis with confidence scores
* Risk level (Low → Critical)
* Emergency alerts
* Patient history tracking
* Disease frequency graph

---

## ⚠️ Disclaimer

> This application generates AI-based medical insights for informational purposes only.
> It is **not a substitute for professional medical advice, diagnosis, or treatment**.
>
> Always consult a qualified healthcare provider for medical decisions.
> In case of emergency, seek immediate medical attention.

---

## 🔮 Future Enhancements

* Doctor dashboard (patient queue & triage)
* Multi-language support (Hindi + English)
* Real-time vitals integration
* Mobile app version
* Cloud deployment (AWS/GCP)
* Fine-tuned medical LLM

---

## 🤝 Contributing

Contributions are welcome!
Feel free to fork the repository and submit a pull request.

---

## 📜 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

Developed by **Neeraj Bhatia**
AI & Data Science Enthusiast 🚀

---

## ⭐ Support

If you found this useful, please ⭐ the repository!

---

