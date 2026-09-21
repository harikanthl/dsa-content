# EP037 · P04E05 · Maximum Absolute Sum of Any Subarray   [Medium]

**Pattern:** Kadane · **Link:** https://leetcode.com/problems/maximum-absolute-sum-of-any-subarray/

---

## 🎬 Hook
> "The word *absolute* makes this look like a new problem. It isn't — it's a signal
> that you need to look in **both directions at once**. The biggest absolute value is
> either the most positive sum or the most negative one, so run both Kadanes and take
> whichever is further from zero."

## 📋 Problem, in your words
```
Given an integer array, return the maximum ABSOLUTE value of the sum
of any subarray.

|x| is the distance from zero, so a sum of -8 beats a sum of +5.
The empty subarray is allowed here and has sum 0.
```

## 🔢 The example
```
Input:  nums = [1, -3, 2, 3, -4]
Output: 5
Why:    [2, 3] sums to 5.  Also [-3, 2, 3, -4] sums to -2, |−2| = 2. Not better.

Input:  nums = [2, -5, 1, -4, 3, -2]
Output: 8
Why:    [-5, 1, -4] sums to -8, and |−8| = 8 -- the NEGATIVE run wins.
```

That second example is the episode. The answer is a negative sum, and a
maximum-only Kadane never even looks at it.

## 🧸 ELI5
> You're measuring how far a needle swings from centre, and it doesn't matter which
> way it swings — only how far.
>
> So you watch for **two** things: the biggest swing to the right, and the biggest swing
> to the left. At the end, whichever swing was longer is your answer.
>
> Two separate tallies, one pass, no interaction between them.

## 🐌 Brute force (say it, don't type it)
Every subarray, take `abs(sum)`. **O(n²).** Same overlap waste as the rest of the
pattern.

## 💡 The pattern reveal
**Signal:** contiguous subarray · **absolute** value of a sum.
**Therefore:** Kadane run in **both directions**, combined at the end.

**Key insight:** `|s|` is maximised by whichever is extreme — so

```
answer = max( max_subarray_sum , |min_subarray_sum| )
```

These are EP33 and EP34, run simultaneously over the same pass, and never interacting.
Unlike EP35 (where the two states swap roles) and EP36 (where one feeds the other),
here they are genuinely independent. Say that contrast out loud — three consecutive
episodes track two states for three different reasons.

**The one detail that differs from EP33/34:** this problem **allows the empty
subarray**, whose sum is 0. So both running states can be seeded at `0` rather than
`nums[0]` — and here that's correct rather than a bug. The constraint changed, so the
seed changes with it. Read the statement; don't apply the previous episode's rule by
reflex.

**The elegant alternative worth knowing:** with prefix sums,

```
max |sum(i..j)|  =  max(prefix) - min(prefix)
```

because every subarray sum is a difference of two prefix values, and the largest
possible difference is the range of the prefix array. One pass, two variables, no
Kadane at all:

```python
best = lo = hi = 0
running = 0
for x in nums:
    running += x
    hi = max(hi, running); lo = min(lo, running)
return hi - lo
```

Show this second. It's shorter, it's a genuinely different insight, and it's the
natural bridge into Pattern 05.

## 🔍 Dry run — `[2, -5, 1, -4, 3, -2]`
Running both Kadanes, seeded at 0 (empty subarray allowed).

| i | x | `cur_max` | `best_max` | `cur_min` | `best_min` |
|---|---|---|---|---|---|
| 0 | 2 | max(2, 2) = **2** | 2 | min(2, 2) = 2 | 0 |
| 1 | −5 | max(−5, −3) = **−3** | 2 | min(−5, −3) = **−5** | −5 |
| 2 | 1 | max(1, −2) = **1** | 2 | min(1, −4) = **−4** | −5 |
| 3 | −4 | max(−4, −3) = **−3** | 2 | min(−4, −8) = **−8** | **−8** |
| 4 | 3 | max(3, 0) = **3** | **3** | min(3, −5) = **−5** | −8 |
| 5 | −2 | max(−2, 1) = **1** | 3 | min(−2, −7) = **−7** | −8 |

