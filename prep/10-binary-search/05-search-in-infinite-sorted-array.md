# EP075 · P10E05 · Search in an Infinite Sorted Array   [Medium]

**Pattern:** Binary Search · **Link:** LeetCode 702 (Premium) https://leetcode.com/problems/search-in-a-sorted-array-of-unknown-size/ · GfG article https://www.geeksforgeeks.org/dsa/find-position-element-sorted-array-infinite-numbers/

---

## 🎬 Hook
> "Binary search needs two walls, `lo` and `hi`. What if there's no right wall? You
> can't call `len()` on an infinite array. So before you search, you **find a wall**:
> check index 1, then 2, 4, 8, 16. The doubling is itself logarithmic, so the whole
> thing is still O(log n), where n is where the target lives, not how big the array is."

## 📋 Problem, in your words
```
A sorted array of UNIQUE values, and you don't know its length.
You can only read one element at a time: reader.get(i).
Reading past the real data returns 2^31 - 1, bigger than any real value.

Return the index of target, or -1 if it isn't there.
```
GfG only has this as an article; there's no practice problem to submit to. The judged
version is LeetCode 702, *Search in a Sorted Array of Unknown Size* (Premium), and the
solution below uses its exact interface: `search(self, reader, target)` with an
`ArrayReader` whose `get(i)` returns `2^31 - 1` out of bounds.

## 🔢 The example
```
Input:  arr = [3, 5, 7, 9, 10, 90, 100, 130, 140, 160, 170, ...], target = 10
Output: 4

Input:  same array, target = 8
Output: -1             <- lands between 7 and 9
```

## 🧸 ELI5
> You're on an endless road with numbered houses in increasing order, and you're
> looking for house 10. You can't see the end of the road. So you jog: check the house
> 1 step away, then 2, then 4, then 8, **doubling** each time, until you pass a number
> that's too big.
>
> ```
> index:   1    2    4        <- jumps
> value:   5    7   10        <- 10 >= 10, stop jogging
> ```
>
> Now you know the house is somewhere between your **last two** checkpoints (2 and 4).
> That's a normal street with two ends. Binary search it.
>
> Why doubling and not "+10 each time"? If the house is a million steps away, +10 takes
> a hundred thousand checks. Doubling takes twenty.

## 🐌 Brute force (say it, don't type it)
Read index 0, 1, 2, ... until you hit the target or pass it: **O(p)** where p is the
target's position. It never needs the length, which is the right instinct, but it
ignores that the data is sorted.

## 💡 The pattern reveal
**Signal:** "sorted" · "size unknown / infinite" · access by index only.
**Therefore:** Shape A, with a **doubling phase** to manufacture `hi`.

**Key insight:** exponential search. Double `hi` until `get(hi) >= target`. At that
moment the answer is in `[hi // 2, hi]`, because `get(hi // 2)` was the previous
checkpoint and it was `< target`. Then run the ordinary template on that window.

| phase | loop | cost |
|---|---|---|
| gallop | `hi = 1, 2, 4, 8 ...` while `get(hi) < target` | O(log p) reads |
| search | lower_bound on `[hi // 2, hi]` | O(log p), the window is at most p wide |

The "past the end returns `2^31 - 1`" rule is what makes the gallop safe: running off
the real data just looks like a very big number, which stops the doubling.

## 🔍 Dry run: `arr = [3, 5, 7, 9, 10, 90, 100, ...]`, `target = 10`

**Phase 1: gallop**

| hi | get(hi) | `< 10`? | action |
|---|---|---|---|
| 1 | 5 | yes | `hi = 2` |
| 2 | 7 | yes | `hi = 4` |
| 4 | 10 | no | stop. Window is `[4 // 2, 4]` = `[2, 4]` |

Half-open, so the search runs on `lo = 2`, `hi = 5`.

**Phase 2: lower_bound on `[2, 5)`**

| step | lo | hi | mid | get(mid) | action |
|---|---|---|---|---|---|
| 1 | 2 | 5 | 3 | 9 (< 10) | `lo = 4` |
| 2 | 4 | 5 | 4 | 10 (>= 10) | `hi = 4` |
| - | 4 | 4 | | | `get(4) == 10` → **4** ✓ |

Three reads to gallop, three to search and confirm. In a test with a target about
390,000 places in, the whole thing took 39 reads.

## ✅ Optimal solution
```python
# """
# This is ArrayReader's API interface.
# You should not implement it, or speculate about its implementation
# """
# class ArrayReader:
#    def get(self, index: int) -> int:

class Solution:
    def search(self, reader: 'ArrayReader', target: int) -> int:
        """Index of target in a sorted array of unknown length, or -1.

        reader.get(i) returns arr[i], or 2^31 - 1 past the end of the data.

        Time:  O(log p), p = target's position: log p doublings, then a
               binary search over a window of width <= p.
        Space: O(1).
        """
        # phase 1: gallop until we're at or past target, so [hi // 2, hi] contains it
        hi = 1
        while reader.get(hi) < target:
            hi *= 2

        # phase 2: plain lower_bound on the window; hi + 1 makes it half-open
        lo, hi = hi // 2, hi + 1
        while lo < hi:
            mid = (lo + hi) // 2
            if reader.get(mid) < target:
                lo = mid + 1
            else:
                hi = mid

        return lo if reader.get(lo) == target else -1
```
**Time:** O(log p) · **Space:** O(1)

## ⚠️ Gotchas
- **`hi + 1`, because `hi` itself is a candidate.** The gallop stopped *on* an element
  `>= target`, which might be the target. The half-open template's `hi` means "one
  past", so the window's upper edge is `hi + 1`. Dropping the `+ 1` misses a target
  sitting exactly on a checkpoint (like this example).
- **`lo = hi // 2`, not 0.** The previous checkpoint was `< target`, so everything up
  to it is ruled out. Starting at 0 still works, still O(log p), but shows you didn't
  use what the gallop told you.
- **Start the gallop at 1, not 0.** `0 * 2 = 0` doubles forever. Index 0 is still
  covered, since the window `[0, 1]` includes it.
- **Past-the-end must compare as big.** LeetCode 702's `get` returns `2^31 - 1` out of
  bounds, which is bigger than any real value, so the gallop stops on its own. If a
  reader you're given throws or returns `None` past the end instead, the gallop
  crashes: wrap it so out-of-range reads come back as a huge number.
- **The final `get(lo)` is always safe** here because `get` never throws. With a real
  array you'd need the `lo < n` check from EP71.

## 🎤 Interview talking points
- *"I don't know the size, so I find an upper bound first by doubling: 1, 2, 4, 8,
  until the value there is at least the target."*
- *"Doubling costs log p reads, the window is at most p wide, so the search is also
  log p. Total O(log p), in terms of where the target is, not how big the data is."*
- *"Linear steps would be O(p). Doubling is what keeps it logarithmic."*
- *"This is called exponential or galloping search. Timsort uses the same gallop when
  merging runs."*

## 🔗 Transfer
That's Shape A finished: every problem so far had a sorted array and asked where a
value goes. Tomorrow, EP76 Peak Index in a Mountain Array, has an array that **isn't
sorted** at all. What's monotonic there is a comparison between neighbours, "am I still
climbing?", and the same template finds where it flips. The doubling trick itself comes
back in spirit in Shape C: when you don't know the answer range, you can gallop to find
`hi`.

## 📹 Metadata
- **Title:** `Binary search with no right wall, gallop first | Binary Search #5`
- **Thumbnail:** `1, 2, 4, 8…` (blue block)
- **Short:** the endless road, jogging 1, 2, 4, 8 and then searching the last gap. 40s.
