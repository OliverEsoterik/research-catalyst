---
name: research-scanner
description: Scan arXiv, SSRN, and archive.org for research papers, preprints, and historical publications.
---

# Research Scanner Skill

Find and fetch research papers across multiple open-access repositories.

## When to use

- The user asks for papers on a topic.
- You need to discover preprints, working papers, or historical archives.
- The built-in `academic_search` tool does not cover the required source (SSRN, archive.org).
- You want to cross-reference findings across different repositories.

## How to use

1. Run the search tool located in the skill directory:

```bash
python .agents/skills/research-scanner/search_research.py "machine learning in biology" --max-results 10
```

2. Filter by a single source with `--source`:

```bash
python .agents/skills/research-scanner/search_research.py "causal inference" --source arxiv --max-results 5
python .agents/skills/research-scanner/search_research.py "market microstructure" --source ssrn --max-results 5
python .agents/skills/research-scanner/search_research.py "vintag computing" --source archive --max-results 5
```

## Supported sources

| Source | Coverage | Notes |
|--------|----------|-------|
| **arXiv** | Physics, CS, math, quantitative biology/finance, etc. | Fast, reliable ATOM API. No API key. Output includes PDF link when available. |
| **SSRN** | Social sciences, economics, law, humanities | Parses search HTML; may break if SSRN changes layout. |
| **archive.org** | Books, papers, historical archives, software | Uses Internet Archive Advanced Search JSON API. |
| **Semantic Scholar** | General science, AI, and large-scale connections | *Available via academic_search tool.* |

## Other Recommended Research Sources

When the `research-scanner` tool doesn't provide enough coverage, consider these specialized sources:

- **PubMed**: The gold standard for biomedical and life sciences research.
- **Google Scholar**: Excellent for broad, multi-disciplinary searches and finding citations.
- **bioRxiv / medRxiv**: The primary repositories for biology and medicine preprints.
- **CORE**: One of the largest aggregators of open access research papers.
- **DOAJ (Directory of Open Access Journals)**: A community-curated list of high-quality, open access, peer-reviewed journals.

## Output format

Each result prints:

```
[Source] Paper Title
  Authors : Author names
  Date    : Publication date
  URL     : Link to abstract / details
  PDF     : Direct PDF link (when available)
  Abstract: Snippet of the abstract / description
```

## Limitations and caveats

- **Rate limits:** Do not hammer the APIs. Respect `timeout` values in the script.
- **SSRN stability:** SSRN does not have a public documented API for search; the tool parses HTML. If SSRN changes their layout, results may be empty.
- **No full-text download:** This tool only returns metadata and links. Follow the PDF/URL links to download or read full text.
- **No deduplication:** If the user searches a topic across all three sources, the same paper may appear on both arXiv and SSRN.

## Troubleshooting

- **Empty SSRN results?** SSRN may be blocking or changed their HTML. Advise the user to search SSRN manually at `https://www.ssrn.com`.
- **Connection timeout?** Check internet connectivity. The script uses 20-second timeouts.
- **Unicode errors?** The script explicitly decodes with `utf-8` and `replace`; report if characters still garble.
