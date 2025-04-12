import os
import spacy
import logging
from spacy.tokens import Span

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Load a pre-trained spaCy model
try:
    nlp = spacy.load("en_core_web_sm")
    logging.info("✅ SpaCy model loaded successfully.")
except Exception as e:
    logging.error(f"❌ Failed to load spaCy model: {e}")
    raise SystemExit

# Define PII categories
PII_LABELS = {"PERSON", "DATE", "GPE", "ORG", "CARDINAL", "ID"}

def detect_pii(text):
    """Detects PII in a given text using spaCy."""
    if not text.strip():
        return []

    doc = nlp(text)
    pii_entities = [(ent.text, ent.label_) for ent in doc.ents if ent.label_ in PII_LABELS]
    
    return pii_entities

def detect_pii_in_notes(notes):
    """Applies PII detection to a list of clinical notes."""
    if not notes:
        logging.warning("⚠️ No clinical notes provided for PII detection.")
        return []

    pii_detected_notes = []
    for note in notes:
        pii_entities = detect_pii(note)
        pii_detected_notes.append((note, pii_entities))

    return pii_detected_notes

def ensure_file_exists(file_path):
    """Ensure the file exists; if not, create a sample clinical note."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("John Doe visited the hospital on 2023-10-01.\n")
            file.write("Patient ID: 12345, Name: Jane Smith, Location: New York.\n")
        logging.warning(f"⚠️ Sample file created: {file_path}")

if __name__ == "__main__":
    FILE_PATH = 'data/processed_clinical_notes.txt'
    
    ensure_file_exists(FILE_PATH)

    try:
        with open(FILE_PATH, 'r', encoding="utf-8") as file:
            processed_notes = file.readlines()
        
        pii_detected_notes = detect_pii_in_notes(processed_notes)

        for note, pii_entities in pii_detected_notes:
            logging.info(f"📄 Note: {note.strip()}")
            logging.info(f"🔍 PII Entities: {pii_entities}")

    except Exception as e:
        logging.error(f"❌ Error processing clinical notes: {e}")
