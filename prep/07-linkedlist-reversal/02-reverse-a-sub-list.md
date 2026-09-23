# EP053 · P07E02 · Reverse a Sub-list   [Medium]

**Pattern:** In-place Reversal of a LinkedList · **Link:** https://leetcode.com/problems/reverse-linked-list-ii/

---

## 🎬 Hook
> "Reverse only positions 2 through 4 and leave the rest alone. The reversal itself is
> yesterday's four lines, unchanged. Everything that makes this Medium instead of Easy
> is the **stitching**: the node before the block, the node after it, and the fact that
> the block's first node quietly becomes its last."

## 📋 Problem, in your words
```
Given the head of a singly linked list and two positions left <= right
(1-INDEXED), reverse the nodes from position left to position right
inclusive, and return the head of the modified list.

One pass, in place. left may be 1, which means the head itself moves.
```

## 🔢 The example
```
Input:  1 -> 2 -> 3 -> 4 -> 5,  left = 2, right = 4
Output: 1 -> 4 -> 3 -> 2 -> 5
              ^^^^^^^^^^ reversed; the 1 and the 5 never move

Input:  1 -> 2 -> 3,  left = 1, right = 3   -> 3 -> 2 -> 1   <- the head moves
Input:  5,            left = 1, right = 1   -> 5             <- nothing to do
```
`left = 1` is the case that justifies the dummy node, and `left == right` is the case
that must not corrupt anything.

## 🧸 ELI5
> Four nodes matter, and only four. Name them before you write anything:
>
> ```
>            before    first          last     after
>              |         |              |        |
>    1  ---->  1   ->    2  ->  3  ->   4   ->   5
>              ^      [ the block to reverse ]
> ```
>
> Reverse the block on its own, `2 -> 3 -> 4` becomes `4 -> 3 -> 2`, and you're left
> holding a loose piece:
>
> ```
>    before -> ???      4 -> 3 -> 2 -> ???      after
> ```
>
> Two rewires and it's done:
>
> 1. `before.next = last`, the list now runs into the reversed block from the left.
> 2. `first.next = after`, **the old first node is the block's tail now**, so it's the
>    one that must point at what came after.
>
> That second one is the whole episode. `first` looks like a head and behaves like a
> tail, and if you don't wire it to `after`, everything past the block is gone.

## 🐌 Brute force (say it, don't type it)
Copy the values into a list, reverse the slice `[left-1:right]`, write them back.
**O(n) time, O(n) space**, and genuinely easy. The interviewer is asking for the pointer
version, so name the array one, name its space cost, and move on.

## 💡 The pattern reveal
**Signal:** reverse **part** of a linked list, given positions · in place.
**Therefore:** dummy node, walk to `before`, run EP52's loop exactly `right − left + 1`
times, rewire two links.

**Key insight, the dummy node.** When `left = 1` there *is* no node before the block,
so every "is this the head?" branch you'd otherwise need disappears if you invent one:

```python
dummy = ListNode(0, head)      # a fake node that is always there
before = dummy
for _ in range(left - 1):      # walk to the node just before position `left`
    before = before.next
...
return dummy.next              # the head, whether or not it moved
```

**The reversal is unchanged from EP52**: it just runs a counted number of times instead
of until the end:

```python
prev, cur = None, before.next
for _ in range(right - left + 1):
    nxt = cur.next
    cur.next = prev
    prev = cur
    cur = nxt
# now: prev == `last` (new head of block), cur == `after`
```

When that loop finishes, **`prev` is the block's new head and `cur` is the node after
the block**: both handed to you for free. That's why the counted loop is worth
preferring over a "walk to position right" approach: it leaves the two values you need
sitting in the two variables you already have.

**🧨 The trap: the order of the two rewires.** Write them like this,
```python
before.next.next = cur     # `before.next` is STILL the old first node -> point it at `after`
before.next = prev         # ...and only NOW move `before` onto the new head
```,

and you never need a separate `first` variable. Swap those two lines and
`before.next` has already been reassigned, so the first line wires the *new* head to
`after`, producing `1 -> 4 -> 5` and losing two nodes. If that's confusing, save
`first = before.next` before the reversal and write the two rewires with explicit names.
Both are fine; mixing them is not.

