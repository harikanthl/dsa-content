# EP185 · P15E14 · Minimum Cost to Cut a Stick   [Hard]

**Pattern:** DP (Dynamic Programming) · **Link:** https://leetcode.com/problems/minimum-cost-to-cut-a-stick/

---

## 🎬 Hook
> "Every cut costs the length of the piece you're cutting, so the **order** of cuts
> changes the bill. Trying every order is factorial. The trick is to stop asking 'which
> cut goes first **overall**' and ask 'which cut goes first **inside this piece**', and
> suddenly the state is just two numbers: the piece's left end and right end."

## 📋 Problem, in your words
```
A stick of length n, marked at positions 0..n. You must make every cut in `cuts`
(distinct positions strictly between 0 and n), in any order you choose.
Cutting a piece costs that piece's current length.
Return the minimum total cost.

2 <= n <= 10^6, 1 <= len(cuts) <= 100.
```

## 🔢 The example
```
Input:  n = 7, cuts = [1, 3, 4, 5]
Output: 16
Why:    cut at 3 first (cost 7), then 1 on [0,3] (3), then 5 on [3,7] (4),
        then 4 on [3,5] (2).   7 + 3 + 4 + 2 = 16
        In the given order 1, 3, 4, 5 it would cost 7 + 6 + 4 + 3 = 20.

Input:  n = 9, cuts = [5, 6, 1, 4, 2]   -> 22
```

## 🧸 ELI5
> You're paying a carpenter by the length of whatever plank they pick up. Cut a long
> plank and you pay a lot; cut a short one and you pay a little.
>
> Here's the question that makes it solvable: for **one** plank, running from mark `a`
> to mark `b`, **which of its marks do you cut first?** Whatever you pick, you pay the
> full plank length `b - a` right now, and then you're left with two smaller planks,
> left and right, that have **nothing to do with each other** any more.
>
> ```
>       [ 0 ------ 3 ---------- 7 ]        cut at 3 first: pay 7
>              /           \
>       [ 0 - 1 - 3 ]   [ 3 - 4 - 5 - 7 ]  two independent sub-problems
> ```
>
> So "best cost for a plank" = its length + the best split point's two halves. Every
> plank is described by just its two end marks.

## 🐌 Brute force (say it, don't type it)
Try every order of the `m` cuts: **O(m! · m)**. At m = 100, that's more orders than
atoms in the universe. The orders overlap massively: whether you cut 1 before or after
5, once 3 is cut the left piece `[0, 3]` is the same sub-problem.

## 💡 The pattern reveal
**Signal:** "the **order** of operations changes the cost" · each operation **splits**
something into two **independent** parts · "minimum total".
**Therefore:** DP, Shape E (interval DP: the state is a range `[l, r]`, split at every `k`).

**Setup:** add the ends and sort, so every piece is between two marks:
`cuts = [0] + sorted(cuts) + [n]` → `[0, 1, 3, 4, 5, 7]`, indices `0..5`.

**State:** `dp[l][r]` = min cost to make every cut strictly between mark `l` and mark `r`
(indices into the padded array).

**Recurrence:** try each mark `k` between them as the **first** cut of this piece:

```
dp[l][r] = (cuts[r] - cuts[l])                          # pay the piece's length once
           + min(dp[l][k] + dp[k][r] for k in range(l + 1, r))
```

**Base:** `dp[l][l+1] = 0`. Adjacent marks, no cut between them.

**Fill order:** `dp[l][r]` reads **shorter** intervals inside it. So loop on interval
**length**, from 2 up. Looping on `l` from 0 would read `dp[k][r]` before it's filled.

**Key insight:** the padded, sorted marks turn "which order" into "which split", and a
split creates two sub-problems that never interact again. Index by marks, not by
positions: n can be 10⁶ but there are at most 102 marks, so the table is 102 × 102, not
10⁶ × 10⁶.

## 🔍 Dry run: `n = 7`, `cuts = [1, 3, 4, 5]` → marks `[0, 1, 3, 4, 5, 7]`

Filled by increasing length (number of mark-gaps). Each row: the interval, its length,
the options for the first cut, the result.

