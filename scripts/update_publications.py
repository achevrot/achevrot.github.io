from scholarly import scholarly
from datetime import datetime

SCHOLAR_USER_ID = "0C7Wc-4AAAAJ"
OUTPUT_MD = "docs/publications.md"

def safe_year_to_int(y):
    try:
        return int(y)
    except Exception:
        return 0

def main():
    author = scholarly.search_author_id(SCHOLAR_USER_ID)
    author = scholarly.fill(author, sections=["publications"])

    pubs = author.get("publications", [])

    items = []
    for p in pubs:
        bib = p.get("bib", {}) or {}
        title = bib.get("title", "Untitled")
        year = bib.get("pub_year") or bib.get("year") or ""
        venue = bib.get("venue") or bib.get("journal") or ""
        authors = bib.get("author") or ""

        # In fast mode we avoid scholarly.fill(p). pub_url may be missing sometimes.
        url = p.get("pub_url") or ""

        items.append((str(year) if year else "Unknown year", title, authors, venue, url))

    # sort by year desc
    items.sort(key=lambda x: safe_year_to_int(x[0]) if x[0] != "Unknown year" else 0, reverse=True)

    lines = []
    lines.append("# Publications\n")
    lines.append(
        f"_Generated from Google Scholar (user id `{SCHOLAR_USER_ID}`) on "
        f"{datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}._\n"
    )
    lines.append(
        "\nNote: this list is generated in **fast mode** (no per-paper lookups) to keep builds quick.\n"
    )

    if not items:
        lines.append("\nNo publications retrieved (Google Scholar may be rate-limiting). Try again later.\n")
    else:
        current_year = None
        for year, title, authors, venue, url in items:
            if year != current_year:
                lines.append(f"\n## {year}\n")
                current_year = year

            entry = f"**{title}**"
            if venue:
                entry += f" — *{venue}*"
            if authors:
                entry += f"<br><small>{authors}</small>"

            if url:
                lines.append(f"- {entry} ([link]({url}))")
            else:
                lines.append(f"- {entry}")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()