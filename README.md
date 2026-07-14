# web-search

Web search skill for Claude Code — replaces the built-in `WebSearch` tool with
richer, better-formatted results.

## Features

- **DuckDuckGo search** — no API key needed, no rate limits for casual use
- **Clean Markdown output** — each result has title, URL, and snippet
- **JSON mode** — structured output for programmatic use
- **Configurable result count** — 1 to 30 results per query
- **Site-specific search** — `site:github.com` etc. supported
- **Zero dependencies fallback** — built-in `WebSearch` tool as backup

## Install

```bash
git clone https://github.com/mars-base/web-search.git
cd web-search
python3 -m pip install duckduckgo-search
```

On Windows, install Python from the Microsoft Store. On macOS/Linux with
system-managed Python, add `--break-system-packages` or use a venv.

## Usage

### As a script

```bash
# Basic search
python3 scripts/search.py "Python asyncio best practices"

# Limit results
python3 scripts/search.py "fastapi tutorial" --limit 5

# JSON output
python3 scripts/search.py "kubernetes helm" --json

# Site-specific
python3 scripts/search.py "site:github.com golang context"
```

### As a Claude Code skill

Symlink or copy the skill into your Claude Code skills directory:

```bash
ln -s ~/bucket/web-search ~/.claude/skills/web-search
```

Then invoke it with:

```
/web-search Python asyncio best practices
```

> **Tip:** If the built-in `WebSearch` tool returns sparse results, use `/web-search`
> as a drop-in replacement — it returns full titles, URLs, and snippets for every result.

### Configure global CLAUDE.md (recommended)

To make Claude Code always use `/web-search` instead of the built-in `WebSearch`
tool, add the following to your `~/.claude/CLAUDE.md`:

```markdown
## Web Search

Always use the `/web-search` skill for web searches — do not use the built-in WebSearch tool.
`/web-search` returns richer results with titles, URLs, and snippets formatted as clean Markdown.
```

## Output Format

Default Markdown:

```markdown
# Search results for: Python asyncio best practices

## 1. Async IO in Python: A Complete Walkthrough
**URL:** https://realpython.com/async-io-python/

Async IO is a concurrent programming design that has received dedicated support in Python...

## 2. asyncio — Asynchronous I/O — Python 3.12 documentation
**URL:** https://docs.python.org/3/library/asyncio.html

The asyncio library is used to write concurrent code using the async/await syntax...
```

## Project structure

```
web-search/
├── SKILL.md              # Claude Code skill definition
├── README.md             # This file
└── scripts/
    └── search.py          # Main search script
```

## License

MIT
