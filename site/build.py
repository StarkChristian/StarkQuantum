#!/usr/bin/env python3
"""Stark Quantum static site generator.

Reads Markdown with YAML front matter from content/, renders it through the
Jinja2 templates in templates/, and writes a plain static site to public/.

The build is deliberately strict. It refuses to produce a site when an essay
is missing its four-part footer, when a brief has no primary source, or when
forbidden marketing vocabulary appears in body copy. A quiet failure would
let the doctrine erode one file at a time.

    .venv/bin/python build.py            build into public/
    .venv/bin/python build.py --serve    build, then serve public/ on :8000
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

from enhance import (build_term_matcher, first_sentence, protect_math,
                     reading_minutes, restore_math, write_og_image)

ROOT = Path(__file__).resolve().parent
CONTENT = ROOT / "content"
TEMPLATES = ROOT / "templates"
STATIC = ROOT / "static"
OUTPUT = ROOT / "public"

SITE = {
    "name": "Stark Quantum",
    "domain": "www.starkquantum.com",
    "base_url": "https://www.starkquantum.com",
    "tagline": "Quantum, without the press release.",
    "description": (
        "Independent notes on quantum hardware, error correction, software, "
        "and the gap between a demo and a machine."
    ),
    "author": "Christian Stark",
    "email": "info@starkquantum.com",
    "telegram": "",
    "doctrine_version": "1.1",
    # Visitor statistics. Self-hosted Umami; no cookies. Remove both keys to
    # drop the script from every page. The privacy notice describes it.
    "umami_src": "https://umami.homomorphicprivacy.com/script.js",
    "umami_website_id": "7f739503-4725-4be1-ac3c-37e1fdfe0c6f",
}

# Doctrine section 2. These must not appear in published body copy.
FORBIDDEN = [
    r"\brevolution",
    r"\bchange the world\b",
    r"\bcomputer of the future\b",
    r"\bdefinitive supremacy\b",
    r"#breakthrough",
]

# "Start here" is a reading order, not a publication order. These three
# foundation essays build on each other and are listed in that sequence.
START_HERE = [
    "physical-qubit-is-not-a-computer",
    "what-a-logical-qubit-actually-is",
    "how-to-read-a-quantum-claim",
]

ESSAY_CATEGORIES = [
    ("foundations", "Foundations"),
    ("hardware-and-error", "Hardware & error"),
    ("tooling", "Tooling"),
    ("applications-and-limits", "Applications & limits"),
]
CATEGORY_LABELS = dict(ESSAY_CATEGORIES)
DIFFICULTIES = ["Intro", "Intermediate", "Advanced"]

MD = markdown.Markdown(
    extensions=["extra", "sane_lists", "smarty", "toc"],
    extension_configs={"toc": {"toc_depth": "2", "permalink": False}},
    output_format="html5",
)

errors: list[str] = []


def fail(where: str, message: str) -> None:
    errors.append(f"{where}: {message}")


def render_markdown_toc(text: str, where: str = "") -> tuple[str, list[dict]]:
    """Render Markdown to HTML, with formulas as MathML, plus its h2 outline."""
    text, formulas = protect_math(text, where, fail)
    MD.reset()
    rendered = MD.convert(text)
    toc = [{"id": t["id"], "name": t["name"]} for t in MD.toc_tokens]
    return restore_math(rendered, formulas), toc


def render_markdown(text: str, where: str = "") -> str:
    return render_markdown_toc(text, where)[0]


def read_doc(path: Path) -> tuple[dict, str]:
    """Split a Markdown file into its YAML front matter and its body."""
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        fail(path.name, "missing YAML front matter")
        return {}, raw
    parts = raw.split("---", 2)
    if len(parts) < 3:
        fail(path.name, "malformed YAML front matter")
        return {}, raw
    try:
        meta = yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError as exc:
        fail(path.name, f"unreadable YAML front matter: {exc}")
        return {}, parts[2]
    if not isinstance(meta, dict):
        fail(path.name, "front matter must be a mapping")
        meta = {}
    return meta, parts[2].strip()


# Arabic, Arabic Supplement/Extended, and Arabic Presentation Forms blocks.
# Written as codepoints so this file stays pure ASCII: a detector should not
# be the one place in the project that contains the script it rejects.
NON_LATIN_RANGES = ((0x0600, 0x06FF), (0x0750, 0x077F), (0x08A0, 0x08FF),
                    (0xFB50, 0xFDFF), (0xFE70, 0xFEFF))


def check_language(path: Path, body: str) -> None:
    """English only. Flag any Arabic-script character, Persian included."""
    for ch in body:
        code = ord(ch)
        if any(low <= code <= high for low, high in NON_LATIN_RANGES):
            fail(path.name, "non-English (Arabic-script) characters found")
            return


def check_forbidden(path: Path, body: str) -> None:
    lowered = body.lower()
    for pattern in FORBIDDEN:
        if re.search(pattern, lowered):
            fail(path.name, f"forbidden vocabulary matches /{pattern}/")


def as_date(value, path: Path, field: str):
    if value is None:
        return None
    if isinstance(value, dt.date):
        return value
    try:
        return dt.date.fromisoformat(str(value))
    except ValueError:
        fail(path.name, f"{field} is not an ISO date (YYYY-MM-DD)")
        return None


def word_count(body: str) -> int:
    return len(re.findall(r"[A-Za-z0-9-]+", body))


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def load_essays() -> list[dict]:
    essays = []
    for path in sorted((CONTENT / "essays").glob("*.md")):
        meta, body = read_doc(path)
        if not meta:
            continue
        check_language(path, body)
        check_forbidden(path, body)
        slug = meta.get("slug") or path.stem

        for field in ("title", "summary", "category", "published"):
            if not meta.get(field):
                fail(path.name, f"missing required field '{field}'")

        category = meta.get("category", "")
        if category and category not in CATEGORY_LABELS:
            fail(path.name, f"unknown category '{category}'")

        difficulty = meta.get("difficulty", "Intermediate")
        if difficulty not in DIFFICULTIES:
            fail(path.name, f"unknown difficulty '{difficulty}'")

        footer = meta.get("footer") or {}
        for key in ("claim", "evidence", "missing_piece", "so_what"):
            if not footer.get(key):
                fail(path.name, f"footer box is missing '{key}'")

        words = word_count(body)
        if not 700 <= words <= 1400:
            fail(path.name, f"{words} words, outside the 700-1400 range")

        body_html, toc = render_markdown_toc(body, path.name)
        essays.append({
            "kind": "essay",
            "slug": slug,
            "url": f"/articles/{slug}/",
            "title": meta.get("title", slug),
            "summary": meta.get("summary", ""),
            "category": category,
            "category_label": CATEGORY_LABELS.get(category, category),
            "difficulty": difficulty,
            "published": as_date(meta.get("published"), path, "published"),
            "reviewed": as_date(meta.get("reviewed"), path, "reviewed"),
            "living": bool(meta.get("living", True)),
            "sources": meta.get("sources") or [],
            "footer": footer,
            "body_html": body_html,
            "toc": toc,
            "minutes": reading_minutes(words),
            "body_text": body,
        })
    essays.sort(key=lambda e: (e["published"] or dt.date.min), reverse=True)
    return essays


def load_briefs() -> list[dict]:
    briefs = []
    for path in sorted((CONTENT / "news").glob("*.md")):
        meta, body = read_doc(path)
        if not meta:
            continue
        check_language(path, body)
        check_forbidden(path, body)
        slug = meta.get("slug") or path.stem

        for field in ("title", "published", "source_url", "source_name"):
            if not meta.get(field):
                fail(path.name, f"missing required field '{field}'")

        is_example = bool(meta.get("example", False))
        if not is_example and not str(meta.get("source_url", "")).startswith("http"):
            fail(path.name, "source_url must be a real primary-source link")

        briefs.append({
            "kind": "brief",
            "slug": slug,
            "url": f"/news/{slug}/",
            "title": meta.get("title", slug),
            "published": as_date(meta.get("published"), path, "published"),
            "source_url": meta.get("source_url", ""),
            "source_name": meta.get("source_name", ""),
            "source_type": meta.get("source_type", ""),
            "entity": meta.get("entity", ""),
            "numbers": meta.get("numbers") or [],
            "limits": meta.get("limits") or [],
            "example": is_example,
            "corrections": meta.get("corrections") or [],
            "body_html": render_markdown(body, path.name),
            "body_text": body,
        })
    briefs.sort(key=lambda b: (b["published"] or dt.date.min), reverse=True)
    return briefs


def load_glossary() -> list[dict]:
    terms = []
    for path in sorted((CONTENT / "glossary").glob("*.md")):
        meta, body = read_doc(path)
        if not meta:
            continue
        check_language(path, body)
        if not meta.get("term"):
            fail(path.name, "missing required field 'term'")
        slug = meta.get("slug") or path.stem
        terms.append({
            "kind": "glossary",
            "slug": slug,
            "url": f"/glossary/#{slug}",
            "term": meta.get("term", path.stem),
            "aka": meta.get("aka") or [],
            "title": meta.get("term", path.stem),
            "definition": first_sentence(body),
            "body_html": render_markdown(body, path.name),
            "body_text": body,
        })
    terms.sort(key=lambda t: t["term"].lower())
    return terms


def load_reality() -> list[dict]:
    cells = []
    allowed = {"not-yet", "early", "partial", "yes"}
    for path in sorted((CONTENT / "reality").glob("*.md")):
        meta, body = read_doc(path)
        if not meta:
            continue
        check_language(path, body)
        # YAML reads a bare 'yes' or 'no' as a boolean, so normalise before
        # comparing. Without this, the guard below never sees the word 'yes'.
        status = meta.get("status", "not-yet")
        if isinstance(status, bool):
            status = "yes" if status else "no"
        status = str(status)
        if status not in allowed:
            fail(path.name, f"status '{status}' is not one of {sorted(allowed)}")
        if status == "yes":
            fail(path.name, "a cell may not be set to 'yes' without a doctrine review")
        cells.append({
            "order": meta.get("order", 99),
            "question": meta.get("question", path.stem),
            "status": status,
            "status_label": meta.get("status_label", "Not yet"),
            "reviewed": as_date(meta.get("reviewed"), path, "reviewed"),
            "would_change_it": meta.get("would_change_it") or [],
            # Dated record of every change to this answer, newest first.
            "changes": sorted(meta.get("changes") or [],
                              key=lambda c: str(c.get("date", "")), reverse=True),
            "body_html": render_markdown(body),
        })
    if len(cells) != 4:
        fail("content/reality", f"the board has {len(cells)} cells; it must have exactly 4")
    cells.sort(key=lambda c: c["order"])
    return cells


def load_page(name: str) -> dict:
    path = CONTENT / "pages" / f"{name}.md"
    meta, body = read_doc(path)
    check_language(path, body)
    # No check_forbidden here on purpose. The forbidden-vocabulary list is a
    # voice rule for drafts (doctrine section 2) and applies to essays and
    # briefs. Legal pages must be free to use the wording the law requires.
    return {
        "title": meta.get("title", name.title()),
        "summary": meta.get("summary", ""),
        "updated": as_date(meta.get("updated"), path, "updated"),
        "body_html": render_markdown(body),
        "body_text": body,
    }


def load_sources() -> dict:
    path = CONTENT / "sources.yml"
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


# ---------------------------------------------------------------------------
# Writing
# ---------------------------------------------------------------------------

def write(env: Environment, out_path: str, template: str, **ctx) -> None:
    clean = out_path.strip("/")
    if clean.endswith(".html"):
        target = OUTPUT / clean
    elif clean == "":
        target = OUTPUT / "index.html"
    else:
        target = OUTPUT / clean / "index.html"
    target.parent.mkdir(parents=True, exist_ok=True)
    ctx.setdefault("og_image", "/og/default.png")
    html = env.get_template(template).render(site=SITE, current=out_path, **ctx)
    target.write_text(html, encoding="utf-8")


def write_og_images(essays, briefs) -> None:
    """One link-preview card per essay and brief, plus a default for the rest."""
    write_og_image(OUTPUT / "og" / "default.png", SITE["description"],
                   SITE["name"])
    for item in essays:
        item["og_image"] = f"/og/essay-{item['slug']}.png"
        write_og_image(OUTPUT / item["og_image"].lstrip("/"), item["title"],
                       f"Essay / {item['category_label']}")
    for item in briefs:
        item["og_image"] = f"/og/brief-{item['slug']}.png"
        write_og_image(OUTPUT / item["og_image"].lstrip("/"), item["title"],
                       "Brief")


def build_pagefind() -> None:
    """Index public/ for in-browser search. The site still works without it:
    site.js falls back to search-index.json when /pagefind/ is missing."""
    try:
        subprocess.run([sys.executable, "-m", "pagefind", "--site", str(OUTPUT)],
                       check=True, capture_output=True, text=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        detail = getattr(exc, "stderr", "") or exc
        print(f"warning: pagefind index not built ({detail})", file=sys.stderr)


def build_search_index(essays, briefs, terms) -> list[dict]:
    index = []
    for item in essays:
        index.append({
            "title": item["title"],
            "url": item["url"],
            "type": "Essay",
            "meta": f"{item['category_label']} / {item['difficulty']}",
            "text": item["summary"],
        })
    for item in briefs:
        index.append({
            "title": item["title"],
            "url": item["url"],
            "type": "Brief",
            "meta": item["source_name"],
            "text": item["body_text"][:280],
        })
    for item in terms:
        index.append({
            "title": item["term"],
            "url": item["url"],
            "type": "Glossary",
            # The type label already says Glossary; repeating it in the meta
            # line renders as "Glossary / Glossary" in the search panel.
            "meta": "",
            "text": item["body_text"][:280],
        })
    return index


def escape(text: str) -> str:
    return (str(text).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;"))


def build_feed(essays, briefs) -> str:
    entries = sorted(essays + briefs,
                     key=lambda e: (e["published"] or dt.date.min),
                     reverse=True)[:40]
    items = []
    for entry in entries:
        link = SITE["base_url"] + entry["url"]
        summary = entry.get("summary") or entry["body_text"][:280]
        pub = entry["published"] or dt.date.today()
        stamp = pub.strftime("%a, %d %b %Y") + " 00:00:00 +0000"
        items.append(
            "    <item>\n"
            f"      <title>{escape(entry['title'])}</title>\n"
            f"      <link>{link}</link>\n"
            f'      <guid isPermaLink="true">{link}</guid>\n'
            f"      <pubDate>{stamp}</pubDate>\n"
            f"      <description>{escape(summary)}</description>\n"
            "    </item>"
        )
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n  <channel>\n'
        f"    <title>{SITE['name']}</title>\n"
        f"    <link>{SITE['base_url']}/</link>\n"
        f"    <description>{escape(SITE['description'])}</description>\n"
        "    <language>en</language>\n"
        + "\n".join(items)
        + "\n  </channel>\n</rss>\n"
    )


def asset_url(name: str) -> str:
    """Return /static/<name> with a content hash appended.

    The edge caches /static/ for an hour. Without a hash in the URL an edited
    stylesheet stays invisible to readers until that expires, which makes a
    rebuild a half-truth. A content hash makes a changed file a new URL.
    """
    digest = hashlib.md5((STATIC / name).read_bytes()).hexdigest()[:10]
    return f"/static/{name}?v={digest}"


def long_date(value) -> str:
    if not value:
        return ""
    return f"{value.day} {value.strftime('%B %Y')}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the Stark Quantum site.")
    parser.add_argument("--serve", action="store_true",
                        help="serve public/ after building")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args()

    essays = load_essays()
    briefs = load_briefs()
    terms = load_glossary()
    cells = load_reality()
    sources = load_sources()
    about = load_page("about")
    privacy = load_page("privacy")
    impressum = load_page("impressum")
    disclaimer = load_page("disclaimer")

    if errors:
        print("Build refused. Fix these first:\n", file=sys.stderr)
        for line in errors:
            print(f"  - {line}", file=sys.stderr)
        return 1

    # Clear the contents of public/ but never the directory itself. The
    # production container bind-mounts this directory, and replacing it would
    # leave that mount pointing at a deleted inode: the site would keep
    # serving stale files until someone recreated the container.
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for child in OUTPUT.iterdir():
        if child.is_dir() and not child.is_symlink():
            shutil.rmtree(child)
        else:
            child.unlink()
    shutil.copytree(STATIC, OUTPUT / "static")
    # Cloudflare Pages reads _headers (and _redirects) from the output root.
    pages_config = ROOT / "pages-config"
    if pages_config.is_dir():
        for extra in pages_config.iterdir():
            shutil.copy2(extra, OUTPUT / extra.name)

    env = Environment(
        loader=FileSystemLoader(TEMPLATES),
        autoescape=True,
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["longdate"] = long_date
    env.globals["asset"] = asset_url

    by_slug = {e["slug"]: e for e in essays}
    start_here = [by_slug[slug] for slug in START_HERE if slug in by_slug]

    # First mention of each glossary term in an essay or brief links to its
    # definition. Glossary entries and legal pages are left alone.
    link_terms = build_term_matcher(terms)
    for item in essays + briefs:
        item["body_html"] = link_terms(item["body_html"])

    write_og_images(essays, briefs)

    write(env, "/", "home.html", essays=essays[:6], briefs=briefs[:5],
          cells=cells, start_here=start_here)
    write(env, "/about/", "page.html", page=about)
    write(env, "/privacy/", "page.html", page=privacy)
    write(env, "/impressum/", "page.html", page=impressum)
    write(env, "/disclaimer/", "page.html", page=disclaimer)
    write(env, "/articles/", "essay_index.html", essays=essays,
          categories=ESSAY_CATEGORIES)
    # essays is newest first, so the older neighbour is the next index.
    for i, essay in enumerate(essays):
        write(env, essay["url"], "essay.html", essay=essay,
              og_image=essay["og_image"],
              newer=essays[i - 1] if i > 0 else None,
              older=essays[i + 1] if i + 1 < len(essays) else None)
    write(env, "/news/", "brief_index.html", briefs=briefs)
    for brief in briefs:
        write(env, brief["url"], "brief.html", brief=brief,
              og_image=brief["og_image"])
    write(env, "/reality/", "reality.html", cells=cells)
    write(env, "/glossary/", "glossary.html", terms=terms)
    write(env, "/sources/", "sources.html", sources=sources)
    write(env, "/404.html", "page.html", page={
        "title": "Not here",
        "summary": "",
        "updated": None,
        "body_html": ('<p>That page does not exist. Try the '
                      '<a href="/articles/">essays</a> or the '
                      '<a href="/news/">briefs</a>.</p>'),
    })

    (OUTPUT / "search-index.json").write_text(
        json.dumps(build_search_index(essays, briefs, terms)), encoding="utf-8")
    (OUTPUT / "feed.xml").write_text(build_feed(essays, briefs), encoding="utf-8")
    (OUTPUT / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {SITE['base_url']}/sitemap.xml\n",
        encoding="utf-8")

    # Every URL carries a lastmod taken from the page's own date: an essay's
    # reviewed or published date, a brief's publication date, a legal page's
    # updated date. Index pages take the newest date of what they list. The
    # glossary and sources pages carry no date of their own, so they use the
    # last git commit date of the files they are built from (file mtime outside git). No changefreq and
    # no priority: both are ignored and neither is a fact about the page.
    def newest(dates):
        real = [d for d in dates if d]
        return max(real) if real else dt.date.today()

    def content_hash(paths):
        digest = hashlib.sha256()
        for path in sorted(paths):
            digest.update(path.name.encode())
            digest.update(path.read_bytes())
        return digest.hexdigest()[:16]

    lastmod_file = ROOT / "lastmod.yml"
    lastmod_map = (yaml.safe_load(lastmod_file.read_text(encoding="utf-8"))
                   if lastmod_file.exists() else None) or {}

    def file_date(paths, key):
        existing = [p for p in paths if p.exists()]
        # A committed date wins while the source files are unchanged since it
        # was recorded (see lastmod.yml). A fresh checkout (CI, Cloudflare
        # Pages) gives every file the checkout time as its mtime, so mtime is
        # no use here.
        entry = lastmod_map.get(key)
        if entry and existing and entry.get("hash") == content_hash(existing):
            return dt.date.fromisoformat(str(entry["date"]))
        # Files changed since the map was written: use the last git commit
        # that touched them. In a shallow clone this is the newest commit.
        if existing:
            try:
                out = subprocess.run(
                    ["git", "log", "-1", "--format=%cs", "--", *map(str, existing)],
                    cwd=ROOT, capture_output=True, text=True, check=True,
                ).stdout.strip()
                if out:
                    return dt.date.fromisoformat(out)
            except (OSError, subprocess.CalledProcessError, ValueError):
                pass
        stamps = [p.stat().st_mtime for p in existing]
        if not stamps:
            return dt.date.today()
        return dt.date.fromtimestamp(max(stamps))

    essay_dates = [e["reviewed"] or e["published"] for e in essays]
    brief_dates = [b["published"] for b in briefs]
    cell_dates = [c["reviewed"] for c in cells]
    glossary_date = file_date(sorted((CONTENT / "glossary").glob("*.md")), "glossary")
    sources_date = file_date([CONTENT / "sources.yml"], "sources")

    pages = [
        ("/about/", about["updated"]),
        ("/articles/", newest(essay_dates)),
        ("/news/", newest(brief_dates)),
        ("/reality/", newest(cell_dates)),
        ("/glossary/", glossary_date),
        ("/sources/", sources_date),
        ("/privacy/", privacy["updated"]),
        ("/impressum/", impressum["updated"]),
        ("/disclaimer/", disclaimer["updated"]),
    ]
    pages += [(e["url"], e["reviewed"] or e["published"]) for e in essays]
    pages += [(b["url"], b["published"]) for b in briefs]
    pages.insert(0, ("/", newest([d for _, d in pages])))

    sitemap = "\n".join(
        f"  <url><loc>{SITE['base_url']}{url}</loc>"
        f"<lastmod>{date.isoformat()}</lastmod></url>"
        for url, date in pages
    )
    (OUTPUT / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{sitemap}\n</urlset>\n", encoding="utf-8")
    urls = [url for url, _ in pages]

    build_pagefind()

    print(f"Built {len(urls)} pages:{len(essays)} essays, {len(briefs)} briefs, "
          f"{len(terms)} glossary terms, {len(cells)} board cells.")

    if args.serve:
        import functools
        import http.server
        import socketserver
        handler = functools.partial(http.server.SimpleHTTPRequestHandler,
                                    directory=str(OUTPUT))
        with socketserver.TCPServer(("0.0.0.0", args.port), handler) as httpd:
            print(f"Serving public/ on http://0.0.0.0:{args.port} — Ctrl-C to stop.")
            httpd.serve_forever()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
