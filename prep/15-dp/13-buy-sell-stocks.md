# EP184 · P15E13 · Best Time to Buy and Sell Stock, I to IV   [Easy → Hard]

**Pattern:** DP (Dynamic Programming) · **Links:**
[I](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/) ·
[II](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/description/) ·
[III](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/description/) ·
[IV](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/description/)

---

## 🎬 Hook
> "Four stock problems, Easy to Hard, and most people learn four separate tricks. Don't.
> Each day you're in one of two moods, **holding** a share or **not**, and you only
> ever move between them by buying or selling. Draw that as two boxes and one arrow
> each way, and all four problems are the **same loop** with a different number of
> transactions allowed."

## 📋 Problem, in your words
```
prices[i] = the price on day i. Buy one share, sell it later, profit the difference.
You may hold at most ONE share at a time (sell before you buy again).

  I:   at most 1 transaction              maxProfit(prices)
  II:  unlimited transactions             maxProfit(prices)
  III: at most 2 transactions             maxProfit(prices)
  IV:  at most k transactions             maxProfit(k, prices)

A transaction = one buy + one sell. Doing nothing (profit 0) is always allowed.
```

## 🔢 The example
```
prices = [7, 1, 5, 3, 6, 4]
  I:   5      buy 1, sell 6
  II:  7      buy 1 sell 5 (+4), buy 3 sell 6 (+3)

prices = [3, 3, 5, 0, 0, 3, 1, 4]
  III: 6      buy 0 sell 3 (+3), buy 1 sell 4 (+3)

k = 2, prices = [3, 2, 6, 5, 0, 3]
  IV:  7      buy 2 sell 6 (+4), buy 0 sell 3 (+3)

prices = [7, 6, 4, 3, 1]  -> 0 for all four (never buy)
```

## 🧸 ELI5
> Every evening you're in one of two states, and you keep a scorecard for each:
>
> ```
>              buy (pay today's price)
>   ┌────────┐  ───────────────────►  ┌─────────┐
>   │  FREE  │                        │ HOLDING │
>   │ (cash) │  ◄───────────────────  │ (share) │
>   └────────┘   sell (earn today's)  └─────────┘
>     ↺ rest                             ↺ rest
> ```
>
> **free** = the most money you could have tonight *not* holding a share.
> **hold** = the most money you could have tonight *holding* one (usually negative:
> you spent cash on it).
>
> Each new day, each scorecard asks "is it better to stay as I am, or to cross over?"
> That's it. Limit the number of crossings and you get I, III and IV. Don't limit them
> and you get II.

## 🐌 Brute force (say it, don't type it)
- **I:** every pair `(buy day, sell day)`: **O(n²)**.
- **II to IV:** every way to choose disjoint buy/sell pairs: exponential.

The general recursion is the state machine itself, `f(day, holding, transactions_left)`,
with rest or cross at each day. Memoised it's O(n · k) states, and that's the DP.

## 💡 The pattern reveal
**Signal:** a **sequence of days** · a **choice each day** (buy, sell, rest) · "maximum
profit" · a limit on transactions.
**Therefore:** DP, Shape A with extra state. The pattern card's trap #1 in action: `f(i)`
alone can't decide whether selling is legal today, so the state grows to
**(day, holding, transactions used)**.

```
# the general recurrence, one day at a time
free[t] = max(free[t],  hold[t] + price)      # rest, or SELL (completes transaction t)
hold[t] = max(hold[t],  free[t-1] - price)    # rest, or BUY  (starts transaction t)
```

| version | limit | what the state collapses to |
|---|---|---|
| **I** | k = 1 | `hold` = `-min_price_so_far`, `free` = best profit. Running minimum *is* DP. |
| **II** | k = ∞ | no transaction count at all: just `hold` and `free` |
| **III** | k = 2 | four variables: `buy1, sell1, buy2, sell2` |
| **IV** | any k | arrays `hold[0..k]`, `free[0..k]` |

**Key insight:** Stock I's "track the minimum price so far" isn't a separate trick. It's
this machine with k = 1: `hold = max(hold, -price)` is literally "remember the cheapest
buy". Once you see I as a state machine, II is "drop the count", III is "two copies
chained together", and IV is "k copies in an array".

## 🔍 Dry run

**I, `[7, 1, 5, 3, 6, 4]`:** min price and best profit.

| price | min_price | price - min | best |
|---|---|---|---|
| 7 | 7 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 5 | 1 | 4 | 4 |
| 3 | 1 | 2 | 4 |
| 6 | 1 | 5 | **5** |
| 4 | 1 | 3 | 5 |

**II, same prices:** `hold, free = max(hold, free - p), max(free, hold + p)`, both
computed from yesterday's values.

| price | hold (best if holding) | free (best if not) | what happened |
|---|---|---|---|
| start | -∞ | 0 | |
| 7 | -7 | 0 | could buy at 7 |
| 1 | -1 | 0 | buying at 1 is better |
| 5 | -1 | **4** | sell: -1 + 5 |
| 3 | **1** | 4 | buy again: 4 - 3 |
| 6 | 1 | **7** | sell: 1 + 6 |
| 4 | 3 | 7 | |

