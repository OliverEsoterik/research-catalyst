#!/usr/bin/env python3 tyrant

"""
Multi-source research paper search tool.
Searches arXiv, SSRN, and Internet Archive for papers/publications.
Usage: python search_research.py <query> [--max-results N] [--source {all,arxiv,ssrn,archive}]
"""

import argparse
import sys
import urllib.parse
import urllib.request
from xml.etree import ElementTree as ET


def search_arxiv(query, max_results=10):
    """Search arXiv using the public ATOM API."""
    url = (
        "http://export.arxiv.org/api/query?"
        f"search_query=all:{urllib.parse.quote(query)}&"
        f"start=0&max_results={max_results}&sortBy=relevance&sortOrder=descending"
    )
    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            data = resp.read()
    except Exception as e:
        print(f"arXiv error: {e}", file=sys.stderr)
        return []

    # ATOM namespace
    ns = {"atom": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(data)
    entries = []

    for entry in root.findall("atom:entry", ns):
        title = entry.find("atom:title", ns)
        summary = entry.find("atom:summary", ns)
        published = entry.find("atom:published", ns)
        link_el = entry.find("atom:id", ns)
        authors = entry.findall("atom:author/atom:name", ns)
        pdf_link_el = entry.find("atom:link[@title='pdf']", ns)

        if title is None:
            continue

        title_text = (title.text or "").strip()
        summary_text = (summary.text or "").strip() if summary is not None else ""
        published_text = (published.text or "").strip() if published is not None else ""
        link_text = (link_el.text or "").strip() if link_el is not None else ""
        author_text = ", ".join((a.text or "").strip() for a in authors)
        pdf_text = pdf_link_el.get("href") if pdf_link_el is not None else ""

        entries.append({
            "source": "arXiv",
            "title": title_text,
            "authors": author_text,
            "published": published_text,
            "url": link_text,
            "pdf": pdf_text,
            "abstract": summary_text[:500] + "..." if len(summary_text) > 500 else summary_text,
        })

    return entries


def search_ssrn(query, max_results=10):
    """
    Search SSRN using their public search endpoint.
    Returns a list of entry dicts (may be empty on failure).
    """
    import json

    # SSRN uses an internal API that serves JSON. We replicate the browser call.
    # This endpoint is subject to change; if it breaks, fall back to manual search.
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0)",
        "Accept": "application/json",
    }

    try:
        # Try the public search page with a structured query
        # SSRN's API is not officially documented, so we use a basic approach
        url = (
            "https://www.ssrn.com/index.cfm/en/search/?"
            f"q={urllib.parse.quote(query)}&t=publications"
        )
        req = urllib.request.Request(url, headers= headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            html = resp.read().decode("utf-8", "replace")

        import re
        results = []
        # Dead-simple extraction of paper links and titles from SSRN search results
        # Each result item looks like: <a href=".../abstract_id=..." ...>Title</a>
        # We grab the most obvious matches
        for m in re.finditer(r'<a[^>]*href="(/abstract=[0-9]+)"[^>]*>([^<]+)</a>', html):
            abstract_url = "https://www.ssrn.com" + m.group(1)
            title = re.sub(r"\s+", " ", m.group(2)).strip()
            if title:
                results.append({
                    "source": "SSRN",
                    "title": title,
                    "authors": "",
                    "published": "",
                    "url": abstract_url,
                    "pdf": "",
                    "abstract": "",
                })
        if results:
            return results[:max_results]
    except Exception as e:
        print(f"SSRN error: {e}", file=sys.stderr)

    # Fallback / alternative: try the SSRN solr endpoint if available
    try:
        url = "https://papers.ssrn.com/solr3/solr/en_select/"  # may be deprecated
        # If the above fails silently, we still return empty list
    except Exception:
        pass

    return []


def search_archive_org(query, max_results=10):
    """Search Internet Archive using the Advanced Search API."""
    import json

    fields = "title,creator,date,description,identifier"
    url = (
        "https://archive.org/advancedsearch.php?"
        f"q={urllib.parse.quote(query)}&"
        f"fl={fields}&"
        f"sort[]=date+desc&rows={max_results}&page=1&output=json&save=yes"
    )

    try:
        with urllib.request.urlopen(url, timeout=20) as resp:
            data = json.loads(resp.read().decode("utf-8", "replace"))
    except Exception as e:
        print(f"archive.org error: {e}", file=sys.stderr)
        return []

    docs = data.get("response", {}).get("docs", [])
    entries = []
    for doc in docs:
        identifier = doc.get("identifier", "")
        title = doc.get("title", "")
        if isinstance(title, list):
            title = title[0] if title else ""
        creator = doc.get("creator", "")
        if isinstance(creator, list):
            creator = ", ".join(creator)
        date = doc.get("date", "")
        desc = doc.get("description", "")
        if isinstance(desc, list):
            desc = " ".join(str(d) for d in desc)

        entries.append({
            "source": "Archive.org",
            "title": str(title),
            "authors": str(creator),
            "published": str(date),
            "url": f"https://archive.org/details/{identifier}" if identifier else "",
            "pdf": f"https://archive.org/download/{identifier}/{identifier}_text.pdf" if identifier else "",
            "abstract": str(desc)[:300] + "..." if len(str(desc)) > 300 else str(desc),
        })

    return entries


def print_results(entries):
    if not entries:
        print("No results found.")
        return

    for entry in entries:
        print("=" * 70)
        print(f"[{entry['source']}] {entry['title']}")
        if entry.get("authors"):
            print(f"  Authors : {entry['authors']}")
        if entry.get("published"):
            print(f"  Date    : {entry['published']}")
        if entry.get("url"):
            print(f"  URL     : {entry['url']}")
        if entry.get("pdf"):
            print(f"  PDF     : {entry['pdf']}")
        if entry.get("abstract"):
            print(f"  Abstract: {entry['abstract']}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Search arXiv, SSRN, and archive.org for research papers.")
    parser.add_argument("query", help="Search query.")
    parser.add_argument("--max-results", type=int, default=10, help="Max results per source (default: 10).")
    parser.add_argument("--source", choices=["all", "arxiv", "ssrn", "archive"], default="all", help="Source to search.")
    args = parser.parse_args()

    all_entries = []
    if args.source in ("all", "arxiv"):
        all_entries.extend(search_arxiv(args.query, args.max_results))
    if args.source in ("all", "ssrn"):
        all_entries.extend(search_ssrn(args.query, args.max_results))
    if args.source in ("all", "archive"):
        all_entries.extend(search_archive_org(args.query, args.max_results))

    print_results(all_entries)


if __name__ == "__main__":
    main()
