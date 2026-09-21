# EP062 · P08E05 · Daily Temperatures   [Medium]

**Pattern:** Stack · **Link:** https://leetcode.com/problems/daily-temperatures/

---

## 🎬 Hook
> "How many days until it gets warmer? Same monotonic stack as yesterday, one change
> that matters: the answer is a **distance**, not a value — so the stack has to hold
> indices, and the pop computes `i − j`. If you ever wondered why the template says
> 'store indices', this is the episode that makes it non-negotiable."

## 📋 Problem, in your words
```
Given an array of daily temperatures, return an array where position i
holds the NUMBER OF DAYS you have to wait after day i for a warmer
temperature.

If no warmer day ever comes, the answer for that day is 0.
Not circular -- the array ends and that's that.
```

## 🔢 The example
```
Input:  [73, 74, 75, 71, 69, 72, 76, 73]
Output: [ 1,  1,  4,  2,  1,  1,  0,  0]
Why:    day 0 (73) -> day 1 is 74, warmer  -> wait 1
        day 2 (75) -> nothing warmer until day 6 (76) -> wait 4
        day 6 (76) -> never gets warmer    -> 0
        day 7 (73) -> the array ends       -> 0

Input:  [30, 40, 50, 60]  -> [1, 1, 1, 0]
Input:  [30, 60, 90]      -> [1, 1, 0]
```

## 🧸 ELI5
> Each day walks in and asks *"has it got warmer yet?"* If not, it **sits down and
> waits** — and you write down which day it was, because the answer will be a number of
> days, and you can't count days without knowing where you started.
>
> ```
> [73, 74, 75, 71, 69, 72, 76, 73]
>
> day 0 (73) sits down.                    waiting: [day0]
> day 1 (74) is warmer than day 0!         -> day 0 waited 1 - 0 = 1 day ✓
>            then day 1 sits down.         waiting: [day1]
> day 2 (75) is warmer than day 1          -> day 1 waited 2 - 1 = 1 ✓
>            sits down.                    waiting: [day2]
> day 3 (71) colder, sits down.            waiting: [day2, day3]
> day 4 (69) colder still, sits down.      waiting: [day2, day3, day4]
> day 5 (72) beats day 4 (69): 5 - 4 = 1 ✓
>            beats day 3 (71): 5 - 3 = 2 ✓
>            but NOT day 2 (75) -> stops.  waiting: [day2, day5]
> day 6 (76) beats day 5: 6 - 5 = 1 ✓
>            beats day 2: 6 - 2 = 4 ✓      <- the long wait, paid out at last
>            sits down.                    waiting: [day6]
> day 7 (73) colder, sits down.            waiting: [day6, day7]
>
> days 6 and 7 are still waiting when the data ends -> 0, 0
> ```
>
> The waiting days are always in **decreasing** temperature order — a colder day joins
> the back, a warmer day clears everyone it beats.

## 🐌 Brute force (say it, don't type it)
For each day, scan forward until you find something warmer. **O(n²)** — and on a
strictly decreasing array it really is quadratic, not just in theory. The stack removes
the rescanning: each day is examined once as a newcomer and once as a waiter.

## 💡 The pattern reveal
**Signal:** "how many days/steps until X" · for **every** element.
**Therefore:** monotonic stack of **indices**, answer written at the pop.

**The four decisions:**

| decision | here |
|---|---|
| increasing or decreasing? | "next warmer" → pop while the top is colder → stack stays **decreasing** |
| index or value? | **index, mandatory** — the answer is `i − j`, and a value can't tell you `j` |
| what happens at the pop? | `res[j] = i − j` ← the distance, computed at the moment of resolution |
| what's left at the end? | days that never warmed → the default `0` |

```python
while stack and temps[stack[-1]] < t:
    j = stack.pop()
    res[j] = i - j          # `i` is the warmer day, `j` is the day that was waiting
stack.append(i)
```