Answer **7** ✓.

**III, `[3, 3, 5, 0, 0, 3, 1, 4]`:** four scorecards, each updated from yesterday's.

| price | buy1 | sell1 | buy2 | sell2 |
|---|---|---|---|---|
| 3 | -3 | 0 | -3 | 0 |
| 3 | -3 | 0 | -3 | 0 |
| 5 | -3 | 2 | -3 | 2 |
| 0 | 0 | 2 | **2** | 2 |
| 0 | 0 | 2 | 2 | 2 |
| 3 | 0 | 3 | 2 | **5** |
| 1 | 0 | 3 | 2 | 5 |
| 4 | 0 | 4 | 2 | **6** |

Answer `sell2` = **6** ✓. Row 4 (price 0): `buy2 = sell1 - 0 = 2` means "I made 2 on the
first trade and bought again for free".

## ✅ Optimal solution
**I** (LeetCode 121):
```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """One transaction. The k = 1 state machine: hold is 'cheapest buy so far'.

        Time: O(n). Space: O(1).
        """
        min_price, best = float("inf"), 0
        for p in prices:
            min_price = min(min_price, p)          # best 'hold' so far, as a price
            best = max(best, p - min_price)        # best 'free': sell today?
        return best
```

**II** (LeetCode 122):
```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """Unlimited transactions: two states, no count.

        Time: O(n). Space: O(1).
        """
        hold, free = float("-inf"), 0
        for p in prices:
            hold, free = max(hold, free - p), max(free, hold + p)   # both from yesterday
        return free
```

**III** (LeetCode 123):
```python
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        """At most two transactions: two machines chained, second starts from sell1.

        Time: O(n). Space: O(1).
        """
        buy1 = buy2 = float("-inf")
        sell1 = sell2 = 0
        for p in prices:
            sell2 = max(sell2, buy2 + p)           # updated in this order so every
            buy2 = max(buy2, sell1 - p)            # right-hand side is still
            sell1 = max(sell1, buy1 + p)           # yesterday's value
            buy1 = max(buy1, -p)
        return sell2
```

**IV** (LeetCode 188), the general case:
```python
class Solution:
    def maxProfit(self, k: int, prices: List[int]) -> int:
        """At most k transactions.

        hold[t] = best cash while holding, in transaction t.
        free[t] = best cash with t transactions completed, not holding.
        Time:  O(n * k). Space: O(k).
        """
        n = len(prices)
        if k >= n // 2:                            # can't use more than n/2: same as II
            return sum(max(0, prices[i + 1] - prices[i]) for i in range(n - 1))

        hold = [float("-inf")] * (k + 1)
        free = [0] * (k + 1)
        for p in prices:
            for t in range(k, 0, -1):              # high t first: reads t-1 before it changes
                free[t] = max(free[t], hold[t] + p)        # rest, or sell
                hold[t] = max(hold[t], free[t - 1] - p)    # rest, or buy
        return free[k]
```
**Time:** O(n) for I to III, O(n · k) for IV · **Space:** O(1), O(k) for IV

## ⚠️ Gotchas
- **Update from yesterday's values.** `hold, free = ...` as one tuple assignment in II.
  In III, update in the order `sell2, buy2, sell1, buy1` so each reads the old value.
  (The other order happens to work too, because buying and selling on the same day nets
  0, but you should be able to say why yours is correct.)
- **`hold` starts at -∞, not 0.** 0 would mean "holding a share that cost nothing", and
  you'd sell it for free profit on day 1.
- **II has a one-line greedy:** sum every positive day-to-day difference. Correct, and
  worth saying, but it doesn't extend to k limits. The state machine does.
- **IV with huge k.** At most `n // 2` transactions are ever useful. Without the
  shortcut, k = 10⁹ allocates a billion-cell array.
- **The answer is a `free` state.** Ending while holding a share is never better than
  having sold it (or never bought it).

## 🎤 Interview talking points
- *"I model it as two states per day, holding or not, with buy and sell as the
  transitions. Each day each state takes the better of resting or crossing over."*
- *"Stock I is that machine with one transaction: 'hold' is just the minimum price so
  far."*
- *"For k transactions I keep hold[t] and free[t] for t up to k, O(nk) time, and if k is
  at least n/2 it's the unlimited case."*
- *"Cooldown and transaction fee are the same machine with one more state or a
  subtraction on the sell edge."* ← LeetCode 309 and 714, before they're asked.

## 🔗 Transfer
The pattern card files this under 1-D linear because Stock I is just a running minimum,
and that's the hook: seeing a running minimum *as* a state lets the harder versions
attach to it. "Add a dimension to the state until each step can be decided" is the same
move as House Robber's reach back to `i-2` (EP174) and LIS's "ending exactly at i"
(EP180). EP185 is the last new shape: the state stops being a position and becomes a
**range**.

## 📹 Metadata
- **Title:** `All 4 Stock problems are ONE state machine | DP #13`
- **Thumbnail:** `HOLD ⇄ FREE`
- **Short:** the two-box diagram, then the II table filling day by day with the two
  sells highlighted. 50s.
