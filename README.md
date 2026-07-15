# Rota Web App

A Python-based shift rota calculator deployed as a static PWA on GitHub Pages.
Generates three years of shift data (2026–2028) viewable as a month-grid calendar, optimised for Android Chrome.

## Prerequisites

- [uv](https://docs.astral.sh/uv/getting-started/installation/) — manages the virtual environment and dependencies
- Python 3 (managed by uv via `.python-version`)

Install dependencies once:

```sh
uv sync
```

## Makefile targets

| Target | What it does |
|---|---|
| `make generate` | Runs `generate.py` to rebuild `docs/` from rota data |
| `make serve` | Regenerates the site then serves it locally at `http://localhost:8000` |
| `make deploy` | Regenerates the site, commits `docs/`, and pushes to the `gh-pages` branch |
| `make help` | Prints a summary of available targets |

### Generate

Rebuilds all static output in `docs/` — `index.html`, `rota.json`, manifest, and service worker.

```sh
make generate
```

### Serve

Runs a local HTTP server so you can preview the PWA in a browser before deploying.

```sh
make serve
```

Then open `http://localhost:8000` in your browser. Stop the server with `Ctrl+C`.

### Deploy

Regenerates the site, stages and commits any changes under `docs/`, then pushes that folder to the `gh-pages` branch via `git subtree`.

```sh
make deploy
```

GitHub Pages must be configured to serve from the root of the `gh-pages` branch. The live site will be available at your GitHub Pages URL shortly after the push completes.

## Rota rules

- 28-day cycle with anchor date **7 January 2026**
- Shift types: **DAYS** (07:00–17:00), **BACKSHIFT** (10:00–20:00), **OFF**

## Colour scheme

| Shift | Colour |
|---|---|
| DAYS | Amber `#F59E0B` |
| BACKSHIFT | Red `#EF4444` |
| OFF | Light grey `#F3F4F6` |
