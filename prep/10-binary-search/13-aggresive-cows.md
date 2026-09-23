# EP083 · P10E13 · Aggressive Cows   [Medium]

**Pattern:** Binary Search · **Link:** https://www.geeksforgeeks.org/problems/aggressive-cows/1

---

## 🎬 Hook
> "Two episodes of *minimise* x. Today the problem asks you to **maximise** it, and the
> template you've typed twice will loop forever if you only flip the `if`. One `+ 1` in
> the midpoint is the whole difference, and this episode is where it earns its place."

## 📋 Problem, in your words
```
You have n stalls at positions stalls[i] on a line, and k cows.
Put each cow in a different stall so that the SMALLEST distance
between any two cows is as LARGE as possible.

Return that largest possible minimum distance.
```

## 🔢 The example
```
Input:  stalls = [1, 2, 4, 8, 9], k = 3
Output: 3
Why:    cows at 1, 4, 8 -> gaps 3 and 4, the smallest is 3.
        No placement of 3 cows keeps every gap >= 4.

Input:  stalls = [10, 1, 2, 7, 5], k = 3   -> 4   (cows at 1, 5, 10)
Input:  stalls = [1, 5], k = 2             -> 4   (only one way to do it)
```

## 🧸 ELI5
> The cows hate each other. You're the farmer and you pick a **rule**: "no two cows
> closer than `g` metres." Then you walk down the barn from the left and drop a cow in
> the first stall that obeys the rule, then the next, and so on.
>
> ```
> stalls:   1  2  .  4  .  .  .  8  9
>
> rule g=3: 1 ------> 4 ----------> 8        3 cows placed  ✓
> rule g=4: 1 ----------------> 8            only 2 cows    ✗
> ```
>
> A gentle rule lets lots of cows in. A strict rule lets few in. So as `g` goes up the
> answer to "do all k cows fit?" is **yes, yes, yes, no, no**. You want the **last yes**.

## 🐌 Brute force (say it, don't type it)
Try every gap from 1 up to `max - min`, run the greedy placement for each, keep the
last one that fits all k cows. **O(n · range)**: with positions up to 10⁹ that's a
billion greedy passes. Or try every subset of k stalls, which is exponential. The
greedy check is already cheap; what's expensive is trying every gap one at a time.

## 💡 The pattern reveal
**Signal:** "the **largest** minimum distance such that all cows fit" · checking one
distance is a single left-to-right pass.
**Therefore:** Shape C, binary search on the answer, the **maximise** flavour.

| decision | here |
|---|---|
| what is `x`? | the minimum gap `g` |
| what is `feasible(g)`? | greedy: place a cow in the first stall, then in every stall at least `g` past the last cow; did we place `k`? |
| why is it monotonic? | if gap `g` works, any smaller gap works too, same placement. So feasible is **true, true, false, false** |
| what is the range? | `[1, stalls[-1] - stalls[0]]` after sorting. The gap can't be 0 (stalls are distinct) and can't beat the whole span |

**Key insight:** the predicate flips from true to false, so we want the **last true**,
not the first. Two edits to the minimise template:

```python
mid = (lo + hi + 1) // 2      # round UP
if can_place(mid):
    lo = mid                  # mid works; the answer is mid or bigger
else:
    hi = mid - 1              # mid fails; everything >= mid fails
```

**🧨 Why round up:** with `lo = 3, hi = 4`, the normal `mid = 3`. If 3 is feasible,
`lo = mid = 3` and nothing moved. Infinite loop. Rounding up makes `mid = 4`, and both
branches now shrink the range.

## 🔍 Dry run: `stalls = [1, 2, 4, 8, 9]`, `k = 3`
Range `[1, 9 - 1] = [1, 8]`.

| step | lo | hi | mid = (lo+hi+1)//2 | greedy placement | cows | feasible? | new range |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 8 | 5 | 1, then first ≥ 6 is 8 | 2 | ✗ | `hi = 4` → `[1, 4]` |
| 2 | 1 | 4 | 3 | 1, 4 (≥ 4), 8 (≥ 7) | 3 | ✓ | `lo = 3` → `[3, 4]` |
| 3 | 3 | 4 | **4** | 1, then first ≥ 5 is 8, then need ≥ 12 | 2 | ✗ | `hi = 3` → `[3, 3]` |
| - | 3 | 3 | stop | | | | answer **3** ✓ |

Step 3 is the one to point at on screen: plain `(3 + 4) // 2` would be 3, feasible,
`lo = 3`, and the loop would sit there forever.

## ✅ Optimal solution
```python
def aggressive_cows(stalls: list[int], k: int) -> int:
    """Largest possible minimum gap when placing k cows in the stalls.

    Time:  O(n log n + n log R), R = max - min: the sort, then log R greedy passes.
    Space: O(1) beyond the sorted copy.
    """
    stalls = sorted(stalls)                 # greedy placement needs left-to-right order

    def can_place(gap: int) -> bool:
        placed, last = 1, stalls[0]         # first cow always goes in the first stall
        for s in stalls[1:]:
            if s - last >= gap:
                placed += 1
                last = s
                if placed == k:
                    return True
        return placed >= k

    lo, hi = 1, stalls[-1] - stalls[0]
    while lo < hi:
        mid = (lo + hi + 1) // 2            # round up, or lo = mid can stall
        if can_place(mid):
            lo = mid                        # mid works; try bigger
        else:
            hi = mid - 1                    # mid fails; so does everything above
    return lo
```
**Time:** O(n log n + n log R) · **Space:** O(1) extra

## ⚠️ Gotchas
- **`(lo + hi + 1) // 2`.** The maximise template without the `+ 1` hangs the first time
  `hi = lo + 1` and `lo` is feasible. Trace `[3, 4]` to prove it to yourself.
- **Sort first.** The stalls arrive unsorted (`[10, 1, 2, 7, 5]`). The greedy only works
  walking left to right.
- **The first cow goes in the first stall, always.** Moving it right can only shrink the
  room for the rest. That's the exchange argument behind the greedy; say it in one line.
- **`lo = 1`, not 0.** With k ≥ 2 and distinct stalls the answer is at least 1. Starting
  at 0 is harmless but it means you didn't think about the range.
- **Early exit at `placed == k`** is optional, but it makes the check stop as soon as
  the answer is known.

## 🎤 Interview talking points
- *"I'm binary searching the answer, the minimum gap. Checking one gap is a greedy
  pass: first stall, then every stall at least `g` past the last cow."*
- *"Monotonic because a smaller gap is always easier: any placement that works for `g`
  works for `g - 1`."*
- *"This is maximise, so I keep `lo = mid` on success and round the midpoint up; with
  `lo < hi` and `lo = mid`, rounding down would loop."* ← the thing they're testing.
- *"n log R instead of n · R: thirty-ish greedy passes even when positions go to 10⁹."*

## 🔗 Transfer
Koko (EP81) and Bouquets (EP82) searched for the *first* true; this is the first *last
true*, and the only change is the midpoint and which side keeps `mid`. EP84, H-Index
II, is a breather that sits between Shape A and Shape C. Then EP85, Maximum Candies,
is maximise again: you'll type this exact loop with a different `feasible`.

## 📹 Metadata
- **Title:** `Aggressive Cows, the + 1 that stops an infinite loop | Binary Search #13`
- **Thumbnail:** `(lo + hi + 1) // 2` (red block)
- **Short:** step 3 of the dry run, `[3, 4]` with and without the `+ 1`. 40s.
