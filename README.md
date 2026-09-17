# Exact 4n/3 Compress-with-Another Threshold for an Explicit Completion of a 3k+6-State Binary Family

Ryutaro Yonezu — Independent Researcher

This repository contains the manuscript source, preprint PDF, and exact reproducibility code for an explicitly defined total binary automaton family \(\widehat{A}_k\) on \(n=3k+6\) states.

## Main result

For every integer `k >= 1`, the explicitly defined completion is strongly connected and synchronizing, and the compress-with-another threshold of `q0` is exactly

`4k + 8 = 4n/3`.

A shortest witness is

`(ba)^(k+2) (ab)^(k+2)`.

For `k >= 5`, the lower bound is proved analytically by an exact symbolic reverse-pair frontier. The cases `k = 1,2,3,4` are verified exactly by finite computation.

## Claim boundary

This repository **does not claim to resolve Conjecture 8 as stated in the source literature**. The source survey's displayed transition definition leaves transitions unspecified. This work defines an explicit total completion that agrees with every displayed transition and specifies the missing cases separately. No claim is made that this completion is identical to the completion intended by the original authors.

## Reproduction

Python 3 standard library only:

```powershell
python .\verify_completion.py --max-k 100 --template-max-k 100
```

Expected final line:

```text
ALL CHECKS PASS
```

The frozen prepublication audit reproduced:

- exact threshold / witness / reset checks for `1 <= k <= 100`;
- exact reverse-layer template checks for `5 <= k <= 100`;
- all cases PASS.

## Files

- `paper.tex` — manuscript source
- `Yonezu_2026_Exact_4n3_Compress_Completion.pdf` — preprint PDF
- `completion_model.py` — exact automaton and pair-graph model
- `experiment_exact_threshold.py` — exact finite threshold/reset audit
- `verify_reverse_layers.py` — independent reverse-layer audit
- `verify_completion.py` — all-in-one verifier
- `experiment_exact_threshold.csv` — fresh 1..100 audit output
- `reverse_layer_audit.csv` — fresh 5..100 reverse-layer audit output
- `PREPUBLICATION_AUDIT.md` — release-boundary audit
- `SHA256SUMS.txt` — integrity manifest

## Licenses

The software and data files are released under the MIT License.  
The paper source and PDF are released under CC BY 4.0.

## Citation

Paper DOI: `10.5281/zenodo.22803636`  
Software DOI: `10.5281/zenodo.22803640`
