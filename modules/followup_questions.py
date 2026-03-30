followup_db = {
    "fever": [
        {
            "question": "How high is the fever (°C)?",
            "type": "number"
        },
        {
            "question": "How many days have you had fever?",
            "type": "number"
        }
    ],
    "cough": [
        {
            "question": "Type of cough?",
            "type": "mcq",
            "options": ["Dry", "With mucus"]
        },
        {
            "question": "How long have you been coughing (days)?",
            "type": "number"
        }
    ],
    "chest pain": [
        {
            "question": "Does pain spread to arm or jaw?",
            "type": "yesno"
        },
        {
            "question": "Type of pain?",
            "type": "mcq",
            "options": ["Sharp", "Dull", "Burning"]
        }
    ],
    "abdominal pain": [
        {
            "question": "Where is the pain located?",
            "type": "text"
        },
        {
            "question": "Pain type?",
            "type": "mcq",
            "options": ["Continuous", "Intermittent"]
        }
    ],
    "headache": [
        {
            "question": "Headache type?",
            "type": "mcq",
            "options": ["One-sided", "Full head"]
        },
        {
            "question": "Sensitivity to light?",
            "type": "yesno"
        }
    ]
}