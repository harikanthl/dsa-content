# EP063 · P08E06 · Remove Nodes From Linked List   [Medium]

**Pattern:** Stack · **Link:** https://leetcode.com/problems/remove-nodes-from-linked-list/

---

## 🎬 Hook
> "Delete every node that has a bigger value anywhere to its right. That's a
> next-greater-element question in disguise, except you don't want the answers, you
> want the **survivors**. So the monotonic stack stops being scaffolding and becomes the
> output, and the last step is stitching it back into a list."

## 📋 Problem, in your words
```
Given the head of a linked list, remove every node that has a node with
a STRICTLY GREATER value anywhere to its right. Return the head of the
modified list.

Equivalently: keep a node only if it is >= everything that follows it.
```

## 🔢 The example
```
Input:  5 -> 2 -> 13 -> 3 -> 8
Output: 13 -> 8
Why:    5  has 13 to its right  -> removed
        2  has 13 to its right  -> removed
        13 has nothing bigger   -> KEPT
        3  has 8 to its right   -> removed
        8  is last              -> KEPT

Input:  1 -> 1 -> 1 -> 1     Output: 1 -> 1 -> 1 -> 1
Why:    "strictly greater" -- equal values don't remove each other.
```
That second example is the one to check first: with `<=` instead of `<`, it collapses to
a single node, and the bug is invisible on the first example.

## 🧸 ELI5
> Read the list left to right, keeping a pile of **survivors so far**.
>
> When a new node arrives, it kills everything on top of the pile that's smaller than
> it, because those nodes now have something bigger to their right, which is exactly
> the removal rule.
>
> ```
> 5  -> pile: 5
> 2  -> 2 < 5, nobody dies      pile: 5 2
> 13 -> 13 kills 2, then kills 5!   pile: 13
> 3  -> 3 < 13, nobody dies     pile: 13 3
> 8  -> 8 kills 3, but not 13   pile: 13 8
> ```
>
> The pile is always **decreasing**, and when the list runs out, the pile *is* the
> answer, read bottom to top. The only work left is to relink those survivors into an
> actual list, because along the way their `.next` pointers have been pointing at nodes
> that are now dead.

## 🐌 Brute force (say it, don't type it)
For every node, scan the rest of the list for something bigger; delete if found.
**O(n²)**, correct, and on a decreasing list it's the full quadratic. Mention the
**reverse-and-sweep** alternative too, reverse the list, walk it keeping a running
maximum, drop anything below it, reverse back. That's O(n) and O(1) space, and it is a
legitimately better answer than the stack; the stack version is the one that shows the
pattern.

## 💡 The pattern reveal
**Signal:** remove elements that have a bigger one to the right · keep the rest, in order.
**Therefore:** a monotonic decreasing stack **whose survivors are the output**.

**Key insight:** compare with EP61 and EP62. All three keep a decreasing stack and pop
when a bigger element arrives. What differs is **what you do with the two groups**:

| episode | the popped elements | the survivors |
|---|---|---|
| EP61 next greater | get their answer written | get the default `-1` |
| EP62 daily temps | get their distance written | get `0` |
| **EP63 (today)** | **are deleted** | **are the answer** |

Same invariant, opposite focus. Saying that in an interview is worth more than the code.

**🧨 The trap: the survivors' `.next` pointers are stale.** Node `5` still points at
node `2` even after `2` has been popped, so you cannot just return the bottom of the
stack and walk it. Relink the survivors in order at the end:

```python
dummy = ListNode(0)
node = dummy
for n in stack:            # bottom to top == left to right
    node.next = n
    node = n
node.next = None           # belt and braces -- see below
```

**A detail worth getting right rather than repeating.** It's tempting to say that final
`node.next = None` is what stops the deleted nodes reappearing. It isn't: the last
element of the stack is **always the original last node**: it's pushed last and nothing
after it can pop it, so its `next` is already `None`. I checked by deleting the line
and running 3000 random lists against a brute-force reference: **zero** differences.

Keep the line anyway (it costs nothing and it makes the invariant explicit), but know
which line is actually load-bearing: it's the **relinking loop**, which repairs the
stale pointers of every *intermediate* survivor.

