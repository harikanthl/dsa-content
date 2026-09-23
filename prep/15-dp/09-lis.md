# EP180 · P15E09 · Longest Increasing Subsequence   [Medium]

**Pattern:** DP (Dynamic Programming) · **Link:** https://leetcode.com/problems/longest-increasing-subsequence/

---

## 🎬 Hook
> "Longest increasing subsequence. The first state everyone writes, 'the LIS of the
> first i numbers', **can't be made to work**. The fix is four words, '**ending exactly
> at i**', and learning to add those words is the most useful state-design trick in DP."

## 📋 Problem, in your words
```
Given an integer array nums, return the length of the longest STRICTLY increasing
subsequence. A subsequence keeps the original order but may skip elements.

1 <= len(nums) <= 2500, values can be negative.
```

## 🔢 The example
```
Input:  nums = [10, 9, 2, 5, 3, 7, 101, 18]
Output: 4
Why:    2, 3, 7, 101   (or 2, 5, 7, 18, or 2, 3, 7, 18)

Input:  nums = [0, 1, 0, 3, 2, 3]  -> 4    (0, 1, 2, 3)
Input:  nums = [7, 7, 7, 7]        -> 1    (strictly: equal doesn't count)
```

## 🧸 ELI5
> Kids line up in a fixed order, and you want the longest group where each kid is
> taller than the one before (you can skip kids, not reorder them).
>
> Ask every kid the same question: **"what's the longest increasing line that ends
> with *you*?"** Each kid answers by looking back at every shorter kid ahead of them in
> the line and saying "I can join the end of *their* best line".
>
> ```
>  heights:     10   9   2   5   3   7   101  18
>  ends here:    1   1   1   2   2   3    4    4
>                            ^ 5 joins 2's line     ^ 101 joins 7's line
> ```
>
> The biggest number anyone says is the answer. It doesn't have to be the last kid.

## 🐌 Brute force (say it, don't type it)
Try every subsequence (2ⁿ), keep the increasing ones, return the longest: **O(2ⁿ · n)**.
Or recursion with "take / skip, and remember the last taken value": correct, but the
state `(i, last_value)` is awkward to memoise. The state below is cleaner.

## 💡 The pattern reveal
**Signal:** the word **subsequence** · "**longest**" · order is fixed, skipping allowed.
**Therefore:** DP, Shape C (LIS: looks back at *every* earlier index).

**Step 1, the state. The obvious one is too small:**

> ~~`f(i)` = the LIS of `nums[0..i]`~~

To extend a subsequence with `nums[i]` you need to know its **last** element, and this
state forgets it. That's pattern-card trap #1: the state can't decide the next step.
Pin the last element down instead:

> `end_at(i)` = length of the longest increasing subsequence that **ends exactly at
> index i** (so `nums[i]` is its last element).

**Step 2, the recurrence.** `nums[i]` can follow any earlier `nums[j]` that's smaller:

```
end_at(i) = 1 + max(end_at(j) for j < i if nums[j] < nums[i])    # or 1 if none
```

**Key insight:** "ending exactly at i" makes every subproblem's last element *known*,
so extending it is a single comparison. The price: the answer is no longer
`end_at(n - 1)`. The best subsequence can end anywhere, so the answer is
**`max(end_at(i) for all i)`**.

## 🔍 Dry run: `nums = [10, 9, 2, 5, 3, 7, 101, 18]`

| i | nums[i] | earlier j with nums[j] < nums[i] (their end_at) | end_at(i) |
|---|---|---|---|
| 0 | 10 | none | **1** |
| 1 | 9 | none (10 is bigger) | **1** |
| 2 | 2 | none | **1** |
| 3 | 5 | j=2: 2 (1) | 1 + 1 = **2** |
| 4 | 3 | j=2: 2 (1) | 1 + 1 = **2** |
| 5 | 7 | j=2: 2 (1), j=3: 5 (2), j=4: 3 (2) | 1 + 2 = **3** |
| 6 | 101 | j=0..5: all smaller, best is j=5: 7 (3) | 1 + 3 = **4** |
| 7 | 18 | j=0: 10 (1), j=1: 9 (1), j=2..5, best is j=5: 7 (3) | 1 + 3 = **4** |

`max` = **4** ✓. Row 7 is the one to point at: 18 is smaller than 101, so it can't
extend that line, but it can start over from 7's line and tie.

## ✅ Optimal solution
```python
from functools import lru_cache


class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        """Length of the longest strictly increasing subsequence.

        end_at(i) = longest increasing subsequence whose LAST element is nums[i].
        Time:  O(n^2), n states, each scanning up to n earlier indices.
        Space: O(n) for the memo and the recursion stack.
        """

        @lru_cache(maxsize=None)
        def end_at(i: int) -> int:
            best = 1                                  # nums[i] alone
            for j in range(i):
                if nums[j] < nums[i]:                 # strictly: equal can't follow
                    best = max(best, end_at(j) + 1)   # join j's line
            return best

        return max(end_at(i) for i in range(len(nums)))   # the best line ends ANYWHERE
```
**Time:** O(n²) · **Space:** O(n)

## ⚠️ Gotchas
- **`max(...)`, not `end_at(n - 1)`.** On the example, `end_at(7)` happens to be 4 too.
  On `[1, 2, 3, 0]`, `end_at(3)` is 1 and the answer is 3. That's the input to test.
- **Strictly means `<`, not `<=`.** `[7, 7, 7, 7]` must return 1. `<=` gives 4, which is
  the longest *non-decreasing* subsequence: a different problem.
- **Subsequence, not subarray.** If it said "longest increasing *subarray*", that's one
  pass with a counter that resets (a Kadane-shaped scan, Pattern 04). The word decides
  the pattern.
- **Recursion depth.** `end_at(2499)` can call `end_at(2498)`... down to 0: 2500 frames,
  over Python's default limit. The memo version is for explaining; the table in EP181
  is what you'd submit.
- **Base case is 1, not 0.** Every element is an increasing subsequence of length 1 on
  its own.

## 🎤 Interview talking points
- *"'LIS of the first i elements' isn't enough, because to extend it I need its last
  element. So I define the state as the longest one ending exactly at i."*
- *"Then end_at(i) is 1 plus the best end_at(j) over earlier, smaller j."*
- *"The answer is the max over all i, since the best subsequence can end anywhere."*
- *"O(n²) time. There's an O(n log n) version with binary search; I'd mention it and do
  it if we have time."* ← that's EP181.

## 🔗 Transfer
"Add *ending exactly here* to the state" is a move you've seen before without the name:
Kadane's `best_ending_here` (EP33) is the same idea on subarrays. It reappears in
Longest String Chain, Largest Divisible Subset and Russian Doll Envelopes. EP181 flips
this memo into a table, finds it **can't** be shrunk to two variables (each cell reads
every earlier cell), and replaces the state entirely to reach O(n log n).

## 📹 Metadata
- **Title:** `LIS, the four words that fix the state ("ending exactly at i") | DP #9`
- **Thumbnail:** `ENDING AT i`
- **Short:** the kids-in-a-line picture, each kid calling out their number, 101 and 18
  both saying 4. 40s.
