# EP186 · P15E15 · DP Revision, and the End of the Series   [Revision]

**Pattern:** DP (Dynamic Programming) · **Link:** no new problem. Every problem from EP172 to EP185, from a blank file.

---

## 🎬 Hook
> "Fourteen DP problems, and they're really **five shapes** and **one method**. Today
> there's no new problem. I'm going to put the five shapes side by side, show you the
> one checklist that finds the state, and then throw problems at you that we *haven't*
> solved, and you name the shape before I do. And then, after 186 episodes, we're done."

## 📋 What this episode is
```
1. The method: four steps, five questions to flip a memo into a table.
2. The five shapes, one problem each, written live from a blank file.
3. The whole pattern in one table: state, transition, base, complexity.
4. Drills: 12 problems we haven't solved. Name the pattern, then the shape.
5. Series close-out.
```

## 🔢 The five shapes, one problem each (the blank-file round)
Write each one live with the recurrence said out loud *before* the code. Target: under
four minutes each. If one takes longer, that's the episode to rewatch.

| shape | reads | problem to write live | the sentence to say first |
|---|---|---|---|
| **A · 1-D linear** | a fixed distance back | House Robber (EP174) | "best from 0..i: skip it, or rob it plus best from 0..i-2" |
| **B · knapsack** | the previous row | Target Sum (EP179) | "P = (total + target) / 2, then count subsets, one row, backwards" |
| **C · LIS** | every earlier index | LIS (EP180 to 181) | "longest ending exactly at i, answer is the max" |
| **D · two sequences / grid** | up, left, diagonal | LCS (EP182) | "match: diagonal + 1; mismatch: max of up and left" |
| **E · interval** | every split inside | Cut a Stick (EP185) | "pay the piece, then the best first cut; fill by length" |

The skeletons, to check yourself against after you've written them (not before):

```python
# A: House Robber
prev2, prev1 = 0, 0
for x in nums:
    prev2, prev1 = prev1, max(prev1, prev2 + x)

# B: count subsets summing to P
dp = [1] + [0] * P
for x in arr:
    for c in range(P, x - 1, -1):
        dp[c] += dp[c - x]

# C: LIS, O(n log n)
tails = []
for x in nums:
    k = bisect_left(tails, x)
    tails[k:k + 1] = [x]              # append if k == len(tails), else replace

# D: LCS
for i in range(1, m + 1):
    for j in range(1, n + 1):
        dp[i][j] = dp[i-1][j-1] + 1 if a[i-1] == b[j-1] else max(dp[i-1][j], dp[i][j-1])

# E: interval
for length in range(2, m):
    for l in range(m - length):
        r = l + length
        dp[l][r] = marks[r] - marks[l] + min(dp[l][k] + dp[k][r] for k in range(l + 1, r))
```

## 🧸 ELI5: the whole pattern in one paragraph
> DP is a notebook. You're solving a big problem by solving smaller versions of it, and
> the smaller versions keep coming back, so you write each answer down the first time.
> The only hard part is deciding **what to write on the top of each page**: the few
> numbers that say "where am I". Get that label right and the rest is filling pages in
> the right order.

## 🐌 The method (the part that never changes)

**Four steps, every problem:**

| # | step | the check |
|---|---|---|
| 1 | **Say the state in words** | "`dp[...]` is the best / number of ways / whether ... for ..." If you can't finish the sentence, don't type. |
| 2 | **Write the recurrence as plain recursion** | Split on the **last choice** (last hop, last house, last item, last character, first cut). Correct and exponential. |
| 3 | **Add the memo** | `@lru_cache(None)`. Now polynomial. Nothing else changes. |
| 4 | **Flip to a table, then shrink** | the five questions below, then "how far back does a cell read?" |

**The five questions that flip any memo into a table (EP176):**

1. What are the memo's arguments and their ranges? → the table's **shape**.
2. Shift indices so the base case is a real cell (`dp[0]` = the empty prefix).
3. Base cases → the first cells you write.
4. Which cells does a cell read? → fill those **first** (left to right, row by row, by
   length).
5. Where was the original call? → that cell is the answer (or `max` over cells, for LIS).

**Then shrink:** reads two back → two variables. Reads one row → one row (backwards if
the left read must be the old row, as in knapsack; forwards if it must be the new row,
as in Unique Paths). Reads everything → you can't shrink; maybe change the state (LIS).

