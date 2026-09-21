# EP015 · P02E03 · Happy Number   [Medium]

**Pattern:** Fast & Slow Pointers · **Link:** https://leetcode.com/problems/happy-number/

---

## 🎬 Hook
> "There is no linked list in this problem. There are no pointers, no nodes, no
> `.next`. And it is still a cycle-detection problem — you solve it with the exact
> code from episode 13. Once you see why, you start seeing linked lists everywhere."

## 📋 Problem, in your words
```
Start with a number. Replace it with the sum of the squares of its digits.
Repeat.

If you eventually reach 1, the number is "happy" — return true.
If you never reach 1, you're stuck in a loop forever — return false.
```

## 🔢 The example
```
Input:  19
19  -> 1² + 9²      = 1 + 81   = 82
82  -> 8² + 2²      = 64 + 4   = 68
68  -> 6² + 8²      = 36 + 64  = 100
100 -> 1² + 0² + 0² = 1              <- happy
Output: true

Input:  2
2 -> 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4 -> ...
                ^                                        |
                +----------------------------------------+
Output: false   (back to 4 — it will go round forever)
```

## 🧸 ELI5
> Every number points at exactly one other number — the sum of its squared digits.
> `19` points at `82`. `82` points at `68`. Nobody points at two places.
>
> That is *precisely* what a linked list is: a node with one `next`.
>
> So you are walking a linked list. You just never see the arrows, because they are
> computed instead of stored. And a walk down this list ends one of two ways: you
> arrive at `1` (the end of the road), or you go round in a circle forever.
>
> "Am I going round in a circle?" is the question you already know how to answer with
> two runners at different speeds.

**Why must it be one or the other?** Because the numbers can't run away from you. Any
number below 1000 maps to at most 9² × 4 = 324, and anything bigger shrinks fast. So
after a step or two you're trapped in a small finite set of values — and walking
forever inside a finite set *must* repeat something. There is no third outcome.

## 🐌 Brute force (say it, don't type it)
Keep a `set` of numbers you've already seen. Loop: if you hit 1, return true; if you
hit something already in the set, return false.

```python
seen = set()
while n != 1 and n not in seen:
    seen.add(n)
    n = sum_of_squares(n)
return n == 1
```

**O(log n) time, O(log n) space.** This is a perfectly good answer and you should say
it first. It's also what most candidates stop at. The follow-up — *"can you do it in
O(1) space?"* — is the actual interview question.

## 💡 The pattern reveal
**Signal:** a value maps to exactly one next value · repeat forever · "does it loop?"
**Therefore:** Fast & Slow pointers, Shape A — on an *implicit* linked list.

**Key insight:** a **function is a linked list**. `next(x) = sum_of_squared_digits(x)`
is the `.next` pointer. You don't need nodes in memory to run Floyd's algorithm; you
just need a rule that turns a position into the next position.

**The one adaptation:** in episode 13, the walk ended when `fast` fell off the end
(`None`). Here there is no end — the chain is infinite. The terminator is the value
`1`, because `1 → 1 → 1 → …` is itself a cycle of length one. So instead of checking
`while fast and fast.next`, you check `while fast != 1`.

## 🔍 Dry run — `n = 19` (happy)
| step | slow = sq(slow) | fast = sq(sq(fast)) | verdict |
|---|---|---|---|
| start | 19 | 19 | — |
| 1 | 82 | 68 | keep going |
| 2 | 68 | **1** | `fast` reached 1 → return `True` |

Note `fast` gets there first — that's the point of moving twice as fast.

## 🔍 Dry run — `n = 2` (unhappy)
| step | slow | fast | verdict |
|---|---|---|---|
| start | 2 | 2 | — |
| 1 | 4 | 16 | |
| 2 | 16 | 58 | |
| 3 | 37 | 145 | |
| 4 | 58 | 20 | |
| 5 | 89 | 16 | |
| 6 | 145 | 58 | |
| 7 | 42 | 145 | |
| 8 | **20** | **20** | they met → return `False` |

Eight steps, and the memory used was two integers. That's the whole sales pitch.

## ✅ Optimal solution
```python
class Solution:
    def isHappy(self, n: int) -> bool:
        """Is n happy? Floyd's cycle detection on an implicit linked list.

        Time:  O(log n) — each step shrinks a large number sharply; the walk is
               then confined to values below ~243, a constant-size set.
        Space: O(1) — two integers. This is the whole point.
        """
        def next_value(x: int) -> int:
            total = 0
            while x:
                x, digit = divmod(x, 10)
                total += digit * digit
            return total

        slow, fast = n, n
        while True:
            slow = next_value(slow)             # 1 step
            fast = next_value(next_value(fast)) # 2 steps
            if fast == 1:                       # 1 is the end of the road
                return True
            if slow == fast:                    # met before reaching 1 -> cycle
                return False
```
**Time:** O(log n) · **Space:** O(1) ✓

### The digit loop, said out loud
`divmod(x, 10)` peels the last digit and shifts the rest down. It's the arithmetic
version of reading a number right to left. The `str(x)` version is one line and also
fine — `sum(int(d)**2 for d in str(x))` — but mention that it allocates a string,
and that an interviewer in C or Java will expect the arithmetic version.

## ⚠️ Gotchas
- **Check `fast == 1` before `slow == fast`.** Once `fast` lands on 1 it stays there,
  so `slow` will eventually meet it at 1 — and if you check the meeting first you
  return `False` on a happy number. Order matters here.
- **Only test `fast`, not `slow`, against 1.** `fast` is ahead; testing both is
  harmless but testing only `slow` makes the fast pointer pointless.
- **Advance before comparing.** Both start at `n`, so comparing first returns
  immediately on every input — the same bug as episode 13.
- `n = 1` must return `True`. Trace it: `slow → 1`, `fast → 1`, the `fast == 1` check
  fires on the first iteration. Works, but check it on camera rather than assuming.
- **No termination guard is needed and none should be added.** A `for _ in range(100)`
  safety loop reads as "I'm not sure this terminates," which is the opposite of the
  signal you want.

## 🎤 Interview talking points
- *"A function that maps each value to exactly one next value is a linked list whose
  pointers are computed rather than stored — so Floyd's applies unchanged."* ← this
  is the sentence the whole episode exists to teach.
- *"It must terminate or cycle because the values are bounded: for a 3-digit number
  the maximum next value is 3 × 81 = 243, so the walk is confined to a finite set,
  and an infinite walk on a finite set has to repeat."*
- *"The hash set is O(log n) space; Floyd's is O(1). Same time complexity, strictly
  less memory."*

## 🔗 Transfer
Tomorrow (EP16, Find the Duplicate Number) is the same trick with a nastier disguise:
`i → nums[i]` is the hidden linked list, and you need Floyd's **phase two** from EP14
to find where the cycle starts. These two episodes together are the reason this
pattern is worth knowing — they look nothing like linked lists and they are.

## 📹 Metadata
- **Title:** `Happy Number — the linked list that isn't there | Fast & Slow #3`
- **Thumbnail:** `A FUNCTION IS A LIST` (teal block)
- **Short:** The "19 → 82 → 68 → 100 → 1" chain drawn as arrows, then the reveal that arrows = `.next`.
