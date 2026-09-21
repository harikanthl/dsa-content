# EP059 · P08E02 · Balanced Parentheses   [Easy]

**Pattern:** Stack · **Link:** https://leetcode.com/problems/valid-parentheses/

---

## 🎬 Hook
> "Three kinds of bracket, and a string is valid only if every one of them closes in the
> right order. It's the canonical stack problem, and the interesting part isn't the
> algorithm — it's that there are **three different ways to be invalid**, and a solution
> that only checks two of them passes most test cases."

## 📋 Problem, in your words
```
Given a string containing only '(', ')', '{', '}', '[' and ']',
determine whether it is valid:

  1. every open bracket is closed by the SAME type, and
  2. brackets close in the correct ORDER (innermost first).

An empty string is valid.
```

## 🔢 The example
```
Input:  "()[]{}"   -> True
Input:  "{[]}"     -> True     <- properly nested
Input:  "(]"       -> False    <- wrong TYPE
Input:  "([)]"     -> False    <- right types, wrong ORDER
Input:  "]"        -> False    <- closes something that was never opened
Input:  "("        -> False    <- opened and never closed
```
Those last four are the three failure modes, and every one of them needs its own line of
code. Write them on the whiteboard before writing the solution.

## 🧸 ELI5
> Every time you open a bracket, put it on a pile. Every time you close one, the pile's
> **top** must be its partner — because the most recently opened bracket is the only one
> you're allowed to close right now.
>
> ```
> "{ [ ] }"
>
>  {  -> pile: {
>  [  -> pile: { [
>  ]  -> top is [ , partner of ] ✓  -> pop  -> pile: {
>  }  -> top is { , partner of } ✓  -> pop  -> pile: (empty)
>
>  empty pile at the end -> valid ✓
> ```
>
> And the counter-example that shows why *order* matters:
>
> ```
> "( [ ) ]"
>
>  (  -> pile: (
>  [  -> pile: ( [
>  )  -> top is [ , NOT my partner ✗  -> invalid
> ```
>
> The `)` wants to close the `(`, but the `[` is in the way — unfinished business, more
> recent. A stack catches that without knowing anything about nesting rules.

## 🐌 Brute force (say it, don't type it)
Repeatedly delete `"()"`, `"[]"` and `"{}"` from the string until nothing changes; valid
iff the result is empty. **O(n²)**, cute, and a legitimate one-liner in Python
(`while` + three `.replace()`s) — worth saying because it is *provably* the same
cancelling process the stack performs in one pass.

## 💡 The pattern reveal
**Signal:** brackets · nesting · "valid" / "balanced".
**Therefore:** a cancelling stack, where the pop must be **verified**.

**Key insight:** the stack's top is the innermost unclosed bracket, which is the only
one a closing bracket may legally match. EP58's pop was unconditional — the characters
were equal by definition. Here you must *check what you popped*:

```python
partner = {')': '(', ']': '[', '}': '{'}     # closer -> its opener

if ch in partner:                            # a closing bracket
    if not stack or stack.pop() != partner[ch]:
        return False
else:
    stack.append(ch)
```

**The three ways to be invalid, each mapped to its line of code:**

| failure | example | the line that catches it |
|---|---|---|
| wrong **type** | `"(]"` | `stack.pop() != partner[ch]` |
| wrong **order** | `"([)]"` | the same line — the top is `[`, not `(` |
| closing something **never opened** | `"]"` | `not stack` |
| opening something **never closed** | `"("` | `return not stack` at the **end** |

That last row is the one people drop. The loop can finish without ever returning
`False` and the string still be invalid, because the pile is not empty. `return True`
instead of `return not stack` is the classic wrong submission.

## 🔍 Dry run — `"{[]}"` (valid)

| ch | kind | stack before | check | stack after |
|---|---|---|---|---|
| `{` | open | — | — | `{` |
| `[` | open | `{` | — | `{ [` |
| `]` | close | `{ [` | pop → `[` = partner ✓ | `{` |
| `}` | close | `{` | pop → `{` = partner ✓ | *(empty)* |

Stack is empty → **True** ✓

## 🔍 Dry run — `"([)]"` (invalid, right types wrong order)

| ch | kind | stack before | check | result |
|---|---|---|---|---|
| `(` | open | — | — | `(` |
| `[` | open | `(` | — | `( [` |
| `)` | close | `( [` | pop → `[`, partner needed `(` ✗ | **return False** |

Answer **False** ✓ — and note the string has equal counts of every bracket type.
Counting can never solve this problem; only order can.

## ✅ Optimal solution
```python
class Solution:
    def isValid(self, s: str) -> bool:
        """True if the bracket string is correctly typed and correctly nested.

        Time:  O(n) — one pass, O(1) work per character.
        Space: O(n) — worst case "(((((((" pushes everything.
        """
        partner = {')': '(', ']': '[', '}': '{'}     # closer -> required opener
        stack = []

        for ch in s:
            if ch in partner:                         # a closing bracket
                # nothing open, or the wrong thing open
                if not stack or stack.pop() != partner[ch]:
                    return False
            else:                                     # an opening bracket
                stack.append(ch)

        return not stack        # anything still open means invalid
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **`return not stack`, not `return True`.** `"("` is invalid and the loop never fires a
  `False`. This is the single most common miss on this problem.
- **`not stack` before `stack.pop()`.** Short-circuit order matters — `"]"` on an empty
  stack must return `False`, not raise `IndexError`.
- **Map closers to openers, not the reverse.** You look up by the character you're
  *holding*, which is the closer. Building the dict the other way costs you an inverted
  lookup at every step.
- **`ch in partner` is the "is this a closer?" test.** Cleaner than three `or`s and it
  can't drift out of sync with the dict.
- **Don't count brackets.** `"([)]"` has perfectly balanced counts. State it when asked
  why a counter isn't enough.
- **An empty string is valid** — the loop doesn't run and `not []` is `True`. Free
  correctness; check it rather than special-casing it.

## 🎤 Interview talking points
- *"The top of the stack is the innermost unclosed bracket, and that's the only one a
  closer is allowed to match."*
- *"There are three ways to fail: wrong type, wrong order, and an unclosed opener at the
  end — the last one is why I return `not stack` rather than `True`."* ← say this
  unprompted.
- *"Counting doesn't work: `([)]` has balanced counts and is invalid."*
- *"O(n) time, O(n) space in the worst case of all openers."*
- *"If the input could contain other characters, I'd only push the ones in my map rather
  than pushing everything."* ← a real robustness point, and LeetCode's constraints
  exclude it.

## 🔗 Transfer
EP58 cancelled equal characters; this cancels *matching* ones, which is why the pop
needs a check. Tomorrow (EP60) is the deliberate outlier — a problem where a stack
works perfectly and is still the wrong answer — and then EP61 opens the monotonic half
of the pattern, where the pop stops being a cancellation and becomes the moment an
answer is discovered.

## 📹 Metadata
- **Title:** `Valid Parentheses — three ways to be invalid | Stack #2`
- **Thumbnail:** `RETURN NOT STACK` (red block)
- **Short:** `"("` returning True with the wrong final line. 35s.
