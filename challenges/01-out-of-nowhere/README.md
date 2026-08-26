# 01 — Out of Nowhere

**Status:** Verified — 25/25

## Objective

Trace the $1.5M transfer arriving on Ethereum back to the source-chain transaction that initiated the withdrawal.

## Starting point

Ethereum transaction:

`0xe7b8d46c3f3e5f727cb42c9dfe7fc36855ab5092cf160e4c8812a2a27a84350b`

The transaction contains an Allbridge `Received` event. The useful cross-chain fields are the lock identifier and source-chain code. The source metadata points to Stacks, so the Ethereum receipt is the destination leg rather than the transaction Wintermute asks for.

## Trace

The destination event identifies:

- recipient: `0xEc5f2EFa1A13c81179dDb0f0d4385e99E275994b`
- received amount: `1,498,500 USDC`
- lock ID: `0x0159fa4cd496a40b6531521bb9138a06`
- source code: `0x53544b5a` (`STKZ`)

The corresponding Allbridge Classic contract on Stacks is:

`SP3Y2ZSH8P7D50B0VBTSX11S7XSG24M1VB9YFQA4K.bridge`

Using the lock ID to correlate the bridge state with the source-side lock invocation leads to:

`0x36f2d5c245d08de980d0d23e4bd23b088312ce9e4b9845b4fd71930f52aab8fc`

The amount also provides a sanity check: roughly 1.5M was locked on the source side and 1,498,500 USDC was released on Ethereum after the bridge fee.

## Answer

```text
origin_tx = 0x36f2d5c245d08de980d0d23e4bd23b088312ce9e4b9845b4fd71930f52aab8fc
```

The normalized answer's SHA-256 digest matches the digest in Wintermute's official local checker.
