# EP173 · P15E02 · Climbing Stairs   [Easy]

**Pattern:** DP (Dynamic Programming) · **Link:** https://leetcode.com/problems/climbing-stairs/description/

---

## 🎬 Hook
> "This problem never mentions Fibonacci. It's Fibonacci anyway. The skill today isn't
> the code, you wrote the code yesterday. It's asking **one question** that pulls the
> recurrence out of a word problem: *what was the last move?*"

## 📋 Problem, in your words
```
A staircase has n steps. Each move you climb 1 step or 2 steps.
How many distinct sequences of moves get you from the ground to the top?

1 <= n <= 45. Order matters: 1+2 and 2+1 are different ways.
```

## 🔢 The example
```
Input:  n = 3
Output: 3
Why:    1+1+1, 1+2, 2+1

Input:  n = 5   -> 8
Input:  n = 1   -> 1
```

## 🧸 ELI5
> You're standing on step 5. Somebody asks "how did you get here?" There are only two
> possible answers: **"I hopped 1 from step 4"** or **"I hopped 2 from step 3"**.
>
> ```
>   step 5  <-- 1 hop -- step 4       every route to 4, plus one more hop
>   step 5  <-- 2 hop -- step 3       every route to 3, plus one more hop
> ```
>
> Those two groups don't overlap (the last hop is different) and they cover everything.
> So the ways to reach 5 is the ways to reach 4 **plus** the ways to reach 3.
>
> Write the count on each step as you climb, and every step is just the sum of the two
> numbers below it.

## 🐌 Brute force (say it, don't type it)
Enumerate every sequence of 1s and 2s and count the ones that sum to n. Or the recursion
`ways(n) = ways(n-1) + ways(n-2)` without a memo. Both are **O(2ⁿ)**: at n = 45 the
answer is 1,836,311,903, and the naive recursion makes more calls than that. Say it,
then say "same tree as Fibonacci, same fix".

## 💡 The pattern reveal
**Signal:** "**how many distinct ways**", and each way is a sequence of small choices.
**Therefore:** DP, Shape A (1-D linear, looks back a fixed distance).

**Key insight:** split every way by its **last move**. The last move is 1 or 2, so

```
ways(i) = ways(i - 1) + ways(i - 2)
```

The base cases are the design decision:

| state | value | why |
|---|---|---|
| `ways(0)` | **1** | standing on the ground, there's exactly one way to be there: do nothing |
| `ways(1)` | 1 | one single hop |
| `ways(2)` | 2 | follows from the recurrence: 1 + 1 ✓ (1+1, 2) |

`ways(0) = 1` feels wrong to people. It's the "empty thing has one way" rule from the
pattern card, and you'll see it again in Target Sum (EP179) and Unique Paths (EP183).

Compared with Fibonacci: `ways(n) = F(n + 1)`. Same sequence, shifted one place.

## 🔍 Dry run: `n = 5`, rolling variables

`prev2` = ways(i-2), `prev1` = ways(i-1). Start with ways(0) = 1, ways(1) = 1.

| i | prev2 (ways i-2) | prev1 (ways i-1) | ways(i) = prev1 + prev2 | after the shift |
|---|---|---|---|---|
| start | 1 | 1 | - | (1, 1) |
| 2 | 1 | 1 | **2** | (1, 2) |
| 3 | 1 | 2 | **3** | (2, 3) |
| 4 | 2 | 3 | **5** | (3, 5) |
| 5 | 3 | 5 | **8** | (5, 8) |

Answer **8** ✓. The whole table, if you'd kept it:

| i | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| ways | 1 | 1 | 2 | 3 | 5 | **8** |

## ✅ Optimal solution
```python
class Solution:
    def climbStairs(self, n: int) -> int:
        """Ways to climb n steps with hops of 1 or 2.

        Split every way by its last hop: ways(i) = ways(i-1) + ways(i-2).
        Time:  O(n), one pass.
        Space: O(1), only the two previous counts are ever read.
        """
        prev2, prev1 = 1, 1                  # ways(0), ways(1)
        for _ in range(2, n + 1):
            prev2, prev1 = prev1, prev1 + prev2
        return prev1
```
**Time:** O(n) · **Space:** O(1)

The memo version, if you want to show step 3 first:

```python
@lru_cache(maxsize=None)
def ways(i: int) -> int:
    if i <= 1:
        return 1                             # ways(0) = ways(1) = 1
    return ways(i - 1) + ways(i - 2)
```

## ⚠️ Gotchas
- **`ways(0) = 1`, not 0.** Set it to 0 and ways(2) comes out as 1, and everything after
  is wrong. If the base case feels odd, check it against n = 2 by hand.
- **`n = 1` must not enter the loop.** `range(2, 2)` is empty, so `prev1 = 1` is
  returned. Correct for free, but trace it once.
- **Order matters here.** 1+2 and 2+1 are two ways. If the problem said "how many
  *combinations* of hop sizes", that's the coin-change counting problem, a knapsack-shaped
  DP, and a different loop order.
- **Generalises cleanly.** Hops of 1, 2 or 3? `ways(i) = ways(i-1) + ways(i-2) + ways(i-3)`.
  Hops from a set `S`? Sum over `s in S`. Have that ready: it's the standard follow-up.

## 🎤 Interview talking points
- *"I split by the last move. It's 1 or 2, those cases don't overlap and they cover
  everything, so the counts add."* ← the move that finds any counting recurrence.
- *"Base case: ways(0) = 1, the empty climb. That makes ways(2) = 2, which I can check."*
- *"It's Fibonacci shifted by one, so O(n) time and O(1) space with two variables."*
- *"If the hop sizes were a set, I'd sum over the set; if cost were involved, I'd take
  a min instead of a sum."* ← that last one is Min Cost Climbing Stairs.

## 🔗 Transfer
EP172 gave you the recurrence. This one makes you **find** it, by splitting on the last
choice. EP174 House Robber keeps the same "look back one or two" shape but swaps the
`+` for a `max` and gives each step a value: the first **optimisation** DP instead of a
counting one. The "empty thing has one way" base comes back in EP179 and EP183.

## 📹 Metadata
- **Title:** `Climbing Stairs is Fibonacci in disguise (ask about the LAST step) | DP #2`
- **Thumbnail:** `LAST STEP?`
- **Short:** a stick figure on step 5 looking down at steps 4 and 3, numbers appearing
  on each step as the sum of the two below. 35s.
