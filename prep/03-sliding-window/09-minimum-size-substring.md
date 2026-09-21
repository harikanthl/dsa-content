# EP029 · P03E09 · Minimum Window Substring   [Hard]

**Pattern:** Sliding Window · **Link:** https://leetcode.com/problems/minimum-window-substring/

---

## 🎬 Hook
> "This is the hardest sliding-window problem there is, and the reason is one
> deceptively simple question: how do you check *'does my window contain everything I
> need'* without comparing two dictionaries every single step? The answer is a single
> integer, and it's the trick that makes this problem tractable."

## 📋 Problem, in your words
```
Given strings s and t, find the SHORTEST substring of s that contains
every character of t, INCLUDING duplicates.

If t = "AABC", the window must hold two As, one B and one C.
Extra characters in the window are fine.
Return "" if no such window exists.
```

## 🔢 The example
```
Input:  s = "ADOBECODEBANC",  t = "ABC"
Output: "BANC"

Why:    "ADOBEC" also contains A, B and C -- length 6.
        "CODEBA" does too -- length 6.
        "BANC" does it in 4. Nothing shorter works.

Input:  s = "a",  t = "a"      Output: "a"
Input:  s = "a",  t = "aa"     Output: ""      (only one 'a' available)
```

That last one matters: **duplicates count.** Most wrong solutions treat `t` as a set.

## 🧸 ELI5
> You have a shopping list — say two apples, a banana, a carrot — and you're walking
> down one long aisle, picking up whatever you pass.
>
> Keep walking right until your basket satisfies the whole list. Now try to make the
> trip shorter: drop things from the **back** of your walk for as long as the list is
> *still* satisfied. When dropping one more would break it, write down how far you
> walked. Then keep going right and repeat.
>
> The clever bit is how you check "is the list satisfied?". You don't re-read the whole
> list every step. You keep **one number: how many items are still missing.** Pick up
> something you needed, the number goes down. Drop something you needed, it goes back
> up. Zero means you're done shopping.

## 🐌 Brute force (say it, don't type it)
Every substring, check whether it covers `t`. **O(n²·m)**, or O(n²) with frequency
counting. Hopeless at the constraint sizes, and — more usefully — it wastes the same
overlap as every other problem in this pattern.

The *slightly* less naive version keeps a window and compares
`Counter(window) ⊇ Counter(t)` at every step. That's **O(n·k)** for an alphabet of size
k, and it's what most people write. Today's job is to get rid of that `k`.

## 💡 The pattern reveal
**Signal:** contiguous · **shortest** · "contains all of ..."
**Therefore:** Sliding Window, Shape C.

**Key insight — the `missing` counter.** Keep `need`, a dictionary of *how many of each
character the window still owes*, and one integer `missing` = how many required
characters remain unmatched.

```python
need = Counter(t)          # need['A'] = 2 means "the window owes two As"
missing = len(t)           # total characters still owed -- NOT len(set(t))
```

Then, for each character entering the window:

```python
if need[char] > 0:         # this character was actually WANTED
    missing -= 1
need[char] -= 1            # goes NEGATIVE for surplus characters
```

Two things are doing the work here:

1. **`need[char] > 0` before decrementing.** A third `A` when only two were needed sees
   `need['A']` already at 0, so `missing` doesn't move. Surplus never counts.
2. **Letting `need` go negative.** `need['A'] = -1` means "one spare A in the window."
   That's how you know, on the way out, whether removing a character actually breaks
   the window — and it's why no dictionary comparison is ever needed.

**`missing == 0` is the validity test. One integer comparison, O(1).** That's the
episode.

## 🔍 Dry run — `s = "ADOBECODEBANC"`, `t = "ABC"`
`need = {A:1, B:1, C:1}`, `missing = 3`. Only the steps where the window becomes valid
are shown — the rest just grow it.

| hi | char | window | `missing` | after shrinking | length | best |
|---|---|---|---|---|---|---|
| 5 | C | `ADOBEC` | 0 | `ADOBEC` | 6 | `ADOBEC` |
| 9 | B | `ADOBECODEB` | 0 | shrink to `CODEB`… still needs A | 10 | `ADOBEC` |
| 10 | A | `…CODEBA` | 0 | `CODEBA` | 6 | `ADOBEC` |
| 12 | C | `…BANC` | 0 | `BANC` | **4** | **`BANC`** |