| len | `[l, r]` | piece | options `dp[l][k] + dp[k][r]` | dp = piece + min |
|---|---|---|---|---|
| 2 | [0, 2] | 0..3 | k=1 (at 1): 0 | 3 + 0 = **3** |
| 2 | [1, 3] | 1..4 | k=2 (at 3): 0 | 3 + 0 = **3** |
| 2 | [2, 4] | 3..5 | k=3 (at 4): 0 | 2 + 0 = **2** |
| 2 | [3, 5] | 4..7 | k=4 (at 5): 0 | 3 + 0 = **3** |
| 3 | [0, 3] | 0..4 | at 1: 0 + 3 = 3 · at 3: 3 + 0 = 3 | 4 + 3 = **7** |
| 3 | [1, 4] | 1..5 | at 3: 0 + 2 = 2 · at 4: 3 + 0 = 3 | 4 + 2 = **6** |
| 3 | [2, 5] | 3..7 | at 4: 0 + 3 = 3 · at 5: 2 + 0 = 2 | 4 + 2 = **6** |
| 4 | [0, 4] | 0..5 | at 1: 6 · at 3: 5 · at 4: 7 | 5 + 5 = **10** |
| 4 | [1, 5] | 1..7 | at 3: 6 · at 4: 6 · at 5: 6 | 6 + 6 = **12** |
| 5 | [0, 5] | 0..7 | at 1: 12 · **at 3: 9** · at 4: 10 · at 5: 10 | 7 + 9 = **16** |

Answer `dp[0][5]` = **16** ✓. The last row is the one to narrate: cutting at 3 first
wins because it splits the stick most evenly among the remaining cuts.

The finished table (upper triangle only; `-` means unused):

| l \ r | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| 0 | - | 0 | 3 | 7 | 10 | **16** |
| 1 | - | - | 0 | 3 | 6 | 12 |
| 2 | - | - | - | 0 | 2 | 6 |
| 3 | - | - | - | - | 0 | 3 |
| 4 | - | - | - | - | - | 0 |

## ✅ Optimal solution
```python
class Solution:
    def minCost(self, n: int, cuts: List[int]) -> int:
        """Min total cost to make every cut, each cut costing its piece's length.

        Marks = [0] + sorted(cuts) + [n].
        dp[l][r] = min cost to finish every cut strictly between marks l and r.
        Time:  O(m^3), m = len(cuts) + 2: O(m^2) intervals, O(m) splits each.
        Space: O(m^2).
        """
        marks = [0] + sorted(cuts) + [n]
        m = len(marks)
        dp = [[0] * m for _ in range(m)]          # length-1 gaps: nothing to cut, cost 0
        for length in range(2, m):                # shorter intervals first
            for l in range(m - length):
                r = l + length
                dp[l][r] = (marks[r] - marks[l]) + min(
                    dp[l][k] + dp[k][r] for k in range(l + 1, r)   # k = first cut inside
                )
        return dp[0][m - 1]
```
**Time:** O(m³) · **Space:** O(m²)

The memo form, which some find easier to write first:

```python
@lru_cache(maxsize=None)
def f(l: int, r: int) -> int:
    if r - l < 2:
        return 0                                   # no mark strictly inside
    return marks[r] - marks[l] + min(f(l, k) + f(k, r) for k in range(l + 1, r))
```

## ⚠️ Gotchas
- **Sort the cuts.** The interval `[l, r]` only means "a contiguous piece" if the marks
  are in order. Unsorted input gives nonsense intervals.
- **Pad with 0 and n.** Without them the outermost piece has no ends to measure.
- **Fill by length, not by `l`.** `for l in range(m): for r in range(l+2, m)` reads
  `dp[k][r]` for `k > l`, which hasn't been computed yet: it reads 0 and underestimates.
- **Index by mark, not by position.** A table indexed by position is n × n = 10¹², for
  a problem with 100 cuts.
- **The piece's length is paid once per interval**, outside the `min`. Adding it inside
  the `min` is the same number; adding it to both halves double-counts.

## 🎤 Interview talking points
- *"The order matters, but cutting a piece at k splits it into two independent pieces.
  So I pick the first cut in each piece, and the state is just the piece's two ends."*
- *"I sort the cuts and pad with 0 and n, and index by those marks, so the table is
  (m+2)² regardless of n."*
- *"dp[l][r] = length of the piece + min over k of dp[l][k] + dp[k][r]. Each reads
  shorter intervals, so I fill by increasing length."*
- *"O(m³) time, O(m²) space. It's the same shape as Matrix Chain Multiplication and
  Burst Balloons."* ← naming the family is half the credit on interval DP.

## 🔗 Transfer
This is Shape E, the last one: the state is a **range**, the transition is a **split**,
and the fill order is by **length**. Burst Balloons, Matrix Chain Multiplication,
Palindrome Partitioning II and Optimal BST are all this loop. It also closes the loop on
EP120 Palindrome Partitioning: that was "try every cut" as backtracking to *list* the
partitions; interval DP is what you do when you only need the *best* one. EP186 puts all
five shapes side by side.

## 📹 Metadata
- **Title:** `Min Cost to Cut a Stick, order becomes a SPLIT (interval DP) | DP #14`
- **Thumbnail:** `dp[l][r]`
- **Short:** the order 1,3,4,5 costing 20, then cutting at 3 first and watching it drop
  to 16. 45s.
