# EP065 · P08E08 · Simplify Path (Problem Challenge)   [Medium]

**Pattern:** Stack · **Link:** https://leetcode.com/problems/simplify-path/

---

## 🎬 Hook
> "Turn `/a/./b/../../c/` into `/c`. Everyone reaches for the stack immediately and gets
> it right — and then loses ten minutes to `//`, to a trailing slash, to `..` at the
> root, and to a directory that is *literally named* `...`. The stack is four lines. The
> episode is about **tokenising first** so those four lines are all you need."

## 📋 Problem, in your words
```
Given an ABSOLUTE Unix-style path, return its simplified canonical form.

Rules:
  .    means "here"          -> ignore it
  ..   means "up one level"  -> remove the previous directory
  //   repeated slashes are the same as one
  the canonical path starts with / and has NO trailing slash
  (except the root itself, which is just "/")

".." at the root stays at the root -- you cannot go above /.
Any other name, including "..." or "....", is an ordinary directory.
```

## 🔢 The example
```
Input:  "/home/"            Output: "/home"        <- trailing slash dropped
Input:  "/../"              Output: "/"            <- can't go above the root
Input:  "/home//foo/"       Output: "/home/foo"    <- // collapses
Input:  "/a/./b/../../c/"   Output: "/c"
Why:    a -> push. "." -> ignore. b -> push. ".." -> pop b. ".." -> pop a. c -> push.
Input:  "/..."              Output: "/..."         <- three dots is a DIRECTORY NAME
```
That last one catches anyone who wrote `if part.startswith("..")`.

## 🧸 ELI5
> A path is a stack of directories, and you're replaying the journey:
>
> ```
> "/a/./b/../../c/"     split on "/"  ->  ["", "a", ".", "b", "..", "..", "c", ""]
>
>  ""  -> noise (from the leading slash)      stack: []
>  a   -> walk into a                         stack: [a]
>  "." -> stay where you are                  stack: [a]
>  b   -> walk into b                         stack: [a, b]
>  ".."-> go up                               stack: [a]
>  ".."-> go up                               stack: []
>  c   -> walk into c                         stack: [c]
>  ""  -> noise (from the trailing slash)     stack: [c]
> ```
>
> Then print it: `"/" + "/".join(stack)` → `/c`.
>
> The empty strings come from splitting on every slash — the leading one, the trailing
> one, and each extra one in `//`. They're all noise, all handled by the same line, and
> once you see that, every "edge case" in this problem is already covered.

## 🐌 Brute force (say it, don't type it)
Repeatedly find a `x/..` and delete it with string surgery, plus a separate cleanup pass
for `.` and `//`. **O(n²)** and horrible to get right — the ordering of the passes
matters and it's easy to build a version that's wrong on `/a/../../b`. It's a good
30-second argument for tokenising instead.

## 💡 The pattern reveal
**Signal:** a path / an undo history · "go up one" · canonical form.
**Therefore:** split into tokens, push names, `..` pops.

**Key insight — do the parsing before the algorithm.** `path.split("/")` converts every
slash problem into an empty-string token, and then there are exactly four cases:

| token | meaning | action |
|---|---|---|
| `""` | a slash artefact — leading, trailing, or doubled | **skip** |
| `"."` | current directory | **skip** |
| `".."` | parent directory | `stack.pop()` **if the stack is non-empty** |
| anything else | a directory name — including `"..."` | `stack.append(token)` |

Four cases, four lines, no regexes and no index arithmetic:

```python
for part in path.split("/"):
    if part == "" or part == ".":
        continue
    if part == "..":
        if stack:
            stack.pop()
    else:
        stack.append(part)
```

**🧨 The three traps, and each one's line.**

1. **`..` at the root.** `if stack:` before popping. `"/../"` must give `"/"`, not a
   crash. You cannot go above the root, and the guard *is* that rule.
2. **`"..."` is a name.** Compare with `==`, never `startswith("..")`. Unix will happily
   let you create a directory called `...`.
