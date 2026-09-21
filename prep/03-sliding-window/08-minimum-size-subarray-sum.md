# EP028 · P03E08 · Minimum Size Subarray Sum (revisited)   [Medium]

**Pattern:** Sliding Window · **Link:** https://leetcode.com/problems/minimum-size-subarray-sum/

---

> **A note on this episode.** This is the same LeetCode problem as EP22. Rather than
> record it twice, this episode is the **second visit**: solve it a completely
> different way — prefix sums plus binary search — and use the comparison to answer the
> question EP22 left open. *What happens when the numbers can be negative?*
>
> That framing is worth an episode on its own. "Here are two correct solutions and here
> is how I'd choose between them" is a senior conversation, and it's the bridge into
> Pattern 05.

---

## 🎬 Hook
> "We already solved this in eight lines with a sliding window. So why solve it again,
> slower? Because the window relies on a property nobody mentioned out loud — and the
> moment that property goes away, the elegant solution silently breaks. Today we find
> the load-bearing assumption."

## 📋 Problem, in your words
```
Given an array of positive integers and a target,
find the length of the SMALLEST contiguous subarray whose sum is >= target.
Return 0 if none exists.

(Same statement as EP22. Today: a second method, and the follow-up.)
```

## 🔢 The example
```
Input:  nums = [2, 3, 1, 2, 4, 3],  target = 7
Output: 2        ([4, 3])

prefix sums:  index:   0  1  2  3  4   5   6
              pre:     0  2  5  6  8  12  15
              pre[i] = sum of the first i elements
```

## 🧸 ELI5
> Imagine walking along the array keeping a **running total** on a clipboard — after
> one step 2, after two steps 5, after three 6, and so on. That list of running totals
> is the *prefix sums*.
>
> The sum of any stretch is just **one reading minus an earlier reading**. The stretch
> from step 2 to step 5 is `pre[5] − pre[2] = 12 − 5 = 7`.
>
> So "find a short stretch summing to at least 7" becomes: for each current reading,
> **how recently was the clipboard at least 7 lower?** And because all the numbers are
> positive, the clipboard only ever goes **up** — which means that list is sorted,
> which means you can **binary search** it.

## 🐌 Brute force
O(n²) — every start, extend right. Covered in EP22.

## 💡 The pattern reveal
**Today's route:** prefix sums + binary search.

**Key insight #1:** `sum(nums[lo:hi]) = pre[hi] − pre[lo]`. Turning "sum of a range"
into "difference of two numbers" is the whole idea of Pattern 05, met here for the
first time.

**Key insight #2:** for each `hi`, you want the **largest** `lo` with
`pre[hi] − pre[lo] ≥ target`, i.e. `pre[lo] ≤ pre[hi] − target`. Largest `lo` means
shortest window.

**Key insight #3 — the load-bearing one:** all values are positive ⟹ `pre` is
**strictly increasing** ⟹ `pre` is sorted ⟹ binary search is legal. *This same
property is what let EP22's window shrink and never look back.* One assumption, two
algorithms standing on it.

## 🔍 Dry run — `[2, 3, 1, 2, 4, 3]`, target = 7
`pre = [0, 2, 5, 6, 8, 12, 15]`

| hi | `pre[hi]` | need `pre[lo] ≤ pre[hi] − 7` | largest such `lo` | length `hi − lo` | best |
|---|---|---|---|---|---|
| 1 | 2 | ≤ −5 | none | — | ∞ |
| 2 | 5 | ≤ −2 | none | — | ∞ |
| 3 | 6 | ≤ −1 | none | — | ∞ |
| 4 | 8 | ≤ 1 | `lo=0` (`pre[0]=0`) | 4 | 4 |
| 5 | 12 | ≤ 5 | `lo=2` (`pre[2]=5`) | 3 | 3 |
| 6 | 15 | ≤ 8 | `lo=4` (`pre[4]=8`) | **2** | **2** |

Return **2** — indices 4..5, `[4, 3]`. ✓ Same answer as EP22, arrived at from the
other end.

