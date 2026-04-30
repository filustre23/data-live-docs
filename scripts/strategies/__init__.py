from .base import Fetcher, FetchResult, FileMeta, SourceConfig
from .github_source import GithubSourceFetcher
from .raw_md import RawMdFetcher
from .sitemap_scrape import SitemapScrapeFetcher

STRATEGIES: dict[str, type[Fetcher]] = {
    "raw-md": RawMdFetcher,
    "github-source": GithubSourceFetcher,
    "sitemap-scrape": SitemapScrapeFetcher,
}

__all__ = [
    "Fetcher",
    "FetchResult",
    "FileMeta",
    "SourceConfig",
    "STRATEGIES",
]
