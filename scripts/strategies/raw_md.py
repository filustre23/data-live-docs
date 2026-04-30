from __future__ import annotations

import logging
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib.parse import urlparse

from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .base import Fetcher, FetchResult, FileMeta, hash_bytes, write_text_atomic

logger = logging.getLogger(__name__)

SITEMAP_NS = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}


class RawMdFetcher(Fetcher):
    """Fetch a sitemap, filter URLs, and download `<url>.md` siblings."""

    def fetch(self) -> FetchResult:
        start = time.monotonic()
        result = FetchResult()

        sitemap = self.source.extra["sitemap"]
        md_suffix = self.source.extra.get("md_suffix", ".md")
        url_patterns: list[str] = self.source.extra.get("url_patterns", [])
        skip_patterns: list[str] = self.source.extra.get("skip_patterns", [])

        urls = self._discover_urls(sitemap)
        if url_patterns:
            urls = [u for u in urls if any(p in u for p in url_patterns)]
        if skip_patterns:
            urls = [u for u in urls if not any(p in u for p in skip_patterns)]
        urls = sorted(set(urls))
        logger.info("[%s] sitemap → %d candidate urls", self.source.slug, len(urls))

        for i, url in enumerate(urls, 1):
            try:
                content = self._fetch_md(url + md_suffix)
                self._validate_md(content)
                rel = self._url_to_rel_path(url)
                target = self.out_dir / rel
                size = write_text_atomic(target, content)
                result.files[rel] = FileMeta(
                    sha256=hash_bytes(content.encode("utf-8")),
                    bytes=size,
                    fetched_at=datetime.now(timezone.utc).isoformat(),
                    source_url=url,
                )
                if i % 10 == 0:
                    logger.info("[%s] %d/%d", self.source.slug, i, len(urls))
                time.sleep(0.3)
            except Exception as e:
                logger.warning("[%s] failed %s: %s", self.source.slug, url, e)
                result.pages_failed.append(url)

        result.duration_s = time.monotonic() - start
        logger.info(
            "[%s] done: %d files, %d failed, %.1fs",
            self.source.slug,
            len(result.files),
            len(result.pages_failed),
            result.duration_s,
        )
        return result

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=30),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _discover_urls(self, sitemap_url: str) -> list[str]:
        r = self.session.get(sitemap_url, timeout=30)
        r.raise_for_status()
        try:
            parser = ET.XMLParser(forbid_dtd=True, forbid_entities=True, forbid_external=True)  # type: ignore[call-arg]
            root = ET.fromstring(r.content, parser=parser)
        except TypeError:
            root = ET.fromstring(r.content)
        urls: list[str] = []
        for url_elem in root.findall(".//ns:url", SITEMAP_NS):
            loc = url_elem.find("ns:loc", SITEMAP_NS)
            if loc is not None and loc.text:
                urls.append(loc.text.strip())
        if not urls:
            for loc in root.findall(".//loc"):
                if loc.text:
                    urls.append(loc.text.strip())
        return urls

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=2, max=30),
        retry=retry_if_exception_type(Exception),
        reraise=True,
    )
    def _fetch_md(self, url: str) -> str:
        r = self.session.get(url, timeout=30, allow_redirects=True)
        if r.status_code == 429:
            wait = int(r.headers.get("Retry-After", 30))
            time.sleep(wait)
            r = self.session.get(url, timeout=30)
        r.raise_for_status()
        return r.text

    @staticmethod
    def _validate_md(content: str) -> None:
        if not content or content.lstrip().lower().startswith("<!doctype") or "<html" in content[:200].lower():
            raise ValueError("got HTML instead of markdown")
        if len(content.strip()) < 50:
            raise ValueError(f"content too short ({len(content)}b)")

    @staticmethod
    def _url_to_rel_path(url: str) -> str:
        path = urlparse(url).path.strip("/")
        for prefix in ("docs/en/", "en/docs/"):
            if path.startswith(prefix):
                path = path[len(prefix):]
                break
        if not path:
            path = "index"
        return path + ".md"
