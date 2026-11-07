---
title: Methodology
summary: How Stark Quantum chooses what to read, how claims are checked, how the Reality Board changes, and what none of this guarantees.
updated: 2026-11-07
---

This page describes how the site is made, so that a reader can judge how far to
trust it. It describes what is done, not what is hoped for. Where the method has
a gap, the gap is listed at the end.

## What is read

Everything begins at a primary source: a preprint, a journal paper, a
laboratory's own technical page, or the repository of a software tool. The
complete list is on the [Sources](/sources/) page, together with the kinds of
source that are refused: news wires, press releases, stock coverage and funding
announcements. A result that reaches the site only through a news article is not
published, however widely it is reported.

Being on the list is not enough. A result is considered only if it carries a new
number or an inspectable result, is tied to hardware or to error, and comes from
the primary source rather than a description of it.

## How a brief is made

A script collects candidates from the listed sources and sorts them with a fixed
set of rules. It does not write the brief. A person reads the paper, writes the
text, and approves it before it is published.

A brief gives the number, the conditions under which it was obtained, and the
limits stated by the authors. After publication a brief is frozen. If it turns
out to be wrong, the correction appears as a dated note at the top of the brief
and the original text stays where it is.

## How essays and lessons are made

Essays are longer arguments and carry the same four-part ending: the claim, the
evidence, the missing piece, and why it matters. Lessons are short, ordered
introductions to one idea each, and end with self-check questions whose answers
sit behind a click. Nothing in them is scored or stored.

Every lesson lists its sources. A number is traced to the paper it comes from,
and the paper is read for that number, not remembered. Where a figure comes from
the company that built the device, the page says so.

The [Claims register](/claims/) lists each factual or numerical claim on the
Learn and tool pages, the page that uses it, its source, and one of four
statuses: checked, vendor-reported, derived here, or standard result. A claim
marked checked means the source says what the page says. It does not mean the
source is right.

Foundation essays are living pages. They show the date they were last reviewed
separately from the date they were first published, and where those differ, the
reviewed date is the one to trust. Each essay and lesson has a revision history
at the bottom of the page.

## How the Reality Board changes

The board has four questions and only four. Each has a status, the conditions
that would change it, and a dated log of every change. The default is "Not yet".

A cell changes only when a person has compared the evidence with the written
conditions and decided that they are met. Software may point to a paper that
could matter. It cannot change a cell. When a review leaves the answer as it
was, that is recorded too, with the reason.

The date shown on a cell is the date of its last review. Funding, headcount,
partnerships and the timing of any cryptographic threat are not on the board.

## What is automated

Two scheduled jobs run on the author's server, one every week and a longer one
every month. They check whether the pages cited on the site still answer, list
new preprints that match a fixed set of search terms, and list pages whose review
date has grown old. They write a report for the author. They change nothing on
the site.

The pages themselves are generated from Markdown files when the site is built.
The build refuses to publish a page with a broken internal link and refuses a
page that is too heavy to load quickly. See [how this site is built](/colophon/).

## What happens when something is wrong

Every substantive change after publication is recorded on
[Corrections and changes](/corrections/), with its date and the reason. Reports
of errors are the most useful thing a reader can send; the address is in the
footer.

## What this method does not give you

- **One person.** The site is written, checked and approved by one author. No
  outside expert reviews a page before it is published, and the claims register
  records what the author checked, not what anyone else confirmed.
- **Preprints.** Most sources are preprints, which have not been peer reviewed.
  A preprint can be revised or withdrawn after it is cited.
- **Currency.** A page that was accurate when written may not describe the field
  today. Check its dates and the primary source.
- **Selection.** The site covers hardware, error and evidence, and leaves out
  quantum sensing, networking and cryptography timelines unless a hardware result
  moves them. Absence from the site is not a judgement on anything left out.