## 🔍 Dry run: `1 -> 2 -> 3 -> 4 -> 5`, `left = 2`, `right = 4`
`dummy -> 1 -> 2 -> 3 -> 4 -> 5`. Walk `left − 1 = 1` step: `before = 1`.

Reverse `right − left + 1 = 3` nodes, starting at `cur = 2`, `prev = None`:

| iteration | `cur` | `nxt` | after `cur.next = prev` | `prev` | `cur` |
|---|---|---|---|---|---|
| 1 | `2` | `3` | `2 -> None` | `2` | `3` |
| 2 | `3` | `4` | `3 -> 2` | `3` | `4` |
| 3 | `4` | `5` | `4 -> 3` | **`4`** | **`5`** |

Loop ends. `prev = 4` (the block's new head), `cur = 5` (the node after the block).

Now the stitching:

| rewire | effect |
|---|---|
| `before.next.next = cur` → node `2`.next = `5` | the block's **tail** rejoins the list |
| `before.next = prev` → node `1`.next = `4` | the list runs into the block's new head |

Result: `1 -> 4 -> 3 -> 2 -> 5` ✓

Point at node `2` on camera and say it out loud: *"this was the first node of the block;
it is now the last."* That sentence is the episode.

## ✅ Optimal solution
```python
class Solution:
    def reverseBetween(self, head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:
        """Reverse positions left..right (1-indexed) in place, one pass.

        Time:  O(n), walk to `left`, reverse the block, done.
        Space: O(1), a dummy node and three pointers.
        """
        if not head or left == right:
            return head                   # nothing to reverse

        dummy = ListNode(0, head)         # so a `before` node always exists
        before = dummy
        for _ in range(left - 1):
            before = before.next          # node just before position `left`

        prev, cur = None, before.next
        for _ in range(right - left + 1):     # exactly this many nodes
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        # prev == new head of the block, cur == the node AFTER the block

        before.next.next = cur            # old first node is the tail: rejoin the rest
        before.next = prev                # ...then point `before` at the new head

        return dummy.next
```
**Time:** O(n) · **Space:** O(1)

## ⚠️ Gotchas
- **`before.next.next = cur` comes BEFORE `before.next = prev`.** Reversed, you lose the
  tail of the list. If in doubt, save `first = before.next` up front and use names.
- **Positions are 1-indexed.** `left - 1` steps to reach `before`, and
  `right - left + 1` nodes in the block. Off-by-one here reverses the wrong slice, which
  looks plausible and is wrong.
- **The dummy node handles `left = 1`.** Without it you need a separate "the head moved"
  branch, write it once to see how ugly it is, then never again.
- **`left == right`** must return the list untouched; the early return is cheaper than
  trusting the loop.
- **Return `dummy.next`, not `head`.** When `left = 1`, `head` is the tail of the
  reversed block.
- **`cur` may legitimately be `None`** when `right` is the last position. `first.next =
  None` is correct, don't guard against it.

## 🎤 Interview talking points
- *"I use a dummy node so the node before the block always exists, even when the block
  starts at the head."* ← say this before writing the loop.
- *"The counted loop leaves me exactly what I need: `prev` is the block's new head and
  `cur` is the node after it."*
- *"The block's old first node is its new tail, so that's the one I wire to the
  remainder."* ← the sentence this problem exists to hear.
- *"One pass, O(1) space. The array version is O(n) space and reverses a slice trivially,
  but that isn't the exercise."*

## 🔗 Transfer
The four-node picture, `before`, first, last, `after`, is now fixed, and the next
three episodes reuse it verbatim, just with the block boundaries decided differently:
fixed at 2 (EP54), fixed at k (EP55), growing (EP56). Tomorrow (EP54) runs it in a loop
for the first time, which introduces the other half of the bookkeeping: where `before`
moves to for the *next* block.

## 📹 Metadata
- **Title:** `Reverse a Sub-list, the first node becomes the tail | LinkedList Reversal #2`
- **Thumbnail:** `BEFORE · BLOCK · AFTER` (green block)
- **Short:** the two rewires in the wrong order, dropping half the list. 45s.
