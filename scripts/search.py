#!/usr/bin/env python3
"""
Web search via DuckDuckGo — returns top results as Markdown.

Usage:
  python3 search.py "query" [--limit N] [--json]

Options:
  --limit N   Number of results (default: 10, max: 30)
  --json      Output as JSON with metadata

Examples:
  python3 search.py "Python asyncio tutorial" --limit 5
  python3 search.py "site:github.com fastapi" 10 --json
"""

import sys
import json
import textwrap


def check_dependencies():
    """Check if required packages are installed and provide install instructions."""
    try:
        from ddgs import DDGS  # noqa: F401
        return
    except ImportError:
        pass

    try:
        from duckduckgo_search import DDGS  # noqa: F401
        return
    except ImportError:
        pass

    print(
        "Error: missing required dependency: ddgs (or duckduckgo-search)\n"
        "Install with one of:\n"
        "  python3 -m pip install ddgs\n"
        "  python3 -m pip install duckduckgo-search",
        file=sys.stderr,
    )
    sys.exit(1)


def search(query, limit=10):
    """
    Search DuckDuckGo and return results.
    Returns list of dicts: [{title, url, snippet}, ...]
    """
    try:
        from ddgs import DDGS
    except ImportError:
        from duckduckgo_search import DDGS

    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=limit))

    out = []
    for r in results:
        out.append({
            "title": r.get("title", ""),
            "url": r.get("href", r.get("link", "")),
            "snippet": r.get("body", r.get("snippet", "")),
        })
    return out


def results_to_markdown(results, query):
    """Format search results as clean Markdown."""
    lines = [f"# Search results for: {query}\n"]
    for i, r in enumerate(results, 1):
        lines.append(f"## {i}. {r['title']}")
        lines.append(f"**URL:** {r['url']}")
        lines.append("")
        # Wrap snippet for readability
        snippet = r.get("snippet", "")
        if snippet:
            wrapped = textwrap.fill(snippet, width=80)
            lines.append(wrapped)
        lines.append("")
    return "\n".join(lines)


def main():
    # Force UTF-8 output on Windows
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")

    if len(sys.argv) < 2:
        print(
            "Usage: python3 search.py <query> [--limit N] [--json]\n"
            "\n"
            "Options:\n"
            "  --limit N   Number of results (default: 10, max: 30)\n"
            "  --json      Output as JSON with metadata\n",
            file=sys.stderr,
        )
        sys.exit(1)

    query = sys.argv[1]
    args = sys.argv[2:]

    limit = 10
    json_output = "--json" in args

    for i, a in enumerate(args):
        if a == "--limit" and i + 1 < len(args):
            try:
                limit = int(args[i + 1])
            except ValueError:
                pass

    limit = max(1, min(limit, 30))

    try:
        results = search(query, limit)

        if json_output:
            print(json.dumps({
                "query": query,
                "count": len(results),
                "results": results,
            }, ensure_ascii=False, indent=2))
        else:
            print(results_to_markdown(results, query))

    except Exception as e:
        error_msg = f"Search error: {type(e).__name__}: {e}"
        if json_output:
            print(json.dumps({"query": query, "error": error_msg}, ensure_ascii=False))
        else:
            print(error_msg, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    check_dependencies()
    main()
