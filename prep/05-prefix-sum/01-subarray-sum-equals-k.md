# EP039 · P05E01 · Subarray Sum Equals K   [Medium]

**Pattern:** Prefix Sum · **Link:** https://leetcode.com/problems/subarray-sum-equals-k/

---

## 🎬 Hook
> "Count the subarrays that sum to K. The array has negatives, so a sliding window is
> out — growing a window can *shrink* the sum. The fix is one sentence: every subarray
> sum is the difference of two running totals, so instead of hunting for subarrays,
> count **pairs of running totals that differ by K**. A dictionary does that in one
> pass."

## 📋 Problem, in your words
```
Given an integer array nums (values may be negative) and an integer k,
return the TOTAL NUMBER of contiguous subarrays whose sum equals k.

Count them -- not the longest, not whether one exists. Overlapping
subarrays each count separately.
```

## 🔢 The example
```
Input:  nums = [1, 1, 1], k = 2
Output: 2            <- [1,1] at (0,1) and [1,1] at (1,2). They OVERLAP. Both count.

Input:  nums = [1, 2, 3], k = 3
Output: 2            <- [1,2] and [3]

Input:  nums = [3, 4, 7, 2, -3, 1, 4, 2], k = 7
Output: 4            <- [3,4], [7], [7,2,-3,1], [1,4,2]
```
That third one is the dry run below. Note the negative in the middle — that is the
element that rules out a sliding window.

## 🧸 ELI5
> You're walking the array keeping a **running total** of everything behind you.
>
> ```
> nums:         3    4    7    2   -3    1    4    2
> running:  0   3    7   14   16   13   14   18   20
>           ^ the empty prefix
> ```
>
> The sum of any stretch is `running_now − running_back_then`. So if I'm standing on a
> running total of `14` and I want a stretch summing to `7`, I need to have stood on
> `14 − 7 = 7` at some earlier point. **Did I?**
>
> That's not a search. That's a lookup. Keep a tally of every running total you've ever
> stood on, and at each step ask the tally one question:
>
> > *"How many times have I already been at `running − k`?"*
>
> Each of those earlier visits is one subarray ending right here. Add them up.

## 🐌 Brute force (say it, don't type it)
Two loops: fix a start, extend an end, keep the running sum, `count += sum == k`.
**O(n²)** time, O(1) space. It is correct and worth 30 seconds on camera — the O(n)
solution is that same running sum with the inner loop replaced by a dictionary.

## 💡 The pattern reveal
**Signal:** count contiguous subarrays · sum condition · **negatives present**.
**Therefore:** prefix sums + a hash map of counts.

**Key insight:** `sum(nums[a..b]) = pre[b+1] − pre[a]`, so

```
sum(a..b) == k     <=>     pre[a] == pre[b+1] − k
```

Fix the right end `b`, and the number of valid left ends is exactly *the number of
earlier prefixes equal to `running − k`*. One pass, one dictionary.

**🧨 The two traps of this episode.**

1. **Seed the map with `{0: 1}`.** The prefix before the array starts is `0`, and it is
   a real candidate: it's the left end of every subarray that begins at index 0. With
   `seen = {}`, `nums = [3, 4], k = 7` returns **0** instead of 1.
2. **Look up *before* you insert.** If you insert `running` first, then for `k = 0`
   every element matches itself and every count is inflated. Query the past, *then*
   join it.

## 🔍 Dry run — `nums = [3, 4, 7, 2, -3, 1, 4, 2]`, `k = 7`
Start: `seen = {0: 1}`, `running = 0`, `count = 0`.

