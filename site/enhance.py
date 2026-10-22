"""Reading aids that build.py applies on top of rendered Markdown.

Everything here works on text and HTML at build time. Nothing ships to the
reader's browser except the markup it produces: MathML, plain links, and a
PNG for link previews.

    protect_math / restore_math   $...$ and $$...$$ to MathML
    autolink_terms                first mention of a glossary term -> glossary
    reading_minutes               words / reading speed
    write_og_image                1200x630 link-preview card
"""

from __future__ import annotations

import html
import math
import re
from pathlib import Path

import latex2mathml.converter
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Math
# ---------------------------------------------------------------------------

# Display math is $$ ... $$. Inline math is $...$ with no space just inside
# the delimiters and no digit straight after the closing one, so a price such
# as "$5 and $10" is left alone.
_DISPLAY = re.compile(r"\$\$(.+?)\$\$", re.DOTALL)
_INLINE = re.compile(r"(?<![\\$])\$(?!\s)([^$\n]+?)(?<!\s)\$(?![\d$])")


def protect_math(text: str, where: str, fail) -> tuple[str, dict[str, str]]:
    """Swap each formula for a token Markdown will not touch.

    Markdown would read the underscores and asterisks inside LaTeX as
    emphasis, so the formulas are converted first and put back afterwards.
    """
    stash: dict[str, str] = {}

    def keep(latex: str, display: bool) -> str:
        try:
            mathml = latex2mathml.converter.convert(
                latex.strip(), display="block" if display else "inline")
        except Exception as exc:  # latex2mathml raises assorted errors
            fail(where, f"cannot render formula {latex.strip()!r}: {exc}")
            mathml = ""
        token = f"SQMATH{len(stash)}END"
        stash[token] = mathml
        return token

    text = _DISPLAY.sub(lambda m: "\n\n" + keep(m.group(1), True) + "\n\n", text)
    text = _INLINE.sub(lambda m: keep(m.group(1), False), text)
    return text, stash


def restore_math(rendered: str, stash: dict[str, str]) -> str:
    for token, mathml in stash.items():
        # A display formula sits alone in its paragraph; unwrap it so the
        # math block is not nested inside a <p>.
        rendered = rendered.replace(f"<p>{token}</p>", mathml)
        rendered = rendered.replace(token, mathml)
    return rendered


# ---------------------------------------------------------------------------
# Glossary links
# ---------------------------------------------------------------------------

_TAG = re.compile(r"(<[^>]+>)")
_SKIP = {"svg", "a", "h1", "h2", "h3", "h4", "h5", "h6", "code", "pre", "math",
         "script", "style", "button"}


def first_sentence(text: str, limit: int = 170) -> str:
    """Plain-text opening of a definition, for the link's tooltip."""
    plain = re.sub(r"[*_`]|\[([^\]]*)\]\([^)]*\)", lambda m: m.group(1) or "", text)
    plain = " ".join(plain.split())
    match = re.match(r"(.+?[.!?])(\s|$)", plain)
    out = match.group(1) if match else plain
    return out if len(out) <= limit else out[: limit - 1].rstrip() + "…"


def build_term_matcher(terms: list[dict]):
    """Return a function that links the first mention of each term in HTML."""
    by_name: dict[str, dict] = {}
    for term in terms:
        for name in [term["term"], *term["aka"]]:
            by_name[name.lower()] = term
    if not by_name:
        return lambda markup: markup

    names = sorted(by_name, key=len, reverse=True)
    pattern = re.compile(
        r"(?<![\w-])(" + "|".join(re.escape(n) for n in names) + r")(?:e?s)?(?![\w-])",
        re.IGNORECASE)

    def link(markup: str) -> str:
        seen: set[str] = set()
        skip = 0
        parts = []
        for piece in _TAG.split(markup):
            if piece.startswith("<"):
                tag = re.match(r"</?\s*([a-zA-Z0-9]+)", piece)
                if tag and tag.group(1).lower() in _SKIP and not piece.endswith("/>"):
                    skip += -1 if piece.startswith("</") else 1
                    skip = max(skip, 0)
                parts.append(piece)
                continue
            if skip:
                parts.append(piece)
                continue

            def swap(m: re.Match) -> str:
                term = by_name[m.group(1).lower()]
                if term["slug"] in seen:
                    return m.group(0)
                seen.add(term["slug"])
                return (f'<a class="term" href="/glossary/#{term["slug"]}" '
                        f'title="{html.escape(term["definition"], quote=True)}">'
                        f"{m.group(0)}</a>")

            parts.append(pattern.sub(swap, piece))
        return "".join(parts)

    return link


