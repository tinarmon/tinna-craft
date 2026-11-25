"""
Store, Implant, Verify, and Sync Antigravity Skills & Rules Globally or per Workspace.

Implanting copies skills (<plugin>/skills/*) and rules (<plugin>/rules/AGENTS.md)
into:
  1. Global plugin: ~/.gemini/config/plugins/tinna-craft/ (skills/, rules/, plugin.json)
  2. Optional target workspace: <workspace>/.agents/skills/ and <workspace>/.agents/rules/
Also validates YAML frontmatter and relative markdown links in every SKILL.md.
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import sys
import tempfile
from pathlib import Path

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("implant_skills")

FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---", re.DOTALL)
MD_LINK_RE = re.compile(r"\[[^\]]+\]\((\.[^)]+)\)")
PLUGIN_NAME = "tinna-craft"


def find_source_root(explicit_source: Path | None = None) -> Path:
    if explicit_source and explicit_source.exists():
        return explicit_source.resolve()
    # Default: walk up from this script's location (<plugin>/skills/skill-implanter/scripts/implant_skills.py)
    script_path = Path(__file__).resolve()
    for parent in script_path.parents:
        if (parent / "plugin.json").exists():
            return parent
        if (parent / ".agents" / "skills").exists():
            return parent
        if parent.name == ".agents" and (parent / "skills").exists():
            return parent.parent
    return Path.cwd()


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        errors.append(f"{skill_dir.name}: Missing SKILL.md")
        return errors

    text = skill_md.read_text(encoding="utf-8")
    m = FRONTMATTER_RE.match(text)
    if not m:
        errors.append(f"{skill_dir.name}: Missing YAML frontmatter (--- ... ---)")
    else:
        fm = m.group(1)
        if "name:" not in fm:
            errors.append(f"{skill_dir.name}: Frontmatter missing 'name:'")
        if "description:" not in fm:
            errors.append(f"{skill_dir.name}: Frontmatter missing 'description:'")

    # Strip fenced code blocks before checking relative markdown links
    text_no_code = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for rel_link in MD_LINK_RE.findall(text_no_code):
        clean_rel = rel_link.split("#", 1)[0]
        target = (skill_dir / clean_rel).resolve()
        if not target.exists():
            errors.append(f"{skill_dir.name}: Broken relative link '{rel_link}' -> {target}")

    return errors


def _norm_path(path_str: str) -> str:
    return os.path.normcase(Path(path_str).as_posix())


def sync_kirocrew(
    plugin_dir: Path,
    src_rules_dir: Path,
    dry_run: bool = False,
) -> None:
    """Sync global steering and extra skill paths into KiroCrew when installed."""
    kiro_dir = Path.home() / ".kiro"
    crew_config_path = kiro_dir / "crew" / "config.json"
    if not crew_config_path.exists():
        logger.debug("KiroCrew config not found; skipping KiroCrew sync.")
        return

    rules_agents = src_rules_dir / "AGENTS.md"
    if rules_agents.exists():
        steering_file = kiro_dir / "steering" / "tinna-craft.md"
        desired_steering = "---\ninclusion: always\n---\n\n" + rules_agents.read_text(encoding="utf-8")
        current_steering = steering_file.read_text(encoding="utf-8") if steering_file.exists() else None
        if current_steering != desired_steering:
            if not dry_run:
                steering_file.parent.mkdir(parents=True, exist_ok=True)
                steering_file.write_text(desired_steering, encoding="utf-8")
            logger.info(f"  [KIROCREW STEERING] AGENTS.md -> {steering_file}")
        else:
            logger.info(f"  [KIROCREW STEERING] Up to date: {steering_file}")

    plugins_root = plugin_dir.parent
    candidate_dirs = [
        plugin_dir / "skills",
        plugins_root / "research-craft" / "skills",
        plugins_root / "ponytail" / "skills",
        plugins_root / "anthropic-skills" / "skills",
    ]
    desired_paths = [d.resolve().as_posix() for d in candidate_dirs if d.is_dir()]
    if not desired_paths:
        return

    try:
        cfg = json.loads(crew_config_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning(f"Could not read KiroCrew config ({crew_config_path}): {exc}")
        return

    if not isinstance(cfg, dict):
        logger.warning(f"Unexpected KiroCrew config format in {crew_config_path}; skipping extra_paths sync.")
        return

    skills_cfg = cfg.setdefault("skills", {})
    if not isinstance(skills_cfg, dict):
        logger.warning(f"Unexpected 'skills' section in {crew_config_path}; skipping extra_paths sync.")
        return

    existing_raw = skills_cfg.get("extra_paths")
    existing: list[str] = list(existing_raw) if isinstance(existing_raw, list) else []
    existing_norm = {_norm_path(p) for p in existing if isinstance(p, str)}
    missing = [p for p in desired_paths if _norm_path(p) not in existing_norm]

    if missing:
        skills_cfg["extra_paths"] = existing + missing
        if not dry_run:
            fd, tmp_name = tempfile.mkstemp(
                prefix=".config-", suffix=".tmp", dir=str(crew_config_path.parent)
            )
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as fh:
                    fh.write(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n")
                os.replace(tmp_name, crew_config_path)
            except BaseException:
                Path(tmp_name).unlink(missing_ok=True)
                raise
        logger.info(f"  [KIROCREW CONFIG] Added extra_paths: {', '.join(missing)}")
    else:
        logger.info(f"  [KIROCREW CONFIG] extra_paths already synced ({len(desired_paths)} packs)")


def implant(
    source_root: Path,
    global_dir: Path,
    target_workspace: Path | None = None,
    dry_run: bool = False,
    sync_kiro: bool = True,
) -> int:
    agents_dir = source_root / ".agents" if (source_root / ".agents").exists() else source_root
    src_skills_dir = agents_dir / "skills"
    src_rules_dir = agents_dir / "rules"
    src_agents_md = source_root / "AGENTS.md"

    if not src_skills_dir.exists():
        logger.error(f"Source skills directory not found: {src_skills_dir}")
        return 1

    skill_dirs = sorted([d for d in src_skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()])
    rule_files = sorted([f for f in src_rules_dir.iterdir() if f.is_file() and f.suffix == ".md"]) if src_rules_dir.exists() else []

    logger.info(f"Source Pack : {source_root}")
    logger.info(f"Skills found: {len(skill_dirs)} ({', '.join(d.name for d in skill_dirs)})")
    logger.info(f"Rules found : {len(rule_files)} ({', '.join(f.name for f in rule_files)})")

    all_errors: list[str] = []
    for sd in skill_dirs:
        all_errors.extend(validate_skill(sd))

    if all_errors:
        for err in all_errors:
            logger.error(f"[VALIDATION ERROR] {err}")
        return 1
    logger.info("Validation  : 100% passed (frontmatter + relative links verified)")

    plugin_dir = global_dir / "plugins" / PLUGIN_NAME
    destinations: list[tuple[str, Path, Path]] = []
    if plugin_dir.resolve() == source_root.resolve():
        logger.info(f"Source IS the installed plugin ({plugin_dir}); skipping global copy.")
    else:
        destinations.append((f"Global Plugin ({plugin_dir})", plugin_dir / "skills", plugin_dir / "rules"))
        if not dry_run and (source_root / "plugin.json").exists():
            plugin_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_root / "plugin.json", plugin_dir / "plugin.json")
    if target_workspace:
        ws_agents = target_workspace.resolve() / ".agents"
        destinations.append((f"Workspace ({target_workspace.resolve()})", ws_agents / "skills", ws_agents / "rules"))

    for label, dst_skills, dst_rules in destinations:
        logger.info("-" * 60)
        logger.info(f"{'[DRY RUN] Would implant' if dry_run else 'Implanting'} into {label}:")
        if not dry_run:
            dst_skills.mkdir(parents=True, exist_ok=True)
            dst_rules.mkdir(parents=True, exist_ok=True)

        for sd in skill_dirs:
            target_sd = dst_skills / sd.name
            if not dry_run:
                if target_sd.exists():
                    shutil.rmtree(target_sd)
                shutil.copytree(sd, target_sd)
            logger.info(f"  [SKILL] {sd.name} -> {target_sd}")

        for rf in rule_files:
            target_rf = dst_rules / rf.name
            if not dry_run:
                shutil.copy2(rf, target_rf)
            logger.info(f"  [RULE]  {rf.name} -> {target_rf}")

    # Remove legacy singular ~/.gemini/config/skill directory if empty
    legacy_singular = global_dir / "skill"
    if not dry_run and legacy_singular.exists() and legacy_singular.is_dir():
        if not any(legacy_singular.iterdir()):
            legacy_singular.rmdir()
            logger.info(f"  [CLEAN] Removed empty legacy folder: {legacy_singular}")

    # Copy AGENTS.md to global_dir (falling back to rules/AGENTS.md) and target_workspace if present
    effective_agents_md = src_agents_md if src_agents_md.exists() else (src_rules_dir / "AGENTS.md")
    if effective_agents_md.exists():
        global_agents_md = global_dir / "AGENTS.md"
        if not dry_run:
            shutil.copy2(effective_agents_md, global_agents_md)
        logger.info(f"  [DIRECTIVE] AGENTS.md -> {global_agents_md}")

        if target_workspace and src_agents_md.exists():
            ws_agents_md = target_workspace.resolve() / "AGENTS.md"
            if not dry_run and ws_agents_md.resolve() != src_agents_md.resolve():
                shutil.copy2(src_agents_md, ws_agents_md)
                logger.info(f"  [DIRECTIVE] AGENTS.md -> {ws_agents_md}")

    # Write ~/.gemini/config/skills.json pointing to ~/.gemini/config/skills
    skills_json_path = global_dir / "skills.json"
    skills_manifest = {
        "entries": [
            {"path": "~/.gemini/config/skills"}
        ]
    }
    if not dry_run:
        skills_json_path.write_text(json.dumps(skills_manifest, indent=2) + "\n", encoding="utf-8")
    logger.info(f"  [CONFIG] skills.json -> {skills_json_path}")

    if sync_kiro:
        sync_kirocrew(plugin_dir, src_rules_dir, dry_run=dry_run)

    logger.info("-" * 60)
    logger.info("Implant complete." if not dry_run else "Dry run complete. Use without --dry-run to execute.")
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate, store, and implant AI skills & rules globally (~/.gemini/config) or into a workspace."
    )
    parser.add_argument(
        "--source", "-s", type=Path, default=None,
        help="Source directory containing .agents/skills (defaults to pack root)"
    )
    parser.add_argument(
        "--global-dir", "-g", type=Path, default=Path.home() / ".gemini" / "config",
        help="Global Antigravity config directory (default: ~/.gemini/config)"
    )
    parser.add_argument(
        "--workspace", "-w", type=Path, default=None,
        help="Optional workspace root to also implant .agents/skills and .agents/rules into"
    )
    parser.add_argument(
        "--verify-only", action="store_true",
        help="Only validate SKILL.md frontmatter and links without copying"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Preview what would be implanted without writing files"
    )
    parser.add_argument(
        "--no-kirocrew", action="store_false", dest="kirocrew", default=True,
        help="Skip syncing steering and extra_paths into KiroCrew (~/.kiro)"
    )
    args = parser.parse_args()

    src = find_source_root(args.source)
    if args.verify_only:
        agents_dir = src / ".agents" if (src / ".agents").exists() else src
        skill_dirs = sorted([d for d in (agents_dir / "skills").iterdir() if d.is_dir() and (d / "SKILL.md").exists()])
        errs: list[str] = []
        for sd in skill_dirs:
            errs.extend(validate_skill(sd))
        if errs:
            for e in errs:
                logger.error(e)
            sys.exit(1)
        logger.info(f"All {len(skill_dirs)} skills in {src} passed validation.")
        sys.exit(0)

    sys.exit(implant(src, args.global_dir, args.workspace, dry_run=args.dry_run, sync_kiro=args.kirocrew))


if __name__ == "__main__":
    main()