| i | x | `running` | need `running−7` | found | `count` | `seen` after insert |
|---|---|---|---|---|---|---|
| 0 | 3 | 3 | −4 | 0 | 0 | `{0:1, 3:1}` |
| 1 | 4 | 7 | **0** | **1** | **1** | `{0:1, 3:1, 7:1}` |
| 2 | 7 | 14 | **7** | **1** | **2** | `+ 14:1` |
| 3 | 2 | 16 | 9 | 0 | 2 | `+ 16:1` |
| 4 | −3 | 13 | 6 | 0 | 2 | `+ 13:1` |
| 5 | 1 | 14 | **7** | **1** | **3** | `14:2` ← repeat key |
| 6 | 4 | 18 | 11 | 0 | 3 | `+ 18:1` |
| 7 | 2 | 20 | **13** | **1** | **4** | `+ 20:1` |

Answer **4** ✓

Read the hits back out loud, because this is where the pairing clicks:

- `i=1`: matched the **empty** prefix `0` → the subarray is `[3,4]`. *This is the hit
  that `{0: 1}` exists for.*
- `i=2`: matched prefix `7` (after index 1) → `[7]`.
- `i=5`: matched prefix `7` again → `[7, 2, −3, 1]` = 7. The negative one.
- `i=7`: matched prefix `13` (after index 4) → `[1, 4, 2]`.

And note `14` appearing **twice** in the map at `i=6`. It never got used here, but that
count is why the answer adds rather than flags: two earlier prefixes with the same value
are two distinct subarrays.

## ✅ Optimal solution
```python
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        """Count contiguous subarrays summing to k.

        Time:  O(n) — one pass, O(1) dictionary work per element.
        Space: O(n) — up to n distinct prefix sums.
        """
        seen = {0: 1}                 # the EMPTY prefix, seen once
        running = count = 0

        for x in nums:
            running += x
            # every earlier prefix equal to (running - k) closes a subarray HERE
            count += seen.get(running - k, 0)      # query the past...
            seen[running] = seen.get(running, 0) + 1   # ...then join it

        return count
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **`seen = {0: 1}`, always.** Without it you lose every subarray starting at index 0.
  Test `[3, 4], k = 7` — it's two elements and it catches the bug instantly.
- **Query before insert.** Swap those two lines and `k = 0` double-counts. Trace
  `[0, 0], k = 0` (correct answer: **3** — `[0]`, `[0]`, `[0,0]`).
- **Add, don't flag.** `count += seen[...]`, never `count += 1`. Three earlier prefixes
  with the same value are three separate subarrays.
- **No sliding window.** Say this out loud in the interview before anyone asks. With
  negatives, extending the window can lower the sum, so shrinking from the left proves
  nothing about what's to the right.
- **`k` can be negative, and so can the answer's elements.** Nothing in the algorithm
  cares — which is the point. Don't add an `abs` or a `sort`; sorting destroys
  contiguity.
- **This counts, it doesn't locate.** If the question asks for the longest such
  subarray, the map value becomes the *first index* instead of a count — that's EP42,
  and it's a different map, not a tweak.

## 🎤 Interview talking points
- *"Any subarray sum is a difference of two prefix sums, so I'll count pairs of prefixes
  that differ by k instead of enumerating subarrays."* ← lead with this.
- *"The array has negatives so a sliding window doesn't apply — the sum isn't monotonic
  in the window size."*
- *"I seed the map with `{0: 1}` for the empty prefix, so subarrays starting at index 0
  are counted."* ← volunteer this; it is the line interviewers wait for.
- *"O(n) time, O(n) space. The space is the trade: I'm buying O(1) access to every
  earlier position."*

## 🔗 Transfer
This is the base case of Pattern 05, and EP41 and EP42 are both *this exact code* with
the running value transformed before it goes in the map — remainders in EP41, ±1 in
EP42. Tomorrow (EP40) does the opposite: prefix sums with **no** map at all, to prove
the idea is about the arithmetic and not the dictionary.

## 📹 Metadata
- **Title:** `Subarray Sum Equals K — count pairs, not subarrays | Prefix Sum #1`
- **Thumbnail:** `PRE[b] − PRE[a]` (green block)
- **Short:** the `{0: 1}` seed — `[3,4], k=7` returning 0, then the one-character fix. 45s.
