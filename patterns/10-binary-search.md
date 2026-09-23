# Pattern 10: Binary Search

**23 episodes · EP 71–93**

---

## The one-sentence version

Whenever you can ask a **yes/no question that flips exactly once** across a range,
false, false, false, **true**, true, true, you can find the flip point by halving the
range instead of walking it: **O(n) → O(log n)**. The array being sorted is just the
most common reason the question flips once; it is not the pattern.

## ELI5

Guess-the-number, but you're the one guessing. Your friend picks a number from 1 to 100
and only says "higher" or "lower". You don't start at 1. You say **50**, and whatever
they answer, half the numbers are gone forever. Then 25 or 75. Then half again. Seven
guesses, guaranteed, for a hundred numbers; twenty guesses for a million.

The trick works because "is the secret bigger than my guess?" is **no, no, no, yes, yes,
yes** as your guess goes up. It switches once. Every guess tells you which side of the
switch you're on.

Now notice: nothing about that required a *sorted array*. It required a **question that
switches once**. "Can Koko finish the bananas eating at speed `x`?" is no, no, no, yes,
yes, yes as `x` grows. Same game, same seven guesses. That realisation, that the thing
you binary search over can be **the answer itself**: is what turns this from a
first-week technique into one you use on hard problems.

## How to recognise it

| Signal | Example |
|---|---|
| "**sorted** array", "find / insert position" | Binary search basic (EP71), Ceiling (EP72) |
| "first / last occurrence", "count of x" | First and Last Position (EP73), Count Occurrences (EP74) |
| "**rotated** sorted array", "mountain array", "peak" | EP76–80 |
| "**minimum** speed / capacity / days / pages such that…" | Koko (EP81), Ship Packages (EP86), Book Allocation (EP87) |
| "**maximum** distance / candies such that…" | Aggressive Cows (EP83), Candies (EP85) |
| the constraints say n ≤ 10⁵ but the answer range is ≤ 10⁹ | any Shape C problem, n log(range) is the intended complexity |
| "kth smallest" in something sorted in **two directions** | Kth Smallest in Sorted Matrix (EP91), Multiplication Table (EP92) |
| "median of two sorted arrays" in O(log) | EP93 |

**The tell for Shape C specifically:** the problem asks for the *smallest x such that*
or *largest x such that* and checking a single candidate `x` is easy (a linear scan).
If you can write `feasible(x)` in five lines and it's monotonic, you're done thinking.

**The anti-signal:** the predicate does **not** flip exactly once. An unsorted array
with "find the target", the question "is target to my left?" has no monotonic answer,
so binary search is simply invalid. That's a hash map or a linear scan. If you can't
argue *why* the predicate is monotonic, don't binary search.

## The three shapes (and a fourth)

### Shape A: Lower bound on a sorted array

Learn **one** template and derive everything from it. `lower_bound(x)` returns the index
of the first element `>= x`, or `n` if none. Half-open: `lo` is a valid answer, `hi` is
"one past the end".

```python
def lower_bound(arr, x):
    lo, hi = 0, len(arr)          # answer is in [lo, hi]; hi == n means "not found"
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            lo = mid + 1          # mid is too small; everything <= mid is out
        else:
            hi = mid              # mid COULD be the answer; keep it
    return lo                     # lo == hi: the first index with arr[i] >= x
```

Everything in EP71–75 is a one-liner on top of it:

| want | write |
|---|---|
| exact match (EP71) | `i = lower_bound(x)`; found iff `i < n and arr[i] == x` |
| ceiling / upper bound (EP72) | `lower_bound(x)` for ceiling; `lower_bound(x + 1)` for first element `> x` |
| first position (EP73) | `lower_bound(x)` |
| last position (EP73) | `lower_bound(x + 1) - 1` |
| count of x (EP74) | `lower_bound(x + 1) - lower_bound(x)` |
| infinite array (EP75) | first find `hi` by **doubling** (1, 2, 4, 8 … until `arr[hi] >= x`), then lower_bound on `[hi//2, hi]` |

**Why it's correct:** the invariant is "the answer is in `[lo, hi]`". When `arr[mid] < x`
the answer can't be at or before `mid`, so `lo = mid + 1` keeps the invariant. When
`arr[mid] >= x`, `mid` itself might be the answer, so `hi = mid`, never `mid - 1`. The
range shrinks by at least one each step, so it terminates; when `lo == hi` there's one
candidate left and the invariant says it's the answer.

### Shape B: Search on a condition, not a value

The array isn't sorted, but **some predicate over indices is monotonic**. Find the
predicate, then it's Shape A.

**Mountain / peak (EP76, EP77):** the predicate is `arr[mid] < arr[mid + 1]`, "am I
still climbing?" That's true, true, true, false, false. The peak is the first `false`.

```python
lo, hi = 0, len(arr) - 1
while lo < hi:
    mid = (lo + hi) // 2
    if arr[mid] < arr[mid + 1]:
        lo = mid + 1      # still climbing; peak is to the right
    else:
        hi = mid          # descending or at peak; peak is here or left
return lo
```

