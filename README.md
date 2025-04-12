# PII Detection and De-identification in Clinical Notes

This project aims to develop an NLP-based model to detect and de-identify PII in clinical notes while maintaining data integrity and ensuring compliance with privacy regulations.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yash-raj-96/pii-detection-deidentification.git
   cd pii-detection-deidentification



   pip install -r requirements.txt

   python -m spacy download en_core_web_sm
   ```


pii-detection-deidentification/
│
├── data/                             # Folder for data files
│   ├── raw_clinical_notes.csv        # Raw data uploaded by user
│   ├── processed_clinical_notes.csv  # Processed version of raw data
│   └── deidentified_clinical_notes.csv # De-identified data after PII removal
│
├── src/                              # Source code folder
│   ├── data_preprocessing.py         # Data preprocessing logic
│   ├── pii_detection.py              # PII detection logic
│   ├── deidentification.py           # De-identification logic
│   ├── evaluation.py                 # Evaluation metrics calculation
│   └── app.py                        # Flask application (main entry point)
│
├── templates/                        # Folder for HTML templates
│   └── index.html                    # HTML template for the web interface
│
├── requirements.txt                  # Python dependencies
├── README.md                         # Project overview and documentation
└── LICENSE                           # License file for your project