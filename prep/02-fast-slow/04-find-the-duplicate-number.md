# EP016 · P02E04 · Find the Duplicate Number   [Medium]

**Pattern:** Fast & Slow Pointers · **Link:** https://leetcode.com/problems/find-the-duplicate-number/description/

---

## 🎬 Hook
> "You get an array. You may not modify it, and you may not use extra memory. Sorting
> is out, a hash set is out, marking elements is out — every obvious tool is banned.
> What's left is to notice the array is secretly a linked list, and that the duplicate
> is the exact place where it loops."

## 📋 Problem, in your words
```
An array of n+1 integers, every value in the range 1..n.
By the pigeonhole principle at least one value must repeat.
There is exactly one repeated value — but it may appear more than twice.

Return that value.

Constraints that matter: do NOT modify the array, and use O(1) extra space.
```

## 🔢 The example
```
Input:  nums = [1, 3, 4, 2, 2]     (n = 4, five slots, values 1..4)
Output: 2

Input:  nums = [3, 1, 3, 4, 2]
Output: 3
```

## 🧸 ELI5
> Treat each index as a room, and the number inside it as the door number it sends
> you to. Room 0 holds a 1, so room 0 sends you to room 1. Room 1 holds a 3, so it
> sends you to room 3. And so on.
>
> Every room has exactly one exit. So walking the rooms is walking a linked list:
> `i → nums[i] → nums[nums[i]] → …`
>
> Now: why must there be a loop? Because two different rooms hold the *same* number,
> and that number is a room. Two doors lead into one room. That room has **two ways
> in and one way out** — which is exactly the shape of the entrance to a cycle.
>
> So the duplicate value isn't just *somewhere* in the loop. It **is** the loop's
> entrance. Find where the cycle starts and you have your answer.

```
nums = [1, 3, 4, 2, 2]

  index:   0    1    2    3    4
  value:   1    3    4    2    2

  0 -> 1 -> 3 -> 2 -> 4 -> 2 -> 4 -> 2 ...
                 ^         |
                 +---------+      the cycle starts at 2 -- the duplicate
```

## 🐌 Brute force (say it, don't type it)
Three answers, each banned by a different constraint — say all three, it shows you
read the constraints instead of pattern-matching:

| Approach | Cost | Why it's ruled out |
|---|---|---|
| Nested loops comparing every pair | O(n²) time, O(1) space | Too slow |
| Sort, then look for adjacent equals | O(n log n) time | **Modifies the array** |
| Hash set of seen values | O(n) time, O(n) space | **Extra memory** |
| Mark visited by negating `nums[abs(v)]` | O(n) time, O(1) space | **Modifies the array** |

That last one is the trap. It's clever, it's O(1) space, and it's *wrong* here because
the problem says read-only. Naming it and then rejecting it is a strong move.

## 💡 The pattern reveal
**Signal:** array of values that are themselves valid indices · find the repeat ·
read-only · O(1) space.
**Therefore:** Fast & Slow pointers, Shape A + B — on an implicit linked list.

**Key insight, in two parts:**

