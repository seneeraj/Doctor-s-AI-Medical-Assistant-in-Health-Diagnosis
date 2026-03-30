import sqlite3
import json
import hashlib
from datetime import datetime

DB_NAME = "patients.db"


# -----------------------------
# INIT DATABASE
# -----------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS patient_records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id TEXT,
        name TEXT,
        dob TEXT,
        gender TEXT,
        father_name TEXT,
        symptoms TEXT,
        report_data TEXT,
        diagnosis TEXT,
        risk_score INTEGER,
        priority TEXT,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()


# -----------------------------
# GENERATE STABLE PATIENT ID
# -----------------------------
def generate_patient_id(name, dob, gender, father_name):
    raw = f"{name}_{dob}_{gender}_{father_name}"
    return hashlib.md5(raw.encode()).hexdigest()


# -----------------------------
# SAVE RECORD
# -----------------------------
def save_record(name, dob, gender, father_name,
                symptoms, report_data, diagnosis, risk_score, priority):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    patient_id = generate_patient_id(name, dob, gender, father_name)

    c.execute("""
    INSERT INTO patient_records
    (patient_id, name, dob, gender, father_name,
     symptoms, report_data, diagnosis, risk_score, priority, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_id,
        name,
        dob,
        gender,
        father_name,
        json.dumps(symptoms),
        json.dumps(report_data),
        json.dumps(diagnosis),   # ✅ structured JSON
        risk_score,
        priority,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()

    return patient_id   # 🔥 return ID to UI


# -----------------------------
# GET PATIENT BASIC DETAILS BY ID
# -----------------------------
def get_patient_by_id(patient_id):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT name, dob, gender, father_name
    FROM patient_records
    WHERE patient_id=?
    LIMIT 1
    """, (patient_id,))

    record = c.fetchone()
    conn.close()

    if record:
        return record  # (name, dob, gender, father_name)

    return None


# -----------------------------
# GET PATIENT HISTORY (BY IDENTITY)
# -----------------------------
def get_patient_history(name, dob, gender, father_name):

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    patient_id = generate_patient_id(name, dob, gender, father_name)

    c.execute("""
    SELECT symptoms, report_data, diagnosis, risk_score, priority, timestamp
    FROM patient_records
    WHERE patient_id=?
    ORDER BY timestamp ASC
    """, (patient_id,))

    records = c.fetchall()
    conn.close()

    # -----------------------------
    # PARSE JSON CLEANLY
    # -----------------------------
    parsed_records = []

    for r in records:
        parsed_records.append((
            json.loads(r[0]),  # symptoms
            json.loads(r[1]),  # report_data
            json.loads(r[2]),  # diagnosis
            r[3],              # risk_score
            r[4],              # priority
            r[5]               # timestamp
        ))

    return parsed_records
    
# -----------------------------
# GET ALL PATIENTS (ID + NAME)
# -----------------------------
def get_all_patients():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
    SELECT DISTINCT patient_id, name FROM patient_records
    """)

    records = c.fetchall()
    conn.close()

    return records  # [(patient_id, name)]    