**Rotated sorted array (EP78, EP79, EP80):** the predicate is `arr[mid] > arr[hi]`,
"am I in the left (rotated-up) half?" True, true, false, false. The minimum (EP78) is
the first `false`. The rotation count (EP79) is that same index. For search (EP80),
compare `arr[mid]` with `arr[lo]` to decide **which half is sorted**, then check whether
the target lies inside the sorted half, if yes, go there; if no, go to the other.

```
[4, 5, 6, 7, 0, 1, 2]   target 0
 lo       mid      hi
arr[lo]=4 <= arr[mid]=7  -> left half [4..7] is sorted
is 0 in [4, 7]?  no      -> go right
```

One comparison to find the sorted half, one range check. That's the whole episode.

### Shape C: Binary search on the answer

The problem asks for **the smallest (or largest) x such that `feasible(x)`**. You don't
search an array at all. You search the **range of possible answers**.

```python
def min_feasible(lo, hi, feasible):        # smallest x in [lo, hi] with feasible(x) True
    while lo < hi:                          # feasible is False...False True...True
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid                        # mid works; try smaller
        else:
            lo = mid + 1                    # mid fails; need bigger
    return lo
```

Three decisions, in this order, every time:

| decision | ask | example |
|---|---|---|
| **what is `x`?** | the quantity being minimised/maximised | Koko: eating speed. Ship: capacity. Cows: min gap. |
| **what is `feasible(x)`?** | a greedy O(n) check, "with this x, can I do it?" | Koko: `sum(ceil(p / x)) <= h`. Ship: greedily fill days, count `<= d` |
| **what is the range?** | pull `lo` and `hi` **from the data**, not from `int max` | Koko: `[1, max(piles)]`. Ship: `[max(w), sum(w)]`. Cows: `[1, max - min]` |

**Min vs max.** Koko, bouquets (EP82), ship (EP86), books (EP87), split array (EP88) are
*minimise x, feasible is monotone increasing* → the template above. Aggressive Cows
(EP83), candies (EP85) are *maximise x, feasible is monotone **de**creasing* (bigger
gap → harder to place cows). Flip the branches: `if feasible(mid): lo = mid` and
`else: hi = mid - 1`, with `mid = (lo + hi + 1) // 2` so it terminates. Or negate and
reuse the template. Pick one and never improvise it live.

**H-Index II (EP84)** is the bridge between Shape A and C: the array is sorted and the
predicate is `citations[i] >= n - i`. Both readings work; noticing that is the episode.

### Shape D: Two dimensions and "kth smallest"

**Search a 2-D Matrix (EP89):** rows sorted, each row starts after the previous ends →
it's a sorted 1-D array in disguise. Index `k` maps to `matrix[k // cols][k % cols]`.
Shape A, one line of arithmetic.

**Search a 2-D Matrix II (EP90):** rows and columns sorted independently, but the
flattening trick fails. Start at the **top-right** corner: if the cell is too big, move
left; too small, move down. Each step eliminates a row or a column → O(m + n). This is
the *staircase* and it is technically two pointers, not binary search, knowing that is
the point of the episode.

