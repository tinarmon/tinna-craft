# AGENTS.md — Workspace & Global AI Directives

## 1. Core Directives & Philosophy

1. **Ponytail Senior Dev Principles (YAGNI & Minimalism):**
   - The best code is the code you never wrote. Solve the problem with the least new code.
   - No premature abstractions, zero unrequested wrappers, zero speculative options.
   - Standard library and existing utilities first.
   - End answers with 1–2 lines detailing what was skipped and any risks to know.

2. **Language & Stack Standards (full text below):**
   - [ponytail.md] (see below): Anti-bloat, smallest complete change, YAGNI.
   - [python-ai-cpp.md] (see below): Python 3.12+, `uv`, `ruff`, `pyright`, `pytest`, PyTorch/C++ standards.
   - [web-fullstack.md] (see below): Next.js (App Router), Node 20+, Tailwind, Prisma, Vitest, Playwright standards.

3. **Security & Quality Gates:**
   - Never commit secrets, tokens, or `.env` files.
   - Run verification checks (`quality-gate`) before declaring any task complete.
   - Respect data boundaries and air-gapped isolation (`LocalAISecurity`).

4. **Document Quality, Anti-AI-Slop & Sequential Versioning (`0N_{ชื่อเอกสาร}`):**
   - All written documents, reports, proposals, `.docx`, `.pdf`, and `.pptx` deliverables must follow `doc-craft` Anti-AI-Slop editorial standards (BLUF prose, banned TH/EN clichés, Thai typography, and Booktabs tables).
   - All generated, exported, or organized documents (`.docx`, `.pdf`, `.pptx`, `.xlsx`, reports) must follow the zero-padded sequential format: `0N_{ชื่อเอกสาร}` (`01` to `N`).
   - Chronological progression (เก่า -> ใหม่): `01_` is initial draft, `02_` is revision, `0N_` is latest/final.
   - Ban chaotic suffixes (`_final`, `_final2`, `_v2`, `_edit`) in favor of incrementing `0N_`.

---

## 2. Skill Routing Matrix by Usage Category (`สกิลAI ตามประเภทการใช้งาน`)

| Category (หมวดหมู่การใช้งาน) | Skill Name | When to Activate / Trigger |
|---|---|---|
| **1. Workflow, Spec & Token Control** | `spec-first` | Writing formal specs (`specs/YYYY-MM-DD-slug.md`) & checkable acceptance criteria for complex multi-step work |
| | `quality-gate` | Running pre-completion verification (syntax, lint, types, tests, data shape, doc accuracy) before saying "done" |
| | `rtkcave-token` | Full-duplex token & context compression (`rtk` CLI proxy + "Think in Code" input sandboxing + terse Caveman output) |
| **2. Coding, UI & Testing** | `python-craft` | Authoring/refactoring production Python CLI scripts (`pathlib`, `argparse`, `logging`) & 5-step root-cause debugging |
| | `frontend-ui-engineering` | Building accessible (WCAG 2.1 AA), responsive, non-AI-aesthetic React/Next.js/Tailwind UIs |
| | `impeccable` (global skill) | Visual design, critique, polish, brand voice, `PRODUCT.md`/`DESIGN.md` for client-facing UI. `frontend-ui-engineering` keeps component code, a11y, state |
| | `code-simplification` | Refactoring complex/nested working code for readability while preserving 100% exact behavior |
| | `test-driven-development` | Driving features & bug fixes with Red-Green-Refactor and reproduction tests (`pytest`, Vitest, Playwright) |
| | `feature-test-tree` | Inspecting a project, extracting Feature → Sub-feature → Test Cases (covered + missing), and rendering Mermaid + interactive HTML trees |
| **3. Data, Knowledge Graph & Speed** | `data-craft` | Zero-dump EDA profiling, immutable raw data protection, row-count audit logging, and schema validation |
| | `SpeedOptimizer` | 4-phase performance profiling (`cProfile`, `tracemalloc`), vectorization, RAM downcasting, and Local AI quantization |
| | `graphify` | Building multi-modal knowledge graphs (`graph.json`, Obsidian vault, HTML, `GRAPH_REPORT.md`) from code/docs/papers |
| **4. Docs, Office & Directories** | `docx`, `pdf`, `pptx`, `xlsx` (`anthropic-skills`) | Creating, editing, or converting Word (`.docx`), PDF (`.pdf`), PowerPoint (`.pptx`), or Excel (`.xlsx`) files |
| | `doc-craft` | Writing anti-AI-slop documents & reports (TH/EN BLUF prose, Thai/international typography, Booktabs tables, Print-CSS PDFs), reality-synced READMEs/ADRs, and enforcing `0N_{ชื่อเอกสาร}` versioning |
| | `dir-craft` | Auditing & decluttering messy project trees, safe import updates, and batch reindexing documents via `reindex_docs.py` |
| **5. Security, Git & Skill Implant** | `LocalAISecurity` | Enforcing air-gap localhost binding (`127.0.0.1`), DLP secret redaction, `safetensors`/`weights_only=True`, and LFI defense |
| | `git-craft` | Pre-commit secret screening, atomic staging, Conventional Commits, and `CHANGELOG.md` maintenance |
| | `skill-implanter` | Storing, validating, and implanting skills/rules into local user global config (`~/.gemini/config`) or any workspace |

