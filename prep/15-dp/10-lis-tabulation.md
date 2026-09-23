# EP181 · P15E10 · LIS Tabulation   [Medium]

**Pattern:** DP (Dynamic Programming) · **Link:** builds on EP180 LIS, https://leetcode.com/problems/longest-increasing-subsequence/

---

## 🎬 Hook
> "Yesterday's LIS memo flips into a table in four lines. Then the usual last step,
> 'shrink it to a couple of variables', **fails**: every cell reads every cell before
> it. So we change what we store. The new array isn't even a real subsequence, and its
> **length** is the answer in O(n log n)."

## 📋 Problem, in your words
```
Same problem as EP180: length of the longest strictly increasing subsequence.

Today: (1) turn the end_at(i) memo into a bottom-up table, O(n^2);
       (2) replace the table with a 'tails' array + binary search, O(n log n).
```

## 🔢 The example
```
Input:  nums = [10, 9, 2, 5, 3, 7, 101, 18]
Output: 4

dp (EP180's end_at, as a table):  [1, 1, 1, 2, 2, 3, 4, 4]
tails at the end:                 [2, 3, 7, 18]   <- length 4, and NOT a subsequence
                                                     of anything you'd pick by hand
```

## 🧸 ELI5
> You're dealing cards into piles, left to right, with one rule: **a card goes on the
> leftmost pile whose top card is bigger than or equal to it**. If there isn't one, it
> starts a new pile on the right.
>
> ```
>  deal 10:  [10]
>  deal 9:   [9]                  9 covers 10
>  deal 2:   [2]                  2 covers 9
>  deal 5:   [2] [5]              nothing >= 5, new pile
>  deal 3:   [2] [3]              3 covers 5
>  deal 7:   [2] [3] [7]          new pile
>  deal 101: [2] [3] [7] [101]    new pile
>  deal 18:  [2] [3] [7] [18]     18 covers 101
> ```
>
> Four piles, so the LIS is 4. Each pile's top is **the smallest possible last element
> of an increasing run of that length**. Keeping those tops as small as possible leaves
> the most room for future cards to extend. (This is called patience sorting.)

## 🐌 Brute force (say it, don't type it)
EP180's memo is O(n²) with an O(n) recursion stack that overflows Python's limit near
n = 1000. The table below fixes the stack; the tails array fixes the time.

## 💡 The pattern reveal
**Part 1: EP176's five questions on `end_at(i)`.**

| # | question | answer |
|---|---|---|
| 1 | shape | one argument `i` in `0..n-1`: array of `n` |
| 2 | index shift | none |
| 3 | base | every cell starts at **1** (the element alone) |
| 4 | reads | `dp[i]` reads `dp[j]` for **every** `j < i`: all to the left, so fill left to right |
| 5 | answer | **`max(dp)`**, not a single cell |

Question 6, "how far back does a cell read?" **All the way.** No rolling variables here.
That's the signal that shrinking the table won't work and the *state* has to change.

**Part 2: the new state.**

> `tails[k]` = the **smallest** possible last element of any increasing subsequence of
> length `k + 1` seen so far.

