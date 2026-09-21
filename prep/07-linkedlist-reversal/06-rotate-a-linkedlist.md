# EP057 · P07E06 · Rotate a LinkedList   [Medium]

**Pattern:** In-place Reversal of a LinkedList · **Link:** https://leetcode.com/problems/rotate-list/

---

## 🎬 Hook
> "Rotate the list right by k. It's the last episode of a reversal pattern and **nothing
> gets reversed** — that's why it's here. Close the list into a ring, walk to the new
> tail, cut. Two things will try to trip you: `k` can be larger than the list, and the
> new tail is counted from the **front**, not the back."

## 📋 Problem, in your words
```
Given the head of a linked list and an integer k, rotate the list to
the RIGHT by k places, and return the new head.

Rotating right by 1 moves the last node to the front. k may be zero,
and k may be much larger than the length of the list.
```

## 🔢 The example
```
Input:  1 -> 2 -> 3 -> 4 -> 5,  k = 2      Output: 4 -> 5 -> 1 -> 2 -> 3
                                                   ^^^^^^ the last two moved to the front

Input:  0 -> 1 -> 2,  k = 4                Output: 2 -> 0 -> 1
Why:    n = 3, so k = 4 % 3 = 1. Rotating by 4 is rotating by 1.

Input:  1 -> 2,  k = 2                     Output: 1 -> 2        <- k % n == 0: unchanged
Input:  None, k = 3                        Output: None
```

## 🧸 ELI5
> Don't think about moving `k` nodes. Think about where the list **breaks**.
>
> Rotating right by 2 means the last two nodes go to the front — which means the list
> now starts at node 4 and ends at node 3:
>
> ```
> 1 -> 2 -> 3 -> 4 -> 5
>           ^ new tail  ^ new head
> ```
>
> So the whole problem is: *find the new tail, cut there.* And the new tail is
> `n − k` nodes from the front — position 3 of 5, when k = 2.
>
> The tidiest way to do the surgery is to **join the tail to the head first**, making a
> ring:
>
> ```
>  +--------------------+
>  |                    |
>  1 -> 2 -> 3 -> 4 -> 5+
>            ^ walk here from the front, then cut
> ```
>
> On a ring there's no "end of the list" to fall off, so cutting in the right place is
> the only decision left. Walk `n − k − 1` steps from the head to land on the new tail,
> take `new_tail.next` as the new head, and set `new_tail.next = None`.

## 🐌 Brute force (say it, don't type it)
Rotate by one, k times: each rotation walks to the last node and moves it. **O(n·k)**,
and with `k = 2 × 10⁹` — which the constraints allow — it never finishes. Say the
complexity out loud; it's the motivation for the modulo.

## 💡 The pattern reveal
**Signal:** a linked list · "rotate" / "shift" by k · in place.
**Therefore:** measure, close the ring, walk `n − k%n`, cut. One and a bit passes.

**Key insight #1 — `k %= n`, always.** Rotating by the length is a no-op, so only the
remainder matters. This is where the O(n·k) brute force collapses to O(n), and it's the
first thing to write after you've counted the nodes.

**Key insight #2 — count from the front, not the back.** Singly linked lists can't walk
backwards, so "the k-th node from the end" has to be re-expressed from the head:

```
new tail = node number (n - k)          1-indexed
         = (n - k - 1) steps from head  0-indexed
new head = new_tail.next
```

With `n = 5, k = 2`: new tail is node 3, reached in 2 steps from the head. ✓

**Key insight #3 — measure and close in the same pass.** Walking to the tail to count
`n` leaves you standing on the tail, so tie it to the head right there:

```python
n, tail = 1, head
while tail.next:
    tail = tail.next
    n += 1
tail.next = head        # close the ring while you're here
```

**🧨 The trap: `k % n == 0` after the modulo.** If `k` is a multiple of `n`, the list is
unchanged — but if you've already closed the ring, returning `head` returns a **circular
list**, and whatever prints it hangs. Either check before closing the ring, or cut at
the original tail. Return early and be explicit:

```python
k %= n
if k == 0:
    return head        # nothing to do -- check BEFORE closing, or undo the closure
```

**Why this is in a reversal pattern.** It isn't a reversal, and that's the point. The
instinct — reverse the whole list, reverse the first k, reverse the rest, as you'd do
for an *array* rotation — produces a **left** rotation of the wrong thing and costs
three passes. Recognising that the same pointer surgery answers it in one is the skill
this episode tests.

## 🔍 Dry run — `1 -> 2 -> 3 -> 4 -> 5`, `k = 2`