`answer = max(3, |−8|) = ` **8** ✓ — the run `[−5, 1, −4]`.

Note how `best_max` peaked at a modest 3 while `best_min` reached −8. Tracking only the
maximum returns 3, which is wrong by more than a factor of two.

## ✅ Optimal solution
```python
class Solution:
    def maxAbsoluteSum(self, nums: List[int]) -> int:
        """Largest |sum| over all subarrays (the empty one, sum 0, is allowed).

        Time:  O(n) — one pass, two independent Kadanes.
        Space: O(1).
        """
        cur_max = best_max = 0
        cur_min = best_min = 0

        for x in nums:
            cur_max = max(x, cur_max + x)      # ordinary Kadane
            best_max = max(best_max, cur_max)

            cur_min = min(x, cur_min + x)      # mirrored Kadane
            best_min = min(best_min, cur_min)

        return max(best_max, abs(best_min))
```
**Time:** O(n) · **Space:** O(1)

### The prefix-sum version
```python
class Solution:
    def maxAbsoluteSum(self, nums: List[int]) -> int:
        """max |subarray sum| = max(prefix) - min(prefix).

        Every subarray sum is prefix[j] - prefix[i], so the largest possible
        magnitude is the full range of the prefix values.
        """
        running = highest = lowest = 0
        for x in nums:
            running += x
            highest = max(highest, running)
            lowest = min(lowest, running)
        return highest - lowest
```
Same O(n)/O(1), four lines, and a completely different argument. Worth being able to
derive both — an interviewer who's seen the Kadane answer twenty times will sit up for
this one.

## ⚠️ Gotchas
- **Seed at 0 here, because the empty subarray is allowed.** This is the opposite of
  EP33/EP34's rule, and it's the trap: applying the previous episode's seeding advice
  by reflex is wrong. Read the constraint each time. (If a variant forbids the empty
  subarray, seed both at `nums[0]` and the code is otherwise unchanged.)
- **`abs(best_min)`, not `-best_min`,** unless you're certain `best_min ≤ 0`. It is,
  given the 0 seed — but writing `abs` costs nothing and can't be wrong.
- **The two Kadanes must not share state.** Unlike EP35, there is no swapping. If you
  find yourself writing `if x < 0: swap`, you've imported the wrong episode.
- In the prefix version, **`highest` and `lowest` both start at 0**, representing the
  empty prefix — exactly the same role `pre[0] = 0` plays in EP28.
- Don't compute `max(abs(x) for subarray sums)` by taking `abs` inside the loop; `abs`
  is not compatible with the running recurrence and you'll get nonsense. Take it once,
  at the end.

## 🎤 Interview talking points
- *"The largest magnitude is either the most positive sum or the most negative one, so
  I run Kadane both ways in one pass and take whichever is further from zero."*
- *"There's a neater argument: every subarray sum is a difference of two prefix sums,
  so the answer is `max(prefix) − min(prefix)`. Four lines and no Kadane."* ← this is
  the answer that gets remembered.
- *"The empty subarray is allowed here, so I seed at zero — which is the opposite of
  what I'd do on plain Maximum Subarray."*

## 🔗 Transfer
The prefix-sum framing here is a direct trailer for **Pattern 05 (EP39–44)**, where
"every range sum is a difference of two prefix values" is the entire pattern. Tomorrow
(EP38) closes Kadane with the circular variant, which also needs both the maximum and
minimum subarray — so today's two-Kadane pass gets reused immediately.

## 📹 Metadata
- **Title:** `Maximum Absolute Sum — run Kadane both ways | Kadane #5`
- **Thumbnail:** `BOTH DIRECTIONS` (green block)
- **Short:** `max(prefix) − min(prefix)` in four lines, as the "wait, that's it?" reveal. 45s.
