"""Figures drawn at build time as inline SVG.

Both figures take their colours from the site's CSS custom properties, so they
follow the light and dark themes with no script. Nothing here is fetched.

    surface_code_figure()    a distance-3 patch with one error and its syndrome
    threshold_view(data)     the simulated threshold chart and its summary
"""

from __future__ import annotations

import math

# ---------------------------------------------------------------------------
# Distance-3 rotated surface code
# ---------------------------------------------------------------------------

def _layout():
    """Data qubits, and the X and Z checks of the rotated distance-3 patch.

    Bulk faces alternate X and Z by (row + column) parity. The weight-two
    boundary checks are X on the top and bottom edges and Z on the left and
    right edges, which is the usual convention.
    """
    d = 3
    data = [(r, c) for r in range(d) for c in range(d)]
    checks = []
    for r in range(-1, d):
        for c in range(-1, d):
            kind = "X" if (r + c) % 2 == 0 else "Z"
            qubits = [(rr, cc) for rr in (r, r + 1) for cc in (c, c + 1)
                      if 0 <= rr < d and 0 <= cc < d]
            bulk = len(qubits) == 4
            top_bottom = (r in (-1, d - 1)) and len(qubits) == 2 and 0 <= c < d - 1
            side = (c in (-1, d - 1)) and len(qubits) == 2 and 0 <= r < d - 1
            if bulk or (top_bottom and kind == "X") or (side and kind == "Z"):
                checks.append({"kind": kind, "qubits": qubits, "r": r, "c": c})
    # The layout is only worth drawing if it is a valid code.
    xs = [set(k["qubits"]) for k in checks if k["kind"] == "X"]
    zs = [set(k["qubits"]) for k in checks if k["kind"] == "Z"]
    assert len(xs) == 4 and len(zs) == 4, "distance 3 needs four X and four Z checks"
    assert all(len(a & b) % 2 == 0 for a in xs for b in zs), "X and Z checks must commute"
    return data, checks


def surface_code_figure() -> str:
    data, checks = _layout()
    x0, y0, step = 90, 70, 70

    def pos(r, c):
        return x0 + step * c, y0 + step * r

    error = (1, 1)
    # An X error on a data qubit flips the Z checks that contain it.
    flagged = [k for k in checks if k["kind"] == "Z" and error in k["qubits"]]

    parts, labels = [], []
    for k in checks:
        lit = k in flagged
        cls = f"sc-{k['kind'].lower()}" + (" sc-lit" if lit else "")
        pts = [pos(r, c) for r, c in k["qubits"]]
        if len(pts) == 4:
            (ax, ay), (bx, by), (cx, cy), (dx, dy) = pts
            path = f"M{ax} {ay} L{bx} {by} L{dx} {dy} L{cx} {cy} Z"
            label = ((ax + dx) / 2, (ay + dy) / 2)
        else:
            (ax, ay), (bx, by) = pts
            half = step / 2
            # A bump on the outside edge of the patch.
            if k["r"] == -1:
                nx, ny = 0, -1
            elif k["r"] == 2:
                nx, ny = 0, 1
            elif k["c"] == -1:
                nx, ny = -1, 0
            else:
                nx, ny = 1, 0
            lift = half * 1.33
            path = (f"M{ax} {ay} L{bx} {by} "
                    f"C{bx + nx * lift:.1f} {by + ny * lift:.1f} "
                    f"{ax + nx * lift:.1f} {ay + ny * lift:.1f} {ax} {ay} Z")
            label = ((ax + bx) / 2 + nx * half * 0.5, (ay + by) / 2 + ny * half * 0.5)
        parts.append(f'<path class="{cls}" d="{path}"/>')
        labels.append(f'<text class="sc-label" x="{label[0]:.0f}" y="{label[1] + 5:.0f}" '
                      f'text-anchor="middle">{k["kind"]}</text>')

    for r, c in data:
        x, y = pos(r, c)
        cls = "sc-data sc-err" if (r, c) == error else "sc-data"
        parts.append(f'<circle class="{cls}" cx="{x}" cy="{y}" r="9"/>')

    ex, ey = pos(*error)
    parts.append(f'<text class="sc-note" x="{ex}" y="{ey - 15}" text-anchor="middle">X error</text>')

    desc = ("A three-by-three grid of data qubits with eight check regions. "
            "One data qubit in the centre has an X error. The two Z checks that "
            "contain it are highlighted: they are the syndrome.")
    return (
        '<figure class="figure">'
        '<svg class="sc-figure" viewBox="45 25 230 230" role="img" '
        'aria-labelledby="sc-t sc-d" xmlns="http://www.w3.org/2000/svg">'
        '<title id="sc-t">A distance-3 surface code patch with one error</title>'
        f'<desc id="sc-d">{desc}</desc>'
        + "".join(parts) + "".join(labels) +
        '</svg>'
        '<figcaption>A distance-3 patch: nine data qubits (circles) and eight '
        'checks. X checks and Z checks are labelled. The central qubit has an '
        'X error, which flips the two Z checks beside it, shown shaded. Those '
        'two flipped checks are the syndrome; the decoder works backwards from '
        'them to the qubit.</figcaption></figure>'
    )


