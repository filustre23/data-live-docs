from __future__ import annotations

import logging
import shutil
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path

from .base import Fetcher, FetchResult, FileMeta, hash_bytes

logger = logging.getLogger(__name__)

KEEP_SUFFIXES = {".md", ".mdx", ".rst", ".txt", ".yaml", ".yml", ".json"}


class GithubSourceFetcher(Fetcher):
    """Sparse, shallow clone of an upstream docs repo."""

    def fetch(self) -> FetchResult:
        start = time.monotonic()
        result = FetchResult()

        repo = self.source.extra["repo"]
        branch = self.source.extra.get("branch", "main")
        sparse_paths: list[str] = self.source.extra.get("sparse_paths", [""])
        rewrite_root: str = self.source.extra.get("rewrite_root", "")

        clone_dir = self.cache_dir / self.source.slug
        self._sync_repo(repo, branch, sparse_paths, clone_dir)

        copy_root = clone_dir / rewrite_root if rewrite_root else clone_dir
        if not copy_root.exists():
            raise RuntimeError(f"rewrite_root '{rewrite_root}' not present after clone")

        copied = 0
        for src in copy_root.rglob("*"):
            if not src.is_file():
                continue
            if src.suffix.lower() not in KEEP_SUFFIXES:
                continue
            rel = src.relative_to(copy_root)
            target = self.out_dir / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            data = src.read_bytes()
            target.write_bytes(data)
            result.files[str(rel)] = FileMeta(
                sha256=hash_bytes(data),
                bytes=len(data),
                fetched_at=datetime.now(timezone.utc).isoformat(),
                source_url=f"https://github.com/{repo}/blob/{branch}/{rewrite_root}{rel}".rstrip("/"),
            )
            copied += 1

        result.duration_s = time.monotonic() - start
        logger.info("[%s] copied %d files in %.1fs", self.source.slug, copied, result.duration_s)
        return result

    def _sync_repo(
        self,
        repo: str,
        branch: str,
        sparse_paths: list[str],
        clone_dir: Path,
    ) -> None:
        url = f"https://github.com/{repo}.git"
        if (clone_dir / ".git").exists():
            logger.info("[%s] updating cached clone", self.source.slug)
            self._run(["git", "fetch", "--depth=1", "origin", branch], cwd=clone_dir)
            self._run(["git", "reset", "--hard", f"origin/{branch}"], cwd=clone_dir)
            return

        if clone_dir.exists():
            shutil.rmtree(clone_dir)
        clone_dir.parent.mkdir(parents=True, exist_ok=True)
        logger.info("[%s] sparse cloning %s@%s", self.source.slug, repo, branch)
        self._run(
            [
                "git",
                "clone",
                "--depth=1",
                "--filter=blob:none",
                "--sparse",
                "--branch",
                branch,
                url,
                str(clone_dir),
            ]
        )
        self._run(["git", "sparse-checkout", "set", *sparse_paths], cwd=clone_dir)

    @staticmethod
    def _run(cmd: list[str], cwd: Path | None = None) -> None:
        logger.debug("$ %s", " ".join(cmd))
        subprocess.run(cmd, cwd=cwd, check=True, capture_output=True, text=True)
