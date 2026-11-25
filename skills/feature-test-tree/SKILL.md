---
name: feature-test-tree
description: >-
  Inspect a project codebase, extract its features and sub-features, map existing test cases
  and identify missing test coverage gaps, then render both a Mermaid tree graph and an
  interactive offline HTML tree. Triggers on "feature-test-tree", "/feature-test-tree",
  "feature test tree", "test case tree", "test coverage tree", "แยก feature",
  "กราฟ test case", or "แตก test case".
triggers: feature-test-tree, feature test tree, test case tree, test coverage tree, แยก feature, กราฟ test case, แตก test case
---

# Feature & Test Case Tree

Inspect a repository, decompose it into **Project → Feature → Sub-feature → Test Cases** (both existing `covered` tests and suggested `missing` gaps), and render a **Mermaid tree graph** plus an **interactive offline HTML tree**.

---

## Step 1: Inspect Project & Tests (Read-Only)

1. Identify stack & entry points (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, routes, controllers, services, CLI commands). Skip `node_modules/`, `.venv/`, `.git/`, `dist/`, `build/`, `__pycache__/`.
2. Locate all test files (`tests/`, `__tests__/`, `*.test.*`, `*.spec.*`, `test_*.py`, `*_test.go`).
3. **Large-repo guardrail:** If source files > 200, list the top-level modules/domains first and ask the user whether to scan all modules at high level or deep-dive a specific module.

## Step 2: Extract Features & Map Test Cases (Hybrid Mode)

Build a JSON tree matching [schema-example.json](./references/schema-example.json):

- **Level 1 (`project`):** Project name + short stack summary.
- **Level 2 (`features[]`):** Domain features (e.g. `Authentication`, `Billing`, `File Upload`).
- **Level 3 (`subfeatures[]`):** Concrete user flows or modules with `source_file` (real path observed in the repo).
- **Level 4 (`tests[]`):** Atomic test cases with:
  - `id`: Unique short ID (e.g. `TC-AUTH-01`).
  - `title`: Clear behavior description.
  - `status`: `"covered"` (backed by an actual test found in Step 1) or `"missing"` (gap inferred from real code branches/edge cases).
  - `type`: `"unit"` | `"integration"` | `"e2e"`.
  - `category`: `"happy"` | `"edge"` | `"error"` | `"security"`.
  - `test_file`: Real test file path when `status == "covered"`, or `""` when `missing`.

**Honesty rules:**
- Never invent file paths or claim a test is `covered` unless you directly observed it in a test file.
- Keep test titles concise (under 60 chars) so graphs stay readable.

## Step 3: Render Graphs & Coverage Summary

Write the JSON to a temporary or output path (e.g. `.feature-test-tree.json` or `docs/feature-test-tree.json`) and run [render_tree_html.py](./scripts/render_tree_html.py):

```powershell
python "<skill_dir>/scripts/render_tree_html.py" "<input.json>" --html-out "feature-test-tree.html" --md-out "feature-test-tree.md"
```

Present to the user:
1. **Mermaid Tree** inline in your reply (from `feature-test-tree.md`, using `graph TD` by default or `--mermaid-mode mindmap` if requested).
2. **Clickable link** to `feature-test-tree.html` (interactive offline tree with search, status/type filters, expand/collapse, and file references).
3. **Coverage Gap Summary** table (`Feature | Covered | Missing | Coverage %`) and offer to implement the missing tests using `test-driven-development`.
