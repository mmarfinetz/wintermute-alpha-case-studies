# 06 — Cold Start

**Status:** Verified — 150/150

## Objective

Use only Robinhood Chain's Ethereum Delayed Inbox to make the challenge user hold at least `1,000,000 CASHCAT` on the L2.

The harness forks:

- Ethereum at block `25,347,213`;
- Robinhood Chain at block `120,000`.

It records the L1 inbox message and replays the encoded L2 call as the user's Arbitrum address alias.

## Solution path

A direct call to the CASHCAT/WETH pool would require the sender to implement the Uniswap V3 swap callback. The aliased L2 sender is an EOA, so the retryable ticket instead targets Robinhood Chain's deployed SwapRouter02:

```text
SwapRouter02: 0xCaf681a66D020601342297493863E78C959E5cb2
WETH:         0x0Bd7D308f8E1639FAb988df18A8011f41EAcAD73
CASHCAT:      0x020bfC650A365f8BB26819deAAbF3E21291018b4
Pool fee:     10000
```

The L2 calldata encodes `exactInputSingle` with:

- WETH as `tokenIn`;
- CASHCAT as `tokenOut`;
- `2 ETH` as `amountIn`;
- the original user, not the alias, as recipient;
- `1,000,000e18` as the minimum output.

The L1 user then calls `createRetryableTicket`, supplying the 2 ETH L2 call value plus submission and execution fees. The harness relays that message on the Robinhood fork, where the router wraps the value, executes the swap, and sends CASHCAT to the user.

## Result

The dual-chain fork test finishes with `11,234,190.620826071356323644 CASHCAT`, well above the required threshold.

```bash
python3 alpha.py check 06
```
