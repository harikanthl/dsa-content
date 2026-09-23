# EP044 · P05E06 · Count of Range Sum   [Hard]

**Pattern:** Prefix Sum · **Link:** https://leetcode.com/problems/count-of-range-sum/

---

## 🎬 Hook
> "Count the subarrays whose sum lands between `lower` and `upper`. Same opening move as
> every episode this week, it's a question about **pairs of prefix sums**: but the
> condition is a *range*, not an exact value, and a hash map cannot answer a range. This
> is the episode where the dictionary finally runs out, and sorting takes over."

## 📋 Problem, in your words
```
Given an integer array nums and two integers lower and upper, return
the NUMBER of contiguous subarrays whose sum lies in [lower, upper]
inclusive.

Values can be large and negative; the sums overflow 32 bits, which is
a real constraint in C++/Java and a non-issue in Python.
```

## 🔢 The example
```
Input:  nums = [-2, 5, -1], lower = -2, upper = 2
Output: 3
Why:    [-2]      = -2   in range
        [-1]      = -1   in range
        [-2,5,-1] =  2   in range
        ([5] = 5, [-2,5] = 3, [5,-1] = 4 are all too big)

Input:  nums = [0], lower = 0, upper = 0     -> 1
```

## 🧸 ELI5
> Prefix sums again:
>
> ```
> nums:          -2    5   -1
> prefix:   0    -2    3    2
> ```
>
> A subarray's sum is `running_now − some_earlier_prefix`, and you want that difference
> to sit inside `[lower, upper]`:
>
> ```
> lower <= running − earlier <= upper
> ```
>
> Rearrange it so the unknown is alone, this one line is the whole episode:
>
> ```
> running − upper  <=  earlier  <=  running − lower
> ```
>
> So standing at each position you're asking: **"how many of the prefixes I've already
> written down fall inside this window of values?"**
>
> A dictionary answers *"is this exact number present?"*. This question is *"how many
> numbers lie between these two bounds?"*, and for that you need them in **sorted
> order**, not scattered in a hash table. That's the upgrade.

## 🐌 Brute force (say it, don't type it)
All O(n²) pairs of prefixes, count the ones whose difference is in range. Perfectly
correct and it's the baseline; the entire difficulty of this problem is replacing that
inner loop with a counted range query.

## 💡 The pattern reveal
**Signal:** count subarrays · sum in a **range** · negatives.
**Therefore:** prefix sums + an **ordered** structure, sorted list, BIT, or merge sort.

**Key insight:** the inequality rearrangement above. Say it slowly on camera, because
everything else is bookkeeping:

```
lower <= pre[j] - pre[i] <= upper
    <=>    pre[j] - upper <= pre[i] <= pre[j] - lower
```

Two `bisect` calls on a sorted collection of the earlier prefixes give the count
directly, `bisect_right(seen, running - lower) − bisect_left(seen, running - upper)`.
Note which bound gets which: **`upper` produces the lower bound** on `pre[i]`, because
subtracting a larger number gives a smaller result. Getting these crossed is the bug of
the episode, and it is silent, you get a plausible wrong count.

**Which structure?** Both are worth knowing, and they answer different interview moods:

| structure | time | why you'd pick it |
|---|---|---|
| `SortedList` (`sortedcontainers`) + `bisect` | O(n log n) | reads like the idea; not in the stdlib |
| plain list + `insort` | O(n²) worst | fine to *show*, say the `insort` cost out loud |
| **merge sort over the prefix array** | **O(n log n)** | stdlib only, the canonical answer |
| Fenwick tree over compressed values | O(n log n) | when the same query recurs |

**The merge-sort version** counts pairs while merging: for each left-half prefix `p`,
the right-half values satisfying `p + lower <= pre[j] <= p + upper` form a *contiguous
run*, and because both halves are sorted, the two pointers bounding that run only ever
move forward. That's the O(n) merge step, O(n log n) overall.

## 🔍 Dry run: `nums = [-2, 5, -1]`, `lower = -2`, `upper = 2`
Sorted-list version. Start `seen = [0]` (the empty prefix), `running = 0`, `count = 0`.

| i | x | `running` | window `[run−upper, run−lower]` | `seen` before | in window | `count` |
|---|---|---|---|---|---|---|
| 0 | −2 | −2 | `[−4, 0]` | `[0]` | **0** ✓ | **1** |
| 1 | 5 | 3 | `[1, 5]` | `[−2, 0]` | none | 1 |
| 2 | −1 | 2 | `[0, 4]` | `[−2, 0, 3]` | **0, 3** ✓✓ | **3** |

Answer **3** ✓

Read the hits back:

- `i = 0` matched the seeded `0` → the subarray `[−2]`, sum −2, which is exactly
  `lower`. **Inclusive bounds matter**: `bisect_right` on the upper side and
  `bisect_left` on the lower side are what keep an exact-boundary sum counted.
