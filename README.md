# Wintermute Alpha Challenge 2026 — Complete Solutions

![Analysis verification](https://github.com/mmarfinetz/wintermute-alpha-case-studies/actions/workflows/verify.yml/badge.svg?branch=main)

Reproducible analysis and Foundry solutions for the educational [Wintermute Alpha Challenge 2026](https://github.com/WintermuteResearch/Alpha-Challenge-2026).

**Full verification:** [900/900 passed in GitHub Actions](https://github.com/mmarfinetz/wintermute-alpha-case-studies/actions/runs/32982797047) on verified commit [`17e63ec`](https://github.com/mmarfinetz/wintermute-alpha-case-studies/commit/17e63ecb9a682bf9fd2ec971a817e9f3aa02884f). See [`VERIFICATION.md`](./VERIFICATION.md) for the run evidence and CI repair record.

The repository preserves Wintermute's checker format: analysis answers live in `answer.txt`, executable answers live in `Solution.t.sol`, and `alpha.py` runs the official-style hash and historical-fork checks.

## Score

| ID | Challenge | Type | Points | Verification |
|---:|---|---|---:|---|
| 00 | Warmup | Code | 25 | Historical fork passed |
| 01 | Out of Nowhere | Analysis | 25 | Official answer hash matched |
| 02 | Falling Dutchman | Code | 100 | Historical fork passed |
| 03 | Too Big To Fail | Code | 100 | Historical fork passed |
| 04 | First Blood | Analysis | 100 | Both official answer hashes matched |
| 05 | Smart Money | Analysis | 100 | All four official answer hashes matched |
| 06 | Cold Start | Code | 150 | Dual-chain historical fork passed |
| 07 | Firepit | Code | 150 | Historical X Layer fork passed |
| 08 | First Move | Analysis | 150 | Both official answer hashes matched |
|  | **Total** |  | **900** | **900/900 verified** |

## Solution highlights

- **Out of Nowhere:** correlate an Allbridge lock ID from Ethereum back to the initiating Stacks transaction.
- **Falling Dutchman:** arbitrage DutchX auction 1051 through a WETH → KNC → WETH round trip, growing 0.1 ETH beyond the 4 ETH requirement without test-only balance writes.
- **Too Big To Fail:** liquidate the billion-dollar Liquity trove and collect roughly 2,504 ETH of liquidator compensation.
- **First Blood:** identify the earliest non-creator TRUMP snipe and the Meteora status-toggle transaction that actually enabled trading.
- **Smart Money:** attribute two fundraises, one VC wallet, and one high-volume company address.
- **Cold Start:** encode a retryable ticket through the Arbitrum Delayed Inbox and route its L2 execution through SwapRouter02 to acquire CASHCAT.
- **Firepit:** collect X Layer protocol fees, burn UNI to release the jar, then route the received assets into more than 45,000 USD₮0.
- **First Move:** derive the honest first counterclaims for hypothetical Ink and Optimism fault-dispute games.

## Run locally

Requirements:

- Python 3.8+
- [Foundry](https://book.getfoundry.sh/getting-started/installation)
- Archive-capable RPC endpoints for the historical blocks used by the code challenges

```bash
cp .env.example .env
# Fill in the archive RPC values in .env.

forge install foundry-rs/forge-std@v1.16.2
python3 alpha.py list
python3 alpha.py check
```

Run a single case with its numeric prefix:

```bash
python3 alpha.py check 02
```

### RPC coverage

- `ETH_RPC_URL`: Ethereum archive state, including blocks 9,462,777; 12,465,029; 21,895,252; and 25,347,213.
- `ROBINHOOD_RPC_URL`: Robinhood Chain archive state at block 120,000.
- `XLAYER_RPC_URL`: X Layer state at block 68,413,600.

For reliable local runs, use your own archive endpoints. The manual GitHub workflow also includes public-provider fallbacks.

## Continuous integration

CI is split so documentation changes do not launch several costly historical forks:

- [`verify.yml`](./.github/workflows/verify.yml) automatically checks all analysis answers when an answer, digest, checker, or the workflow itself changes.
- [`fork-tests.yml`](./.github/workflows/fork-tests.yml) manually runs one executable challenge or all five, sequentially, from the Actions tab.

The manual workflow uses `ETH_RPC_URL`, `ROBINHOOD_RPC_URL`, and `XLAYER_RPC_URL` repository secrets when configured. Public fallbacks remain available for reproducibility.

## Layout

```text
.
├── alpha.py
├── challenges/
│   └── <id>/
│       ├── README.md
│       ├── answer.txt       # analysis cases
│       ├── Solution.t.sol   # code cases
│       └── challenge.json
├── scripts/
│   └── throttled_rpc_proxy.py
├── .github/workflows/
│   ├── verify.yml
│   └── fork-tests.yml
├── SOURCES.md
└── VERIFICATION.md
```

## Verification and attribution

The analysis values are validated against Wintermute's stored SHA-256 digests. The executable cases are tested against the unmodified historical end-state requirements in `checkSolve()`.

The official harnesses, public chain data, and public community write-ups were used as specifications and cross-checks. The repository does not present the work as an unaided first discovery; see [`SOURCES.md`](./SOURCES.md) for detailed attribution.

This educational solution journal is not affiliated with Wintermute.
