"""
generate.py

Generates the static site for the rota web app.
Run via: uv run python3 generate.py

Steps:
  1. Generate 3 years of shift data from Shifts.py
  2. Write docs/rota.json (debug/validation artifact)
  3. Build calendar data structure (year → month → weeks)
  4. Render docs/index.html via Jinja2 template
  5. Write docs/manifest.json and docs/service-worker.js (PWA)
"""

import calendar
import json
import os
from datetime import date

from jinja2 import Environment, FileSystemLoader
from markupsafe import Markup

from Shifts import shids, ShiftType
from make_icons import make_svg

# ── Config ────────────────────────────────────────────────────
YEARS = [2026, 2027, 2028]
DOCS_DIR = os.path.join(os.path.dirname(__file__), "docs")
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


# ── Helpers ───────────────────────────────────────────────────

def ensure_docs():
    os.makedirs(DOCS_DIR, exist_ok=True)


def build_rota_data():
    """Return rota as a flat list of dicts for JSON serialisation."""
    return [
        {
            "date": day.date.isoformat(),
            "shift": day.inWork.value,
            "weekday": day.weekDay,
        }
        for day in shids(YEARS)
    ]


def write_rota_json(data):
    path = os.path.join(DOCS_DIR, "rota.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"  wrote {path}  ({len(data)} entries)")


def validate_rota_data(data):
    """Basic assertions on generated data — fail fast if something is wrong."""
    assert len(data) == 1096, f"Expected 1096 days, got {len(data)}"

    from datetime import timedelta
    prev = date.fromisoformat(data[0]["date"])
    for entry in data[1:]:
        current = date.fromisoformat(entry["date"])
        assert current == prev + timedelta(days=1), f"Gap between {prev} and {current}"
        prev = current

    valid_shifts = {"DAYS", "BACKSHIFT", "OFF"}
    for entry in data:
        assert entry["shift"] in valid_shifts, f"Invalid shift: {entry['shift']}"

    anchor = next(e for e in data if e["date"] == "2026-01-07")
    assert anchor["shift"] == "DAYS", f"Anchor date wrong: {anchor['shift']}"

    leap = next((e for e in data if e["date"] == "2028-02-29"), None)
    assert leap is not None, "Leap day 2028-02-29 missing"

    for year, expected in [(2026, 365), (2027, 365), (2028, 366)]:
        count = sum(1 for e in data if e["date"].startswith(str(year)))
        assert count == expected, f"{year}: expected {expected} days, got {count}"

    print("  validation OK")


def build_calendar(data):
    """
    Build a nested structure for the Jinja2 template:

      [ (year, [ (month_name, [ week, ... ]), ... ]), ... ]

    Each week is a list of 7 cells (Mon–Sun).
    A cell is either None (padding) or a dict:
      { date, day, shift }
    """
    # Index data by date string for quick lookup
    by_date = {e["date"]: e for e in data}

    result = []
    for year in YEARS:
        months = []
        for month_num in range(1, 13):
            month_name = calendar.month_name[month_num]

            # calendar.monthcalendar returns weeks as lists of 7 ints (0 = no day)
            # Week starts Monday by default
            raw_weeks = calendar.monthcalendar(year, month_num)
            weeks = []
            for raw_week in raw_weeks:
                week = []
                for day_num in raw_week:
                    if day_num == 0:
                        week.append(None)
                    else:
                        d = date(year, month_num, day_num)
                        entry = by_date.get(d.isoformat())
                        week.append({
                            "date": d.isoformat(),
                            "day": day_num,
                            "shift": entry["shift"] if entry else "OFF",
                        })
                weeks.append(week)
            months.append((month_name, weeks))
        result.append((year, months))
    return result


def render_html(data, cal):
    # autoescape=False: rota_json is trusted data we generate ourselves.
    # The template outputs it inside a <script> block, not into HTML attributes,
    # so HTML-escaping quotes would break the JS — we want raw JSON.
    env = Environment(
        loader=FileSystemLoader(TEMPLATES_DIR),
        autoescape=False,
    )
    template = env.get_template("index.html.j2")
    rota_json_str = json.dumps(data, separators=(",", ":"))
    html = template.render(
        years=YEARS,
        calendar=cal,
        rota_json=Markup(rota_json_str),
    )
    return html


def write_html(html):
    path = os.path.join(DOCS_DIR, "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  wrote {path}")


def write_pwa_assets():
    """Write manifest.json, service-worker.js, and SVG icons."""
    # Icons
    for size in [192, 512]:
        path = os.path.join(DOCS_DIR, f"icon-{size}.svg")
        with open(path, "w") as f:
            f.write(make_svg(size))

    manifest = {
        "name": "Rota",
        "short_name": "Rota",
        "description": "Shift rota calendar",
        "start_url": ".",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#F59E0B",
        "icons": [
            {"src": f"icon-{s}.svg", "sizes": f"{s}x{s}", "type": "image/svg+xml"}
            for s in [192, 512]
        ],
    }
    manifest_path = os.path.join(DOCS_DIR, "manifest.json")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"  wrote {manifest_path}")

    import time
    cache_key = f"rota-{int(time.time())}"
    sw = (
        f"const CACHE = '{cache_key}';\n"
        "const ASSETS = ['./'];\n"
        "\n"
        "self.addEventListener('install', e => {\n"
        "  e.waitUntil(\n"
        "    caches.open(CACHE).then(c => c.addAll(ASSETS))\n"
        "  );\n"
        "  self.skipWaiting();\n"
        "});\n"
        "\n"
        "self.addEventListener('activate', e => {\n"
        "  e.waitUntil(\n"
        "    caches.keys().then(keys =>\n"
        "      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))\n"
        "    )\n"
        "  );\n"
        "  self.clients.claim();\n"
        "});\n"
        "\n"
        "self.addEventListener('fetch', e => {\n"
        "  e.respondWith(\n"
        "    caches.match(e.request).then(cached => cached || fetch(e.request))\n"
        "  );\n"
        "});\n"
    )
    sw_path = os.path.join(DOCS_DIR, "service-worker.js")
    with open(sw_path, "w") as f:
        f.write(sw)
    print(f"  wrote {sw_path}")


# ── Main ──────────────────────────────────────────────────────

if __name__ == "__main__":
    ensure_docs()

    print("Generating rota data...")
    data = build_rota_data()
    write_rota_json(data)

    print("Validating...")
    validate_rota_data(data)

    print("Building calendar structure...")
    cal = build_calendar(data)

    print("Rendering HTML...")
    html = render_html(data, cal)
    write_html(html)

    print("Writing PWA assets...")
    write_pwa_assets()

    print("\nDone. Preview with: uv run python3 -m http.server 8000 --directory docs")
