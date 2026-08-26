# 02 — Falling Dutchman

**Status:** Verified — 100/100

## Objective

At Ethereum block `9,462,777`, turn the user's starting `0.1 ETH` into at least `4 ETH` by trading through the deprecated DutchX exchange.

## Opportunity

DutchX auction index `1051` exposes a large historical pricing discrepancy across the KNC/WETH pair. The solution takes both sides in sequence rather than writing storage or assigning itself tokens with Foundry cheatcodes.

## Execution

1. Wrap `0.1 ETH` into WETH.
2. Deposit WETH into DutchX.
3. Bid WETH into the `KNC/WETH` auction, claim the KNC, and withdraw it.
4. Deposit all received KNC.
5. Bid the KNC into the reverse `WETH/KNC` auction at the same index.
6. Claim and withdraw WETH.
7. Unwrap the WETH to native ETH.

The core calls are:

```solidity
dx.postBuyOrder(KNC, WETH, 1051, 0.1 ether);
dx.claimBuyerFunds(KNC, WETH, user, 1051);

dx.postBuyOrder(WETH, KNC, 1051, knc);
dx.claimBuyerFunds(WETH, KNC, user, 1051);
```

## Result

The official fork assertion passes with roughly `6.012 ETH`, above the required `4 ETH`.

```bash
python3 alpha.py check 02
```
