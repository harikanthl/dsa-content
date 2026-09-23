# Pattern 02: Fast & Slow Pointers (Floyd's Tortoise and Hare)

**8 episodes · EP 13–20**

---

## The one-sentence version

Two pointers moving at **different speeds** through a sequence detect cycles, find
midpoints, and locate structure, in **O(1) space**, without a hash set.

## ELI5

Two runners on a track. One jogs, one sprints at double speed.

- **If the track is a loop**, the sprinter eventually laps the jogger and they meet.
  They *must*, the sprinter gains exactly one step on the jogger every tick, so the
  gap closes by 1 each time until it hits 0. It can't be skipped over.
- **If the track is a straight line**, the sprinter hits the end and there's no meeting.

That's the whole pattern. "Did they meet?" answers *is there a cycle?* And when the
sprinter reaches the end, the jogger is standing exactly **halfway**: which gives you
the midpoint for free, in the same single pass.

## How to recognise it

| Signal | Example |
|---|---|
| A **linked list** and you're asked about a cycle | Linked List Cycle I / II |
| Find the **middle** of a list in one pass | Middle of the Linked List |
| An **implicit** sequence: `x → f(x) → f(f(x))` | Happy Number, Find the Duplicate |
| "Do it in **O(1) space**" on a list problem | the constraint that rules out a hash set |
| Reorder / palindrome-check a list in place | Reorder List, Palindrome Linked List |

**The tell:** the naive answer is a hash set of visited nodes, O(n) space. Any time
the problem says *constant space*, it's asking for this.

**The hidden version is the one that wins interviews.** Happy Number and Find the
Duplicate have no linked list anywhere in sight. But `n → sum_of_squared_digits(n)`
and `i → nums[i]` are **functions that map a value to a next value**, and iterating a
function on a finite set *must* eventually repeat. That's a linked list in disguise.
Spotting it is the entire trick.

## The three shapes

### Shape A: Cycle detection
```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast:
        return True          # they met: there's a cycle
return False                 # fast fell off the end: no cycle
```

**Why `while fast and fast.next`:** `fast` takes two steps, so you must verify both
exist before stepping. Checking only `fast` crashes on `fast.next.next` when `fast`
is the last node.

**Why they're guaranteed to meet:** once both are inside the loop, `fast` closes the
gap by exactly 1 per iteration. A gap shrinking by 1 can never jump past 0.

### Shape B: Finding the cycle's start (Floyd's second phase)
After they meet, reset one pointer to the head and move **both at the same speed**.
They meet again at the entrance of the cycle.

```python
slow = head
while slow is not fast:
    slow = slow.next
    fast = fast.next
return slow                  # the node where the cycle begins
```

**Why it works**: know this proof, it gets asked:

Let `F` = distance from head to the cycle entrance, `a` = distance from the entrance
to the meeting point, `C` = cycle length.

- `slow` travelled `F + a`.
- `fast` travelled `F + a + nC` (it went round the loop `n` more times).
- `fast` moved twice as far: `2(F + a) = F + a + nC` → **`F + a = nC`** → **`F = nC − a`**.

So walking `F` steps from the head lands you at the same place as walking `nC − a`
steps from the meeting point, which is the entrance. Hence: same speed, they collide
there.

### Shape C: Midpoint
```python
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
return slow                  # fast at the end => slow at the middle
```

**The off-by-one to decide consciously:** for an even-length list, this returns the
**second** middle (`[1,2,3,4] → 3`). To get the **first** middle, start
`fast = head.next`. Both are "correct"; the problem tells you which it wants, and
mixing them up is the most common bug in Reorder List and Palindrome Linked List.

## Complexity

| Shape | Time | Space |
|---|---|---|
| A, cycle detection | O(n) | **O(1)** |
| B, cycle start | O(n) | **O(1)** |
| C, midpoint | O(n) | **O(1)** |
| naive hash-set alternative | O(n) | O(n) ← this is what you're beating |

## The episodes

| EP | Problem | Shape | The thing it teaches |
|---|---|---|---|
| 13 | LinkedList Cycle | A | The base case. Why they must meet. |
| 14 | Start of LinkedList Cycle | A + B | Floyd's phase 2 and the `F = nC − a` proof. |
| 15 | Happy Number | A (implicit) | **No linked list.** A function iterated *is* a list. |
| 16 | Find the Duplicate Number | A + B (implicit) | `i → nums[i]` is a linked list. Read-only + O(1). |
| 17 | Middle of the LinkedList | C | Midpoint free, and the first/second-middle choice. |
| 18 | Palindrome LinkedList | C + reverse | Compose: find middle, reverse half, compare. |
| 19 | Rearrange a LinkedList | C + reverse + merge | Three techniques in one. The composition episode. |
| 20 | Cycle in a Circular Array | A (hardest) | Direction constraints + per-start-index reset. |

## What "knowing this in your sleep" means

1. Why must fast and slow meet inside a cycle? *(The gap shrinks by exactly 1 per
   step, so it must hit 0.)*
2. Why does resetting to head and walking at equal speed find the entrance?
   *(`F = nC − a`, from `2(F+a) = F+a+nC`.)*
3. Why `while fast and fast.next` and not `while fast`? *(`fast.next.next`
   dereferences two links ahead.)*
4. When is a problem with no linked list still this pattern? *(Whenever you have
   `next = f(current)` over a finite set, iteration must eventually cycle.)*
5. What does this buy over a hash set? *(O(1) space instead of O(n). That's the
   entire reason the pattern exists.)*