Return **`"BANC"`**.

Watch what happens between `hi=5` and `hi=10`: the window stays valid the whole time,
so the left edge keeps creeping right, discarding the surplus `A` and `D` and `O` as it
goes. The shrink loop is not an occasional event — it runs constantly, which is exactly
why `lo` only moving forward is what keeps this linear.

## ✅ Optimal solution
```python
from collections import Counter

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        """Shortest substring of s containing all characters of t (with duplicates).

        Time:  O(n + m) — every index enters and leaves the window at most once.
        Space: O(k) — one counter over the characters of t.
        """
        if not s or not t:
            return ""

        need = Counter(t)          # how many of each char the window still owes
        missing = len(t)           # total owed; NOT len(set(t)) -- duplicates count
        lo = 0
        best_len, best_lo = float('inf'), 0

        for hi, char in enumerate(s):
            if need[char] > 0:     # only a WANTED char reduces the debt
                missing -= 1
            need[char] -= 1        # may go negative == surplus in the window

            while missing == 0:                    # shrink while STILL valid
                if hi - lo + 1 < best_len:
                    best_len, best_lo = hi - lo + 1, lo   # record BEFORE breaking it

                need[s[lo]] += 1                   # putting it back
                if need[s[lo]] > 0:                # it was needed -> window now broken
                    missing += 1
                lo += 1

        return "" if best_len == float('inf') else s[best_lo:best_lo + best_len]
```
**Time:** O(n + m) · **Space:** O(k)

### The asymmetry to say out loud
Going **in**: check `need[char] > 0` *before* decrementing.
Coming **out**: increment *first*, then check `need[s[lo]] > 0`.

That's not sloppiness — it's the same test on opposite sides of the change. Entering,
"was it needed *before* I took it?" Leaving, "is it needed *now* that I've given it
back?" Write both lines next to each other on screen; the symmetry is what makes them
memorable instead of magic.

## ⚠️ Gotchas
- **`missing = len(t)`, not `len(set(t))`.** With `t = "AABC"` you owe *four*
  characters. Using the set is the single most common wrong answer and it passes the
  basic examples, which is what makes it dangerous — `s="a", t="aa"` catches it.
- **`need` must be allowed to go negative.** Clamping at zero destroys the surplus
  information and the shrink step can no longer tell whether removing a character
  breaks the window.
- **Record the window before removing `s[lo]`.** Shape C. Measure while it's still
  valid.
- **Return the substring, not its length.** Track `best_lo` alongside `best_len` —
  reconstructing it afterwards from a length alone is impossible.
- **`Counter` returns 0 for missing keys, it doesn't raise.** That's why
  `need[char] -= 1` works for characters that aren't in `t` at all — they go straight
  to −1, marked as surplus. Using a plain `dict` here needs `.get()` everywhere.
- Guard the empty inputs. `t = ""` should arguably return `""`, and `len(t) > len(s)`
  can never match.

## 🎤 Interview talking points
- *"The naive check is comparing two frequency maps every step — O(k) per character. I
  replace it with a single integer, `missing`, updated in O(1), so the whole thing is
  O(n)."*
- *"Letting the counts go negative is deliberate: a negative count is surplus, and
  that's exactly the information the shrink step needs."*
- *"It's Shape C — shrink while the window is still valid and record before breaking
  it. The mirror of the longest-window problems earlier in the pattern."*
- *"Every index enters and leaves at most once, so O(n) amortised despite the nested
  loop."*

## 🔗 Transfer
The `missing`-counter trick is the direct ancestor of EP30 and EP31, where the window
is a fixed size and the same bookkeeping answers "is this an anagram?". If you can
write today's cold, those two are twenty minutes each. This problem also shows up in
interviews more than any other in the pattern — it's worth being the one you can do
from memory.

## 📹 Metadata
- **Title:** `Minimum Window Substring — one integer instead of two dictionaries | Sliding Window #9`
- **Thumbnail:** `COUNT WHAT'S MISSING` (amber block)
- **Short:** The in/out asymmetry — `if need>0 then decrement` vs `increment then if need>0`. 55s.
