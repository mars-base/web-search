#!/usr/bin/env python3
"""
Web search — returns top results as Markdown.

Usage:
  python3 search.py "query" [--engine ENGINE] [--limit N] [--json]

Options:
  --engine    Search engine: duck (default) | google
  --limit N   Number of results (default: 10, max: 30)
  --json      Output as JSON with metadata

Examples:
  python3 search.py "Python asyncio tutorial" --limit 5
  python3 search.py "site:github.com fastapi" --engine google --limit 10 --json
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


def search_google(query, limit=10):
    """
    Search Google by scraping the search results page with CloakBrowser.
    No API key required — uses stealth Chromium to bypass bot detection.
    Returns list of dicts: [{title, url, snippet}, ...]
    """
    import urllib.parse
    try:
        import cloakbrowser
    except ImportError:
        raise RuntimeError(
            "Google search via CloakBrowser requires the 'cloakbrowser' package.\n"
            "Install with: python3 -m pip install cloakbrowser"
        )

    search_url = "https://www.google.com/search?q=" + urllib.parse.quote(query)

    browser = cloakbrowser.launch(headless=True)
    try:
        page = browser.new_page()
        page.goto(search_url, wait_until="networkidle", timeout=60000)

        # Extract search results from Google DOM
        # Google result selectors (may change over time)
        results = []

        # Try multiple selector strategies
        selectors = [
            "div.g",           # Classic Google result container
            "div[data-sokoban-container]",  # Modern Google result
            "div.tF2Cxc",      # Another variant
        ]

        for sel in selectors:
            elements = page.query_selector_all(sel)
            if elements:
                for el in elements[:limit]:
                    try:
                        # Title
                        title_el = el.query_selector("h3")
                        title = title_el.inner_text() if title_el else ""

                        # URL
                        link_el = el.query_selector("a[href]")
                        url = ""
                        if link_el:
                            href = link_el.get_attribute("href") or ""
                            if href.startswith("/url?q="):
                                # Extract actual URL from Google's redirect
                                url = href.split("/url?q=")[1].split("&")[0]
                            elif href.startswith("http"):
                                url = href

                        # Snippet
                        snippet_el = el.query_selector("div.VwiC3b, span.aCOpRe, div.s3v94d")
                        snippet = snippet_el.inner_text() if snippet_el else ""

                        if title and url:
                            results.append({
                                "title": title,
                                "url": url,
                                "snippet": snippet,
                            })
                    except Exception:
                        continue

                if results:
                    break

        return results[:limit]
    finally:
        browser.close()


def search(query, limit=10, engine="duck"):
    """
    Search using the specified engine.
    engine: 'duck' (DuckDuckGo, default) or 'google' (CloakBrowser scraping)
    """
    if engine == "google":
        return search_google(query, limit)
    return search_duck(query, limit)
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
            "Usage: python3 search.py <query> [--engine ENGINE] [--limit N] [--json]\n"
            "\n"
            "Options:\n"
            "  --engine    Search engine: duck (default) | google\n"
            "  --limit N   Number of results (default: 10, max: 30)\n"
            "  --json      Output as JSON with metadata\n"
            "\n"
            "Google search uses CloakBrowser to scrape results (no API key).\n",
            file=sys.stderr,
        )
        sys.exit(1)

    query = sys.argv[1]
    args = sys.argv[2:]

    engine = "duck"
    limit = 10
    json_output = "--json" in args

    for i, a in enumerate(args):
        if a == "--engine" and i + 1 < len(args):
            engine = args[i + 1]
        if a == "--limit" and i + 1 < len(args):
            try:
                limit = int(args[i + 1])
            except ValueError:
                pass

    limit = max(1, min(limit, 30))

    try:
        results = search(query, limit, engine=engine)

        if json_output:
            print(json.dumps({
                "query": query,
                "engine": engine,
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