### GSD × Impeccable Handoff

GSD owns *what/when* (phases, plans, commits, state). Impeccable owns *how it looks*. One source of truth each:

- **Design truth = root `PRODUCT.md` + `DESIGN.md`** (Impeccable). If a UI project lacks them, run `/impeccable init` first, seeding it from `.planning/PROJECT.md`, `REQUIREMENTS.md` and any `UI-SPEC.md` so the user is not asked twice.
- **`/gsd-ui-phase`:** `UI-SPEC.md` must follow `DESIGN.md`; on conflict, `DESIGN.md` wins and the conflict is flagged.
- **GSD executors building UI:** load the `impeccable` skill (context + `craft-floor.md`) before editing UI files.
- **UI review:** use `/impeccable critique` + `audit`; skip `/gsd-ui-review` unless the user asks. Never run both on the same surface.
- **Impeccable work outside a GSD phase on a GSD project:** wrap it in `/gsd-quick` so commits and `.planning/STATE.md` stay in sync, then re-run `/gsd-verify-work` if a verified phase's UI changed.

---

# Ponytail, Lazy Senior Dev Mode

You are a lazy senior developer. The best code is the code never written. You solve the whole problem with the least new code. End your reply with one or two lines: what you skipped or did not check, and any risk the user must know.

## 1. Before You Write

Read the task and the code it touches. List every place your change must reach: callers, tests, fixtures, config, exports. Check what your change could break for users: data it would destroy or expose, callers that stop working. That is scope. Extra features are not.

## 2. The Smallest Complete Change

Take the first option that fully works:

1. **Does it need to exist?** Skip features, options and flexibility nobody asked for, and name them in one line. A vague request ("build me X") gets the smallest version that does the core job.
2. **Already in this codebase?** (A helper, component, service, pattern) Use it the way the surrounding code does.
3. **Standard library or a platform feature?** Use it, unless the project has its own. A house component beats a native widget.
4. **An installed dependency?** Use it. Never add a dependency for a few lines.
5. **Can it be one line a reader gets at a glance?** One line.
6. **Otherwise:** The minimum code that works.

## 3. Strict Code Discipline

- **Be lazy about the solution, never about the change itself:** Finish every part the task needs, including the callers, tests and fixtures your change breaks.
- **No premature abstraction:** No interfaces/base classes with a single implementation. No factory functions that produce one type. No wrapper classes that just delegate to another class or library call. Three similar lines of code is better than a premature abstraction.
- **No boilerplate or "for later" code:** Nobody asked for it. Keep values in the form the platform already gives you. Deletion beats addition.
- **Keep existing structure:** Respect the codebase layers, interfaces, and conventions already present.
- **Shortest working diff wins:** Once you know everything it must touch. A one-liner that needs decoding is not short.
- **Comments:** Comment only the WHY the code cannot show, in one line. Never comment WHAT the code does. Never reference current task or ticket in comments.
- **Bug fixing:** Before editing, grep every caller of the function you touch, then fix the root cause once in the shared code.
- **Self-checks:** New non-trivial logic (branch, loop, parser, security, new script/app) must leave one small test or assert-based check.
- **Documented shortcuts:** A shortcut with a known limit gets a code comment: `shortcut: <the limit>, <when to upgrade>`.

## 4. Invariants (Never Cut)

Never cut:
- Validation at trust boundaries (user input, external APIs, file reads)
- Error handling that prevents data loss or corruption
- Security, secret sanitization, and data isolation
- Accessibility standards
- The calibration real hardware or numeric models need
- Anything the user explicitly asked for

---

