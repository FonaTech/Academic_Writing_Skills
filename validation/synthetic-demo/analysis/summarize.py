"""Describe the supplied synthetic values; perform no inferential test."""
import csv
import hashlib
import json
import platform
from collections import defaultdict
from decimal import Decimal
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/temperatures.csv"
rows = list(csv.DictReader(SOURCE.open(encoding="utf-8", newline="")))
groups = defaultdict(list)
for row in rows:
    groups[row["condition"]].append(Decimal(row["temperature_C"]))
means = {condition: sum(values) / len(values) for condition, values in groups.items()}
result = {
    "data_status": "artificially synthesized test data; no physical measurements",
    "method": "Arithmetic mean within condition; B mean minus A mean",
    "unit": "°C",
    "conditions": {
        condition: {"record_count": len(values), "values": [str(v) for v in values],
                    "mean": str(means[condition])}
        for condition, values in sorted(groups.items())
    },
    "difference_B_minus_A": str(means["B"] - means["A"]),
    "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
    "environment": {"python": platform.python_version(), "arithmetic": "decimal.Decimal"},
    "limitations": "Descriptive arithmetic only; no causal or statistical-significance claim"
}
(ROOT / "analysis/results.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