## ✅ Solution — prefix sums + binary search
```python
import bisect

class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        """Prefix sums + binary search. O(n log n) -- the instructive solution.

        Time:  O(n log n) — one binary search per index.
        Space: O(n) — the prefix array.
        """
        n = len(nums)
        pre = [0] * (n + 1)
        for i, value in enumerate(nums):
            pre[i + 1] = pre[i] + value        # pre is increasing BECAUSE values > 0

        best = float('inf')
        for hi in range(1, n + 1):
            need = pre[hi] - target
            # largest index lo < hi with pre[lo] <= need
            lo = bisect.bisect_right(pre, need, 0, hi) - 1
            if lo >= 0:
                best = min(best, hi - lo)

        return 0 if best == float('inf') else best
```
**Time:** O(n log n) · **Space:** O(n)

### And the one from EP22, for comparison
```python
lo = window_sum = 0
best = float('inf')
for hi, value in enumerate(nums):
    window_sum += value
    while window_sum >= target:
        best = min(best, hi - lo + 1)
        window_sum -= nums[lo]; lo += 1
return 0 if best == float('inf') else best
```
**O(n) time, O(1) space.** Strictly better on both axes. Put the two side by side on
screen — that image is the episode.

## 🧨 The follow-up: what if negatives are allowed?
Change the problem to *"array may contain negative numbers."* Then:

| | Sliding window | Prefix + binary search |
|---|---|---|
| Still correct? | **No** | **No** |
| Why not | shrinking can *increase* the sum, so the left pointer can't move forward permanently | `pre` is no longer sorted, so binary search is meaningless |

Concretely: `nums = [10, -5, 5]`, `target = 10`. The window `[10]` is valid at length
1. But at `[10,-5]` the sum drops to 5, so a naive window shrinks past the answer;
and `pre = [0, 10, 5, 10]` is not increasing, so you can't binary search it.

**The correct tool becomes a monotonic deque over the prefix sums** — keep indices whose
prefix values are increasing, pop from the front when a valid window is found, pop from
the back to maintain monotonicity. That's LeetCode 862 (*Shortest Subarray with Sum at
Least K*), rated Hard, and it's the honest answer to the follow-up.

**You do not need to code that today.** You need to be able to say: *"both my solutions
assume positivity; with negatives I'd reach for a monotonic deque over prefix sums."*
That sentence is the entire value of this episode in an interview.

## ⚠️ Gotchas
- **`bisect_right(...) - 1`, searching in `[0, hi)`.** Searching the whole array lets
  `lo` land at or past `hi` and you'd report a zero-length or negative window.
- **The prefix array has `n+1` entries.** `pre[0] = 0` is the empty prefix and it is
  *required* — without it you can't express a window that starts at index 0. (Row
  `hi=4` in the trace uses exactly that.)
- **Length is `hi - lo`, not `hi - lo + 1`.** These are prefix indices, not element
  indices — `pre[hi] − pre[lo]` covers elements `lo .. hi-1`. Mixing the two
  conventions is the off-by-one of Pattern 05, and it is worth being slow and explicit
  about it on camera.
- Don't present this as *the* answer to the original problem. It's O(n log n) where an
  O(n) solution exists. Present it as the second lens, and say so.

## 🎤 Interview talking points
- *"Sliding window is O(n) and strictly better here. I'm showing the prefix-sum version
  because it makes the assumption visible: both are correct only because the values are
  positive."*
- *"The prefix array is sorted precisely because every element is positive. That's the
  same property the sliding window depends on to move its left edge forward
  permanently."*
- *"With negatives, neither works — the standard answer is a monotonic deque over
  prefix sums, LeetCode 862."* ← knowing the name of the harder problem and not
  pretending it's easy is a strong signal.

## 🔗 Transfer
`sum(range) = pre[hi] − pre[lo]` is the whole of **Pattern 05 (Prefix Sum, EP39–44)**,
introduced here early so it's familiar when it arrives. The monotonic-deque idea is
**Pattern 08 (Stack, EP58–66)**. Next episode is the hardest window problem in the
sheet: Minimum Window Substring.

## 📹 Metadata
- **Title:** `Minimum Size Subarray Sum, again — the assumption nobody mentions | Sliding Window #8`
- **Thumbnail:** `WHY IT BREAKS` (amber block)
- **Short:** `[10,-5,5]`, target 10 — "watch both solutions fail," 50s.
