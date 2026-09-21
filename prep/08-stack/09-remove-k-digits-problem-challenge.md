# EP066 · P08E09 · Remove K Digits (Problem Challenge)   [Hard]

**Pattern:** Stack · **Link:** https://leetcode.com/problems/remove-k-digits/

---

## 🎬 Hook
> "Delete exactly k digits to make the number as small as possible. The greedy rule is
> one sentence — *whenever a digit is followed by a smaller one, delete it* — and that
> is a monotonic stack with a **budget**. Then three loose ends decide whether you pass:
> leftover budget, leading zeros, and the empty string."

## 📋 Problem, in your words
```
Given a string num representing a non-negative integer and an integer k,
remove exactly k digits so the resulting number is as SMALL as possible.
Return it as a string.

The remaining digits keep their original ORDER -- you are choosing a
subsequence, not rearranging.

No leading zeros in the answer, and if everything is removed the answer
is "0".
```

## 🔢 The example
```
Input:  num = "1432219", k = 3     Output: "1219"
Why:    remove 4, 3 and 2 -> 1219, the smallest 4-digit subsequence.

Input:  num = "10200", k = 1       Output: "200"
Why:    remove the 1 -> "0200" -> strip the leading zero -> "200"

Input:  num = "10", k = 2          Output: "0"       <- everything removed
Input:  num = "112", k = 1         Output: "11"      <- nothing is ever "bigger than next"
```
Those last two are the loose ends. `"112"` never triggers a single greedy deletion, so
the budget survives the whole loop — and something still has to be removed.

## 🧸 ELI5
> Read the digits left to right, keeping the answer you've built so far in a pile.
>
> The rule: **a digit is worth deleting when the digit after it is smaller**, because
> deleting it lets a smaller digit move into a more significant position — and the
> leftmost positions dominate the value of a number.
>
> ```
> "1432219", k = 3
>
>  1  -> pile: 1
>  4  -> pile: 1 4
>  3  -> 4 > 3, and I still have budget -> DELETE the 4   (k: 3 -> 2)   pile: 1 3
>  2  -> 3 > 2, delete the 3            (k: 2 -> 1)                     pile: 1 2
>  2  -> 2 is not > 2, keep it                                          pile: 1 2 2
>  1  -> 2 > 1, delete the 2            (k: 1 -> 0)                     pile: 1 2 1
>  9  -> no budget left, just keep it                                   pile: 1 2 1 9
> ```
>
> Answer `1219`. Each deletion happened at the **most significant place it could**,
> which is why greedy is correct here: a smaller digit earlier always beats any
> arrangement of the digits behind it.

## 🐌 Brute force (say it, don't type it)
Try every subsequence of length `n − k` and take the smallest. **O(C(n, k))** —
exponential, fine for a 6-digit string, useless beyond. Worth saying because it defines
the answer precisely (*the smallest subsequence of length n−k*), which is the sentence
that makes the greedy argument checkable.

## 💡 The pattern reveal
**Signal:** "remove k to make it smallest" · order preserved.
**Therefore:** a monotonic **increasing** stack with a **budget** of k pops.

**The four decisions:**

| decision | here |
|---|---|
| increasing or decreasing? | we want small digits early → pop while the top is **bigger** → the stack stays **increasing** |
| index or value? | **value** (the digit character) — the output is the stack itself |
| what happens at the pop? | one unit of budget is spent: `k -= 1` |
| what's left at the end? | the answer — **after** three fix-ups |

```python
for d in num:
    while k and stack and stack[-1] > d:
        stack.pop()
        k -= 1
    stack.append(d)
```

**Why greedy is correct**, in one line you can say out loud: among subsequences of the
same length, the one with the smaller digit in the **leftmost differing position** wins
— so removing the first digit that is followed by something smaller is always at least
as good as any alternative.

**🧨 The three loose ends, each one line, each its own wrong answer.**

1. **Leftover budget.** If the digits are non-decreasing (`"112"`), the `while` never
   fires and `k` is still positive at the end. The remaining deletions must come off the
   **back**, because the stack is increasing and the largest digits are last:
   ```python
   if k:
       stack = stack[:-k]
   ```
   Miss this and you return a number that's too long — you were told to remove
   *exactly* k.

2. **Leading zeros.** `"10200"`, k=1 leaves `"0200"`. Strip them:
   ```python
   "".join(stack).lstrip("0")
   ```

3. **The empty string.** `"10"`, k=2 removes everything, and `"".lstrip("0")` is `""`,
   which is not a number. `or "0"` is the whole fix:
   ```python
   return "".join(stack).lstrip("0") or "0"
   ```
   That final `or "0"` also covers `"0000"`, k=0 → `"0"`.

Note the order: **trim, then strip, then default.** Stripping before trimming would
delete zeros you're about to remove anyway and leave the count wrong.

## 🔍 Dry run — `num = "1432219"`, `k = 3`

