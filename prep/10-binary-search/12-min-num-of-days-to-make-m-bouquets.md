# EP082 · P10E12 · Minimum Number of Days to Make m Bouquets   [Medium]

**Pattern:** Binary Search · **Link:** https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/

---

## 🎬 Hook
> "Same loop as Koko, character for character. The only new code is a five-line
> `feasible` that counts flowers standing **next to each other**, and one line before
> the loop that catches the case where no amount of waiting will ever be enough. Once
> you see that, Shape C problems stop being problems and start being fill-in-the-blank."

## 📋 Problem, in your words
```
bloomDay[i] is the day flower i blooms. A bouquet needs k ADJACENT bloomed
flowers, and each flower can be used in at most one bouquet.

Return the minimum day on which you can make m bouquets, or -1 if it's
impossible no matter how long you wait.
```

## 🔢 The example
```
Input:  bloomDay = [1, 10, 3, 10, 2], m = 3, k = 1
Output: 3
Why:    by day 3, flowers 0, 2, 4 have bloomed -> 3 bouquets of 1

Input:  bloomDay = [1, 10, 3, 10, 2], m = 3, k = 2
Output: -1             <- needs 6 flowers, only 5 exist

Input:  bloomDay = [7, 7, 7, 7, 12, 7, 7], m = 2, k = 3
Output: 12
Why:    by day 7:  X X X X _ X X   -> one run of 3 (+1 leftover), one run of 2: 1 bouquet
        by day 12: X X X X X X X   -> two runs of 3 fit: 2 bouquets
```

## 🧸 ELI5
> A row of flower pots. Each pot has a sticker saying which day it'll bloom. You need
> to make m bouquets, and each bouquet must be k flowers from pots **side by side**.
>
> Pick a day, walk down the row, and count: bloomed, bloomed, bloomed, that's a bouquet,
> start over. Hit a pot that hasn't bloomed? Your run is broken, start counting again.
>
> ```
> day 7:   7   7   7   7  12   7   7
>          X   X   X   X   _   X   X
>          [bouquet]   1   ^broken  2   -> only 1 bouquet of 3
> ```
>
> Waiting longer never un-blooms a flower. So if day d is enough, day d + 1 is enough
> too. That's the "flips once" we need.

## 🐌 Brute force (say it, don't type it)
Try every day from `min(bloomDay)` to `max(bloomDay)` and return the first that works:
**O(n · D)**, D up to 10⁹. Or try only the distinct bloom days, sorted: O(n²). Either
way, you check days one at a time when every check tells you about all later days too.

## 💡 The pattern reveal
**Signal:** "**minimum** number of days such that" · checking one day is a linear
scan · answer range up to 10⁹.
**Therefore:** Shape C, EP81's template.

| decision | here |
|---|---|
| **what is `x`?** | the day |
| **what is `feasible(day)`?** | walk the row, count runs of k adjacent `bloomDay[i] <= day`, reset the run on a gap and after each bouquet; `bouquets >= m` |
| **why monotonic?** | flowers only bloom, never un-bloom. Every bouquet possible on day d is possible on d + 1 |
| **what is the range?** | `[min(bloomDay), max(bloomDay)]`. Before the min, nothing has bloomed. At the max, everything has |
| **impossible?** | if `m * k > n`, not enough flowers exist. Return -1 **before** searching |

**Key insight:** the impossible check is separate from the search. If `m * k <= n`,
then on day `max(bloomDay)` every flower is open, the row is one unbroken run, and it
holds at least `m * k` flowers, so `feasible(max)` is guaranteed true. The search then
always has an answer to find.

## 🔍 Dry run: `bloomDay = [7, 7, 7, 7, 12, 7, 7]`, `m = 2`, `k = 3`

`m * k = 6 <= 7`, possible. `lo = 7`, `hi = 12`.

