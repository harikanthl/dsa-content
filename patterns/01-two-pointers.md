# Pattern 01 — Two Pointers

**12 episodes · EP 1–12**

---

## The one-sentence version

When data is **sorted** (or can be treated as if it were), two indices walking the
array under a rule replace a nested loop: **O(n²) → O(n)**.

## ELI5

You're looking for two books on a long shelf whose page counts add to exactly 500.
The shelf is sorted thinnest to thickest.

You put a finger on the thinnest book and a finger on the thickest. Add them.

- Too big? The thick book is too thick. Slide the right finger left.
- Too small? The thin book is too thin. Slide the left finger right.

Every slide **permanently eliminates an entire book** from consideration, because
sorting guarantees everything past it is worse in the same direction. You never
back up. Two fingers, one pass down the shelf.

The naive way is to compare every book against every other book — that's the nested
loop. The sorted order is the free information that lets you skip almost all of it.

## How to recognise it

You are almost certainly looking at Two Pointers when you see:

| Signal | Example |
|---|---|
| The input is **sorted**, and the problem mentions it | "Given a **sorted** array…" |
| Find a **pair / triplet / quadruplet** matching a condition | 2Sum II, 3Sum, 4Sum |
| **In-place** rearrangement with O(1) extra space | Sort Colors, Remove Duplicates |
| Something is compared **from both ends** | Palindromes, Container With Most Water |
| The answer is a **subarray** and the array is all-positive | Subarray Product Less Than K |

**The tell that it is *not* Two Pointers:** unsorted input where you need exact
values → that's a hash map (Two Sum I). Sorting first costs O(n log n), so only sort
if you need order for another reason (like skipping duplicates in 3Sum).

## The three shapes

Nearly every problem in this pattern is one of these.

### Shape A — Opposite ends (converging)
For sorted arrays and palindromes. The window shrinks from both sides.

```python
lo, hi = 0, len(arr) - 1
while lo < hi:
    cur = arr[lo] + arr[hi]
    if cur == target:
        return [lo, hi]
    elif cur < target:
        lo += 1          # need bigger → only the left can grow
    else:
        hi -= 1          # need smaller → only the right can shrink
```

**Why it's correct:** when `cur < target`, `arr[lo]` paired with *anything* at or
below `hi` is still too small. So `lo` can never be part of an answer — discard it
forever. Each step kills one candidate, so the loop runs at most n times.

### Shape B — Fast / slow, same direction (read & write)
For in-place filtering. `slow` marks where the next keeper goes; `fast` scans.

```python
slow = 0
for fast in range(len(arr)):
    if keep(arr[fast]):
        arr[slow] = arr[fast]
        slow += 1
return slow              # length of the cleaned prefix
```

**Mental model:** `slow` is the boundary of the "finished" region. Everything left
of `slow` is final and correct. You are compacting the array in place.

### Shape C — Three regions (Dutch National Flag)
For partitioning into 3 buckets in one pass.

```python
low, mid, high = 0, 0, len(arr) - 1
while mid <= high:
    if arr[mid] == 0:
        arr[low], arr[mid] = arr[mid], arr[low]; low += 1; mid += 1
    elif arr[mid] == 1:
        mid += 1
    else:
        arr[mid], arr[high] = arr[high], arr[mid]; high -= 1   # note: mid does NOT move
```

**The trap everyone hits:** after swapping with `high`, you do *not* advance `mid`.
The value you just pulled in from the right is unexamined. Say this out loud on
camera — it's the whole reason this one is a Medium.

## Complexity you should be able to state cold

| Shape | Time | Space |
|---|---|---|
| A — converging on sorted input | O(n) | O(1) |
| A — after you sort it yourself | O(n log n) | O(1) or O(n) depending on sort |
| B — read/write | O(n) | O(1) |
| C — DNF | O(n) | O(1) |
| kSum (k pointers, sort + nested converge) | O(n^(k−1)) | O(1) extra |

## The episodes

| EP | Problem | Shape | The thing it teaches |
|---|---|---|---|
| 1 | Pair with Target Sum | A | The base case. Why sorted = free elimination. |
| 2 | Rearrange 0 and 1 | B/C | Partitioning with a write pointer. |
| 3 | Remove Duplicates | B | Read/write compaction; the linked-list variant. |
| 4 | Squaring a Sorted Array | A | Negatives make the *largest* value live at the ends. Fill backwards. |
| 5 | Triplet Sum to Zero (3Sum) | A + loop | Fix one, converge on two. Duplicate-skipping. |
| 6 | Triplet Sum Close to Target | A + loop | Track the best-so-far instead of exact match. |
| 7 | Triplets with Smaller Sum | A + loop | Counting, not listing: `hi - lo` counts a whole batch at once. |
| 8 | Subarray Product Less Than K | Window | Monotonic window; counting subarrays ending at `hi`. |
| 9 | Dutch National Flag (Sort Colors) | C | Three regions, one pass, the `mid` trap. |
| 10 | Quadruple Sum (4Sum) | A + 2 loops | Generalising to kSum. Overflow and pruning. |
| 11 | Backspace String Compare | A (reverse) | Two pointers walking *backwards* because backspaces look left. |
| 12 | Minimum Window Sort | A | Scan from both ends to find the first out-of-order element. |

## What "knowing this in your sleep" means

You should be able to answer these without hesitating:

1. Why does `lo += 1` not lose a valid answer? *(Sorted order guarantees every pair
   using `arr[lo]` is ≤ the current sum.)*
2. Why is it O(n) and not O(n²)? *(`lo` and `hi` each move at most n times total,
   and never backwards — so ≤ 2n steps.)*
3. When do you skip duplicates, and where exactly? *(After recording a hit, and on
   the outer fixed index — before the inner loop starts.)*
4. What breaks Two Pointers? *(Unsorted input, or negative numbers in a
   product/sum-window problem — negatives destroy monotonicity, which is why
   Subarray Product Less Than K requires all-positive input.)*
