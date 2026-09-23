# EP113 · P12E03 · Check if Array is Sorted   [Easy]

**Pattern:** Recursion and Backtracking · **Link:** https://www.geeksforgeeks.org/problems/check-if-an-array-is-sorted0701/1

---

## 🎬 Hook
> "An array is sorted if its first two elements are in order **and the rest of it is
> sorted.** That's the recursion. The interesting part isn't the code, it's the base
> case: get it one element wrong and the function either crashes on the last index or
> says every array is sorted."

## 📋 Problem, in your words
```
Given an array arr, return True if it is sorted in non-decreasing order
(each element <= the next), otherwise False.

Equal neighbours are allowed. Solve it recursively.
```

## 🔢 The example
```
Input:  [1, 2, 2, 5, 9]   -> True     <- 2, 2 is fine: non-decreasing
Input:  [1, 3, 2, 4]      -> False    <- 3 > 2
Input:  [7]               -> True     <- one element is always sorted
Input:  []                -> True     <- so is none
```

## 🧸 ELI5
> A line of kids is supposed to be shortest to tallest. You're the first kid. You only
> check one thing: "am I no taller than the kid behind me?" If yes, you tap them on the
> shoulder and they check the same thing with the kid behind *them*.
>
> ```
> 1   2   2   5   9
> ✓ → ✓ → ✓ → ✓ → last kid: nobody behind, nothing to check
> ```
>
> The first kid who finds a taller person in front of a shorter one shouts "no!" and
> that answer travels back up the line. Nobody checks more than their own pair.

## 🐌 Brute force (say it, don't type it)
The loop is the real answer and it's short:

```python
return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))
```

O(n) time, O(1) space, no stack. The recursive version is the same comparisons made one
frame at a time. It's here because it's the cleanest example of recursing on an
**index that moves one way**: the shape you'll use in EP115, and the `start` index you'll
use in EP119 and EP120.

## 💡 The pattern reveal
**Signal:** "sorted" is a property of every adjacent pair, so it's "this pair is fine
and the rest is sorted".
**Therefore:** Shape A with an index `i` that advances by one.

| question | answer here |
|---|---|
| smallest input, answered without recursing? | fewer than 2 elements left (`i >= n - 1`) → `True` |
| the early exit? | `arr[i] > arr[i + 1]` → `False` |
| how does i follow from i + 1? | this pair is in order **and** `sorted_from(i + 1)` |

**Key insight: the base case is about pairs, not elements.** The last index has no
neighbour. So the recursion must stop when there's **no pair left** to compare, at
`i == n - 1`, not when `i == n`. Stopping at `i == n` means evaluating
`arr[n - 1] > arr[n]`, which is an `IndexError`.

## 🔍 Dry run: `[1, 3, 2, 4]`, the call stack

| step | stack (top on the right) | i | pair | event |
|---|---|---|---|---|
| 1 | S(0) | 0 | 1, 3 | in order, call S(1) |
| 2 | S(0) S(1) | 1 | 3, 2 | **3 > 2**, returns False |
| 3 | S(0) | | | returns **False** |

## 🔍 Dry run: `[1, 2, 2]`

| step | stack | i | pair | event |
|---|---|---|---|---|
| 1 | S(0) | 0 | 1, 2 | in order, call S(1) |
| 2 | S(0) S(1) | 1 | 2, 2 | equal is allowed, call S(2) |
| 3 | S(0) S(1) S(2) | 2 | - | `i >= n - 1`, no pair left, returns **True** |
| 4 | S(0) S(1) | | | returns True |
| 5 | S(0) | | | returns **True** |

## ✅ Optimal solution
```python
def is_sorted(arr: list[int]) -> bool:
    """True if arr is non-decreasing, checked one adjacent pair per call.

    Time:  O(n), one call per pair.
    Space: O(n), the call stack is up to n - 1 frames deep.
    """
    n = len(arr)

    def sorted_from(i: int) -> bool:
        if i >= n - 1:                 # 0 or 1 elements left: no pair to break it
            return True
        if arr[i] > arr[i + 1]:        # this pair is out of order
            return False
        return sorted_from(i + 1)      # trust the call on the rest

    return sorted_from(0)
```
**Time:** O(n) · **Space:** O(n) call stack

## ⚠️ Gotchas
- **`>`, not `>=`.** Non-decreasing allows equal neighbours. `arr[i] >= arr[i + 1]`
  rejects `[2, 2]`, which is sorted. If the problem says *strictly* increasing, flip it.
- **Base case `i >= n - 1`.** `i == n` walks off the end; `>=` also covers the empty
  array, where `n - 1 = -1` and `0 >= -1` returns True immediately.
- **Don't slice.** `is_sorted(arr[1:])` copies the array each call, O(n²). Same lesson
  as EP112: pass the index.
- **Recursion limit.** 1000 frames by default, so an array of 5000 raises
  `RecursionError`. `sys.setrecursionlimit` is a workaround, not a fix. The loop has no
  limit.

## 🎤 Interview talking points
- *"Sorted means every adjacent pair is in order, so I check one pair and trust the call
  on the rest."*
- *"The base case is 'no pair left', which is i at n minus 1, not i at n; otherwise I'd
  index past the end."* ← say this as you type the base case.
- *"Non-decreasing, so equal neighbours pass: I test `>`, not `>=`."*
- *"O(n) time and O(n) stack. The iterative version is O(1) space and it's what I'd
  use for real input sizes."*

## 🔗 Transfer
The one-directional index (`i`, then `i + 1`) is the workhorse of this pattern. EP114
recurses on a **number** instead of an array, and EP115 uses this exact index walk but
has to **build** something on the way back instead of just returning a yes or no.

## 📹 Metadata
- **Title:** `Is it sorted? The base case that crashes | Recursion #3`
- **Thumbnail:** `i == n  💥` vs `i == n - 1 ✓`
- **Short:** the line of kids tapping shoulders, the "no!" travelling back. 35s.
