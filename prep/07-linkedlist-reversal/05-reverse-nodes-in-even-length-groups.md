# EP056 · P07E05 · Reverse Nodes in Even Length Groups   [Hard]

**Pattern:** In-place Reversal of a LinkedList · **Link:** https://leetcode.com/problems/reverse-nodes-in-even-length-groups/

---

## 🎬 Hook
> "Split the list into groups of 1, 2, 3, 4, … and reverse only the groups with an
> **even** number of nodes. The machinery is yesterday's, unchanged. What's new is that
> the last group can be short, so a group nominally of size 5 might really be 3, and
> whether it gets reversed depends on the **actual** count, not the intended one.
> Everything hinges on that distinction."

## 📋 Problem, in your words
```
The list is divided into groups whose lengths follow 1, 2, 3, 4, 5, ...
in order. The FINAL group may be shorter than its nominal length -- it
just takes whatever nodes are left.

Reverse the nodes of every group whose ACTUAL length is even. Leave the
odd-length groups alone. Return the head.
```

## 🔢 The example
```
Input:  5 -> 2 -> 6 -> 3 -> 9 -> 1 -> 7 -> 3 -> 8 -> 4      (10 nodes)
groups: [5] [2,6] [3,9,1] [7,3,8,4]
sizes:   1    2      3        4
         odd even   odd     even
Output: 5 -> 6 -> 2 -> 3 -> 9 -> 1 -> 4 -> 8 -> 3 -> 7

Input:  1 -> 1 -> 0 -> 6
groups: [1] [1,0] [6]        <- last group WANTED 3 nodes, only got 1
sizes:   1    2     1
Output: 1 -> 0 -> 1 -> 6

Input:  2 -> 1
groups: [2] [1]              <- last group wanted 2, got 1: ODD, so untouched
Output: 2 -> 1
```
Those last two examples are the episode. `[6]` and `[1]` are short final groups whose
*real* length is odd, so nothing happens to them, even though the group they belong to
was supposed to be even-sized in one case.

## 🧸 ELI5
> March down the list carrying a counter: this group wants 1 node, the next wants 2,
> then 3, then 4…
>
> ```
>  want 1   want 2     want 3        want 4
>   [5]     [2,6]     [3,9,1]      [7,3,8,4]
>    |        |          |             |
>   odd     EVEN        odd          EVEN
>   keep    flip        keep         flip
> ```
>
> At each group, **count what you actually got** before deciding anything. The list runs
> out when it runs out, the final group takes the remainder, which may be less than it
> wanted.
>
> Then one question: *is the count I actually got even?* If yes, reverse exactly that
> many nodes. If no, walk past them, untouched.

## 🐌 Brute force (say it, don't type it)
Values into an array, slice it into 1, 2, 3, … chunks, reverse the even-length ones,
write back. **O(n) space** and much easier to reason about, genuinely the right answer
if someone hands you this in production. The pointer version is the exercise.

## 💡 The pattern reveal
**Signal:** groups of **varying** size · a condition deciding which groups change.
**Therefore:** EP55's loop with two changes, measure the real length, and make the
reversal conditional.

**Key insight, nominal vs actual length.** This is the only genuinely new idea in the
episode, and it deserves to be said twice:

```python
node, length = group_prev.next, 0
while node and length < size:      # stop at the list's end OR the group's size
    length += 1
    node = node.next
# `length` is what we ACTUALLY got; `node` is the node after the group
```

`size` is what the group wanted. `length` is what it got. The reversal decision uses
`length % 2 == 0`, **never** `size % 2 == 0`.

The two readings agree far more often than they disagree, which is why the bug survives.
On `[1,1,0,6]` the last group wants 3 and gets 1, odd either way, same answer. The
smallest input that separates them is five nodes:

```
1 -> 2 -> 3 -> 4 -> 5    groups [1] [2,3] [4,5]
                         the last one WANTED 3 and got 2
  length % 2  ->  2 is even  ->  reverse  ->  1 -> 3 -> 2 -> 5 -> 4   ✓
  size   % 2  ->  3 is odd   ->  leave    ->  1 -> 3 -> 2 -> 4 -> 5   ✗
```

**And notice what else that walk gives you:** `node` is the node *after* the group,
exactly the `group_next` sentinel EP55 needed. One walk, two facts, again.

**🧨 The trap: advancing `group_prev` in the odd case.** When a group is reversed, the
bookkeeping is EP55's, `group_prev` moves to the old head. When a group is **not**
reversed, you must still walk `group_prev` past it, one node at a time:

```python
else:
    for _ in range(length):
        group_prev = group_prev.next
```

Forget that branch and `group_prev` sits still while `size` keeps growing, you'll
re-measure the same nodes with a bigger size each round, and the output is quietly
wrong (or the loop never terminates).

## 🔍 Dry run: `5 -> 2 -> 6 -> 3 -> 9 -> 1 -> 7 -> 3 -> 8 -> 4`
`group_prev = dummy`, `size = 1`.

