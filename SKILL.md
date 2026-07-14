---
name: web-search
description: >
  Search the web and return top results as clean Markdown.
  Uses DuckDuckGo (via built-in WebSearch tool or local duckduckgo-search package).
  Returns titles, URLs, and snippets for each result.
  Use this skill whenever the user wants to search the web, find information online,
  look up current events, or research a topic — including phrases like "搜索一下",
  "查一下", "网上搜", "google一下", "search for", "look up", "find online".
---

# Web Search

Given a query, return the top web search results as clean Markdown — each result
includes title, URL, and a snippet/summary.

No initialization step needed. Works on Linux, macOS, and Windows.

## Recommended: Replace Built-in WebSearch

To make Claude Code always use `/web-search` instead of the built-in `WebSearch`
tool, add the following to your `~/.claude/CLAUDE.md`:

```markdown
## Web Search

Always use the `/web-search` skill for web searches — do not use the built-in WebSearch tool.
`/web-search` returns richer results with titles, URLs, and snippets formatted as clean Markdown.
```

This ensures every project automatically prefers `/web-search` over the default tool.

## Skill Invocation

When this skill is invoked, treat `args` as a search query (and optional flags).

### Search command

```bash
python3 <SKILL_DIR>/scripts/search.py "<query>" [--limit N] [--json]
```

`<SKILL_DIR>` is the directory where this SKILL.md lives.

> **Model instruction:** 
> 1. Run `search.py` with the provided query (default `--limit 10`).
> 2. **先总结**：把前 10 条搜索结果用 3-5 句话概括核心要点，呈现给用户。
> 3. **再询问**：问用户是否需要深入探索某个链接的内容，提供选项：
>    - "需要我提取前 3 个链接的正文吗？"
>    - "需要我提取前 5 个链接的正文吗？"
>    - "需要我提取全部 10 个链接的正文吗？"
>    - "不需要，这些摘要就够了"
> 4. 如果用户选择深入 → 用 `/web-fetch` 逐个提取所选链接的完整正文内容。
> 5. 如果脚本不可用，回退到内置 `WebSearch` 工具。

## Search Strategy

1. **Script first** — run `search.py` if `duckduckgo-search` is installed locally.
   Returns structured results with titles, URLs, and snippets.
2. **Built-in fallback** — if the script fails or dependencies are missing, use
   the built-in `WebSearch` tool as fallback.

## Script Options

```bash
# Basic search — returns top 10 results
python3 <SKILL_DIR>/scripts/search.py "Python asyncio best practices"

# Limit results
python3 <SKILL_DIR>/scripts/search.py "fastapi tutorial" --limit 5

# JSON output with metadata
python3 <SKILL_DIR>/scripts/search.py "kubernetes helm" --json

# Site-specific search
python3 <SKILL_DIR>/scripts/search.py "site:github.com golang context"
```

## Install Dependencies

First use only — the script checks and tells you if anything is missing:

```bash
python3 -m pip install duckduckgo-search
```

If on system-managed Python (macOS/Linux), add `--break-system-packages` or use a venv.

## Output Format

Default Markdown output:

```markdown
# Search results for: Python asyncio best practices

## 1. Async IO in Python: A Complete Walkthrough
**URL:** https://realpython.com/async-io-python/

Async IO is a concurrent programming design that has received dedicated support in Python...

## 2. asyncio — Asynchronous I/O — Python 3.12 documentation
**URL:** https://docs.python.org/3/library/asyncio.html

The asyncio library is used to write concurrent code using the async/await syntax...
```

## Failure Rules

- Search fails once → give up, tell the user "unable to search for this query"
- Do not retry the same query — each failed call wastes context tokens