## 💡 Recognition checklist

| if the problem says... | think |
|---|---|
| "number of ways", "how many" | DP, counting (`+`), base = 1 way to do nothing |
| "minimum / maximum cost, profit, length" | DP, optimising (`min`/`max`) |
| "is it possible", "can you" | DP, boolean (`or`), or maybe greedy |
| **take or skip** each item, with a budget | Shape B, knapsack |
| **subsequence** | Shape C (one sequence) or D (two) |
| two strings compared position by position | Shape D |
| grid, moves right/down | Shape D (grid) |
| order of operations matters, each splits a range | Shape E, interval |
| day by day with a mode (holding, cooling down) | Shape A with a state machine (EP184) |
| **"return all"** of them | **not DP**: backtracking, Pattern 12 |
| a local choice is provably safe | **not DP**: greedy |
| **contiguous** subarray, one running value | **not DP (well, Kadane)**: Pattern 04 |

**When the answer is wrong on a small case:** the state is too small. Ask "what does
step `i` need to know that my state doesn't tell it?" and add that dimension (House
Robber's reach to `i-2`, LIS's "ending at i", Stock's "am I holding").

## 🔍 The whole pattern in one table

| EP | problem | shape | state `dp[...]` means | transition | base | time · space |
|---|---|---|---|---|---|---|
| 172 | Fibonacci | A | `f(k)`: k-th Fibonacci | `f(k-1) + f(k-2)` | `f(0)=0, f(1)=1` | O(n) · O(1) |
| 173 | Climbing Stairs | A | ways to reach step i | `w(i-1) + w(i-2)` | `w(0)=w(1)=1` | O(n) · O(1) |
| 174 | House Robber | A | best from houses 0..i | `max(f(i-1), f(i-2) + nums[i])` | `f(<0) = 0` | O(n) · O(1) |
| 175 | 0/1 Knapsack (memo) | B | best value, first i items, capacity c | `max(skip, take)` if it fits | `best(0, c) = 0` | O(nW) · O(nW) |
| 176 | Tabulation Intro | method | House Robber as `dp[k]` = first k houses | `max(dp[k-1], dp[k-2] + nums[k-1])` | `dp[0]=0, dp[1]=nums[0]` | O(n) · O(n) → O(1) |
| 177 | 0/1 Knapsack (table) | B | best value at capacity c | `max(dp[c], dp[c-w] + v)`, **backwards** | row of 0s | O(nW) · O(W) |
| 178 | Subset Sum | B | can I make exactly c? | `dp[c] or dp[c-x]`, backwards | `dp[0] = True` | O(n·S) · O(S) |
| 179 | Target Sum | B | number of subsets summing to c | `dp[c] + dp[c-x]`, backwards, `P = (total+target)/2` | `dp[0] = 1` | O(n·S) · O(S) |
| 180 | LIS (memo) | C | longest increasing ending **exactly at i** | `1 + max(end_at(j))`, `j < i`, `nums[j] < nums[i]` | each = 1 | O(n²) · O(n) |
| 181 | LIS (table, tails) | C | `tails[k]`: smallest end of a length-(k+1) run | `bisect_left`, append or replace | empty | O(n log n) · O(n) |
| 182 | LCS | D | LCS of `a[:i]`, `b[:j]` | match: `↖ + 1`, else `max(↑, ←)` | row/col 0 = 0 | O(mn) · O(min(m,n)) |
| 183 | Unique Paths | D (grid) | paths to cell (r, c) | `↑ + ←` | border = 1 | O(mn) · O(n) |
| 184 | Buy Sell Stock I to IV | A + state | best cash on day, holding or not, t trades | rest or cross: `hold+p`, `free-p` | `hold = -∞, free = 0` | O(nk) · O(k) |
| 185 | Cut a Stick | E | min cost to finish all cuts in `[l, r]` | `len + min(dp[l][k] + dp[k][r])` | adjacent marks = 0 | O(m³) · O(m²) |

## ✅ Drills: name the pattern, then the shape
Problems we haven't solved. Pause after each one, say the pattern and (if DP) the state
in one sentence, then check. The answers are below the table on purpose.

