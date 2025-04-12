import re
from sklearn.metrics import precision_score, recall_score, f1_score

def evaluate_pii_detection(true_labels, predicted_labels):
    """
    Evaluates PII detection performance using precision, recall, and F1-score.
    Ensures a minimum threshold of 0.9 for HIPAA compliance.
    """
    if not true_labels or not predicted_labels:
        raise ValueError("Error: True and predicted labels must not be empty.")

    precision = precision_score(true_labels, predicted_labels, average='weighted', zero_division=0)
    recall = recall_score(true_labels, predicted_labels, average='weighted', zero_division=0)
    f1 = f1_score(true_labels, predicted_labels, average='weighted', zero_division=0)

    # HIPAA threshold warning
    if f1 < 0.9:
        print("⚠️ Warning: F1-score is below the recommended threshold for HIPAA compliance (0.9)")

    return round(precision, 3), round(recall, 3), round(f1, 3)


def evaluate_deidentification(true_notes, deidentified_notes):
    """
    Evaluates de-identification effectiveness by ensuring all PII is fully redacted.
    - Checks if expected PII terms are correctly removed.
    - Computes an accuracy score based on full redaction.
    """
    if len(true_notes) != len(deidentified_notes):
        raise ValueError("Error: Mismatch in the number of true vs. deidentified notes.")

    correct_deidentifications = 0
    total_notes = len(true_notes)

    pii_patterns = [
        r"\b\d{4,10}\b",  # ID numbers (e.g., "56789", "123456789")
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2}, \d{4}\b",  # Dates (e.g., "March 3, 2024")
        r"\b(?:Dr\.?|Mr\.?|Mrs\.?|Ms\.?|Miss)\s[A-Z][a-z]+\b",  # Names (e.g., "Dr. Smith")
        r"\b[A-Z][a-z]+ Hospital\b",  # Hospital/Organization names (e.g., "St. Mary's Hospital")
        r"\b[A-Z][a-z]+,?\s[A-Z]{2}\b",  # Locations (e.g., "New York, NY")
        r"\b\d{3}-\d{2}-\d{4}\b",  # Social Security Number (SSN) format
        r"\b\d{10}\b",  # Phone numbers (e.g., "5551234567")
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",  # Email addresses
    ]

    for true_note, deidentified_note in zip(true_notes, deidentified_notes):
        pii_detected = any(re.search(pattern, true_note) for pattern in pii_patterns)
        pii_removed = not any(re.search(pattern, deidentified_note) for pattern in pii_patterns)

        if pii_detected and pii_removed:
            correct_deidentifications += 1

    accuracy = correct_deidentifications / total_notes if total_notes > 0 else 0
    return round(accuracy, 3)


if __name__ == "__main__":
    # Example PII detection evaluation (Replace with real data)
    true_labels = [1, 1, 0, 1, 1, 0, 1]  # 1 = PII present, 0 = No PII
    predicted_labels = [1, 1, 0, 1, 1, 1, 1]  # Model's predictions

    precision, recall, f1 = evaluate_pii_detection(true_labels, predicted_labels)
    print(f"🔍 PII Detection - Precision: {precision}, Recall: {recall}, F1-Score: {f1}")

    # Example de-identification evaluation (Replace with real patient notes)
    true_notes = [
        "Patient Name: John Doe\nDate of Visit: March 3, 2024\nHospital: St. Mary's Hospital",
        "Patient ID: 123456789\nDr. Smith attended the case in New York.",
        "Patient's contact: (555) 123-4567. Follow-up scheduled for April 5, 2024.",
        "Email: johndoe@email.com, SSN: 123-45-6789"
    ]

    deidentified_notes = [
        "Patient Name: [REDACTED_NAME]\nDate of Visit: [REDACTED_DATE]\nHospital: [REDACTED_ORG]",
        "Patient ID: [REDACTED_ID]\nDr. [REDACTED_NAME] attended the case in [REDACTED_LOCATION].",
        "Patient's contact: [REDACTED_PHONE]. Follow-up scheduled for [REDACTED_DATE].",
        "Email: [REDACTED_EMAIL], SSN: [REDACTED_SSN]"
    ]

    accuracy = evaluate_deidentification(true_notes, deidentified_notes)
    print(f"🛡️ De-identification Accuracy: {accuracy}")
