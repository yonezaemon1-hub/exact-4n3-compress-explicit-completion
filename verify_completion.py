#!/usr/bin/env python3
"""All-in-one compatibility verifier for the Paper 14 draft.

Canonical public scripts:
  * experiment_exact_threshold.py  -- exact finite threshold/reset experiment
  * verify_reverse_layers.py       -- reverse-layer formula audit

This wrapper runs both with the requested finite ranges.
"""
import argparse
import subprocess
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-k", type=int, default=100)
    ap.add_argument("--template-max-k", type=int, default=100)
    args = ap.parse_args()
    if args.max_k < 1:
        ap.error("--max-k must be >= 1")
    if args.template_max_k < 5:
        ap.error("--template-max-k must be >= 5")

    here = Path(__file__).resolve().parent
    subprocess.run(
        [
            sys.executable,
            str(here / "experiment_exact_threshold.py"),
            "--max-k", str(args.max_k),
            "--csv", str(here / "experiment_exact_threshold.csv"),
        ],
        check=True,
    )
    subprocess.run(
        [
            sys.executable,
            str(here / "verify_reverse_layers.py"),
            "--max-k", str(args.template_max_k),
            "--csv", str(here / "reverse_layer_audit.csv"),
        ],
        check=True,
    )
    print("ALL CHECKS PASS")


if __name__ == "__main__":
    main()