| step | what happens | state |
|---|---|---|
| 1 | walk to the tail, counting | `n = 5`, `tail = 5` |
| 2 | `k %= n` → `2 % 5 = 2` | `k = 2`, not zero, carry on |
| 3 | `tail.next = head` | ring: `1 -> 2 -> 3 -> 4 -> 5 -> 1 -> …` |
| 4 | steps to new tail = `n − k = 3`, so walk `3 − 1 = 2` from the head | `new_tail = 3` |
| 5 | `new_head = new_tail.next` | `new_head = 4` |
| 6 | `new_tail.next = None` | `4 -> 5 -> 1 -> 2 -> 3 -> None` |

Answer **`4 -> 5 -> 1 -> 2 -> 3`** ✓

## 🔍 Dry run — `0 -> 1 -> 2`, `k = 4` (the modulo)

| step | what happens | state |
|---|---|---|
| 1 | count | `n = 3`, `tail = 2` |
| 2 | `k = 4 % 3` | **`k = 1`** ← without this, step 4 walks off the end |
| 3 | close the ring | `0 -> 1 -> 2 -> 0 -> …` |
| 4 | `n − k = 2`, walk 1 step | `new_tail = 1` |
| 5–6 | cut after node `1` | `2 -> 0 -> 1 -> None` |

Answer **`2 -> 0 -> 1`** ✓

Run it once with `k = 4` and no modulo on camera: the walk loop runs past the end of
what you expected, and on a ring it keeps going quite happily — landing somewhere
arbitrary. A wrong answer with no crash, courtesy of the ring you just built.

## ✅ Optimal solution
```python
class Solution:
    def rotateRight(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """Rotate the list right by k places.

        Time:  O(n) — one pass to measure, a partial pass to the cut point.
        Space: O(1).
        """
        if not head or not head.next or k == 0:
            return head                    # nothing to rotate

        # 1. measure, and stop on the tail
        n, tail = 1, head
        while tail.next:
            tail = tail.next
            n += 1

        k %= n                             # rotating by n is a no-op
        if k == 0:
            return head                    # check BEFORE closing the ring

        # 2. close the ring
        tail.next = head

        # 3. the new tail is node (n - k), counted from the FRONT
        new_tail = head
        for _ in range(n - k - 1):
            new_tail = new_tail.next

        # 4. cut
        new_head = new_tail.next
        new_tail.next = None

        return new_head
```
**Time:** O(n) · **Space:** O(1)

## ⚠️ Gotchas
- **`k %= n` before anything else.** Constraints allow `k` up to 2×10⁹; without the
  modulo the walk is either astronomically slow or lands in the wrong place on the ring.
- **Handle `k % n == 0` before closing the ring** — or you return a circular list and
  the test harness hangs instead of failing.
- **`n - k - 1` steps, not `n - k`.** You want to *land on* the new tail, and you start
  already standing on node 1. Check it against the example: `n=5, k=2` → 2 steps → node
  3 ✓.
- **Right, not left.** Rotating right by k moves the **last** k nodes to the front.
  Rotating left by k is `n - k` to the right — read the statement twice.
- **`new_tail.next = None` is mandatory.** Forgetting it leaves the ring intact and the
  list infinite.
- **Empty or single-node lists** return immediately; there's nothing the ring logic
  could do for them anyway.

## 🎤 Interview talking points
- *"Rotating right by k means the list breaks between node n−k and node n−k+1, so I find
  that cut point rather than moving anything."* ← reframe first.
- *"`k %= n`, because rotating by the length changes nothing — that's what turns the
  naive O(n·k) into O(n)."*
- *"I close the list into a ring while I'm counting, walk `n − k − 1` from the head, and
  cut. One and a bit passes, O(1) space."*
- *"Nothing is reversed here. The array trick of three reversals also works, but it's
  three passes and it's solving a problem this list doesn't have."* ← the sentence that
  shows you know why this problem is grouped where it is.

## 🔗 Transfer
That closes Pattern 07 — and it closes it on the reminder that a pattern is a *shape*,
not a keyword: five reversal problems and one that only looks like one. The dummy node
and the save-before-you-overwrite discipline carry straight into Pattern 08 (Stack,
EP58–66), where the structure keeps the bookkeeping for you instead of you holding it in
three named pointers.

## 📹 Metadata
- **Title:** `Rotate List — close the ring, then cut | LinkedList Reversal #6`
- **Thumbnail:** `k %= n` (green block)
- **Short:** `k = 4` on a 3-node list, with and without the modulo. 40s.
