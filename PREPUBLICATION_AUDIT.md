# No.14 Prepublication Audit

Status: **FINAL FREEZE PASS / ZENODO PUBLICATION WAITING**

## Frozen claim

The paper proves the exact compress-with-another threshold only for the explicitly defined total completion `Ahat_k` in the manuscript.

It does **not** claim that this completion is the unpublished/intended completion behind the cited source construction, and therefore it does **not** claim to resolve Conjecture 8 as stated without a separate source-level identification.

## Fresh reproduction

Fresh verifier run performed from the packaged source:

- `python verify_completion.py --max-k 100 --template-max-k 100`
- threshold/witness/reset cases `k=1..100`: PASS
- reverse-layer template cases `k=5..100`: PASS
- final marker: `ALL CHECKS PASS`

## Bibliography in manuscript

1. Marek Szykuła, *Synchronizing Automata: Open Problems*, EPTCS 451:33–47 (2026), DOI `10.4204/EPTCS.451.3`, arXiv:2608.24245.
2. Michalina Dżyga, *Synchronizing Automata with Extremal Properties*, Master's thesis, University of Wrocław (2018). The manuscript uses this only as attribution metadata and does not infer missing transitions from it.
3. Mikhail V. Volkov, *Synchronization of finite automata*, Russian Mathematical Surveys 77(5):819–891 (2022), DOI `10.4213/rm10005e`.

## Primary-source source audit

The 2026 Szykuła survey was checked directly against the public arXiv text before packaging:

- Sec. 1.1 explicitly defines the ambient model as deterministic finite **complete** semiautomata.
- Sec. 2.3 prints the `a` transition with `q0 -> q0`, but the displayed `b` transition has no `q0` case.
- The terminal state `q_{3k+5}` is assigned a self-loop under `a` only for even terminal parity and under `b` only for odd terminal parity, leaving the parity-complementary terminal action unspecified.
- Conjecture 8 prints `(ab)^(k+2) a (ab)^(k+2)` and labels its length `4n/3`; the literal word length is `4k+9`, whereas `n=3k+6` gives `4n/3=4k+8`.
- The survey attributes the series to Michalina Dżyga's 2018 master's thesis. The supervisor's public thesis list confirms that thesis title/year. This package still makes no source-level identification of the missing transitions.

These observations support the manuscript's conservative claim boundary.

## Publication state

- public GitHub repository created;
- Paper DOI reserved: `10.5281/zenodo.22803636`;
- Software DOI reserved: `10.5281/zenodo.22803640`;
- reserved DOI metadata inserted;
- DOI-bearing PDF rebuilt and frozen;
- final DOI-bearing GitHub state produced by GitHub Actions after a successful exact reproduction run;
- generated `__pycache__` removed from the frozen package.

## Remaining publication actions

- create the GitHub `v1.0.0` release at the final frozen commit;
- upload the exact frozen PDF and exact source archive to the two Zenodo drafts;
- audit draft files and metadata;
- publish Software and Paper records.

No mathematical blocker remains in the current release candidate.
