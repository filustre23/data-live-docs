#!/usr/bin/env python3
"""Per-source size budget guardrail. Warn at 80%, fail at 150%."""
from __future__ import annotations

import argparse
import logging
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_FILE = REPO_ROOT / "sources.yml"
DOCS_ROOT = REPO_ROOT / "docs"

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)


def dir_size_bytes(path: Path) -> int:
    if not path.exists():
        return 0
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", help="check a single source")
    args = ap.parse_args()

    raw = yaml.safe_load(SOURCES_FILE.read_text())
    sources = raw.get("sources", [])
    if args.source:
        sources = [s for s in sources if s["slug"] == args.source]
        if not sources:
            logger.error("no source %r", args.source)
            return 2

    rc = 0
    for s in sources:
        slug = s["slug"]
        budget_mb = int(s.get("size_budget_mb", 50))
        actual = dir_size_bytes(DOCS_ROOT / slug)
        actual_mb = actual / 1_048_576
        pct = (actual_mb / budget_mb) * 100 if budget_mb else 0
        line = f"[{slug}] {actual_mb:.1f}MB / {budget_mb}MB ({pct:.0f}%)"
        if pct > 150:
            logger.error("%s — OVER 150%% budget", line)
            rc = 1
        elif pct > 80:
            logger.warning("%s — over 80%% budget", line)
        else:
            logger.info("%s — ok", line)
    return rc


if __name__ == "__main__":
    sys.exit(main())
