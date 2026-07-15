.PHONY: help generate serve deploy

UV := uv run python3

# ── Default target ────────────────────────────────────────────
help:
	@echo ""
	@echo "  Rota - available targets:"
	@echo ""
	@echo "    make generate   Regenerate docs/ from rota data"
	@echo "    make serve      Preview the site at http://localhost:8000"
	@echo "    make deploy     Regenerate and push to GitHub Pages"
	@echo ""

# ── Regenerate the static site ────────────────────────────────
generate:
	$(UV) generate.py

# ── Local preview ─────────────────────────────────────────────
serve: generate
	$(UV) -m http.server 8000 --directory docs

# ── Deploy to GitHub Pages ────────────────────────────────────
# Pushes the docs/ folder to the gh-pages branch.
# GitHub Pages must be configured to serve from that branch root.
deploy: generate
	git add docs/
	git commit -m "chore(deploy): regenerate static site" || echo "  nothing to commit"
	git subtree push --prefix docs origin gh-pages
