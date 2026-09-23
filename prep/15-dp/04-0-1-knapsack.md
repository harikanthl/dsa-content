# EP175 · P15E04 · 0/1 Knapsack   [Medium]

**Pattern:** DP (Dynamic Programming) · **Link:** https://www.geeksforgeeks.org/problems/0-1-knapsack-problem0945/1

---

## 🎬 Hook
> "House Robber with one extra number: your bag has a **weight limit**. That single
> number is why the state needs **two** coordinates instead of one, and once you can say
> what those two coordinates mean in one sentence, knapsack is done."

## 📋 Problem, in your words
```
n items. Item i weighs wt[i] and is worth val[i]. The bag holds at most W.
Each item is taken whole or left behind (that's the "0/1": no fractions,
no taking it twice). Return the most value that fits.

GfG: knapsack(W, val, wt) -> int.  n up to ~1000, W up to ~1000.
```

## 🔢 The example
```
Input:  W = 7, val = [1, 4, 5, 7], wt = [1, 3, 4, 5]
Output: 9
Why:    items 1 and 2: weight 3 + 4 = 7, value 4 + 5 = 9
        (the single most valuable item, value 7 at weight 5, only reaches 8 with item 0)

Input:  W = 4, val = [1, 2, 3], wt = [4, 5, 1]  -> 3
Input:  W = 3, val = [1, 2, 3], wt = [4, 5, 6]  -> 0   (nothing fits)
Input:  W = 5, val = [10, 40, 30, 50], wt = [5, 4, 2, 3]  -> 80   (items 2 + 3: 2 + 3 kg)
```

## 🧸 ELI5
> You're packing a 7 kg bag for a trip. You lay the items out in a row and walk down it,
> item by item. At each item you ask the House Robber question: **take it or leave it?**
>
> But now "take it" has a price beyond "the neighbour is forbidden": it **uses up
> weight**. After you take a 4 kg item, the rest of the trip is packed with a 3 kg bag.
>
> So "how well can I still do?" depends on two things, not one:
>
> ```
>   which items are still on the table?     -> i
>   how much room is left in the bag?       -> c
> ```
>
> Write the answer for every (i, c) pair on a grid of sticky notes and you never pack
> the same situation twice.

## 🐌 Brute force (say it, don't type it)
Try every subset: 2ⁿ of them, sum weights, keep the best value among those that fit.
**O(2ⁿ · n)**. Greedy by value-per-kg fails because items are indivisible: on the
example, ratios are 1, 1.33, 1.25, 1.4, so greedy takes item 3 (5 kg, value 7), then
item 0 (1 kg, value 1), total 8, and misses 9. (Greedy by ratio *is* optimal for the
**fractional** knapsack; say that, it shows you know why this one is different.)

## 💡 The pattern reveal
**Signal:** a **take-or-skip** choice per item · a **capacity** that choices consume ·
"**maximum** value".
**Therefore:** DP, Shape B (0/1 knapsack).

**Step 1, the state in one sentence:**

> `best(i, c)` = the most value I can get using **only the first `i` items**, with a bag
> of capacity `c`.

**Step 2, the recurrence.** Look at the last item in play, item `i - 1`:

```
skip = best(i - 1, c)                          # leave it: same bag, one fewer item
take = best(i - 1, c - wt[i - 1]) + val[i - 1] # take it: smaller bag, earn its value
best(i, c) = max(skip, take)                   # take only if wt[i - 1] <= c
```

Base case: `best(0, c) = 0`. No items, no value, whatever the bag.

**Key insight:** in House Robber, "take" moved you back two houses. Here "take" moves you
back one item **and shrinks the bag**. That shrinking is why one index isn't enough:
two calls with the same `i` but different `c` are different questions. The number of
distinct questions is `(n + 1) × (W + 1)`, and that's the whole cost.

## 🔍 Dry run: `W = 7`, `val = [1, 4, 5, 7]`, `wt = [1, 3, 4, 5]`

Items by index: 0 = (1 kg, 1), 1 = (3 kg, 4), 2 = (4 kg, 5), 3 = (5 kg, 7).
The table shows each state **in the order it finishes** (children before parents).
`best(0, *)` = 0 is the base and isn't listed.

