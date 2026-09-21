# EP019 · P02E07 · Rearrange a LinkedList   [Medium]

**Pattern:** Fast & Slow Pointers · **Link:** https://leetcode.com/problems/reorder-list/

---

## 🎬 Hook
> "This is yesterday's problem with the last step swapped. Find the middle, reverse
> the back half — and instead of comparing the two halves, zip them together. Three
> techniques you already own, and the whole episode is about the seams between them."

## 📋 Problem, in your words
```
Given a list  L0 -> L1 -> ... -> Ln-1 -> Ln

reorder it to  L0 -> Ln -> L1 -> Ln-1 -> L2 -> Ln-2 -> ...

Take one from the front, one from the back, alternating.
Do it by rewiring nodes — you may not change the values.
```

## 🔢 The example
```
Input:  1 -> 2 -> 3 -> 4
Output: 1 -> 4 -> 2 -> 3

Input:  1 -> 2 -> 3 -> 4 -> 5
Output: 1 -> 5 -> 2 -> 4 -> 3
```

## 🧸 ELI5
> You're dealing out a deck into a new pile: top card, bottom card, next-from-top,
> next-from-bottom, until they meet in the middle.
>
> The problem is you can't reach the bottom of a linked list — there is no "previous."
> So you cut the deck in half, **flip the back half over** so its bottom card is now
> on top, and then you just take alternately from the two piles, front to front.
>
> Cut · flip · zip.

## 🐌 Brute force (say it, don't type it)
Dump the nodes into an array, then rewire using two indices walking inwards.

```python
nodes = []
cur = head
while cur: nodes.append(cur); cur = cur.next
i, j = 0, len(nodes) - 1
while i < j:
    nodes[i].next = nodes[j]; i += 1
    if i == j: break
    nodes[j].next = nodes[i]; j -= 1
nodes[i].next = None
```

**O(n) time, O(n) space.** It works, and the array gives you the random access the
list denies you. It's a good thing to say first — then note that the follow-up wants
O(1) space, and the array is the only thing standing in the way.

## 💡 The pattern reveal
**Signal:** interleave a list front-to-back · in place · O(1) space.
**Therefore:** Fast & Slow (Shape C) for the middle → reverse → merge.

**Key insight:** the reason this is hard is that you need to walk *backwards* from the
tail, and a singly linked list won't let you. Reversing the second half converts
"walk backwards from the end" into "walk forwards from the middle" — and forwards is
the only direction you have.

**This is the composition episode of the pattern.** Every piece is from an earlier
day. What's tested is whether you can hold three moving parts in your head at once
without dropping a pointer.

## 🔍 Dry run — `1 → 2 → 3 → 4 → 5`

**Step 1 — find the middle.** Note the loop condition changed from yesterday:
`while fast.next and fast.next.next`.

| step | slow | fast |
|---|---|---|
| start | 1 | 1 |
| 1 | 2 | 3 |
| 2 | **3** | **5** | `fast.next` is `None` → stop |

`slow` = 3, the **end of the first half**. (Yesterday's `while fast and fast.next`
would have stopped on the *start* of the second half — see the gotcha below; this one
line is the difference between working and a lost node.)

**Step 2 — cut and reverse.** `second = slow.next` (the node `4`), then
`slow.next = None`:

```
first:   1 -> 2 -> 3 -> None
second:  4 -> 5 -> None      reversed:  5 -> 4 -> None
```

**Step 3 — zip:**

| step | take from first | take from second | list so far |
|---|---|---|---|
| 1 | 1 | 5 | `1 -> 5` |
| 2 | 2 | 4 | `1 -> 5 -> 2 -> 4` |
| 3 | 3 | — | `1 -> 5 -> 2 -> 4 -> 3` ✓ |

The first half is the longer one for odd lengths, so it supplies the final node and
the zip ends naturally.

