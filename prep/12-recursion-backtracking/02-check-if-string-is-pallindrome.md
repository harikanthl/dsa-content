# EP112 · P12E02 · Check if String is Palindrome   [Easy]

**Pattern:** Recursion and Backtracking · **Link:** https://www.geeksforgeeks.org/problems/palindrome-string0817/1

---

## 🎬 Hook
> "A palindrome is a string whose first and last letters match, **with a palindrome in
> the middle.** That sentence is the whole algorithm. Say it out loud and the recursion
> writes itself: the only real decision is what to pass to the smaller call, and the
> obvious choice, a slice, quietly makes it O(n²)."

## 📋 Problem, in your words
```
Given a string S, return True if it reads the same forwards and backwards,
otherwise False.

Solve it recursively.
```

## 🔢 The example
```
Input:  "racecar"   -> True
Input:  "abba"      -> True     <- even length: the middle is EMPTY
Input:  "abca"      -> False    <- outer pair a/a matches, inner pair b/c doesn't
Input:  "a"         -> True     <- one character is always a palindrome
Input:  ""          -> True     <- so is nothing
```

## 🧸 ELI5
> Hold a word written on a strip of paper. Look at the two ends. Same letter? Snip both
> off and hand the shorter strip to a friend with the same question. Different letters?
> Stop, it's not a palindrome.
>
> ```
> r a c e c a r     r = r ✓  snip
>   a c e c a       a = a ✓  snip
>     c e c         c = c ✓  snip
>       e           one letter left: yes, automatically
> ```
>
> Your friend doesn't need to know anything about the letters you already snipped.
> They only need the strip in front of them. That's what "trust the smaller call"
> means.

## 🐌 Brute force (say it, don't type it)
In Python the honest answer is one line, `return s == s[::-1]`, O(n) time and O(n)
space for the reversed copy. A two-pointer loop does it in O(1) space (that's EP001's
Shape A, converging from both ends).

Both are better than recursion in production. This episode is here because it's the
same converging-pointer idea you already know, **rewritten as a recursive call**. If
you can see that `lo + 1, hi - 1` in a loop and `check(lo + 1, hi - 1)` in a recursion
are the same move, the recursion stops being magic.

## 💡 The pattern reveal
**Signal:** the definition refers to itself: a palindrome contains a smaller palindrome.
**Therefore:** Shape A, one smaller call, shrinking from **both ends** at once.

| question | answer here |
|---|---|
| smallest input, answered without recursing? | length 0 or 1 → `True` |
| the early exit? | ends differ → `False`, no call at all |
| how does n follow from smaller? | ends match **and** the middle is a palindrome |

**Key insight: pass indices, not slices.** The tempting version is:

```python
return s[0] == s[-1] and is_pal(s[1:-1])     # correct, and O(n²)
```

`s[1:-1]` **copies** the string every call: n + (n-2) + (n-4) + ... = O(n²) time and
O(n²) total memory churn. Passing `lo` and `hi` shares one string between every frame
and each call does O(1) work.

## 🔍 Dry run: `"abba"`, the call stack

| step | stack (top on the right) | lo, hi | s[lo], s[hi] | event |
|---|---|---|---|---|
| 1 | P(0,3) | 0, 3 | a, a | match, call P(1,2) |
| 2 | P(0,3) P(1,2) | 1, 2 | b, b | match, call P(2,1) |
| 3 | P(0,3) P(1,2) P(2,1) | 2, 1 | - | `lo >= hi`, returns **True** |
| 4 | P(0,3) P(1,2) | | | returns True |
| 5 | P(0,3) | | | returns **True** |

Even length ends with `lo > hi` (the pointers crossed). Odd length ends with
`lo == hi` (one middle letter). `lo >= hi` handles both.

## 🔍 Dry run: `"abca"`

| step | stack | lo, hi | s[lo], s[hi] | event |
|---|---|---|---|---|
| 1 | P(0,3) | 0, 3 | a, a | match, call P(1,2) |
| 2 | P(0,3) P(1,2) | 1, 2 | b, c | **differ**, returns False |
| 3 | P(0,3) | | | returns **False** |

The mismatch at depth 2 flows straight up. No frame above it does any more work.

## ✅ Optimal solution
```python
def is_palindrome(s: str) -> bool:
    """True if s reads the same both ways, checked recursively from the ends inward.

    Time:  O(n), n/2 calls, O(1) work each.
    Space: O(n), the call stack is n/2 frames deep. No copies of s.
    """

    def check(lo: int, hi: int) -> bool:
        if lo >= hi:                  # 0 or 1 characters left: a palindrome
            return True
        if s[lo] != s[hi]:            # outer pair differs: stop right here
            return False
        return check(lo + 1, hi - 1)  # trust the smaller call on the middle

    return check(0, len(s) - 1)
```
**Time:** O(n) · **Space:** O(n) call stack

If the judge wants `1`/`0` instead of a bool, wrap it: `return int(is_palindrome(s))`.

## ⚠️ Gotchas
- **Slicing is the hidden O(n²).** `s[1:-1]` builds a new string every frame. Say it
  when you write the index version, it's the point of the episode.
- **`lo >= hi`, not `lo == hi`.** Even-length strings never land on `lo == hi`; the
  pointers cross. `==` alone recurses forever on `"abba"`.
- **The empty string.** `check(0, -1)` hits `lo >= hi` immediately and returns True.
  Check it rather than special-casing it.
- **Depth is n/2.** Python's default recursion limit is about 1000, so a string over
  ~2000 characters raises `RecursionError`. The loop version has no such limit, and
  that's the honest trade-off to mention.
- **Case and punctuation.** This problem compares characters exactly. LeetCode 125
  (Valid Palindrome) skips non-alphanumerics and ignores case; don't import those rules
  here unless asked.

## 🎤 Interview talking points
- *"A palindrome is matching ends around a smaller palindrome, so the recursion is: check
  the ends, then trust the call on the middle."*
- *"I pass indices rather than slices, because slicing copies and turns this into
  O(n²)."* ← the line that separates a clean answer from a correct one.
- *"`lo >= hi` is the base case because even lengths cross and odd lengths meet."*
- *"It's O(n) time and O(n) stack space; the iterative two-pointer version is O(1)
  space, and that's what I'd ship."*

## 🔗 Transfer
This is EP001's converging pointers wearing a recursion costume, and seeing that
costume clearly is the goal. EP113 uses the same index trick moving in **one**
direction, and EP120 (Palindrome Partitioning) calls exactly this check thousands of
times as its prune.

## 📹 Metadata
- **Title:** `Palindrome check, the slice that makes it O(n²) | Recursion #2`
- **Thumbnail:** `s[1:-1] = O(n²)` (red strike through the slice)
- **Short:** the paper strip being snipped from both ends, "racecar" to "e". 40s.
