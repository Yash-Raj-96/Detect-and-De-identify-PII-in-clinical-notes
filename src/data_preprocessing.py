import os
import re
import csv

def load_data(file_path):
    """
    Loads data from a file (either .txt or .csv).
    - If .txt, reads line by line.
    - If .csv, extracts text from the "TEXT" column.
    """
    _, file_extension = os.path.splitext(file_path)

    if file_extension == ".txt":
        with open(file_path, "r", encoding="utf-8") as file:
            data = file.readlines()

    elif file_extension == ".csv":
        data = []
        with open(file_path, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            if "TEXT" not in reader.fieldnames:
                raise ValueError("Error: Missing 'TEXT' column in CSV file.")
            
            for row in reader:
                data.append(row["TEXT"])

    else:
        raise ValueError("Error: Unsupported file format. Only .txt and .csv are allowed.")

    return data


def preprocess_data(data):
    """
    Cleans and processes clinical text data.
    - Removes extra spaces, newlines, and special characters.
    - Ensures consistency for HIPAA compliance.
    """
    processed_data = []
    
    for line in data:
        line = line.strip()
        line = re.sub(r"\s+", " ", line)  # Normalize spaces
        line = re.sub(r"[^\w\s.,-]", "", line)  # Remove unwanted characters (except punctuation)
        processed_data.append(line)

    return processed_data


def save_processed_data(data, file_path):
    """
    Saves processed data.
    - If saving a .txt file, writes line by line.
    - If saving a .csv file, writes structured data.
    """
    _, file_extension = os.path.splitext(file_path)

    if file_extension == ".txt":
        with open(file_path, "w", encoding="utf-8") as file:
            for line in data:
                file.write(line + "\n")

    elif file_extension == ".csv":
        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["TEXT"])  # Column header
            for line in data:
                writer.writerow([line])

    else:
        raise ValueError("Error: Unsupported file format.")


if __name__ == "__main__":
    input_file = "data/raw_clinical_notes.txt"  # Change if testing with a CSV
    output_file = "data/processed_clinical_notes.txt"  # Change if saving as CSV

    raw_data = load_data(input_file)
    processed_data = preprocess_data(raw_data)
    save_processed_data(processed_data, output_file)

    print(f"Processed data saved to {output_file}")
