#!/bin/bash
set -euo pipefail

# data-live-docs Helper Script
# Installation path: ~/.data-live-docs/data-docs-helper.sh

SCRIPT_VERSION="0.1.0"
DOCS_PATH="$HOME/.data-live-docs"
DOCS_DIR="$DOCS_PATH/docs"

sanitize_input() {
    echo "$1" | sed 's/[^a-zA-Z0-9 _.,'\''/?-]//g' | sed 's/  */ /g' | sed 's/^ *//;s/ *$//'
}

print_header() {
    echo "📚 MIRROR: https://github.com/filustre23/data-live-docs"
    echo ""
}

auto_update() {
    cd "$DOCS_PATH" 2>/dev/null || return 1
    local BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    if ! git fetch --quiet origin "$BRANCH" 2>/dev/null; then
        if ! git fetch --quiet origin main 2>/dev/null; then
            return 2
        fi
        BRANCH="main"
    fi
    local LOCAL=$(git rev-parse HEAD 2>/dev/null)
    local REMOTE=$(git rev-parse "origin/$BRANCH" 2>/dev/null)
    local BEHIND=$(git rev-list HEAD.."origin/$BRANCH" --count 2>/dev/null || echo "0")
    if [[ "$LOCAL" != "$REMOTE" ]] && [[ "$BEHIND" -gt 0 ]]; then
        echo "🔄 Updating documentation..." >&2
        git pull --quiet origin "$BRANCH" 2>&1 | grep -v "Merge made by" || true
    fi
    return 0
}

list_sources() {
    print_header
    if [[ ! -d "$DOCS_DIR" ]]; then
        echo "❌ No docs directory found at $DOCS_DIR"
        echo "Reinstall: curl -fsSL https://raw.githubusercontent.com/filustre23/data-live-docs/main/install.sh | bash"
        return 1
    fi
    auto_update || true
    echo "Available sources:"
    echo ""
    ls "$DOCS_DIR" 2>/dev/null | while read -r src; do
        [[ -d "$DOCS_DIR/$src" ]] || continue
        local count=$(find "$DOCS_DIR/$src" \( -name '*.md' -o -name '*.mdx' -o -name '*.rst' \) -not -name 'README.md' 2>/dev/null | wc -l | tr -d ' ')
        printf "  • %-20s (%s topics)\n" "$src" "$count"
    done
    echo ""
    echo "Usage: /livedocs <source> <topic>   |   /livedocs search <query>"
}

list_topics() {
    local source=$(sanitize_input "$1")
    local source_dir="$DOCS_DIR/$source"
    if [[ ! -d "$source_dir" ]]; then
        print_header
        echo "❌ Unknown source: $source"
        echo ""
        list_sources
        return 1
    fi
    print_header
    if [[ -f "$source_dir/README.md" ]]; then
        cat "$source_dir/README.md"
    else
        echo "Topics under $source:"
        find "$source_dir" -name '*.md' -not -name 'README.md' \
            | sed "s|^$source_dir/||" | sed 's|\.md$||' | sort
    fi
}

official_root_for() {
    local source="$1"
    local manifest="$DOCS_DIR/$source/_manifest.json"
    [[ -f "$manifest" ]] || { echo ""; return; }
    # Cheap jq replacement so we don't require it at read time.
    grep -o '"official_root": *"[^"]*"' "$manifest" | head -1 | sed 's/.*"official_root": *"\([^"]*\)".*/\1/'
}

read_doc() {
    local source=$(sanitize_input "$1")
    local topic=$(sanitize_input "$2")
    topic="${topic%.md}"

    local doc_path="$DOCS_DIR/$source/$topic.md"
    if [[ ! -f "$doc_path" ]]; then
        print_header
        echo "🔍 Not found: $source/$topic"
        echo ""
        echo "Searching for matches..."
        local matches=$(find "$DOCS_DIR/$source" -name '*.md' 2>/dev/null \
            | sed "s|^$DOCS_DIR/$source/||;s|\.md$||" \
            | grep -i -- "$topic" | head -10 || true)
        if [[ -n "$matches" ]]; then
            echo "$matches" | sed 's/^/  • /'
        else
            echo "No matches under $source. Try: /livedocs $source"
        fi
        return 1
    fi

    print_header
    auto_update || true

    cat "$doc_path"
    echo ""
    local official=$(official_root_for "$source")
    if [[ -n "$official" ]]; then
        echo "📖 Official: ${official}${topic}"
    fi
}

