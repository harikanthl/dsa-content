# EP117 · P12E07 · Letter Combinations of a Phone Number   [Medium]

**Pattern:** Recursion and Backtracking · **Link:** https://leetcode.com/problems/letter-combinations-of-a-phone-number/description/

---

## 🎬 Hook
> "It's EP116's template with the brain removed. There's no pruning at all, every branch
> is an answer, and the only thing that changes is where the choices come from: a
> lookup table. The bug people ship isn't in the recursion. It's what they return for
> an empty string."

## 📋 Problem, in your words
```
Given a string of digits 2-9, return every letter string the
digits could spell on an old phone keypad.

  2: abc   3: def   4: ghi   5: jkl
  6: mno   7: pqrs  8: tuv   9: wxyz

Any order. 0 <= len(digits) <= 4
```

## 🔢 The example
```
"23"  ->  ["ad","ae","af","bd","be","bf","cd","ce","cf"]
"2"   ->  ["a","b","c"]
""    ->  []                    <- not [""]
```
3 × 3 = 9 answers for "23". For "79" it's 4 × 4 = 16. The answer count is the product
of the button sizes, which tells you there is nothing to prune.

## 🧸 ELI5
> A combination lock with one dial per digit. The first dial has the letters of the
> first button, the second dial has the letters of the second button.
>
> ```
> dial 1 (2):  a  b  c
> dial 2 (3):  d  e  f
>
> fix dial 1 on a, spin dial 2:  ad  ae  af
> move dial 1 to b, spin dial 2: bd  be  bf
> move dial 1 to c, spin dial 2: cd  ce  cf
> ```
>
> "Fix one dial, spin the rest" is recursion. Moving dial 1 to the next letter means
> first taking your hand off the current one: that's the unchoose.

## 🐌 Brute force (say it, don't type it)
Nested loops, one per digit. It works for exactly the number of digits you wrote loops
for, and the input length varies. That's the real reason for recursion here: **a
variable number of nested loops.** (`itertools.product(*letters)` does it in one line;
say so, then write the backtracker because that's what's being tested.)

## 💡 The pattern reveal
**Signal:** "return **all** combinations", one choice per position, tiny input.
**Therefore:** backtracking, build-by-position. Depth `i` chooses the letter for digit `i`.

**Key insight:** `available()` from the pattern card is just `keypad[digits[i]]`.
Everything else is EP116's skeleton:

```python
def backtrack(i):
    if i == len(digits):              # every digit has a letter
        record ''.join(path)
        return
    for ch in keypad[digits[i]]:
        path.append(ch)               # choose
        backtrack(i + 1)              # explore
        path.pop()                    # unchoose
```

No pruning, because no prefix can ever become invalid. Every leaf is an answer.

## 🔍 Dry run: `"23"`

| depth i | digit | path before | choice | path after | action |
|---|---|---|---|---|---|
| 0 | 2 | `""` | `a` | `a` | recurse |
| 1 | 3 | `a` | `d` | `ad` | i = 2, **record** `ad`, pop |
| 1 | 3 | `a` | `e` | `ae` | **record** `ae`, pop |
| 1 | 3 | `a` | `f` | `af` | **record** `af`, pop |
| 0 | 2 | `a` → `""` | `b` | `b` | pop `a` first, then recurse |
| 1 | 3 | `b` | `d`, `e`, `f` | … | record `bd`, `be`, `bf` |
| 0 | 2 | `""` | `c` | `c` | record `cd`, `ce`, `cf` |

```
                   ""
          /        |        \
        a          b          c        <- depth 0: letters of "2"
      / | \      / | \      / | \
    ad ae af   bd be bf   cd ce cf     <- depth 1: letters of "3", all leaves
```

Nine leaves, nine answers.

## ✅ Optimal solution
```python
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        """Every letter string the digits can spell on a phone keypad.

        Time:  O(4^n · n), at most 4 letters per digit, O(n) to join each leaf.
        Space: O(n) for the recursion and path, excluding the output.
        """
        if not digits:
            return []                              # not [""]

        keypad = {'2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
                  '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'}
        result, path = [], []

        def backtrack(i: int) -> None:
            if i == len(digits):                   # one letter per digit
                result.append(''.join(path))
                return
            for ch in keypad[digits[i]]:
                path.append(ch)                    # choose
                backtrack(i + 1)                   # explore
                path.pop()                         # unchoose

        backtrack(0)
        return result
```
**Time:** O(n · 4ⁿ) · **Space:** O(n) excluding the output

## ⚠️ Gotchas
- **Empty input returns `[]`, not `[""]`.** Without the guard, `backtrack(0)` sees
  `i == len("") == 0` immediately and records one empty string. LeetCode expects `[]`.
  This is the most common wrong submission.
- **7 and 9 have four letters.** Hard-coding "3 letters per button" or writing the Big-O
  as 3ⁿ misses them. The worst case is 4ⁿ.
- **The path is a list, joined at the leaf.** `path += ch` on a string also works (strings
  are immutable, so there's nothing to undo), but then say *why* there's no pop.
- **Index by `digits[i]`, a character.** The keypad keys are strings `'2'`, not ints.
- **Base case on `i == len(digits)`, not `len(path) == len(digits)`.** Both work here;
  the index form is the one that generalises.

## 🎤 Interview talking points
- *"The number of digits varies, so I can't write nested loops; recursion gives me one
  loop per digit."*
- *"No pruning, because every prefix is valid, so the leaves are exactly the answers:
  up to 4ⁿ of them, times n to build each."*
- *"Empty input returns an empty list, I guard that first."* ← say this unprompted.
- *"In production I'd use `itertools.product`; I'm writing it by hand to show the
  backtracking."*
- *"Same template as Generate Parentheses; the choices come from a table instead of a
  budget."*

## 🔗 Transfer
EP116 had choices limited by a budget; here they come from a lookup and nothing is
pruned. EP118 changes what `available()` means again: every element that hasn't been
used yet, which adds a second piece of state to undo.

## 📹 Metadata
- **Title:** `Letter Combinations, a variable number of nested loops | Backtracking #2`
- **Thumbnail:** `[] NOT [""]` (red block)
- **Short:** the keypad dials animation for "23", then the empty-input bug. 45s.
