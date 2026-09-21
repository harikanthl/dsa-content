# EP055 · P07E04 · Reverse every K-element Sub-list   [Hard]

**Pattern:** In-place Reversal of a LinkedList · **Link:** https://leetcode.com/problems/reverse-nodes-in-k-group/

---

## 🎬 Hook
> "Reverse the list in blocks of k — and if the last block is short, leave it alone.
> That last clause is what makes this Hard: you cannot start reversing a block until you
> know it's **full**, and by the time you find out you've already walked it. So you
> count first, then reverse, and the counting walk hands you the node after the block
> for free."

## 📋 Problem, in your words
```
Given the head of a linked list and an integer k, reverse the nodes in
groups of k and return the modified list.

If the number of nodes left is FEWER than k, leave them as they are.
Swap nodes, not values. O(1) extra space.
```

## 🔢 The example
```
Input:  1 -> 2 -> 3 -> 4 -> 5,  k = 2     Output: 2 -> 1 -> 4 -> 3 -> 5
                                                                   ^ leftover, untouched
Input:  1 -> 2 -> 3 -> 4 -> 5,  k = 3     Output: 3 -> 2 -> 1 -> 4 -> 5
                                                            ^^^^^^^^^ only 2 left, untouched
Input:  1 -> 2 -> 3,            k = 1     Output: 1 -> 2 -> 3      <- k=1 is a no-op
Input:  1 -> 2,                 k = 5     Output: 1 -> 2           <- one short block
```

