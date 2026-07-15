# Rota Web App - Project Steering

## Project Overview
A Python-based shift rota calculator deployed as a static PWA on GitHub Pages.
Generates 3 years of shift data (2026, 2027, 2028) viewable as a month-grid calendar, optimised for Android Chrome.

## Repository
`/Users/zaza/Main/Code/Python/backshiftchecker`

## Key Files
- `Shifts.py` — core rota logic, `ShiftType` enum, `Day` class, `shids()` generator
- `generate.py` — reads rota data, writes `docs/index.html` + PWA assets
- `docs/` — static site output (served by GitHub Pages)
- `Makefile` — `make generate`, `make serve`, `make deploy`

## Rota Rules
- 28-day cycle, **anchor date: 7th January 2026** (`ANCHOR_DATE = date(2026, 1, 7)`)
- Any start date offset must be calculated as `(start_date - ANCHOR_DATE).days % 28`
- Shift types: `DAYS` (7am–5pm), `BACKSHIFT` (10am–8pm), `OFF`

## Colour Scheme
- 🟧 DAYS — amber `#F59E0B`
- 🟥 BACKSHIFT — red `#EF4444`
- ⬜ OFF — light grey `#F3F4F6`

## Target Platform
- Android Chrome (Pixel-class viewport, ~412px wide)
- Minimum 44×44px touch targets
- 16px minimum font size (prevents Chrome auto-zoom)
- PWA installable via Chrome "Add to Home Screen"

## Dependency Management
- **uv** manages the virtual environment and dependencies
- `pyproject.toml` + `uv.lock` are the source of truth
- Add packages with `uv add <package>`, run scripts with `uv run python3 generate.py`
- Key dependency: `jinja2>=3.1.6` for HTML templating
- Templates live in `templates/index.html.j2`

## Deployment
- GitHub Pages from `gh-pages` branch (pushed via `git subtree push --prefix docs origin gh-pages`)
- No build tools, no frameworks — vanilla HTML/CSS/JS only

## Commit Conventions
Use **Conventional Commits** for every meaningful change:

```
<type>(<scope>): <short description>

Types: feat, fix, refactor, chore, docs, test, style
Scope: optional, e.g. shifts, generate, ui, pwa, makefile

Examples:
  feat(shifts): add offset-aware multi-year generation
  feat(generate): serialise 3 years of rota data to JSON
  feat(ui): add month-grid calendar with amber/red colour scheme
  feat(pwa): add manifest and service worker for Android install
  chore(makefile): add generate, serve and deploy targets
  docs: add project steering doc
```

Commit after every completed task — never bundle multiple tasks into one commit.

## Task Progress
- [x] Steering doc created
- [ ] Task 1: Refactor `Shifts.py` — offset-aware multi-year generation
- [ ] Task 2: `generate.py` — serialise 3 years to `docs/rota.json`
- [ ] Task 3: Calendar HTML — Android-optimised month grid
- [ ] Task 4: PWA — manifest, service worker, icons
- [ ] Task 5: Makefile — generate, serve, deploy targets
