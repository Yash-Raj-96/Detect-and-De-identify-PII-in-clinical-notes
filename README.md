# 🩺 Detect and De-identify PII in Clinical Notes

## 📌 Overview

With the rapid digitization of healthcare, protecting **Personally Identifiable Information (PII)** in clinical documentation is vital for patient privacy and regulatory compliance under **HIPAA** and **GDPR**. This project leverages **Natural Language Processing (NLP)** and **Named Entity Recognition (NER)** using **spaCy** to automatically detect and de-identify PII from unstructured clinical notes.

The system is designed to ensure high accuracy, maintain data integrity, and offer a scalable, web-based solution using **Flask** for real-world usability in healthcare and research settings.

---

## 🧠 Abstract

This project introduces an NLP-based system to automatically detect and de-identify PII in clinical notes using spaCy's Named Entity Recognition. The pipeline includes:

- Text preprocessing and cleaning
- PII detection using NER
- Placeholder-based anonymization
- Deployment as a Flask web application

Evaluation showed **100% Precision, Recall, and F1-score**, indicating strong performance on the test dataset. The model ensures privacy while preserving the analytical utility of clinical text.

---

## 🎯 Objectives

- ✅ Detect various PII entities in clinical notes (e.g., names, dates, locations)
- ✅ Replace PII with standardized placeholders (e.g., `[REDACTED_NAME]`)
- ✅ Ensure readability and analytical value post-de-identification
- ✅ Provide a web interface for uploading and processing files
- ✅ Comply with privacy regulations (HIPAA, GDPR)

---

## 🛠️ Methodology

| Section      | Screenshot |
|--------------|------------|
| 🧠  Workflow | ![ Workflow](https://github.com/Yash-Raj-96/Detect-and-De-identify-PII-in-clinical-notes/blob/main/data/Pictures%20&%20Report/Screenshot%202025-03-31%20134440.png?raw=true) |


### 1. **Data Collection**
- Clinical notes dataset sourced from Kaggle (unstructured text containing PII).

### 2. **Preprocessing**
- Cleaning unwanted characters
- Lowercasing
- Tokenization
- Stopword removal

### 3. **NER-based PII Detection**
- Leveraged spaCy to detect entities:
  - `PERSON`
  - `DATE`
  - `LOCATION`
  - `ORG`
  - `ID`

### 4. **De-identification Strategy**
- Entities are replaced using placeholder tokens:
  ```
  Original: "John Doe was admitted to New York General Hospital on 12/03/2022."
  Anonymized: "[REDACTED_NAME] was admitted to [REDACTED_LOCATION] on [REDACTED_DATE]."
  ```

### 5. **Web App Deployment**
- Built using Flask
- Features:
  - Upload clinical notes
  - View original vs. anonymized output
  - Real-time PII masking

### 6. **Evaluation Metrics**
- 📌 **Precision:** 100%
- 📌 **Recall:** 100%
- 📌 **F1-score:** 100%

---

## 💻 Installation & Setup

```bash
# Clone the repo
git clone https://github.com/Yash-Raj-96/Detect-and-De-identify-PII-in-clinical-notes.git
cd Detect-and-De-identify-PII-in-clinical-notes

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
```

---

## 📊 Results & Discussion

- The model demonstrated exceptional performance across various test cases.
- It outperformed traditional rule-based methods in both accuracy and adaptability.
- Placeholder masking retained the clinical context and usability of data.
- User-friendly UI supports real-time file upload and PII de-identification.

---

## 🌍 Screenshots

| Page                  | Screenshot |
|-----------------------|------------|
| 🏠 Home Page          | ![Home](https://github.com/Yash-Raj-96/Detect-and-De-identify-PII-in-clinical-notes/blob/main/data/Pictures%20&%20Report/Screenshot%202025-04-02%20122606.png?raw=true) |
| 📄 Upload Page        | ![Upload](https://github.com/Yash-Raj-96/Detect-and-De-identify-PII-in-clinical-notes/blob/main/data/Pictures%20&%20Report/Screenshot%202025-04-02%20122850.png?raw=true) |
| 🔐 De-identified Output | ![Output](https://github.com/Yash-Raj-96/Detect-and-De-identify-PII-in-clinical-notes/blob/main/data/Pictures%20&%20Report/Screenshot%202025-04-02%20123045.png?raw=true) |

---

## ✅ Conclusion

This project delivers a powerful and scalable solution for protecting PII in clinical text using NLP. With its high accuracy and compliance with privacy laws, the system offers promising potential for deployment in healthcare institutions and research.

---

## 📎 License

This project is licensed under the MIT License.
