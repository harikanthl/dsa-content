# EP032 · P03E12 · Words Concatenation   [Hard]

**Pattern:** Sliding Window · **Link:** https://leetcode.com/problems/substring-with-concatenation-of-all-words/

---

## 🎬 Hook
> "Every window problem so far moved one character at a time. This one can't, its
> pieces are whole words of equal length, so a window that starts one character late is
> nonsense. The fix is to stop thinking about one window and start thinking about
> **several independent lanes**, one per starting offset."

## 📋 Problem, in your words
```
Given a string s and a list of words, all of the SAME length,
find every starting index in s where a substring is exactly a
concatenation of all the words, each used exactly once, in any order.

If words has duplicates, that word must appear that many times.
```

## 🔢 The example
```
Input:  s = "barfoothefoobarman",  words = ["foo","bar"]
Output: [0, 9]

  index:  0     3     6     9    12    15
          bar   foo   the   foo   bar   man
          ^--------^              
          index 0: "barfoo" = bar + foo    -- both words, once each
                                ^--------^
          index 9: "foobar" = foo + bar

Input:  s = "wordgoodgoodgoodbestword",  words = ["word","good","best","word"]
Output: []       ("word" is needed TWICE and never appears twice in range)

Input:  s = "barfoofoobarthefoobarman",  words = ["bar","foo","the"]
Output: [6, 9, 12]
```

## 🧸 ELI5
> The words are all the same length, say 3 letters. So a valid answer is a run of
> whole 3-letter blocks, lined up on a grid.
>
> Here's the catch: a block starting at index 0 and a block starting at index 1 are on
> **different grids**. They never share a block, so they can never interfere. With
> 3-letter words there are exactly **three grids**: offsets 0, 1 and 2, and every
> answer lives on exactly one of them.
>
> So run the ordinary sliding window **three separate times**, once per grid, and on
> each grid the "characters" are whole words. After offset 3 you'd be back on grid 0,
> which is why there are only `word_length` lanes, not `n`.

## 🐌 Brute force (say it, don't type it)
At every index, chop the next `n × word_length` characters into words and check the
multiset.

```python
for i in range(len(s) - total + 1):
    seen = Counter()
    for j in range(n):
        w = s[i + j*wl : i + (j+1)*wl]
        if w not in need: break
        seen[w] += 1
        if seen[w] > need[w]: break
    else:
        result.append(i)
```

**O(n_s × n_w × wl).** This is genuinely acceptable at LeetCode's constraints and is
the right first answer, write it, get it passing, *then* improve it. The waste is the
usual one: consecutive starts on the same grid share all but one word.

## 💡 The pattern reveal
**Signal:** fixed total length · "all the words, each exactly once" · equal word
lengths.
**Therefore:** Sliding Window, Shape A, with the **unit changed from a character to a
word**, run once per starting offset.

**Key insight #1:** because all words have the same length `wl`, any valid substring is
aligned to one of `wl` grids. Offsets `0 .. wl-1` partition the problem into `wl`
independent scans, and each scan visits `n/wl` positions, so the total work is still
one pass over `s`.

**Key insight #2, two different ways a window can break**, and they need different
responses:

| What happened | Response |
|---|---|
| The next block isn't a word at all | **Reset** the lane: clear the counter, jump `lo` past it |
| The next block is a word, but one too many of it | **Shrink**: drop words from the left until that word's count is legal again |

Getting these two confused is the bug of the episode. An unknown word can never be part
of any future window on this lane, so there's nothing to salvage, reset. A surplus
word only means you started too early, shrink.

## 🔍 Dry run: `s = "barfoothefoobarman"`, `words = ["foo","bar"]`
`wl = 3`, `n = 2`, `need = {foo:1, bar:1}`. Lane 0 (offsets 0, 3, 6, 9, 12, 15):

| hi | block | in `need`? | window | count | action |
|---|---|---|---|---|---|
| 0 | `bar` | yes | `{bar:1}` | 1 | |
| 3 | `foo` | yes | `{bar:1,foo:1}` | **2 = n** | **record index 0**, drop `bar`, lo=3 |
| 6 | `the` | **no** | - | 0 | **reset** the lane, lo = 9 |
| 9 | `foo` | yes | `{foo:1}` | 1 | |
| 12 | `bar` | yes | `{foo:1,bar:1}` | **2 = n** | **record index 9**, drop `foo`, lo=12 |
| 15 | `man` | **no** | - | 0 | reset, lo = 18 |

