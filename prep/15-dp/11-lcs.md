# EP182 · P15E11 · Longest Common Subsequence   [Medium]

**Pattern:** DP (Dynamic Programming) · **Link:** https://leetcode.com/problems/longest-common-subsequence/description/

---

## 🎬 Hook
> "Two strings, and you want the longest sequence of letters that appears in both, in
> order. The state is **two pointers**, one in each string, and at every step there are
> only two situations: the letters **match**, or they **don't**. That's the entire
> algorithm behind `diff` and DNA alignment."

## 📋 Problem, in your words
```
Given strings text1 and text2, return the length of their longest common
subsequence: the longest string you can get from BOTH by deleting characters
without reordering. Return 0 if there is none.

1 <= len(text1), len(text2) <= 1000, lowercase letters.
```

## 🔢 The example
```
Input:  text1 = "abcde", text2 = "ace"
Output: 3                 ("ace")

Input:  text1 = "abc", text2 = "abc"   -> 3
Input:  text1 = "abc", text2 = "def"   -> 0
```

## 🧸 ELI5
> Two friends each read out a list of letters, one at a time, and you're trying to find
> the longest run of letters **both** of them said, in the same order.
>
> Look at the first letter from each friend:
>
> ```
>   same letter?   ->  great, it's in the answer. Both friends move on.   (+1)
>   different?     ->  one of the two letters isn't in the answer.
>                      Try throwing away friend A's, try throwing away friend B's,
>                      keep whichever turns out better.
> ```
>
> "Which one to throw away" is the choice you can't make greedily, so you try both and
> write every (position in A, position in B) answer on a grid.

## 🐌 Brute force (say it, don't type it)
List all 2^m subsequences of `text1` and check each against `text2` in O(n):
**O(2^m · n)**. At m = 1000, never. The match/no-match recursion has only
`(m + 1) × (n + 1)` distinct `(i, j)` pairs; that grid is the DP.

## 💡 The pattern reveal
**Signal:** **two sequences** · **subsequence** · "longest".
**Therefore:** DP, Shape D (two sequences: the state is a pair).

**State:** `dp[i][j]` = LCS of the **prefixes** `text1[:i]` and `text2[:j]`.

**Recurrence**, comparing the last characters of those prefixes, `text1[i-1]` and
`text2[j-1]`:

| case | `dp[i][j]` | reads |
|---|---|---|
| match | `dp[i-1][j-1] + 1` | the diagonal ↖ |
| no match | `max(dp[i-1][j], dp[i][j-1])` | up ↑ (drop a char from text1) or left ← (drop from text2) |

**Base:** row 0 and column 0 are **the empty prefix**. LCS with an empty string is 0.

**Key insight:** on a match, taking the character is **always** safe (a proof sketch:
any common subsequence that doesn't use this match can be rewritten to use it without
getting shorter). So there's no "match but skip" branch. The only real choice is on a
mismatch, and it's only two ways.

Fill order: each cell reads up, left and up-left, so **row by row, left to right**.

## 🔍 Dry run: `text1 = "abcde"`, `text2 = "ace"`

Rows are prefixes of `text1`, columns prefixes of `text2`. `""` = empty prefix.

| | "" | a | c | e |
|---|---|---|---|---|
| **""** | 0 | 0 | 0 | 0 |
| **a** | 0 | **1** ↖ | 1 | 1 |
| **b** | 0 | 1 | 1 | 1 |
| **c** | 0 | 1 | **2** ↖ | 2 |
| **d** | 0 | 1 | 2 | 2 |
| **e** | 0 | 1 | 2 | **3** ↖ |

Answer bottom-right: **3** ✓. Bold cells are the matches, each one 1 + its diagonal.

Narrate three cells:
- **(a, a) → 1:** match. Diagonal is `dp[0][0]` = 0, so 0 + 1.
- **(b, c) → 1:** `b ≠ c`. Up is (a, c) = 1, left is (b, a) = 1. Max 1.
- **(e, e) → 3:** match. Diagonal is (d, c) = 2, so 3. The "ace" is the three diagonal
  steps.

## ✅ Optimal solution
```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        """LCS length.

        dp[i][j] = LCS of text1[:i] and text2[:j]; row 0 / col 0 are empty prefixes.
        Time:  O(m * n), each cell O(1).
        Space: O(m * n) for the grid.
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:          # prefix i ends at index i - 1
                    dp[i][j] = dp[i - 1][j - 1] + 1       # match: extend the diagonal
                else:
                    dp[i][j] = max(dp[i - 1][j],          # drop text1's char
                                   dp[i][j - 1])          # drop text2's char
        return dp[m][n]
```
**Time:** O(m · n) · **Space:** O(m · n)

The memo form (step 3), with indices walking forward instead:

```python
@lru_cache(maxsize=None)
def f(i: int, j: int) -> int:                  # LCS of text1[i:] and text2[j:]
    if i == len(text1) or j == len(text2):
        return 0
    if text1[i] == text2[j]:
        return 1 + f(i + 1, j + 1)
    return max(f(i + 1, j), f(i, j + 1))
```

Space-optimised, two rows (each row reads only the row above):

```python
prev = [0] * (n + 1)
for i in range(1, m + 1):
    cur = [0] * (n + 1)
    for j in range(1, n + 1):
        cur[j] = prev[j - 1] + 1 if text1[i - 1] == text2[j - 1] else max(prev[j], cur[j - 1])
    prev = cur
return prev[n]
```

## ⚠️ Gotchas
- **`dp[i][j]` compares `text1[i-1]`, not `text1[i]`.** Row `i` is "the first `i`
  characters". This is pattern-card trap #3 in its purest form: write `text1[i]` and
  the last row reads past the end of the string, an IndexError on the very first test.
- **No `+1` on a mismatch, and no three-way max on a match.** On a match, `dp[i-1][j-1]
  + 1` is always at least as big as up or left, so checking them is wasted work (harmless,
  but it tells the interviewer you don't know why).
- **Two-row version needs a fresh `cur` each row**, or a single row plus a saved
  diagonal variable. Reusing one row naively loses `dp[i-1][j-1]` before you read it.
- **Subsequence ≠ substring.** Longest common *substring* resets to 0 on a mismatch
  instead of taking the max, and the answer is the max cell, not the corner.

## 🎤 Interview talking points
- *"The state is a pair of prefix lengths, so the table is (m+1) by (n+1), with row and
  column 0 as the empty prefix."*
- *"If the last characters match, they're in the LCS: one plus the diagonal. If not,
  one of them isn't, so I take the better of dropping either."*
- *"O(mn) time. Each row only reads the one above, so O(min(m, n)) space if I put the
  shorter string on the columns."*
- *"Edit distance is the same grid with three operations and a min; diff tools are LCS
  underneath."*

## 🔗 Transfer
The state just became a **pair**, and that grid shape is the template for Edit
Distance, Longest Palindromic Subsequence (LCS of a string and its reverse), Shortest
Common Supersequence and Distinct Subsequences. EP183 Unique Paths is the same grid
with no strings at all: two neighbours instead of three, and a border of 1s instead of
0s.

## 📹 Metadata
- **Title:** `LCS, match goes diagonal, mismatch takes the max | DP #11`
- **Thumbnail:** `↖ +1   or   max(↑, ←)`
- **Short:** the grid filling row by row, the three diagonal matches lighting up to
  spell "ace". 45s.
