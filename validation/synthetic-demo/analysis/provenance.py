"""Write explicit provenance metadata from the actual CSV and computed output."""
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
def digest(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()

raw_path = "data/temperatures.csv"
result = json.loads((ROOT / "analysis/results.json").read_text(encoding="utf-8"))
records = {}
common = {"conditions": "Artificially synthesized test data; A and B are supplied labels without physical definitions",
          "source_role": "original", "access_status": "raw-files", "verification": "verified",
          "data_status": "synthetic test data, not a physical measurement or physical simulation"}
raw_artifact = {"path": raw_path, "sha256": digest(raw_path)}
for line, row in enumerate(csv.DictReader((ROOT / raw_path).open(encoding="utf-8", newline="")), 2):
    key = row["condition"] + ".record." + row["replicate"]
    records[key] = dict(common, key=key, source_kind="raw_data", value=row["temperature_C"], unit="°C",
                        metric="synthetic temperature value", entity="synthetic condition " + row["condition"],
                        result_method="synthetic", provenance={"artifacts": [raw_artifact],
                        "locator": f"CSV line {line}, column temperature_C, condition {row['condition']}, replicate {row['replicate']}",
                        "method": "Values supplied by the user as artificial test records; read without conversion", "environment": result["environment"]})
artifacts = [raw_artifact] + [{"path": p, "sha256": digest(p)} for p in ("analysis/summarize.py", "analysis/results.json")]
for condition, values in result["conditions"].items():
    inputs = [key for key in records if key.startswith(condition + ".record.")]
    for metric, field, value_unit, formula in [
        ("arithmetic mean temperature", "mean", "°C", "sum(temperature_C for condition) / count(records for condition)"),
        ("synthetic record count", "record_count", "", "count(CSV records with condition label)")]:
        key = condition + (".mean" if field == "mean" else ".count")
        records[key] = dict(common, key=key, source_kind="derived", value=str(values[field]), unit=value_unit,
                            metric=metric, entity="synthetic condition " + condition, result_method="inferred",
                            provenance={"artifacts": artifacts, "locator": "analysis/results.json: conditions." + condition + "." + field,
                            "method": result["method"], "environment": result["environment"], "formula": formula, "inputs": inputs})
key = "B_minus_A.mean"
records[key] = dict(common, key=key, source_kind="derived", value=result["difference_B_minus_A"], unit="°C",
                    metric="difference of arithmetic mean temperatures", entity="synthetic condition B minus A", result_method="inferred",
                    provenance={"artifacts": artifacts, "locator": "analysis/results.json: difference_B_minus_A",
                    "method": result["method"], "environment": result["environment"], "formula": "B.mean - A.mean", "inputs": ["B.mean", "A.mean"]})
(ROOT / "evidence/temperature.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {len(records)} evidence records from inspected raw data and arithmetic")
