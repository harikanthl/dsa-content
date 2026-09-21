# Pattern 07 — In-place Reversal of a LinkedList

**6 episodes · EP 52–57**

---

## The one-sentence version

Reversing a linked list is **three pointers and one fixed order of assignment** — save
the next node, flip the current one backwards, step both forward — and every harder
variant is that same loop wrapped in bookkeeping about the node **before** the block and
the node **after** it: **O(n) time, O(1) space**, no new nodes ever allocated.

## ELI5

You're walking a chain of nodes, and each link points forward. To reverse it you flip
each link to point backwards instead — but the instant you flip one, you've **destroyed
your only way forward**. So you save it first:

```
      prev      cur       nxt
       |         |         |
  ... [3]  <--  [4]  -->  [5] --> ...
                 ^
       1. nxt = cur.next     save the way forward  (or you're stranded)
       2. cur.next = prev    flip this link
       3. prev = cur         the flipped node becomes the new "behind me"
       4. cur = nxt          step forward
```

Four lines, always in that order. When `cur` falls off the end, `prev` is standing on
the last node it flipped — which is the **new head**.

```python
prev = None
cur = head
while cur:
    nxt = cur.next      # save
    cur.next = prev     # flip
    prev = cur          # advance prev
    cur = nxt           # advance cur
return prev             # NOT head -- head is now the tail
```

`return prev` is the line people get wrong. `head` still exists, but it's the last node
now, and returning it gives you a one-element list.

## How to recognise it

| Signal | Example |
|---|---|
| "reverse" + a linked list | Reverse a LinkedList (EP52) |
| reverse **part** of a list, given positions | Reverse a Sub-list (EP53) |
| "in pairs", "every k nodes", "in groups" | EP54, EP55, EP56 |
| "**in-place**" or "O(1) extra space" stated | rules out copying to an array |
| the list is rearranged but no values change | Rotate a LinkedList (EP57) |

**The tell that this is not the pattern:** if you're allowed O(n) space, dumping the
values into a Python list, rearranging, and rebuilding is legitimate, shorter, and
easier to get right. The whole point of these six episodes is the O(1)-space version, so
say the array version out loud, then say why you're not writing it.

## The shape

Every episode after EP52 reverses a **block** in the middle of a list, and every one of
them needs the same four nodes:

```
  before -> [ first ... last ] -> after
              ^block starts      ^block ends

  after reversing the block:

  before -> [ last ... first ] -> after
     |         ^new head          ^
     |         |                  |
     +-- before.next = last       first.next = after
```

Two rewires, and the trap is that **the block's old first node becomes its tail**, so
you must have saved `after` *before* the reversal destroyed the link to it.

```python
dummy = ListNode(0, head)     # so "before" always exists, even at position 1
before = dummy
...
tail = before.next            # the old first node -- it will BE the tail
before.next = new_head
tail.next = after
```

**The dummy node is not optional decoration.** The head changes in five of these six
problems, and every "is this the first node?" special case disappears the moment a fake
node sits in front of the real one. Allocate it, wire `dummy.next = head`, return
`dummy.next` at the end.

## The three shapes you need

### 1. Reverse the whole thing (EP52)

The four-line loop, `return prev`. Everything else is built from it.

### 2. Reverse one block, given its boundaries (EP53, EP57)

Walk to `before`, reverse exactly the right number of nodes, rewire the two ends. The
boundaries come from the problem: positions in EP53, a computed offset in EP57.

### 3. Reverse every block, marching down the list (EP54, EP55, EP56)

The loop above, run repeatedly, with `before` advancing to the block's **new tail** each
time — which is the node you were holding *before* the reversal:

```python
group_prev = dummy
while <another block exists>:
    ...reverse the block...
    tail = group_prev.next     # old head, now the tail
    group_prev.next = new_head
    group_prev = tail          # the next block hangs off here
```

Getting `group_prev` wrong doesn't crash — it silently loses everything after the first
group, or builds a **cycle**. Print the list after each group when debugging; an
infinite loop in the print is the diagnosis.

### And the one that isn't a reversal at all (EP57)

Rotation moves nodes without flipping a single link. Close the list into a **ring**,
walk to the new tail, cut. It's in this pattern because it's the same pointer
bookkeeping, and because it's the one where people reflexively reverse something and
can't say why.

## Complexity

| Problem | Time | Space |
|---|---|---|
| all six episodes | O(n) | **O(1)** — a handful of pointers |
| EP55, EP56 | O(n) — each node is visited a constant number of times | O(1) |
| the array version you're beating | O(n) | O(n) |

If your solution allocates anything per node, it isn't this pattern.

## The episodes

| EP | Problem | Shape | The thing it teaches |
|---|---|---|---|
| 52 | Reverse a LinkedList | whole list | The four lines, the order, and `return prev`. |
| 53 | Reverse a Sub-list | one block | The dummy node and the two rewires. |
| 54 | Reverse List in Pairs | every block | Blocks of two, and the odd leftover. |
| 55 | Reverse every K-element Sub-list | every block | Check the block is *full* before touching it. |
| 56 | Reverse nodes in Even Length Groups | every block | The block size varies, and only some blocks flip. |
| 57 | Rotate a LinkedList | ring + cut | Not a reversal. `k %= n`, and count from the front. |

## What "knowing this in your sleep" means

1. Why save `nxt` before flipping? *(`cur.next = prev` destroys the only pointer to the
   rest of the list.)*
2. What do you return from the reversal loop, and why? *(`prev` — when `cur` is null,
   `prev` is the last flipped node, i.e. the new head. `head` is now the tail.)*
3. What is the dummy node for? *(So "the node before the block" always exists, even when
   the block starts at position 1 — it deletes every head special case.)*
4. After reversing a block, which node is its tail? *(The one that was its head. Wire
   that node to whatever followed the block, and wire `before` to the new head.)*
5. Why is rotation in this pattern if nothing is reversed? *(Same pointer surgery: close
   the ring, walk `n − k%n` steps, cut. The instinct to reverse is wrong and worth
   naming.)*
