import os
import csv
import json
from collections import defaultdict

# Directory containing your CSVs
# Directory containing your CSVs
CSV_DIR = "../synthea/output/csv/"
OUTPUT_DIR = "../resources/schemas/"
SAMPLE_SIZE = 2

# Basic type inference function
def infer_type(values):
    is_float = True
    is_int = True
    for v in values:
        if v == "" or v.lower() == "null":
            continue
        try:
            int(v)
        except ValueError:
            is_int = False
        try:
            float(v)
        except ValueError:
            is_float = False

    if is_int:
        return "int"
    elif is_float:
        return "float"
    else:
        return "string"

# Ensure output dir exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Loop through CSV files
for file in os.listdir(CSV_DIR):
    if not file.endswith(".csv"):
        continue

    path = os.path.join(CSV_DIR, file)
    with open(path, newline='', encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        headers = next(reader)
        samples = list(reader)[:SAMPLE_SIZE]

    # Create column-wise sample list
    col_samples = defaultdict(list)
    for row in samples:
        for i, val in enumerate(row):
            if i < len(headers):
                col_samples[headers[i]].append(val)

    # Infer field types
    fields = []
    for col in headers:
        field_type = infer_type(col_samples[col])
        fields.append({
            "name": col.strip(),
            "type": field_type
        })

    # Create Avro schema
    base_name = os.path.splitext(file)[0]
    schema = {
        "type": "record",
        "name": base_name.capitalize(),
        "namespace": "com.yourcompany.schemas",
        "fields": fields
    }

    # Write to .avsc
    out_path = os.path.join(OUTPUT_DIR, f"{base_name}.avsc")
    with open(out_path, "w") as f:
        json.dump(schema, f, indent=2)

    print(f"Generated schema for {file} → {out_path}")
