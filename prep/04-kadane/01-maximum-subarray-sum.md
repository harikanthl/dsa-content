# EP033 · P04E01 · Maximum Subarray Sum   [Medium]

**Pattern:** Kadane · **Link:** https://leetcode.com/problems/maximum-subarray/

---

## 🎬 Hook
> "One question, asked once per element: *is what I'm carrying helping me, or should I
> drop it and start here?* That's the entire algorithm. It's four lines, it's O(n), and
> the reason people still get it wrong is a single initial value."

## 📋 Problem, in your words
```
Given an integer array (it may contain negatives),
find the contiguous subarray with the largest sum, and return that sum.

The subarray must be non-empty -- at least one element.
```

## 🔢 The example
```
Input:  nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
Output: 6
Why:    [4, -1, 2, 1] sums to 6, and nothing does better.

Input:  nums = [-3, -1, -2]
Output: -1        <- NOT 0. An empty subarray is not allowed,
                     so the answer is the least-bad single element.
```

Put the all-negative example on screen from the start. It's the case that separates a
working solution from one that merely passes the first test.

## 🧸 ELI5
> You're walking along the array with a running score, and at every step you ask one
> question: **is my score helping me?**
>
> If you're carrying +7 and the next number is −1, keep going — you're at +6, still
> better than starting over at −1.
>
> If you're carrying −4 and the next number is 2, **drop the −4**. Nothing you add to a
> negative pile is as good as just starting fresh. Carrying it forward can only make
> every future total worse.
>
> Write down the best score you've ever held. That's the answer.

## 🐌 Brute force (say it, don't type it)
Every start, every end, sum it.

```python
best = nums[0]
for i in range(len(nums)):
    total = 0
    for j in range(i, len(nums)):
        total += nums[j]
        best = max(best, total)
```

**O(n²).** (The truly naive version with an inner `sum()` is O(n³) — worth mentioning
as the thing *not* to write.) The waste: the subarray starting at `i+1` is the one
starting at `i` minus one element, and this learns nothing from that.

There's also a **divide and conquer** solution at O(n log n) — split, solve both halves,
and handle the subarray crossing the middle. It's a genuinely nice answer and worth
naming, because the follow-up on LeetCode explicitly asks for it. But it's beaten by
the linear scan.

## 💡 The pattern reveal
**Signal:** contiguous subarray · maximum sum · **negatives present**.
**Therefore:** Kadane.

**Key insight:** define `current` = *the best subarray sum that **ends exactly at this
index***. Then, for the next element `x`, there are only two candidates:

- extend the previous best run: `current + x`
- start a brand-new run at `x`: just `x`

Take the larger. One comparison, no memory of anything else.

```python
current = max(x, current + x)
```

**And the second quantity:** `best` = the largest `current` you've ever seen. These are
*different things*, and conflating them is the classic bug. `current` can fall; `best`
never does.

**Why dropping a negative prefix is always right:** if `current < 0`, then for any
future element `x` we have `current + x < x`. Keeping it is strictly worse, always. No
cleverness needed — it's an inequality.

## 🔍 Dry run — `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`
Seed: `current = best = -2`.

| i | x | `current + x` | `x` | `current` = max | `best` |
|---|---|---|---|---|---|
| 1 | 1 | −1 | 1 | **1** (start fresh) | 1 |
| 2 | −3 | −2 | −3 | **−2** (extend) | 1 |
| 3 | 4 | 2 | 4 | **4** (start fresh) | 4 |
| 4 | −1 | 3 | −1 | **3** (extend) | 4 |
| 5 | 2 | 5 | 2 | **5** (extend) | 5 |
| 6 | 1 | 6 | 1 | **6** (extend) | **6** |
| 7 | −5 | 1 | −5 | **1** (extend) | 6 |
| 8 | 4 | 5 | 4 | **5** (extend) | 6 |

Return **6** — the run `[4, −1, 2, 1]`, which is exactly the stretch where `current`
climbed from 4 to 6.

Look at rows 1 and 3: both times the running total had gone negative, so the algorithm
threw it away. Those two rows are the algorithm.

## ✅ Optimal solution
```python
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        """Largest sum of any non-empty contiguous subarray.

        Time:  O(n) — one pass, one comparison per element.
        Space: O(1) — two integers.
        """
        best = current = nums[0]           # seed with a REAL element, never 0

        for x in nums[1:]:
            current = max(x, current + x)  # abandon the past, or extend it
            best = max(best, current)      # best subarray ANYWHERE so far

        return best
```
**Time:** O(n) · **Space:** O(1)

### If they also want the indices
```python
best = current = nums[0]
start = best_start = best_end = 0
for i, x in enumerate(nums[1:], 1):
    if x > current + x:
        current, start = x, i          # a new run begins here
    else:
        current = current + x
    if current > best:
        best, best_start, best_end = current, start, i
```
Worth having ready — interviewers often follow up with *"now return the subarray
itself."* The only new idea is remembering where the current run started.

## ⚠️ Gotchas
- **Seed with `nums[0]`, never `0`.** On `[-3, -1, -2]` a zero seed returns `0`, which
  corresponds to the empty subarray — not allowed. **This is the bug of the episode.**
  Write the zero version first on camera, run the all-negative test, watch it fail.
- **`current` and `best` are different variables with different meanings.** `current`
  is "ending here"; `best` is "anywhere". Using one variable returns the sum of the
  final run instead of the maximum.
- **Update `best` after `current`,** every iteration — not only when you extend.
- **Empty input.** `nums[0]` raises `IndexError`. LeetCode guarantees at least one
  element; a production function should say what it does.
- If a variant *does* allow the empty subarray, the answer is `max(best, 0)` — one
  character of difference, so read the statement rather than assuming.
- Don't reach for a sliding window here. With negatives, "shrink from the left while
  the sum is too big" isn't a valid move — see the EP28 discussion.

## 🎤 Interview talking points
- *"`current` is the best subarray ending at this index. At each element I either
  extend it or start over, whichever is larger."*
- *"Dropping a negative running total is provably right: if `current < 0` then
  `current + x < x` for every future `x`, so carrying it is strictly worse."*
- *"I seed with the first element rather than zero so all-negative arrays return the
  largest element rather than an empty subarray."*
- *"There's an O(n log n) divide-and-conquer solution — split, recurse, handle the
  crossing subarray — which is what the follow-up asks for, but O(n) beats it."*

## 🔗 Transfer
The next five episodes are all this loop with one thing changed: mirrored to a minimum
(EP34), two states for products (EP35), a second state for a deletion budget (EP36),
both directions at once (EP37), and total-minus-minimum for circular arrays (EP38).
The `current` vs `best` distinction also reappears throughout Pattern 15 (DP), where
it's the difference between a local and a global optimum.

## 📹 Metadata
- **Title:** `Maximum Subarray (Kadane's) — one question per element | Kadane #1`
- **Thumbnail:** `DROP THE NEGATIVE` (green block)
- **Short:** `[-3,-1,-2]` returning 0 instead of −1, then the one-token fix. 40s.
