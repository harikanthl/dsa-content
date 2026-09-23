# EP070 · P09E04 · Ransom Note   [Easy]

**Pattern:** Hash Maps · **Link:** https://leetcode.com/problems/ransom-note/

---

## 🎬 Hook
> "Can you cut this note out of that magazine? Count both, then check the magazine has
> at least as much of every letter the note needs. In Python it's one subtraction of
> two Counters, and knowing *why* that subtraction works is the actual lesson."

## 📋 Problem, in your words
```
Given two strings ransomNote and magazine, return True if ransomNote can be
built from the letters of magazine, using each magazine letter at most once.
```

## 🔢 The example
```
Input:  note="a",    magazine="b"      -> False
Input:  note="aa",   magazine="ab"     -> False    enough kinds, not enough copies
Input:  note="aa",   magazine="aab"    -> True
```
`"aa"` from `"ab"` is the one to put on screen. The magazine *has* an `a`, so a
"does it contain the letter?" check says yes. It's a count problem, not a membership
problem.

## 🧸 ELI5
> You're cutting letters out of a magazine to glue onto a note. Every letter you cut is
> gone.
>
> Make two piles: one for what the **note needs**, one for what the **magazine has**.
> Go through the note's pile, letter by letter, and check the magazine's pile is at
> least as tall.
>
> ```
> note "aa" needs:     a:2
> magazine "ab" has:   a:1  b:1
>
> a: need 2, have 1  -> short by 1  -> False
> ```
>
> Extra letters in the magazine don't matter. Missing letters in the magazine read as a
> pile of height zero.

## 🐌 Brute force (say it, don't type it)
For each letter of the note, find it in the magazine and delete it
(`magazine.replace(ch, '', 1)` or `list.remove`). If any letter isn't found, return
False. Each find-and-delete is O(m), so **O(n · m)**. It's correct, and it's the
"simulate the scissors" solution. Counting replaces the scissors with arithmetic.

## 💡 The pattern reveal
**Signal:** "can A be **constructed from** B" · "each letter used once".
**Therefore:** Shape A from the card, on two strings: multiset **containment**.

**Key insight:** the note is buildable iff for every letter,
`have[ch] >= need[ch]`. That's EP68's budget with the answer capped at "at least once".

```python
need = Counter(ransomNote)
have = Counter(magazine)
return all(have[ch] >= n for ch, n in need.items())
```

And the Python shortcut, which is the same check:

```python
return not (Counter(ransomNote) - Counter(magazine))
```

**Why the subtraction works:** `Counter` subtraction keeps only **positive** results.
So `need - have` holds exactly the letters the note needs more of than the magazine
has. Empty means nothing is short, which means the note is buildable.

## 🔍 Dry run: note=`"aa"`, magazine=`"aab"` (True)

| letter | need | have | have ≥ need? |
|---|---|---|---|
| `a` | 2 | 2 | ✓ |

`b` is in `have` but not in `need`, it's never checked. All pass → **True** ✓.

## 🔍 Dry run: note=`"aa"`, magazine=`"ab"` (False)

| letter | need | have | have ≥ need? | `need - have` |
|---|---|---|---|---|
| `a` | 2 | 1 | ✗ | `{a: 1}` |

`need - have = Counter({'a': 1})`, not empty → **False** ✓.

## ✅ Optimal solution
```python
from collections import Counter

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        """True if ransomNote can be spelled using magazine's letters, each once.

        Time:  O(n + m), one pass over each string.
        Space: O(1), at most 26 keys per counter.
        """
        if len(ransomNote) > len(magazine):          # can't cut more letters than exist
            return False

        have = Counter(magazine)
        for ch in ransomNote:                        # spend the magazine's letters
            if have[ch] == 0:                        # none left of this one (or never any)
                return False
            have[ch] -= 1

        return True
```
**Time:** O(n + m) · **Space:** O(1)

This version counts only the magazine and *spends* it while walking the note, so it
exits on the first letter that runs out. Show the `Counter` subtraction one-liner
next to it: same complexity, less code, no early exit.

## ⚠️ Gotchas
- **Membership isn't enough.** `"aa"` from `"ab"`: `a in magazine` is True, the answer
  is False. Say "count, not contain."
- **Missing key must be 0.** A letter the magazine never had is the most important
  case. `Counter` gives 0; a plain `dict` gives `KeyError`. Use `.get(ch, 0)` on a dict.
- **Check `== 0` before decrementing**, not after. Decrementing first and checking
  `< 0` also works, but then the counter holds a negative number, which surprises
  anyone who reads it later.
- **Counter subtraction drops negatives and zeros.** That's what makes
  `not (need - have)` correct. Plain `dict` arithmetic doesn't exist, and
  `Counter.subtract()` (the method) *keeps* negatives, so `not need.subtract(...)` is
  wrong in two ways at once.
- **The length check is a free early exit**, not a requirement. Mention it, keep it.

## 🎤 Interview talking points
- *"It's multiset containment: the magazine needs at least as many of every letter the
  note uses."*
- *"I count the magazine and spend it while reading the note, so I exit on the first
  letter that runs out."*
- *"In Python, `not (Counter(note) - Counter(magazine))` is the same check, because
  Counter subtraction drops everything that isn't positive."*
- *"O(n + m) time, O(1) space for a fixed alphabet."*

## 🔗 Transfer
This closes the pattern. **Record a short recap video after this one:** four problems,
one move (count once, then ask the piles), four different questions: which is first
(EP67), how many copies fit (EP68), how many pair up (EP69), is one pile covered by
another (EP70). Next is EP71, Binary Search, which is the opposite trade: instead of
spending memory to avoid order, it spends order to avoid looking at most of the data.
"Does multiset A fit inside B?" comes back inside Sliding Window's Permutation in a
String (EP30) and Minimum Window Substring (EP29), with a window moving across B.

## 📹 Metadata
- **Title:** `Ransom Note, count, don't contain | Hash Maps #4`
- **Thumbnail:** `COUNT ≠ CONTAIN` (red block)
- **Short:** the magazine-scissors ELI5 and `"aa"` from `"ab"`. 35s.
