# EP003 · P01E03 · Remove Duplicates   [Easy]

**Pattern:** Two Pointers · **3 variants in one video**

- https://leetcode.com/problems/remove-duplicates-from-sorted-list/ (linked list)
- https://leetcode.com/problems/remove-duplicates-from-sorted-array/ (array)
- https://leetcode.com/problems/remove-duplicates-from-sorted-array-ii/ (allow 2)

---

## 🎬 Hook
> "You can't actually delete from an array. So how does LeetCode expect you to
> 'remove' duplicates in place? The answer is that you don't delete — you *overwrite*.
> And once that clicks, three different problems become the same four lines."

## 📋 Problem, in your words
```
Variant A (linked list): a sorted linked list. Delete duplicate nodes so each
                         value appears once. Return the head.

Variant B (array):       a sorted array. Move the unique values to the front,
                         in order, and return how many there are.
                         Whatever sits past that count is ignored by the grader.

Variant C (array II):    same, but each value may appear AT MOST TWICE.
```

## 🔢 The examples
```
A:  1 -> 1 -> 2 -> 3 -> 3        =>  1 -> 2 -> 3
B:  [1, 1, 2, 2, 2, 3]           =>  k = 3, array starts [1, 2, 3, ...]
C:  [1, 1, 2, 2, 2, 3]           =>  k = 5, array starts [1, 1, 2, 2, 3, ...]
```

## 🧸 ELI5
> You're retyping a guest list that's alphabetised but has accidental repeats.
>
> You read down the original list with one finger (**fast**), and you have a second
> finger on the clean list you're building (**slow**). For each name you read, you
> glance at the last name you wrote. Same? Skip it. Different? Write it, move the
> writing finger down one.
>
> The clean list is being written *on top of* the messy one, but that's fine —
> your writing finger is always at or behind your reading finger, so you can never
> scribble over something you haven't read yet.

**That last sentence is the whole insight of the pattern.** Say it slowly on camera.

## 🐌 Brute force (say it, don't type it)
Build a new array, append when the value differs from the last appended — O(n) time
but **O(n) extra space**, which the problem explicitly forbids. Or: find a duplicate
and shift every later element left one slot — that's **O(n²)**.

## 💡 The pattern reveal
**Signal:** *sorted* + *in place* + *return the new length*.
**Therefore:** Two Pointers, Shape B — fast (read) and slow (write), same direction.

**Key insight:** because the array is sorted, duplicates are **adjacent**. You never
need to remember what you've seen — you only need to compare against the element you
most recently kept. That's an O(1) memory of the past instead of a hash set.

## 🔍 Dry run — Variant B on `[1, 1, 2, 2, 2, 3]`
`slow` = index of the last kept element. Start `slow = 0` (first element is always kept).

| fast | arr[fast] | arr[slow] | same? | action | array so far |
|---|---|---|---|---|---|
| 1 | 1 | 1 | yes | skip | `[1,1,2,2,2,3]` |
| 2 | 2 | 1 | no | `slow=1`, `arr[1]=2` | `[1,2,2,2,2,3]` |
| 3 | 2 | 2 | yes | skip | `[1,2,...]` |
| 4 | 2 | 2 | yes | skip | `[1,2,...]` |
| 5 | 3 | 2 | no | `slow=2`, `arr[2]=3` | `[1,2,3,2,2,3]` |

Return `slow + 1` = **3**. The first 3 slots are `[1, 2, 3]`. The junk after them is
exactly what the problem says to ignore.

## ✅ Optimal solutions

### A — Linked list
```python
class Solution:
    def deleteDuplicates(self, head: Optional[ListNode]) -> Optional[ListNode]:
        cur = head
        while cur and cur.next:
            if cur.val == cur.next.val:
                cur.next = cur.next.next      # unlink the duplicate, stay put
            else:
                cur = cur.next                # values differ, advance
        return head
```
**Do not advance `cur` after unlinking** — there may be a third copy right behind it.
This is the one bug people ship. `1 -> 1 -> 1` breaks if you advance.

### B — Array, keep 1 copy
```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        if not nums:
            return 0
        slow = 0                               # last index we decided to keep
        for fast in range(1, len(nums)):
            if nums[fast] != nums[slow]:
                slow += 1
                nums[slow] = nums[fast]
        return slow + 1
```

### C — Array, keep up to 2 copies (the generalisation)
```python
class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        k = 2                                  # max copies allowed
        slow = 0
        for n in nums:
            # keep n if we have fewer than k written, or n differs from the
            # element k positions back in the kept region
            if slow < k or n != nums[slow - k]:
                nums[slow] = n
                slow += 1
        return slow
```
**This one solution solves A, B and C** — set `k = 1` and it's variant B. Showing that
on camera is the payoff of the whole episode: three LeetCode problems, one idea.

**Time:** O(n) all three · **Space:** O(1) all three

## ⚠️ Gotchas
- Variant A: don't move the pointer after unlinking.
- Variant B: `slow` starts at **0**, `fast` at **1**. Starting both at 0 compares an
  element with itself and keeps nothing.
- Return value: B returns `slow + 1` (slow is an *index*), C returns `slow` (slow is
  a *count*). Mixing these up is an off-by-one you'll hit live — good, fix it on camera.
- Variant C's `nums[slow - k]` looks at the **kept** region, not the original array.
  That's why it stays correct as you overwrite.

## 🎤 Interview talking points
- *"Sorted means duplicates are adjacent, so I only need O(1) memory of the past —
  no hash set."*
- *"The write pointer never overtakes the read pointer, so overwriting in place is
  always safe."*
- *"I'd write the `k`-copies version, because setting k=1 recovers the simpler problem
  for free."*

## 🔗 Transfer
Shape B (read/write compaction) is everywhere: Move Zeroes, Remove Element, Remove
Nodes From Linked List (EP 68). The `nums[slow - k]` trick generalises to any
"at most k occurrences" problem.

## 📹 Metadata
- **Title:** `Remove Duplicates — 3 LeetCode problems, 1 pattern | Two Pointers #3`
- **Thumbnail:** `DON'T DELETE. OVERWRITE.` (blue block)
- **Short:** Beat 4 — the guest-list retyping analogy.
