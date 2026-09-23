# EP011 · P01E11 · Comparing Strings Containing Backspaces   [Medium]

**Pattern:** Two Pointers · **Link:** https://leetcode.com/problems/backspace-string-compare/

---

## 🎬 Hook
> "Everyone solves this with a stack, and the stack is fine, it's O(n) time. But the
> follow-up asks for O(1) space, and the answer is genuinely clever: you read both
> strings **backwards**. Because a backspace only ever affects what's to its left."

## 📋 Problem, in your words
```
Two strings where '#' means backspace (delete the previous character).
Return true if they produce the same final text.

'#' on an empty string does nothing, it doesn't error.
Follow-up: can you do it in O(n) time and O(1) space?
```

## 🔢 The example
```
s = "ab#c"   ->  "ac"     (b gets deleted)
t = "ad#c"   ->  "ac"     (d gets deleted)
Output: true

s = "a##c"   ->  "c"      (# deletes 'a', second # deletes nothing)
t = "#a#c"   ->  "c"
Output: true
```

## 🧸 ELI5
> Reading a string **forwards**, you can never be sure a character survives, a `#`
> might be coming up later that erases it. You're always in suspense.
>
> Reading **backwards**, the suspense is gone. You see the `#` *before* you see the
> character it kills. So you can count: "I've got 2 pending backspaces, so skip the
> next 2 real characters."
>
> It's like reading a list of edits in reverse. You know the deletion before you meet
> the victim.

## 🐌 Brute force (say it, don't type it)
Build both strings with a stack (or a list), then compare:
```python
def build(s):
    out = []
    for ch in s:
        if ch == '#':
            if out: out.pop()
        else:
            out.append(ch)
    return out
return build(s) == build(t)
```
**O(n) time, O(n) space.** This is a perfectly good answer and you should write it on
camera first, it's readable and it passes. Then say: *"the follow-up wants O(1)
space, and that's the real question."*

## 💡 The pattern reveal
**Signal:** compare two sequences + an O(1) space constraint + an operation that
looks **backwards** (`#` deletes what's behind it).
**Therefore:** Two Pointers walking **right to left**, one per string.

**Key insight:** direction is a design choice, not a given. Backspace is a
right-to-left operator, so scanning right-to-left makes it a simple counter instead of
a data structure. Whenever an operation refers to "the previous thing," ask whether
reversing the scan turns state into a count.

## 🔍 Dry run: `s = "ab#c"`, `t = "ad#c"`
| i (s) | j (t) | skipS | skipT | resolved chars | verdict |
|---|---|---|---|---|---|
| 3 | 3 | 0 | 0 | `c` vs `c` | match, step both |
| 2 | 2 | - | - | both are `#` → `skip=1`, step both | - |
| 1 | 1 | 1 | 1 | `b`/`d` consumed by skip → `skip=0`, step both | - |
| 0 | 0 | 0 | 0 | `a` vs `a` | match, step both |
| −1 | −1 | | | both exhausted | **true** |

## ✅ Optimal solution
```python
class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        i, j = len(s) - 1, len(t) - 1
        skip_s = skip_t = 0

        while i >= 0 or j >= 0:                  # OR: one may be longer
            # find the next surviving character in s
            while i >= 0:
                if s[i] == '#':
                    skip_s += 1
                    i -= 1
                elif skip_s > 0:
                    skip_s -= 1
                    i -= 1
                else:
                    break                        # s[i] survives

            # find the next surviving character in t
            while j >= 0:
                if t[j] == '#':
                    skip_t += 1
                    j -= 1
                elif skip_t > 0:
                    skip_t -= 1
                    j -= 1
                else:
                    break

            # compare the two survivors
            if i >= 0 and j >= 0:
                if s[i] != t[j]:
                    return False
            elif i >= 0 or j >= 0:
                return False                     # one ran out, the other didn't

            i -= 1
            j -= 1

        return True
```
**Time:** O(n + m) · **Space:** O(1) ✓

## ⚠️ Gotchas
- **`while i >= 0 or j >= 0`**, not `and`. With `and`, you exit as soon as one string
  is exhausted, so `"a"` vs `"ab"` wrongly returns true.
- **Three states in the inner loop**, in this order: is it a `#` (bank a skip)?
  do I owe a skip (spend it)? otherwise it's a survivor (stop). Reordering these
  breaks it.
- The final `elif i >= 0 or j >= 0: return False` is the length check. Without it,
  a string with leftover characters compares equal. Easy to forget, easy to spot in
  testing, good place to let the test fail on camera and then fix it.
- `'#'` on empty does nothing: naturally handled, since `i` just walks off the end.

## 🎤 Interview talking points
- *"I'd write the stack version first because it's clearer, then optimise to O(1)
  space if asked."* ← This is exactly the right interview instinct, and saying it out
  loud is worth more than jumping straight to the clever one.
- *"Backspace is a backwards-looking operator, so I scan backwards. That converts
  'remember what I've seen' into 'count what I owe', state becomes a counter."*

## 🔗 Transfer
The stack version is a warm-up for **Pattern 7: Stack** (EP 65–73), Remove All
Adjacent Duplicates is literally this. The "scan in the direction the operator
points" idea shows up again in Next Greater Element and Daily Temperatures.

## 📹 Metadata
- **Title:** `Backspace String Compare, O(1) space by reading backwards | Two Pointers #11`
- **Thumbnail:** `READ IT BACKWARDS` (blue block)
- **Short:** "Why backwards?", the suspense analogy, 45s.