# ---------------------------------------------------------------------------
# Threshold chart
# ---------------------------------------------------------------------------

MIN_ERRORS = 20  # a point with fewer observed failures is too noisy to plot
SUP = str.maketrans("0123456789-", "⁰¹²³⁴⁵⁶⁷⁸⁹⁻")


def _pct(p: float) -> str:
    return f"{p * 100:g}%"


def _crossing(points, d_small: int, d_large: int):
    """Physical error rate at which two distances fail equally often."""
    a = {p["p"]: p["shot"] for p in points if p["d"] == d_small}
    b = {p["p"]: p["shot"] for p in points if p["d"] == d_large}
    rates = sorted(set(a) & set(b))
    gap = [(r, math.log(b[r]) - math.log(a[r])) for r in rates if a[r] > 0 and b[r] > 0]
    for (r1, g1), (r2, g2) in zip(gap, gap[1:]):
        if g1 < 0 <= g2:
            t = -g1 / (g2 - g1)
            return math.exp(math.log(r1) + t * (math.log(r2) - math.log(r1)))
    return None


def threshold_view(data: dict) -> dict:
    # The chart plots the failure probability of a whole d-round experiment,
    # the standard way to find a threshold: every distance runs d rounds, and
    # the curves cross where a bigger code stops helping. The table gives the
    # per-round rate, which is the number the overhead calculator uses.
    points = [dict(p, shot=p["errors"] / p["shots"]) for p in data["points"]]
    kept = [p for p in points if p["errors"] >= MIN_ERRORS and p["shot"] > 0]
    distances = sorted({p["d"] for p in kept})
    lo = min(p["shot"] for p in kept)
    hi = max(p["shot"] for p in kept)
    y_lo, y_hi = math.floor(math.log10(lo)), math.ceil(math.log10(hi))
    xmin, xmax = math.log10(0.0009), math.log10(0.0135)

    w, h, ml, mr, mt, mb = 720, 430, 74, 24, 24, 58
    pw, ph = w - ml - mr, h - mt - mb

    def sx(p):
        return ml + (math.log10(p) - xmin) / (xmax - xmin) * pw

    def sy(v):
        return mt + (y_hi - math.log10(v)) / (y_hi - y_lo) * ph

    out = []
    for k in range(y_lo, y_hi + 1):
        y = mt + (y_hi - k) / (y_hi - y_lo) * ph
        out.append(f'<line class="ch-grid" x1="{ml}" x2="{ml + pw}" y1="{y:.1f}" y2="{y:.1f}"/>')
        out.append(f'<text class="ch-tick" x="{ml - 8}" y="{y + 4:.1f}" text-anchor="end">10{str(k).translate(SUP)}</text>')
    for p in (0.001, 0.002, 0.005, 0.01):
        x = sx(p)
        out.append(f'<line class="ch-grid" x1="{x:.1f}" x2="{x:.1f}" y1="{mt}" y2="{mt + ph}"/>')
        out.append(f'<text class="ch-tick" x="{x:.1f}" y="{mt + ph + 20}" text-anchor="middle">{_pct(p)}</text>')
    out.append(f'<line class="ch-axis" x1="{ml}" x2="{ml + pw}" y1="{mt + ph}" y2="{mt + ph}"/>')
    out.append(f'<line class="ch-axis" x1="{ml}" x2="{ml}" y1="{mt}" y2="{mt + ph}"/>')
    out.append(f'<text class="ch-title" x="{ml + pw / 2}" y="{h - 12}" text-anchor="middle">Physical error rate per operation</text>')
    out.append(f'<text class="ch-title" transform="translate(16 {mt + ph / 2}) rotate(-90)" text-anchor="middle">Chance the logical qubit fails during a d-round experiment</text>')

    cross = _crossing(kept, distances[1] if len(distances) > 1 else distances[0], distances[-1])
    if cross:
        x = sx(cross)
        out.append(f'<line class="ch-cross" x1="{x:.1f}" x2="{x:.1f}" y1="{mt}" y2="{mt + ph}"/>')

    shapes = ["circle", "square", "triangle", "diamond"]

    def marker(shape, x, y, cls):
        s = 4.5
        if shape == "circle":
            return f'<circle class="{cls}" cx="{x:.1f}" cy="{y:.1f}" r="{s}"/>'
        if shape == "square":
            return f'<rect class="{cls}" x="{x - s:.1f}" y="{y - s:.1f}" width="{2 * s}" height="{2 * s}"/>'
        if shape == "triangle":
            return f'<path class="{cls}" d="M{x:.1f} {y - s - 1:.1f} L{x + s + 1:.1f} {y + s:.1f} L{x - s - 1:.1f} {y + s:.1f} Z"/>'
        return f'<path class="{cls}" d="M{x:.1f} {y - s - 1:.1f} L{x + s + 1:.1f} {y:.1f} L{x:.1f} {y + s + 1:.1f} L{x - s - 1:.1f} {y:.1f} Z"/>'

    for i, d in enumerate(distances):
        pts = sorted((p for p in kept if p["d"] == d), key=lambda q: q["p"])
        line = " ".join(f"{sx(p['p']):.1f},{sy(p['shot']):.1f}" for p in pts)
        out.append(f'<polyline class="ch-line ch-d{i}" points="{line}"/>')
        for p in pts:
            out.append(marker(shapes[i % 4], sx(p["p"]), sy(p["shot"]), f"ch-pt ch-d{i}"))
        ly = mt + 14 + i * 20
        out.append(f'<line class="ch-line ch-d{i}" x1="{ml + 14}" x2="{ml + 38}" y1="{ly}" y2="{ly}"/>')
        out.append(marker(shapes[i % 4], ml + 26, ly, f"ch-pt ch-d{i}"))
        out.append(f'<text class="ch-tick" x="{ml + 46}" y="{ly + 4}">distance {d}</text>')

    svg = (
        f'<svg class="chart" viewBox="0 0 {w} {h}" role="img" aria-labelledby="ch-t ch-d" '
        'xmlns="http://www.w3.org/2000/svg">'
        '<title id="ch-t">Simulated logical failure probability against physical error rate</title>'
        '<desc id="ch-d">Lines for several surface-code distances on logarithmic axes. '
        'Below about one percent per operation, larger distance gives a lower logical '
        'error rate; above it, larger distance gives a higher one. The lines cross near '
        'the threshold. The same numbers are in the table below.</desc>'
        + "".join(out) + "</svg>"
    )

    # Table at three physical error rates, for readers who cannot use the chart.
    table_rates = [r for r in (0.002, 0.004, 0.006, 0.008) if r in data["rates"]]
    lookup = {(p["d"], p["p"]): p for p in points}
    rows = []
    for d in distances:
        cells = []
        for r in table_rates:
            pt = lookup.get((d, r))
            if pt and pt["errors"] >= MIN_ERRORS:
                m, e = f"{pt['per_round']:.1e}".split("e")
                cells.append(f"{m} × 10{str(int(e)).translate(SUP)}")
            else:
                cells.append("too few failures")
        rows.append({"d": d, "cells": cells})

    return {
        "svg": svg,
        "distances": distances,
        "table_rates": [_pct(r) for r in table_rates],
        "rows": rows,
        "crossing": _pct(round(cross, 4)) if cross else None,
        "crossing_pair": (distances[1] if len(distances) > 1 else distances[0], distances[-1]),
        "points": len(kept),
        "dropped": len(points) - len(kept),
        "shots": sum(p["shots"] for p in data["points"]),
        "min_errors": MIN_ERRORS,
    }
