# EP172 · P15E01 · Fibonacci   [Easy]

**Pattern:** DP (Dynamic Programming) · **Link:** https://leetcode.com/problems/fibonacci-number/description/

---

## 🎬 Hook
> "You already solved this one. EP111, three lines of recursion. For n = 30 those three
> lines made **2,692,537 calls**. Today we add one line and it makes **59**. That one
> line has a name, and the name is the whole of this pattern: **dynamic programming**."

## 📋 Problem, in your words
```
F(0) = 0, F(1) = 1, F(n) = F(n - 1) + F(n - 2).
Given n (0 <= n <= 30), return F(n).

Same problem as EP111. This time the question isn't "can you recurse",
it's "why is the recursion slow, and what's the general cure".
```

## 🔢 The example
```
n:     0  1  2  3  4  5  6  7   8
F(n):  0  1  1  2  3  5  8  13  21

Input:  n = 5   -> 5
Input:  n = 0   -> 0      <- base case
Input:  n = 30  -> 832040
```

## 🧸 ELI5
> Your teacher asks the class "what's F(5)?" and the rule is: to answer F(k), you must ask
> two classmates for F(k-1) and F(k-2). Without notes, the classroom explodes: someone is
> asked F(2) three separate times and works it out from scratch every time.
>
> Now put a **whiteboard** at the front. The first time anyone works out an answer, they
> write it up. Before starting any work, you look at the board first.
>
> ```
> no whiteboard (EP111):              with whiteboard (today):
>
>             F5                                 F5
>          /      \                            /    \
>        F4        F3                        F4     [F3]  <- read off the board
>       /  \      /  \                      /  \
>     F3    F2   F2   F1                  F3   [F2]       <- read off the board
>    /  \   / \  / \                     /  \
>   F2  F1 F1 F0 F1 F0                  F2   F1
>  /  \                                /  \
> F1  F0                              F1   F0
>
>  15 calls                             9 calls, a straight spine
> ```
>
> The tree collapses to a **line**. That whiteboard is the memo. Everything in Pattern 15
> is "what do we write on the whiteboard, and under what label".

## 🐌 Brute force (say it, don't type it)
The EP111 recursion without a memo: correct, **O(2ⁿ)**. Every call spawns two, and the
same subproblems (F(2), F(3), ...) are recomputed in every branch that reaches them.
The work isn't hard, it's **repeated**. That's the diagnosis DP exists to treat.

| n | calls, no memo | calls, memo |
|---|---|---|
| 5 | 15 | 9 |
| 10 | 177 | 19 |
| 20 | 21,891 | 39 |
| 30 | 2,692,537 | 59 |

The memo column is `2n - 1`: each F(k) is computed once and asked for at most twice.

## 💡 The pattern reveal
**Signal:** the recursion's call tree has **repeated nodes**. Same arguments, same answer,
computed again.
**Therefore:** DP. Run the four steps from the pattern card, for the first time.

| step | Fibonacci |
|---|---|
| 1. the state, in words | `f(k)` = the k-th Fibonacci number. One number describes the subproblem. |
| 2. the recurrence as plain recursion | `f(k) = f(k-1) + f(k-2)`, base `f(0)=0, f(1)=1` |
| 3. add the memo | `@lru_cache(None)`: O(2ⁿ) → O(n) |
| 4. flip to a table, then shrink | `dp[k] = dp[k-1] + dp[k-2]` left to right; only two cells are ever read, so two variables |

**Key insight:** DP has two ingredients and Fibonacci has both, in their plainest form.
**Overlapping subproblems** (F(3) is needed by F(5) and by F(4)) is why a memo helps.
**Optimal substructure** (F(5) is built *only* from F(4) and F(3)) is why the memo's
answers can be trusted. Spot both and you've spotted DP.

## 🔍 Dry run: `n = 5`, memoised, in call order

