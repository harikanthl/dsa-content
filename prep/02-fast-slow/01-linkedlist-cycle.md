# EP013 · P02E01 · LinkedList Cycle   [Easy]

**Pattern:** Fast & Slow Pointers · **Link:** https://leetcode.com/problems/linked-list-cycle/

---

## 🎬 Hook
> "Two runners on a track, one twice as fast as the other. If the track loops, the
> fast one *has* to lap the slow one, it's not luck, it's arithmetic. That single
> fact replaces a whole hash set and drops this to constant memory."

## 📋 Problem, in your words
```
Given the head of a linked list, return true if it has a cycle in it.

A cycle means some node's `next` points back to an earlier node,
so following `next` forever never reaches null.

Follow-up: solve it using O(1) memory.
```

## 🔢 The example
```
3 -> 2 -> 0 -> -4
     ^           |
     +-----------+
Output: true   (the tail links back to the node with value 2)

1 -> 2 -> null
Output: false
```

## 🧸 ELI5
> You and a friend start walking a path. You walk normally; your friend jogs at
> exactly double your pace.
>
> If the path is **straight**, your friend reaches the end and stops. No cycle.
>
> If the path is a **loop**, your friend keeps going round and round, and eventually
> comes up behind you and taps you on the shoulder. They *must*, because every step
> they close the gap between you by exactly one. A gap that shrinks by one each time
> can't jump over zero, it lands on it.
>
> So the question "is there a loop?" becomes "did they tap my shoulder?"

## 🐌 Brute force (say it, don't type it)
Keep a `set` of nodes you've visited. Walk the list; if you ever see a node already
in the set, there's a cycle.

```python
seen = set()
while head:
    if head in seen: return True
    seen.add(head)
    head = head.next
return False
```

**O(n) time, O(n) space.** This is correct and readable, and you should absolutely
say it out loud, it's the natural first answer. Then: *"but the follow-up asks for
O(1) memory, and that's the real question."*

## 💡 The pattern reveal
**Signal:** linked list + cycle + an O(1) space constraint.
**Therefore:** Fast & Slow pointers, Shape A (Floyd's cycle detection).

**Key insight:** you don't need to *remember* where you've been. You need a second
observer moving at a different speed. Relative motion does the remembering for you.

If both pointers are inside the loop, `fast` gains exactly **one** position on `slow`
per iteration. So the gap goes `k, k-1, k-2, … 1, 0`. It can never skip 0, which is
why a meeting is guaranteed rather than likely.

## 🔍 Dry run: `3 → 2 → 0 → -4 → (back to 2)`
Label the nodes A(3) B(2) C(0) D(-4), with `D.next = B`.

| step | slow | fast | met? |
|---|---|---|---|
| start | A | A | - |
| 1 | B | C | no |
| 2 | C | B | no *(fast went D → B)* |
| 3 | D | D | **yes** → return `True` |

And on `1 → 2 → null`:

| step | slow | fast | note |
|---|---|---|---|
| start | 1 | 1 | - |
| 1 | 2 | null | `fast` fell off → loop exits → return `False` |

## ✅ Optimal solution
```python
class Solution:
    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = fast = head

        while fast and fast.next:        # fast takes 2 steps, both must exist
            slow = slow.next             # 1 step
            fast = fast.next.next        # 2 steps
            if slow is fast:             # identity, not equality
                return True

        return False                     # fast ran off the end: no cycle
```
**Time:** O(n), `slow` visits each node at most once before a meeting.
**Space:** O(1) ✓

## ⚠️ Gotchas
- **`while fast and fast.next`, not `while fast`.** You dereference *two* links
  (`fast.next.next`), so both must exist. Writing `while fast` throws
  `AttributeError: 'NoneType' object has no attribute 'next'` on any list with an
  even number of nodes. This is *the* bug on this problem, let it happen on camera.
- **`is`, not `==`.** You're comparing node *identity*, not values. Two different
  nodes can both hold the value `2`; `==` on custom objects without `__eq__` happens
  to fall back to identity in Python, so it works by accident, but say `is`, because
  it states what you mean and it's what you'd need in a language with value equality.
- **Advance before comparing.** Both start at `head`, so checking `slow is fast`
  *before* moving returns `True` on every list immediately.
- Empty list and single node both work with no special-casing: the `while` guard
  fails instantly and you return `False`.

## 🎤 Interview talking points
- *"I'd start with a hash set for clarity, then optimise to Floyd's if constant space
  is required."*
- *"They're guaranteed to meet because fast closes the gap by exactly one each
  iteration, so the gap decrements to zero rather than skipping it."* ← say this; it
  proves you know *why* rather than having memorised the shape.
- If asked about speeds other than 2: *"Any speeds p > q work for detection, but 2
  and 1 are what make the second phase, finding the cycle's start, come out to a
  clean equation."*

## 🔗 Transfer
Tomorrow (EP14) adds phase two: *where* does the cycle start? Then EP15 and EP16 use
this on problems with **no linked list at all**, which is the real payoff of the
pattern.

## 📹 Metadata
- **Title:** `Linked List Cycle, why the fast runner ALWAYS catches up | Fast & Slow #1`
- **Thumbnail:** `NO HASH SET NEEDED` (teal block)
- **Short:** The gap-shrinks-by-one argument, 45s.
