# EP085 · P10E15 · Maximum Candies Allocated to K Children   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/maximum-candies-allocated-to-k-children/description/

---

## 🎬 Hook
> "Split candy piles so k kids each get the same amount, as much as possible. The whole
> feasibility check is `sum(pile // x) >= k`. One line. And there's a sneaky zero in the
> range that decides whether your code divides by zero."

## 📋 Problem, in your words
```
candies[i] is a pile size. You may split any pile into smaller piles,
but never merge two piles. Give each of k children exactly ONE pile,
all the same size. Some candy can be left over.

Return the largest pile size every child can get (0 if impossible).
```

## 🔢 The example
```
Input:  candies = [5, 8, 6], k = 3
Output: 5
Why:    5 -> one 5, 8 -> one 5 (+3 spare), 6 -> one 5 (+1 spare): three 5s.
        Size 6: 5 gives none, 8 gives one, 6 gives one -> only two kids.

Input:  candies = [2, 5], k = 11   -> 0   (only 7 candies for 11 kids)
Input:  candies = [4, 7, 5], k = 4 -> 3
```

## 🧸 ELI5
> You own a knife and a promise: every kid gets a bar exactly `x` long. From each bar
> you cut as many `x`-length pieces as fit and throw the stub in the bin.
>
> ```
> bars: 5, 8, 6       k = 3 kids
>
> x = 4:  5 -> 1 piece   8 -> 2   6 -> 1    = 4 pieces  ✓ enough
> x = 5:  5 -> 1         8 -> 1   6 -> 1    = 3 pieces  ✓ enough
> x = 6:  5 -> 0         8 -> 1   6 -> 1    = 2 pieces  ✗ one kid cries
> ```
>
> Bigger pieces, fewer pieces. So "enough for everyone?" goes **yes, yes, yes, no, no**
> as `x` grows. We want the last yes.

## 🐌 Brute force (say it, don't type it)
Try `x = max(candies)` down to 1 and return the first `x` where `sum(c // x) >= k`.
**O(n · max)**: with piles up to 10⁷ that's ten million passes over up to 10⁵ piles.
Each check is cheap; trying every size is the waste.

## 💡 The pattern reveal
**Signal:** "the **maximum** number of candies each child can get" · checking one size
is one pass of integer division.
**Therefore:** Shape C, maximise flavour, EP83's loop with a new `feasible`.

| decision | here |
|---|---|
| what is `x`? | the pile size each child gets |
| what is `feasible(x)`? | `sum(c // x for c in candies) >= k` |
| why monotonic? | a bigger `x` never yields more pieces from any pile |
| what is the range? | `[0, max(candies)]`: 0 is the "impossible" answer, and no child can get more than the biggest pile |

**Key insight:** the answer can legitimately be **0**, so 0 belongs in the range. And
because the maximise template rounds `mid` **up**, `mid` is never 0, so `c // mid`
never divides by zero. The rounding that stopped EP83 from looping also makes this safe.

## 🔍 Dry run: `candies = [5, 8, 6]`, `k = 3`
Range `[0, 8]`.

| step | lo | hi | mid = (lo+hi+1)//2 | pieces per pile | total | ≥ 3? | new range |
|---|---|---|---|---|---|---|---|
| 1 | 0 | 8 | 4 | 1, 2, 1 | 4 | ✓ | `lo = 4` → `[4, 8]` |
| 2 | 4 | 8 | 6 | 0, 1, 1 | 2 | ✗ | `hi = 5` → `[4, 5]` |
| 3 | 4 | 5 | 5 | 1, 1, 1 | 3 | ✓ | `lo = 5` → `[5, 5]` |
| - | 5 | 5 | stop | | | | answer **5** ✓ |

For `[2, 5]`, `k = 11`: every `mid` fails (even size 1 gives only 7 pieces), `hi`
keeps dropping to `mid - 1`, and the loop ends at `lo = 0`. The impossible case falls
out of the range for free, no special check.

## ✅ Optimal solution
```python
class Solution:
    def maximumCandies(self, candies: List[int], k: int) -> int:
        """Largest equal pile size that k children can each receive.

        Time:  O(n log M), M = max(candies): log M checks, each a pass over the piles.
        Space: O(1).
        """
        lo, hi = 0, max(candies)            # 0 = impossible; nobody beats the biggest pile
        while lo < hi:
            mid = (lo + hi + 1) // 2        # round up: also keeps mid >= 1, no // 0
            if sum(c // mid for c in candies) >= k:
                lo = mid                    # enough pieces; try bigger
            else:
                hi = mid - 1
        return lo
```
**Time:** O(n log M) · **Space:** O(1)

## ⚠️ Gotchas
- **`lo = 0` is part of the answer space.** Start at 1 and `[2, 5], k = 11` returns 1,
  which is wrong: no child can get even one candy each.
- **Rounding up protects the division.** With `lo = 0, hi = 1`, round-down gives
  `mid = 0` and `c // 0` crashes. Round-up gives `mid = 1`.
- **No merging.** Two piles of 3 can't make a 6. That's why it's `c // x` per pile and
  not `sum(candies) // x`.
- **`k` can be 10¹², bigger than any count.** Python doesn't care; in Java/C++ the
  running sum needs a `long`.
- **Leftovers are allowed.** The check is `>= k`, not `== k`.

## 🎤 Interview talking points
- *"Binary search on the pile size. `feasible(x)` is `sum(c // x) >= k`, because each
  pile gives `c // x` pieces and the stub is wasted."*
- *"Monotonic: bigger pieces, never more of them. So I want the last feasible size."*
- *"The range includes 0 for the impossible case, and rounding the midpoint up means I
  never divide by zero."*
- *"O(n log M), about 24 passes for piles up to 10⁷."*

## 🔗 Transfer
Same loop as EP83 Aggressive Cows, but a one-line `feasible` instead of a greedy
placement. From EP86 on, the pattern swings back to **minimise**: Ship Packages, Book
Allocation and Split Array are one problem told three times, and they all use the
round-down template.

## 📹 Metadata
- **Title:** `Maximum Candies, one line of feasibility | Binary Search #15`
- **Thumbnail:** `sum(c // x) >= k` (green block)
- **Short:** the ELI5 knife table, x = 4, 5, 6, with the crying kid on 6. 35s.
