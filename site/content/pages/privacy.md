---
title: Privacy / Datenschutzerklärung
summary: What this site stores about you, which is almost nothing, and the rights you have over it.
updated: 2026-09-19
---

Stark Quantum is a static site. Every page is a file generated ahead of time
and served as it is. This page describes only what the site actually does; it
does not list practices that do not apply here.

Last updated: 19 September 2026.

## Controller

The controller within the meaning of Article 4 (7) GDPR is:

<p class="address">
Christian Stark<br>
Maxstr. 14<br>
52070 Aachen<br>
Germany
</p>

Email: <!--email_off-->[info@starkquantum.com](mailto:info@starkquantum.com)<!--/email_off-->

The controller is a private individual operating a non-commercial
publication. No goods or services are sold, no advertising is run, and no
revenue is generated, so there is no payment processing, no customer data, no
marketing, and no advertising or commercial profiling anywhere on this site.

No data protection officer has been appointed, because the site does not meet
the thresholds in Article 37 GDPR or section 38 BDSG.

## Purpose of processing

The site exists to publish and deliver a static editorial archive: essays,
short source-tied briefs, a glossary, and the Reality Board. Personal data is
processed only to the extent that delivering those pages, counting visits in
aggregate, and answering email require it.

## What is not here

There is no Google Analytics, and nothing on this site follows you across
other websites. There are no advertising pixels, no third-party embeds, no
social widgets, no comment system, and no newsletter. Visits are counted in
aggregate by a self-hosted tool, described under *Visitor statistics* below.

**No cookies are set by this site**, including by that statistics tool.

Fonts, stylesheets, and images all come from this site. The one script loaded
from another hostname is the statistics script, and that hostname is operated
by the controller as well.

There is no user account, no login, and no payment processing. Personal data
is never sold, and it is not used for advertising or profiling.

## Storage on your device

One value, and only if you use it.

If you change the theme with the control in the header, the site writes your
choice to `localStorage` under the key `sq-theme`. This is stored in your
browser, never transmitted to the server, and never read by anyone else. It
exists so the page does not change appearance as you navigate.

Setting the theme back to automatic deletes the value. Clearing your browser's
site data also removes it.

This is storage strictly necessary to provide a function you explicitly
requested, so it is permitted under section 25 (2) no. 2 TDDDG without
consent. To the extent any personal data is involved, the legal basis is
Article 6 (1) (f) GDPR — the legitimate interest in presenting the site as the
reader configured it.

Nothing else is written to your device. No other `localStorage` key, no
`sessionStorage`, no IndexedDB, no cookie.

## Visitor statistics

Visits are counted with Umami, an open-source statistics tool that the
controller runs on the controller's own server. Every page loads its script
from `umami.homomorphicprivacy.com`, a hostname the controller operates. No
outside analytics company is involved.

For each page view the script sends the address of the page, the referring
page if your browser supplies one, your browser, operating system and device
type, screen size, and browser language. The server derives an approximate
location from your IP address; the IP address itself is not stored. To tell
one visit from another without cookies, Umami computes an identifier from
technical data such as the IP address and the browser, combined with a value
that changes periodically. That identifier cannot be used to recognise you on
other websites.

The script sets no cookies and writes nothing to your device. It reads one
value from your browser's local storage, `umami.disabled`, which exists only
if you have switched the counting off yourself.

The figures are used in aggregate only, to see which pages are read and how
readers arrive. They are not combined with other data, not used to build
profiles, not used for advertising, and not shared with anyone. The legal
basis is Article 6 (1) (f) GDPR: the legitimate interest in understanding, in
aggregate, how the site is used. Like everything else here, the script is
delivered through Cloudflare, described below.

You may object at any time under Article 21 GDPR by writing to
<!--email_off-->[info@starkquantum.com](mailto:info@starkquantum.com)<!--/email_off-->.
Blocking the script with a browser extension also works; the site behaves
exactly the same without it.

## Server log files

The web server that delivers this site records ordinary access data: the
requesting IP address, the date and time, the requested path, the HTTP status
code, the amount of data transferred, the referrer if the browser sends one,
and the user agent string.

This is technically required to deliver the site and to identify faults and
abuse. The legal basis is Article 6 (1) (f) GDPR; the legitimate interest is
operating the site securely and reliably. Logs are not combined with other
data, not used to build profiles, and not used to identify individual readers.
They are kept only as long as needed for that purpose and are then overwritten
or deleted.

## Delivery through Cloudflare

The site is delivered through Cloudflare as a content delivery network and
reverse proxy, which is what makes it reachable and protects it against
attack. Requests therefore pass through Cloudflare's infrastructure, and
Cloudflare processes connection data — including your IP address — on the
controller's behalf as a category of recipient.

Legal basis: Article 6 (1) (f) GDPR, the legitimate interest in secure and
reliable delivery. Where data is transferred outside the EU or EEA, the
transfer is based on the European Commission's standard contractual clauses.

Cloudflare's own privacy information is published at
[cloudflare.com/privacypolicy](https://www.cloudflare.com/privacypolicy/).

## The archive search

The search in the header runs entirely in your browser. It fetches one file
from this site, `/search-index.json`, containing the titles and summaries of
everything published here, and searches that file locally. **Your query is
never transmitted** and is not logged, because it never leaves your device.

## Email

If you write to <!--email_off-->[info@starkquantum.com](mailto:info@starkquantum.com)<!--/email_off-->, your
message, your address, and anything else you choose to include are processed
in order to read and answer it. The legal basis is Article 6 (1) (b) GDPR
where the message concerns a possible or existing agreement, and otherwise
Article 6 (1) (f) GDPR, the legitimate interest in answering correspondence.

Messages are kept only as long as needed to deal with the matter and are then
deleted, unless a statutory retention period requires otherwise. Your address
is not added to any mailing list, because there is no mailing list.

## Links to other sites

Briefs and essays link to primary sources: preprints, code repositories, and
technical pages published by laboratories and companies. Following such a link
means visiting a third party's server under that party's own terms and privacy
practices, over which this site has no control and for which it accepts no
responsibility.

## No automated decision-making

There is no automated decision-making in the sense of Article 22 GDPR and no
profiling. Nothing on this site evaluates you or reaches a decision about you.

## Your rights

Under the GDPR you have the right to:

- **access** the personal data held about you (Article 15);
- **rectification** of inaccurate data (Article 16);
- **erasure** (Article 17);
- **restriction** of processing (Article 18);
- **data portability** (Article 20);
- **object** to processing based on legitimate interests, on grounds relating
  to your particular situation (Article 21).

To exercise any of these, write to
<!--email_off-->[info@starkquantum.com](mailto:info@starkquantum.com)<!--/email_off-->.

Where processing relies on consent, you may withdraw that consent at any time
with effect for the future, without affecting the lawfulness of processing
carried out beforehand.

## Right to complain to a supervisory authority

You have the right to lodge a complaint with a data protection supervisory
authority under Article 77 GDPR. The authority responsible for this controller
is:

Landesbeauftragte für Datenschutz und Informationsfreiheit Nordrhein-Westfalen
(LDI NRW) — [www.ldi.nrw.de](https://www.ldi.nrw.de/)

You may also complain to the supervisory authority where you live or work.

## Changes to this notice

If what the site does changes, this page changes with it, and the date at the
top is updated.
