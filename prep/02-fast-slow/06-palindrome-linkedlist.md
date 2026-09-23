# EP018 · P02E06 · Palindrome LinkedList   [Medium]

**Pattern:** Fast & Slow Pointers · **Link:** https://leetcode.com/problems/palindrome-linked-list/

---

## 🎬 Hook
> "A palindrome check needs you to read backwards. A singly linked list only goes
> forwards. So you do the only thing left: you find the middle, you physically turn
> the second half around, and then you walk both halves forwards at once."

## 📋 Problem, in your words
```
Given the head of a singly linked list, return true if it reads the same
forwards and backwards.

Follow-up: O(n) time AND O(1) space.
```

## 🔢 The example
```
Input:  1 -> 2 -> 2 -> 1
Output: true

Input:  1 -> 2 -> 3 -> 2 -> 1
Output: true        (odd length, the middle 3 is its own mirror)

Input:  1 -> 2
Output: false
```

## 🧸 ELI5
> You have a line of numbered cards you can only read left to right, you can't flip
> the line around.
>
> So: walk to the middle. Take the back half off the table and lay it out reversed, so
> its last card is now first. Now you have two half-lines, both readable left to right,
> and the question "is it a palindrome?" becomes "do these two halves match card for
> card?"
>
> That's three things you already know, stacked: **find the middle** (EP17), **reverse
> a list**, **compare two lists**.

## 🐌 Brute force (say it, don't type it)
Copy the values into an array and check the array with two pointers.

```python
vals = []
while head: vals.append(head.val); head = head.next
return vals == vals[::-1]
```

**O(n) time, O(n) space.** This is correct, takes ten seconds to write, and is the
right first answer in an interview. Then the follow-up lands: *O(1) space*. That's
where the real work starts, and note that the recursive solution people reach for
next is also O(n) space, just hidden in the call stack. Say that; it catches people.

## 💡 The pattern reveal
**Signal:** linked list · compare front to back · O(1) space required.
**Therefore:** Fast & Slow (Shape C) to find the middle, then in-place reversal.

**Key insight:** you cannot read a singly linked list backwards, so stop trying. Turn
half of it around instead. Reversal is O(1) space because it only rewires existing
`.next` pointers, it allocates nothing.

**This is the pattern's first composition episode.** Nothing here is new. The skill
being tested is assembling three known pieces in the right order and getting the seams
right.

## 🔍 Dry run: `1 → 2 → 2 → 1` (even length)

**Step 1, find the middle** (`while fast and fast.next`):

| step | slow | fast |
|---|---|---|
| start | 1ᵃ | 1ᵃ |
| 1 | 2ᵇ | 2ᶜ |
| 2 | **2ᶜ** | `None` |

`slow` stops at the third node, the start of the second half. (Superscripts label
positions, since values repeat.)

**Step 2, reverse from `slow`:** `2ᶜ → 1ᵈ` becomes `1ᵈ → 2ᶜ`, and the list is now:

```
first half:   1ᵃ -> 2ᵇ -> (2ᶜ, now the tail of the reversed half)
second half:  1ᵈ -> 2ᶜ -> None
```

**Step 3, walk both:**

| step | left | right | match? |
|---|---|---|---|
| 1 | 1ᵃ | 1ᵈ | ✓ |
| 2 | 2ᵇ | 2ᶜ | ✓ |
| 3 | - | `None` | right exhausted → return `True` |

## 🔍 Dry run: `1 → 2 → 3 → 2 → 1` (odd length)
The middle pointer lands on `3`. Reversing from `3` gives `1 → 2 → 3`, and comparing
`1 → 2 → 3 …` against `1 → 2 → 3` matches for two steps before the right side runs
out. **The odd middle is compared against itself and always matches, which is
correct**: a single central element is its own mirror. This is why the loop condition
is on the *right* (shorter) half.

## ✅ Optimal solution
```python
class Solution:
    def isPalindrome(self, head: Optional[ListNode]) -> bool:
        """Find the middle, reverse the second half, walk both halves forwards.

        Time:  O(n), three linear passes: middle, reverse, compare.
        Space: O(1), only pointer rewiring; nothing is allocated.
        """
        # 1. middle, for even lengths this lands on the START of the second half
        slow = fast = head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # 2. reverse from the middle onwards
        prev = None
        while slow:
            slow.next, prev, slow = prev, slow, slow.next

        # 3. compare the two halves; the reversed half is the shorter one, so
        #    stopping when it runs out handles odd lengths for free
        left, right = head, prev
        while right:
            if left.val != right.val:
                return False
            left, right = left.next, right.next

        return True
```
**Time:** O(n) · **Space:** O(1) ✓

### That reversal line, said slowly
```python
slow.next, prev, slow = prev, slow, slow.next
```
Python evaluates the **entire right side first**, then assigns left to right. So
`slow.next` gets the old `prev`, `prev` gets the old `slow`, and `slow` gets the old
`slow.next`, no temporary variable needed and no ordering bug possible. Write it as
four explicit lines the first time on camera, *then* collapse it, so viewers see
they're the same thing:

```python
nxt = slow.next      # save where we were going
slow.next = prev     # flip this arrow backwards
prev = slow          # prev walks forward
slow = nxt           # so does slow
```

## ⚠️ Gotchas
- **Loop on `right`, not `left`.** After reversing, the two halves are *not* the same
  length, for odd inputs the left half is one longer, and for even inputs the middle
  node ends up in both. Looping on the reversed (right) half stops at the right moment
  in both cases. Looping on `left` walks off the end.
- **The list is left mutated.** The second half now points backwards. LeetCode doesn't
  check, but an interviewer might ask, the polite version re-reverses at the end to
  restore it. Mention it; offering to restore is a real-world signal.
- **Don't try to cut the list in half first.** Setting `first_half_tail.next = None` is
  tempting and adds a bookkeeping pointer you don't need. The comparison already stops
  correctly without it.
- **Empty list and single node** both return `True` with no special case: the middle
  loop doesn't run, reversal produces a one-node list, one comparison passes.
- Comparing `left.val != right.val`, not `left is not right`, this is about **values**,
  unlike EP13 where identity was the point. Say the contrast out loud.

## 🎤 Interview talking points
- *"I'd give the array copy first, O(n) space, ten seconds to write, obviously
  correct. For the O(1) follow-up I reverse the second half in place."*
- *"Recursion is not a space win here; the call stack is O(n). People offer it as the
  clever answer and it fails the same constraint."*
- *"I loop on the reversed half because it's the shorter one, which makes odd-length
  lists work without a special case."*
- *"I'm mutating the input. I can reverse it back in O(n) if the caller needs it
  intact."*

## 🔗 Transfer
EP19 (Reorder List) is this exact recipe with the last step changed: instead of
*comparing* the two halves, you *interleave* them. If you can write today's solution
cold, tomorrow's is a ten-line edit. The same middle-then-reverse move also powers
merge sort on linked lists.

## 📹 Metadata
- **Title:** `Palindrome Linked List, reverse half of it | Fast & Slow #6`
- **Thumbnail:** `TURN HALF AROUND` (teal block)
- **Short:** The reversal three-liner expanded to four lines and collapsed back, 45s.
