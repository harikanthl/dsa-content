# EP081 · P10E11 · Koko Eating Bananas   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/koko-eating-bananas/

---

## 🎬 Hook
> "There's no sorted array in this problem. There's no array to search at all. And
> it's the most important binary search episode in the series, because the thing we
> search is **the answer itself**. Speed 1: too slow. Speed 11: fast enough. Somewhere
> in between, 'too slow' flips to 'fast enough', exactly once. Find the flip."

## 📋 Problem, in your words
```
There are piles of bananas. Koko picks an eating speed k (bananas/hour).
Each hour she picks one pile and eats k from it. If the pile has fewer
than k, she finishes it and waits out the rest of that hour.

Return the MINIMUM integer k that lets her finish all piles within h hours.
(h >= number of piles, so an answer always exists.)
```

## 🔢 The example
```
Input:  piles = [3, 6, 7, 11], h = 8
Output: 4
Why:    at k=4: 1 + 2 + 2 + 3 = 8 hours  <= 8  fits
        at k=3: 1 + 2 + 3 + 4 = 10 hours > 8   too slow

Input:  piles = [30, 11, 23, 4, 20], h = 5
Output: 30             <- one pile per hour, so k must cover the biggest pile

Input:  piles = [30, 11, 23, 4, 20], h = 6
Output: 23
```

## 🧸 ELI5
> You have homework: four chapters of 3, 6, 7 and 11 pages, and 8 hours. Each hour you
> can only work on one chapter. How few pages an hour can you get away with?
>
> Try 1 page/hour: 27 hours. Way too slow. Try 11: 4 hours. Plenty. The answer is
> somewhere between 1 and 11, and here's the thing: **if a speed works, every faster
> speed works too.** Reading faster never makes you late.
>
> ```
> speed:   1   2   3   4   5   6   7   8   9  10  11
> works?:  N   N   N   Y   Y   Y   Y   Y   Y   Y   Y
>                      ^ the first Y
> ```
>
> That's a guess-the-number game. Guess 6: works, try slower. Guess 3: doesn't, try
> faster. Guess 5: works. Guess 4: works. Answer 4.

## 🐌 Brute force (say it, don't type it)
Try `k = 1, 2, 3, ...` and return the first one that fits: **O(n · max(piles))**. With
piles up to 10⁹, that's a billion speeds times n piles. The redundancy: you check every
failing speed one by one, when each check tells you about **all** smaller (or all larger)
speeds at once.

## 💡 The pattern reveal
**Signal:** "**minimum** speed such that ... within h hours" · checking one speed is
easy · the answer can be huge (10⁹).
**Therefore:** Shape C, binary search on the answer.

**Key insight:** the three decisions from the pattern card, said out loud before any
code:

| decision | here |
|---|---|
| **what is `x`?** | eating speed `k` |
| **what is `feasible(k)`?** | `sum(ceil(p / k) for p in piles) <= h`, an O(n) check |
| **why is it monotonic?** | faster speed → each pile takes the same or fewer hours → if `k` works, `k + 1` works |
| **what is the range?** | `[1, max(piles)]`. Speed `max(piles)` finishes every pile in 1 hour, n hours total, and `h >= n`. Faster than that never helps. |

Then it's the `min_feasible` template: `if feasible(mid): hi = mid else lo = mid + 1`.

## 🔍 Dry run: `piles = [3, 6, 7, 11]`, `h = 8`

`lo = 1`, `hi = 11`.

| step | lo | hi | mid | hours per pile | total | ≤ 8? | action |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 11 | 6 | 1, 1, 2, 2 | 6 | yes | `hi = 6` |
| 2 | 1 | 6 | 3 | 1, 2, 3, 4 | 10 | no | `lo = 4` |
| 3 | 4 | 6 | 5 | 1, 2, 2, 3 | 8 | yes | `hi = 5` |
| 4 | 4 | 5 | 4 | 1, 2, 2, 3 | 8 | yes | `hi = 4` |
| 5 | 4 | 4 | - | | | | return **4** ✓ |

Steps 3 and 4 give the **same** total, 8 hours, at speeds 5 and 4. Feasible still
says yes at 4, so the search keeps pushing down. It only stops when `lo` and `hi` meet,
and step 2 already proved 3 is too slow.

Four `feasible` calls instead of up to eleven. With `max(piles) = 10⁹`, about thirty.

## ✅ Optimal solution
```python
class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        """Smallest eating speed that finishes every pile within h hours.

        Time:  O(n log M), M = max(piles): log M guesses, each an O(n) check.
        Space: O(1).
        """
        def feasible(speed: int) -> bool:
            # ceil(p / speed) without floats: a partial hour still costs a full hour
            return sum((p + speed - 1) // speed for p in piles) <= h

        lo, hi = 1, max(piles)          # max(piles) always works since h >= len(piles)
        while lo < hi:                  # feasible is False...False True...True
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid                # mid works; maybe something slower does too
            else:
                lo = mid + 1            # mid is too slow; need faster
        return lo
```
**Time:** O(n log M) · **Space:** O(1)

## ⚠️ Gotchas
- **Ceiling division.** A pile of 7 at speed 3 takes 3 hours, not 2. `p // k` is
  wrong; `math.ceil(p / k)` works but uses floats; `(p + k - 1) // k` is exact.
  `-(-p // k)` is the other idiom.
- **`lo = 1`, not 0.** Speed 0 divides by zero and means nothing.
- **`hi = max(piles)`, not `sum(piles)` or 10⁹.** Both still work, but the pattern
  card's rule is "the range comes from the data". Say why `max(piles)` is enough.
- **Minimise → `hi = mid` on success.** Mid worked, so it's a candidate; keep it. This
  is the Shape A template with `feasible(mid)` in place of `arr[mid] >= x`.
- **State monotonicity before coding.** "Faster never makes her later." If you can't
  say that sentence, you're not allowed to binary search.
- **Don't return early when `feasible(mid)` is exactly `h`.** Step 4 above: speed 5
  gives exactly 8 hours, and 4 also does. Exact equality doesn't mean minimal.

## 🎤 Interview talking points
- *"I'm binary searching over speeds, not over the array. The predicate 'can she finish
  at speed k' is monotonic: if k works, anything faster works."*
- *"Checking one speed is O(n), I need log of max-pile checks, so O(n log M)."*
- *"The range is 1 to max(piles): at max speed every pile is one hour, and h is at
  least the number of piles."*
- *"This is the 'minimise x such that feasible(x)' template. Ship Packages, Book
  Allocation, Split Array are the same code with a different feasible."* ← signal that
  you see the family.

## 🔗 Transfer
Koko is the template for eight episodes. Tomorrow's EP82, Minimum Days to Make m
Bouquets, keeps the exact loop and only changes what `feasible(day)` counts: runs of
**adjacent** bloomed flowers, which makes the check slightly trickier and adds an
"impossible" case. EP83 Aggressive Cows then flips it: **maximise** x, and the branches
and the rounding of `mid` both change.

## 📹 Metadata
- **Title:** `Koko Eating Bananas, binary search the ANSWER | Binary Search #11`
- **Thumbnail:** `N N N Y Y Y` (blue block)
- **Short:** the speed/works? row, then four guesses landing on 4. 50s.
