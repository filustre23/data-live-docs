#!/usr/bin/env python3
"""Dispatcher: read sources.yml, run the right Fetcher per source, write _manifest.json."""
from __future__ import annotations

import argparse
import json
import logging
import shutil
import sys
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path

import requests
import yaml

sys.path.insert(0, str(Path(__file__).parent))
from strategies import STRATEGIES, SourceConfig  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SOURCES_FILE = REPO_ROOT / "sources.yml"
DOCS_ROOT = REPO_ROOT / "docs"
CACHE_ROOT = REPO_ROOT / "scripts" / ".cache"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def load_sources() -> list[SourceConfig]:
    raw = yaml.safe_load(SOURCES_FILE.read_text())
    return [SourceConfig.from_dict(s) for s in raw.get("sources", [])]


def fetch_source(source: SourceConfig, dry_run: bool = False) -> int:
    StrategyCls = STRATEGIES.get(source.strategy)
    if StrategyCls is None:
        logger.error("[%s] unknown strategy: %s", source.slug, source.strategy)
        return 2

    final_dir = DOCS_ROOT / source.slug
    tmp_dir = DOCS_ROOT / f".{source.slug}.tmp"

    if dry_run:
        logger.info("[%s] DRY RUN — strategy=%s out=%s", source.slug, source.strategy, final_dir)
        return 0

    if tmp_dir.exists():
        shutil.rmtree(tmp_dir)
    tmp_dir.mkdir(parents=True)
    CACHE_ROOT.mkdir(parents=True, exist_ok=True)

    session = requests.Session()
    session.headers.update({"Cache-Control": "no-cache"})

    fetcher = StrategyCls(source=source, out_dir=tmp_dir, session=session, cache_dir=CACHE_ROOT)

    try:
        result = fetcher.fetch()
    except Exception as e:
        logger.exception("[%s] fetcher crashed: %s", source.slug, e)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return 1

    if not result.files:
        logger.error("[%s] no files fetched; aborting swap", source.slug)
        shutil.rmtree(tmp_dir, ignore_errors=True)
        return 1

    manifest = {
        "slug": source.slug,
        "strategy": source.strategy,
        "official_root": source.official_root,
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "duration_s": round(result.duration_s, 2),
        "file_count": len(result.files),
        "failed_count": len(result.pages_failed),
        "failed_pages": result.pages_failed[:50],
        "files": {k: asdict(v) for k, v in result.files.items()},
    }
    (tmp_dir / "_manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True))

    if final_dir.exists():
        shutil.rmtree(final_dir)
    tmp_dir.rename(final_dir)
    logger.info("[%s] swapped → %s", source.slug, final_dir)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", help="single slug; omit with --all")
    ap.add_argument("--all", action="store_true", help="fetch every source in sources.yml")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    sources = load_sources()
    if args.source:
        sources = [s for s in sources if s.slug == args.source]
        if not sources:
            logger.error("no source named %r in sources.yml", args.source)
            return 2
    elif not args.all:
        ap.error("must pass --source <slug> or --all")

    DOCS_ROOT.mkdir(exist_ok=True)
    rc = 0
    for s in sources:
        code = fetch_source(s, dry_run=args.dry_run)
        if code != 0:
            rc = code
    return rc


if __name__ == "__main__":
    sys.exit(main())
