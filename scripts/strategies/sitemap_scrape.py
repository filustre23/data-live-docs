from __future__ import annotations

import logging
import re
import time
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from urllib import robotparser
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from markdownify import markdownify as md
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from .base import Fetcher, FetchResult, FileMeta, hash_bytes, write_text_atomic

logger = logging.getLogger(__name__)

SITEMAP_NS = {"ns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
MAX_PAGE_BYTES = 500_000


class SitemapScrapeFetcher(Fetcher):
    """Fetch sitemap → GET each page → strip → html2md."""

    def fetch(self) -> FetchResult:
        start = time.monotonic()
        result = FetchResult()
        cfg = self.source.extra

        sitemap = cfg["sitemap"]
        url_filter = re.compile(cfg["url_filter"])
        strip_selectors: list[str] = cfg.get("strip_selectors", [])
        delay = float(cfg.get("request_delay_s", 0.5))
        ua = cfg.get("user_agent", "data-live-docs/1.0")

        self.session.headers["User-Agent"] = ua
        rp = self._load_robots(cfg.get("robots_url") or self._robots_url(sitemap), ua)

        urls = [u for u in self._discover_urls(sitemap) if url_filter.search(u)]
        urls = [u for u in urls if rp is None or rp.can_fetch(ua, u)]
        urls = sorted(set(urls))
        logger.info("[%s] sitemap → %d candidate urls", self.source.slug, len(urls))

        for i, url in enumerate(urls, 1):
            try:
                html = self._fetch_html(url)
                markdown = self._html_to_md(html, strip_selectors)
                if not markdown.strip():
                    raise ValueError("empty after strip")
                rel = self._url_to_rel_path(url, self.source.official_root)
                target = self.out_dir / rel
                size = write_text_atomic(target, markdown)
                result.files[rel] = FileMeta(
                    sha256=hash_bytes(markdown.encode("utf-8")),
                    bytes=size,
                    fetched_at=datetime.now(timezone.utc).isoformat(),
                    source_url=url,
                )
                if i % 10 == 0:
                    logger.info("[%s] %d/%d", self.source.slug, i, len(urls))
                time.sleep(delay)
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
        r = self.session.get(sitemap_url, timeout=60)
        r.raise_for_status()
        try:
            parser = ET.XMLParser(forbid_dtd=True, forbid_entities=True, forbid_external=True)  # type: ignore[call-arg]
            root = ET.fromstring(r.content, parser=parser)
        except TypeError:
            root = ET.fromstring(r.content)

        urls: list[str] = []
        # Sitemap index? Recurse.
        for sm in root.findall(".//ns:sitemap/ns:loc", SITEMAP_NS):
            if sm.text:
                urls.extend(self._discover_urls(sm.text.strip()))
        for loc in root.findall(".//ns:url/ns:loc", SITEMAP_NS):
            if loc.text:
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
    def _fetch_html(self, url: str) -> str:
        r = self.session.get(url, timeout=30)
        if r.status_code == 429:
            time.sleep(int(r.headers.get("Retry-After", 30)))
            r = self.session.get(url, timeout=30)
        r.raise_for_status()
        if len(r.content) > MAX_PAGE_BYTES:
            logger.warning("page over %dB cap, truncating: %s", MAX_PAGE_BYTES, url)
            return r.content[:MAX_PAGE_BYTES].decode("utf-8", errors="ignore")
        return r.text

    @staticmethod
    def _html_to_md(html: str, strip_selectors: list[str]) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for sel in strip_selectors:
            for el in soup.select(sel):
                el.decompose()
        # Pick the most likely main content container if present.
        main = soup.find("main") or soup.find("article") or soup.body or soup
        return md(str(main), heading_style="ATX", strip=["script", "style"]).strip()

    @staticmethod
    def _url_to_rel_path(url: str, official_root: str) -> str:
        path = urlparse(url).path
        root_path = urlparse(official_root).path
        if path.startswith(root_path):
            path = path[len(root_path):]
        path = path.strip("/")
        if not path:
            path = "index"
        return path + ".md"

    @staticmethod
    def _robots_url(sitemap_url: str) -> str:
        p = urlparse(sitemap_url)
        return f"{p.scheme}://{p.netloc}/robots.txt"

    def _load_robots(self, robots_url: str, user_agent: str) -> robotparser.RobotFileParser | None:
        try:
            rp = robotparser.RobotFileParser()
            rp.set_url(robots_url)
            rp.read()
            return rp
        except Exception as e:
            logger.warning("could not load robots.txt %s: %s", robots_url, e)
            return None
