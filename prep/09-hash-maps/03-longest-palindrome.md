# EP069 · P09E03 · Longest Palindrome   [Easy]

**Pattern:** Hash Maps · **Link:** https://leetcode.com/problems/longest-palindrome/

---

## 🎬 Hook
> "You're not finding a palindrome, you're **building** one. A palindrome is pairs on
> the outside and at most one lonely letter in the middle. Count the pairs, add one if
> anything's left over, done. The bug everyone ships adds one for **every** leftover."

## 📋 Problem, in your words
```
Given a string s of upper- and lowercase letters, return the LENGTH of the
longest palindrome that can be BUILT from those letters (any order, each
letter used at most once).

Letters are case-sensitive: 'A' and 'a' are different.
```

## 🔢 The example
```
Input:  "abccccdd"   -> 7     e.g. "dccaccd"
Input:  "a"          -> 1
Input:  "Aa"         -> 1     case-sensitive, so no pair
Input:  "aaabbb"     -> 5     e.g. "abbba" or "ab a ba"; NOT 6
```
`"aaabbb"` is the one to put on screen. Two odd counts, and only **one** of them gets
to keep its extra letter.

## 🧸 ELI5
> You're seating guests at a long table for a photo, and the photo has to look the same
> in a mirror. Every guest on the left needs an identical twin in the same seat on the
> right.
>
> So you seat people **in pairs**. Three sisters named Ann? Two of them pair up, one is
> left over. Four Carls? Two pairs.
>
> And the head of the table, the one seat in the exact middle, is the only seat that
> reflects onto itself. **One** leftover guest can sit there. Just one.
>
> ```
> a:3  b:3
> pairs:     a a | b b          (4 letters)
> leftovers: a, b               (two of them)
> middle:    pick ONE           (+1)
> total:     5    e.g.  a b [b] b a  ... "abbba"
> ```

## 🐌 Brute force (say it, don't type it)
Try every permutation of every subset of letters and check which are palindromes.
Exponential. There's no sensible brute force to type, and saying so is the point:
the question is about **counts**, and once you see that, there's nothing to search.

## 💡 The pattern reveal
**Signal:** "palindrome you can **build**" · "any order" · letters, not positions.
**Therefore:** Shape A from the card: count, then ask the piles "how many pair up?"

**Key insight:** a palindrome's letters, read as counts, are **all even except at most
one**. So from each pile take the largest even number of letters, and if any pile had
a leftover, add 1 for the centre.

```python
counts = Counter(s)
length = sum(v // 2 * 2 for v in counts.values())   # every pair, from every pile
if any(v % 2 for v in counts.values()):             # at least one leftover exists
    length += 1                                     # exactly ONE can sit in the middle
return length
```

**Why it's correct:** mirrored positions must hold equal letters, so every letter
except the one in the centre is used an even number of times. That makes
`sum(v // 2 * 2)` an upper bound on the non-centre letters, and it's achievable by
placing half of each pair on each side. The centre holds at most one letter, and we
can fill it iff some pile had a leftover.

## 🔍 Dry run: `"abccccdd"`

| letter | count | `v // 2 * 2` (paired letters) | odd? |
|---|---|---|---|
| `a` | 1 | 0 | yes |
| `b` | 1 | 0 | yes |
| `c` | 4 | 4 | no |
| `d` | 2 | 2 | no |

Paired letters: 0 + 0 + 4 + 2 = **6**. Any odd? yes → **+1**. Answer **7** ✓
(`"dccaccd"`: `d c c` / `a` / `c c d`).

## 🔍 Dry run: `"aaabbb"` (the trap)

| letter | count | paired letters | odd? |
|---|---|---|---|
| `a` | 3 | 2 | yes |
| `b` | 3 | 2 | yes |

Paired: **4**. Any odd? yes → **+1** → **5** ✓.
The buggy version adds 1 **per** odd count → 6. There is no 6-letter palindrome from
three a's and three b's, because two letters can't both be in the middle.

## ✅ Optimal solution
```python
from collections import Counter

class Solution:
    def longestPalindrome(self, s: str) -> int:
        """Length of the longest palindrome that can be built from the letters of s.

        Time:  O(n), one pass to count, one over at most 52 keys.
        Space: O(1), at most 52 keys (upper and lower case).
        """
        counts = Counter(s)

        length = 0
        has_leftover = False
        for v in counts.values():
            length += v // 2 * 2          # the largest even amount of this letter
            if v % 2:
                has_leftover = True       # this pile has one letter spare

        # exactly one spare letter can go in the centre, however many piles had one
        return length + 1 if has_leftover else length
```
**Time:** O(n) · **Space:** O(1)

## ⚠️ Gotchas
- **`+1` once, not once per odd pile.** `"aaabbb"` → 5, not 6. The flag, or `any(...)`,
  is the whole problem.
- **`v // 2 * 2`, not `v // 2`.** The first is letters, the second is pairs, and the
  answer is a length in letters. `"cccc"` → 4 letters, 2 pairs.
- **Don't drop odd piles entirely.** A count of 3 contributes 2 letters, not 0. `v - 1`
  for odd `v` is the same as `v // 2 * 2`. Write whichever you can explain.
- **Case-sensitive.** `"Aa"` → 1. Lowercasing the input is a wrong answer here.
- **The one-line alternative** is `len(s) - odd + (odd > 0)`, where `odd` is the number
  of piles with an odd count. Every odd pile gives up one letter, then one is
  given back for the centre. Show it after the loop version, it's a nice second
  derivation of the same fact.

## 🎤 Interview talking points
- *"A palindrome is all even counts except at most one. So it's pairs from every pile,
  plus one centre letter if anything was left over."*
- *"The centre is a single position, so I add 1 at most once, however many odd counts
  there are."* ← say this unprompted, it's the bug they're checking for.
- *"O(n) time, O(1) space, 52 possible keys."*
- *"I'm returning a length, so I never actually build the string. If they wanted the
  string, I'd put half of each pair on the left, reverse it for the right, and a
  leftover letter in the middle."*

## 🔗 Transfer
EP68 asked the piles "how many copies fit?". This asks "how many pair up?". Both throw
the order away. EP70 compares two sets of piles. The "all even except at most one"
fact comes back as a parity check in Palindrome Partitioning (EP120) and in
bitmask problems like LeetCode 1915, where an odd count is a bit that's switched on.

## 📹 Metadata
- **Title:** `Longest Palindrome, pairs plus ONE middle letter | Hash Maps #3`
- **Thumbnail:** `+1 ONCE` (red block)
- **Short:** the mirror-photo ELI5 and `"aaabbb"` giving 6 in the buggy version. 45s.