| # | problem |
|---|---|
| 1 | Coin Change: fewest coins to make an amount, unlimited coins of each kind |
| 2 | Coin Change II: number of combinations of coins that make an amount |
| 3 | Return every subset of `nums` whose sum is `target` |
| 4 | Largest sum of any contiguous subarray |
| 5 | Edit Distance: min inserts, deletes, replaces to turn one word into another |
| 6 | Longest Palindromic Subsequence of a string |
| 7 | Can the array be split into two parts with equal sums? |
| 8 | Jump Game: can you reach the last index (each value = max jump length)? |
| 9 | Minimum Path Sum in a grid, moving right or down |
| 10 | Burst Balloons: order of bursting changes the coins you earn |
| 11 | Longest substring without repeating characters |
| 12 | Decode Ways: count decodings of a digit string, 'A'=1 .. 'Z'=26 |

**Answers:**

| # | pattern | the state, in one sentence |
|---|---|---|
| 1 | DP, Shape B, **unbounded** knapsack | `dp[c]` = fewest coins for amount c; `min(dp[c], dp[c-coin] + 1)` with the loop **forwards** (reuse allowed) |
| 2 | DP, Shape B, unbounded, counting | `dp[c] += dp[c-coin]`, coins in the **outer** loop so each combination is counted once, `dp[0] = 1` |
| 3 | **Not DP.** Backtracking (Pattern 12) | "return every" means the output is exponential. EP119's `start` index. |
| 4 | **Kadane** (Pattern 04, EP33) | contiguous, one running value. (Technically a 1-state DP.) |
| 5 | DP, Shape D | `dp[i][j]` = edits for `a[:i]` → `b[:j]`; match: diagonal, else 1 + min of three neighbours |
| 6 | DP, Shape D (or E) | LCS of `s` and `reversed(s)`; or interval `dp[l][r]` over the string |
| 7 | DP, Shape B | Subset Sum (EP178) with target `total / 2`, after checking total is even |
| 8 | **Greedy** | track the farthest reachable index. DP works but is O(n²) for no reason: a local choice is safe. |
| 9 | DP, Shape D (grid) | Unique Paths with `min(↑, ←) + grid[r][c]` instead of a sum |
| 10 | DP, Shape E | interval `dp[l][r]` with `k` = the **last** balloon burst in the range |
| 11 | **Sliding window** (Pattern 03, EP25) | contiguous, "longest", a window that shrinks when a letter repeats |
| 12 | DP, Shape A | Climbing Stairs where a 1-hop needs a non-zero digit and a 2-hop needs 10..26 |

## ⚠️ The mistakes worth one more look
- **The state is too small** (the real bug behind most wrong answers). Add the missing
  dimension; don't patch the loop.
- **Knapsack inner loop direction.** Backwards = each item once. Forwards = unlimited.
- **The empty prefix.** `dp[0]` is "nothing yet", so row `i` compares `a[i-1]`.
- **The answer isn't always the last cell.** LIS is `max(dp)`. Kadane is the max too.
- **"Return all" is never DP.** If the output is exponential, no table helps.

## 🎤 Interview talking points
- *"Let me say the state in one sentence before I write anything."* ← the single
  highest-value habit from this pattern.
- *"I'll write the recursion first, memoise it, then convert to a table if we need the
  space or the recursion depth."*
- *"This cell reads the previous row only, so I can keep one row; I'll loop backwards
  so each item is used once."*
- *"If the output were every solution, I'd backtrack instead; DP only helps when the
  answer is a number, a yes/no, or one best choice."*

## 🔗 Transfer: the end of the series
That's 186 episodes and 15 patterns: Two Pointers through DP. Most of the later
patterns were earlier ones with more state. Sliding Window was Two Pointers with a
rule, Kadane was DP with one number, Backtracking was Recursion with an undo, and DP
was Backtracking where the subproblems came back. If one idea from the whole series
sticks, make it the one this pattern opened with: **name the state, and the code
follows.**

What to do with it now: go back to Pattern 01 and re-solve from a blank file, one
problem a day, with no sheet open. The `reps` column in the progress sheet is there for
exactly that. The second pass is where it becomes yours.

## 📹 Metadata
- **Title:** `All of Dynamic Programming in 5 shapes (and the end of the series) | DP #15`
- **Thumbnail:** `5 SHAPES · 1 METHOD`
- **Short:** the drills: problem on screen, 3-second pause, the shape appears. Six
  drills, 60s.
