# EP030 · P03E10 · Permutation in a String   [Hard]

**Pattern:** Sliding Window · **Link:** https://leetcode.com/problems/permutation-in-string/

---

## 🎬 Hook
> "A permutation is just a bag of letters with the order thrown away. So the question
> 'does a permutation of this appear in that?' is really 'does any window have exactly
> this letter count?' — and once you see it that way, the window size is fixed and the
> problem collapses."

## 📋 Problem, in your words
```
Given strings s1 and s2, return true if s2 contains a PERMUTATION of s1
as a contiguous substring.

In other words: is there a window in s2, of length len(s1),
whose letters are exactly the letters of s1 in some order?
```

## 🔢 The example
```
Input:  s1 = "ab",  s2 = "eidbaooo"
Output: true        ("ba" at index 3 is a permutation of "ab")

Input:  s1 = "ab",  s2 = "eidboaoo"
Output: false       (contains 'b' and 'a' but never adjacent:
                     "bo", "oa" -- no window of length 2 has both)

Input:  s1 = "adc", s2 = "dcda"
Output: true        ("dca" at index 1)
```

## 🧸 ELI5
> You have a little bag of Scrabble tiles — say one `a` and one `b`. You're sliding a
> two-tile viewing frame along a long row of tiles, and you want to know if the frame
> ever holds **exactly** your bag: same letters, same counts, order irrelevant.
>
> The frame is a fixed size, because a permutation of a 2-letter word is always 2
> letters long. So this is the very first problem again — EP21's fixed window — except
> what you carry along isn't a running *sum*, it's a running **tally of letters**.
>
> One tile enters on the right, one leaves on the left, the tally updates, and you ask:
> does the tally match my bag?

## 🐌 Brute force (say it, don't type it)
Every window of length `len(s1)`, sort it, compare to sorted `s1`.

```python
target = sorted(s1)
for i in range(len(s2) - len(s1) + 1):
    if sorted(s2[i:i+len(s1)]) == target:
        return True
```

**O(n · k log k)** where k = `len(s1)`. Correct and very quick to write — say it first.
The waste is familiar: neighbouring windows differ by two characters, and this re-sorts
all k of them.

## 💡 The pattern reveal
**Signal:** "contains a permutation / anagram of" · contiguous.
**Therefore:** Sliding Window, Shape A — fixed size `len(s1)`, carrying a frequency map.

**Key insight #1:** a permutation of `s1` has exactly `len(s1)` characters, so **the
window size is fixed and known in advance**. There is no growing or shrinking, no
`while` loop, no decision to make. That's what makes this easier than EP29 despite
looking similar.

**Key insight #2:** "is a permutation" ⟺ "character counts are equal." Order never
enters the algorithm, which is why a `Counter` is the right object.

**Key insight #3 — the cheap comparison.** Comparing two `Counter`s is O(k) per step.
You can drop that to O(1) with a `matches` integer that tracks *how many distinct
characters currently have exactly the right count* — the same idea as EP29's `missing`,
one abstraction level up. Show the O(k) version first; it's usually fast enough, and
the constant is tiny for a 26-letter alphabet.

## 🔍 Dry run — `s1 = "ab"`, `s2 = "eidbaooo"`
`need = {a:1, b:1}`, window size 2.

| window | chars | counts | equal to need? |
|---|---|---|---|
| `ei` | e,i | `{e:1,i:1}` | no |
| `id` | i,d | `{i:1,d:1}` | no |
| `db` | d,b | `{d:1,b:1}` | no |
| `ba` | b,a | `{b:1,a:1}` | **yes** → return `True` |

## 🔍 Dry run — `s1 = "ab"`, `s2 = "eidboaoo"` (the false case)
| window | counts | match? |
|---|---|---|
| `ei` | `{e:1,i:1}` | no |
| `id` | `{i:1,d:1}` | no |
| `db` | `{d:1,b:1}` | no |
| `bo` | `{b:1,o:1}` | no ← the `b` is here |
| `oa` | `{o:1,a:1}` | no ← the `a` is here, one step too late |
| `ao` | `{a:1,o:1}` | no |
| `oo` | `{o:2}` | no |

