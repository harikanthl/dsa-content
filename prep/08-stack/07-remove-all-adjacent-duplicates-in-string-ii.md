# EP064 · P08E07 · Remove All Adjacent Duplicates in String II   [Medium]

**Pattern:** Stack · **Link:** https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/

---

## 🎬 Hook
> "EP58 removed adjacent *pairs*. Now remove every run of exactly **k** identical
> letters, repeatedly. The naive upgrade — push each character and check the last k
> entries — is O(nk) and fiddly at the boundaries. The fix is to stop storing characters
> and start storing **`[character, count]`**: one stack entry per run, and the check
> becomes a single integer comparison."

## 📋 Problem, in your words
```
Given a string s and an integer k, repeatedly remove k ADJACENT and
EQUAL letters, until no such run remains. Return the final string.

Removing a run can bring new letters together, which may then form
another run of k -- that cascade must be handled too.
```

## 🔢 The example
```
Input:  s = "abcd", k = 2
Output: "abcd"           <- nothing to do

Input:  s = "deeedbbcccbdaa", k = 3
Output: "aa"
Why:    "deeedbbcccbdaa"
         -> eee goes  -> "ddbbcccbdaa"
         -> ccc goes  -> "ddbbbdaa"       <- bbb only exists because ccc left
         -> bbb goes  -> "dddaa"
         -> ddd goes  -> "aa"
        FOUR cascading removals, three of which the original string doesn't show.

Input:  s = "pbbcggttciiippooaais", k = 2
Output: "ps"
```

## 🧸 ELI5
> Don't stack letters. Stack **runs**: a letter and how many of it you're holding.
>
> ```
> "deeedbbcccbdaa", k = 3
>
>  d  -> new run          stack: [d×1]
>  e  -> new run          stack: [d×1, e×1]
>  e  -> same as top      stack: [d×1, e×2]
>  e  -> same as top -> count hits 3 -> POP the whole run   stack: [d×1]
>  d  -> top is d!        stack: [d×2]        <- it merged with the d from the start
>  ...
> ```
>
> Look at that fifth step. The incoming `d` is the *fifth* character of the string, and
> the `d` it merges with is the *first* — they became neighbours only because the `eee`
> between them vanished. The stack knows, because the top of the stack is always *"the
> run immediately to my left in the answer so far"*.
>
> When a count reaches `k`, the whole entry disappears, and the next character is
> compared against whatever was underneath. The cascade handles itself.

## 🐌 Brute force (say it, don't type it)
Search the string for k identical adjacent characters, delete them, **start over**,
repeat. **O(n²/k)** at best and genuinely slow, but it is what the statement describes.
Also mention the halfway house — a stack of single characters, counting back k entries
each time — and reject it: O(nk), and the boundary handling is worse than the real
solution's.

## 💡 The pattern reveal
**Signal:** "remove k adjacent equal" · removals cascade.
**Therefore:** a cancelling stack of **`[char, count]`** pairs.

**Key insight — compress the state.** A stack of characters stores `d d d` as three
entries and forces you to look backwards to count them. A stack of runs stores it as one
entry `['d', 3]`, and "is this run complete?" becomes a single `== k`:

```python
if stack and stack[-1][0] == ch:
    stack[-1][1] += 1                 # extend the run in place
    if stack[-1][1] == k:
        stack.pop()                   # complete: the whole run vanishes
else:
    stack.append([ch, 1])             # a different letter starts a new run
```

**Why `== k` and never `>= k`:** the count is incremented one at a time and checked
immediately, so it can never overshoot. `>=` works but it advertises that you weren't
sure — and if you ever *do* see a count above `k`, something else is wrong.

**Why a list `[ch, cnt]` and not a tuple:** you mutate the count in place. With tuples
you'd pop and re-push, which works fine but is noisier. Say which you picked and why.

**🧨 The trap: rebuild with `ch * cnt`.** The stack holds runs, so the answer isn't
`"".join(stack)` — each entry expands back into `cnt` copies:

```python
return "".join(ch * cnt for ch, cnt in stack)
```
Forget the multiplication and `"ddaa"` comes back as `"da"`.

## 🔍 Dry run — `s = "deeedbbcccbdaa"`, `k = 3`

