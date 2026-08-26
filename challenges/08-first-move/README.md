# 08 — First Move

**Status:** Verified — 150/150

## Objective

For hypothetical game-type-8 fault-dispute games on Ink and Optimism, derive the honest `bytes32` counterclaim for the first attack on the invalid root claim.

## Method

For the first root attack, the trace position maps to a claimed L2 block far beyond the available chain tip. The honest provider therefore clamps to the safe L2 head corresponding to the supplied L1 head.

For each chain, the output root is constructed as:

```text
keccak256(
    bytes32(0)
    || stateRoot
    || messagePasserStorageRoot
    || blockHash
)
```

The two chains have different starting block numbers and safe heads, so their output roots differ even though the hypothetical games share the same invalid root claim.

## Answers

```text
ink_claim = 0x82c941153a9de14c4533b301799ee33206b6a475d7c4fdbe7cd2f1c9d7271b6f
op_claim = 0x192f163548d61d555a282e1ffcec8ec7b1e4cf9deced7e910b87292f0aeab5f1
```

Both values match Wintermute's official answer hashes.

```bash
python3 alpha.py check 08
```
