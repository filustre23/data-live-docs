#!/bin/bash
set -euo pipefail

# data-live-docs uninstaller

INSTALL_DIR="$HOME/.data-live-docs"
COMMAND_FILE="$HOME/.claude/commands/livedocs.md"
SETTINGS_FILE="$HOME/.claude/settings.json"

echo "data-live-docs uninstaller"
echo "=========================="
echo ""
echo "This will remove:"
echo "  • $COMMAND_FILE"
echo "  • the data-live-docs hook in $SETTINGS_FILE"
echo "  • $INSTALL_DIR"
echo ""

if [[ "${1:-}" != "-y" ]]; then
    read -p "Continue? [y/N]: " -n 1 -r
    echo
    [[ $REPLY =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
fi

if [[ -f "$COMMAND_FILE" ]]; then
    rm -f "$COMMAND_FILE"
    echo "✓ Removed $COMMAND_FILE"
fi

if [[ -f "$SETTINGS_FILE" ]] && command -v jq >/dev/null 2>&1; then
    tmp=$(mktemp)
    jq '
      .hooks.PreToolUse =
        ((.hooks.PreToolUse // [])
          | map(select(
              (.hooks // [])
              | map(.command // "")
              | any(contains("data-live-docs")) | not
            ))
        )
    ' "$SETTINGS_FILE" > "$tmp"
    mv "$tmp" "$SETTINGS_FILE"
    echo "✓ Removed hook from $SETTINGS_FILE"
fi

if [[ -d "$INSTALL_DIR" ]]; then
    rm -rf "$INSTALL_DIR"
    echo "✓ Removed $INSTALL_DIR"
fi

echo ""
echo "✅ Uninstalled. Restart Claude Code to drop the slash command."