## ✅ Optimal solution
```python
class Solution:
    def reorderList(self, head: Optional[ListNode]) -> None:
        """Reorder in place: L0 -> Ln -> L1 -> Ln-1 -> ...

        Time:  O(n) — three linear passes: middle, reverse, zip.
        Space: O(1) — pointer rewiring only.
        """
        if not head or not head.next:
            return

        # 1. middle — this condition leaves `slow` on the END of the first half
        slow = fast = head
        while fast.next and fast.next.next:
            slow = slow.next
            fast = fast.next.next

        # 2. split, then reverse the second half
        second = slow.next
        slow.next = None                 # the cut matters — see gotchas
        prev = None
        while second:
            second.next, prev, second = prev, second, second.next

        # 3. zip the two halves together
        first, second = head, prev
        while second:
            first.next, second.next, first, second = (
                second, first.next, first.next, second.next
            )
```
**Time:** O(n) · **Space:** O(1) ✓ · returns `None`, mutates in place ✓

### The zip line, unpacked
That tuple assignment is four operations at once. Written out:

```python
while second:
    tmp1 = first.next      # remember the rest of the front half
    tmp2 = second.next     # remember the rest of the back half
    first.next = second    # front node now points at a back node
    second.next = tmp1     # that back node points at the next front node
    first = tmp1           # advance both
    second = tmp2
```

Write the six-line version on camera first. The one-liner is only safe because Python
evaluates the whole right-hand side before assigning anything — worth saying, because
the same line in C would corrupt the list.

## ⚠️ Gotchas
- **The middle condition is different from EP17 and EP18.** Here it's
  `while fast.next and fast.next.next`, which leaves `slow` on the **last node of the
  first half**. Yesterday's `while fast and fast.next` leaves it on the **first node
  of the second half**. Use yesterday's here and on `[1,2,3,4]` you'll split as
  `[1,2]` and `[3,4]` with `3` still reachable from `2` — a node ends up in both
  halves and the zip produces a cycle. **This is the bug of the episode.** Let it
  happen on camera, then fix it.
- **You must cut with `slow.next = None`.** Without it the first half still runs into
  the second, and the zip builds a loop. The cut is one line and it is load-bearing.
- **Loop the zip on `second`, not `first`.** After the cut, the first half is equal
  (even) or one longer (odd). `second` is never longer, so it's the safe terminator.
- **Return `None`.** The signature says in-place. Returning `head` is harmless on
  LeetCode and wrong against the stated contract — say which you're doing.
- **Guard `not head or not head.next` at the top.** A single node would otherwise hit
  `fast.next.next` on a `None`.
- `[1,2]` must come out as `[1,2]`, unchanged. Trace it: the middle loop never runs,
  `second` = `2`, the cut gives `[1]` and `[2]`, the zip restores `1 -> 2`. Good
  test — it's the smallest case where a wrong middle shows up.

## 🎤 Interview talking points
- *"The obstacle is that a singly linked list has no previous pointer, so I can't walk
  in from the tail. Reversing the back half turns 'backwards from the end' into
  'forwards from the middle'."*
- *"Three passes, all O(n), so O(n) overall — and no allocation, which is what the
  follow-up is really asking for."*
- *"I pick the middle so that `slow` ends on the first half's tail, because I need to
  cut there. Which middle you want depends on what you do next — it's a deliberate
  choice, not a detail."*

## 🔗 Transfer
Middle + reverse + merge is exactly **merge sort on a linked list** (split at the
middle, sort, merge) — the same three moves with a different combine step. Tomorrow
(EP20) closes the pattern by going back to cycle detection at its hardest. After that
the two-pointer family is done and Pattern 03 (Sliding Window) begins.

## 📹 Metadata
- **Title:** `Reorder List — cut, flip, zip | Fast & Slow #7`
- **Thumbnail:** `CUT · FLIP · ZIP` (teal block)
- **Short:** The `[1,2,3,4]` wrong-middle bug producing a cycle, then the one-word fix.
