"""
Reindex Documents & PDFs to Sequential '0N_{ชื่อเอกสาร}' Format.

Scans a folder, sorts documents by modification time (or natural name order),
strips chaotic suffixes (_final, _v2, _edit, ฉบับร่าง, แก้ครั้งที่...),
and standardizes them into 01_..., 02_..., 0N_... prefixes.
"""

from __future__ import annotations

import argparse
import logging
import re
import sys
from pathlib import Path

if sys.platform == "win32":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if hasattr(sys.stderr, "reconfigure"):
        sys.stderr.reconfigure(encoding="utf-8")

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger("reindex_docs")

DOC_EXTENSIONS = {".docx", ".doc", ".pdf", ".pptx", ".xlsx", ".md"}

LEADING_PREFIX_RE = re.compile(r"^(?:\d{1,4}[\s_.\-]+)+")
CHAOTIC_SUFFIX_RE = re.compile(
    r"(?:[\s_\-]*(?:really[\s_\-]*)?(?:final\d*|v\d+(?:\.\d+)?|rev\d*|edit\d*|draft\d*|new\d*|copy\d*|backup\d*|"
    r"ฉบับร่าง|ฉบับแก้ไข|แก้ไขครั้งที่\s*\d+|แก้ครั้งที่\s*\d+))+$",
    re.IGNORECASE,
)


def clean_base_name(filename: str) -> str:
    """Strip existing numeric prefixes and messy tags like _final, _v2, _edit, etc."""
    stem = Path(filename).stem.strip()
    stem = LEADING_PREFIX_RE.sub("", stem).strip()
    cleaned = CHAOTIC_SUFFIX_RE.sub("", stem).strip(" _-.")
    return cleaned if cleaned else stem


def reindex_directory(
    target_dir: Path,
    dry_run: bool = True,
    sort_by: str = "mtime",
    custom_name: str | None = None,
) -> None:
    if not target_dir.exists() or not target_dir.is_dir():
        logger.error(f"Target directory does not exist: {target_dir}")
        sys.exit(1)

    files = [
        f for f in target_dir.iterdir()
        if f.is_file() and f.suffix.lower() in DOC_EXTENSIONS
    ]

    if not files:
        logger.info(f"No document files ({', '.join(sorted(DOC_EXTENSIONS))}) found in {target_dir}")
        return

    if sort_by == "mtime":
        files.sort(key=lambda x: x.stat().st_mtime)
    elif sort_by == "ctime":
        files.sort(key=lambda x: x.stat().st_ctime)
    else:
        files.sort(key=lambda x: x.name)

    total = len(files)
    pad = 3 if total >= 100 else 2

    logger.info(f"Found {total} documents in {target_dir}. Planning reindex ({'DRY RUN' if dry_run else 'APPLYING'}):")
    logger.info("-" * 60)

    for idx, f in enumerate(files, start=1):
        prefix = f"{idx:0{pad}d}"
        clean_name = custom_name if custom_name else clean_base_name(f.name)
        new_name = f"{prefix}_{clean_name}{f.suffix.lower()}"
        new_path = target_dir / new_name

        if f.name == new_name:
            logger.info(f"  [OK] {f.name} (already properly indexed)")
            continue

        logger.info(f"  [RENAME] {f.name} -> {new_name}")
        if not dry_run:
            f.rename(new_path)

    logger.info("-" * 60)
    if dry_run:
        logger.info("Dry run complete. Use --apply to execute renaming.")
    else:
        logger.info("Successfully reindexed all documents.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Reindex documents into sequential 0N_{ชื่อเอกสาร} format."
    )
    parser.add_argument(
        "--dir", "-d", type=Path, default=Path("."), help="Directory containing documents"
    )
    parser.add_argument(
        "--apply", action="store_true", help="Execute rename operations (default is dry-run)"
    )
    parser.add_argument(
        "--sort", choices=["mtime", "ctime", "name"], default="mtime",
        help="Sorting criteria: mtime (modified time, default), ctime (created), name (alphabetical)"
    )
    parser.add_argument(
        "--name", "-n", type=str, default=None,
        help="Optional uniform document name (e.g., 'รายงานวิจัย' -> 01_รายงานวิจัย.docx)"
    )

    args = parser.parse_args()
    reindex_directory(
        target_dir=args.dir,
        dry_run=not args.apply,
        sort_by=args.sort,
        custom_name=args.name,
    )


if __name__ == "__main__":
    main()
