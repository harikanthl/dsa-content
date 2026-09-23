# EP027 · P03E07 · Longest Subarray with Ones after Replacement   [Hard]

**Pattern:** Sliding Window · **Link:** https://leetcode.com/problems/max-consecutive-ones-iii/

---

## 🎬 Hook
> "Yesterday's problem had a variable we had to argue was safe despite being stale.
> Today the alphabet shrinks to two symbols, and that entire argument disappears,
> because now you can just count the zeros. Same window, no defending required."

## 📋 Problem, in your words
```
Given a binary array and a number k,
you may flip at most k ZEROS to ones.

Return the length of the longest run of consecutive 1s you can produce.
```

## 🔢 The example
```
Input:  nums = [1,1,1,0,0,0,1,1,1,1,0],  k = 2
Output: 6

  index:   0  1  2  3  4  5  6  7  8  9 10
  value:   1  1  1  0  0  0  1  1  1  1  0
                       ^-----------------^
                       window 4..9, two zeros in it

Why:    the window at indices 4..9 is [0,0,1,1,1,1] -- exactly two zeros,
        so both can be flipped, giving six consecutive 1s. Length 6.

Input:  nums = [1,1,1,0],  k = 0
Output: 3        (no flips allowed -- just the longest existing run)
```

Say the answer as a window, not as a picture: **indices 4–9, containing exactly two
zeros, length 6.** That framing is the solution.

## 🧸 ELI5
> You're walking along a line of lights, some on and some off, and you have **k
> batteries**. Each battery turns one dead light on.
>
> Keep walking right. Every time you pass a dead light, spend a battery. When you run
> out, you have to move your starting point forward, and you only get a battery back
> when a **dead** light drops off the left end.
>
> The longest stretch you ever hold is the answer.

## 🐌 Brute force (say it, don't type it)
Every start index, walk right counting zeros, stop when the count passes k.
**O(n²).** Same redundancy as the rest of the pattern.

## 💡 The pattern reveal
**Signal:** contiguous · longest · "change at most k things."
**Therefore:** Sliding Window, Shape B.

**Key insight:** with only two symbols, *"how many characters must I replace?"* has a
direct answer, **the number of zeros in the window**: so there's nothing to
approximate and nothing to keep stale. The validity test is simply `zeros <= k`.

**The reframe worth saying out loud:** the problem is not "flip k zeros." It is
**"find the longest window containing at most k zeros."** Flipping is a story; the
window condition is the algorithm. (Same translation habit as EP24.)

**Relationship to EP26:** this is exactly yesterday's problem with an alphabet of size
2, where `max_count` = count of ones, and
`length − max_count = length − ones = zeros`. The messy version becomes the clean one.
Put both validity tests on screen together:

```
EP26:  (hi - lo + 1) - max_count  <=  k        # "how many aren't the winner"
EP27:               zeros         <=  k        # the same thing, two symbols
```

## 🔍 Dry run: `[1,1,1,0,0,0,1,1,1,1,0]`, k = 2
| hi | val | zeros | zeros ≤ 2? | action | window (lo..hi) | len | best |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 0 | ✓ | | 0..0 | 1 | 1 |
| 1 | 1 | 0 | ✓ | | 0..1 | 2 | 2 |
| 2 | 1 | 0 | ✓ | | 0..2 | 3 | 3 |
| 3 | 0 | 1 | ✓ | | 0..3 | 4 | 4 |
| 4 | 0 | 2 | ✓ | | 0..4 | 5 | 5 |
| 5 | 0 | 3 | ✗ | drop `nums[0]`=1 → 1..5, still 3 ✗; drop 1 → 2..5, still 3 ✗; drop 1 → 3..5, still 3 ✗; drop **0** → zeros 2 ✓, lo=4 | 4..5 | 2 | 5 |
| 6 | 1 | 2 | ✓ | | 4..6 | 3 | 5 |
| 7 | 1 | 2 | ✓ | | 4..7 | 4 | 5 |
| 8 | 1 | 2 | ✓ | | 4..8 | 5 | 5 |
| 9 | 1 | 2 | ✓ | | 4..9 | **6** | **6** |
| 10 | 0 | 3 | ✗ | drop `nums[4]`=0 → zeros 2 ✓, lo=5 | 5..10 | 6 | 6 |

Return **6**: the window `4..9`, which is `[0,0,1,1,1,1]` with both zeros flipped.

Row `hi=5` is the teaching moment: **three removals did nothing** because they were all
ones. You only get a battery back when a zero leaves. That's why it's a `while`.

## ✅ Optimal solution
```python
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        """Longest window containing at most k zeros.

        Time:  O(n) amortised, lo only moves forward.
        Space: O(1), one counter.
        """
        lo = 0
        zeros = 0
        best = 0

        for hi, value in enumerate(nums):
            if value == 0:
                zeros += 1                     # spend a battery

            while zeros > k:                   # shrink only while BROKEN
                if nums[lo] == 0:
                    zeros -= 1                 # a battery comes back
                lo += 1

            best = max(best, hi - lo + 1)      # measure AFTER repair

        return best
```
**Time:** O(n) · **Space:** O(1)

### The no-shrink variant (and why it's worth seeing)
```python
lo = 0
for hi, value in enumerate(nums):
    k -= (value == 0)          # spend
    if k < 0:                  # over budget: slide, don't shrink
        k += (nums[lo] == 0)
        lo += 1
return len(nums) - lo
```
Same trick as EP26: the window never shrinks, so its final length is its maximum. It's
four lines and slightly magic. Show it *after* the honest version, and say which one
you'd write in an interview, the readable one, unless asked.

## ⚠️ Gotchas
- **`while`, not `if`** in the honest version. Removing a one doesn't refund anything;
  you may need several removals before a zero leaves. Row `hi=5` proves it.
- **Only decrement `zeros` when the departing element is a zero.** Decrementing
  unconditionally gives you free batteries and a wildly inflated answer.
- **Measure after the while loop**: Shape B. Inside, you'd be measuring invalid
  windows.
- **`k = 0`** reduces to "longest run of consecutive ones," and the same code handles
  it, no special case. Good test.
- **`k >= number of zeros`** returns `len(nums)`. Also no special case.
- The array is binary by the constraints. For a general array with "at most k elements
  not equal to `x`," the identical code works with `value != x`.

## 🎤 Interview talking points
- *"I reframe it as 'longest window with at most k zeros', flipping is a story, the
  window condition is the algorithm."*
- *"This is the k-replacement problem with a two-symbol alphabet, so the most-frequent
  count becomes the count of ones and the validity test simplifies to counting
  zeros."*
- *"O(n) amortised: `lo` only moves forward, so the two pointers do at most 2n steps
  between them."*

## 🔗 Transfer
This closes the "longest window" run (EP23–27), five problems, one skeleton, different
validity tests. Next (EP28) we go back to *shortest* windows and, on the way, look at
the same problem from EP22 through a completely different lens: prefix sums. That's the
bridge into Pattern 05.

## 📹 Metadata
- **Title:** `Max Consecutive Ones III, count the zeros, forget the flips | Sliding Window #7`
- **Thumbnail:** `k BATTERIES` (amber block)
- **Short:** Row `hi=5`, three removals, no refund, "this is why it's a while loop." 45s.