search_docs() {
    local query=$(sanitize_input "$1")
    if [[ -z "$query" ]]; then
        echo "Usage: /livedocs search <query>"
        return 1
    fi
    print_header
    if command -v rg >/dev/null 2>&1; then
        echo "🔍 Searching for: $query"
        echo ""
        rg --type md --max-count 3 -n -C 1 -- "$query" "$DOCS_DIR" 2>/dev/null || echo "No matches."
    else
        echo "⚠️  ripgrep (rg) not installed; falling back to grep"
        grep -rni --include='*.md' -- "$query" "$DOCS_DIR" 2>/dev/null | head -50 || echo "No matches."
    fi
}

show_freshness() {
    print_header
    auto_update
    local sync_status=$?
    cd "$DOCS_PATH" 2>/dev/null || exit 1
    local BRANCH=$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo "main")
    local AHEAD=$(git rev-list "origin/$BRANCH"..HEAD --count 2>/dev/null || echo "0")
    local BEHIND=$(git rev-list "HEAD..origin/$BRANCH" --count 2>/dev/null || echo "0")

    if [[ $sync_status -eq 2 ]]; then
        echo "⚠️  Could not sync with GitHub (using local cache)"
    elif [[ "$AHEAD" -gt 0 ]]; then
        echo "⚠️  Local is $AHEAD commit(s) ahead of origin"
    elif [[ "$BEHIND" -gt 0 ]]; then
        echo "⚠️  Local is $BEHIND commit(s) behind origin"
    else
        echo "✅ Up to date with origin/$BRANCH"
    fi
    echo "📦 Helper: v$SCRIPT_VERSION"
    echo ""
    echo "Per-source last fetch:"
    for src_dir in "$DOCS_DIR"/*/; do
        [[ -d "$src_dir" ]] || continue
        local manifest="$src_dir/_manifest.json"
        local slug=$(basename "$src_dir")
        if [[ -f "$manifest" ]]; then
            local fetched=$(grep -o '"fetched_at": *"[^"]*"' "$manifest" | head -1 \
                | sed 's/.*"fetched_at": *"\([^"]*\)".*/\1/')
            local count=$(grep -o '"file_count": *[0-9]*' "$manifest" | head -1 \
                | sed 's/.*"file_count": *\([0-9]*\).*/\1/')
            printf "  • %-20s %s (%s files)\n" "$slug" "$fetched" "$count"
        else
            printf "  • %-20s (no manifest)\n" "$slug"
        fi
    done
}

whats_new() {
    set +e
    print_header
    auto_update || true
    cd "$DOCS_PATH" 2>/dev/null || { echo "❌ Cannot cd to $DOCS_PATH"; return 1; }
    echo "📚 Recent updates:"
    echo ""
    local count=0
    while IFS= read -r commit_line && [[ $count -lt 5 ]]; do
        local hash=$(echo "$commit_line" | cut -d' ' -f1)
        local date=$(git show -s --format=%cr "$hash" 2>/dev/null || echo "unknown")
        echo "• $date:"
        echo "  📎 https://github.com/filustre23/data-live-docs/commit/$hash"
        local changed=$(git diff-tree --no-commit-id --name-only -r "$hash" -- 'docs/**/*.md' 2>/dev/null \
            | grep -v '/_manifest.json' | grep -v '/README.md' | head -8)
        if [[ -n "$changed" ]]; then
            echo "$changed" | sed 's|^docs/|  📄 |;s|\.md$||'
        fi
        echo ""
        ((count++))
    done < <(git log --oneline -10 -- 'docs/' 2>/dev/null | grep -v "Merge" || true)
    if [[ $count -eq 0 ]]; then
        echo "No recent updates found."
    fi
    echo "📎 Full log: https://github.com/filustre23/data-live-docs/commits/main"
    set -e
    return 0
}

hook_check() { exit 0; }

uninstall_msg() {
    print_header
    echo "Run: ~/.data-live-docs/uninstall.sh"
}

FULL_ARGS="$*"

case "${1:-}" in
    "")
        list_sources
        ;;
    -t|--check)
        show_freshness
        ;;
    hook-check)
        hook_check
        ;;
    whats-new|whats|what)
        if [[ "$FULL_ARGS" =~ new ]] || [[ "$1" == "whats-new" ]]; then
            whats_new
        else
            list_sources
        fi
        ;;
    search)
        shift
        search_docs "$*"
        ;;
    uninstall)
        uninstall_msg
        ;;
    *)
        if [[ "$FULL_ARGS" =~ what.*new ]]; then
            whats_new
        elif [[ -n "${2:-}" ]]; then
            read_doc "$1" "$2"
        else
            list_topics "$1"
        fi
        ;;
esac

exit 0