**Kth Smallest in Sorted Matrix (EP91) / Multiplication Table (EP92):** Shape C on the
**value**, not the index. `feasible(x)` = "are there at least k values `<= x`?", and
counting them uses the staircase (EP91) or `sum(min(x // i, n))` per row (EP92) in
O(n). Range: `[matrix[0][0], matrix[-1][-1]]`. Answer: the smallest `x` with count
`>= k`. It is guaranteed to be an actual matrix value, say why in the interview (if
`x` weren't present, `x - 1` would have the same count).

**Median of Two Sorted Arrays (EP93):** binary search on **how many elements to take
from the shorter array** into the left half. The predicate: "is the partition valid?"
(`a[i-1] <= b[j]` and `b[j-1] <= a[i]`). O(log min(m, n)). It's Shape C where `x` is a
cut position, the hardest problem in the pattern and still the same template.

## The three things that go wrong

### 1. `lo < hi` with `hi = mid`, or `lo <= hi` with `hi = mid - 1`: never mix

Two consistent styles exist. The half-open one above (`hi = n`, `lo < hi`, `hi = mid`)
never skips the answer and never loops forever, because `mid < hi` always so `hi = mid`
always shrinks. The closed one (`hi = n - 1`, `lo <= hi`, `hi = mid - 1`) also works,
but only if you return from *inside* the loop or track a `best`. Mix them and you get
either an infinite loop (`lo < hi` with `lo = mid`) or a skipped answer (`hi = mid - 1`
when `mid` was the answer). Trace `[1, 3]` looking for 3 with your template *before*
you trust it:

```
lo=0 hi=2  mid=1 arr[1]=3 >= 3 -> hi=1
lo=0 hi=1  mid=0 arr[0]=1 <  3 -> lo=1
lo=1 hi=1  stop -> 1   correct
```

### 2. Picking the wrong half in rotated arrays

The instinct is to compare `arr[mid]` with `target`. Wrong: in a rotated array that
tells you nothing about direction. Compare `arr[mid]` with `arr[lo]` (or `arr[hi]`) to
find **which half is sorted**, then range-check the target against that half. With
duplicates (`[1, 1, 1, 0, 1]`) even that breaks, `arr[lo] == arr[mid] == arr[hi]`, and
the honest answer is `lo += 1` and O(n) worst case. Say so.

### 3. The predicate isn't monotonic, so the search is meaningless

Binary search on the answer *always compiles*. It returns *something*. If `feasible(x)`
is true, false, true as `x` grows, that something is garbage. Before writing the loop,
say out loud why "bigger `x` makes it easier (or harder)", "more capacity means fewer
days, so if `x` works, `x + 1` works". If you can't say it, the problem isn't Shape C.

## Complexity

| Problem | Time | Space |
|---|---|---|
| Shape A (EP71–75) | O(log n) | O(1) |
| EP75 infinite array | O(log p) where p is the target's position | O(1) |
| Shape B (EP76–80) | O(log n) | O(1) |
| Shape C (EP81–88) | O(n · log(range)), the check is linear, the range is halved | O(1) |
| EP89 flattened matrix | O(log(m·n)) | O(1) |
| EP90 staircase | O(m + n), **not** logarithmic | O(1) |
| EP91, EP92 kth in matrix | O(n · log(max − min)) | O(1) |
| EP93 median | O(log min(m, n)) | O(1) |
| linear scan you're beating | O(n), or O(n · range) for Shape C | - |

## The episodes

| EP | Problem | Family | The thing it teaches |
|---|---|---|---|
| 71 | Binary Search Basic | A | The half-open template. `lo < hi`, `hi = mid`. |
| 72 | Upper Bound / Ceiling | A | `lower_bound(x)` vs `lower_bound(x + 1)`, one template, two answers. |
| 73 | First and Last Position | A | First is `lower_bound(x)`; last is `lower_bound(x + 1) - 1`. |
| 74 | Count Occurrences | A | The difference of two lower bounds. |
| 75 | Search in Infinite Sorted Array | A | Find the right edge by doubling, then search. |
| 76 | Peak Index in Mountain Array | B | The predicate is `arr[mid] < arr[mid + 1]`. |
| 77 | Find Peak Element | B | Same predicate; any peak counts; the edges are walls. |
| 78 | Find Minimum in Rotated Sorted Array | B | Compare to `arr[hi]`; the min is the first non-rotated index. |
| 79 | Number of Rotations | B | EP78's answer *is* the rotation count. |
| 80 | Search in Rotated Sorted Array | B | Find the sorted half, then range-check. |
| 81 | Koko Eating Bananas | C | The first answer-search. `x` = speed, `feasible` = hours ≤ h. |
| 82 | Minimum Days to Make m Bouquets | C | `feasible(day)` counts adjacent runs; impossible case returns −1. |
| 83 | Aggressive Cows | C | **Maximise** x. Flip the branches; `mid` rounds up. |
| 84 | H-Index II | A → C | A sorted array where the predicate is `citations[i] >= n - i`. |
| 85 | Maximum Candies to k Children | C | Maximise again: `sum(c // x) >= k`. |
| 86 | Capacity to Ship Packages in D Days | C | Range from the data: `[max(w), sum(w)]`. |
| 87 | Book Allocation | C | Greedy fill, count partitions. Same as EP86 with a different story. |
| 88 | Split Array Largest Sum | C | EP87 verbatim. Recognising duplicates is a skill. |
| 89 | Search a 2-D Matrix | D | Flatten with `divmod`. |
| 90 | Search a 2-D Matrix II | D | The staircase from top-right. O(m + n), not a binary search. |
| 91 | Kth Smallest in Sorted Matrix | D / C | Search the value; count with the staircase. |
| 92 | Kth Smallest in Multiplication Table | D / C | Search the value; count with `min(x // i, n)`. |
| 93 | Median of Two Sorted Arrays | D / C | Search the cut in the shorter array; two inequalities validate it. |

## What "knowing this in your sleep" means

1. What is the predicate, and why does it flip exactly once? *(Say it before typing.
   "Bigger capacity → fewer days, so feasibility is monotone.")*
2. Which template, `lo < hi` with `hi = mid`, or `lo <= hi` with `hi = mid - 1`? *(Pick
   one for life. Know how it handles "not found".)*
3. Minimise or maximise? *(Minimise: `if feasible: hi = mid`. Maximise: flip the
   branches and round `mid` up.)*
4. Where do `lo` and `hi` come from? *(From the data, `max(piles)`, `sum(weights)`,
   `matrix[-1][-1]`. Never a magic constant.)*
5. Why is the answer to a value-search guaranteed to be a real element? *(If `x`
   weren't present, `x - 1` would have the same count, so `x` wouldn't be minimal.)*
6. When is it *not* binary search? *(Unsorted with no monotonic predicate. The 2-D
   staircase, which is O(m + n) and two pointers.)*
