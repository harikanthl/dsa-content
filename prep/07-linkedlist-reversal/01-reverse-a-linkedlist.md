# EP052 · P07E01 · Reverse a LinkedList   [Easy]

**Pattern:** In-place Reversal of a LinkedList · **Link:** https://leetcode.com/problems/reverse-linked-list/

---

## 🎬 Hook
> "Four lines of code, and they only work in one order. The moment you flip a node's
> pointer backwards you have destroyed your only route to the rest of the list — so the
> first line saves it. Everybody can recite this loop; today is about being able to
> *derive* it, because the next five episodes are this loop with bookkeeping around it."

## 📋 Problem, in your words
```
Given the head of a singly linked list, reverse it IN PLACE and return
the new head.

In place: rewire the existing nodes. No new nodes, no array of values,
O(1) extra space.
```

## 🔢 The example
```
Input:  1 -> 2 -> 3 -> 4 -> 5 -> None
Output: 5 -> 4 -> 3 -> 2 -> 1 -> None

Input:  1 -> 2 -> None     -> 2 -> 1 -> None
Input:  None               -> None          <- empty list, no special case needed
Input:  1 -> None          -> 1 -> None
```

## 🧸 ELI5
> Picture a line of people, each with a hand on the shoulder of the person in front. To
> reverse the line, each person lets go and grabs the shoulder of the person **behind**
> them instead.
>
> But the instant you let go of the person in front, you can't reach them any more. So
> before you let go, you **remember who they are**:
>
> ```
>        prev        cur         nxt
>         |           |           |
>  None  [1]   <--   [2]   -->   [3] -> [4] -> [5]
>                     ^
>   1. nxt = cur.next     remember the way forward
>   2. cur.next = prev    let go, grab backwards
>   3. prev = cur         I am now the one behind
>   4. cur = nxt          walk to the person I remembered
> ```
>
> Repeat until `cur` walks off the end. Where's the new head? It's `prev` — the last
> person you flipped. The original head is now standing at the **back** of the line.

## 🐌 Brute force (say it, don't type it)
Walk the list into a Python list, reverse it, rebuild (or just rewrite the values).
**O(n) time, O(n) space** — and for a linked list, allocating a parallel array is
precisely what the question is testing you *not* to do. Say it in one sentence, name the
space cost, move on.

## 💡 The pattern reveal
**Signal:** a singly linked list · "reverse" · in place / O(1) space.
**Therefore:** three pointers, one pass.

**Key insight:** you need exactly three pieces of state and no more:

| pointer | means |
|---|---|
| `prev` | the part already reversed — starts as `None`, ends as the answer |
| `cur` | the node being flipped right now |
| `nxt` | the untouched remainder, saved before the flip destroys the link |

**🧨 The two traps of this episode.**

1. **Order.** `cur.next = prev` before `nxt = cur.next` loses the rest of the list
   instantly — you end up with a two-node list and no error message.
2. **`return prev`, not `return head`.** When the loop ends, `cur` is `None` and `prev`
   is the last node flipped. `head` is still a valid node — it's the **tail** now — so
   returning it gives you `1 -> None` and a wrong answer that looks almost right.

And the reason `prev` starts at `None`: the old head becomes the new tail, and a tail
points at nothing. Seeding `prev = head` builds a **cycle**, which hangs the next thing
that walks the list.

## 🔍 Dry run — `1 -> 2 -> 3 -> None`

| step | `prev` | `cur` | `nxt` | list after the flip |
|---|---|---|---|---|
| start | `None` | `1` | — | `1 -> 2 -> 3 -> None` |
| 1 | `1` | `2` | `2` | `None <- 1`, `2 -> 3 -> None` |
| 2 | `2` | `3` | `3` | `None <- 1 <- 2`, `3 -> None` |
| 3 | `3` | `None` | `None` | `None <- 1 <- 2 <- 3` |

`cur` is `None`, so stop. `prev` is `3` → **return `3`**, and reading forward from it
gives `3 -> 2 -> 1 -> None` ✓

Narrate row 1 slowly on camera: after `cur.next = prev`, node `1` points at `None` — it
is *already* the tail, on the very first iteration. Everything after that is repetition.

## ✅ Optimal solution
```python
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Reverse a singly linked list in place.

        Time:  O(n) — each node is visited once.
        Space: O(1) — three pointers, nothing allocated.
        """
        prev = None          # the reversed part; the old head will point here
        cur = head

        while cur:
            nxt = cur.next       # 1. save the way forward -- before destroying it
            cur.next = prev      # 2. flip this link backwards
            prev = cur           # 3. this node is now the reversed part
            cur = nxt            # 4. step into what we saved

        return prev          # NOT head -- head is the tail now
```
**Time:** O(n) · **Space:** O(1)

**The one-liner you'll see in other people's code** — same four steps, evaluated
right-hand side first:

```python
while cur:
    cur.next, prev, cur = prev, cur, cur.next
```
It's the idiom used back in EP18's palindrome check. Know it, be able to expand it into
the four lines, and prefer the four lines on camera — the order is the lesson.

## ⚠️ Gotchas
- **`nxt = cur.next` must come first.** The other three lines can be re-derived; this
  one is the whole trick.
- **`return prev`.** If your output is a single node, this is why.
- **`prev = None` to start.** `prev = head` makes a cycle (`head.next = head`), and the
  test harness hangs rather than failing cleanly.
- **Empty list works with no guard**: `cur = None`, the loop never runs, `prev = None`
  is returned. Check it rather than adding `if not head`.
- **Single node works too**: one flip, `1 -> None`, `prev = 1`. Two free test cases.
- **Don't touch `.val`.** Rewriting values instead of pointers is a different (and for a
  singly linked list, much worse) algorithm.

## 🎤 Interview talking points
- *"Three pointers: what's reversed, what I'm flipping, and what's left. The first line
  of the loop saves the remainder, because the second line destroys the link to it."*
- *"I return `prev`, because when `cur` falls off the end, `prev` is the last node I
  flipped — the new head."*
- *"O(n) time, O(1) space. Copying into an array is O(n) space and defeats the point of
  the question."*
- *"There's a recursive version — reverse the tail, then make `head.next.next = head` —
  but it's O(n) stack, so I'd only write it if you want to see recursion."* ← knowing
  its cost is the point.

## 🔗 Transfer
This loop is the whole pattern. EP53 runs it on a **slice** of the list, which needs a
dummy node and two rewires; EP54 and EP55 run it repeatedly on fixed-size blocks; EP56
runs it on blocks that grow. Tomorrow (EP53) introduces the four-node picture —
`before`, first, last, `after` — that every remaining episode uses.

## 📹 Metadata
- **Title:** `Reverse a Linked List — four lines, one order | LinkedList Reversal #1`
- **Thumbnail:** `SAVE · FLIP · ADVANCE` (green block)
- **Short:** flipping the first link before saving `next`, and watching the list vanish. 40s.
