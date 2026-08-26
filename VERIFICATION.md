# Verification record

This repository contains complete solutions for the Wintermute Alpha Challenge 2026. The full challenge set has passed Wintermute's checker for a total score of **900/900**.

## Full verification

- **GitHub Actions run:** [900/900 historical-fork and analysis verification](https://github.com/mmarfinetz/wintermute-alpha-case-studies/actions/runs/32982797047)
- **Verified commit:** [`17e63ecb9a682bf9fd2ec971a817e9f3aa02884f`](https://github.com/mmarfinetz/wintermute-alpha-case-studies/commit/17e63ecb9a682bf9fd2ec971a817e9f3aa02884f)
- **Result:** **900/900**
- **Verification date:** August 26, 2026

| Check | Result | Observed end state |
|---|---:|---|
| Analysis challenges 01, 04, 05, and 08 | 375/375 | Every stored answer digest matched |
| 00 — Warmup | 25/25 | Official fork test passed |
| 02 — Falling Dutchman | 100/100 | 4.486821747353859972 ETH |
| 03 — Too Big To Fail | 100/100 | 2,504.476053968045169842 ETH |
| 06 — Cold Start | 150/150 | 11,234,190.620826071356323644 CASHCAT |
| 07 — Firepit | 150/150 | 50,650.152015 USD₮0 |
| **Total** | **900/900** | **All official checks passed** |

The current `main` branch is ahead of the verified commit only through documentation, environment examples, CI configuration, and RPC-proxy maintenance. No `answer.txt` or `Solution.t.sol` file was changed during the workflow repair.

## Current CI design

The original workflow launched five expensive historical forks in parallel after every push, including documentation-only changes. That created duplicate runs, public RPC contention, cache collisions, and misleading red status indicators unrelated to solution correctness.

CI is now split into two workflows:

### Automatic analysis verification

[`.github/workflows/verify.yml`](./.github/workflows/verify.yml) runs only when the official analysis inputs or checker change:

- `alpha.py`
- `challenges/**/answer.txt`
- `challenges/**/challenge.json`
- the workflow itself

The repaired workflow passed on [run 32984861534](https://github.com/mmarfinetz/wintermute-alpha-case-studies/actions/runs/32984861534).

### Manual historical-fork verification

[`.github/workflows/fork-tests.yml`](./.github/workflows/fork-tests.yml) is started manually from the Actions tab. It can run one code challenge or the complete set:

- `00`
- `02`
- `03`
- `06`
- `07`
- `all`

The fork cases execute sequentially rather than competing for public RPC capacity. Repository secrets named `ETH_RPC_URL`, `ROBINHOOD_RPC_URL`, and `XLAYER_RPC_URL` are used when present; otherwise the workflow uses the documented public fallbacks.

## Workflow incident and repair

Two kinds of failures appeared in the Actions history:

1. Documentation-only commits retriggered every historical-fork job even though no solution had changed.
2. The first manual-workflow revision contained an unquoted 160-bit hexadecimal `USER_ADDRESS`. GitHub's YAML loader treated it as a numeric scalar, rejected the workflow before job creation, and displayed immediate failed push runs with zero jobs.

The address is now quoted, the workflow parses correctly as a manual-only workflow, and later non-workflow commits no longer create phantom fork-test runs.

The Cold Start throttling proxy was also updated to treat `BrokenPipeError` and `ConnectionResetError` as normal early client disconnects, preventing duplicate error traces after successful Foundry requests.

## Local verification

```bash
cp .env.example .env
# Add archive-capable RPC endpoints.

forge install foundry-rs/forge-std@v1.16.2
python3 alpha.py check
```

A single case can be checked with:

```bash
python3 alpha.py check 03
```

Historical fork reproducibility ultimately depends on the selected RPC provider retaining archive state for the required block.
