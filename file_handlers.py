import csv
import json
import os

STATEMENT_FIELDS = ["Date & Time", "Transaction Type", "Amount (₱)", "Balance (₱)", "Note"]

# ──────────────────// File Reader Writer //──────────────────
class FileReaderWriter:
    def read(self):
        print("This is the default read method.")

    def write(self):
        print("This is the default write method.")

# ──────────────────// JSON File Reader Writer //──────────────────
class JSONFileReaderWriter(FileReaderWriter):
    def read(self, filepath):
        with open(filepath, "r") as json_file:
            data = json.load(json_file)
            return data

    def write(self, filepath, data):
        with open(filepath, "w") as write_file:
            json.dump(obj=data, fp=write_file, indent=4)

# ──────────────────// CSV File Reader Writer //──────────────────
class CSVFileReaderWriter(FileReaderWriter):
    def read_csv(self, filepath):
        with open(filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = []
            for row in reader:
                rows.append({
                    "timestamp": row["Date & Time"],
                    "type":      row["Transaction Type"],
                    "amount":    float(row["Amount (₱)"].replace(",", "")),
                    "balance":   float(row["Balance (₱)"].replace(",", "")),
                    "note":      row["Note"]
                })
            return rows

    def append_csv(self, filepath, row: dict):
        file_exists = os.path.exists(filepath)
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=STATEMENT_FIELDS)
            if not file_exists:
                writer.writeheader()
            writer.writerow({
                "Date & Time":      row["timestamp"],
                "Transaction Type": row["type"],
                "Amount (₱)":       f"{row['amount']:,.2f}",
                "Balance (₱)":      f"{row['balance']:,.2f}",
                "Note":             row["note"]
            })
