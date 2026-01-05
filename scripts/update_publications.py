from scholarly import scholarly
from datetime import datetime

SCHOLAR_USER_ID = "0C7Wc-4AAAAJ"
OUTPUT_MD = "docs/publications.md"

def main():
    author = scholarly.search_author_id(SCHOLAR_USER_ID)
    author = scholarly.fill(author, sections=["publications"])

    pubs = author.get("publications", [])
    items = []
    for p in pubs:
        try:
            fp = scholarly.fill(p)  # fetch bib details
            bib = fp.get("bib", {})
            title = bib.get("title", "Untitled")
            year = bib.get("pub_year") or bib.get("year") or ""
            venue = bib.get("venue") or bib.get("journal") or ""
            authors = bib.get("author") or ""
            url = fp.get("pub_url") or ""
            items.append((year, title, authors, venue, url))
        except Exception:
            # If a single publication fails, skip it (Scholar can be flaky).
            continue

    # Sort by year desc (best-effort)
    def year_key(y):
        try:
            return int(y) if y else 0
        except ValueError:
            return 0

    items.sort(key=lambda x: year_key(x[0]), reverse=True)

    lines = []
    lines.append("# Publications\n")
    lines.append(f"_Generated from Google Scholar (user id `{SCHOLAR_USER_ID}`) on {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}._\n")

    if not items:
        lines.append("\nNo publications retrieved (Google Scholar may be rate-limiting). Try again later.\n")
    else:
        current_year = None
        for year, title, authors, venue, url in items:
            year = str(year) if year else "Unknown year"
            if year != current_year:
                lines.append(f"\n## {year}\n")
                current_year = year

            citation = f"**{title}**"
            if venue:
                citation += f" — *{venue}*"
            if authors:
                citation += f"<br><small>{authors}</small>"

            if url:
                lines.append(f"- {citation} ([link]({url}))")
            else:
                lines.append(f"- {citation}")

    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

if __name__ == "__main__":
    main()