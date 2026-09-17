#!/usr/bin/env python3
"""Independent finite audit of the closed-form reverse-pair frontier in Paper 14.

For each k >= 5, compares every exact reverse-BFS layer used by the symbolic
lower-bound lemma with the manuscript template, then checks that q0 first enters
at the next layer. Standard library only.
"""
import argparse
import csv
from pathlib import Path

from completion_model import reverse_layers_from_collision_pairs, template_layers


def run_one(k):
    if k < 5:
        raise ValueError("the symbolic layer template is stated for k >= 5")
    last_template_depth = 4 * k + 6
    exact = reverse_layers_from_collision_pairs(k, last_template_depth + 1)
    templ = template_layers(k)

    for depth in range(last_template_depth + 1):
        if exact[depth] != templ[depth]:
            missing = sorted(templ[depth] - exact[depth])
            extra = sorted(exact[depth] - templ[depth])
            raise AssertionError((k, depth, "missing", missing, "extra", extra))
        if any(0 in pair for pair in exact[depth]):
            raise AssertionError((k, depth, "q0 entered too early"))

    first_q0_depth = last_template_depth + 1
    expected_pairs = {(0, 2), (0, 2 * k + 5)}
    q0_pairs = {p for p in exact[first_q0_depth] if 0 in p}
    if not expected_pairs.issubset(q0_pairs):
        raise AssertionError((k, first_q0_depth, q0_pairs))

    return {
        "k": k,
        "n": 3 * k + 6,
        "last_verified_template_depth": last_template_depth,
        "first_q0_depth_from_collision_frontier": first_q0_depth,
        "q0_pairs_at_first_depth": ";".join(f"{x}-{y}" for x, y in sorted(q0_pairs)),
        "status": "PASS",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--min-k", type=int, default=5)
    ap.add_argument("--max-k", type=int, default=100)
    ap.add_argument("--csv", default="reverse_layer_audit.csv")
    args = ap.parse_args()
    if args.min_k < 5 or args.max_k < args.min_k:
        raise SystemExit("require 5 <= --min-k <= --max-k")

    rows = []
    for k in range(args.min_k, args.max_k + 1):
        row = run_one(k)
        rows.append(row)
        print(
            f"k={k:3d} n={row['n']:3d} template<=d{row['last_verified_template_depth']:3d} "
            f"first_q0=d{row['first_q0_depth_from_collision_frontier']:3d} PASS"
        )

    out = Path(args.csv)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS: {len(rows)} cases; CSV={out}")


if __name__ == "__main__":
    main()
