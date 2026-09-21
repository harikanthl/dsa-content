# EP054 · P07E03 · Reverse List in Pairs   [Medium]

**Pattern:** In-place Reversal of a LinkedList · **Link:** https://leetcode.com/problems/swap-nodes-in-pairs/

---

## 🎬 Hook
> "Swap every two adjacent nodes. Blocks of size two are small enough that you can skip
> the reversal loop entirely and just rewire three pointers by hand — which makes this
> the cleanest possible place to learn the *other* half of the bookkeeping: after you
> finish a block, where does `before` move to? Get that wrong and you build a cycle."

## 📋 Problem, in your words
```
Given the head of a linked list, swap every two adjacent nodes and
return the head.

Swap the NODES, not the values -- rewiring is the exercise. If the list
has an odd number of nodes, the last one stays where it is.
```

## 🔢 The example
```
Input:  1 -> 2 -> 3 -> 4      Output: 2 -> 1 -> 4 -> 3
Input:  1 -> 2 -> 3           Output: 2 -> 1 -> 3        <- odd: the 3 is left alone
Input:  1                     Output: 1
Input:  None                  Output: None
```

## 🧸 ELI5
> Take the first two nodes and make them change places. The tricky part is that **three**
> links change, not one:
>
> ```
> before -> [ a -> b ] -> rest
>
>    1. a.next = b.next     a now points at `rest`      (a is going to the back)
>    2. b.next = a          b points at a               (the swap itself)
>    3. before.next = b     the list runs into b first  (b is going to the front)
>
> before -> [ b -> a ] -> rest
> ```
>
> Then — and this is the bit people drop — the **next** pair hangs off `a`, because `a`
> is now the second node of this pair. So `before = a`, not `before = b`, and definitely
> not `before = before.next` after the rewire.
>
> ```
> dummy -> 2 -> 1 -> 3 -> 4
>               ^ before for the next round
> ```

## 🐌 Brute force (say it, don't type it)
Walk the list swapping `.val` in pairs. **O(n) time, O(1) space** — and it genuinely
works here. Say it, then say why it's not the answer: the problem explicitly asks for
node swaps, and in real code the nodes may carry more than a single value (or be
immutable). This is one of the few episodes where the "wrong" answer is worth
articulating properly, because the reason is engineering, not complexity.

## 💡 The pattern reveal
**Signal:** reverse/swap in **fixed-size groups** · linked list · in place.
**Therefore:** dummy node, loop, three rewires per pair, advance `before` to the pair's
new tail.

**Key insight:** a block of two doesn't need the reversal loop. It needs three
assignments, in an order where nothing is read after it's overwritten:

```python
a = prev.next
b = a.next

a.next = b.next      # a points past the pair FIRST -- b.next is still intact
b.next = a           # now the swap
prev.next = b        # and the list joins at b

prev = a             # a is the pair's tail: next pair starts after it
```

**The loop condition is the other half of the correctness:**

```python
while prev.next and prev.next.next:      # a full pair remains
```

Two checks, and both are needed: `prev.next` may be `None` (list exhausted), and
`prev.next.next` may be `None` (an odd node left over, which must be left alone). Drop
the second and an odd-length list raises `AttributeError: 'NoneType' object has no
attribute 'next'`.

**🧨 The trap: `prev = a`.** After the swap, the pair reads `b -> a`, so `a` is its
tail. Writing `prev = b` puts you back at the front of the pair you just swapped and the
loop swaps it again, forever — the classic infinite loop of this pattern. If your test
run hangs, this line is why.

## 🔍 Dry run — `1 -> 2 -> 3 -> 4`
`dummy -> 1 -> 2 -> 3 -> 4`, `prev = dummy`.

**Round 1** — `a = 1`, `b = 2`:

