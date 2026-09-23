# EP120 · P12E10 · Palindrome Partitioning   [Medium]

**Pattern:** Recursion and Backtracking · **Link:** https://leetcode.com/problems/palindrome-partitioning/description/

---

## 🎬 Hook
> "Cut a string into pieces so that every piece reads the same backwards, and list
> every way to do it. It looks like a string problem. It's the backtracking template
> again, except the choice at each step isn't *which item*, it's **where to cut**, and
> the palindrome check is the pruning."

## 📋 Problem, in your words
```
Given a string s, split it into substrings so that every substring is a palindrome.
Return all possible such splits.

  - every character belongs to exactly one piece
  - pieces stay in their original order
  - a single character is always a palindrome
```

## 🔢 The example
```
Input:  s = "aab"
Output: [["a", "a", "b"], ["aa", "b"]]

Input:  s = "a"
Output: [["a"]]

Input:  s = "abc"
Output: [["a", "b", "c"]]     <- the all-singles split always exists
```

## 🧸 ELI5
> You've got a ribbon with letters on it and a pair of scissors. You're only allowed
> to cut off a piece from the **front** of the ribbon, and only if that piece reads
> the same both ways.
>
> ```
> ribbon: a a b
>
> cut after 1 letter:  "a"   ✓ palindrome, keep cutting "ab"
> cut after 2 letters: "aa"  ✓ palindrome, keep cutting "b"
> cut after 3 letters: "aab" ✗ not a palindrome, don't even try
> ```
>
> Every time the ribbon runs out, the pile of pieces in your hand is one answer. Then
> you tape the last piece back on (unchoose) and try a longer cut instead.

## 🐌 Brute force (say it, don't type it)
A string of length n has n - 1 gaps, and each gap is either cut or not: 2^(n-1) ways
to split. Generate them all, then check every piece of every split. It works, and it
spends most of its time building splits that were doomed at the very first piece. The
backtracker below visits the same tree but stops descending the moment a piece fails.

## 💡 The pattern reveal
**Signal:** "return **all** possible partitions" · a string · a validity rule per piece.
**Therefore:** backtracking, flavour 4 from the pattern card: **partitioning**.

**Key insight:** the state is just **where the uncut part starts**. At each step, try
every prefix of the remainder as the next piece. If it's a palindrome, commit it and
recurse on what's left. If not, that branch never starts: **the check is the prune.**

| template slot | in this problem |
|---|---|
| state | `start`, the index where the uncut ribbon begins |
| choices | every `end` from `start + 1` to `n` |
| allowed? | `s[start:end]` is a palindrome |
| complete | `start == len(s)`, nothing left to cut |

```python
for end in range(start + 1, len(s) + 1):
    if is_pal(start, end - 1):             # the check IS the prune
        path.append(s[start:end])          # choose
        cut(end)                           # explore the rest
        path.pop()                         # unchoose
```

## 🔍 Dry run: `s = "aab"`

The decision tree. Each edge is a piece cut from the front:

```
                     "aab"
        "a" /        "aa" |       "aab" x   (not a palindrome)
          "ab"             "b"
    "a" /    "ab" x    "b" |
      "b"                  "" ✓ ["aa","b"]
  "b" |
      "" ✓ ["a","a","b"]
```

| step | call | path before | try `s[start:end]` | palindrome? | action |
|---|---|---|---|---|---|
| 1 | `cut(0)` | `[]` | `"a"` | ✓ | choose → `["a"]` |
| 2 | `cut(1)` | `["a"]` | `"a"` | ✓ | choose → `["a","a"]` |
| 3 | `cut(2)` | `["a","a"]` | `"b"` | ✓ | choose → `["a","a","b"]` |
| 4 | `cut(3)` | `["a","a","b"]` | - | - | start == 3, **record** |
| 5 | `cut(2)` | `["a","a"]` | (no more ends) | - | return, pop → `["a"]` |
| 6 | `cut(1)` | `["a"]` | `"ab"` | ✗ | **pruned**, never recurse; pop → `[]` |
| 7 | `cut(0)` | `[]` | `"aa"` | ✓ | choose → `["aa"]` |
| 8 | `cut(2)` | `["aa"]` | `"b"` | ✓ | choose → `["aa","b"]` |
| 9 | `cut(3)` | `["aa","b"]` | - | - | **record**; pop → `[]` |
| 10 | `cut(0)` | `[]` | `"aab"` | ✗ | **pruned** |

