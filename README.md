# data-live-docs

Auto-updated documentation mirror for the modern data stack. Read fresh, locally cached docs from inside Claude Code via the `/livedocs` slash command.

Pattern is borrowed from [`ericbuess/claude-code-docs`](https://github.com/ericbuess/claude-code-docs) but extended to many sources via three pluggable fetcher strategies.

## Install

```bash
curl -fsSL https://raw.githubusercontent.com/filustre23/data-live-docs/main/install.sh | bash
```

The installer:

1. Clones this repo to `~/.data-live-docs`
2. Registers the `/livedocs` slash command at `~/.claude/commands/livedocs.md`
3. Adds a `PreToolUse` hook into `~/.claude/settings.json` (currently a no-op stub)

After install, restart Claude Code and try:

```
/livedocs                            # list sources
/livedocs dbt-core                   # list topics under dbt-core
/livedocs dbt-core overview          # read a topic
/livedocs search materialized        # full-text search across all sources
/livedocs -t                         # freshness summary
/livedocs whats-new                  # recent commits
```

## Sources (Phase A)

| Slug | Strategy | Upstream |
|------|----------|----------|
| `claude-code` | raw-md | https://code.claude.com/docs/ |
| `dbt-core` | github-source | https://github.com/dbt-labs/docs.getdbt.com |
| `bigquery` | sitemap-scrape | https://cloud.google.com/bigquery/docs/ |

More sources land in subsequent phases — see `sources.yml`.

## How it stays fresh

A GitHub Actions workflow runs every 6 hours (`.github/workflows/update-docs.yml`), fetches each source via its declared strategy, and commits diffs to `main`. The helper script auto-pulls when you read a doc that's behind upstream.

## Uninstall

```bash
~/.data-live-docs/uninstall.sh
```

## License

MIT — see `LICENSE`. Not affiliated with Anthropic, dbt Labs, Google, or any other documented project. Each upstream's content remains under its own license.
