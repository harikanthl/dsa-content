# EP111 · P12E01 · Fibonacci Number   [Easy]

**Pattern:** Recursion and Backtracking · **Link:** https://leetcode.com/problems/fibonacci-number/description/

---

## 🎬 Hook
> "Fibonacci is three lines of recursion, and those three lines make almost **three million
> calls** for n = 30. Everything you need to know about recursion is in why that
> happens: the leap of faith that makes it easy to write, the call tree that makes it
> slow, and the one-line memo that makes it fast."

## 📋 Problem, in your words
```
F(0) = 0, F(1) = 1, and every later number is the sum of the two before it:
F(n) = F(n - 1) + F(n - 2).

Given n (0 <= n <= 30), return F(n).
```

## 🔢 The example
```
n:     0  1  2  3  4  5  6  7   8
F(n):  0  1  1  2  3  5  8  13  21

Input:  n = 4   -> 3
Input:  n = 0   -> 0     <- base case, no recursion at all
Input:  n = 1   -> 1     <- the other base case
```

## 🧸 ELI5
> You want to know how many rabbits are in the field this month. You don't count them.
> You ask two helpers: "how many were here last month?" and "how many the month
> before?" and add the answers.
>
> Each helper does exactly the same thing: asks two more helpers. The only helpers
> who answer straight away are the ones asked about month 0 and month 1. They just
> *know*.
>
> ```
>              F(4)
>            /      \
>         F(3)       F(2)
>        /    \      /   \
>     F(2)   F(1)  F(1)  F(0)
>     /  \
>  F(1)  F(0)
> ```
>
> Look at the picture. **F(2) got asked twice.** Nobody wrote the answer down, so two
> separate helpers worked it out from scratch. At n = 30 that waste is the whole run
> time.

## 🐌 Brute force (say it, don't type it)
The honest baseline here is **the loop**, and it's better than anything recursive:

```python
a, b = 0, 1
for _ in range(n):
    a, b = b, a + b
return a
```

O(n) time, **O(1)** space, no call stack. In production you'd write this and move on.

So why an episode on the recursive version? Because EP111 to EP115 are the warm-up.
They exist to build one reflex, **trust the smaller call**, on problems small enough
that you can check it by hand. EP116 to EP120 (Generate Parentheses through
Palindrome Partitioning) have no loop version you'd want to write, and you'll need the
reflex to already be there.

## 💡 The pattern reveal
**Signal:** the problem is **defined by a smaller version of itself**. The statement
literally gives you the recurrence.
**Therefore:** Shape A from the pattern card, a base case plus smaller calls.

Two questions, answered before any code:

| question | answer here |
|---|---|
| what's the smallest input, and its answer *without recursing*? | `n = 0 -> 0`, `n = 1 -> 1` (both, or F(1) calls F(-1)) |
| how does the answer for n follow from smaller answers? | `F(n - 1) + F(n - 2)` |

**Key insight:** Fibonacci is the one Shape A problem with **two** smaller calls, and
two calls per level is what makes the call tree double at every level: **O(2ⁿ)**. The
fix isn't a different algorithm. It's writing each answer down the first time you
compute it, a **memo**, so the second request for F(2) is a lookup. That turns 2ⁿ
calls into n + 1 distinct ones.

Hold on to that idea. It comes back as the entire first half of Pattern 15: EP172 is
this same problem, taught as DP.

## 🔍 Dry run: `n = 4`, memoised, the call stack

Each row is one moment. "Down" means a frame is pushed; "up" means it returns.

| step | stack (top on the right) | event | memo after |
|---|---|---|---|
| 1 | F4 | F4 calls F3 | {} |
| 2 | F4 F3 | F3 calls F2 | {} |
| 3 | F4 F3 F2 | F2 calls F1 | {} |
| 4 | F4 F3 F2 F1 | base case, returns **1** | {} |
| 5 | F4 F3 F2 F0 | base case, returns **0** | {} |
| 6 | F4 F3 F2 | returns 1 + 0 = **1** | {2: 1} |
| 7 | F4 F3 F1 | base case, returns **1** | {2: 1} |
| 8 | F4 F3 | returns 1 + 1 = **2** | {2: 1, 3: 2} |
| 9 | F4 F2 | **memo hit**, returns 1 with no calls | {2: 1, 3: 2} |
| 10 | F4 | returns 2 + 1 = **3** | {2: 1, 3: 2, 4: 3} |

