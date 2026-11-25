# tinna-craft — User Manual (คู่มือ)

Your personal Antigravity toolkit, packaged as **one plugin**: 17 skills + your global rules.
This folder is the **master copy**. Keep it in git; install it on any computer in a few minutes.

---

## 1. What's inside

```text
tinna-craft/
├── plugin.json                 # plugin manifest (name, description, prompts)
├── 01_tinna-craft-manual.md    # this file
├── rules/AGENTS.md             # always-on: global directives + Ponytail + Python/AI/C++ + Web rules
└── skills/                     # 17 skills
```

| Category | Skills |
|---|---|
| Workflow & tokens | `spec-first`, `quality-gate`, `rtkcave-token` |
| Coding, UI, testing | `python-craft`, `frontend-ui-engineering`, `code-simplification`, `test-driven-development`, `feature-test-tree` |
| Data, graph, speed | `data-craft`, `SpeedOptimizer`, `graphify` |
| Docs, Thai Word, dirs | `thai-docx-polisher`, `doc-craft`, `dir-craft` |
| Security, git, install | `LocalAISecurity`, `git-craft`, `skill-implanter` |

GSD (the 72 `gsd-*` skills + `gsd-*` agents) is **not** in this plugin. It stays in
`~/.gemini/config/skills` and `~/.gemini/config/agents` and is installed by the GSD installer.

---

## 2. Install on a new computer

Requirements: Antigravity installed and opened once (creates `~/.gemini/config`). Python 3.12+ only if you use the implanter.

```powershell
# 1. Get this folder (clone the project that contains it)
git clone <your-repo-url>
cd <repo>

# 2a. Simplest: copy the folder into the plugins directory
Copy-Item -Recurse -Force .\tinna-craft "$HOME\.gemini\config\plugins\"

# 2b. OR use the implanter (validates first, then copies)
python .\tinna-craft\skills\skill-implanter\scripts\implant_skills.py --dry-run
python .\tinna-craft\skills\skill-implanter\scripts\implant_skills.py
```

3. **Restart Antigravity.** New plugin folders are only discovered on startup.
4. Check: Plugins page → **Tinna Craft** should list 17 skills and 1 rule.

Optional — reinstall GSD on that computer with its own installer (not part of this plugin).

---

## 3. Update a skill or rule

Edit the **master copy** (this folder in the project), never the installed copy, then push:

```powershell
python .\tinna-craft\skills\skill-implanter\scripts\implant_skills.py --verify-only   # frontmatter + link check
python .\tinna-craft\skills\skill-implanter\scripts\implant_skills.py                 # re-install
git add tinna-craft; git commit -m "chore(tinna-craft): update <skill>"
```

- New skill → `skills/<name>/SKILL.md` with `name:` + `description:` frontmatter.
- New always-on rule → append to `rules/AGENTS.md` (plain markdown, no frontmatter).
- Bump `version` in `plugin.json` when you change things.

> [!WARNING]
> The implanter **replaces** each installed skill folder with the master copy. Edits made directly in
> `~/.gemini/config/plugins/tinna-craft` will be overwritten. Removed skills are **not** deleted from the
> installed copy — delete those by hand.

---

## 4. Turn on / off, uninstall

| Action | How |
|---|---|
| Disable / enable all 16 skills + rules | Plugins page → Tinna Craft → toggle (no restart) |
| Uninstall | Delete `~/.gemini/config/plugins/tinna-craft`, then restart |

---

## 5. Rules of thumb

- **Never** copy these skills into `~/.gemini/config/skills/`. Two skills with the same name collide and one is dropped silently.
- The old master vault (`proud-brahmagupta\สกิลAI ตามประเภทการใช้งาน\.agents\`) is **stale**. Its old implanter writes to `config/skills` and would create duplicates — do not run it. This folder replaces it.
- Don't put secrets in skills or rules; this folder is meant to live in git.

---

## 6. Troubleshooting

| Symptom | Fix |
|---|---|
| Plugin not shown | Restart Antigravity; check `plugin.json` exists at `~/.gemini/config/plugins/tinna-craft/plugin.json` |
| A skill missing | `--verify-only` to find bad frontmatter; check no duplicate name in `~/.gemini/config/skills` |
| Rules not applied | Plugin disabled? Check the toggle on the Plugins page |
| Plugin comes back disabled after reinstall | Enable it on the Plugins page (old enablement state is remembered) |

---

## 7. Overlap with GSD (checked 2026-10-19)

No name collisions. GSD skills are workflow steps that need a `.planning/` project; these skills are standalone and work in any repo.
Closest pairs — keep both:

| Yours | GSD | Difference |
|---|---|---|
| `graphify` | `gsd-graphify` | GSD's is off by default, needs `.planning/config.json` + gsd-tools; yours runs anywhere |
| `spec-first` | `gsd-spec-phase` | GSD writes a phase SPEC inside its roadmap; yours writes `specs/YYYY-MM-DD-slug.md` for any task |
| `quality-gate` | `gsd-verify-work` | GSD = conversational UAT of a phase; yours = lint/type/test gate before "done" |
| `doc-craft` | `gsd-docs-update` | Similar goal; yours adds ADRs + `0N_` versioning |
| `test-driven-development` | `gsd-add-tests` | GSD adds tests after a phase; yours drives red-green-refactor |
| `git-craft` | `gsd-ship` / `gsd-pr-branch` | GSD = PR flow; yours = commits, secret screening, CHANGELOG |