Answer **`[["a","a","b"], ["aa","b"]]`** ✓

## ✅ Optimal solution
```python
class Solution:
    def partition(self, s: str) -> List[List[str]]:
        """Every way to split s into pieces that are all palindromes.

        Time:  O(n · 2^n): up to 2^(n-1) partitions, O(n) to check and copy each.
        Space: O(n) for the recursion stack and path, excluding the output.
        """
        results, path = [], []

        def is_pal(lo: int, hi: int) -> bool:
            while lo < hi:                  # two pointers, no slice needed to check
                if s[lo] != s[hi]:
                    return False
                lo += 1
                hi -= 1
            return True

        def cut(start: int) -> None:
            if start == len(s):             # nothing left to cut: path is an answer
                results.append(path[:])
                return
            for end in range(start + 1, len(s) + 1):
                if is_pal(start, end - 1):              # the check is the prune
                    path.append(s[start:end])           # choose
                    cut(end)                            # explore the rest
                    path.pop()                          # unchoose

        cut(0)
        return results
```
**Time:** O(n · 2^n) · **Space:** O(n) excluding the output

## ⚠️ Gotchas
- **Slicing costs O(n) every time.** `s[start:end] == s[start:end][::-1]` builds two
  new strings per check. Checking with two pointers on indices creates nothing, and
  you slice only once a piece has already passed. Same big-O, less garbage, and worth
  saying.
- **The speedup is a table, and it's DP.** The same substrings get checked again and
  again in different branches. Precompute `pal[i][j]` once in O(n²):
  `pal[i][j] = s[i] == s[j] and (j - i < 2 or pal[i + 1][j - 1])`, filled with `i`
  going **downwards**. Now every check is O(1). That's Pattern 15 (EP172 onward)
  showing up inside a backtracker; mention it, don't necessarily type it.
- **`end` runs to `len(s)` inclusive of the slice end.** `range(start + 1, len(s) + 1)`.
  Stop at `len(s)` and you never try the piece that takes the whole remainder, so
  `"aa"` loses its `["aa"]` answer.
- **`is_pal(start, end - 1)`: the slice end is exclusive, the check's `hi` is not.**
  Mixing the two conventions is the off-by-one in this problem.
- **`path[:]`.** Same as every episode in this pattern. `[[], []]` means you forgot.
- **There is always at least one answer.** Single characters are palindromes, so the
  all-singles split exists for any non-empty string. If you ever return `[]` for a
  non-empty input, the loop bounds are wrong.

## 🎤 Interview talking points
- *"The state is where the uncut part begins. At each step I try every prefix of the
  remainder as the next piece."*
- *"The palindrome check happens before the recursive call, so it's the pruning: a bad
  first piece kills the whole branch."*
- *"Worst case is a string of identical letters: every split is valid, 2^(n-1) of
  them, so O(n · 2^n) is also a lower bound on the output."*
- *"To stop re-checking the same substrings, I'd precompute an n by n palindrome table
  in O(n²), which makes every check O(1)."* ← say this unprompted; it's the follow-up.
- *"If they asked for the **minimum** number of cuts instead of all partitions, that's
  Palindrome Partitioning II, and it's pure DP."*

## 🔗 Transfer
This closes the pattern. Across EP116 to EP120 the template never changed: choose,
explore, unchoose, with a copy at the leaf. Only three things moved: what a choice is
(a character, a number, a cut), what's allowed (the pruning), and what "complete"
means. **Recap video:** put Generate Parentheses, Permutations, Combination Sum and
this side by side and fill in the template table for each; that's the whole pattern
on one screen.

Next is EP121, Tree Inorder traversal. From here on recursion stops being the topic
and becomes the default tool: every one of the 31 tree episodes is "trust the call on
the left child, trust the call on the right child, combine." If today felt natural,
trees will too.

## 📹 Metadata
- **Title:** `Palindrome Partitioning, the choice is where to cut | Backtracking #5`
- **Thumbnail:** `✂️ WHERE TO CUT` (red block)
- **Short:** the ribbon ELI5 on `"aab"`, scissors animation, two answers. 50s.