- `i = 2` matched **two** earlier prefixes: `0` (the empty prefix → `[−2, 5, −1] = 2`)
  and `3` (after index 1 → `[−1] = −1`). Two hits, one step, `count += 2`, the same
  "add, don't flag" rule as EP39.

Row `i = 1` is the one to narrate: the window `[1, 5]` sits entirely *above* everything
in `seen`. Nothing matches, and the structure told you so in O(log n) without looking at
the elements one by one. That is the whole reason it's sorted.

## ✅ Solution: sorted list + binary search (the readable one)
```python
from sortedcontainers import SortedList

class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        """Count subarrays whose sum lies in [lower, upper].

        Time:  O(n log n), one insert and two binary searches per element.
        Space: O(n), the sorted prefixes.
        """
        seen = SortedList([0])         # the EMPTY prefix
        running = count = 0

        for x in nums:
            running += x
            # lower <= running - earlier <= upper  <=>  running-upper <= earlier <= running-lower
            count += seen.bisect_right(running - lower) - seen.bisect_left(running - upper)
            seen.add(running)

        return count
```

## ✅ Solution: merge sort (stdlib only, the one to write if asked)
```python
class Solution:
    def countRangeSum(self, nums: List[int], lower: int, upper: int) -> int:
        """Same count, via a counting merge sort over the prefix array.

        Time:  O(n log n) · Space: O(n)
        """
        pre = [0]
        for x in nums:
            pre.append(pre[-1] + x)

        def sort_count(lo: int, hi: int) -> int:
            if hi - lo <= 1:
                return 0
            mid = (lo + hi) // 2
            count = sort_count(lo, mid) + sort_count(mid, hi)

            # both halves are sorted now; i and j only move FORWARD across the whole loop
            i = j = mid
            for p in pre[lo:mid]:
                while i < hi and pre[i] - p < lower:
                    i += 1                     # first index reaching `lower`
                while j < hi and pre[j] - p <= upper:
                    j += 1                     # first index PAST `upper`
                count += j - i

            pre[lo:hi] = sorted(pre[lo:hi])
            return count

        return sort_count(0, len(pre))
```
**Time:** O(n log n) · **Space:** O(n)

## ⚠️ Gotchas
- **`upper` gives the LOWER bound.** `running − upper <= earlier <= running − lower`.
  Cross them and the count is wrong with no error. Re-derive the inequality on camera
  rather than recalling which way round it goes.
- **Inclusive on both ends.** `bisect_left` for the low bound, `bisect_right` for the
  high bound. The example's `[−2]` sum of exactly `lower` is the test that catches it.
- **Seed with the empty prefix `0`.** Fourth episode in a row. Without it, `[0]` with
  `lower = upper = 0` returns 0 instead of 1.
- **`i` and `j` must not be reset inside the merge loop.** They advance monotonically
  across the *whole* left half, that's what makes the step O(n) instead of O(n²). If
  you find yourself writing `i = mid` inside the `for`, you've lost the complexity.
- **Overflow.** Python is immune; C++/Java need `long long` for the prefix sums given
  the stated constraints. Mention it, it's the kind of detail this problem is set to
  probe.
- **`sortedcontainers` is available on LeetCode but is not stdlib.** Say which one
  you're using and why, and have the merge-sort version ready for "without libraries".
- **A plain list with `insort` is O(n) per insert**, so that variant is O(n²) overall.
  It passes small inputs and is a fine thing to *show*, as long as you name the cost
  rather than pretend it's O(n log n).

## 🎤 Interview talking points
- *"It's a pairs-of-prefix-sums problem again, but the condition is a range, so I need
  an ordered structure rather than a hash map."* ← the one sentence the problem is
  testing for.
- *"Rearranged: `running − upper <= earlier <= running − lower`, so per step it's two
  binary searches and an insert."*
- *"With a sorted list that's O(n log n); without libraries I'd count pairs during a
  merge sort, where the two pointers into the right half only move forward."*
- *"Prefix sums can exceed 32 bits here, so in Java or C++ I'd use 64-bit."*

## 🔗 Transfer
This closes Pattern 05, and it closes it on the honest boundary: the prefix insight is
universal, but the lookup structure scales with the question, a dict for equality
(EP39–42), a monotonic deque for a one-sided threshold (EP43), an ordered structure for
a two-sided range (EP44). The merge-sort counting trick returns for inversion counting,
and the Fenwick tree reappears in Pattern 11. Next is **Pattern 06 (Merge Intervals,
EP45–51)**, which leaves running totals behind entirely and sorts by start time instead.

## 📹 Metadata
- **Title:** `Count of Range Sum, when the hash map runs out | Prefix Sum #6`
- **Thumbnail:** `run − upper ≤ earlier ≤ run − lower` (green block)
- **Short:** the rearranged inequality in one shot, then the two bisect calls. 50s.
