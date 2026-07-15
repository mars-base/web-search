# web-search

Web search skill for Claude Code — replaces the built-in `WebSearch` tool with
richer, better-formatted results.

## Features

- **Multi-engine support** — DuckDuckGo (default, free) or Google Custom Search (API key)
- **Dependency check** — auto-detects missing `ddgs`/`duckduckgo-search` on startup
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
python3 -m pip install ddgs
```

> **Note:** `ddgs` is the renamed package for `duckduckgo-search`. The script supports both — it tries `ddgs` first, then falls back to `duckduckgo-search`.

On Windows, install Python from the Microsoft Store. On macOS/Linux with
system-managed Python, add `--break-system-packages` or use a venv.

## Usage

### As a script

```bash
# Basic search — DuckDuckGo (default)
python3 scripts/search.py "Python asyncio best practices"

# Google search (requires API key)
python3 scripts/search.py "fastapi tutorial" --engine google

# Limit results
python3 scripts/search.py "kubernetes helm" --limit 5

# JSON output
python3 scripts/search.py "golang context" --json

# Site-specific
python3 scripts/search.py "site:github.com react hooks"
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

Search workflow:
1. Invoke `/web-search` to fetch top 10 results
2. Summarize key points in 3-5 sentences
3. Ask the user whether to explore deeper: extract content from top 3 / top 5 / all 10 links, or stop here
4. If the user chooses to explore, use `/web-fetch` to extract full content from each selected link
```

## Search Engines

| Engine | Flag | Requirements | Best for |
|--------|------|--------------|----------|
| DuckDuckGo | `--engine duck` (default) | `ddgs` or `duckduckgo-search` | Free, privacy-focused, no API key |
| Google | `--engine google` | `GOOGLE_API_KEY` + `GOOGLE_CX` | Higher quality, precise results |

### Google Custom Search setup (optional)

1. Get API Key: [Google Custom Search JSON API](https://developers.google.com/custom-search/v1/overview)
2. Create Search Engine: [Programmable Search Engine](https://programmablesearchengine.google.com/)
3. Set environment variables:
   ```bash
   export GOOGLE_API_KEY=your_api_key
   export GOOGLE_CX=your_search_engine_id
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