| ch | top | action | stack after |
|---|---|---|---|
| `d` | — | new run | `d×1` |
| `e` | `d` | new run | `d×1, e×1` |
| `e` | `e` | count → 2 | `d×1, e×2` |
| `e` | `e` | count → 3 **== k → pop** | `d×1` |
| `d` | `d` | count → 2 | `d×2` |
| `b` | `d` | new run | `d×2, b×1` |
| `b` | `b` | count → 2 | `d×2, b×2` |
| `c` | `b` | new run | `d×2, b×2, c×1` |
| `c` | `c` | count → 2 | `d×2, b×2, c×2` |
| `c` | `c` | count → 3 **== k → pop** | `d×2, b×2` |
| `b` | `b` | count → 3 **== k → pop** | `d×2` |
| `d` | `d` | count → 3 **== k → pop** | *(empty)* |
| `a` | — | new run | `a×1` |
| `a` | `a` | count → 2 | `a×2` |

Rebuild: `a×2` → **`"aa"`** ✓

Rows 10–12 are the cascade, and they're the reason this is Medium: three consecutive
pops, each one exposing a run that was only completed because the run above it left.
Nothing in the code looks backwards to make that happen.

## ✅ Optimal solution
```python
class Solution:
    def removeDuplicates(self, s: str, k: int) -> str:
        """Repeatedly remove runs of exactly k identical adjacent characters.

        Time:  O(n) — each character is pushed once and popped at most once.
        Space: O(n) — the stack of runs.
        """
        stack = []                       # [character, count] -- one entry per RUN

        for ch in s:
            if stack and stack[-1][0] == ch:
                stack[-1][1] += 1        # extend the run on top
                if stack[-1][1] == k:
                    stack.pop()          # the run is complete: it vanishes
            else:
                stack.append([ch, 1])    # a new run begins

        return "".join(ch * cnt for ch, cnt in stack)
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **Expand the counts when rebuilding.** `ch * cnt`, not `ch`. The most common wrong
  answer on this problem is the right letters with the wrong multiplicities.
- **Check `== k` immediately after incrementing**, inside the same branch. Checking at
  the top of the next iteration leaves a complete run on the stack for one step, which
  breaks the "top is the run to my left" invariant.
- **`stack[-1][0] == ch` compares the character**, `stack[-1][1]` is the count. Indexing
  the wrong slot compiles fine and compares a letter to an int.
- **`k = 1` is outside the constraints (`2 <= k`), and this code does not handle it.**
  The `== k` check lives only in the "extend an existing run" branch, so a freshly
  pushed run of count 1 is never tested and nothing is ever removed — `removeDuplicates("abbaca", 1)`
  returns `"abbaca"`, not `""`. I checked rather than assumed. If you wanted k=1 to
  work you'd have to test the count in the append branch too; since the constraints
  exclude it, the simpler code is the right code — but know *why* it's safe.
- **Mutating `stack[-1][1]` requires a list**, not a tuple. Tuples are immutable and
  you'd need pop-and-repush.
- **This is EP58 when `k = 2`.** Run it to confirm — if it disagrees, the bug is in the
  count handling.

## 🎤 Interview talking points
- *"I stack runs, not characters: `[char, count]`. Then 'is this run complete?' is one
  integer comparison rather than looking back k entries."* ← the insight being tested.
- *"The top of the stack is the run immediately to my left in the answer, so when a run
  pops, the next character is naturally compared against what was underneath — the
  cascade is free."*
- *"O(n): each character joins a run once and is removed at most once. The
  stack-of-characters version is O(nk)."*
- *"With `k = 2` this is exactly the simpler version of the problem."*

## 🔗 Transfer
That's the cancelling stack at full strength — entries carrying state rather than bare
characters. Tomorrow (EP65) keeps that idea and changes the alphabet: the stack holds
**path segments**, `..` cancels the entry below it, and the real work moves to
tokenising the input before the stack ever sees it.

## 📹 Metadata
- **Title:** `Remove Adjacent Duplicates II — stack the runs, not the letters | Stack #7`
- **Thumbnail:** `[CHAR, COUNT]` (green block)
- **Short:** the three-pop cascade in `"deeedbbcccbdaa"`. 45s.