Answer **3** ✓. Step 9 is the whole lesson: without the memo, that row expands into
another F1 and F0. The stack never got deeper than **4 frames + the base**, which is
the O(n) space.

## ✅ Optimal solution
```python
from functools import lru_cache


class Solution:
    def fib(self, n: int) -> int:
        """The n-th Fibonacci number, by memoised recursion.

        Time:  O(n), each of F(0)..F(n) is computed once, then looked up.
        Space: O(n), the memo holds n + 1 entries and the call stack is n deep.
        """

        @lru_cache(maxsize=None)
        def f(k: int) -> int:
            if k < 2:                  # F(0) = 0, F(1) = 1: answer by looking
                return k
            return f(k - 1) + f(k - 2) # trust both smaller calls

        return f(n)
```
**Time:** O(n) · **Space:** O(n)

Without `@lru_cache`, the same function is **O(2ⁿ)** time and still O(n) space: the
tree is huge, but only one branch of it is on the stack at a time.

## ⚠️ Gotchas
- **Both base cases.** `if k == 0: return 0` alone means `f(1)` calls `f(0)` and
  `f(-1)`, and `f(-1)` recurses forever. `if k < 2: return k` covers both in one line.
- **The un-memoised version is O(2ⁿ), not O(n²).** People guess n² because "it's two
  calls". State it properly: the tree doubles per level. At n = 30 that's about 2.7
  million calls, still under LeetCode's limit, which is why the naive version passes
  and why you must *say* it's exponential anyway. (The tight bound is O(φⁿ), about
  1.618ⁿ, because the F(n-2) side is shorter. O(2ⁿ) is the upper bound everyone
  quotes, and it's the one to say unless asked for the tight one.)
- **Space is O(n) even without the memo.** The stack depth is the longest root-to-leaf
  path, F(n), F(n-1), ..., F(1), not the size of the tree.
- **`lru_cache` on a method** caches on `self` too and keeps the object alive. Putting
  it on an inner function, as above, keeps the cache per call.
- **Python's recursion limit is about 1000.** Fine for n ≤ 30. For n = 10,000 the
  recursive version raises `RecursionError`, and that's the moment to say "and this is
  why I'd write the loop."

## 🎤 Interview talking points
- *"The recurrence is given, so the base cases are the only design decision: I need
  both F(0) and F(1), or F(1) walks off the end."*
- *"Plain recursion is O(2ⁿ) because every call makes two calls; the tree doubles each
  level."* ← say "doubles", not "it's slow".
- *"The same subproblems repeat, F(2) is computed many times, so I memoise. That's O(n)
  time and O(n) space."*
- *"Space is O(n) either way, because it's the stack depth, not the number of calls."*
- *"In production I'd write the two-variable loop: O(n) time, O(1) space, no recursion
  limit."* ← shows you know when *not* to recurse.

## 🔗 Transfer
This is the only episode in Pattern 12 with two smaller calls. EP112 to EP115 go back
to **one** smaller call, and practise the other half of the skill: choosing *what*
"smaller" means (shrink from both ends in EP112, advance an index in EP113, drop a
digit in EP114). The memo idea leaves here and returns at EP172, where Fibonacci opens
Dynamic Programming and "write the answer down" gets a name.

## 📹 Metadata
- **Title:** `Fibonacci, why 3 lines make 3 million calls | Recursion #1`
- **Thumbnail:** `F(2) TWICE?` (call tree with the repeat circled)
- **Short:** the call tree for F(4) growing on screen, F(2) highlighted twice, then the
  memo turning the second one into a lookup. 45s.
