# EP105 · P11E12 · Reorganize String   [Medium]

**Pattern:** Heap (greedy + heap) · **Link:** https://leetcode.com/problems/reorganize-string/

---

## 🎬 Hook
> "Rearrange a string so no two neighbours match. Greedy says: always place the most
> common letter. But then you'd place it **twice in a row**. The fix is one variable:
> the letter you just used sits **outside the heap for exactly one turn**. It's Task
> Scheduler with a cooldown of 1, and a cooling rack that holds one thing."

## 📋 Problem, in your words
```
Given a string s, rearrange its characters so that no two adjacent
characters are the same. Return any valid arrangement, or "" if none
exists.
```

## 🔢 The example
```
Input:  "aab"     -> "aba"
Input:  "aaab"    -> ""          <- three a's need two separators; only one b
Input:  "aaabbc"  -> "ababac"    (any valid answer is accepted)
```

## 🧸 ELI5
> Seating kids at a long bench so that no two **from the same school** sit together.
> You always seat a kid from the school with **the most kids still standing**, since
> they're the hardest to fit. But the kid you just seated's school is **not allowed**
> next, so you hold that school's line aside for one turn, seat someone else, then let
> it back in.
>
> ```
> standing:  a a a   b b   c
> seat a     -> a         hold a's line aside
> seat b     -> a b       a's line back; hold b's
> seat a     -> a b a     b back; hold a
> seat b     -> a b a b   ...
> ```
>
> If the only school left standing is **the one you're holding aside**, you're stuck.
> That's the "" case.

## 🐌 Brute force (say it, don't type it)
Try permutations until one has no equal neighbours: **O(n!)**. Useless beyond 10
characters, but it states the problem honestly. The greedy + heap does it in
**O(n log 26)**.

## 💡 The pattern reveal
**Signal:** "rearrange" · "no two adjacent equal" · counts matter.
**Therefore:** count (Pattern 9), then Shape D greedy + heap with a one-turn hold.

**Key insight:** each step, pop the most frequent letter, append it, and **then** push
back the letter you were holding from the *previous* step. The one you just used
becomes the new held letter.

```python
cnt, ch = heapq.heappop(heap)        # most frequent that's ALLOWED right now
out.append(ch)
if held:
    heapq.heappush(heap, held)       # last turn's letter is allowed again
held = (cnt + 1, ch) if cnt + 1 < 0 else None    # this one sits out a turn
```

The order of those lines is the whole problem: pop **before** pushing `held` back, or
the letter you just used could be popped again.

**When is it impossible?** If some letter appears more than `(n + 1) // 2` times.
The loop discovers this on its own: the heap runs empty while `held` still has copies.

## 🔍 Dry run: `"aaabbc"`
Heap: `(-3,'a') (-2,'b') (-1,'c')`, `held = None`.

| step | pop | out | push back held | new held | heap after |
|---|---|---|---|---|---|
| 1 | a (3) | `a` | - | a (2 left) | {b2, c1} |
| 2 | b (2) | `ab` | a2 | b (1 left) | {a2, c1} |
| 3 | a (2) | `aba` | b1 | a (1 left) | {b1, c1} |
| 4 | b (1) | `abab` | a1 | None (b done) | {a1, c1} |
| 5 | a (1) | `ababa` | - | None | {c1} |
| 6 | c (1) | `ababac` | - | None | {} |

Heap empty, `held` is None → **`"ababac"`** ✓.

And `"aaab"`: pop a → `a`, hold a2 · pop b → `ab`, push a2, b done · pop a → `aba`,
hold a1 · heap empty, **`held` still has an a** → return `""` ✓.

## ✅ Optimal solution
```python
class Solution:
    def reorganizeString(self, s: str) -> str:
        """Rearrange s so no two adjacent characters match, or "" if impossible.

        Time:  O(n log 26) = O(n), one pop and at most one push per character.
        Space: O(26) for the heap, O(n) for the output.
        """
        heap = [(-cnt, ch) for ch, cnt in Counter(s).items()]   # MAX-heap on count
        heapq.heapify(heap)

        out = []
        held = None                     # the letter used last turn, sitting out
        while heap:
            cnt, ch = heapq.heappop(heap)
            out.append(ch)
            if held:
                heapq.heappush(heap, held)          # allowed again now
            held = (cnt + 1, ch) if cnt + 1 < 0 else None

        # a letter still waiting with nothing left to separate it -> impossible
        return "".join(out) if held is None else ""
```
**Time:** O(n) · **Space:** O(1) heap + O(n) output

## ⚠️ Gotchas
- **Pop, then push `held`.** Reversed, you can pop the letter you just placed and get
  `"aa..."`.
- **The failure check is `held is not None` at the end**, not `len(out) < len(s)`. They
  agree, but the first one says *why*.
- **`cnt + 1 < 0`** because counts are negated. A finished letter must not be held;
  holding `(0, 'b')` would push a phantom `b` back later.
- **Up-front check is optional.** `max(count) > (len(s) + 1) // 2` → `""` immediately.
  Say it as the O(n) early exit; the loop handles it anyway.
- **Ties.** `(-2,'a')` vs `(-2,'b')` tie-break alphabetically, harmless. Any valid answer
  is accepted.

## 🎤 Interview talking points
- *"Greedy: always place the most frequent letter that isn't the one I just placed. A
  max-heap on count, and the last-used letter held outside for one turn."*
- *"It's Task Scheduler with n = 1, where the output is the arrangement instead of the
  time."*
- *"Impossible exactly when one letter has more than (n + 1) / 2 copies: there aren't
  enough other letters to separate them."*
- *"There's an O(n) no-heap version: place the most frequent letter at even indices,
  then fill the rest in order. Nice to mention; the heap version generalises to 'at
  least k apart'."*

## 🔗 Transfer
EP104 used a queue of cooling tasks; today the queue shrank to one variable because the
cooldown is exactly one. Tomorrow (EP106, Minimum Refueling Stops) is where greedy +
heap gets strange: you drive **past** stations without deciding, and only when the tank
runs dry do you go back in time and pick the best one you passed.

## 📹 Metadata
- **Title:** `Reorganize String, hold the last letter out for one turn | Heap #12`
- **Thumbnail:** `held = ?` (green block)
- **Short:** the school bench, and "aaab" getting stuck with a held a. 45s.
