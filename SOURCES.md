# Sources and attribution

## Primary specification

- [`WintermuteResearch/Alpha-Challenge-2026`](https://github.com/WintermuteResearch/Alpha-Challenge-2026) — official challenge descriptions, constants, `setUp()` fixtures, `checkSolve()` assertions, scoring metadata, and answer hashes.

The official fixtures and end-state assertions are treated as the source of truth. Analysis answers are normalized and checked against their official SHA-256 digests. Code cases are executed on the specified historical forks.

## Public community cross-checks

- [`NickGardi/alpha-challenge-2026-solutions`](https://github.com/NickGardi/alpha-challenge-2026-solutions) — complete public write-up and executable solution examples used to cross-check all cases, especially Cold Start and Firepit.
- [`VarozXYZ/Alpha-Challenge-2026`](https://github.com/VarozXYZ/Alpha-Challenge-2026) — independent executable solutions, including the real DutchX WETH/KNC round trip used as the basis for Challenge 02.
- [`0xTyche/alpha-challenge-2026-writeups`](https://github.com/0xTyche/alpha-challenge-2026-writeups) — detailed Allbridge/Stacks tracing notes for Challenge 01.

## Representation of the work

The code and explanations in this repository were reviewed, reorganized, and rewritten into one reproducible solution journal. They are not represented as unaided original discovery. Where community work supplied a solution lead, it is named above.

Independent verification performed here includes:

- reproducing every analysis digest with the official checker;
- compiling the full Solidity project with Foundry;
- executing the code cases against the exact historical fork assertions;
- avoiding test-only storage or token-balance writes in the DutchX solution;
- retaining the official challenge actor, fork blocks, and `checkSolve()` requirements.