## 🧸 ELI5
> Same four nodes as EP53, except now you march them down the list:
>
> ```
> group_prev            kth      group_next
>     |                  |           |
>  dummy -> [ 1 -> 2 -> 3 ] ->  4 -> 5
>              the block
> ```
>
> Each round has three beats:
>
> 1. **Count.** Walk `k` nodes from `group_prev`. If you fall off the end first, the
>    block is short — **stop, return, change nothing.** If you land on a node, that's
>    `kth`, the block's last node, and `kth.next` is `group_next`.
> 2. **Reverse** the block, stopping at `group_next` instead of at `None`.
> 3. **Stitch**: `group_prev.next = kth` (the block's new head), and the block's old
>    head — which is now its tail — points at `group_next`. Then `group_prev` moves onto
>    that old head, ready for the next block.
>
> The counting walk isn't overhead. It's how you learn *both* whether the block is full
> *and* where it ends — two facts, one walk.

## 🐌 Brute force (say it, don't type it)
Values into an array, reverse each full chunk of k, write back. **O(n) space**, easy,
and not what's being asked. Say it and move on — this problem's difficulty isn't the
algorithm, it's the pointer discipline.

## 💡 The pattern reveal
**Signal:** reverse in groups of **k** · leftover left alone · in place.
**Therefore:** count k ahead, reverse to a sentinel, stitch, advance.

**Key insight #1 — check before you touch.** The "leave the remainder alone" rule means
a block must be verified full *before* a single pointer is flipped. Once you start
reversing and run out of nodes, undoing it is far harder than checking first:

```python
kth = group_prev
for _ in range(k):
    kth = kth.next
    if not kth:
        return dummy.next        # fewer than k remain: we're done, untouched
```

**Key insight #2 — reverse *to a sentinel*, not to `None`.** EP52's loop seeds
`prev = None` because the whole list ends in `None`. Here the block ends at
`group_next`, so seed `prev = group_next` and the block's tail is wired to the remainder
**by the reversal itself** — one fewer rewire to forget:

```python
prev, cur = group_next, group_prev.next       # note: NOT None
while cur is not group_next:                  # note: NOT `while cur`
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
```

That's a genuinely elegant trick and it's worth slowing down for on camera: the sentinel
does double duty as the stop condition *and* as the tail's forward link.

**🧨 The trap: `group_prev` must move to the block's OLD head.** After reversing, the
old head is the block's tail, and the next block hangs off it:

```python
tail = group_prev.next        # save BEFORE rewiring -- this is the old head
group_prev.next = kth         # the block's new head
group_prev = tail             # ...and the next block starts after the old head
```

Read `group_prev.next` after the rewire and you'll pick up `kth` instead, which sends
the next round back over nodes you've already reversed — a cycle, and a hang.

**Use `is not`, not `!=`.** You're comparing node identity, and `!=` on nodes without
`__eq__` happens to do the same thing — but saying `is not` states the intent and is
immune to a class that defines `__eq__` by value.

## 🔍 Dry run — `1 -> 2 -> 3 -> 4 -> 5`, `k = 2`
`dummy -> 1 -> 2 -> 3 -> 4 -> 5`, `group_prev = dummy`.

| round | count 2 from `group_prev` | `kth` | `group_next` | reverse | stitch | list after |
|---|---|---|---|---|---|---|
| 1 | `1`, `2` ✓ | `2` | `3` | `2 -> 1 -> 3` | `dummy -> 2`; `group_prev = 1` | `2 -> 1 -> 3 -> 4 -> 5` |
| 2 | `3`, `4` ✓ | `4` | `5` | `4 -> 3 -> 5` | `1 -> 4`; `group_prev = 3` | `2 -> 1 -> 4 -> 3 -> 5` |
| 3 | `5` ✓, then `None` ✗ | — | — | — | **return** | `2 -> 1 -> 4 -> 3 -> 5` ✓ |

Answer **`2 -> 1 -> 4 -> 3 -> 5`** ✓

Round 3 is the episode's whole point: the counting loop walks onto node `5`, then tries
for a second node, finds `None`, and returns **without having flipped anything**. The
leftover survives because nothing touched it.

## 🔍 Dry run — the reversal of round 1, in detail
`prev = group_next = 3`, `cur = 1`:

| iteration | `cur` | `nxt` | `cur.next = prev` | `prev` | `cur` | stop? |
|---|---|---|---|---|---|---|
| 1 | `1` | `2` | `1 -> 3` ← the tail is wired already | `1` | `2` | `2 is not 3` → continue |
| 2 | `2` | `3` | `2 -> 1` | `2` | `3` | `3 is not 3` is **False** → stop |

`prev = 2` is the block's new head; node `1` already points at `3`. **The sentinel seed
did the tail rewire for us** — that's the line to point at on camera.

## ✅ Optimal solution
```python
class Solution:
    def reverseKGroup(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        """Reverse in groups of k; a final group shorter than k is left alone.

        Time:  O(n) — each node is counted once and reversed at most once.
        Space: O(1) — a dummy node and a few pointers.
        """
        dummy = ListNode(0, head)
        group_prev = dummy

        while True:
            # 1. is there a FULL block? walking it also finds its last node
            kth = group_prev
            for _ in range(k):
                kth = kth.next
                if not kth:
                    return dummy.next        # short block: leave it untouched
            group_next = kth.next

            # 2. reverse the block, stopping AT group_next
            #    seeding prev with group_next wires the block's tail for free
            prev, cur = group_next, group_prev.next
            while cur is not group_next:
                nxt = cur.next
                cur.next = prev
                prev = cur
                cur = nxt

            # 3. stitch, and move group_prev onto the block's OLD head (its new tail)
            tail = group_prev.next
            group_prev.next = kth
            group_prev = tail
```
**Time:** O(n) · **Space:** O(1)

## ⚠️ Gotchas
- **Verify the block is full before flipping anything.** The counting loop's `if not
  kth: return` is the entire "leftover" rule.
- **Seed `prev = group_next`, not `None`.** With `None` the block's tail terminates the
  list and everything after the block is lost.
- **`while cur is not group_next`, not `while cur`.** Otherwise you reverse the whole
  remainder of the list in the first round.
- **Save `tail = group_prev.next` before rewiring.** Afterwards it points at `kth` and
  the next round loops over the same nodes — a hang.
- **`k = 1`** must be a no-op: every block of one reverses to itself. Run it; if it
  hangs, the `group_prev` bookkeeping is wrong.
- **`while True` with the return inside** is deliberate — the exit condition is "not
  enough nodes left", which is discovered mid-count, not at the top.
- **Each node is touched a constant number of times** (once counting, once reversing),
  so it's O(n) despite the nested loops. Expect to be asked.

## 🎤 Interview talking points
- *"I count k nodes ahead first, because the leftover rule means I can't start reversing
  until I know the block is full — and the same walk gives me the node after the
  block."* ← the answer to the question being asked.
- *"I seed the reversal with `group_next` instead of `None`, so the block's tail is
  wired to the remainder as part of the reversal."* ← the detail that reads as fluent.
- *"After reversing, the old head is the tail, so that's where the next group hangs
  from."*
- *"O(n) overall — every node is counted once and flipped at most once — and O(1)
  space."*

## 🔗 Transfer
EP54 was this with `k = 2` and the reversal unrolled by hand. Tomorrow (EP56) keeps the
machinery identical and makes the block size **change every round** — 1, 2, 3, 4, … —
with the extra twist that only *some* blocks get reversed, and the last block's real
length may be shorter than its nominal size. The counting walk you just wrote is exactly
how you find that out.

## 📹 Metadata
- **Title:** `Reverse Nodes in k-Group — count before you flip | LinkedList Reversal #4`
- **Thumbnail:** `COUNT FIRST` (green block)
- **Short:** the sentinel seed doing the tail rewire for free, traced on two nodes. 50s.