| step | call | event | memo after |
|---|---|---|---|
| 1 | F5 | not on the board, compute: call F4 | {} |
| 2 | F4 | compute: call F3 | {} |
| 3 | F3 | compute: call F2 | {} |
| 4 | F2 | compute: F1 = 1, F0 = 0 (base cases) | {} |
| 5 | F2 | returns 1 + 0 = **1**, write it | {2:1} |
| 6 | F3 | F1 = 1 (base), returns 1 + 1 = **2** | {2:1, 3:2} |
| 7 | F4 | asks F2: **on the board**, 1, no calls | {2:1, 3:2} |
| 8 | F4 | returns 2 + 1 = **3** | {2:1, 3:2, 4:3} |
| 9 | F5 | asks F3: **on the board**, 2, no calls | {2:1, 3:2, 4:3} |
| 10 | F5 | returns 3 + 2 = **5** | {2:1, 3:2, 4:3, 5:5} |

Answer **5** ✓. Steps 7 and 9 are the two branches that got pruned in the ELI5 picture.

Now look at the memo's **fill order**: 2, 3, 4, 5. Smallest first. The recursion went
*down* from 5 but wrote answers *up* from 2. Step 4 of the method just writes that order
directly:

| k | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| dp[k] | 0 | 1 | 1 | 2 | 3 | **5** |

Each cell reads the two to its left. Nothing further back is ever read, so keep two.

## ✅ Optimal solution
```python
from functools import lru_cache


class Solution:
    def fib(self, n: int) -> int:
        """F(n) by memoised recursion: step 3 of the DP method.

        Time:  O(n), each of F(0)..F(n) is computed once, every other request is a lookup.
        Space: O(n), the memo plus a call stack n deep.
        """

        @lru_cache(maxsize=None)
        def f(k: int) -> int:
            if k < 2:                     # F(0) = 0, F(1) = 1
                return k
            return f(k - 1) + f(k - 2)    # unchanged from EP111: the memo is the only edit

        return f(n)
```

And step 4, rolled all the way down:

```python
class Solution:
    def fib(self, n: int) -> int:
        """F(n) bottom-up, keeping only the two cells the recurrence reads.

        Time:  O(n), one pass from 2 to n.
        Space: O(1), two variables.
        """
        prev2, prev1 = 0, 1               # F(0), F(1)
        for _ in range(n):
            prev2, prev1 = prev1, prev2 + prev1
        return prev2                      # after n shifts, prev2 holds F(n)
```
**Time:** O(n) · **Space:** O(n) memoised, O(1) rolled

## ⚠️ Gotchas
- **The memo is the only change.** If adding memoisation made you rewrite the recursion,
  the recursion wasn't pure: it depended on something other than its arguments. A
  function you can memoise must return the same answer for the same arguments, every time.
- **`return prev2`, not `prev1`, in the loop version.** After n shifts `prev2` is F(n)
  and `prev1` is F(n+1). Check with n = 0: the loop doesn't run, and you must return 0.
- **Memo space is O(n) because of the stack too.** Even with a dictionary the recursion
  still goes n deep. Python's limit (~1000) makes the memo version crash for big n; the
  loop never does.
- **Don't call the naive version "O(n²)".** It's exponential: the tree doubles every
  level. The memo is what makes it linear.

## 🎤 Interview talking points
- *"The naive recursion recomputes the same subproblems, F(3) appears in several
  branches. That's overlapping subproblems, so I memoise."*
- *"Memoised, each F(k) is computed once: O(n) time, O(n) space."*
- *"The memo fills smallest-first, so I can fill a table left to right instead. And
  since each cell reads only the two before it, two variables are enough: O(1) space."*
- *"Recursion, memo, table, rolling variables. I'll use those four steps on every DP
  problem."* ← announces a method, not a trick.

## 🔗 Transfer
EP111 taught the recursion; this episode teaches what's wrong with it and the cure. The
four steps you just did are the template for all fifteen episodes. EP173 Climbing Stairs
is this exact recurrence hidden inside a word problem, and the whole job there is
*finding* it. EP176 comes back to step 4 and does the memo-to-table flip slowly.

## 📹 Metadata
- **Title:** `Fibonacci, 2.7 million calls to 59 with one line | DP #1`
- **Thumbnail:** `2,692,537 → 59`
- **Short:** the F(5) call tree drawn in full, then the memo'd branches greying out until
  only the spine is left. 40s.