Lanes 1 and 2 (offsets 1,4,7,… and 2,5,8,…) produce only non-words, `arf`, `oot`,
`rfo`, `oth`, so they reset immediately and contribute nothing.

Result **`[0, 9]`**. ✓

## ✅ Optimal solution
```python
from collections import Counter

class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        """Start indices where s contains a concatenation of every word, once each.

        Time:  O(wl * n_s / wl) = O(n_s) block visits, each O(wl) to slice
               -> O(n_s * wl) overall.
        Space: O(n_w * wl) for the counters.
        """
        if not s or not words:
            return []

        wl, n = len(words[0]), len(words)
        need = Counter(words)
        result = []

        for offset in range(wl):              # wl independent lanes
            lo = offset
            count = 0
            window = Counter()

            for hi in range(offset, len(s) - wl + 1, wl):
                block = s[hi:hi + wl]

                if block not in need:
                    window.clear()            # unknown word: nothing is salvageable
                    count = 0
                    lo = hi + wl              # restart the lane after it
                    continue

                window[block] += 1
                count += 1

                while window[block] > need[block]:   # too many of THIS word
                    window[s[lo:lo + wl]] -= 1
                    lo += wl
                    count -= 1

                if count == n:                # a full concatenation ends here
                    result.append(lo)
                    window[s[lo:lo + wl]] -= 1   # slide on to look for the next
                    lo += wl
                    count -= 1

        return sorted(result)
```
**Time:** O(n_s · wl) · **Space:** O(n_w · wl)

### Why the lanes don't overlap, said precisely
Lane `r` visits indices `r, r+wl, r+2wl, …`. Two lanes with different `r` share no
index, and a valid answer is a run of consecutive blocks all on one lane. So every
answer is found exactly once, by exactly one lane, no deduplication needed, and
`sorted()` at the end is only there because the lanes finish out of order.

## ⚠️ Gotchas
- **Reset on an unknown word; shrink on a surplus word.** Using `clear()` for both is
  wrong (you'd lose valid partial windows and miss answers like index 9 above); using
  shrink for both loops forever, because removing words never makes an unknown block
  become known.
- **After recording a hit, slide by one word**: don't clear. Overlapping answers are
  possible (`s = "aaaaaa"`, `words = ["aa","aa"]` has several), and clearing loses
  them.
- **`range(offset, len(s) - wl + 1, wl)`**: the `- wl + 1` keeps the final slice
  in bounds. Python would silently return a short string otherwise, which compares
  unequal to every word and merely *looks* like it's working.
- **Duplicate words in `words` are meaningful.** `["word","good","best","word"]` needs
  two `"word"`s. A `set` here is wrong, and the second example is specifically built to
  catch it.
- **All words are guaranteed the same length.** The lane decomposition depends on it
  completely, say so out loud; if lengths varied, this becomes a different (much
  harder) problem.
- Slicing `s[hi:hi+wl]` allocates a new string each time, which is where the extra
  `wl` factor in the time bound comes from. Rolling hashes remove it and are almost
  never worth the risk in an interview.

## 🎤 Interview talking points
- *"All words share a length, so any answer is aligned to one of `wl` grids. I run the
  window once per offset, together they still visit each character a constant number
  of times."*
- *"There are two failure modes and they need different handling: an unknown word can
  never be part of a later window on this lane, so I reset; a surplus word just means I
  started too early, so I shrink."*
- *"I'd write the straightforward O(n·m·wl) check first, confirm it passes, and offer
  this as the refinement."* ← the right answer in a real interview, and saying it is
  not a weakness.

## 🔗 Transfer
This closes Pattern 03. The lane idea, **decompose by offset when the unit is bigger
than one element**: comes back in string-hashing and in block-based problems generally.
Next up is Pattern 04 (Kadane), which is a different answer to "contiguous subarray"
questions: instead of maintaining a window, you keep one running decision per element.

## 📹 Metadata
- **Title:** `Substring with Concatenation of All Words, three grids, not one | Sliding Window #12`
- **Thumbnail:** `WORDS, NOT LETTERS` (amber block)
- **Short:** The offset-0/1/2 grid drawing, "these can never interfere." 55s.
