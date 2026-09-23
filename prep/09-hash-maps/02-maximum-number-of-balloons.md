# EP068 · P09E02 · Maximum Number of Balloons   [Easy]

**Pattern:** Hash Maps · **Link:** https://leetcode.com/problems/maximum-number-of-balloons/

---

## 🎬 Hook
> "How many times can you spell 'balloon' from a pile of letters? The scarcest letter
> decides. The trap is that 'balloon' needs **two** l's and **two** o's, so you have to
> divide before you compare, and the version everyone writes from memory forgets to."

## 📋 Problem, in your words
```
Given a string text, you may use each character at most once.
Return the maximum number of times you can form the word "balloon".
```

## 🔢 The example
```
Input:  "nlaebolko"           -> 1
Input:  "loonbalxballpoon"    -> 2
Input:  "leetcode"            -> 0     no 'b' at all
```

## 🧸 ELI5
> You're making fruit baskets. Each basket needs 1 banana, 1 apple, **2** lemons and
> **2** oranges. You've got 10 bananas, 10 apples, 4 lemons and 9 oranges.
>
> ```
> bananas:  10 / 1 = 10 baskets' worth
> apples:   10 / 1 = 10
> lemons:    4 / 2 =  2    <- the bottleneck
> oranges:   9 / 2 =  4
> ```
>
> You can make **2** baskets. Not 4 (the lemon count), not 10 (the banana count).
> Each fruit tells you how many baskets it could support *on its own*, and the answer
> is the smallest of those.
>
> "balloon" is the basket. `l` and `o` are the lemons and oranges.

## 🐌 Brute force (say it, don't type it)
Repeatedly try to remove one `b`, `a`, two `l`s, two `o`s and one `n` from the text
(for example with `.replace(ch, '', 1)`), counting how many full rounds succeed.
Each round rescans the string: **O(n²)** in the worst case. It's a simulation of the
answer, not a calculation of it.

## 💡 The pattern reveal
**Signal:** "how many times can you **form** X from Y" · "each character at most once".
**Therefore:** Shape A from the card: count, then interrogate the counts, as a
**budget with a ratio**.

**Key insight:** each letter of the target independently caps the answer at
`have[ch] // need[ch]`. The real answer is the **minimum** of those caps, because the
scarcest letter runs out first and the rest are surplus.

```python
have = Counter(text)
need = Counter("balloon")            # b:1 a:1 l:2 o:2 n:1, the ratios come free
return min(have[ch] // need[ch] for ch in need)
```

**Why it's correct:** `k` copies are possible iff `have[ch] >= k * need[ch]` for every
`ch` in the target, iff `k <= have[ch] // need[ch]` for every `ch`. The largest `k`
satisfying all of them is the minimum of the right-hand sides.

## 🔍 Dry run: `"loonbalxballpoon"`

| letter | have | need | have // need |
|---|---|---|---|
| `b` | 2 | 1 | 2 |
| `a` | 2 | 1 | 2 |
| `l` | 4 | **2** | 2 |
| `o` | 4 | **2** | 2 |
| `n` | 2 | 1 | 2 |

`min = 2` → answer **2** ✓. The `x` and `p` never matter, they aren't in `need`.

**The same table without dividing by need** (the bug):

| letter | have |
|---|---|
| `l` | 4 |
| `o` | 4 |
| `b`, `a`, `n` | 2 |

Still gives 2 here, by luck. Try `"balon"`: `l` and `o` are 1 each, `min(have)` says
**1**, but you can't spell "balloon" once. `1 // 2 = 0` → the correct answer is **0**.
That's the input to show on camera.

## ✅ Optimal solution
```python
from collections import Counter

class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        """How many times "balloon" can be spelled from the letters of text.

        Time:  O(n), one pass to count, then 5 lookups.
        Space: O(1), at most 26 keys.
        """
        have = Counter(text)
        need = Counter("balloon")            # b:1 a:1 l:2 o:2 n:1

        # each letter caps the answer at have // need; the scarcest letter wins
        return min(have[ch] // need[ch] for ch in need)
```
**Time:** O(n) · **Space:** O(1)

## ⚠️ Gotchas
- **Divide by `need[ch]`, not by 1.** `"balon"` is the input that exposes it. Build
  `need` with `Counter("balloon")` so the 2s come from the word, not your memory.
- **Missing letters must read as 0.** `"leetcode"` has no `b`. With `Counter`,
  `have['b']` is 0 and the `min` is 0. With a plain dict, `have['b']` raises
  `KeyError`. Use `have.get(ch, 0)` if you're not on a `Counter`.
- **Iterate `need`, not `have`.** Letters in the text that aren't in "balloon" are
  irrelevant. Taking the `min` over `have` includes the `x` in `"loonbalxballpoon"`
  and gives the wrong answer.
- **`//` not `/`.** Half a balloon isn't a balloon, and `/` returns a float that the
  judge will reject.
- **Generalise out loud:** pass the target word as a parameter and nothing else
  changes. LeetCode 2287 (Rearrange Characters to Make Target String) is this exact
  function.

## 🎤 Interview talking points
- *"Every letter of the target caps the answer at have divided by need, and the
  scarcest one decides, so it's a min over five ratios."*
- *"I build `need` from the word itself so the doubled l and o can't be forgotten."*
- *"O(n) time, O(1) space, because the alphabet is fixed."*
- *"This works for any target word, not just balloon. The word is just a Counter."*

## 🔗 Transfer
EP67 needed the input's order back after counting. This one throws order away
completely: only the piles matter. EP69 asks the piles a different question (how many
pair up), and EP70 generalises "can I form this word once" to "can I form this whole
note". The `min(have // need)` budget comes back in Binary Search on the answer
(EP81–88), where "can I do it `k` times?" becomes a predicate you search over.

## 📹 Metadata
- **Title:** `Maximum Number of Balloons, the scarcest letter decides | Hash Maps #2`
- **Thumbnail:** `DIVIDE BY 2` (red block)
- **Short:** the fruit-basket ELI5 and `"balon"` returning 1 instead of 0. 40s.
