# EP114 · P12E04 · Sum of Digits of a Number   [Easy]

**Pattern:** Recursion and Backtracking · **Link:** https://www.geeksforgeeks.org/problems/sum-of-digits1742/1

---

## 🎬 Hook
> "Sum the digits of 345. You don't need a string, a list or a loop: `345 % 10` is the
> last digit and `345 // 10` is everything else. **One step of work plus the smaller
> call.** This is the purest recursion in the series, and it's the one to trace by hand
> once so you never have to trace one again."

## 📋 Problem, in your words
```
Given a non-negative integer n, return the sum of its decimal digits.
Solve it recursively.
```

## 🔢 The example
```
Input:  345      -> 12     (3 + 4 + 5)
Input:  1000     -> 1      <- the zeros still get peeled, they just add 0
Input:  7        -> 7      <- one digit: the answer is itself
Input:  0        -> 0
```

## 🧸 ELI5
> Someone hands you a long number on a strip of paper and asks for the sum of its
> digits. You tear off the **last** digit, keep it in your hand, and pass the rest of
> the strip to a friend with the same question.
>
> ```
> 3 4 5    keep 5, pass "34"
> 3 4      keep 4, pass "3"
> 3        one digit: the answer is 3
> ```
>
> Now the answers come back: your friend's friend says 3, your friend adds their 4
> and says 7, you add your 5 and say **12**. Everyone did one addition.

## 🐌 Brute force (say it, don't type it)
Two honest non-recursive answers:

```python
return sum(int(d) for d in str(n))     # string version
```
```python
total = 0
while n:
    total += n % 10
    n //= 10
return total                           # arithmetic loop, O(1) space
```

The recursive version is exactly the arithmetic loop, with each iteration turned into a
stack frame. That's the point: **a loop that peels one piece and continues on the rest
is a recursion in disguise**, and this is the example small enough to see it.

## 💡 The pattern reveal
**Signal:** the input shrinks naturally, a number minus its last digit is a smaller
number of the same kind.
**Therefore:** Shape A, the exact code on the pattern card.

| question | answer here |
|---|---|
| smallest input, answered without recursing? | a single digit, `n < 10` → `n` |
| one step of work | `n % 10`, the last digit |
| the smaller call | `sum_of_digits(n // 10)`, everything but the last digit |

**Key insight: the leap of faith.** Don't follow `sum_of_digits(n // 10)` down in your
head. Assume it returns the right digit sum of 34. Then is `5 + (digit sum of 34)` the
digit sum of 345? Yes. That's the whole proof. Do the trace below **once** to believe
it; after that, trust it.

## 🔍 Dry run: `n = 345`, the call stack

| step | stack (top on the right) | n | event | returns |
|---|---|---|---|---|
| 1 | D(345) | 345 | keep 5, call D(34) | |
| 2 | D(345) D(34) | 34 | keep 4, call D(3) | |
| 3 | D(345) D(34) D(3) | 3 | `n < 10`, base case | **3** |
| 4 | D(345) D(34) | | 4 + 3 | **7** |
| 5 | D(345) | | 5 + 7 | **12** |

Going **down**, each frame is waiting with one digit in its hand. Going **up**, each
frame does its one addition. The additions happen in reverse order of the calls, and
that "work on the way back up" is the idea EP115 is built on.

## ✅ Optimal solution
```python
def sum_of_digits(n: int) -> int:
    """Sum of the decimal digits of a non-negative integer, recursively.

    Time:  O(d), d = number of digits = O(log10 n). One call per digit.
    Space: O(d), the call stack is d frames deep.
    """
    if n < 10:                              # one digit: the answer is itself
        return n
    return n % 10 + sum_of_digits(n // 10)  # last digit + trust the smaller call
```
**Time:** O(log n) · **Space:** O(log n) call stack

## ⚠️ Gotchas
- **The complexity is in digits, not in n.** One call per digit means O(log₁₀ n). Saying
  "O(n)" here is a common slip; n is the *value*, not the length.
- **`//`, not `/`.** `345 / 10` is `34.5` in Python 3, and the recursion never hits an
  integer base case cleanly.
- **Base case `n < 10`, not `n == 0`.** Both work (`n == 0 → 0` peels one extra level),
  but `n < 10` says what you mean: a single digit is its own sum. Check `0` either way.
- **Negative input.** `-345 < 10` is already true, so the function returns `-345`
  without recursing. Wrong. The problem says non-negative; if asked, recurse on
  `abs(n)`.
- **Depth is tiny.** A 64-bit integer has at most 20 digits, so the recursion limit
  never matters here. Say that: it's the one Pattern 12 warm-up where recursion costs
  you nothing real.

## 🎤 Interview talking points
- *"`n % 10` is the last digit and `n // 10` is the rest, so it's one step of work plus
  the call on a smaller number."*
- *"I don't trace the call; I assume it returns the right sum for the smaller number and
  check that adding the last digit is correct."* ← the leap of faith, said out loud.
- *"It's O(number of digits), which is O(log n) in the value."*
- *"The iterative version is the same arithmetic with a running total and O(1) space."*

## 🔗 Transfer
The trace here, frames holding a value going down and combining it going up, is the
picture to keep. EP115 makes the "going up" half do real work: the frames **rebuild a
string** on the way back. Pattern 13 (Tree) is this exact picture with two children
instead of one: EP139 Maximum Depth is `1 + max(left, right)` built on the way up.

## 📹 Metadata
- **Title:** `Sum of digits, the leap of faith | Recursion #4`
- **Thumbnail:** `345 → 5 + f(34)`
- **Short:** tearing digits off a paper strip, then the answers coming back up the
  line: 3, 7, 12. 40s.
