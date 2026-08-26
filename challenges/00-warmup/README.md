# 00 — Warmup

**Status:** Verified — 25/25

## Objective

Fork Ethereum at block `21,895,252`, start the challenge actor with 10 ETH, and finish with at least 1 WETH.

## Solution

WETH wraps native ETH one-for-one. The solution broadcasts from the provided user and calls:

```solidity
IWETH(WETH).deposit{value: 1 ether}();
```

No swap or approval is required because `deposit()` mints WETH directly to `msg.sender`.

## Verification

```bash
python3 alpha.py check 00
```

The historical fork test satisfies `IERC20(WETH).balanceOf(user) >= 1 ether`.
