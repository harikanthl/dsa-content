# EP115 · P12E05 · Remove Occurrences of a Character in a String   [Easy]

**Pattern:** Recursion and Backtracking · **Link:** https://www.geeksforgeeks.org/problems/remove-all-occurrences-of-a-character-in-a-string/1

---

## 🎬 Hook
> "The first four episodes returned a number or a yes/no. This one has to **return a
> string**, which means the frames aren't just checking things any more, they're
> building the answer on the way back up. And the natural way to build it, `s[i] +
> rest`, is secretly O(n²). The fix is a list you pass down, and that list is the `path`
> that runs every backtracking problem from tomorrow on."

## 📋 Problem, in your words
```
Given a string s and a character c, return s with every occurrence of c removed.
The order of the remaining characters stays the same.
Solve it recursively.
```

## 🔢 The example
```
Input:  s = "banana", c = "a"   -> "bnn"
Input:  s = "hello",  c = "z"   -> "hello"   <- nothing to remove
Input:  s = "aaaa",   c = "a"   -> ""        <- everything removed
Input:  s = "",       c = "a"   -> ""
```

## 🧸 ELI5
> A row of letter tiles. You look at the **first** tile only. Hand the rest of the row
> to a friend: "give me this row with the a's taken out." When they hand it back, you
> either stick your tile on the front, or, if your tile is an `a`, throw it away and
> pass their answer on untouched.
>
> ```
> b a n a n a
> b | "anana" -> friend returns "nn"  -> "b" + "nn" = "bnn"
> a | "nana"  -> friend returns "nn"  -> drop the a  = "nn"
> ```
>
> Going down, nobody decides anything. Coming back up, **every tile gets its keep-or-drop
> decision.** That's the new move in this episode.

## 🐌 Brute force (say it, don't type it)
`s.replace(c, "")` is the answer in Python, O(n) time, done. A loop with a list and
`"".join` is the same thing by hand.

Recursion is here for the shape, not the speed. EP111 to EP114 returned a value.
This one **accumulates output**, and there are two ways to do that recursively: build it
on the way back up, or carry a list down and append to it. The second way is how every
problem from EP116 onwards works, so this is where you learn it on an easy problem.

## 💡 The pattern reveal
**Signal:** process one character, recurse on the rest, output must preserve order.
**Therefore:** Shape A with an index (EP113's walk), plus an accumulator.

**Version 1: build on the way back up.** The natural recursive thought:

```python
def rem(i):
    if i == len(s):
        return ""
    rest = rem(i + 1)                           # trust the call on s[i+1:]
    return rest if s[i] == c else s[i] + rest   # keep or drop THIS character
```

Correct. But `s[i] + rest` creates a **new string** in every frame, copying `rest`
each time: 1 + 2 + ... + n = **O(n²)**.

**Version 2: carry an output list down.** Pass one list to every frame; each frame
appends its character (or doesn't) and moves on. Nothing is copied until a single
`"".join` at the end: **O(n)**.

**Key insight:** in version 2 the list isn't returned, it's **shared**. Every frame
writes into the same object. That is exactly the `path` list in the backtracking
template on the pattern card. The only thing EP116 adds is `path.pop()` after the call,
because there, unlike here, you'll want to try a *different* choice next.

## 🔍 Dry run: `s = "aba"`, `c = "a"`, version 1 (build on the way up)

| step | stack (top on the right) | i | event | returns |
|---|---|---|---|---|
| 1 | R(0) | 0 | call R(1) | |
| 2 | R(0) R(1) | 1 | call R(2) | |
| 3 | R(0) R(1) R(2) | 2 | call R(3) | |
| 4 | R(0) R(1) R(2) R(3) | 3 | `i == n`, base case | `""` |
| 5 | R(0) R(1) R(2) | | `s[2] = a`, **drop** | `""` |
| 6 | R(0) R(1) | | `s[1] = b`, keep: `"b" + ""` | `"b"` |
| 7 | R(0) | | `s[0] = a`, **drop** | **`"b"`** |

All the decisions happen in steps 5 to 7, bottom to top.

## 🔍 Dry run: same input, version 2 (carry a list down)

| step | stack | i | s[i] | out after |
|---|---|---|---|---|
| 1 | R(0) | 0 | a, drop | `[]` |
| 2 | R(0) R(1) | 1 | b, keep | `['b']` |
| 3 | R(0) R(1) R(2) | 2 | a, drop | `['b']` |
| 4 | R(0) R(1) R(2) R(3) | 3 | base case, return | `['b']` |

`"".join(['b'])` → **`"b"`** ✓. Here the decisions happen on the way **down**, and the
way up does nothing.

## ✅ Optimal solution
```python
def remove_char(s: str, c: str) -> str:
    """s with every occurrence of c removed, order kept. Recursive, one char per call.

    Time:  O(n), one call per character, O(1) amortised append, one join at the end.
    Space: O(n), the output list plus a call stack n frames deep.
    """
    out: list[str] = []            # shared by every frame: this is tomorrow's `path`

    def walk(i: int) -> None:
        if i == len(s):            # nothing left to look at
            return
        if s[i] != c:
            out.append(s[i])       # keep it
        walk(i + 1)                # trust the call on the rest

    walk(0)
    return "".join(out)
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **`s[i] + rest` is O(n²).** Python strings are immutable; every concatenation copies.
  It passes on small inputs, so name it rather than waiting to be asked.
- **`s[1:]` is O(n²) too.** Same lesson as EP112 and EP113: recurse on an index.
- **Base case `i == len(s)`**, one past the last index, because every character
  including the last one needs its keep-or-drop decision.
- **The shared list outlives the call.** `out` is created once, outside `walk`. Creating
  it inside `walk` gives every frame its own empty list and the answer is always `""`.
- **Recursion depth is n.** A string over about 1000 characters raises
  `RecursionError` in Python. `s.replace` has no such problem, and saying so shows you
  know this is a teaching shape.

## 🎤 Interview talking points
- *"Each frame decides keep-or-drop for one character and trusts the call on the rest."*
- *"Building the answer with `s[i] + rest` copies the string in every frame, O(n²). I
  pass a list down instead and join once at the end, O(n)."* ← the line to say.
- *"The list is shared by every frame, which is the same idea as the path in
  backtracking."*
- *"In real code this is `s.replace(c, '')`."*

## 🔗 Transfer
This closes the plain-recursion warm-up. You now have: base cases (EP111), shrinking
from both ends (EP112), a one-way index (EP113), the leap of faith (EP114), and a
shared output list (EP115). **EP116, Generate Parentheses**, is where the forks appear:
at every step there are **two** choices, `(` or `)`, so the shared list needs a
`path.pop()` after each call to undo the choice before trying the other one. Choose,
explore, unchoose. Everything from here to EP120 is that template.

## 📹 Metadata
- **Title:** `Remove a character, and meet the path list | Recursion #5`
- **Thumbnail:** `s[i] + rest = O(n²)` (red) vs `out.append` (green)
- **Short:** the letter tiles, decisions happening on the way back up, "banana" to
  "bnn". 45s.