3. **The output format.** `"/" + "/".join(stack)` handles both the root (empty stack →
   `"/"`) and the no-trailing-slash rule, in one expression. Building the string with a
   loop and appending slashes is how the trailing-slash bug gets in.

Also worth noticing: the input is guaranteed **absolute** (it starts with `/`), so
there's no relative-path case to handle. Read the constraints and say so.

## 🔍 Dry run — `"/a/./b/../../c/"`
`split("/")` → `["", "a", ".", "b", "..", "..", "c", ""]`

| token | case | action | stack |
|---|---|---|---|
| `""` | slash artefact | skip | `[]` |
| `"a"` | name | push | `[a]` |
| `"."` | here | skip | `[a]` |
| `"b"` | name | push | `[a, b]` |
| `".."` | up | pop | `[a]` |
| `".."` | up | pop | `[]` |
| `"c"` | name | push | `[c]` |
| `""` | trailing slash | skip | `[c]` |

Output `"/" + "c"` → **`"/c"`** ✓

## 🔍 Dry run — `"/../"` (the root guard)
`split("/")` → `["", "..", ""]`

| token | action | stack |
|---|---|---|
| `""` | skip | `[]` |
| `".."` | stack is **empty** → do nothing | `[]` |
| `""` | skip | `[]` |

Output `"/" + "/".join([])` = `"/" + ""` → **`"/"`** ✓ — the root, produced by the
join of an empty list rather than by a special case.

## ✅ Optimal solution
```python
class Solution:
    def simplifyPath(self, path: str) -> str:
        """Canonical form of an absolute Unix path.

        Time:  O(n) — one split, one pass over the tokens.
        Space: O(n) — the tokens and the stack.
        """
        stack = []

        for part in path.split("/"):
            if part == "" or part == ".":
                continue                  # slash artefacts and "stay here"
            if part == "..":
                if stack:                 # can't go above the root
                    stack.pop()
            else:
                stack.append(part)        # a real directory name, "..." included

        return "/" + "/".join(stack)      # empty stack -> "/" -- the root, for free
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **`if stack:` before popping on `..`.** `"/../"` and `"/a/../../"` both bottom out at
  the root rather than erroring.
- **`part == ".."`, not `startswith("..")`.** `"/..."` is a directory named `...`.
- **`"/" + "/".join(stack)` for the output.** It gives `"/"` for an empty stack and
  never leaves a trailing slash. Don't hand-roll it.
- **`split("/")` produces empty strings** for the leading slash, the trailing slash and
  every doubled slash — one `continue` covers all three.
- **Don't strip or pre-clean the input.** Tokenising makes every whitespace-free
  cleanup unnecessary; extra preprocessing is where bugs move in.
- **The path is absolute** by constraint, so there's no `.` -relative start to handle.
  Check the constraints and say it out loud.

## 🎤 Interview talking points
- *"I split on `/` first, which turns every slash oddity — leading, trailing, doubled —
  into an empty token I skip. After that there are only four cases."* ← the framing that
  makes this easy.
- *"`..` pops, but only if the stack is non-empty: you can't go above the root."*
- *"`...` is a legal directory name, so I compare tokens exactly rather than by
  prefix."* ← the detail that shows you've thought about real filesystems.
- *"`'/' + '/'.join(stack)` gives the root and the no-trailing-slash rule for free."*
- *"O(n) time and space; the space is the token list."*

## 🔗 Transfer
This is the cancelling stack at its most literal — `..` annihilates the entry below it,
exactly as `)` annihilated `(` in EP59. Tomorrow (EP66) closes Pattern 08 by putting the
two halves together: a **monotonic** stack whose pops are limited by a budget, where the
greedy decision, the leftover budget, and the output formatting each need their own
line.

## 📹 Metadata
- **Title:** `Simplify Path — tokenise first, then the stack is four lines | Stack #8`
- **Thumbnail:** `SPLIT ON /` (green block)
- **Short:** `"/..."` — the directory called dot-dot-dot that breaks `startswith`. 40s.
