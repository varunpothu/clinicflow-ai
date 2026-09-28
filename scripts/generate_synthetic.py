import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = ROOT / "data" / "synthetic" / "clinic.json"
target = ROOT / "data" / "synthetic" / "generated_summary.json"

data = json.loads(source.read_text(encoding="utf-8"))
summary = {
    "clinic": data["clinic"]["name"],
    "timezone": data["clinic"]["timezone"],
    "clinician_count": len(data["clinicians"]),
    "appointment_type_count": len(data["appointment_types"]),
}
target.write_text(json.dumps(summary, indent=2) + "
", encoding="utf-8")
print(f"Wrote {target}")
