# EP060 · P08E03 · Reverse a String   [Easy]

**Pattern:** Stack · **Link:** https://leetcode.com/problems/reverse-string/

---

## 🎬 Hook
> "A stack reverses things by construction — push everything, pop everything, done. It's
> the textbook demonstration of LIFO and it's the **wrong answer to this problem**. This
> episode is three minutes long on purpose: knowing a tool is not the same as knowing
> when to put it down."

## 📋 Problem, in your words
```
Reverse an array of characters IN PLACE.

Do it with O(1) extra memory -- the array itself is the output, and
you may not allocate a second one.
```

## 🔢 The example
```
Input:  ['h','e','l','l','o']     Output: ['o','l','l','e','h']
Input:  ['H','a','n','n','a','h'] Output: ['h','a','n','n','a','H']
Input:  ['a']                     Output: ['a']
Input:  []                        Output: []
```

## 🧸 ELI5
> **The stack version**, which is what this pattern would have you write:
>
> ```
> push h, e, l, l, o     pile: h e l l o
>                                     ^ top
> pop into position 0: o
> pop into position 1: l
> pop into position 2: l
> pop into position 3: e
> pop into position 4: h
> ```
>
> It works. It is also a **second copy of the entire string** — O(n) extra memory to
> perform an operation that needs none.
>
> **The two-pointer version**, which is what the problem is actually asking for:
>
> ```
>  h  e  l  l  o
>  ^           ^      swap  ->  o e l l h
>     ^     ^         swap  ->  o l l e h
>        ^^           pointers meet, stop
> ```
>
> Two indices walking towards each other, swapping as they go. No pile, no copy, and it
> touches each element exactly once.

## 🐌 Brute force (say it, don't type it)
`chars[:] = chars[::-1]` — one line, correct, and it allocates a reversed copy before
assigning it back, so it is O(n) space in the same way the stack is. Say it, say why it
doesn't satisfy the constraint, and then write the real one.

## 💡 The pattern reveal
**Signal:** "reverse" · **in place** · O(1) extra space stated explicitly.
**Therefore:** two pointers from the ends. **Not** a stack.

**Key insight — what a stack actually costs.** A stack buys you *memory of an arbitrary
number of unresolved items*. That is exactly what EP58, EP59 and EP64 need, and exactly
what this problem doesn't: reversal has no "unresolved" state at all. Every element's
destination is known from the start — position `i` goes to position `n − 1 − i`.

**When a stack is right and when it isn't:**

| the problem needs | tool |
|---|---|
| "the most recent thing that hasn't been settled" | **stack** (EP58, 59, 64, 65) |
| "the first element to my right that beats me" | **monotonic stack** (EP61, 62, 63, 66) |
| a destination you can compute directly | **two pointers** (this episode) |

**The interview point, and the reason this episode exists:** being handed the "obvious"
data structure and declining it, with a reason, reads far stronger than using it. The
stack version is worth writing on camera *first* — it's a clean LIFO demonstration —
and then deleting.

## 🔍 Dry run — `['h','e','l','l','o']` (two pointers)

| `lo` | `hi` | swap | array after |
|---|---|---|---|
| 0 | 4 | `h` ↔ `o` | `o e l l h` |
| 1 | 3 | `e` ↔ `l` | `o l l e h` |
| 2 | 2 | `lo < hi` is false → **stop** | `o l l e h` |

Answer **`['o','l','l','e','h']`** ✓ — the middle element of an odd-length array never
moves, and needs no special case.

## 🔍 Dry run — `['a','b','c','d']` (even length)

| `lo` | `hi` | swap | array after |
|---|---|---|---|
| 0 | 3 | `a` ↔ `d` | `d b c a` |
| 1 | 2 | `b` ↔ `c` | `d c b a` |
| 2 | 1 | `lo < hi` false → stop | `d c b a` |

Answer **`['d','c','b','a']`** ✓ — the pointers **cross** rather than meet, which is why
the condition is `lo < hi` and not `lo != hi`.

## ✅ Optimal solution — two pointers, O(1) space
```python
class Solution:
    def reverseString(self, s: List[str]) -> None:
        """Reverse the character array in place.

        Time:  O(n) — n/2 swaps.
        Space: O(1) — two indices. Nothing is allocated.
        """
        lo, hi = 0, len(s) - 1

        while lo < hi:                      # `<`, so they may cross without swapping
            s[lo], s[hi] = s[hi], s[lo]
            lo += 1
            hi -= 1
```

## ✅ The stack version — correct, and O(n) space
```python
class Solution:
    def reverseStringWithStack(self, s: List[str]) -> None:
        """The LIFO demonstration. Correct, but allocates a full copy.

        Time:  O(n) · Space: O(n) -- which is why it is not the answer here.
        """
        stack = list(s)                     # push everything

        for i in range(len(s)):
            s[i] = stack.pop()              # pop everything: LIFO reverses by itself
```
**Time:** O(n) both · **Space:** O(1) vs O(n)

## ⚠️ Gotchas
- **`while lo < hi`, not `<=` or `!=`.** With `<=`, the middle element of an odd-length
  array is swapped with itself — harmless but sloppy. With `!=`, an even-length array
  never satisfies it and the loop runs off the ends.
- **Modify in place.** The function returns `None`; assigning `s = s[::-1]` rebinds a
  local name and changes nothing for the caller. If you must use a slice, it's
  `s[:] = s[::-1]` — and that's still O(n) space.
- **Python's tuple swap is one line**; in C-like languages you need a temporary, and
  saying so shows you know what the line compiles to.
- **Empty and single-element arrays** never enter the loop. No guards.
- **Don't reach for `reversed()` or `list.reverse()`** unless asked — the point is the
  index arithmetic. (`list.reverse()` *is* in-place and O(1) space, though, so name it
  as the library answer.)

## 🎤 Interview talking points
- *"A stack reverses by construction, but it costs O(n) memory to do something that
  needs none — so I'd use two pointers here."* ← the whole episode in one sentence.
- *"Reversal has no unresolved state. Every element's destination is known up front,
  which is the tell that a stack is unnecessary."*
- *"`lo < hi`, so they cross on even lengths and the middle element of an odd length is
  left alone."*
- *"In place means mutating the caller's list — `s[:] = …` rather than `s = …`."*

## 🔗 Transfer
That's the cancelling half of the pattern closed, with one deliberate counter-example.
Tomorrow (EP61) opens the **monotonic** half, where the stack stops being the answer and
becomes scaffolding: you push elements that are still waiting for something bigger, and
the moment one arrives, the pop *is* the answer being written down.

## 📹 Metadata
- **Title:** `Reverse a String — when NOT to use a stack | Stack #3`
- **Thumbnail:** `PUT THE TOOL DOWN` (red block)
- **Short:** the stack version, then the two-pointer version, and the memory difference. 35s.