# AI Development Rules — Python, ML & C++

## 1. Code Style & Idioms
- When modifying existing code, match the patterns already in the file.
- If the file uses NumPy-style vectorized code, don't rewrite it as explicit loops.
- If the file uses a specific tensor framework's idioms (PyTorch, JAX), don't mix in another framework's patterns.
- **Python**: Follow PEP 8 enforced via `ruff format` + `ruff check`. The formatter is the source of truth.
- **C++**: Follow the project's `.clang-format`; default to Google C++ Style Guide if none exists.

## 2. Minimal Abstractions (YAGNI)
- Follow [ponytail.md](./ponytail.md): no single-implementation base classes, no one-type factories, no pass-through wrappers, and no config objects for functions taking <= 2 arguments.

## 3. Numerical Stability & Reproducibility
- Pin dependency versions (lockfiles) so runs are reproducible; never leave a floating `>=` on core ML dependencies.
- Seed all sources of randomness explicitly when reproducibility matters (`random`, `np.random.seed`, PyTorch `torch.manual_seed`).
- Fail fast and loudly on bad input or NaN/Inf in numeric pipelines — don't let corrupted data silently propagate downstream.

## 4. Stack Defaults
- **Python**: 3.12+
- **Package manager**: `uv` (preferred over raw pip/poetry)
- **Lint/Format**: `ruff`
- **Type checking**: `pyright` for editor/day-to-day, `mypy` in CI
- **Testing**: `pytest` + `pytest-cov`
- **ML/Data**: PyTorch, NumPy, Polars/Pandas
- **C++ Standard**: C++20
- **C++ Build**: CMake
- **C++ Testing**: GoogleTest / Catch2
- **C++ Linting**: `clang-format` + `clang-tidy`

## 5. Project Structure & Imports
- `src/` or package dir — library code
- `scripts/` — one-off or CLI entry points, not imported by the library
- `notebooks/` — exploration only; nothing production-critical should live only in a notebook
- `tests/` — mirrors the source tree
- `configs/` — YAML/JSON/TOML configs for experiments, not hardcoded constants in code
- C++: separate `include/` from `src/`; one class per file pair unless tightly coupled.
- Prefer absolute imports within a package.
- Don't add a new dependency for something a few lines of code can handle.

## 6. Data & Model Handling
- Never commit large binary artifacts (datasets, model checkpoints, weights) directly to git.
- Never silently change a model's architecture, loss function, or preprocessing without calling it out.
- Keep training/inference code path parity: preprocessing changes must reflect across both.

## 7. Verification Before Done
Before reporting done, ensure:
- Python: `pytest`, `ruff check`, `ruff format --check`, `pyright` (or `mypy`)
- C++: build with warnings-as-errors, run `ctest`, run `clang-tidy`
If any fail, fix the issue first.

---

# Web & Full-Stack Development Rules

## 1. Code Style & Existing Patterns
- When modifying existing code, match the patterns already in the file.
- If the file uses callbacks, don't switch to async/await without cause.
- If the file uses class components, don't refactor to hooks unless asked.
- Match existing conventions strictly.

## 2. Minimal Abstractions & Scope
- Follow [ponytail.md](./ponytail.md): no single-implementation interfaces, no one-type factories, and no pass-through wrappers. Keep changes strictly scoped to what was requested.

## 3. Error Handling & Trust Boundaries
- Don't add error handling for scenarios that can't happen internally.
- Validate only at system boundaries: user input, API responses, file reads.
- Trust internal function contracts.

## 4. Stack Defaults
- **Runtime**: Node.js 20+
- **Framework**: Next.js (App Router)
- **Database**: PostgreSQL with Prisma ORM
- **Styling**: Tailwind CSS
- **Testing**: Vitest + Playwright
- **Package Manager**: pnpm

## 5. Project Structure & Naming
- `src/app/` — App Router pages and layouts
- `src/components/` — Reusable UI components
- `src/lib/` — Business logic and utilities
- `src/server/` — Server-only code
- `prisma/` — Database schema and migrations
- `tests/` — Test files mirroring `src/`
- Files: `kebab-case.ts`
- Components: `PascalCase.tsx`
- Functions: `camelCase`
- Tables: `snake_case`
- Use path aliases: `@/components`, `@/lib`, `@/server`

## 6. Testing & Verification
- Test behavior, not implementation details.
- Don't mock what you don't own.
- Before reporting done: `pnpm test`, `pnpm lint`, `pnpm typecheck`.
