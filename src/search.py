"""
Voice AI news search module using Firecrawl Search API.
"""

import os
import logging
import requests

logger = logging.getLogger(__name__)

FIRECRAWL_API_URL = "https://api.firecrawl.dev/v1"

SEARCH_QUERIES = [
    '"voice AI" acquisition merger',
    '"voice AI" OR "语音AI" 并购 收购',
    '"voice AI startup" funding raised series',
    '"speech AI" OR "conversational AI" acquisition',
    '"voice agent" startup funding',
]


def _firecrawl_search(query: str, api_key: str, limit: int = 8) -> list[dict]:
    """Execute a single Firecrawl search query."""
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": query,
        "limit": limit,
    }
    try:
        resp = requests.post(
            f"{FIRECRAWL_API_URL}/search",
            json=payload,
            headers=headers,
            timeout=30,
        )
        resp.raise_for_status()
        data = resp.json()
        results = []
        for item in data.get("data", []):
            results.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "description": item.get("description", ""),
                "source": _extract_domain(item.get("url", "")),
            })
        return results
    except Exception as e:
        logger.warning(f"Search failed for query '{query}': {e}")
        return []


def _extract_domain(url: str) -> str:
    """Extract domain name from URL."""
    try:
        from urllib.parse import urlparse
        parsed = urlparse(url)
        domain = parsed.netloc.replace("www.", "")
        return domain
    except Exception:
        return ""


def _deduplicate(results: list[dict]) -> list[dict]:
    """Deduplicate search results by URL."""
    seen_urls = set()
    unique = []
    for item in results:
        url = item.get("url", "")
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(item)
    return unique


def search_voice_ai_news(api_key: str | None = None) -> list[dict]:
    """
    Search for recent Voice AI M&A news and startup introductions.

    Returns a deduplicated list of search results:
    [{"title", "url", "description", "source"}, ...]
    """
    api_key = api_key or os.environ.get("FIRECRAWL_API_KEY", "")
    if not api_key:
        raise ValueError("FIRECRAWL_API_KEY is required")

    all_results = []
    for query in SEARCH_QUERIES:
        logger.info(f"Searching: {query}")
        results = _firecrawl_search(query, api_key)
        all_results.extend(results)
        logger.info(f"  Found {len(results)} results")

    unique = _deduplicate(all_results)
    logger.info(f"Total unique results: {len(unique)}")
    return unique


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = search_voice_ai_news()
    for r in results:
        print(f"- {r['title']} ({r['source']})")
        print(f"  {r['url']}")
