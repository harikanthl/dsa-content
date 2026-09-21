# EP025 · P03E05 · No-repeat Substring   [Hard]

**Pattern:** Sliding Window · **Link:** https://leetcode.com/problems/longest-substring-without-repeating-characters/

---

## 🎬 Hook
> "This is the most-asked string question in interviewing, and almost everyone writes
> the version that walks the left pointer forward one step at a time. There's a
> version that *teleports* it — and the two-character guard that makes teleporting
> safe is the whole reason this problem is worth an episode."

## 📋 Problem, in your words
```
Given a string, find the length of the longest substring
with NO repeated characters.

Substring = contiguous. "abcabcbb" -> "abc", length 3.
```

## 🔢 The example
```
Input:  "abcabcbb"     Output: 3     ("abc")
Input:  "bbbbb"        Output: 1     ("b")
Input:  "pwwkew"       Output: 3     ("wke" -- note "pwke" is a SUBSEQUENCE, not a
                                      substring, so it does not count)
Input:  "abba"         Output: 2     (the case that breaks naive teleporting)
```

That last example is the one to put on screen early. It's small, and it's where the
clever version goes wrong.

## 🧸 ELI5
> You're reading a word letter by letter, keeping a window of what you've read with no
> repeats.
>
> You hit a letter you've already got. The window is now illegal, and the only fix is
> to start it *after* the earlier copy of that letter — everything before that is dead
> weight.
>
> The slow way is to shuffle the left edge forward one letter at a time until the
> duplicate falls out. The fast way is to **remember where you last saw each letter**
> and jump the left edge straight past it in one move.

## 🐌 Brute force (say it, don't type it)
Every start, extend right with a set, stop on the first repeat. **O(n²)**. Building a
fresh set for every start is the waste; the sets are nearly identical.

## 💡 The pattern reveal
**Signal:** contiguous · longest · "no repeated characters" (= at most 1 of each).
**Therefore:** Sliding Window, Shape B.

**Key insight:** you don't need to walk `lo` forward. Keep `last[char] = the most
recent index where you saw it`. When `char` reappears, the earliest legal window start
is `last[char] + 1`, so **jump** there.

**And the guard that makes it correct:** only jump if the previous sighting is *inside
the current window*.

```python
if char in last and last[char] >= lo:
    lo = last[char] + 1
```

Without `last[char] >= lo` you can move `lo` **backwards** — re-admitting characters
you already evicted — and report a window with duplicates in it. `"abba"` is the
minimal case, which is why it's in the examples.

## 🔍 Dry run — `"abcabcbb"`
| hi | char | seen before at | jump? | lo | window | best |
|---|---|---|---|---|---|---|
| 0 | a | — | no | 0 | `a` | 1 |
| 1 | b | — | no | 0 | `ab` | 2 |
| 2 | c | — | no | 0 | `abc` | **3** |
| 3 | a | 0 (≥ lo) | lo = 1 | 1 | `bca` | 3 |
| 4 | b | 1 (≥ lo) | lo = 2 | 2 | `cab` | 3 |
| 5 | c | 2 (≥ lo) | lo = 3 | 3 | `abc` | 3 |
| 6 | b | 4 (≥ lo) | lo = 5 | 5 | `cb` | 3 |
| 7 | b | 6 (≥ lo) | lo = 7 | 7 | `b` | 3 |

## 🔍 Dry run — `"abba"`, the case that breaks the naive version
| hi | char | seen before at | `>= lo`? | lo | window | best |
|---|---|---|---|---|---|---|
| 0 | a | — | — | 0 | `a` | 1 |
| 1 | b | — | — | 0 | `ab` | **2** |
| 2 | b | 1 | yes | **2** | `b` | 2 |
| 3 | a | **0** | **0 ≥ 2 is FALSE → do not jump** | 2 | `ba` | 2 |

At `hi=3` the letter `a` was last seen at index 0 — but `lo` is already at 2, so that
`a` is long gone from the window. Jumping to `last['a'] + 1 = 1` would drag `lo`
*backwards* from 2 to 1, re-admitting the `b` at index 1, and you'd report a window of
length 3 containing two `b`s. **Return 3 instead of 2 — silently wrong.** Let this
happen on camera, then add the guard.

## ✅ Optimal solution
```python
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """Longest substring with no repeated characters.

        Time:  O(n) — a single pass; lo jumps and never walks backwards.
        Space: O(min(n, alphabet)) — the last-seen map.
        """
        last_seen: Dict[str, int] = {}
        lo = 0
        best = 0

        for hi, char in enumerate(s):
            # Jump only if the earlier copy is INSIDE the window.
            if char in last_seen and last_seen[char] >= lo:
                lo = last_seen[char] + 1

            last_seen[char] = hi
            best = max(best, hi - lo + 1)

        return best
```
**Time:** O(n) · **Space:** O(min(n, |alphabet|))

### The simpler version, also correct
```python
window = set()
lo = best = 0
for hi, char in enumerate(s):
    while char in window:            # walk lo forward until the duplicate leaves
        window.remove(s[lo]); lo += 1
    window.add(char)
    best = max(best, hi - lo + 1)
```
Also **O(n) amortised**, has no `>= lo` trap, and is easier to get right under
pressure. The jumping version does one pass instead of two-ish and is what people mean
by "the optimal solution," but the honest comparison is: *same complexity, fewer ways
to be wrong.* Show both. Say which you'd write in a real interview and why — that
judgement is worth more than the micro-optimisation.

## ⚠️ Gotchas
- **`last_seen[char] >= lo` is not optional.** See the `"abba"` trace. This is *the*
  bug on this problem and it produces a plausible-looking wrong answer rather than a
  crash.
- **`lo` must never decrease.** An equivalent, arguably clearer formulation is
  `lo = max(lo, last_seen[char] + 1)` — which makes the invariant impossible to
  violate. Prefer it if you find the guard fiddly.
- **Update `last_seen[char]` after the jump**, not before, or you'll compare a
  character against its own current index.
- **Substring, not subsequence.** `"pwwkew"` → `"wke"` (3), not `"pwke"` (4). Read the
  word; it decides whether this pattern applies at all.
- Empty string returns 0 with no special case. Single character returns 1.
- The alphabet may not be 26 letters — LeetCode's input includes digits, symbols and
  spaces. Don't use a fixed-size array unless the constraints promise ASCII.

## 🎤 Interview talking points
- *"I keep the last index of each character so the left edge jumps past a duplicate
  instead of walking to it."*
- *"The guard `last[c] >= lo` stops the left edge moving backwards — without it,
  `'abba'` returns 3."* ← naming a concrete failing input is far stronger than saying
  "there's an edge case."
- *"Both versions are O(n) amortised. The set version is easier to write correctly; I'd
  pick it under time pressure and mention the jumping one as the refinement."*

## 🔗 Transfer
EP26 and EP27 keep this skeleton and change only the validity test — and both need a
genuinely surprising argument for why the window is allowed to be "wrong" sometimes.
The last-seen-index idea itself reappears in Pattern 09 (Hash Maps) whenever you need
"where did I last see this?"

## 📹 Metadata
- **Title:** `Longest Substring Without Repeating Characters — the >= lo trap | Sliding Window #5`
- **Thumbnail:** `DON'T GO BACKWARDS` (amber block)
- **Short:** The `"abba"` failure — wrong answer 3, then the one-condition fix. 50s.