# ---------------------------------------------------------------------------
# Reading time
# ---------------------------------------------------------------------------

def reading_minutes(words: int, per_minute: int = 230) -> int:
    return max(1, math.ceil(words / per_minute))


# ---------------------------------------------------------------------------
# Link-preview image
# ---------------------------------------------------------------------------

OG_SIZE = (1200, 630)
_PAPER, _INK, _MUTED = "#f6f2e8", "#1f1c17", "#8a8173"
_RULE, _ACCENT = "#ddd5c6", "#8c3a22"
_SERIF = ROOT / "og" / "SourceSerif4-Variable.ttf"
_SANS = ROOT / "og" / "Inter-Variable.ttf"


def _font(path: Path, size: int, weight: int) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(str(path), size)
    font.set_variation_by_axes([weight])
    return font


def _wrap(draw: ImageDraw.ImageDraw, text: str, font, width: int) -> list[str]:
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if line and draw.textlength(trial, font=font) > width:
            lines.append(line)
            line = word
        else:
            line = trial
    if line:
        lines.append(line)
    return lines


def _tracked(draw, xy, text, font, fill, spacing: float) -> None:
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + spacing


def write_og_image(path: Path, title: str, eyebrow: str) -> None:
    img = Image.new("RGB", OG_SIZE, _PAPER)
    draw = ImageDraw.Draw(img)
    left, width = 84, OG_SIZE[0] - 168

    draw.rectangle([0, 0, OG_SIZE[0], 10], fill=_ACCENT)
    _tracked(draw, (left, 78), eyebrow.upper(), _font(_SANS, 22, 600), _ACCENT, 3.2)

    # Largest size at which the title fits in four lines.
    for size in range(76, 38, -2):
        font = _font(_SERIF, size, 480)
        lines = _wrap(draw, title, font, width)
        if len(lines) <= 4 and (len(lines) * size * 1.2) <= 340:
            break
    # Centre the title between the eyebrow and the rule, so a short title
    # does not leave the card top-heavy.
    block = len(lines) * int(size * 1.2)
    y = 130 + max(0, (390 - block) // 2)
    for line in lines:
        draw.text((left, y), line, font=font, fill=_INK)
        y += int(size * 1.2)

    draw.line([left, 530, left + width, 530], fill=_RULE, width=2)
    draw.text((left, 556), "Stark Quantum", font=_font(_SERIF, 34, 620), fill=_INK)
    tag = "Quantum, without the press release."
    tag_font = _font(_SANS, 22, 450)
    draw.text((left + width - draw.textlength(tag, font=tag_font), 566), tag,
              font=tag_font, fill=_MUTED)

    path.parent.mkdir(parents=True, exist_ok=True)
    img.save(path, optimize=True)


# ---------------------------------------------------------------------------
# Structured data, Markdown copies, llms.txt
# ---------------------------------------------------------------------------

def article_ld(site: dict, item: dict) -> dict:
    """schema.org Article for an essay or a brief."""
    url = site["base_url"] + item["url"]
    person = {"@type": "Person", "name": site["author"]}
    ld = {
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": item["title"],
        "url": url,
        "mainEntityOfPage": url,
        "image": site["base_url"] + item["og_image"],
        "datePublished": item["published"].isoformat(),
        "dateModified": (item.get("reviewed") or item["published"]).isoformat(),
        "inLanguage": "en",
        "isAccessibleForFree": True,
        "author": person,
        "publisher": person,
    }
    if item["kind"] in ("essay", "lesson"):
        ld["description"] = item["summary"]
        ld["articleSection"] = item["category_label"]
        if item["kind"] == "lesson":
            ld["learningResourceType"] = "lesson"
            ld["educationalLevel"] = item["level"]
        ld["timeRequired"] = f"PT{item['minutes']}M"
        cites = [{"@type": "CreativeWork", "name": s.get("name", ""), "url": s["url"]}
                 for s in item["sources"] if s.get("url")]
        if cites:
            ld["citation"] = cites
    else:
        ld["description"] = item["body_text"][:200]
        if item["source_url"]:
            ld["isBasedOn"] = {"@type": "CreativeWork", "name": item["source_name"],
                               "url": item["source_url"]}
    return ld


def markdown_copy(site: dict, item: dict) -> str:
    """The page as plain Markdown, for readers and tools that want no chrome."""
    url = site["base_url"] + item["url"]
    lines = [f"# {item['title']}", ""]
    by = f"By {site['author']}. Published {item['published'].isoformat()}."
    if item.get("reviewed"):
        by += f" Reviewed {item['reviewed'].isoformat()}."
    lines += [by, f"Canonical page: {url}", ""]
    if item["kind"] in ("essay", "lesson"):
        lines += [f"> {' '.join(item['summary'].split())}", ""]
    else:
        lines += [f"Source: [{item['source_name']}]({item['source_url']})", ""]
    lines += [item["body_text"], ""]
    if item["kind"] == "essay":
        f = item["footer"]
        lines += ["## The short version", "",
                  f"- **Claim:** {' '.join(str(f['claim']).split())}",
                  f"- **Evidence:** {' '.join(str(f['evidence']).split())}",
                  f"- **Missing piece:** {' '.join(str(f['missing_piece']).split())}",
                  f"- **So what:** {' '.join(str(f['so_what']).split())}", ""]
        if item["sources"]:
            lines += ["## Sources", ""]
            for s in item["sources"]:
                text = f"[{s['name']}]({s['url']})" if s.get("url") else s["name"]
                note = f" — {s['note']}" if s.get("note") else ""
                lines.append(f"- {text}{note}")
            lines.append("")
    elif item["kind"] == "lesson":
        lines += ["## Check yourself", ""]
        for n, c in enumerate(item["check"], 1):
            lines += [f"{n}. {c['q_text']}", f"   Answer: {c['a_text']}"]
        lines.append("")
        if item["sources"]:
            lines += ["## Sources", ""]
            for s in item["sources"]:
                text = f"[{s['name']}]({s['url']})" if s.get("url") else s["name"]
                note = f" \u2014 {s['note']}" if s.get("note") else ""
                lines.append(f"- {text}{note}")
            lines.append("")
    else:
        if item["numbers"]:
            lines += ["## Numbers", ""] + [f"- {n}" for n in item["numbers"]] + [""]
        if item["limits"]:
            lines += ["## Limits", ""] + [f"- {n}" for n in item["limits"]] + [""]
    return "\n".join(lines)


def llms_txt(site: dict, essays: list[dict], briefs: list[dict],
             lessons: list[dict]) -> str:
    """An index for language-model readers, in the llmstxt.org layout."""
    base = site["base_url"]
    out = [f"# {site['name']}", "", f"> {site['description']}", "",
           "Independent, unpaid writing by one person. Every essay ends with the "
           "claim, the evidence, the missing piece and why it matters, and cites "
           "primary sources. Each page below has a plain Markdown copy.", "",
           "## Learn (read in order)", ""]
    for l in lessons:
        out.append(f"- [{l['title']}]({base}{l['url']}index.md): "
                   f"{' '.join(l['summary'].split())}")
    out += ["", "## Essays", ""]
    for e in essays:
        out.append(f"- [{e['title']}]({base}{e['url']}index.md): "
                   f"{' '.join(e['summary'].split())}")
    out += ["", "## Briefs", ""]
    for b in briefs:
        out.append(f"- [{b['title']}]({base}{b['url']}index.md): {b['source_name']}")
    out += ["", "## Reference", "",
            f"- [Reality Board]({base}/reality/): four questions that decide whether the field has arrived",
            f"- [Glossary]({base}/glossary/): working definitions",
            f"- [Sources]({base}/sources/): the allowlist this site reads from",
            f"- [About]({base}/about/)", ""]
    return "\n".join(out)
