# EP014 · P02E02 · Start of LinkedList Cycle   [Medium]

**Pattern:** Fast & Slow Pointers · **Link:** https://leetcode.com/problems/linked-list-cycle-ii/

---

## 🎬 Hook
> "Finding *that* there's a loop was yesterday. Finding *where* it starts looks like
> it should need extra memory — and it doesn't. Four lines of algebra prove that if
> you just reset one pointer to the head, the two will collide exactly at the
> entrance. This is the prettiest result in the whole pattern."

## 📋 Problem, in your words
```
Given the head of a linked list, return the node where the cycle BEGINS.
If there is no cycle, return null.

Do not modify the list. Follow-up: O(1) memory.
```

## 🔢 The example
```
3 -> 2 -> 0 -> -4
     ^           |
     +-----------+
Output: the node with value 2   (index 1 — where the loop re-enters)
```

## 🧸 ELI5
> Picture a lasso: a straight rope (the **tail**) leading into a loop.
>
> Yesterday's runners meet somewhere *inside* the loop — but not usually at the knot
> where the rope joins it. You want the knot.
>
> Here's the trick. It turns out the distance from the **start of the rope** to the
> knot is exactly the same as the distance from **where they met** back around to the
> knot. So: leave one runner at the meeting point, send the other back to the very
> start, and let them both walk at *normal* speed. They arrive at the knot together.
>
> It feels like magic. It's actually just one equation.

## 🐌 Brute force (say it, don't type it)
Hash set again — walk the list, and the **first** node you see twice *is* the cycle
entrance. O(n) time, O(n) space. Honest and clear. Then go for O(1).

## 💡 The pattern reveal
**Signal:** cycle + "where does it start" + O(1) space.
**Therefore:** Floyd's **two-phase** algorithm — detection, then entrance.

**Key insight — the algebra. Put this on screen.**

Let `F` = head → entrance, `a` = entrance → meeting point, `C` = cycle length.

At the meeting:
- `slow` has walked `F + a`
- `fast` has walked `F + a + nC`  *(n full extra laps)*
- `fast` walked twice as far, so: `2(F + a) = F + a + nC`

Simplify:
```
2F + 2a = F + a + nC
     F + a = nC
         F = nC − a
```

**Read that last line out loud:** the distance from the head to the entrance equals
the distance from the meeting point forward to the entrance (plus whole laps, which
don't matter). So two pointers walking at equal speed — one from the head, one from
the meeting point — arrive together. At the entrance.

## 🔍 Dry run — `3 → 2 → 0 → -4 → (back to 2)`
Nodes A(3) B(2) C(0) D(-4). Entrance is **B**. `F = 1`, `C = 3`.

**Phase 1 — detect:**

| step | slow | fast |
|---|---|---|
| 1 | B | C |
| 2 | C | B |
| 3 | D | D ← **meet at D** |

Meeting point D, so `a = 2` (B → C → D). Check: `F = nC − a` → `1 = 1·3 − 2` ✓

**Phase 2 — find the entrance:**

| step | slow (from head) | fast (from meet) |
|---|---|---|
| start | A | D |
| 1 | **B** | **B** ← meet at the entrance ✓ |

Return B. One step, exactly as `F = 1` predicted.

## ✅ Optimal solution
```python
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = fast = head

        # phase 1 — is there a cycle, and where do they meet?
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                break
        else:
            return None                  # loop ended normally => no cycle
        if not (fast and fast.next):
            return None                  # belt and braces for the break-less exit

        # phase 2 — reset one to head, walk BOTH at the same speed
        slow = head
        while slow is not fast:
            slow = slow.next
            fast = fast.next

        return slow                      # == fast == the cycle entrance
```
**Time:** O(n) — phase 1 is ≤ n, phase 2 is ≤ n.
**Space:** O(1) ✓

> The `while ... else` is a genuinely nice Python detail worth explaining on camera:
> the `else` runs only if the loop finished *without* `break`, i.e. no cycle. Most
> people have never seen it. Small moments like that are memorable and shareable.

## ⚠️ Gotchas
- **Reset `slow` to `head`, and move both by ONE.** The single most common error is
  leaving `fast` on double speed in phase 2 — then they meet somewhere arbitrary.
- **Don't reset `fast`.** It must stay parked at the meeting point; that's the whole
  premise of the equation.
- **`while slow is not fast`, checked *before* stepping.** If the entrance is the
  head itself (`F = 0`), they're already equal and the answer is `head` with zero
  steps. Stepping first overshoots by a full lap.
- Return `None`, not `False` — the problem wants a node or null.

## 🎤 Interview talking points
- Recite the derivation. *"`slow` walks `F + a`, `fast` walks `F + a + nC`, and
  `fast` walks double — so `F = nC − a`, which means head-to-entrance equals
  meeting-point-to-entrance."* **This is the answer that gets you hired on this
  question.** Everyone can memorise "reset to head"; almost nobody can say why.
- *"It's O(1) space, versus O(n) for the hash-set version."*

## 🔗 Transfer
EP16 (Find the Duplicate Number) is *this exact algorithm* on an array — the hard
part there is only seeing that `i → nums[i]` is a linked list. If phase 2 lands
today, EP16 is a 10-minute problem.

## 📹 Metadata
- **Title:** `Linked List Cycle II — the algebra behind "just reset to head" | Fast & Slow #2`
- **Thumbnail:** `F = nC − a` (teal block)
- **Short:** The four-line derivation. Whiteboard it. Great standalone.