| round | `size` | nodes in group | actual `length` | even? | action | list after |
|---|---|---|---|---|---|---|
| 1 | 1 | `[5]` | 1 | ✗ | walk past | `5 · 2 6 3 9 1 7 3 8 4` |
| 2 | 2 | `[2, 6]` | 2 | **✓** | **reverse** → `6, 2` | `5 · 6 2 · 3 9 1 7 3 8 4` |
| 3 | 3 | `[3, 9, 1]` | 3 | ✗ | walk past | unchanged |
| 4 | 4 | `[7, 3, 8, 4]` | 4 | **✓** | **reverse** → `4, 8, 3, 7` | `5 · 6 2 · 3 9 1 · 4 8 3 7` |
| 5 | 5 | - | `group_prev.next` is `None` | - | loop ends | - |

Answer **`5 -> 6 -> 2 -> 3 -> 9 -> 1 -> 4 -> 8 -> 3 -> 7`** ✓

## 🔍 Dry run: `1 -> 1 -> 0 -> 6` (the short final group)

| round | `size` | group | actual `length` | even? | action |
|---|---|---|---|---|---|
| 1 | 1 | `[1]` | 1 | ✗ | walk past |
| 2 | 2 | `[1, 0]` | 2 | **✓** | **reverse** → `0, 1` |
| 3 | 3 | `[6]` | **1** ← wanted 3, got 1 | ✗ | walk past |

Answer **`1 -> 0 -> 1 -> 6`** ✓

Say the third row out loud: *"this group wanted three nodes and got one; one is odd, so
nothing happens."*

Note that `size % 2` gives the **same** answer on this input, both readings call the
last group odd. To show the bug on camera you need an input where they disagree, and
`1..9` is the clearest:

```
1..9   groups [1] [2,3] [4,5,6] [7,8,9]      the last WANTED 4 and got 3
  length % 2  ->  1 -> 3 -> 2 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9   ✓
  size   % 2  ->  1 -> 3 -> 2 -> 4 -> 5 -> 6 -> 9 -> 8 -> 7   ✗ reversed a group of 3
```

## ✅ Optimal solution
```python
class Solution:
    def reverseEvenLengthGroups(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Groups of size 1, 2, 3, ...; reverse those whose ACTUAL length is even.

        Time:  O(n), each node is measured once and reversed at most once.
        Space: O(1).
        """
        dummy = ListNode(0, head)
        group_prev = dummy
        size = 1

        while group_prev.next:
            # 1. how many nodes did this group ACTUALLY get?
            node, length = group_prev.next, 0
            while node and length < size:
                length += 1
                node = node.next
            # `node` is now the node after the group -- the sentinel

            if length % 2 == 0:              # ACTUAL length, never `size`
                # 2. reverse the group, stopping at the sentinel (EP55's trick)
                group_next = node
                prev, cur = group_next, group_prev.next
                while cur is not group_next:
                    nxt = cur.next
                    cur.next = prev
                    prev = cur
                    cur = nxt

                tail = group_prev.next       # old head == new tail
                group_prev.next = prev       # new head
                group_prev = tail
            else:
                # 3. odd: leave it, but still walk past it
                for _ in range(length):
                    group_prev = group_prev.next

            size += 1

        return dummy.next
```
**Time:** O(n) · **Space:** O(1)

## ⚠️ Gotchas
- **`length % 2`, not `size % 2`.** The final group's real length is the one that
  decides. This is the bug this problem exists to catch.
- **The odd branch still advances `group_prev`.** By `length` nodes, one at a time.
  Omitting it re-processes the same nodes with a growing `size`.
- **The measuring loop needs both conditions**: `node and length < size`, to stop at
  the end of the list *or* the end of the group.
- **`group_prev.next = prev`** in the reversed branch (`prev` is the new head), and
  `tail` must be saved before that assignment. Same discipline as EP55.
- **`size` increments every round**, reversed or not. It's the group index, not a
  measure of progress through the list.
- **A single-node list** returns immediately: group 1 has length 1, odd, walk past,
  `group_prev.next` is `None`, done.

## 🎤 Interview talking points
- *"Group sizes are 1, 2, 3, … but the last group takes what's left, so I measure the
  actual length before deciding, and the measuring walk also gives me the node after
  the group."* ← the whole answer.
- *"The reversal is the k-group reversal with the sentinel seed; only the decision and
  the group size changed."* ← names the reuse.
- *"The odd case still has to advance my group pointer past those nodes."*
- *"Every node is measured once and flipped at most once, so O(n), O(1) space."*

## 🔗 Transfer
That's the reversal family complete: whole list, one block, fixed blocks, growing
blocks. Tomorrow (EP57) closes Pattern 07 with the problem that *looks* like it belongs
and isn't, rotation reverses nothing at all. It's here to test whether you recognise
the pattern or just pattern-match on the words "linked list" and "rearrange".

## 📹 Metadata
- **Title:** `Reverse Nodes in Even Length Groups, count what you GOT | LinkedList Reversal #5`
- **Thumbnail:** `ACTUAL ≠ NOMINAL` (green block)
- **Short:** `1..9`, `length % 2` vs `size % 2`, the last three nodes flipped or not. 50s.
