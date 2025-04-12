import os
import logging
from data_preprocessing import load_data, preprocess_data, save_processed_data
from pii_detection import detect_pii_in_notes
from deidentification import deidentify_notes
from evaluation import evaluate_pii_detection, evaluate_deidentification

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

DATA_DIR = 'data'
RAW_FILE = os.path.join(DATA_DIR, 'raw_clinical_notes.txt')
PROCESSED_FILE = os.path.join(DATA_DIR, 'processed_clinical_notes.txt')
DEIDENTIFIED_FILE = os.path.join(DATA_DIR, 'deidentified_clinical_notes.txt')

def ensure_file_exists(file_path):
    """Ensure the file exists; if not, create a sample clinical note."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("John Doe visited the hospital on 2023-10-01.\n")
            file.write("Patient ID: 12345, Name: Jane Smith, Location: New York.\n")
        logging.warning(f"⚠️ Sample file created: {file_path}")


def main():
    logging.info("\n🚀 Starting PII Processing Pipeline...\n")

    # Step 1: Ensure Data File Exists
    ensure_file_exists(RAW_FILE)

    # Step 2: Data Preprocessing
    logging.info("🔄 Preprocessing raw clinical notes...")
    try:
        raw_data = load_data(RAW_FILE)
        processed_data = preprocess_data(raw_data)
        save_processed_data(processed_data, PROCESSED_FILE)
        logging.info(f"✅ Processed data saved: {PROCESSED_FILE}\n")
    except Exception as e:
        logging.error(f"❌ Error in data preprocessing: {e}")
        return

    # Step 3: PII Detection
    logging.info("🔍 Detecting PII in clinical notes...")
    try:
        pii_detected_notes = detect_pii_in_notes(processed_data)
        if not pii_detected_notes:
            logging.warning("⚠️ No PII detected in the notes.")
    except Exception as e:
        logging.error(f"❌ Error in PII detection: {e}")
        return

    # Step 4: De-identification
    logging.info("🛑 De-identifying detected PII...")
    try:
        deidentified_notes = deidentify_notes(pii_detected_notes)
        with open(DEIDENTIFIED_FILE, 'w') as file:
            for note in deidentified_notes:
                file.write(note + '\n')
        logging.info(f"✅ Deidentified notes saved: {DEIDENTIFIED_FILE}\n")
    except Exception as e:
        logging.error(f"❌ Error in de-identification: {e}")
        return

    # Step 5: Evaluation
    logging.info("📊 Evaluating PII detection performance...")
    try:
        true_labels = [1, 1, 0, 1]  # Replace with actual ground truth labels
        predicted_labels = [1, 0, 0, 1]  # Replace with model's predicted labels

        precision, recall, f1 = evaluate_pii_detection(true_labels, predicted_labels)
        logging.info(f"📈 PII Detection Metrics:\n   - Precision: {precision:.3f}\n   - Recall: {recall:.3f}\n   - F1-Score: {f1:.3f}\n")
    except Exception as e:
        logging.error(f"❌ Error in PII detection evaluation: {e}")

    logging.info("🧪 Evaluating de-identification accuracy...")
    try:
        true_notes = [
            "John Doe visited the hospital.",
            "Patient ID: 12345, Name: Jane Smith, Location: New York."
        ]

        accuracy = evaluate_deidentification(true_notes, deidentified_notes)
        logging.info(f"📊 De-identification Accuracy: {accuracy:.3f}\n")
    except Exception as e:
        logging.error(f"❌ Error in de-identification evaluation: {e}")

    logging.info("✅ Processing Completed!\n")


if __name__ == "__main__":
    main()