## 🔍 Dry run: `5 -> 2 -> 13 -> 3 -> 8`

| node | pops (deleted) | stack after |
|---|---|---|
| `5` | - | `[5]` |
| `2` |, (2 < 5) | `[5, 2]` |
| `13` | **pop 2, pop 5** | `[13]` |
| `3` |, (3 < 13) | `[13, 3]` |
| `8` | **pop 3** | `[13, 8]` |

Survivors `[13, 8]` → relink → **`13 -> 8`** ✓

The `13` row is the cascade: one node removes two, and it doesn't matter that `5` was
never adjacent to `13`, being *anywhere* to the right is the rule, and the stack
enforces it automatically.

## 🔍 Dry run: `1 -> 1 -> 1 -> 1` (the strictness test)

| node | `stack[-1] < val`? | pops | stack |
|---|---|---|---|
| `1` | - | - | `[1]` |
| `1` | 1 < 1 ✗ | - | `[1, 1]` |
| `1` | ✗ | - | `[1, 1, 1]` |
| `1` | ✗ | - | `[1, 1, 1, 1]` |

Answer **`1 -> 1 -> 1 -> 1`** ✓, nothing is removed, because nothing is *strictly*
greater. Swap `<` for `<=` and you get a single `1`.

## ✅ Optimal solution
```python
class Solution:
    def removeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Remove every node that has a strictly greater node to its right.

        Time:  O(n), each node is pushed once and popped at most once.
        Space: O(n), the stack of survivors.
        """
        stack = []                          # survivors so far, values DECREASING

        cur = head
        while cur:
            # anything smaller than me now has something bigger to its right
            while stack and stack[-1].val < cur.val:
                stack.pop()
            stack.append(cur)
            cur = cur.next

        # the survivors' .next pointers are stale -- relink them in order
        dummy = ListNode(0)
        node = dummy
        for n in stack:
            node.next = n
            node = n
        node.next = None                    # terminate, or the deleted tail comes back

        return dummy.next
```
**Time:** O(n) · **Space:** O(n)

## ⚠️ Gotchas
- **The relinking loop is the part that matters**, not the terminator. Every surviving
  node's `next` may point at something that was popped, and the loop is what repairs it.
  The trailing `node.next = None` is defensive only, the last survivor is always the
  original tail, so it already terminates. (Verified: removing it changes nothing on
  3000 random lists.)
- **`<`, not `<=`.** Strictly greater. `[1,1,1,1]` is the test.
- **Push nodes, not values.** You have to rebuild a list of the original nodes at the
  end; a stack of ints can't be relinked.
- **Iterate the stack bottom to top** (`for n in stack`), it's already in left-to-right
  order. Popping it would reverse the list.
- **The reverse-and-max version is O(1) space** and worth naming; if the interviewer
  asks for constant space, that's the answer, and it reuses EP52's reversal.
- **An empty list** produces an empty stack, `dummy.next` is `None`, which is correct,
  but note `node.next = None` runs on the dummy itself, harmlessly.

## 🎤 Interview talking points
- *"It's a next-greater-element sweep, but I keep the survivors instead of recording the
  answers, a decreasing stack, and anything a bigger node clears out is deleted."*
- *"The survivors' `next` pointers are stale afterwards, they point at deleted nodes,
  so I relink them in order. The last survivor is necessarily the original tail, so it
  already terminates."* ← the detail that makes it a linked-list problem, stated
  precisely rather than superstitiously.
- *"Strictly greater, so equal values all survive."*
- *"There's an O(1)-space version: reverse, sweep keeping a running max, reverse back.
  Same answer, more passes."* ← offering the better-space alternative unprompted.

## 🔗 Transfer
That closes the pure monotonic trio. The next two episodes go back to cancelling stacks
with more state on them, EP64 stacks `[char, count]` pairs, EP65 stacks path segments,
before EP66 brings the monotonic idea back one last time, with a budget attached to the
pops.

## 📹 Metadata
- **Title:** `Remove Nodes From Linked List, keep the survivors | Stack #6`
- **Thumbnail:** `THE STACK IS THE LIST` (green block)
- **Short:** `13` clearing two nodes at once, then the relink. 45s.