| digit | pops (budget spent) | `k` left | stack |
|---|---|---|---|
| `1` | — | 3 | `1` |
| `4` | — (4 > 1, so it just sits on top) | 3 | `14` |
| `3` | **pop `4`** | **2** | `13` |
| `2` | **pop `3`** | **1** | `12` |
| `2` | — (top is `2`, not greater) | 1 | `122` |
| `1` | **pop `2`** | **0** | `121` |
| `9` | — (no budget) | 0 | `1219` |

`k = 0`, so no trimming. No leading zero. Answer **`"1219"`** ✓

Row 5 is the `>` vs `>=` question: the top is `2` and the incoming digit is `2`.
**Equal digits must not be popped** — removing one and keeping the other changes
nothing about the value but wastes a unit of budget you'll need later. Here it matters
directly: that budget is spent one row down on the `2` before the `1`.

## 🔍 Dry run — `num = "10200"`, `k = 1` (leading zero)

| digit | pops | `k` left | stack |
|---|---|---|---|
| `1` | — | 1 | `1` |
| `0` | **pop `1`** | **0** | `0` |
| `2` | — | 0 | `02` |
| `0` | — (no budget) | 0 | `020` |
| `0` | — | 0 | `0200` |

Stack is `"0200"`, `k = 0` so nothing to trim, then `.lstrip("0")` → **`"200"`** ✓

## 🔍 Dry run — `num = "112"`, `k = 1` (leftover budget)

| digit | pops | `k` left | stack |
|---|---|---|---|
| `1` | — | 1 | `1` |
| `1` | — (`1 > 1` is false) | 1 | `11` |
| `2` | — | 1 | `112` |

The loop ends with `k = 1` **unspent**. Trim from the back: `stack[:-1]` → **`"11"`** ✓

Removing from the back is right because an increasing stack has its largest digits at
the end — and the least significant positions are the cheapest place to lose digits.

## ✅ Optimal solution
```python
class Solution:
    def removeKdigits(self, num: str, k: int) -> str:
        """Remove exactly k digits to leave the smallest possible number.

        Time:  O(n) — each digit is pushed once and popped at most once.
        Space: O(n) — the stack, which is the answer.
        """
        stack = []                     # digits kept so far, non-decreasing

        for d in num:
            # a bigger digit followed by a smaller one is always worth removing
            while k and stack and stack[-1] > d:
                stack.pop()
                k -= 1                 # one unit of budget spent
            stack.append(d)

        if k:                          # non-decreasing input: budget unspent
            stack = stack[:-k]         # remove from the BACK -- the largest digits

        return "".join(stack).lstrip("0") or "0"   # no leading zeros; "" means 0
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **`stack[-1] > d`, strictly.** Equal digits must stay — popping one wastes budget for
  no gain. `"1432219"` needs that budget two steps later.
- **`while k and stack and …`** — the budget check comes first, and both guards are
  needed. Without `k`, you'd delete more than k digits; without `stack`, `stack[-1]`
  raises on the first digit.
- **Leftover k trims from the back.** `stack[:-k]`, and only inside `if k:` — `stack[:-0]`
  is `stack[:0]`, the empty string, which would wipe out a correct answer. This is the
  sneakiest bug in the problem.
- **`lstrip("0")`, not `int()`.** Converting to int and back loses arbitrary precision
  on long inputs and is the kind of shortcut that fails only on the big test cases.
- **`or "0"` at the very end** for the empty result: `"10"`, k=2 → `"0"`.
- **Order matters: trim → strip → default.** Any other order produces a wrong length or
  a wrong string.
- **`k == len(num)`** must give `"0"`, and the code handles it without a special case —
  run it.

## 🎤 Interview talking points
- *"The answer is the smallest subsequence of length n−k, and greedily removing a digit
  whenever the next one is smaller achieves it — that's a monotonic increasing stack
  with a budget."*
- *"Equal digits don't get popped, because that spends budget without improving the
  number."*
- *"If the input is non-decreasing the budget is never spent, so I trim the last k
  digits — the largest ones sit at the end of an increasing stack."* ← the case most
  people miss.
- *"Then leading zeros, then the empty-string default. Those three fix-ups are where
  this problem is actually won."*
- *"O(n): each digit is pushed once and popped at most once."*

## 🔗 Transfer
That closes Pattern 08, with both halves in one problem: a monotonic stack doing the
greedy work and a cancelling stack's instinct — *what's left is the answer* — doing the
output. The monotonic stack itself returns in **Pattern 15 (DP)** for Largest Rectangle
in a Histogram, which is this same invariant with areas measured at the pop. Next is
**Pattern 09 (Hash Maps, EP67–70)**, four short episodes after nine long ones.

## 📹 Metadata
- **Title:** `Remove K Digits — greedy with a budget | Stack #9`
- **Thumbnail:** `POP WHILE BIGGER` (green block)
- **Short:** `"112"` — the budget nobody spends, and where the digits come off. 50s.