| step | assignment | list now |
|---|---|---|
| 1 | `a.next = b.next` → `1 -> 3` | `dummy -> 1 -> 3 -> 4`, with `2 -> 3` |
| 2 | `b.next = a` → `2 -> 1` | `2 -> 1 -> 3 -> 4` |
| 3 | `prev.next = b` → `dummy -> 2` | `dummy -> 2 -> 1 -> 3 -> 4` ✓ |
| 4 | `prev = a` | `prev` is node `1` |

**Round 2** — `prev.next = 3` and `prev.next.next = 4`, so a full pair remains.
`a = 3`, `b = 4`:

| step | assignment | list now |
|---|---|---|
| 1 | `a.next = b.next` → `3 -> None` | `... 3 -> None`, with `4 -> None`… |
| 2 | `b.next = a` → `4 -> 3` | `4 -> 3 -> None` |
| 3 | `prev.next = b` → `1 -> 4` | `dummy -> 2 -> 1 -> 4 -> 3` ✓ |
| 4 | `prev = a` | `prev` is node `3` |

**Round 3** — `prev.next` is `None`, so the loop stops.

Answer **`2 -> 1 -> 4 -> 3`** ✓

## 🔍 Dry run — `1 -> 2 -> 3` (the odd leftover)
Round 1 swaps to `dummy -> 2 -> 1 -> 3`, `prev = 1`. Round 2 checks:
`prev.next` is node `3` ✓, `prev.next.next` is `None` ✗ → **stop**.

Answer **`2 -> 1 -> 3`** ✓ — the lone `3` is untouched, which is exactly what the second
half of the loop condition is for.

## ✅ Optimal solution
```python
class Solution:
    def swapPairs(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Swap every two adjacent NODES (not values), in place.

        Time:  O(n) — each node is rewired once.
        Space: O(1) — a dummy node and three pointers.
        """
        dummy = ListNode(0, head)
        prev = dummy

        while prev.next and prev.next.next:     # a FULL pair remains
            a = prev.next
            b = a.next

            a.next = b.next      # read b.next before anything overwrites it
            b.next = a           # the swap
            prev.next = b        # the list now enters the pair at b

            prev = a             # `a` is the pair's tail -- next pair starts after it

        return dummy.next
```
**Time:** O(n) · **Space:** O(1)

## ⚠️ Gotchas
- **`prev = a`, never `prev = b`.** `prev = b` re-swaps the same pair forever. A hang,
  not a wrong answer.
- **Both halves of the loop condition.** `prev.next` for the end of the list,
  `prev.next.next` for the odd node. One without the other either crashes or drops a
  node.
- **`a.next = b.next` first.** Reverse the order and `b.next` has already become `a`, so
  `a.next = a` — a one-node cycle.
- **Swap nodes, not values.** Say why: the problem asks for it, and node payloads aren't
  always a single mutable int.
- **`return dummy.next`** — the head always changes for any list of length ≥ 2.
- **Empty and single-node lists** fall straight through the loop and return correctly.
  No guards needed; verify rather than add them.

## 🎤 Interview talking points
- *"Blocks of two are small enough to rewire directly: point `a` past the pair, point
  `b` at `a`, point the previous node at `b`."*
- *"After the swap, `a` is the pair's tail, so that's where the next pair hangs from."*
  ← the line that separates working code from an infinite loop.
- *"The loop condition checks for a **full** pair, which is also how the odd leftover
  gets left alone."*
- *"I could swap the values in two lines, but the question asks for node swaps and real
  nodes carry more than one field."*

## 🔗 Transfer
This is the k = 2 case of tomorrow's problem. EP55 generalises it to blocks of any `k`,
where "rewire three pointers by hand" stops being practical and EP52's reversal loop
comes back — but the `before`-moves-to-the-block's-tail bookkeeping you just learned is
identical, and so is the "only touch a **full** block" rule.

## 📹 Metadata
- **Title:** `Swap Nodes in Pairs — where does the previous pointer go? | LinkedList Reversal #3`
- **Thumbnail:** `PREV = A, NOT B` (red block)
- **Short:** `prev = b` and the infinite loop it causes, live. 40s.
