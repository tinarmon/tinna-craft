"""Deterministic outer-loop slop, boundary, and secret scanner for quality-gate."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKIP_DIRS = {
    ".git",
    ".venv",
    "venv",
    "node_modules",
    "__pycache__",
    "dist",
    ".next",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}
TARGET_EXTS = {".py", ".ts", ".tsx", ".js", ".jsx"}

SILENT_EXCEPT_RE = re.compile(
    r"(^\s*except\s*:\s*$|^\s*except\s+Exception(?:\s+as\s+\w+)?\s*:\s*pass\b|catch\s*\([^)]*\)\s*\{\s*\})"
)
DEBUG_LEFTOVER_RE = re.compile(r"\b(?:breakpoint\s*\(|pdb\.set_trace\s*\(|console\.log\s*\()")
SECRET_RE = re.compile(
    r"""(?:(?:api_key|secret|token|password)\s*=\s*["'][A-Za-z0-9_\-]{16,}["']|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,})""",
    re.IGNORECASE,
)
FEATURE_PATH_RE = re.compile(r"(?:^|[/\\])features[/\\]([A-Za-z0-9_\-]+)[/\\]")
CROSS_FEATURE_IMPORT_RE = re.compile(
    r"""(?:from|import)\s+["']?(?:@/|[\w.]+\.)?features[./]([A-Za-z0-9_\-]+)[./]([A-Za-z0-9_\-]+)"""
)


@dataclass(frozen=True)
class Finding:
    path: Path
    line: int
    rule: str
    snippet: str


def iter_target_files(root: Path, diff_only: bool = False) -> list[Path]:
    if diff_only:
        res = subprocess.run(
            ["git", "-C", str(root), "diff", "--name-only", "HEAD"],
            capture_output=True,
            text=True,
            check=False,
        )
        if res.returncode == 0:
            files = []
            for rel in res.stdout.splitlines():
                p = (root / rel.strip()).resolve()
                if p.is_file() and p.suffix in TARGET_EXTS:
                    files.append(p)
            return sorted(files)

    files: list[Path] = []
    for p in root.rglob("*"):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.is_file() and p.suffix in TARGET_EXTS:
            files.append(p)
    return sorted(files)


def scan_file(path: Path, root: Path | None = None) -> list[Finding]:
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return []

    rel_str = str(path.relative_to(root)) if root and path.is_relative_to(root) else str(path)
    own_feat_match = FEATURE_PATH_RE.search(rel_str)
    own_feature = own_feat_match.group(1) if own_feat_match else None

    findings: list[Finding] = []
    for idx, line in enumerate(lines, start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith(("#", "//")):
            continue

        if SILENT_EXCEPT_RE.search(line):
            findings.append(Finding(path, idx, "SILENT_EXCEPT", stripped))
        if DEBUG_LEFTOVER_RE.search(line):
            findings.append(Finding(path, idx, "DEBUG_LEFTOVER", stripped))
        if SECRET_RE.search(line):
            findings.append(Finding(path, idx, "SECRET_PATTERN", "<redacted>"))

        imp_match = CROSS_FEATURE_IMPORT_RE.search(line)
        if imp_match:
            target_feat, target_sub = imp_match.group(1), imp_match.group(2)
            # Only public entrypoint (__init__ / index) may be imported across features
            if target_feat != own_feature and target_sub not in {"__init__", "index"}:
                findings.append(Finding(path, idx, "CROSS_FEATURE_IMPORT", stripped))

    return findings


def run_self_test() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        feat_a = root / "src" / "features" / "auth"
        feat_b = root / "src" / "features" / "billing"
        feat_a.mkdir(parents=True)
        feat_b.mkdir(parents=True)

        bad = feat_a / "service.py"
        bad.write_text(
            "from src.features." + "billing.internal import calc\n"
            "def f():\n"
            "    try:\n"
            "        break" + "point()\n"
            "    except Exception: pass\n",
            encoding="utf-8",
        )
        good = feat_b / "service.py"
        good.write_text(
            "from src.features.auth import login\n"
            "def ok() -> int:\n"
            "    return 1\n",
            encoding="utf-8",
        )

        bad_rules = {f.rule for f in scan_file(bad, root)}
        assert bad_rules == {"CROSS_FEATURE_IMPORT", "DEBUG_LEFTOVER", "SILENT_EXCEPT"}, bad_rules
        assert scan_file(good, root) == []
    print("slop_audit self-test: PASS")


def main() -> int:
    parser = argparse.ArgumentParser(description="Deterministic slop & boundary audit")
    parser.add_argument("--root", type=Path, default=Path("."), help="Project root to scan")
    parser.add_argument("--diff", action="store_true", help="Scan only git-modified files vs HEAD")
    parser.add_argument("--self-test", action="store_true", help="Run built-in self-tests")
    args = parser.parse_args()

    if args.self_test:
        run_self_test()
        return 0

    root = args.root.resolve()
    files = iter_target_files(root, diff_only=args.diff)
    all_findings: list[Finding] = []
    for f in files:
        all_findings.extend(scan_file(f, root))

    for item in all_findings:
        rel = item.path.relative_to(root) if item.path.is_relative_to(root) else item.path
        print(f"{rel}:{item.line}: [{item.rule}] {item.snippet}")

    print(f"Scanned {len(files)} file(s): {len(all_findings)} finding(s).")
    return 1 if all_findings else 0


if __name__ == "__main__":
    sys.exit(main())