Return `False`. Both letters exist in `s2`, but never inside one window — that's the
difference between "contains the letters" and "contains a permutation," and it's the
sentence to say on camera.

## ✅ Optimal solution
```python
from collections import Counter

class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        """Does any window of s2 have exactly s1's character counts?

        Time:  O(n) — one pass; each Counter comparison is O(26), a constant.
        Space: O(26) = O(1).
        """
        k, n = len(s1), len(s2)
        if k > n:
            return False

        need = Counter(s1)
        window = Counter(s2[:k])               # seed the first window
        if window == need:
            return True

        for hi in range(k, n):
            window[s2[hi]] += 1                # the character entering
            left = s2[hi - k]                  # the character leaving
            window[left] -= 1
            if window[left] == 0:
                del window[left]               # keep the maps comparable
            if window == need:
                return True

        return False
```
**Time:** O(n) · **Space:** O(1)

### Why the `del` is required here
`Counter({'a': 1, 'b': 0}) == Counter({'a': 1})` is **False** in Python — a zero-count
key still makes the dictionaries differ. Without the `del`, the comparison fails
forever after the first character leaves and you return `False` on everything. **This
is the bug of the episode.** Same `del` as EP23, different reason: there it kept
`len()` honest, here it keeps `==` honest.

### The O(1)-comparison version, if asked
```python
need = [0]*26; win = [0]*26
for c in s1: need[ord(c)-97] += 1
for c in s2[:k]: win[ord(c)-97] += 1
matches = sum(need[i] == win[i] for i in range(26))
# then maintain `matches` as counts change; matches == 26 means a hit
```
Strictly O(1) per step instead of O(26). Worth naming; rarely worth writing unless the
interviewer pushes.

## ⚠️ Gotchas
- **`del` zero-count keys** (above), or use fixed-size arrays where zeros compare fine.
  Arrays sidestep the problem entirely — mention that as the reason to prefer them.
- **Guard `len(s1) > len(s2)`** before slicing. Otherwise the seed window is short and
  can never match, which happens to return the right answer for the wrong reason —
  don't rely on accidents.
- **Seed the first window before the loop; start the loop at `k`.** Same structure as
  EP21, same negative-index trap if you start at 0.
- **`s2[hi - k]` is the departing character.** Say it as a sentence as you write it.
- **Permutation means *exactly* these counts** — not "at least." A window of `"aab"`
  does not contain a permutation of `"ab"`; it's the wrong length anyway, which is the
  fixed window protecting you.
- Constraints say lowercase English letters, so O(26) space. Don't assume that if the
  problem doesn't say it.

## 🎤 Interview talking points
- *"A permutation has a fixed length, so the window size is fixed — that's what makes
  this a Shape A problem rather than the variable-window ones."*
- *"Permutation equality is frequency equality; order never enters the algorithm."*
- *"Comparing counters is O(26), a constant, so the whole thing is O(n). If pushed I'd
  maintain a `matches` counter for a true O(1) per step."*
- *"I delete zero-count keys because `Counter` treats a zero entry as different from an
  absent one — or I'd use two 26-element arrays and avoid the issue."*

## 🔗 Transfer
EP31 (String Anagrams) is **this exact code with `return True` replaced by
`result.append(...)`** — it asks for every match instead of the first. EP32 generalises
the window's unit from a character to a whole word. Three episodes, one fixed window.

## 📹 Metadata
- **Title:** `Permutation in String — a fixed window with a letter tally | Sliding Window #10`
- **Thumbnail:** `ORDER DOESN'T MATTER` (amber block)
- **Short:** The `Counter({'a':1,'b':0}) != Counter({'a':1})` gotcha, 40s.
