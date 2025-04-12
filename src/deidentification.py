import os
import re
import csv

def redact_dates(note):
    """
    Redacts dates from the note.
    """
    date_patterns = [
        r"\b\d{4}[-/]\d{1,2}[-/]\d{1,2}\b",  # yyyy-mm-dd or yyyy/mm/dd
        r"\b\d{1,2}[-/]\d{1,2}[-/]\d{4}\b",  # dd-mm-yyyy or dd/mm/yyyy
        r"\b\d{1,2}\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b"  # dd Month yyyy
    ]
    for pattern in date_patterns:
        note = re.sub(pattern, "[REDACTED_DATE]", note)
    return note

def redact_pii(note):
    """
    Redacts common PII from the note.
    """
    note = re.sub(r"(?i)\bPatient ID:\s*\d{4,10}\b", "Patient ID: [REDACTED_ID]", note)
    note = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[REDACTED_SSN]", note)
    note = re.sub(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b", "[REDACTED_PHONE]", note)  # Flexible phone numbers
    note = re.sub(r"\b(\d{4}[-/]\d{1,2}[-/]\d{1,2})\b", "[REDACTED_DATE]", note)  # YYYY-MM-DD, YYYY/MM/DD, YYYY/MM/DD
    note = re.sub(r"\b\d{1,2}[-\s][A-Za-z]+[-\s]\d{4}\b", "[REDACTED_DATE]", note)  # Formats like 14-February-2024, 1 Jan 2023
    note = re.sub(r"\b\d{1,2}/\d{1,2}/\d{4}\b", "[REDACTED_DATE]", note)  # MM/DD/YYYY format
    note = re.sub(r"\b\d{3,6}\b", "[REDACTED_ID]", note)
    note = re.sub(r"(?im)^Patient Name\s*[:\-]?\s*([A-Z][a-zA-Z.'-]+\s*)+", "Patient Name: [REDACTED_NAME]", note)
    #note = re.sub(r"(?i)(EMail|Email|E-Mail)\s*[:\-]?\s*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", r"\1: [REDACTED_EMAIL]", note)
    note = re.sub(r"(?i)(EMail|Email|E-Mail)\s*[:\-]?\s*[A-Za-z0-9._%+-]+(\s*|\s*example\.com)?", r"\1: [REDACTED_EMAIL]", note)
    return note

def redact_addresses(note):
    """
    Redacts addresses from the note.
    """
    note = re.sub(r"\b\d{1,5}\s\w+(\s\w+)*,\s\w+,\s\w+\b", "[REDACTED_ADDRESS]", note)
    return note

def redact_headers(note):
    """
    Redacts common section headers from the note.
    """
    section_headers = [
        "ADMISSION LABS", "MEDICINE CONSULT", "DISCHARGE SUMMARY", "PHYSICAL EXAM",
        "PAST MEDICAL HISTORY", "CHIEF COMPLAINT", "HISTORY OF PRESENT ILLNESS",
        "LAB RESULTS", "RADIOLOGY REPORT", "FAMILY HISTORY", "SOCIAL HISTORY",
        "REVIEW OF SYSTEMS", "PROGRESS NOTE", "TREATMENT PLAN", "ASSESSMENT AND PLAN",
        "RADIOLOGY"
    ]
    for header in section_headers:
        note = re.sub(rf"(?im)^{header}(\s*={1,}|:)?", "[REDACTED_SECTION]", note)
    return note

def redact_medical_terms(note):
    """
    Redacts medical terms to ensure privacy while preserving medical data.
    """
    # List of medical terms that should NOT be redacted
    preserved_terms = [
        "WBC", "RBC", "Hgb", "Hct", "MCV", "MCH", "MCHC", "RDW", "Plt Ct",
        "PT", "PTT", "INR", "CK", "CPK", "Amylase", "Calcium", "Phos", "Mg",
        "Glucose", "Lactate", "Na", "K", "Cl", "HCO3", "BUN", "Creatinine",
        "Albumin", "Bilirubin", "ALT", "AST", "Alk Phos", "LDH", "CRP", "ESR",
        "D-Dimer", "Troponin", "Ferritin", "Lipase", "Osmolality", "TIBC", "Iron",
        "Transferrin", "Uric Acid", "Vitamin D", "TSH", "T3", "T4", "HbA1c", "A1c"
    ]
    
    # List of diseases and medical conditions to redact
    diseases = [
        "hypertension", "diabetes", "aids", "hiv", "cancer", "asthma", "arthritis",
        "osteoporosis", "tuberculosis", "hepatitis", "stroke", "heart disease",
        "chronic kidney disease", "copd", "alzheimer's", "parkinson's", "epilepsy",
        "schizophrenia", "depression", "anxiety", "bipolar disorder"
    ]
    
    # List of medication-related terms to redact
    medication_patterns = [
        r"\b\d+mg\b",  # Matches dosages like "100mg"
        r"\b[A-Z][a-z]+\s\d+mg\b",  # Matches drug names with dosages like "Metformin 500mg"
        r"\b[A-Z][a-z]+\s(BD|OD|TDS|QID)\b",  # Matches drug names with frequencies like "Telmisartan OD"
        r"\b\d+\s*tablets?\b",  # Matches "100 tablets" or "1 tablet"
        r"\b\d+\s*capsules?\b",  # Matches "100 capsules" or "1 capsule"
    ]
    
    # Preserve medical terms
    for term in preserved_terms:
        note = re.sub(rf"\b{term}\b", f"[REDACTED_{term.upper()}]", note)
    
    # Redact diseases
    for disease in diseases:
        note = re.sub(rf"\b{disease}\b", "[REDACTED_DISEASE]", note, flags=re.IGNORECASE)
    
    # Redact medication-related terms
    for pattern in medication_patterns:
        note = re.sub(pattern, "[REDACTED_TABLET]", note, flags=re.IGNORECASE)
    
    return note

def redact_health_info(note):
    """
    Redacts numeric health information such as BP, HR, and other lab values.
    """
    # Redact blood pressure values like "115/80"
    note = re.sub(r"\b\d{2,3}/\d{2,3}\b", "[REDACTED_BP]", note)

    # Redact heart rate and other numeric health values like "115" or "80"
    note = re.sub(r"\b\d{1,3}\b", "[REDACTED]", note)

    # Redact specific health-related measurements like blood sugar level
    note = re.sub(r"\b\d{1,3}\.\d{1,2}\b", "[REDACTED_HEALTH_VAL]", note)

    return note

def deidentify_note(note, pii_entities):
    """
    Main function to redact PII and sensitive information from the clinical note.
    """
    note = redact_dates(note)
    note = redact_pii(note)
    note = redact_addresses(note)
    note = redact_headers(note)
    note = redact_medical_terms(note)
    note = redact_health_info(note)

    # Now redact any remaining PII entities detected
    redacted_entities = set()

    for entity, label in pii_entities:
        replacement = {
            "PERSON": "[REDACTED_NAME]",
            "DATE": "[REDACTED_DATE]",
            "GPE": "[REDACTED_LOCATION]",
            "ORG": "[REDACTED_ORG]",
            "ID": "[REDACTED_ID]",
            "SSN": "[REDACTED_SSN]",
            "PHONE": "[REDACTED_PHONE]",
            "EMAIL": "[REDACTED_EMAIL]",
            "ADDRESS": "[REDACTED_ADDRESS]",
            "FACILITY": "[REDACTED_FACILITY]",
            "MEDICAL_CONDITION": "[REDACTED_DISEASE]",
            "PROCEDURE": "[REDACTED_PROCEDURE]",
            "DEVICE": "[REDACTED_DEVICE]",
            "MEDICATION": "[REDACTED_TABLET]"
        }.get(label, "[REDACTED]")

        if entity not in redacted_entities:
            note = re.sub(rf"\b{re.escape(entity)}\b", replacement, note)
            redacted_entities.add(entity)

    note = re.sub(r"(\[REDACTED_[A-Z]+\]), \1", r"\1", note)  # Remove redundant redactions
    return note

def deidentify_notes(pii_detected_notes):
    return [deidentify_note(note, pii_entities) for note, pii_entities in pii_detected_notes]

def save_deidentified_data(deidentified_notes, file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension == ".txt":
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n\n".join(deidentified_notes))
    elif file_extension == ".csv":
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerow(["Deidentified Text"])
            for note in deidentified_notes:
                writer.writerow([note])
    elif file_extension == ".json":
        import json
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(deidentified_notes, file, ensure_ascii=False, indent=4)
    else:
        raise ValueError("Error: Unsupported file format. Only .txt, .csv, and .json are allowed.")

if __name__ == "__main__":
    pii_detected_notes = [
        (
            """Patient Name: John Doe

            Patient ID: 56789

            Date of Visit: 14-February-2024

            Physician: Dr. Priya Rao

            Location: St. John's Medical College Hospital, Bangalore, Karnataka

            Address: 1234 Elm Street, Bangalore, Karnataka

            ADMISSION LABS
            ====================
            WBC-8.4 RBC-4.43* Hgb-11.9* Hct-38.6* MCV-87 MCH-26.9*
            MCHC-30.9* RDW-17.3* Plt Ct-191

            RADIOLOGY
            ====================
            Chest X-ray normal
            BP: 115/80 HR: 80 Glucose: 8.9

            Medical History: Hypertension, Diabetes, AIDS
            Medications: Metformin 500mg BD, Telmisartan OD, 100mg tablets
            """,
            [
                ("John Doe", "PERSON"), ("56789", "ID"),
                ("14-February-2024", "DATE"), ("Priya Rao", "PERSON"),
                ("St. John's Medical College Hospital", "ORG"),
                ("Bangalore", "GPE"), ("Karnataka", "GPE"),
                ("1234 Elm Street, Bangalore, Karnataka", "ADDRESS")
            ]
        )
    ]

    deidentified_notes = deidentify_notes(pii_detected_notes)
    save_deidentified_data(deidentified_notes, "deidentified_clinical_notes.csv")

    for note in deidentified_notes:
        print(note)