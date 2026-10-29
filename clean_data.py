
import csv
import os
import statistics
from tkinter import Tk, filedialog

root = Tk()
root.withdraw()

path = filedialog.askopenfilename(
    title="Select titanic_original.csv",
    filetypes=[("CSV files", "*.csv")]
)
root.destroy()

if path:
    with open(path, encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames
        data = list(reader)

    # Remove duplicate rows
    unique = []
    seen = set()

    for row in data:
        key = tuple((row.get(c) or "").strip() for c in columns)
        if key not in seen:
            seen.add(key)
            unique.append(row)

    data = unique

    # Clean text values
    for row in data:
        for c in columns:
            if row.get(c) is not None:
                row[c] = row[c].strip()

        if row.get("sex"):
            row["sex"] = row["sex"].lower()

        if row.get("embarked"):
            row["embarked"] = row["embarked"].upper()

    # Convert numeric columns
    for c in ["pclass", "survived", "sibsp", "parch",
              "age", "fare", "body"]:
        for row in data:
            try:
                value = row.get(c, "").strip()
                if value:
                    number = float(value)
                    if c in ["pclass", "survived", "sibsp", "parch"]:
                        if not number.is_integer():
                            raise ValueError
                        row[c] = str(int(number))
                    else:
                        row[c] = str(number)
            except (ValueError, TypeError):
                row[c] = ""

    # Fill missing age and fare with median
    for c in ["age", "fare"]:
        values = [float(r[c]) for r in data if r.get(c)]
        if values:
            median = statistics.median(values)
            for row in data:
                if not row.get(c):
                    row[c] = str(median)

    # Replace other missing values
    for row in data:
        for c in columns:
            if not row.get(c):
                row[c] = "Unknown"

    output = os.path.join(
        os.path.dirname(path), "titanic_cleaned.csv"
    )

    with open(output, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(data)

    print("Cleaning complete!")
    print("Rows:", len(data))
    print("Saved file:", output)
else:
    print("No file selected.")
