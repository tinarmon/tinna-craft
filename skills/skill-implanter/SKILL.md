---
name: skill-implanter
description: >-
  Use this skill to store, validate, sync, and implant AI skills and rules from the
  tinna-craft plugin master copy into the local user's global Antigravity plugin
  (~/.gemini/config/plugins/tinna-craft) or into any project workspace
  (.agents/). Triggers on "implant skill", "install global skills", "ฝังสกิล",
  "ติดตั้งสกิล global", "sync skills", or "update global skills".
triggers: skill-implanter, implant skill, install global skills, sync skills, ฝังสกิล, ติดตั้งสกิล global
---

# Skill Implanter: Store, Validate & Implant the tinna-craft Plugin

Validates frontmatter and relative links, then copies the `tinna-craft` plugin from its master copy into `~/.gemini/config/plugins/tinna-craft/` (active in every workspace on this machine) or into a specific project's `.agents/` directory.

---

## 1. Architecture & Discovery Paths

| Scope | Target Path (Windows) | Purpose |
|---|---|---|
| **Master Copy (Storage)** | `<project>\tinna-craft\` (e.g. `C:\Users\tinna\Documents\antigravity\quirky-volta\tinna-craft\`) | Source of truth, carried between computers via git |
| **Global Plugin (Implant)** | `C:\Users\tinna\.gemini\config\plugins\tinna-craft\` | Active across **all** workspaces; toggle on/off as one unit |
| **KiroCrew Sync (Auto)** | `C:\Users\tinna\.kiro\steering\tinna-craft.md` & `~/.kiro/crew/config.json` | Mirrors `AGENTS.md` (as `inclusion: always` steering) and registers `skills.extra_paths` |
| **Workspace Local** | `<workspace>\.agents\skills\` & `<workspace>\.agents\rules\` | Project-specific override / VCS-shareable pack |

Plugin layout:

```text
tinna-craft/
├── plugin.json
├── rules/AGENTS.md        # always-on global directives + Ponytail/Python/Web rules
└── skills/<skill>/SKILL.md
```

> Do NOT copy these skills into `~/.gemini/config/skills/` — a second copy with the same name collides and one is silently dropped. That folder belongs to GSD.

---

## 2. Step-by-Step Procedure

### Step 1: Store or Update a Skill in the Master Copy
1. Place the skill inside `tinna-craft/skills/<skill-name>/SKILL.md`.
2. Ensure the `SKILL.md` starts with valid YAML frontmatter:
   ```yaml
   ---
   name: <skill-name>
   description: >-
     Clear third-person description of what the skill does and when to trigger it (include Thai/English trigger phrases).
   triggers: <skill-name>, english trigger, คำค้นภาษาไทย
   ---
   ```
   > Keep `triggers:` on a single unquoted line at column 0 so KiroCrew's `SKILL_LOADER` frontmatter parser reads it reliably.
3. Place helper scripts in `skills/<skill-name>/scripts/` and reference docs in `skills/<skill-name>/references/`, linked via relative markdown links (`./scripts/...`, `./references/...`).
4. Global rules go in `tinna-craft/rules/AGENTS.md` (plain markdown, no frontmatter).

### Step 2: Validate All Skills (Frontmatter & Link Check)
Run [implant_skills.py](./scripts/implant_skills.py) from the master copy with `--verify-only`:
```powershell
python "tinna-craft/skills/skill-implanter/scripts/implant_skills.py" --verify-only
```

### Step 3: Implant into the Global Plugin
```powershell
# Preview:
python "tinna-craft/skills/skill-implanter/scripts/implant_skills.py" --dry-run

# Implant to ~/.gemini/config/plugins/tinna-craft (and sync KiroCrew if present):
python "tinna-craft/skills/skill-implanter/scripts/implant_skills.py"

# Skip KiroCrew steering/extra_paths sync:
python "tinna-craft/skills/skill-implanter/scripts/implant_skills.py" --no-kirocrew

# Also into a specific workspace's .agents/:
python "tinna-craft/skills/skill-implanter/scripts/implant_skills.py" --workspace "C:\path\to\workspace"
```
Restart Antigravity the first time the plugin folder is created; later updates to an existing plugin are picked up without reinstalling.

### Step 4: Verify Implanted Files
```powershell
Get-ChildItem "$HOME\.gemini\config\plugins\tinna-craft\skills" | Select-Object Name
Get-Item "$HOME\.gemini\config\plugins\tinna-craft\rules\AGENTS.md"
```
