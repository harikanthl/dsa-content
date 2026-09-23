# EP084 · P10E14 · H-Index II   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/h-index-ii/description/

---

## 🎬 Hook
> "The definition of h-index sounds like you need to try every h. But the array is
> sorted, so at every index you can read off **how many papers have at least this many
> citations**: it's just `n - i`. Compare those two numbers and the question flips once.
> That's `lower_bound` with a disguise on."

## 📋 Problem, in your words
```
citations[i] is how many times paper i was cited; the array is sorted ascending.
The h-index is the largest h such that at least h papers have
at least h citations each.

Return it in O(log n).
```

## 🔢 The example
```
Input:  citations = [0, 1, 3, 5, 6]
Output: 3
Why:    3 papers (3, 5, 6) have >= 3 citations.
        4 papers would need >= 4 each, but only 5 and 6 qualify.

Input:  [1, 2, 100]  -> 2
Input:  [0]          -> 0
Input:  [100]        -> 1   (h can't exceed the number of papers)
```

## 🧸 ELI5
> Line the papers up from least cited to most cited. Stand at any paper and look right.
> Everyone from you to the end of the line has **at least your** citation count, because
> the line is sorted. So you can ask one question at each spot:
>
> ```
> index i:           0   1   2   3   4
> citations[i]:      0   1   3   5   6
> papers from here:  5   4   3   2   1      <- that's n - i
> citations >= papers from here?
>                    no  no  YES YES YES
> ```
>
> The first YES is at index 2, and from there `n - i = 3` papers each have at least 3
> citations. That's the h-index.

## 🐌 Brute force (say it, don't type it)
Try every h from `n` down to 0 and count papers with at least h citations. **O(n²)**,
or O(n) if you notice the sorted order and scan once from the left for the first
`citations[i] >= n - i`. The O(n) scan is honestly fine, but the problem says log n, and
the scan is already a monotonic predicate being checked left to right. Halve it.

## 💡 The pattern reveal
**Signal:** "sorted" · "O(log n)" · a definition phrased as "at least h … at least h".
**Therefore:** Shape A with a custom predicate, the bridge into Shape C.

**Key insight:** at index `i`, exactly `n - i` papers have at least `citations[i]`
citations. The predicate `citations[i] >= n - i` is **false, false, true, true, true**:
as `i` grows the left side goes up and the right side goes down, so once true it stays
true. Find the first true with the lower-bound template; the answer is `n - lo`.

```python
if citations[mid] >= n - mid:
    hi = mid          # mid qualifies; the first qualifier is here or left
else:
    lo = mid + 1
```

**Two readings, same code (the point of the episode):**

| reading | what you search | predicate |
|---|---|---|
| Shape A | an **index** in the sorted array | `citations[i] >= n - i` |
| Shape C | the **answer** `h` in `[0, n]` | "at least h papers have ≥ h citations" |

`h = n - i`, so searching one is searching the other in reverse.

## 🔍 Dry run: `[0, 1, 3, 5, 6]`, `n = 5`
Half-open: `lo = 0`, `hi = n = 5` (`hi == n` would mean "no paper qualifies", h = 0).

| step | lo | hi | mid | citations[mid] | n - mid | ≥ ? | action |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 5 | 2 | 3 | 3 | ✓ | `hi = 2` |
| 2 | 0 | 2 | 1 | 1 | 4 | ✗ | `lo = 2` |
| - | 2 | 2 | stop | | | | h = `5 - 2` = **3** ✓ |

Two probes for five papers. Step 1 landed on the answer immediately, and the template
still checked the left side to be sure it was the *first* true.

## ✅ Optimal solution
```python
class Solution:
    def hIndex(self, citations: List[int]) -> int:
        """Largest h with at least h papers cited at least h times; input sorted.

        Time:  O(log n), one lower-bound search over the indices.
        Space: O(1).
        """
        n = len(citations)
        lo, hi = 0, n                       # hi == n means no index qualifies -> h = 0
        while lo < hi:
            mid = (lo + hi) // 2
            if citations[mid] >= n - mid:   # n - mid papers have >= citations[mid] each
                hi = mid
            else:
                lo = mid + 1
        return n - lo
```
**Time:** O(log n) · **Space:** O(1)

## ⚠️ Gotchas
- **Return `n - lo`, not `citations[lo]`.** In `[0, 1, 3, 5, 6]` they happen to both be
  3. In `[1, 2, 100]` the first qualifier is index 1 with value 2, and `n - 1 = 2` is
  right; but `[0, 4, 4]` gives index 1, value 4, and the answer is `n - 1 = 2`. Test it.
- **`hi = n`, not `n - 1`.** `[0, 0, 0]` has no qualifying index, and the loop has to be
  able to say so by ending at `lo = 3`, giving h = 0.
- **`>=`, not `>`.** "At least h citations" includes exactly h.
- **h is capped at n.** `[100]` is 1, not 100. The `n - i` side enforces it for free.

## 🎤 Interview talking points
- *"Sorted means at index `i` there are exactly `n - i` papers with at least
  `citations[i]` citations. So I'm looking for the first `i` where
  `citations[i] >= n - i`."*
- *"That predicate is monotonic: the left side only rises and the right side only
  falls, so it flips from false to true once."*
- *"It's lower_bound with a predicate instead of a target. Equivalently, it's a search
  over h in `[0, n]`, the same thing read backwards."*
- *"H-Index I, unsorted, is a counting-sort O(n) problem. Sorted is what buys log n."*

## 🔗 Transfer
EP83 was the first maximise; this one is back to "first true", but the predicate talks
about the answer (`n - i`) rather than a stored target. That's exactly the jump Shape C
makes all the way: tomorrow's EP85, Maximum Candies, has no index at all, only a range
of answers and a check.

## 📹 Metadata
- **Title:** `H-Index II, lower_bound in disguise | Binary Search #14`
- **Thumbnail:** `c[i] >= n - i` (green block)
- **Short:** the "papers from here" row appearing under the array, then the first YES. 35s.
