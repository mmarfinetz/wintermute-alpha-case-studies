# Wintermute Alpha Challenge 2026 — Solutions

Reproducible analysis and Foundry solutions for the educational [Wintermute Alpha Challenge 2026](https://github.com/WintermuteResearch/Alpha-Challenge-2026).

The repository keeps Wintermute's checker format: analysis answers live in `answer.txt`, code answers live in `Solution.t.sol`, and `alpha.py` runs the corresponding hash or fork test.

## Progress

| ID | Challenge | Type | Points | Status |
|---:|---|---|---:|---|
| 00 | Warmup | Code | 25 | Included; CI fork test |
| 01 | Out of Nowhere | Analysis | 25 | Checker verified |
| 02 | Falling Dutchman | Code | 100 | Included; CI fork test |
| 03 | Too Big To Fail | Code | 100 | Included; CI fork test |
| 04 | First Blood | Analysis | 100 | Checker verified |
| 05 | Smart Money | Analysis | 100 | Checker verified |
| 06 | Cold Start | Code | 150 | Included; CI fork test |
| 07 | Firepit | Code | 150 | Included; CI fork test |
| 08 | First Move | Analysis | 150 | Checker verified |

**Analysis checker total: 375/375.** The workflow runs all five code cases against their historical fork blocks before they are marked complete.

## Run locally

```bash
cp .env.example .env
forge install foundry-rs/forge-std --no-commit
python3 alpha.py list
python3 alpha.py check
```

The Ethereum cases require an archive-capable RPC. Cold Start also needs a Robinhood Chain RPC, and Firepit needs an X Layer RPC.

## Repository layout

```text
challenges/<id>/
├── README.md or investigation notes
├── answer.txt          # analysis cases
├── Solution.t.sol      # code cases
└── challenge.json      # official checker metadata
```

## Method and attribution

The solutions were reconstructed from the official harnesses and public chain data, then cross-checked against public community solution repositories. Analysis values were independently validated against Wintermute's stored SHA-256 digests. See [`SOURCES.md`](./SOURCES.md).

This is an educational solution journal and is not affiliated with Wintermute.