**This is EP61 with two edits:** no second lap (the array doesn't wrap), and `res[j] =
i - j` instead of `res[j] = cur`. Say that on camera — recognising that two problems
are the same code is worth more than solving both.

**🧨 The trap: `i − j`, in that order.** `j` is the *earlier* day sitting on the stack;
`i` is the current, warmer day. Writing `j − i` gives negative waits, and writing
`res[i] = i - j` writes the answer onto the wrong day — which is subtler, because the
output is full of plausible-looking small numbers.

## 🔍 Dry run — `[73, 74, 75, 71, 69, 72, 76, 73]`
`res = [0]*8`, `stack = []` (indices).

| i | temp | pops → answers written | stack after | `res` so far |
|---|---|---|---|---|
| 0 | 73 | — | `[0]` | `[0,0,0,0,0,0,0,0]` |
| 1 | 74 | pop 0 → `res[0] = 1−0 = 1` | `[1]` | `[1,0,…]` |
| 2 | 75 | pop 1 → `res[1] = 2−1 = 1` | `[2]` | `[1,1,…]` |
| 3 | 71 | — (71 < 75) | `[2,3]` | — |
| 4 | 69 | — | `[2,3,4]` | — |
| 5 | 72 | pop 4 → `res[4] = 1`; pop 3 → `res[3] = 2`; stop at 75 | `[2,5]` | `[1,1,0,2,1,0,0,0]` |
| 6 | 76 | pop 5 → `res[5] = 1`; **pop 2 → `res[2] = 6−2 = 4`** | `[6]` | `[1,1,4,2,1,1,0,0]` |
| 7 | 73 | — | `[6,7]` | unchanged |

Indices 6 and 7 never pop → they keep `0`. Answer **`[1,1,4,2,1,1,0,0]`** ✓

Two rows carry the episode:

- **`i = 5`** pops twice and then *stops* — 72 beats 69 and 71 but not 75. The `while`
  ends the moment the invariant is restored, which is what keeps the stack decreasing.
- **`i = 6`** pays out day 2's four-day wait. Index 2 sat on the stack for four
  iterations, which is exactly what "still waiting" means.

## ✅ Optimal solution
```python
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:
        """Days to wait for a warmer temperature, for every day.

        Time:  O(n) — each index is pushed once and popped at most once.
        Space: O(n) — the stack (worst case: a strictly decreasing array).
        """
        res = [0] * len(temperatures)       # default: it never gets warmer
        stack = []                          # INDICES of days still waiting

        for i, t in enumerate(temperatures):
            # today is warmer than everyone still waiting below it
            while stack and temperatures[stack[-1]] < t:
                j = stack.pop()
                res[j] = i - j              # distance, not value -- hence indices

            stack.append(i)

        return res
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **`res[j] = i - j`** — current index minus the waiting index. Both the order and the
  target (`res[j]`, not `res[i]`) are easy to get backwards and hard to spot.
- **Indices on the stack, always.** This problem has no value-based variant; the answer
  is a position difference.
- **`<` vs `<=`:** `<` means a day with an *equal* temperature doesn't count as warmer,
  which matches "warmer". `[70, 70, 71]` → `[2, 1, 0]`. Test the duplicate.
- **Default `0`, not `-1`.** The statement says 0 for "never". Copying EP61's `-1` here
  is a paste error that passes the first example.
- **No second lap.** This array doesn't wrap. Adding EP61's circular loop gives wrong
  answers for the trailing days.
- **`enumerate` rather than `range(len(...))`** — you need both the index and the value
  on every iteration.

## 🎤 Interview talking points
- *"Monotonic decreasing stack of indices. Each day pops everyone it's warmer than, and
  each pop is that day's answer: current index minus waiting index."*
- *"Indices rather than values, because the answer is a distance."* ← the reason this
  problem exists.
- *"Amortised O(n): every index is pushed once and popped once, even though there's a
  `while` inside the `for`."*
- *"It's Next Greater Element with the value replaced by a distance and the wrap-around
  removed."* ← naming the reuse.

## 🔗 Transfer
Two monotonic episodes down, and both wrote their answers into a separate array.
Tomorrow (EP63) changes what the stack is *for*: the same decreasing invariant runs over
a **linked list**, and at the end the stack's survivors aren't failures — they're the
output list itself, which has to be re-stitched.

## 📹 Metadata
- **Title:** `Daily Temperatures — the answer is a distance | Stack #5`
- **Thumbnail:** `i − j` (green block)
- **Short:** day 2 waiting four iterations and being paid out at day 6. 45s.
