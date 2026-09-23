# EP021 · P03E01 · Maximum Sum Subarray of Size K   [Easy]

**Pattern:** Sliding Window · **Link:** https://www.geeksforgeeks.org/problems/max-sum-subarray-of-size-k5313/1

---

## 🎬 Hook
> "Every window of size k shares k−1 elements with the one before it. Recomputing that
> overlap is the single most common waste in array problems, and killing it is a
> whole pattern, not a trick. This is the simplest problem in that pattern, so it's
> where the idea is cleanest."

## 📋 Problem, in your words
```
Given an array of positive numbers and a number k,
find the maximum sum of any CONTIGUOUS subarray of exactly size k.
```

## 🔢 The example
```
Input:  nums = [2, 1, 5, 1, 3, 2],  k = 3
Output: 9
Why:    the windows are [2,1,5]=8, [1,5,1]=7, [5,1,3]=9, [1,3,2]=6
        the best is [5,1,3] = 9
```

## 🧸 ELI5
> You're looking at a row of houses through a cardboard tube that shows exactly three
> at a time, and you want the three with the most windows between them.
>
> You could walk back to the start and recount for every position. Or you could just
> **shuffle the tube one house to the right**: house 4 comes into view, house 1 drops
> out. The two houses in the middle didn't change, so why would you recount them?
>
> Add the one that entered. Subtract the one that left. That's the whole algorithm.

## 🐌 Brute force (say it, don't type it)
Two nested loops: for every start index, sum the next k elements.

```python
best = 0
for i in range(len(nums) - k + 1):
    best = max(best, sum(nums[i:i+k]))
```

**O(n·k) time.** The waste is precise and worth naming out loud: consecutive windows
overlap in `k−1` elements, and this re-adds every one of them. For `k = 1000` you do a
thousand additions to learn what two would have told you.

## 💡 The pattern reveal
**Signal:** *contiguous* · *of size k* · a quantity you can update incrementally.
**Therefore:** Sliding Window, Shape A, the fixed window.

**Key insight:** the sum of the next window is the current sum, **plus the element
entering on the right, minus the element leaving on the left**. Two operations per
step instead of k. Nothing else changes, so nothing else needs recomputing.

```
[2, 1, 5, 1, 3, 2]     sum = 8
 ^-----^

[2, 1, 5, 1, 3, 2]     sum = 8 + 1 - 2 = 7
    ^-----^             ^^^^^^^^^^^^  one in, one out
```

## 🔍 Dry run: `[2, 1, 5, 1, 3, 2]`, k = 3
Seed with the first window, then slide.

| hi | entering `nums[hi]` | leaving `nums[hi-k]` | window | sum | best |
|---|---|---|---|---|---|
| - | - | - | `[2,1,5]` | 8 | 8 |
| 3 | 1 | 2 | `[1,5,1]` | 8 + 1 − 2 = 7 | 8 |
| 4 | 3 | 1 | `[5,1,3]` | 7 + 3 − 1 = **9** | **9** |
| 5 | 2 | 5 | `[1,3,2]` | 9 + 2 − 5 = 6 | 9 |

Return **9**. Four windows, three additions and three subtractions, not twelve.

## ✅ Optimal solution
```python
class Solution:
    def maximumSumSubarray(self, nums: List[int], k: int) -> int:
        """Max sum over all contiguous subarrays of exactly size k.

        Time:  O(n), each element is added once and removed once.
        Space: O(1), one running sum.
        """
        if len(nums) < k:
            return 0                       # no window of size k exists

        window_sum = sum(nums[:k])         # seed the first window
        best = window_sum

        for hi in range(k, len(nums)):
            window_sum += nums[hi] - nums[hi - k]   # one in, one out
            best = max(best, window_sum)

        return best
```
**Time:** O(n) · **Space:** O(1)

### The index that trips people
`nums[hi - k]` is the element **leaving**. When `hi = k` (the first slide), that's
`nums[0]`, correct, the first element drops out. Say it as a sentence while you write
it: *"hi is entering, hi minus k is leaving."* Deriving it live beats memorising it,
because the same index shows up in EP30, EP31 and EP32.

## ⚠️ Gotchas
- **Seed the first window before the loop, and start the loop at `k`, not `0`.**
  Starting at 0 makes `nums[hi-k]` a negative index, which in Python silently reads
  from the *end* of the array, no crash, wrong answer. That's the worst kind of bug
  and it's worth showing on camera.
- **Guard `len(nums) < k`.** `sum(nums[:k])` happily returns a short sum and you
  report a window that doesn't exist.
- **This problem states positive numbers, so `best = 0` would survive as an initial
  value. Don't rely on it.** Seed `best` with the first real window instead, then the
  same code is correct when a variant allows negatives. (Same lesson as EP6: seed with
  a real value, never a hopeful one.)
- The sum must be updated *before* comparing to `best`, and `best` compared once per
  window, not inside a nested loop that's secretly still O(n·k).

## 🎤 Interview talking points
- *"Consecutive windows share k−1 elements, so I update the sum in O(1) instead of
  recomputing it in O(k). That's O(n) overall rather than O(n·k)."*
- *"This only works because the window size is fixed and the quantity is reversible,
  I can subtract the departing element. For something like a maximum, subtracting
  isn't possible, and I'd need a monotonic deque instead."* ← this forward reference
  to Pattern 08 makes you sound like someone who's seen the whole map.
- If asked about negatives: *"Nothing changes for a fixed window. It only matters for
  variable windows, where 'add more to get closer' stops being true."*

## 🔗 Transfer
This is the base case for twelve episodes. EP22 makes the window size variable, which
is where the real decisions start. EP30–32 come back to the fixed window with a
frequency map instead of a sum. And the "one in, one out" update is the same idea as
prefix sums in Pattern 05, two different ways of refusing to recompute.

## 📹 Metadata
- **Title:** `Max Sum Subarray of Size K, stop recomputing the overlap | Sliding Window #1`
- **Thumbnail:** `ONE IN, ONE OUT` (amber block)
- **Short:** The tube-over-houses analogy with the +1/−2 arithmetic on screen, 40s.
