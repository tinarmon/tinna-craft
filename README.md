# 🛠️ Tinna Craft

[![Version](https://img.shields.io/badge/version-1.1.0-blue.svg)](./plugin.json)
[![Platform](https://img.shields.io/badge/Antigravity-Plugin-blueviolet.svg)](https://github.com/tinarmon/tinna-craft)
[![Skills](https://img.shields.io/badge/skills-16-brightgreen.svg)](./01_tinna-craft-manual.md)

> *One portable Antigravity plugin bundling 16 battle-tested engineering skills and always-on coding guardrails.*

---

## 🌟 Highlights

- **16 Ready-to-Use Skills** covering workflow, testing, data profiling, knowledge graphs, documentation, and security
- **Feature & Test Case Tree** (`feature-test-tree`) — inspect any project, extract features, map covered vs. missing tests, and render Mermaid + offline interactive HTML trees
- **Always-On Discipline** (`rules/AGENTS.md`) — Ponytail YAGNI minimalism, Python 3.12+ (`uv`, `ruff`, `pytest`), and Next.js/TypeScript standards
- **Built-In Quality & Security Gates** — pre-completion checks (`quality-gate`), secret/air-gap protection (`LocalAISecurity`), and zero-dump CSV/Parquet profiling (`data-craft`)
- **One-Command Implant** — validate frontmatter/links and sync globally or per-workspace via `skill-implanter`

---

## ℹ️ Overview

**Tinna Craft** is a personal developer toolkit packaged as a single Antigravity plugin. Instead of copy-pasting prompts or re-explaining engineering standards across repositories, you install this plugin once and every workspace inherits consistent workflows for planning (`spec-first`), testing (`test-driven-development`, `feature-test-tree`), refactoring (`code-simplification`), documentation (`doc-craft`), and safe git hygiene (`git-craft`).

| Category | Included Skills |
|---|---|
| **Workflow & Tokens** | `spec-first`, `quality-gate`, `rtkcave-token` |
| **Coding, UI & Testing** | `python-craft`, `frontend-ui-engineering`, `code-simplification`, `test-driven-development`, `feature-test-tree` |
| **Data, Graph & Speed** | `data-craft`, `SpeedOptimizer`, `graphify` |
| **Docs & Directories** | `doc-craft`, `dir-craft` |
| **Security, Git & Setup** | `LocalAISecurity`, `git-craft`, `skill-implanter` |

For the full reference and troubleshooting guide, see [01_tinna-craft-manual.md](./01_tinna-craft-manual.md).

### ✍️ Author

Created and maintained by [@tinarmon](https://github.com/tinarmon).

---

## 🚀 Usage

Just ask your agent naturally in any workspace — no boilerplate needed:

```text
"Extract features and test case tree for this project"
```

```text
"Run the quality gate on my last change"
```

```text
"Profile this CSV without dumping it"
```

```text
"Build a knowledge graph for this codebase"
```

---

## ⬇️ Installation

**Requirements:** Antigravity installed (opened at least once) and **Python 3.12+** for helper scripts.

Clone directly into your Antigravity plugins directory and restart Antigravity:

```powershell
git clone https://github.com/tinarmon/tinna-craft.git "$HOME\.gemini\config\plugins\tinna-craft"
```

Or validate and install from an existing clone using the built-in implanter:

```powershell
python .\tinna-craft\skills\skill-implanter\scripts\implant_skills.py --verify-only
python .\tinna-craft\skills\skill-implanter\scripts\implant_skills.py
```

---

## 💭 Feedback and Contributing

Have an idea for a new skill or found a bug in one of the helper scripts?

- Open an [Issue](https://github.com/tinarmon/tinna-craft/issues) or start a [Discussion](https://github.com/tinarmon/tinna-craft/discussions).
- Before submitting a PR, run `python skills/skill-implanter/scripts/implant_skills.py --verify-only` to verify all `SKILL.md` frontmatter and relative links pass.
