# EP067 · P09E01 · First Non-repeating Character   [Easy]

**Pattern:** Hash Maps · **Link:** https://leetcode.com/problems/first-unique-character-in-a-string/

---

## 🎬 Hook
> "You can't know a letter is unique until you've read the whole string. That one fact
> forces two passes, and the second pass has to walk the **string**, not the dictionary,
> because the dictionary knows *how many* and only the string knows *where*."

## 📋 Problem, in your words
```
Given a string s of lowercase letters, return the INDEX of the first
character that appears exactly once in s.

If every character repeats, return -1.
```

## 🔢 The example
```
Input:  "leetcode"       -> 0     'l' appears once and comes first
Input:  "loveleetcode"   -> 2     'l' and 'o' repeat; 'v' is the first loner
Input:  "aabb"           -> -1    nothing appears once
```
`"loveleetcode"` is the one to put on screen. The first character, `l`, *looks* unique
for the first four letters, and only the `l` at index 4 exposes it. That is the whole
reason one pass can't work.

## 🧸 ELI5
> A class photo, and you want the first kid (standing left to right) who has no twin in
> the class.
>
> You can't decide about the first kid by looking at the first kid. Their twin could be
> standing at the far end. So you do it in two walks:
>
> 1. **Walk the row once and tally names on a clipboard.** `l: 2, o: 2, v: 1, e: 4 ...`
> 2. **Walk the row again from the left**, glance at the clipboard for each kid, and stop
>    at the first one whose tally is 1.
>
> ```
> "l o v e l e e t c o d e"
>  2 2 1 4 ...
>      ^ first tally of 1 -> index 2
> ```
>
> The clipboard can't answer "who's first", it has no idea where anyone stands. The row
> can't answer "who's unique" without being read end to end. You need both.

## 🐌 Brute force (say it, don't type it)
For each index `i`, scan the whole string to see whether `s[i]` appears anywhere else.
Return the first `i` that survives. **O(n²)** time, O(1) space.

Honest note: `s.count(ch) == 1` inside a loop is the one-liner people write, and it *is*
this brute force, `.count` rescans the string every time. On a 26-letter alphabet it
still passes LeetCode because you can loop over the 26 letters instead of the n
positions. Say that, then say the interviewer wants the pattern, not the trick.

## 💡 The pattern reveal
**Signal:** "appears **exactly once**" · "**first**".
**Therefore:** Shape B from the card: count, then walk the original in order.

**Key insight:** "exactly once" is a question about **counts**, "first" is a question
about **order**. A `Counter` answers the first in one pass; the string itself answers
the second in another. Neither structure can answer both.

```python
counts = Counter(s)                  # pass 1: how many of each
for i, ch in enumerate(s):           # pass 2: in the string's order
    if counts[ch] == 1:
        return i
return -1
```

**Why it's correct:** after pass 1, `counts[ch] == 1` is exactly "ch is unique in s".
Pass 2 checks positions in increasing order, so the first hit is the smallest index
with that property. There is nothing left to prove.

## 🔍 Dry run: `"loveleetcode"`

**Pass 1 (counting):**

| letter | l | o | v | e | t | c | d |
|---|---|---|---|---|---|---|---|
| count | 2 | 2 | **1** | 4 | 1 | 1 | 1 |

**Pass 2 (walking s):**

| i | s[i] | counts[s[i]] | == 1? |
|---|---|---|---|
| 0 | `l` | 2 | no |
| 1 | `o` | 2 | no |
| 2 | `v` | 1 | **yes → return 2** |

Answer **2** ✓. Note `t`, `c` and `d` also have count 1, and the dictionary doesn't
know `v` beats them. The walk does.

## ✅ Optimal solution
```python
from collections import Counter

class Solution:
    def firstUniqChar(self, s: str) -> int:
        """Index of the first character that appears exactly once, else -1.

        Time:  O(n), two passes over s.
        Space: O(1), at most 26 keys in the counter.
        """
        counts = Counter(s)                  # pass 1: letter -> how many

        for i, ch in enumerate(s):           # pass 2: walk s, because s knows the order
            if counts[ch] == 1:
                return i

        return -1                            # every character repeats
```
**Time:** O(n) · **Space:** O(1) (26 letters)

## ⚠️ Gotchas
- **Walk `s`, not `counts`.** `for ch, n in counts.items()` happens to work in Python
  3.7+ because dicts keep insertion order, which for a string is first-appearance order.
  That's an accident of the language, not the algorithm. Walk `s` and say why.
- **Return the index, not the character.** The LeetCode version wants `2`, not `'v'`.
  Some versions of this problem (the GfG one) want the character. Read the signature.
- **`-1` when nothing is unique.** `"aabb"` falls off the end of the loop. Don't forget
  the final return.
- **One pass is impossible here, and you should say so.** You can't commit to `l` at
  index 0 until you've seen index 4. "Could you do it in one pass?" is the follow-up;
  the answer is "one pass over s plus one over the 26-letter alphabet, if I also store
  each letter's first index." That's the stream variant.
- **An array of 26 works too:** `counts[ord(ch) - ord('a')]`. Same complexity, no
  import. Mention it, use `Counter` on camera for readability.

## 🎤 Interview talking points
- *"Unique is a count question, first is an order question. The counter answers one,
  the string answers the other."*
- *"I need the counting pass to finish before I can trust any count, so it's two
  passes, both O(n)."*
- *"Space is O(1): at most 26 keys, whatever the length of the string."*
- *"If this were a stream and I couldn't reread it, I'd store each letter's first index
  alongside its count and scan the 26 letters at the end."* ← the follow-up, answered
  before it's asked.

## 🔗 Transfer
This is Shape B, the only episode in the pattern where order survives counting. EP68
and EP69 throw the order away entirely and only ask the piles. EP70 counts two strings
and compares piles. The "count first, then walk the original" move comes back in
Sliding Window's anagram problems (EP30, EP31) and in Heap's Top K Frequent (EP96).

## 📹 Metadata
- **Title:** `First Unique Character, the dictionary doesn't know who's first | Hash Maps #1`
- **Thumbnail:** `WALK THE STRING` (red block)
- **Short:** the ELI5 class photo, with `loveleetcode` and the `l` that only looks unique. 45s.
