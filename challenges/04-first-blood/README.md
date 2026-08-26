# 04 — First Blood

**Status:** Verified — 100/100

## Objective

For the Official TRUMP launch on Solana, identify:

1. the first attempt to snipe the token; and
2. the transaction that actually made trading possible.

## Method

The relevant market is the Meteora TRUMP/USDC pool. The apparent pair-creation time is misleading because the pool was initialized and funded before trading was enabled.

- For `trading_possible`, inspect the first successful pool swap and then the immediately preceding Meteora `TogglePairStatus` transaction.
- For `first_snipe`, examine the earliest pool activity, exclude creator/deployer setup transactions, and take the first non-creator attempt.

## Answers

```text
first_snipe = 41h3CuLHamSdfsmgWC887eoyvrTiUcGjhLZpKMeqE9Rg9ZkP42C2gBr5PrQM9D25jRFwwQYPfBUJYCEUXC1qAxcv
trading_possible = 4SMUTho76nrPXxGNdDBNdBNbtbSC48oDDkivVKSdWUJR8KZGQwv1tEwJnHFXmpFDFkkLRupzzW28e6HHpv49afQt
```

Both normalized values match Wintermute's official hashes.

```bash
python3 alpha.py check 04
```
