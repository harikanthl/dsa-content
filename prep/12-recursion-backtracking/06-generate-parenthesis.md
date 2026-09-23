# EP116 · P12E06 · Generate Parentheses   [Medium]

**Pattern:** Recursion and Backtracking · **Link:** https://leetcode.com/problems/generate-parentheses/description/

---

## 🎬 Hook
> "Every valid bracket string of length 2n, and you never build a single invalid one.
> The whole trick is two `if` statements that stop you walking down dead corridors,
> and one of them is written wrong by almost everyone the first time: it's
> `close < open`, not `close < n`."

## 📋 Problem, in your words
```
Given n pairs of parentheses, return every string of length 2n
that is a well-formed bracket sequence.

Order of the output doesn't matter.
1 <= n <= 8
```

## 🔢 The example
```
n = 1  ->  ["()"]
n = 2  ->  ["(())", "()()"]
n = 3  ->  ["((()))", "(()())", "(())()", "()(())", "()()()"]
```
Five answers for n = 3, fourteen for n = 4. Those are the Catalan numbers, and the
count is the first clue that we are not generating all 2^(2n) strings.

## 🧸 ELI5
> You're laying bricks in a row, and each brick is either an opener `(` or a closer `)`.
> You have exactly n of each. Two rules keep the wall standing:
>
> 1. You can lay an opener as long as you **have openers left** (`open < n`).
> 2. You can lay a closer only if there's an **unclosed opener waiting** for it
>    (`close < open`).
>
> ```
> path so far:  ( ( )
> open = 2, close = 1
>
> lay "(" ?  open 2 < n=3   yes
> lay ")" ?  close 1 < open 2  yes, the second "(" is still waiting
> ```
>
> Follow those two rules and every wall you finish is valid. You never have to check
> anything at the end.

## 🐌 Brute force (say it, don't type it)
Generate all 2^(2n) strings of `(` and `)`, then keep the ones that pass EP59's
validity check. For n = 8 that's 65,536 strings to find 1,430 answers. **O(2^(2n) · n)**.
Worth saying out loud, because the optimal solution is exactly this with the invalid
branches cut off **before** they're built, instead of filtered after.

## 💡 The pattern reveal
**Signal:** "return **all** valid …" and a tiny n (≤ 8).
**Therefore:** backtracking, build-by-position flavour: at each depth, choose the next
character.

**Key insight:** validity can be enforced *while building*, one character at a time.
A prefix is still completable exactly when `open <= n` and `close <= open`. So those
become the conditions for being allowed to take a step:

```python
if open < n:                 # an opener is still available
    choose "(" ; explore ; unchoose
if close < open:             # some opener is waiting to be closed
    choose ")" ; explore ; unchoose
```

**The trap: `close < n` instead of `close < open`.** `close < n` lets you lay `)` first
and builds `")("`, which is invalid. The closer's budget isn't n, it's however many
openers are currently unmatched.

## 🔍 Dry run: n = 2

| depth | path | open | close | try `(`? | try `)`? |
|---|---|---|---|---|---|
| 0 | `""` | 0 | 0 | 0 < 2 ✓ | 0 < 0 ✗ pruned |
| 1 | `(` | 1 | 0 | 1 < 2 ✓ | 0 < 1 ✓ |
| 2 | `((` | 2 | 0 | 2 < 2 ✗ pruned | 0 < 2 ✓ |
| 3 | `(()` | 2 | 1 | ✗ pruned | 1 < 2 ✓ |
| 4 | `(())` | 2 | 2 | **complete, record** | |
| 2 | `()` | 1 | 1 | 1 < 2 ✓ | 1 < 1 ✗ pruned |
| 3 | `()(` | 2 | 1 | ✗ pruned | 1 < 2 ✓ |
| 4 | `()()` | 2 | 2 | **complete, record** | |

```
                 ""
                 |
                "("            <- ")" never tried: close would exceed open
              /      \
           "(("      "()"      <- "(((" never tried: open would exceed n
            |          |
          "(()"      "()("
            |          |
         "(())"     "()()"     <- both leaves are answers
```

Every leaf is an answer. Zero wasted leaves: that is what pruning buys.

## ✅ Optimal solution
```python
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        """Every well-formed string of n bracket pairs.

        Time:  O(4^n / sqrt(n)), the nth Catalan number of leaves, O(n) to join each.
        Space: O(n) for the recursion and path, excluding the output.
        """
        result, path = [], []

        def backtrack(open_used: int, close_used: int) -> None:
            if len(path) == 2 * n:                 # complete
                result.append(''.join(path))       # join makes a copy
                return
            if open_used < n:                      # an opener is still available
                path.append('(')                   # choose
                backtrack(open_used + 1, close_used)   # explore
                path.pop()                         # unchoose
            if close_used < open_used:             # an opener is waiting
                path.append(')')
                backtrack(open_used, close_used + 1)
                path.pop()

        backtrack(0, 0)
        return result
```
**Time:** O(4ⁿ / √n) · **Space:** O(n) excluding the output

## ⚠️ Gotchas
- **`close < open`, not `close < n`.** The second one generates `")("` and every other
  string that closes before it opens. Test with n = 1: the wrong version returns
  `["()", ")("]`.
- **`''.join(path)`, not `path`.** Appending the list itself stores a reference to the
  one list you keep mutating, and by the end every entry is empty. `join` makes a new
  string, so the copy is free here.
- **Pop after each call, both branches.** Forget the pop after the `(` branch and the
  `)` branch starts from a path with an extra `(` in it.
- **Two `if`s, not `if/elif`.** From most prefixes *both* moves are legal, and both
  subtrees need exploring. `elif` silently drops half the answers.
- **Don't validate at the leaf.** If the guards are right, every leaf is valid.
  Checking at the end means you built the dead branches first.

## 🎤 Interview talking points
- *"Instead of generating 2^(2n) strings and filtering, I only take a step that keeps
  the prefix completable, so every leaf is an answer."*
- *"Openers are limited by n; closers are limited by how many openers are unmatched,
  that's `close < open`."* ← say this unprompted, it's the trap.
- *"The number of answers is the nth Catalan number, about 4ⁿ / n^1.5, and each costs
  O(n) to build, so O(4ⁿ / √n)."*
- *"Space is O(n) for the recursion, excluding the output."*
- *"This is DFS on an implicit tree where the nodes are prefixes."*

## 🔗 Transfer
EP59 checked a bracket string after the fact; this builds only the ones that would
pass. The template here (choose, explore, unchoose, with pruning before descending)
is reused unchanged in EP117, where a keypad lookup supplies the choices, and in
EP118, where the choices are whatever hasn't been used yet.

## 📹 Metadata
- **Title:** `Generate Parentheses, never build an invalid string | Backtracking #1`
- **Thumbnail:** `CLOSE < OPEN` (red block)
- **Short:** the n = 1 run with `close < n` producing `")("`, then the one-word fix. 40s.