1. `i → nums[i]` is a `.next` pointer, so the array is a linked list (EP15's lesson).
2. **The duplicate is the cycle's entrance**, because the entrance is by definition
   the one node with two predecessors — and two predecessors means two indices
   holding the same value.

That second half is what makes this problem hard and what makes it beautiful. Cycle
*detection* (phase 1) is not enough; you need Floyd's phase 2 from EP14 to find
**where** the cycle begins.

**Why start at `nums[0]` and not at index `0`?** Values are in `1..n`, so no value is
ever `0`. Nothing points back at index 0 — it's outside the cycle, a tail leading in,
which is exactly what phase 2 requires. If `0` were a legal value, the reduction
would break.

## 🔍 Dry run — `nums = [1, 3, 4, 2, 2]`
The list: `1 → 3 → 2 → 4 → 2 → 4 → …`

**Phase 1 — find a meeting point** (`slow = nums[slow]`, `fast = nums[nums[fast]]`):

| step | slow | fast | note |
|---|---|---|---|
| start | 1 | 1 | both at `nums[0]` |
| 1 | 3 | 2 | |
| 2 | **2** | **2** | met — somewhere inside the cycle, not necessarily the start |

**Phase 2 — walk both at the same speed, one from the head:**

| step | slow | fast | note |
|---|---|---|---|
| reset | 1 | 2 | `slow` back to `nums[0]`, `fast` stays put |
| 1 | 3 | 4 | |
| 2 | **2** | **2** | met at the entrance → answer is `2` ✓ |

Point at the two tables on screen together. Phase 1 answers *is there a loop*; phase 2
answers *where does it start*. They are different questions and the second is the one
being asked.

## ✅ Optimal solution
```python
class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        """The duplicate value is the entrance of the cycle in i -> nums[i].

        Time:  O(n) — each phase walks a bounded number of steps.
        Space: O(1) — two integers, and the array is never written to.
        """
        # Phase 1 — Floyd: find a meeting point inside the cycle.
        slow = fast = nums[0]
        while True:
            slow = nums[slow]              # 1 hop
            fast = nums[nums[fast]]        # 2 hops
            if slow == fast:
                break

        # Phase 2 — reset one runner to the head; equal speed; they collide
        # at the entrance, because F = nC - a (see the pattern card).
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]
        return slow
```
**Time:** O(n) · **Space:** O(1) ✓ · **The array is never modified** ✓

### The alternative worth knowing: binary search on the answer
```python
lo, hi = 1, len(nums) - 1
while lo < hi:
    mid = (lo + hi) // 2
    count = sum(1 for v in nums if v <= mid)   # how many values land in 1..mid
    if count > mid:                            # pigeonhole: the dupe is in 1..mid
        hi = mid
    else:
        lo = mid + 1
return lo
```
**O(n log n) time, O(1) space, also read-only.** Slower, but far easier to explain and
much harder to get wrong under pressure. Say this out loud: *"if I were shaky on
Floyd's phase two, I'd write this — it's O(n log n) instead of O(n), and correct."*
Knowing when to trade a log factor for certainty is a senior signal.

## ⚠️ Gotchas
- **`while True` with a `break`, not a `while slow != fast` loop.** They start equal,
  so a pre-checked loop exits immediately without moving. Same trap as EP13.
- **Start both at `nums[0]`, not at `0`.** Starting at index `0` also works if you're
  careful, but `nums[0]` keeps the two phases symmetric and is the version to
  memorise. What you must *not* do is start phase 2 from the meeting point for both.
- **Phase 2 resets only `slow`.** `fast` stays where they met. Resetting both restarts
  the whole thing and loops forever.
- **Both phases move by value, never by index arithmetic.** `nums[nums[fast]]` is two
  hops; `nums[fast] + 1` is nonsense. Easy to fumble live.
- The duplicate may appear **more than twice** (`[2,2,2,2,2]`). The cycle argument
  doesn't care — more predecessors is still an entrance. Test that case.
- Values are `1..n` with `n+1` slots, so index `0` is never a target. If a variant
  allows `0`, this reduction is invalid — say so, it shows you know why it works.

## 🎤 Interview talking points
- *"The values are valid indices, so the array defines a functional graph. Pigeonhole
  guarantees a repeat, a repeat means two edges into one node, and a node with two
  in-edges and one out-edge is a cycle entrance. So the answer is the entrance."*
- *"Phase 2 is `F = nC − a`: slow walked `F + a`, fast walked twice that, and the
  difference is whole loops. So the distance from the head to the entrance equals the
  distance from the meeting point to the entrance."*
- *"Read-only plus O(1) space is what rules out the negate-marking trick, which is the
  answer people give when they've seen the problem but not read the constraints."*

## 🔗 Transfer
This closes the "implicit linked list" arc: EP15 introduced it, EP16 needs both
phases. From here (EP17–19) the pattern goes back to real linked lists and switches to
Shape C — using the fast runner to find the **middle** instead of a cycle. Same two
pointers, different question.

## 📹 Metadata
- **Title:** `Find the Duplicate — your array is a linked list | Fast & Slow #4`
- **Thumbnail:** `THE DUPE IS THE LOOP` (teal block)
- **Short:** The `[1,3,4,2,2]` room-and-door drawing, 50s, ending on "two doors into room 2."