| step | lo | hi | mid | garden on day mid | bouquets | ≥ 2? | action |
|---|---|---|---|---|---|---|---|
| 1 | 7 | 12 | 9 | `X X X X _ X X` | 1 | no | `lo = 10` |
| 2 | 10 | 12 | 11 | `X X X X _ X X` | 1 | no | `lo = 12` |
| 3 | 12 | 12 | - | | | | return **12** ✓ |

Inside `feasible(9)`, walking the row: run 1, 2, **3 → bouquet, run = 0**, 1 (the 4th
seven), **gap → run = 0**, 1, 2. One bouquet. The 4th flower and the last two are
wasted because they're cut off from each other by the 12.

Days 9 and 11 give the same garden: nothing blooms between day 7 and 12. The search
doesn't know that, and doesn't need to.

## ✅ Optimal solution
```python
class Solution:
    def minDays(self, bloomDay: List[int], m: int, k: int) -> int:
        """Earliest day with m bouquets of k adjacent bloomed flowers, or -1.

        Time:  O(n log D), D = max(bloomDay) - min(bloomDay): log D guesses,
               each an O(n) walk of the row.
        Space: O(1).
        """
        if m * k > len(bloomDay):
            return -1                   # not enough flowers even if all bloom

        def feasible(day: int) -> bool:
            bouquets = run = 0
            for b in bloomDay:
                if b <= day:
                    run += 1
                    if run == k:        # a full bouquet of adjacent flowers
                        bouquets += 1
                        run = 0         # those k flowers are used up
                else:
                    run = 0             # an unbloomed flower breaks adjacency
            return bouquets >= m

        lo, hi = min(bloomDay), max(bloomDay)
        while lo < hi:                  # feasible is False...False True...True
            mid = (lo + hi) // 2
            if feasible(mid):
                hi = mid                # enough by mid; maybe earlier works
            else:
                lo = mid + 1            # not enough yet; wait longer
        return lo
```
**Time:** O(n log D) · **Space:** O(1)

## ⚠️ Gotchas
- **`m * k > n` check first.** Without it the search returns `max(bloomDay)` for an
  impossible input instead of -1. In Python the product can't overflow; in Java
  `m * k` can (m up to 10⁶, k up to 10⁵, product 10¹¹). Use `long` there.
- **Reset `run` after a bouquet.** Forget it and `run == k` fires only once per
  unbroken stretch, so `[X X X X]` with k = 2 counts 1 bouquet instead of 2. (Write
  `run >= k` to "fix" that and it counts 3, reusing flowers.) Each flower is used once.
- **Reset `run` on an unbloomed flower.** That's what "adjacent" means. Forget it and
  you're just counting bloomed flowers, which is wrong on the third example (it would
  answer 7).
- **Range from the data.** `[min, max]` of bloomDay, not `[1, 10⁹]`. The wide range
  still works; the narrow one is what the card asks for.
- **Could return early once `bouquets >= m`** inside feasible. A fine micro-optimisation;
  mention it, don't lead with it.

## 🎤 Interview talking points
- *"First, if m times k exceeds n it's impossible, return -1. Otherwise the last bloom
  day always works, so the search has an answer."*
- *"Feasible walks the row once counting runs of k adjacent bloomed flowers, resetting
  after each bouquet and on each gap."*
- *"Monotonic because flowers never un-bloom. So it's Koko's loop with a different
  feasible: O(n log of the day range)."*

## 🔗 Transfer
Koko and bouquets both **minimise**: feasible is False...True and you want the first
True. Tomorrow's EP83 Aggressive Cows **maximises** the minimum gap between cows, and
feasible runs the other way, True...False: a small gap is easy, a big gap is hard. The
loop keeps its shape but the branches flip and `mid` must round **up**, or it loops
forever. That's the one trap left in Shape C.

## 📹 Metadata
- **Title:** `Minimum Days for m Bouquets, Koko's loop, new feasible | Binary Search #12`
- **Thumbnail:** `X X X X _ X X` (blue block)
- **Short:** day 7's garden, the 12 breaking the row and wasting three flowers. 45s.
