#!/usr/bin/env python3
"""Simulate the surface-code threshold and write data/threshold.json.

Run by hand, not by the site build. The result is committed, so the published
chart can be rebuilt without simulating and the numbers can be rerun by anyone.

    pip install stim sinter pymatching
    python tools/threshold_sim.py            # full run, a few minutes
    python tools/threshold_sim.py --quick    # coarse run, for a smoke test

Model: rotated surface code, memory experiment (Z basis), d rounds, uniform
circuit-level depolarizing noise at rate p on gates, resets, measurements and
idle data qubits, minimum-weight perfect-matching decoder. This is the standard
noise model for such plots. It is not a model of any particular device.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path

import pymatching
import sinter
import stim

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "threshold.json"

DISTANCES = [3, 5, 7, 9]
RATES = [0.001, 0.002, 0.003, 0.004, 0.005, 0.006, 0.007, 0.008, 0.009, 0.010,
         0.011, 0.012]


def task(d: int, p: float) -> sinter.Task:
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=d,
        rounds=d,
        after_clifford_depolarization=p,
        after_reset_flip_probability=p,
        before_measure_flip_probability=p,
        before_round_data_depolarization=p,
    )
    return sinter.Task(circuit=circuit, json_metadata={"d": d, "p": p})


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--quick", action="store_true")
    parser.add_argument("--workers", type=int, default=12)
    args = parser.parse_args()

    shots, errors = (20_000, 50) if args.quick else (2_000_000, 400)
    stats = sinter.collect(
        num_workers=args.workers,
        tasks=[task(d, p) for d in DISTANCES for p in RATES],
        decoders=["pymatching"],
        max_shots=shots,
        max_errors=errors,
        print_progress=False,
    )

    points = []
    for s in stats:
        d, p = s.json_metadata["d"], s.json_metadata["p"]
        shot_rate = s.errors / s.shots
        # A memory experiment of d rounds fails if the logical flips an odd
        # number of times, so the per-round flip rate r satisfies
        # 1 - 2 * shot_rate = (1 - 2 r) ** d.
        base = max(1 - 2 * shot_rate, 0.0)
        per_round = (1 - base ** (1 / d)) / 2
        points.append({"d": d, "p": p, "shots": s.shots, "errors": s.errors,
                       "per_round": per_round})
    points.sort(key=lambda x: (x["d"], x["p"]))

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({
        "generated": dt.date.today().isoformat(),
        "versions": {"stim": stim.__version__, "sinter": sinter.__version__,
                     "pymatching": pymatching.__version__},
        "model": "rotated surface code, memory Z, d rounds, uniform circuit-level "
                 "depolarizing noise, minimum-weight perfect matching",
        "distances": DISTANCES, "rates": RATES, "points": points,
    }, indent=1) + "\n", encoding="utf-8")
    print(f"wrote {OUT} with {len(points)} points")


if __name__ == "__main__":
    main()
