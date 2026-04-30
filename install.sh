#!/bin/bash
set -euo pipefail

# data-live-docs installer
# Installs/updates ~/.data-live-docs and registers /livedocs.

echo "data-live-docs installer"
echo "========================"

INSTALL_DIR="$HOME/.data-live-docs"
INSTALL_BRANCH="main"
REPO_URL="https://github.com/filustre23/data-live-docs.git"
COMMAND_FILE="$HOME/.claude/commands/livedocs.md"
SETTINGS_FILE="$HOME/.claude/settings.json"
HOOK_COMMAND='~/.data-live-docs/data-docs-helper.sh hook-check'

if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "✓ Detected macOS"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    echo "✓ Detected Linux"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

echo "Checking dependencies…"
for cmd in git jq curl python3; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "❌ Missing required dependency: $cmd"
        exit 1
    fi
done
if ! command -v rg >/dev/null 2>&1; then
    echo "ℹ️  ripgrep (rg) not found — search will fall back to grep. Install: brew install ripgrep"
fi
echo "✓ Dependencies ok"

# Clone or update
if [[ -d "$INSTALL_DIR/.git" ]]; then
    echo ""
    echo "Updating existing installation at $INSTALL_DIR…"
    cd "$INSTALL_DIR"
    git fetch --quiet origin "$INSTALL_BRANCH"
    git checkout -B "$INSTALL_BRANCH" "origin/$INSTALL_BRANCH" >/dev/null 2>&1
    git reset --hard "origin/$INSTALL_BRANCH" >/dev/null 2>&1
    git clean -fd >/dev/null 2>&1 || true
    echo "✓ Updated to latest $INSTALL_BRANCH"
else
    echo ""
    echo "Cloning $REPO_URL → $INSTALL_DIR…"
    if [[ -d "$INSTALL_DIR" ]]; then
        rm -rf "$INSTALL_DIR"
    fi
    git clone -b "$INSTALL_BRANCH" "$REPO_URL" "$INSTALL_DIR"
    echo "✓ Cloned"
fi

chmod +x "$INSTALL_DIR/data-docs-helper.sh" 2>/dev/null || true
chmod +x "$INSTALL_DIR/scripts/"*.py 2>/dev/null || true

echo ""
echo "Registering /livedocs slash command…"
mkdir -p "$(dirname "$COMMAND_FILE")"
cat > "$COMMAND_FILE" << 'EOF'
Execute the data-live-docs helper script at ~/.data-live-docs/data-docs-helper.sh

Usage:
- /livedocs                       — list available sources
- /livedocs <source>              — list topics under a source
- /livedocs <source> <topic>      — read a doc
- /livedocs search <query>        — full-text search across all sources
- /livedocs -t                    — freshness summary
- /livedocs whats-new             — recent updates

Examples:
  /livedocs dbt-core overview
  /livedocs bigquery partitioning
  /livedocs search materialized

Execute: ~/.data-live-docs/data-docs-helper.sh "$ARGUMENTS"
EOF
echo "✓ Wrote $COMMAND_FILE"

echo ""
echo "Registering PreToolUse hook…"
mkdir -p "$(dirname "$SETTINGS_FILE")"
if [[ -f "$SETTINGS_FILE" ]]; then
    # Strip any prior data-live-docs hook entries, then append a fresh one.
    tmp=$(mktemp)
    jq --arg cmd "$HOOK_COMMAND" '
      .hooks.PreToolUse =
        ((.hooks.PreToolUse // [])
          | map(select(
              (.hooks // [])
              | map(.command // "")
              | any(contains("data-live-docs")) | not
            ))
        )
        + [{matcher: "Read", hooks: [{type: "command", command: $cmd}]}]
    ' "$SETTINGS_FILE" > "$tmp"
    mv "$tmp" "$SETTINGS_FILE"
    echo "✓ Updated $SETTINGS_FILE"
else
    jq -n --arg cmd "$HOOK_COMMAND" '{
        hooks: {
            PreToolUse: [
                {matcher: "Read", hooks: [{type: "command", command: $cmd}]}
            ]
        }
    }' > "$SETTINGS_FILE"
    echo "✓ Created $SETTINGS_FILE"
fi

echo ""
echo "✅ data-live-docs installed"
echo ""
echo "📂 Location: $INSTALL_DIR"
echo "📚 Command:  /livedocs"
echo ""
echo "Try:"
echo "  /livedocs"
echo "  /livedocs dbt-core overview"
echo "  /livedocs search materialized"
echo ""
echo "⚠️  Restart Claude Code for the hook and slash command to take effect."
