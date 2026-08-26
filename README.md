# Wintermute Alpha Challenge 2026 — Case Studies

Reproducible investigation notes and solutions for Wintermute's Alpha Challenge 2026.

## Progress

| Challenge | Type | Points | Status |
|---|---|---:|---|
| 00 — Warmup | Code | 25 | Pending |
| 01 — Out of Nowhere | Analysis | 25 | ✅ Verified |
| 02 — Falling Dutchman | Code | 100 | Pending |
| 03 — Too Big To Fail | Code | 100 | Pending |
| 04 — First Blood | Analysis | 100 | Pending |
| 05 — Smart Money | Analysis | 100 | Pending |
| 06 — Cold Start | Code | 150 | Pending |
| 07 — Firepit | Code | 150 | Pending |
| 08 — First Move | Analysis | 150 | Pending |

**Verified score:** 25 / 900

## Challenge 01 — Out of Nowhere

Starting Ethereum transaction:

`0xe7b8d46c3f3e5f727cb42c9dfe7fc36855ab5092cf160e4c8812a2a27a84350b`

Verified source-chain transaction:

`0x36f2d5c245d08de980d0d23e4bd23b088312ce9e4b9845b4fd71930f52aab8fc`

The investigation follows the Allbridge transfer from Ethereum back to its Stacks source using the bridge event's lock identifier and source-chain metadata. A detailed write-up lives under `challenges/01-out-of-nowhere/`.

## Verification

Wintermute's official challenge runner checks analysis answers locally and uses Foundry fork tests for code challenges. No secrets or RPC credentials should be committed to this repository.

## Disclaimer

This is an independent solution journal for the educational Wintermute Alpha Challenge. It is not affiliated with or endorsed by Wintermute.
