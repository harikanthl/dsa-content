# EP031 · P03E11 · String Anagrams   [Hard]

**Pattern:** Sliding Window · **Link:** https://leetcode.com/problems/find-all-anagrams-in-a-string/

---

## 🎬 Hook
> "Yesterday's problem asked *does* a permutation appear. Today asks *where do they all
> appear*. The algorithm is identical — you change a `return True` into an `append` —
> and that tiny difference is worth an episode, because knowing when a problem is a
> re-skin saves you the ten minutes you'll need elsewhere."

## 📋 Problem, in your words
```
Given strings s and p, return the START INDICES of every substring of s
that is an anagram of p.

An anagram is a rearrangement: same letters, same counts, any order.
Windows may overlap.
```

## 🔢 The example
```
Input:  s = "cbaebabacd",  p = "abc"
Output: [0, 6]
Why:    index 0 -> "cba"  (anagram of "abc")
        index 6 -> "bac"  (anagram of "abc")

Input:  s = "abab",  p = "ab"
Output: [0, 1, 2]
Why:    "ab" at 0, "ba" at 1, "ab" at 2 -- they OVERLAP, and all three count.
```

That second example is the one to lead with. Overlapping matches are where a
"find, then skip forward" approach quietly loses answers.

## 🧸 ELI5
> Exactly yesterday's sliding frame of Scrabble tiles — but instead of shouting "found
> one!" and stopping, you **write down the position** and keep sliding.
>
> And you slide by **one** tile, not by the width of the frame. Anagrams can overlap:
> in `"abab"`, the match at index 0 and the match at index 1 share a letter. Jumping
> the frame past a match would skip the second one.

## 🐌 Brute force (say it, don't type it)
Every window of length `len(p)`, sort and compare. **O(n · k log k)**. Same waste as
EP30 — re-sorting k characters to learn what two comparisons would tell you.

## 💡 The pattern reveal
**Signal:** "find all anagrams / permutations" · contiguous · fixed length.
**Therefore:** Sliding Window, Shape A — the same fixed window as EP30, collecting
results instead of returning early.

**Key insight:** there is no new idea today. That *is* the lesson. When you meet this
in an interview, the strongest thing you can say is: *"this is Permutation in a String
with every match collected instead of the first."* Recognising a re-skin instantly is a
skill you are deliberately practising, and this pair of episodes exists to build it.

**The one genuinely new detail:** the window advances by **one**, so overlapping
anagrams are all found. Nothing in the code has to change for that — but you should
know *why* you're not tempted to skip ahead.

## 🔍 Dry run — `s = "cbaebabacd"`, `p = "abc"`
`need = {a:1, b:1, c:1}`, window size 3.

| start | window | counts | match? | result |
|---|---|---|---|---|
| 0 | `cba` | `{c:1,b:1,a:1}` | **yes** | `[0]` |
| 1 | `bae` | `{b:1,a:1,e:1}` | no | `[0]` |
| 2 | `aeb` | `{a:1,e:1,b:1}` | no | `[0]` |
| 3 | `eba` | `{e:1,b:1,a:1}` | no | `[0]` |
| 4 | `bab` | `{b:2,a:1}` | no | `[0]` |
| 5 | `aba` | `{a:2,b:1}` | no | `[0]` |
| 6 | `bac` | `{b:1,a:1,c:1}` | **yes** | `[0, 6]` |
| 7 | `acd` | `{a:1,c:1,d:1}` | no | `[0, 6]` |

Return **`[0, 6]`**.

Note rows 4 and 5: `{b:2,a:1}` and `{a:2,b:1}` have the right *total* length and the
right *letters*, and are still not anagrams — the counts differ. "Same set of letters"
is not the test; "same multiset" is.

## ✅ Optimal solution
```python
from collections import Counter

class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        """Start indices of every anagram of p inside s.

        Time:  O(n) — one pass; each comparison is O(26), a constant.
        Space: O(26) = O(1) beyond the output.
        """
        k, n = len(p), len(s)
        if k > n:
            return []

        need = Counter(p)
        window = Counter(s[:k])                # seed the first window
        result = [0] if window == need else []

        for hi in range(k, n):
            window[s[hi]] += 1                 # entering on the right
            left = s[hi - k]                   # leaving on the left
            window[left] -= 1
            if window[left] == 0:
                del window[left]               # zero-count keys break ==
            if window == need:
                result.append(hi - k + 1)      # the window's START index

        return result
```
**Time:** O(n) · **Space:** O(1) beyond the output

### The index to be careful about
You append `hi - k + 1`, not `hi`. At the moment of the check, `hi` is the **last**
index of the window; the problem wants the **first**. Derive it on camera rather than
recalling it: the window covers `hi-k+1 .. hi`, which is `k` indices — count them out.

## ⚠️ Gotchas
- **Append the start index, not `hi`.** The single most common bug, and it produces a
  list of plausible-looking wrong numbers.
- **Check the seed window before the loop.** An anagram at index 0 is otherwise missed
  entirely — `"abab"`/`"ab"` catches it, since the expected output starts at 0.
- **`del` zero-count keys**, or use 26-element arrays. Same reason as EP30:
  `Counter({'a':1,'b':0}) != Counter({'a':1})`.
- **Slide by one; never skip past a match.** `"abab"` with `p = "ab"` returns
  `[0, 1, 2]` — overlapping matches all count.
- **Guard `len(p) > len(s)`** and return `[]`.
- Same letters is not enough — the **counts** must match. Rows 4 and 5 of the trace are
  the counterexample to show.

## 🎤 Interview talking points
- *"This is Permutation in a String, collecting every match instead of returning on the
  first."* ← say it immediately; it demonstrates pattern recognition, which is the
  thing being tested.
- *"Fixed window because an anagram of p always has length len(p); the comparison is
  O(26), so the whole thing is O(n)."*
- *"The window advances by one, so overlapping anagrams are found — `'abab'` with
  `'ab'` gives three answers."*

## 🔗 Transfer
EP32 (Words Concatenation) takes this same fixed-window-with-a-frequency-map and
changes the **unit** from a character to a whole word — which turns one window into
`len(word)` independent windows. It's the hardest problem in the pattern and it's built
entirely from what you already have.

## 📹 Metadata
- **Title:** `Find All Anagrams — yesterday's code, one line changed | Sliding Window #11`
- **Thumbnail:** `THEY CAN OVERLAP` (amber block)
- **Short:** `"abab"` / `"ab"` → `[0,1,2]` — "three answers from four letters." 35s.
