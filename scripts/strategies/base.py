from __future__ import annotations

import hashlib
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import requests

logger = logging.getLogger(__name__)


@dataclass
class SourceConfig:
    slug: str
    strategy: str
    official_root: str
    schedule: str = "6h"
    size_budget_mb: int = 50
    extra: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "SourceConfig":
        known = {"slug", "strategy", "official_root", "schedule", "size_budget_mb"}
        return cls(
            slug=raw["slug"],
            strategy=raw["strategy"],
            official_root=raw["official_root"],
            schedule=raw.get("schedule", "6h"),
            size_budget_mb=int(raw.get("size_budget_mb", 50)),
            extra={k: v for k, v in raw.items() if k not in known},
        )


@dataclass
class FileMeta:
    sha256: str
    bytes: int
    fetched_at: str
    source_url: str | None = None


@dataclass
class FetchResult:
    files: dict[str, FileMeta] = field(default_factory=dict)
    pages_failed: list[str] = field(default_factory=list)
    duration_s: float = 0.0


class Fetcher(ABC):
    def __init__(
        self,
        source: SourceConfig,
        out_dir: Path,
        session: requests.Session,
        cache_dir: Path,
    ) -> None:
        self.source = source
        self.out_dir = out_dir
        self.session = session
        self.cache_dir = cache_dir

    @abstractmethod
    def fetch(self) -> FetchResult: ...


def hash_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_text_atomic(path: Path, content: str) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = content.encode("utf-8")
    path.write_bytes(payload)
    return len(payload)