| finishes | state `(i, c)` | item considered | skip | take | result |
|---|---|---|---|---|---|
| 1 | (1, 7) | item 0 (1 kg, 1) | 0 | 0 + 1 = 1 | **1** |
| 2 | (1, 4) | item 0 | 0 | 1 | **1** |
| 3 | (2, 7) | item 1 (3 kg, 4) | best(1,7) = 1 | best(1,4) + 4 = 5 | **5** |
| 4 | (1, 3) | item 0 | 0 | 1 | **1** |
| 5 | (1, 0) | item 0 | 0 | too heavy | **0** |
| 6 | (2, 3) | item 1 | best(1,3) = 1 | best(1,0) + 4 = 4 | **4** |
| 7 | (3, 7) | item 2 (4 kg, 5) | best(2,7) = 5 | best(2,3) + 5 = 9 | **9** |
| 8 | (1, 2) | item 0 | 0 | 1 | **1** |
| 9 | (2, 2) | item 1 | best(1,2) = 1 | too heavy | **1** |
| 10 | (3, 2) | item 2 | best(2,2) = 1 | too heavy | **1** |
| 11 | (4, 7) | item 3 (5 kg, 7) | best(3,7) = **9** | best(3,2) + 7 = 8 | **9** |

Answer **9** ✓. Only **11** of the 32 possible `(i, c)` states were ever asked. That's
the memo's advantage over a table: it only visits reachable states. Row 11 is the one to
narrate: taking the most valuable item (7) leaves 2 kg, worth only 1 more, so skipping
it and keeping 9 wins.

## ✅ Optimal solution
```python
from functools import lru_cache

class Solution:
    def knapsack(self, W: int, val: List[int], wt: List[int]) -> int:
        """Most value from items taken whole, total weight at most W.

        best(i, c) = most value using the first i items with capacity c.
        Time:  O(n * W), at most (n + 1)(W + 1) states, O(1) work each.
        Space: O(n * W) for the memo, plus O(n) recursion depth.
        """

        @lru_cache(maxsize=None)
        def best(i: int, c: int) -> int:
            if i == 0:
                return 0                              # no items left to consider
            w, v = wt[i - 1], val[i - 1]              # the i-th item is index i - 1
            skip = best(i - 1, c)
            if w > c:
                return skip                           # doesn't fit: skip is forced
            return max(skip, best(i - 1, c - w) + v)  # take it: smaller bag, earn v

        return best(len(val), W)
```
**Time:** O(n · W) · **Space:** O(n · W)

## ⚠️ Gotchas
- **`i` counts items, so the item is `i - 1`.** `best(i, c)` means "first `i` items";
  the one being decided is index `i - 1`. This is the pattern card's "empty prefix at 0"
  trap, and the same indexing carries straight into the EP177 table.
- **Check `w > c` before recursing.** Otherwise `c - w` goes negative and you either
  need a `c < 0` base case returning `-inf`, or you silently count an overweight bag.
- **O(n · W) is pseudo-polynomial.** It's polynomial in the *value* of W, not its size
  in bits. If W were 10⁹, this is useless. Say "pseudo-polynomial" if asked why
  knapsack is NP-hard but this runs fast.
- **Recursion depth is n.** GfG allows n near 1000, which brushes Python's recursion
  limit. That's one honest reason EP177 exists: the table has no stack.
- **Don't memoise on a list.** `lru_cache` needs hashable arguments; pass indices,
  never slices of `val`.

## 🎤 Interview talking points
- *"Greedy by ratio is right for fractional knapsack but wrong here, because items are
  indivisible. [1-line counterexample]."*
- *"State: best value from the first i items with capacity c. Two numbers, because
  taking an item changes the capacity left for everything else."*
- *"Recurrence: skip gives best(i-1, c); take gives best(i-1, c-w) + v, if it fits."*
- *"(n+1)(W+1) states, O(1) each: O(nW) time. That's pseudo-polynomial."*
- *"Next I'd turn this into a table, and then into a single row with a backwards loop."*

## 🔗 Transfer
The state just went 2-D, and "what does `best(i, c)` mean" is the sentence you'll say
in every knapsack-family episode. EP176 slows down and does the memo-to-table flip on
the 1-D problems you already know, so that EP177 can flip *this* one into a 2-D table
and then a single row. EP178 Subset Sum and EP179 Target Sum are this exact state with
the `max` replaced by `or` and `+`.

## 📹 Metadata
- **Title:** `0/1 Knapsack, why the state needs TWO numbers | DP #4`
- **Thumbnail:** `best(i, c)`
- **Short:** greedy-by-ratio packing 8 on the example, then the DP skipping the "best"
  item and landing on 9. 45s.
