# EP017 · P02E05 · Middle of the LinkedList   [Easy]

**Pattern:** Fast & Slow Pointers · **Link:** https://leetcode.com/problems/middle-of-the-linked-list/

---

## 🎬 Hook
> "You can't ask a linked list how long it is. So how do you find its middle without
> walking it twice? You send a second runner at double speed, when he hits the end,
> the slow one is standing exactly halfway. One pass, no counting."

## 📋 Problem, in your words
```
Given the head of a singly linked list, return the middle node.

If there are two middle nodes (even length), return the SECOND one.
```

## 🔢 The example
```
Input:  1 -> 2 -> 3 -> 4 -> 5
Output:           3 -> 4 -> 5        (the node 3, and everything after it)

Input:  1 -> 2 -> 3 -> 4 -> 5 -> 6
Output:                4 -> 5 -> 6   (the SECOND middle, 4, not 3)
```

## 🧸 ELI5
> Two people start at the front of a queue. One walks, one runs at double speed.
>
> When the runner reaches the back of the queue, how far has the walker got? Exactly
> half as far, because he's been moving at exactly half the speed for exactly the
> same amount of time.
>
> Half the distance is the middle. You didn't count anybody.

That's it. This is the shortest episode in the pattern, and it's worth doing carefully
because the next two episodes are built entirely on top of it.

## 🐌 Brute force (say it, don't type it)
Walk the list once to count the nodes; walk again to node `count // 2`.

```python
n = 0
cur = head
while cur: n += 1; cur = cur.next
cur = head
for _ in range(n // 2): cur = cur.next
return cur
```

**O(n) time, O(1) space**: and honestly, this is fine. It's the same complexity class
as the optimal answer. The two-pointer version is better because it's **one pass**,
which matters when the data is a stream you can only read once, and because it's the
building block the next two problems need.

Say that distinction out loud: *"both are O(n); I prefer the two-pointer one because
it's single-pass and it composes."*

## 💡 The pattern reveal
**Signal:** find the middle of a linked list · one pass · O(1) space.
**Therefore:** Fast & Slow pointers, Shape C.

**Key insight:** position is time × speed. Run two pointers for the same duration at
speeds 1 and 2, and when the fast one has covered the whole list, the slow one has
covered exactly half of it. The middle falls out of the arithmetic; you never measure
anything.

## 🔍 Dry run: odd length, `1 → 2 → 3 → 4 → 5`
Loop condition is `while fast and fast.next`.

| step | slow | fast | `fast and fast.next`? |
|---|---|---|---|
| start | 1 | 1 | yes |
| 1 | 2 | 3 | yes |
| 2 | **3** | **5** | `fast.next` is `None` → stop |

Return `slow` = **3**. ✓ (Odd length always lands cleanly on the single middle.)

## 🔍 Dry run: even length, `1 → 2 → 3 → 4 → 5 → 6`
| step | slow | fast | `fast and fast.next`? |
|---|---|---|---|
| start | 1 | 1 | yes |
| 1 | 2 | 3 | yes |
| 2 | 3 | 5 | yes |
| 3 | **4** | `None` | `fast` is `None` → stop |

Return `slow` = **4**: the *second* middle, which is what this problem wants. ✓

Put these two tables side by side on screen. The same four lines of code produce both
answers, and knowing which one you get is the whole skill.

## ✅ Optimal solution
```python
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Return the middle node; the second middle when the length is even.

        Time:  O(n), fast traverses the list once, slow does half of it.
        Space: O(1), two references.
        """
        slow = fast = head

        while fast and fast.next:    # fast takes two steps, so both must exist
            slow = slow.next
            fast = fast.next.next

        return slow                  # fast at the end => slow at the middle
```
**Time:** O(n) · **Space:** O(1) ✓

### The variant you must be able to produce on demand
To return the **first** middle of an even list (`[1,2,3,4] → 2` instead of `3`), start
the fast pointer one node ahead:

```python
slow, fast = head, head.next     # <- the only change
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow
```

Neither is "the right answer", the problem decides. Say which one you're writing and
why, every time. This one-line difference is the single most common bug in episodes 18
and 19, so burn it in now.

## ⚠️ Gotchas
- **`while fast and fast.next`**: the same two-link dereference as EP13. `while fast`
  alone crashes on even-length lists.
- **Second vs first middle.** `fast = head` gives the second; `fast = head.next` gives
  the first. Decide deliberately, don't discover it from a failing test.
- **Single node** returns itself: the guard fails immediately, `slow` is still `head`.
  Correct with no special case.
- **Empty list** returns `None`, also with no special case, but only because `slow`
  was initialised to `head`. If you'd written `slow = head.next` anywhere, this
  throws. Trace it on camera.
- The problem asks for the **node**, not its value, and returning a node returns the
  whole tail with it. That's expected, don't "fix" it.

## 🎤 Interview talking points
- *"Distance is speed times time. Equal time at half the speed means half the
  distance, so when fast finishes, slow is at the midpoint."*
- *"Counting first is also O(n) and perfectly acceptable; I'm using two pointers
  because it's single-pass, which matters if the list is a stream, and because the
  same shape is how I'd split a list for merge sort or a palindrome check."*
- If asked for the first middle: change `fast` to start at `head.next`, and say it
  out loud rather than silently editing.

## 🔗 Transfer
This is a component, not a destination. EP18 (Palindrome LinkedList) finds the middle,
reverses the second half, and compares. EP19 (Reorder List) finds the middle, reverses
the second half, and interleaves. **Merge sort on a linked list** splits at the middle
the same way. Get the off-by-one right here and the next two episodes are assembly.

## 📹 Metadata
- **Title:** `Middle of a Linked List, one pass, no counting | Fast & Slow #5`
- **Thumbnail:** `HALF SPEED = HALFWAY` (teal block)
- **Short:** The two dry-run tables side by side, odd lands on the middle, even lands on the second.
