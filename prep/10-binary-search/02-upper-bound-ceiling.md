# EP072 · P10E02 · Ceiling in a Sorted Array (Upper Bound)   [Easy]

**Pattern:** Binary Search · **Link:** https://www.geeksforgeeks.org/problems/ceil-in-a-sorted-array/1

---

## 🎬 Hook
> "Ceiling, floor, upper bound, lower bound. Four names, and people learn four
> functions. You need **one**. Yesterday's template already returns the ceiling. Change
> `x` to `x + 1` and it returns the upper bound. Subtract one and it's the floor. Same
> eight lines, zero new code."

## 📋 Problem, in your words
```
Given a sorted array (duplicates allowed) and a number x,
return the INDEX of the ceiling of x: the smallest element >= x.

  - if the ceiling appears more than once, return its first index
  - if every element is smaller than x, return -1
```

## 🔢 The example
```
Input:  arr = [1, 2, 8, 10, 11, 12, 19], x = 5
Output: 2              <- arr[2] = 8, the smallest value >= 5

Input:  arr = [1, 2, 8, 10, 11, 12, 19], x = 20
Output: -1             <- nothing is >= 20

Input:  arr = [1, 1, 2, 8, 8, 10], x = 8
Output: 3              <- x itself is present; its FIRST index
```

## 🧸 ELI5
> You're 5 feet tall and walking down a line of doorways sorted from shortest to
> tallest. The **ceiling** is the first doorway you can walk through without ducking.
> The **floor** is the tallest doorway that is no taller than you (one exactly your
> height counts for both).
>
> ```
> doorways:   1   2   8   10   11   12   19
> you (5):          ^ floor = 2
>                       ^ ceiling = 8
> ```
>
> Ceiling and floor are always neighbours. Find one and the other is right next to it.

## 🐌 Brute force (say it, don't type it)
Scan left to right and return the first index with `arr[i] >= x`: **O(n)**. It's
correct, and it's literally the definition of lower bound written as a loop. Binary
search is the same question asked in O(log n).

## 💡 The pattern reveal
**Signal:** "sorted" · "smallest element greater than or equal to".
**Therefore:** Shape A. `lower_bound(x)` **is** the ceiling. Not "can be adapted to",
it is the definition.

**Key insight:** the four named searches are one function called with different
arguments.

| want | definition | code |
|---|---|---|
| **ceiling** (this problem) | first index with `arr[i] >= x` | `lower_bound(x)` |
| **upper bound** (C++ `upper_bound`) | first index with `arr[i] > x` | `lower_bound(x + 1)` |
| **floor** | last index with `arr[i] <= x` | `lower_bound(x + 1) - 1` |
| last index with `arr[i] < x` | the element just before the ceiling | `lower_bound(x) - 1` |

`lower_bound(x + 1)` works because the array holds **integers**: "first element `> x`"
and "first element `>= x + 1`" are the same question. For floats you'd flip the
comparison to `<=` instead.

## 🔍 Dry run: `arr = [1, 2, 8, 10, 11, 12, 19]`, `x = 5`

| step | lo | hi | mid | arr[mid] | compare | action |
|---|---|---|---|---|---|---|
| 1 | 0 | 7 | 3 | 10 | 10 >= 5 | `hi = 3` |
| 2 | 0 | 3 | 1 | 2 | 2 < 5 | `lo = 2` |
| 3 | 2 | 3 | 2 | 8 | 8 >= 5 | `hi = 2` |
| 4 | 2 | 2 | - | - | stop | `2 < 7`, return **2** ✓ |

**Floor for free:** `lower_bound(6)` on the same array runs the identical three steps
(10, 2, 8 are compared against 6 the same way) and lands on 2. Minus one → index 1,
value 2 ✓. The floor is the element just left of where 5 would be inserted.

`x = 20`: every comparison is `<`, `lo` walks to 7 = `n` → **-1** ✓.

## ✅ Optimal solution
```python
def lower_bound(arr: list[int], x: int) -> int:
    """First index i with arr[i] >= x, or len(arr) if there isn't one."""
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < x:
            lo = mid + 1                # mid is too small; drop it
        else:
            hi = mid                    # mid could be the answer; keep it
    return lo


def find_ceil(arr: list[int], x: int) -> int:
    """Index of the first element >= x, or -1.

    Time:  O(log n), one lower_bound.
    Space: O(1).
    """
    i = lower_bound(arr, x)
    return i if i < len(arr) else -1    # n means "past the end": no ceiling


def find_floor(arr: list[int], x: int) -> int:
    """Index of the last element <= x, or -1. The sibling, for free."""
    return lower_bound(arr, x + 1) - 1  # one before the first element > x
```
**Time:** O(log n) · **Space:** O(1)

## ⚠️ Gotchas
- **"Upper bound" means two different things.** In C++ `upper_bound(x)` is the first
  element **strictly greater** than x. Many tutorials (and this episode's title) use
  "upper bound" loosely for the ceiling. Ask which one, then show both lines.
- **First index among duplicates comes free.** `hi = mid` on `>=` keeps pushing left
  through equal values, so `[1, 1, 2, 8, 8, 10]` with x = 8 gives 3, not 4. No extra
  code.
- **`n` is not an index.** `lower_bound` returning `len(arr)` means "no ceiling";
  translate it to -1 before returning.
- **`find_floor` returns -1 naturally** when x is smaller than everything:
  `lower_bound(x + 1)` is 0, minus one is -1. Test `x = 0`.
- **`x + 1` only works for integers.** Say so if the interviewer asks about floats.

## 🎤 Interview talking points
- *"Ceiling is lower bound by definition. The first element `>= x`."*
- *"Upper bound is lower bound of `x + 1`, and floor is that minus one. I don't write
  three functions."*
- *"Duplicates are handled by the template itself: `hi = mid` on equality keeps
  moving left, so I get the first occurrence."*
- *"`lower_bound` returns n when nothing qualifies, which I map to -1."*

## 🔗 Transfer
Two calls to `lower_bound`, `x` and `x + 1`, bracket every copy of `x` in the array.
Tomorrow's EP73, First and Last Position, is exactly that bracket, and EP74 Count
Occurrences is its width. Keep `find_floor` in mind for EP84 H-Index II, where you'll
want "the first index where the condition holds" on a sorted array again.

## 📹 Metadata
- **Title:** `Ceiling, floor, upper bound: one function, three answers | Binary Search #2`
- **Thumbnail:** `x  vs  x + 1` (blue block)
- **Short:** the table of four searches, all one line on top of lower_bound. 35s.
