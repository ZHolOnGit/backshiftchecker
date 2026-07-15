"""Generate SVG icons for the PWA manifest."""
import json
import os

DOCS = os.path.join(os.path.dirname(__file__), "docs")


def make_svg(size):
    r = size // 2
    font = int(size * 0.42)
    corner = int(size * 0.22)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 {size} {size}">'
        f'<rect width="{size}" height="{size}" rx="{corner}" fill="#F59E0B"/>'
        f'<text x="{r}" y="{r + int(font * 0.38)}" text-anchor="middle" '
        f'font-family="system-ui,sans-serif" font-size="{font}" font-weight="700" fill="white">R</text>'
        f"</svg>"
    )


if __name__ == "__main__":
    os.makedirs(DOCS, exist_ok=True)

    for size in [192, 512]:
        path = os.path.join(DOCS, f"icon-{size}.svg")
        with open(path, "w") as f:
            f.write(make_svg(size))
        print(f"  wrote {path}")

    # Update manifest to use SVG icons (widely supported on Android Chrome)
    manifest_path = os.path.join(DOCS, "manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path) as f:
            manifest = json.load(f)
        manifest["icons"] = [
            {"src": f"icon-{s}.svg", "sizes": f"{s}x{s}", "type": "image/svg+xml"}
            for s in [192, 512]
        ]
        with open(manifest_path, "w") as f:
            json.dump(manifest, f, indent=2)
        print(f"  updated {manifest_path} to use SVG icons")
