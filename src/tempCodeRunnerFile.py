from flask import Flask, request, render_template, redirect, url_for, flash
import os
import csv
from werkzeug.utils import secure_filename
from data_preprocessing import load_data, preprocess_data, save_processed_data
from pii_detection import detect_pii_in_notes
from deidentification import deidentify_notes
from evaluation import evaluate_pii_detection

# Initialize Flask app
app = Flask(__name__, template_folder="../templates")
app.config["SECRET_KEY"] = "your_secret_key"  # Required for flash messages

# Ensure necessary directories exist
DATA_FOLDER = 'data'
UPLOAD_FOLDER = os.path.join(DATA_FOLDER, 'uploads')
os.makedirs(DATA_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"txt", "csv"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("No file part", "error")
            return redirect(request.url)
        
        file = request.files["file"]
        if file.filename == "":
            flash("No selected file", "error")
            return redirect(request.url)

        if not allowed_file(file.filename):
            flash("Invalid file type. Only .txt and .csv are allowed.", "error")
            return redirect(request.url)

        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Process .txt files directly
        if filename.endswith(".txt"):
            with open(file_path, "r", encoding="utf-8") as f:
                raw_data = f.readlines()

            processed_data = preprocess_data(raw_data)
            pii_detected_notes = detect_pii_in_notes(processed_data)
            deidentified_notes = deidentify_notes(pii_detected_notes)

            # Save the de-identified text file
            deidentified_file_path = os.path.join(DATA_FOLDER, f"deidentified_{filename}")
            with open(deidentified_file_path, "w", encoding="utf-8") as f:
                f.writelines(deidentified_notes)

        # Process .csv files and store in uploads/
        elif filename.endswith(".csv"):
            raw_data = load_data(file_path)
            processed_data = preprocess_data(raw_data)
            pii_detected_notes = detect_pii_in_notes(processed_data)
            deidentified_notes = deidentify_notes(pii_detected_notes)

            # Save de-identified notes in CSV format
            deidentified_csv_path = os.path.join(UPLOAD_FOLDER, "deidentified_clinical_notes.csv")
            with open(deidentified_csv_path, "w", newline="", encoding="utf-8") as csvfile:
                writer = csv.writer(csvfile, delimiter=",")  # Comma-separated CSV
                writer.writerow(["SUBJECT_ID", "ROW_ID", "HADM_ID", "CATEGORY", "ADMISSION_TYPE", "DIAGNOSIS", "TEXT"])

                for idx, note in enumerate(deidentified_notes):
                    writer.writerow(["12345", str(idx+1), "67890", "Discharge Summary", "Emergency", "Generalized Condition", note])

        # Evaluate performance
        true_labels = [1, 1, 0, 1, 1]  # Replace with actual labels
        predicted_labels = [1, 1, 0, 1, 1]  # Replace with predicted labels
        precision, recall, f1 = evaluate_pii_detection(true_labels, predicted_labels)

        scores = {
            "f1": round(f1, 3),
            "precision": round(precision, 3),
            "recall": round(recall, 3)
        }

        flash("File successfully uploaded and processed.", "success")
        return render_template("index.html", original=raw_data, deidentified=deidentified_notes, scores=scores)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
