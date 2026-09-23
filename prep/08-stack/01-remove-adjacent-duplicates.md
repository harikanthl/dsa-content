# EP058 · P08E01 · Remove All Adjacent Duplicates in String   [Easy]

**Pattern:** Stack · **Link:** https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/

---

## 🎬 Hook
> "Delete adjacent pairs of equal letters, over and over, until none are left. The catch
> is that deleting a pair creates *new* neighbours that might now match, so a naive
> scan has to start over every time. A stack never starts over: the letter you're
> holding is always compared with the one that will actually end up next to it."

## 📋 Problem, in your words
```
Given a string s of lowercase letters, repeatedly remove two ADJACENT
and EQUAL letters, until no such pair remains. Return the final string.

The answer is unique -- it does not matter which pair you remove first.
```

## 🔢 The example
```
Input:  "abbaca"
Output: "ca"
Why:    "abbaca" -> remove "bb" -> "aaca" -> remove "aa" -> "ca"
                                    ^^ these two only became neighbours
                                       AFTER the bb was deleted

Input:  "azxxzy"
Output: "ay"     <- xx goes, then zz becomes adjacent and goes too

Input:  "aa"     -> ""      <- the answer can be empty
Input:  "abc"    -> "abc"   <- nothing to do
```

## 🧸 ELI5
> Walk the string building a new one, letter by letter, in a pile:
>
> ```
> "abbaca"
>
>  a  ->  pile: a
>  b  ->  top is a, different  -> pile: a b
>  b  ->  top is b, SAME       -> pop!  pile: a
>  a  ->  top is a, SAME       -> pop!  pile: (empty)
>  c  ->  pile: c
>  a  ->  pile: c a
> ```
>
> Look at what happened at the fourth letter. The `a` on the pile was the *first* letter
> of the string, and the incoming `a` was the fourth, they were never neighbours in the
> original text. They became neighbours because everything between them cancelled out,
> and **the pile knows that automatically**. That's the whole trick: the top of the pile
> is always the letter that will genuinely sit next to whatever comes in.

## 🐌 Brute force (say it, don't type it)
Scan for an adjacent equal pair, delete it, **start the scan again**, repeat until a
full pass finds nothing. **O(n²)**: each deletion rescans, and it's the honest
description of what the problem statement literally asks for. The stack does the same
thing without ever going backwards.

## 💡 The pattern reveal
**Signal:** "remove adjacent …" · deletions create new adjacencies · the process repeats.
**Therefore:** a **cancelling stack**. One pass, O(n).

**Key insight:** the top of the stack is *"the letter immediately to my left in the
answer so far."* Not in the input, in the **answer**. Those are different the moment a
deletion happens, and tracking the answer's left neighbour rather than the input's is
exactly what makes one pass sufficient.

```python
if stack and stack[-1] == ch:
    stack.pop()        # they annihilate
else:
    stack.append(ch)   # unresolved: it survives, for now
```

**And the stack *is* the answer.** No second pass, no reconstruction, `"".join(stack)`
is the output, in order, because a stack in Python is a list and the list is already in
left-to-right order. Say that out loud; it's the difference between this family and the
monotonic stacks coming in EP61.

## 🔍 Dry run: `"abbaca"`

| ch | top of stack | same? | action | stack after |
|---|---|---|---|---|
| `a` | - | - | push | `a` |
| `b` | `a` | ✗ | push | `a b` |
| `b` | `b` | **✓** | **pop** | `a` |
| `a` | `a` | **✓** | **pop** | *(empty)* |
| `c` | - | - | push | `c` |
| `a` | `c` | ✗ | push | `c a` |

Answer **`"ca"`** ✓

Row 4 is the one to narrate: the `a` being cancelled is the string's *first* character,
cancelled by its *fourth*. No rescan, no backtracking, the stack had already forgotten
everything that cancelled in between.

## 🔍 Dry run: `"azxxzy"`

| ch | stack before | action | stack after |
|---|---|---|---|
| `a` | - | push | `a` |
| `z` | `a` | push | `a z` |
| `x` | `a z` | push | `a z x` |
| `x` | `a z x` | **pop** (matches `x`) | `a z` |
| `z` | `a z` | **pop** (matches `z`) | `a` |
| `y` | `a` | push | `a y` |

Answer **`"ay"`** ✓, a two-level cascade, resolved without a single backwards step.

## ✅ Optimal solution
```python
class Solution:
    def removeDuplicates(self, s: str) -> str:
        """Repeatedly remove adjacent equal pairs; return what's left.

        Time:  O(n), each character is pushed once and popped at most once.
        Space: O(n), the stack, which IS the answer.
        """
        stack = []

        for ch in s:
            if stack and stack[-1] == ch:
                stack.pop()            # the pair annihilates
            else:
                stack.append(ch)       # no match: it stays, for now

        return "".join(stack)
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **`if stack and …`, check emptiness first.** `stack[-1]` on an empty list raises
  `IndexError`, and the first character always meets an empty stack.
- **Pop, don't push, on a match.** Writing `stack.append(ch)` in both branches is a
  typo that produces the input unchanged, and reads as correct at a glance.
- **`"".join(stack)`, not `str(stack)`.** The latter gives you `['c', 'a']`.
- **The answer can be empty**: `"aa"` → `""`. Don't add a guard that returns the input
  when the stack is empty.
- **Only pairs cancel here**, not runs of three or more. `"aaa"` → `"a"`: the first two
  cancel, the third survives. That generalisation is EP64, and it needs a counter.
- **Don't mutate the string** with repeated slicing, that's the O(n²) version wearing a
  stack's clothes.

## 🎤 Interview talking points
- *"The top of the stack is the character to my left **in the answer**, which is what
  makes deletions cascade for free."* ← the sentence that explains why one pass works.
- *"Each character is pushed once and popped at most once, so it's O(n), the repeated
  rescanning in the naive version is what the stack removes."*
- *"The stack is the output, in order, so there's nothing to reconstruct at the end."*
- *"If runs of k had to cancel instead of pairs, I'd keep counts on the stack rather
  than individual characters."* ← name the generalisation before they ask; it's EP64.

## 🔗 Transfer
This is the smallest cancelling stack there is, and the family runs through the whole
pattern: EP59 cancels brackets against their partners, EP64 cancels runs of `k` by
carrying a count, EP65 cancels `..` against the directory above it. Tomorrow (EP59) adds
the twist that the two cancelling items aren't equal, they have to *match*, which means
the pop needs to check what it popped.

## 📹 Metadata
- **Title:** `Remove Adjacent Duplicates, the stack IS the answer | Stack #1`
- **Thumbnail:** `TOP = LEFT NEIGHBOUR` (green block)
- **Short:** `"abbaca"` cascading in six steps on the pile. 35s.
