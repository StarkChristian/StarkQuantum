#!/usr/bin/env python3
"""Freshness agent: find what the world may have changed under the site.

It reads the site's own sources and claims, checks them against the outside, and
writes a report for a person. It never edits content, never publishes, never
touches the Reality Board. A page changes only when a human reads the report,
decides, and commits.

    python tools/freshness.py                  write a report, print where
    python tools/freshness.py --offline        local checks only (ages)
    python tools/freshness.py --no-watch       skip the arXiv watch queries
    python tools/freshness.py --monthly        wider watch, a table of every claim,
                                               and a trial build of the site

State (what was seen last time) is kept outside the repository, in
~/work/sq-freshness/, so a run does not dirty the working tree.

What it checks
    1. every arXiv paper cited on the site: a newer version, a journal reference
       or DOI that was not there before, a changed title, a withdrawal notice;
    2. every other cited link: does it still answer;
    3. the watch queries in data/watch.yml: new papers since the last run;
    4. age: claims, lessons and Reality Board cells not reviewed for too long.

Text from the outside is treated as data. It is quoted in the report as a title
and a link and is never followed as an instruction.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
STATE_DIR = Path.home() / "work" / "sq-freshness"
STATE = STATE_DIR / "state.json"
UA = "StarkQuantum-freshness/1.0 (+https://www.starkquantum.com/colophon/)"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
ARXIV_ID = re.compile(r"arxiv\.org/abs/([A-Za-z.\-]+/\d{7}|\d{4}\.\d{4,5})(v\d+)?")
today = dt.date.today()


def get(url: str, timeout: int = 25) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.read()
    except urllib.error.HTTPError as exc:
        return exc.code, b""
    except (urllib.error.URLError, TimeoutError, OSError):
        return 0, b""


def arxiv_api(params: dict) -> list[dict]:
    time.sleep(3.2)  # the API asks for at most one request every three seconds
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    status, body = get(url)
    if status != 200:
        return []
    out = []
    for entry in ET.fromstring(body).findall(ATOM + "entry"):
        raw = entry.findtext(ATOM + "id", "")
        m = re.search(r"abs/(.+?)(v\d+)?$", raw)
        if not m:
            continue
        out.append({
            "id": m.group(1),
            "version": int(m.group(2)[1:]) if m.group(2) else 1,
            "title": " ".join(entry.findtext(ATOM + "title", "").split()),
            "authors": [a.findtext(ATOM + "name", "") for a in entry.findall(ATOM + "author")],
            "updated": entry.findtext(ATOM + "updated", "")[:10],
            "published": entry.findtext(ATOM + "published", "")[:10],
            "journal": " ".join(entry.findtext(ARXIV + "journal_ref", "").split()),
            "doi": entry.findtext(ARXIV + "doi", ""),
            "comment": " ".join(entry.findtext(ARXIV + "comment", "").split()),
        })
    return out


def load_state() -> dict:
    try:
        return json.loads(STATE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {"papers": {}, "seen": {}, "first_run": True}


def collect_citations() -> dict[str, list[str]]:
    """url -> the pages or files that cite it."""
    cites: dict[str, list[str]] = {}

    def add(url, where):
        if url and str(url).startswith("http"):
            cites.setdefault(str(url), [])
            if where not in cites[str(url)]:
                cites[str(url)].append(where)

    claims = yaml.safe_load((ROOT / "data" / "claims.yml").read_text(encoding="utf-8"))
    for c in claims["claims"]:
        add(c.get("url"), "/claims/ (" + ", ".join(c["where"]) + ")")
    for folder in ("learn", "essays"):
        for path in sorted((ROOT / "content" / folder).glob("*.md")):
            raw = path.read_text(encoding="utf-8")
            front = yaml.safe_load(raw.split("---", 2)[1]) or {}
            for s in front.get("sources") or []:
                add(s.get("url"), f"content/{folder}/{path.name}")
    return cites


def check_citations(cites: dict, state: dict, offline: bool) -> list[str]:
    notes: list[str] = []
    if offline:
        return notes
    ids = {}
    others = []
    for url, where in cites.items():
        m = ARXIV_ID.search(url)
        if m:
            ids[m.group(1)] = where
        else:
            others.append(url)
    papers = {}
    batch = list(ids)
    for i in range(0, len(batch), 20):
        for p in arxiv_api({"id_list": ",".join(batch[i:i + 20]), "max_results": 20}):
            papers[p["id"]] = p
    for pid, where in sorted(ids.items()):
        p = papers.get(pid)
        if not p:
            notes.append(f"- **{pid}**: not returned by the arXiv API (cited in {', '.join(where)}). Check the link.")
            continue
        old = state["papers"].get(pid)
        if old and not state.get("first_run"):
            if p["version"] > old["version"]:
                notes.append(f"- **arXiv:{pid}** is now version {p['version']} (was {old['version']}), updated {p['updated']}: {p['title']}. Cited in {', '.join(where)}. Re-read the abstract.")
            if p["journal"] and not old.get("journal"):
                notes.append(f"- **arXiv:{pid}** now has a journal reference ({p['journal']}). Consider citing the published version. Cited in {', '.join(where)}.")
            if p["title"] != old["title"]:
                notes.append(f"- **arXiv:{pid}** changed its title to \"{p['title']}\". Cited in {', '.join(where)}.")
        if re.search(r"withdrawn", p["comment"], re.I):
            notes.append(f"- **arXiv:{pid}** carries a withdrawal note in its comment: \"{p['comment']}\". Cited in {', '.join(where)}.")
        state["papers"][pid] = {"version": p["version"], "title": p["title"], "journal": p["journal"]}
    for url in others:
        status, _ = get(url, timeout=20)
        if status == 0 or status >= 500:      # a hiccup is not a finding: ask twice
            time.sleep(4)
            status, _ = get(url, timeout=20)
        if status in (401, 403, 429, 999):
            notes.append(f"- {url} refused an automated request ({status}); open it by hand (cited in {', '.join(cites[url])}).")
        elif status == 0 or status >= 400:
            notes.append(f"- {url} answered {status or 'nothing'} twice (cited in {', '.join(cites[url])}).")
        time.sleep(0.5)
    return notes


def watch(state: dict, cfg: dict) -> list[str]:
    out: list[str] = []
    for q in cfg["queries"]:
        found = arxiv_api({"search_query": q["query"], "sortBy": "submittedDate",
                           "sortOrder": "descending", "max_results": cfg["limits"]["max_per_query"]})
        seen = set(state["seen"].get(q["id"], []))
        new = [p for p in found if p["id"] not in seen]
        state["seen"][q["id"]] = sorted(seen | {p["id"] for p in found})
        if state.get("first_run"):
            continue  # the first run only learns what already exists
        if new:
            out.append(f"### {q['id']}: {q['why']}\nMay affect: {', '.join(q['affects'])}\n")
            for p in new:
                authors = ", ".join(p["authors"][:3]) + (" et al." if len(p["authors"]) > 3 else "")
                out.append(f"- [{p['title']}](https://arxiv.org/abs/{p['id']}) ({authors}, {p['published']})")
            out.append("")
    return out


def ages(cfg: dict) -> list[str]:
    notes = []
    lim = cfg["limits"]
    claims = yaml.safe_load((ROOT / "data" / "claims.yml").read_text(encoding="utf-8"))
    checked = claims["checked_on"]
    age = (today - checked).days
    if age > lim["claim_stale_days"]:
        notes.append(f"- The claims register was last checked on {checked} ({age} days ago). Limit is {lim['claim_stale_days']}.")
    for path in sorted((ROOT / "content" / "learn").glob("*.md")):
        front = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
        reviewed = front.get("reviewed")
        if reviewed and (today - reviewed).days > lim["lesson_stale_days"]:
            notes.append(f"- Lesson \"{front['title']}\" was last reviewed on {reviewed} ({(today - reviewed).days} days ago).")
    for path in sorted((ROOT / "content" / "reality").glob("*.md")):
        front = yaml.safe_load(path.read_text(encoding="utf-8").split("---", 2)[1])
        reviewed = front.get("reviewed")
        if reviewed and (today - reviewed).days > lim["reality_stale_days"]:
            notes.append(f"- Reality Board cell \"{front['question']}\" was last reviewed on {reviewed} ({(today - reviewed).days} days ago). The doctrine asks for a review date a reader can trust.")
    return notes


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    ap.add_argument("--no-watch", action="store_true")
    ap.add_argument("--monthly", action="store_true")
    args = ap.parse_args()

    cfg = yaml.safe_load((ROOT / "data" / "watch.yml").read_text(encoding="utf-8"))
    if args.monthly:
        cfg["limits"]["max_per_query"] = 25
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    first = state.get("first_run", True)

    cites = collect_citations()
    cite_notes = check_citations(cites, state, args.offline)
    watch_lines = [] if (args.offline or args.no_watch) else watch(state, cfg)
    age_notes = ages(cfg)

    state["first_run"] = False
    STATE.write_text(json.dumps(state, indent=1), encoding="utf-8")

    lines = [f"# Freshness report, {today.isoformat()}", ""]
    if first:
        lines += ["This was the first run. It recorded the current versions of "
                  f"{len(state['papers'])} cited papers and the papers that already match each watch query, "
                  "so later runs can report what changed. Only age and link checks are reported below.", ""]
    lines += ["## Cited sources that changed or stopped answering", ""]
    lines += cite_notes or ["Nothing."]
    lines += ["", "## New papers matching the watch queries", ""]
    lines += watch_lines or ["Nothing new."]
    lines += ["", "## Reviews that are overdue", ""]
    lines += age_notes or ["Nothing overdue."]
    if args.monthly:
        lines += ["", "## Every claim on the register", ""]
        claims = yaml.safe_load((ROOT / "data" / "claims.yml").read_text(encoding="utf-8"))
        for c in claims["claims"]:
            lines.append(f"- [{c['status']}] {c['claim'][:110]} ({', '.join(c['where'])})")
        lines += ["", "## Trial build", ""]
        try:
            res = subprocess.run([sys.executable, "build.py"], cwd=ROOT, capture_output=True,
                                 text=True, timeout=600)
            tail = (res.stdout + res.stderr).strip().splitlines()[-6:]
            lines += [("The site builds." if res.returncode == 0 else "**The build was refused or failed.**")] + [f"    {t}" for t in tail]
        except (OSError, subprocess.TimeoutExpired) as exc:
            lines += [f"The trial build could not run: {exc}"]
    lines += ["", "## What to do with this", "",
              "A person reads it. Nothing here has been changed on the site. If a paper or a "
              "changed source alters a statement, edit the page on a branch, update the claim in "
              "`data/claims.yml` and its `checked_on` date, and publish through the usual preview.", ""]
    report = "\n".join(lines)
    kind = "monthly" if args.monthly else "weekly"
    out = STATE_DIR / f"report-{today.isoformat()}-{kind}.md"
    out.write_text(report, encoding="utf-8")
    latest = STATE_DIR / "latest.md"
    latest.write_text(report, encoding="utf-8")
    print(report)
    print(f"\nWritten to {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
