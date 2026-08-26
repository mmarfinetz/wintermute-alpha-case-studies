# 07 — Firepit

**Status:** Verified — 150/150

## Objective

At X Layer block `68,413,600`, start with 2,000 UNI and end with at least `45,000 USD₮0`.

## Solution path

1. Call the V3 open-fee adapter for 22 pools to collect accumulated protocol fees into the token jar.
2. Approve the releaser to spend 2,000 UNI.
3. Burn the UNI through `release()` and receive the jar's USDT and other assets.
4. Convert the non-USDT balances through liquid X Layer V3 pools.

The direct routes include:

- WOKB → USDT;
- XBTC → USDT;
- USDC → USDT.

XETH uses a deeper two-hop route:

- XETH → USDG;
- USDG → USDT.

The test contract implements `uniswapV3SwapCallback` and pays each pool from the user's approved balances.

## Result

The historical fork ends with approximately `50,650.152015 USD₮0`, above the required 45,000.

```bash
python3 alpha.py check 07
```
