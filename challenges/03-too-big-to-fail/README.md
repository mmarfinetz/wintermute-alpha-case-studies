# 03 — Too Big To Fail

**Status:** Verified — 100/100

## Objective

At Ethereum block `12,465,029`, liquidate the enormous Liquity trove that survived the May 19, 2021 crash and finish with more than 2,500 ETH.

## Identification

The borrower is the sender of the later rebalance transaction referenced by the case:

```text
0x903d12bf2c57A29f32365917c706ce0e1a84Cce3
```

Liquity V1's TroveManager is:

```text
0xA39739EF8b0231DbFA0DcdA07d7e29faAbCf4bb2
```

## Solution

The position is liquidatable at the fork state. Only one protocol call is required:

```solidity
ITroveManager(TROVE_MANAGER).liquidate(WHALE);
```

Liquity pays the caller collateral gas compensation. A fraction of a billion-dollar trove is still thousands of ETH.

## Result

The historical fork ends with approximately `2,504.476 ETH`, satisfying the `> 2,500 ETH` assertion.

```bash
python3 alpha.py check 03
```