`tails` is always **sorted** (a longer run can't end smaller than the best shorter run),
and sorted means binary search. For each `x`:

| where `bisect_left(tails, x)` lands | meaning | action |
|---|---|---|
| past the end | `x` beats every tail: it extends the longest run | `append(x)` |
| at index `k` | `x` makes a length-`k+1` run with a smaller ending | `tails[k] = x` |

**Key insight:** we stopped tracking *which* subsequence and started tracking *the best
ending for each length*. Replacing `tails[k]` never shortens anything, it only makes the
future easier. The length of `tails` is the LIS; its contents are not.

`bisect_left`, not `bisect_right`, because strictly increasing: an equal `x` must
**replace** its twin, not extend past it. That's EP73's first-occurrence binary search.

## 🔍 Dry run: `nums = [10, 9, 2, 5, 3, 7, 101, 18]`

| x | `bisect_left(tails, x)` | action | tails after | the run it represents |
|---|---|---|---|---|
| 10 | 0 (empty) | append | [10] | 10 |
| 9 | 0 | tails[0] = 9 | [9] | 9 (a length-1 run ending lower) |
| 2 | 0 | tails[0] = 2 | [2] | 2 |
| 5 | 1 (end) | append | [2, 5] | 2, 5 |
| 3 | 1 | tails[1] = 3 | [2, 3] | 2, 3 |
| 7 | 2 (end) | append | [2, 3, 7] | 2, 3, 7 |
| 101 | 3 (end) | append | [2, 3, 7, 101] | 2, 3, 7, 101 |
| 18 | 3 | tails[3] = 18 | [2, 3, 7, 18] | 2, 3, 7, 18 |

`len(tails)` = **4** ✓.

For comparison, the O(n²) table fills the same way EP180's memo did:

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| nums | 10 | 9 | 2 | 5 | 3 | 7 | 101 | 18 |
| dp | 1 | 1 | 1 | 2 | 2 | 3 | 4 | 4 |

Here's a case where `tails` is plainly not an answer: `[3, 4, 1]` ends with
`tails = [1, 4]`, and `1, 4` isn't a subsequence (the 1 comes after the 4). Length 2
is still correct.

## ✅ Optimal solution
```python
from bisect import bisect_left


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """LIS length by patience sorting.

        tails[k] = smallest possible last element of an increasing subsequence of
        length k + 1. tails stays sorted, so each element is placed by binary search.
        Time:  O(n log n), one bisect per element.
        Space: O(n) for tails.
        """
        tails = []
        for x in nums:
            k = bisect_left(tails, x)             # first tail >= x
            if k == len(tails):
                tails.append(x)                   # extends the longest run
            else:
                tails[k] = x                      # same length, smaller ending
        return len(tails)

    def lengthOfLIS_table(self, nums: List[int]) -> int:
        """EP180's memo, bottom-up. dp[i] = LIS ending exactly at i.

        Time:  O(n^2). Space: O(n). No recursion limit.
        """
        dp = [1] * len(nums)                      # each element alone
        for i in range(len(nums)):
            for j in range(i):                    # every earlier cell: all already filled
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)
```
**Time:** O(n log n) (O(n²) for the table) · **Space:** O(n)

## ⚠️ Gotchas
- **`tails` is not the subsequence.** Don't return it, don't print it as "the answer".
  If asked to reconstruct the actual LIS, keep the O(n²) table plus a `parent[i]` index,
  or store indices in `tails` with a parent array.
- **`bisect_left` for strictly increasing.** `bisect_right` lets `[7, 7, 7]` append
  every 7 and return 3. For **non-decreasing**, `bisect_right` is exactly right.
- **The table's answer is `max(dp)`.** Same trap as EP180, it survives the flip.
- **Don't try to roll the O(n²) table.** Each cell reads every earlier one, so any
  "keep the last two" version is wrong. Spotting that is the point of the episode.
- **Why replacing is safe:** swapping `tails[k]` for a smaller `x` doesn't change
  `len(tails)` and can only make it easier for later elements to extend. It never loses
  a run that could have been longer.

## 🎤 Interview talking points
- *"The memo becomes a table filled left to right; every cell reads all earlier cells,
  so it stays O(n²) and can't be rolled."*
- *"To go faster I change the state: tails[k] is the smallest ending of any increasing
  run of length k + 1. It's sorted, so I binary search where each element goes."*
- *"Either it extends the longest run, or it lowers the ending of a run of the same
  length. O(n log n)."*
- *"tails isn't the actual subsequence, only its length is meaningful."* ← say this
  before they catch it.
- *"bisect_left because strictly increasing; bisect_right would give non-decreasing."*

## 🔗 Transfer
This is the one episode where the last step of the method isn't "roll the table" but
"**rethink the state**", and binary search (Pattern 10) turns out to live inside a DP.
Russian Doll Envelopes is this exact code after sorting by width ascending and height
descending. EP182 LCS goes back to tables, but now with **two** sequences, so the
state becomes a pair `(i, j)` and the table becomes a grid.

## 📹 Metadata
- **Title:** `LIS in O(n log n), the array that's wrong but has the right LENGTH | DP #10`
- **Thumbnail:** `[2, 3, 7, 18] ≠ answer`
- **Short:** the card piles being dealt, 18 dropping onto 101. 45s.
