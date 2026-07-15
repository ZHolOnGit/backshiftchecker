"""
generate.py

Generates the static site for the rota web app.
Run this script to rebuild docs/ — called by `make generate`.

Steps:
  1. Generate 3 years of shift data from Shifts.py
  2. Write docs/rota.json (used for validation and debugging)
  3. Write docs/index.html (self-contained calendar page)
  4. Write docs/manifest.json and docs/service-worker.js (PWA)
"""

import json
import os
from datetime import date

from Shifts import shids, ShiftType

DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")
YEARS = [2026, 2027, 2028]


def ensure_docs():
    os.makedirs(DOCS_DIR, exist_ok=True)


def build_rota_data():
    """Return rota as a list of dicts serialisable to JSON."""
    all_days = shids(YEARS)
    return [
        {
            "date": day.date.isoformat(),
            "shift": day.inWork.value,
            "weekday": day.weekDay,
        }
        for day in all_days
    ]


def write_rota_json(data):
    path = os.path.join(DOCS_DIR, "rota.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  wrote {path}  ({len(data)} entries)")


def validate_rota_data(data):
    """Run basic assertions on the generated data."""
    assert len(data) == 1096, f"Expected 1096 days, got {len(data)}"

    # No date gaps
    from datetime import date, timedelta
    prev = date.fromisoformat(data[0]["date"])
    for entry in data[1:]:
        current = date.fromisoformat(entry["date"])
        assert current == prev + timedelta(days=1), f"Gap between {prev} and {current}"
        prev = current

    # All shifts valid
    valid = {"DAYS", "BACKSHIFT", "OFF"}
    for entry in data:
        assert entry["shift"] in valid, f"Invalid shift: {entry['shift']}"

    # Anchor date is DAYS
    anchor = next(e for e in data if e["date"] == "2026-01-07")
    assert anchor["shift"] == "DAYS", f"Anchor date wrong shift: {anchor['shift']}"

    # Leap day present
    leap = next((e for e in data if e["date"] == "2028-02-29"), None)
    assert leap is not None, "Leap day 2028-02-29 missing"

    # Year counts
    for year, expected in [(2026, 365), (2027, 365), (2028, 366)]:
        count = sum(1 for e in data if e["date"].startswith(str(year)))
        assert count == expected, f"{year}: expected {expected} days, got {count}"

    print("  validation OK")


if __name__ == "__main__":
    ensure_docs()
    print("Generating rota data...")
    data = build_rota_data()
    write_rota_json(data)
    print("Validating...")
    validate_rota_data(data)
    print("Done.")
