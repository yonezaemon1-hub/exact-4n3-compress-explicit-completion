#!/usr/bin/env python3
"""Exact finite experiment for the explicit completion in Paper 14.

Computes the q0 compress-with-another threshold by exact pair BFS, checks the
explicit length-4n/3 witness and reset construction, and writes a CSV audit log.
Standard library only.
"""
import argparse
import csv
from pathlib import Path

from completion_model import (
    automaton,
    c_word,
    image_set,
    image_state,
    letter_profile,
    q0_threshold,
    reset_word,
)


def run_one(k):
    a, b = automaton(k)
    n = len(a)
    A, B = 2 * k + 4, 2 * k + 5

    rank_a, collisions_a, missing_a = letter_profile(a)
    rank_b, collisions_b, missing_b = letter_profile(b)
    if rank_a != n - 1 or rank_b != n - 1:
        raise AssertionError((k, "rank", rank_a, rank_b))
    if [set(x) for x in collisions_a] != [{4, B}]:
        raise AssertionError((k, "a collision", collisions_a))
    if [set(x) for x in collisions_b] != [{3, A}]:
        raise AssertionError((k, "b collision", collisions_b))

    witness = c_word(k)
    expected = 4 * k + 8
    if len(witness) != expected:
        raise AssertionError((k, "witness length", len(witness), expected))
    witness_images = [image_state(q, witness, a, b) for q in (0, 2, B)]
    if witness_images != [2, 2, 2]:
        raise AssertionError((k, "witness image", witness_images))

    threshold, minimizers = q0_threshold(k)
    if threshold != expected or 2 not in minimizers or B not in minimizers:
        raise AssertionError((k, "threshold", threshold, minimizers))

    rw = reset_word(k)
    expected_reset_len = 3 * k * k + 16 * k + 19
    reset_image = image_set(range(n), rw, a, b)
    if len(rw) != expected_reset_len or reset_image != {2}:
        raise AssertionError((k, "reset", len(rw), reset_image))

    return {
        "k": k,
        "n": n,
        "threshold": threshold,
        "expected_4k_plus_8": expected,
        "q0_minimizing_partners": ";".join(map(str, minimizers)),
        "witness_length": len(witness),
        "reset_length": len(rw),
        "rank_a": rank_a,
        "rank_b": rank_b,
        "missing_a": ";".join(map(str, missing_a)),
        "missing_b": ";".join(map(str, missing_b)),
        "status": "PASS",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-k", type=int, default=100)
    ap.add_argument("--csv", default="experiment_exact_threshold.csv")
    args = ap.parse_args()
    if args.max_k < 1:
        raise SystemExit("--max-k must be >= 1")

    rows = []
    for k in range(1, args.max_k + 1):
        row = run_one(k)
        rows.append(row)
        print(
            f"k={k:3d} n={row['n']:3d} threshold={row['threshold']:3d} "
            f"partners={row['q0_minimizing_partners']} reset={row['reset_length']} PASS"
        )

    out = Path(args.csv)
    with out.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    print(f"PASS: {len(rows)} cases; CSV={out}")


if __name__ == "__main__":
    main()
