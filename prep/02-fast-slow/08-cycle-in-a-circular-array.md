# EP020 · P02E08 · Cycle in a Circular Array   [Hard]

**Pattern:** Fast & Slow Pointers · **Link:** https://leetcode.com/problems/circular-array-loop/

---

## 🎬 Hook
> "Same two runners, same meeting rule — but now the track has one-way streets, some
> loops don't count, and you have to try every starting line. This is Floyd's
> algorithm with three extra conditions bolted on, and it's the episode where you find
> out whether you actually understood the pattern or just memorised its shape."

## 📋 Problem, in your words
```
A circular array of NON-ZERO integers. Standing at index i, nums[i] tells you
how far to jump:
  positive -> that many steps forward
  negative -> that many steps backward
The array wraps at both ends.

Return true if a valid cycle exists. A cycle is valid only if:
  1. its length is greater than 1  (a self-loop does NOT count), and
  2. every jump in it goes the SAME direction (all forward, or all backward).
```

## 🔢 The example
```
Input:  nums = [2, -1, 1, 2, 2]
Output: true

  index:  0   1   2   3   4
  value:  2  -1   1   2   2
  jumps:  0 -> 2 -> 3 -> 0        length 3, and nums[0], nums[2], nums[3]
          ^              |        are 2, 1, 2 -- all positive. Valid.
          +--------------+

Input:  nums = [-1, -2, -3, -4, -5, 6]
Output: false

Input:  nums = [-2, 1, -1, -2, -2]
Output: false     (a cycle exists: 1 -> 2 -> 1, but nums[1]=1 is forward
                   and nums[2]=-1 is backward -- mixed direction, so it
                   doesn't count)
```

That third example is the whole difficulty of the problem. Put it on screen early.

## 🧸 ELI5
> It's the runner game again, on a circular track — but now every square has an arrow
> painted on it telling you how many squares to move and which way.
>
> Two rules the referee added:
>
> - **You can't win by standing still.** If a square's arrow points right back at
>   itself, that's a loop of one, and it doesn't count.
> - **No U-turns.** If your lap used some forward arrows and some backward arrows,
>   it doesn't count either. The whole lap has to go one way round.
>
> And because a lap might exist in one corner of the track that you'd never reach from
> where you started, you have to try starting from **every square**.

## 🐌 Brute force (say it, don't type it)
From each start index, walk forward and keep a `set` of indices you've visited on this
walk; if you revisit one, you found a cycle — then check its length and direction.

**O(n²) time, O(n) space.** The direction rule actually makes this *easier* to reason
about than it looks: the moment you step on a value whose sign differs from your
start's, that entire walk is dead and you can stop. So the honest brute force isn't
far off the real answer — the win here is dropping the set, not the outer loop.

## 💡 The pattern reveal
**Signal:** `i → (i + nums[i]) mod n` maps each index to exactly one next index ·
"does it loop?"
**Therefore:** Fast & Slow pointers, Shape A — plus three rejection rules.

**Key insight:** this is EP15's lesson (a function *is* a linked list) with a modular
next-function, and EP13's meeting rule unchanged. What's genuinely new is that **not
every cycle is an answer**, so you need guards that abandon a walk early:

| Rule | Check | Why |
|---|---|---|
| Same direction | `(nums[i] > 0) != forward` | the moment a sign flips, this walk is dead |
| Length > 1 | `i == next(i)` | a self-loop; kill it before the pointers can "meet" on it |
| Reachability | try every start index | a valid cycle may sit in a part of the array you never enter |

**The self-loop check is the subtle one.** Without it, `slow` and `fast` both park on a
one-element loop and compare equal — you'd return `True` for a cycle of length 1,
which the problem explicitly forbids. Every guard has to be applied *after each
individual hop*, including both of the fast pointer's hops, or a bad index slips
through between them.

## 🔍 Dry run — `nums = [2, -1, 1, 2, 2]`, starting at index 0
Next-index map: `0→2, 1→0, 2→3, 3→0, 4→1`. Direction for this start: **forward**
(`nums[0] = 2 > 0`).

| step | slow | fast | checks |
|---|---|---|---|
| start | 0 | 0 | direction fixed as forward |
| 1 | 2 | 3 | `nums[2]=1>0` ✓, `nums[3]=2>0` ✓, no self-loops |
| 2 | 3 | 2 | fast hopped 3→0→2; all forward ✓ |
| 3 | **0** | **0** | they met → cycle `0→2→3→0`, length 3, all forward → `True` |

## 🔍 Dry run — `nums = [-2, 1, -1, -2, -2]` (the rejection case)
Next map: `0→3, 1→2, 2→1, 3→1, 4→2`. There *is* a cycle — `1 ⇄ 2` — but:

| start | direction | what happens |
|---|---|---|
| 0 | backward | reaches index 3, then 1, where `nums[1] = 1` is **forward** → abandon |
| 1 | forward | first hop lands on index 2, `nums[2] = -1` is **backward** → abandon |
| 2 | backward | hop to 1, `nums[1]` is forward → abandon |
| 3 | backward | hop to 1, same → abandon |
| 4 | backward | hop to 2, then 1, forward → abandon |

Every start dies on the direction rule. Return `False`. ✓ The cycle was real; it just
wasn't *valid*.

## ✅ Optimal solution
```python
class Solution:
    def circularArrayLoop(self, nums: List[int]) -> bool:
        """Floyd's cycle detection per start index, with direction and
        self-loop rejection.

        Time:  O(n^2) worst case — n starts, each walk O(n).
        Space: O(1) — two indices and a direction flag.
        """
        n = len(nums)

        def next_index(i: int) -> int:
            return (i + nums[i]) % n          # Python's % is already non-negative

        for start in range(n):
            forward = nums[start] > 0
            slow = fast = start

            while True:
                slow = next_index(slow)
                if (nums[slow] > 0) != forward or slow == next_index(slow):
                    break                      # wrong direction, or a self-loop

                fast = next_index(fast)        # fast's FIRST hop — check it
                if (nums[fast] > 0) != forward or fast == next_index(fast):
                    break

                fast = next_index(fast)        # fast's SECOND hop — check it too
                if (nums[fast] > 0) != forward or fast == next_index(fast):
                    break

                if slow == fast:
                    return True                # valid cycle: len > 1, one direction

        return False
```
**Time:** O(n²) worst case · **Space:** O(1) ✓

### The O(n) version worth mentioning
Mark every index of a failed walk as `0` so no later start re-walks it. Each index is
then visited a constant number of times overall, giving **O(n) time** — at the cost of
destroying the input. Say this out loud and then say the trade: *"O(n) if I'm allowed
to write to the array, O(n²) if it has to stay read-only."* Naming the trade is worth
more than having the faster answer.

## ⚠️ Gotchas
- **`(nums[i] > 0) != forward` — compare booleans, not signs.** Writing
  `nums[i] * nums[start] < 0` also works but overflows in C++ and reads worse. The
  boolean form says exactly what you mean.
- **Check after *every* hop, including both of fast's.** Skipping the check between
  fast's two hops lets it pass *through* a direction change and land somewhere legal,
  and you report a cycle that isn't there. This is the hardest bug here to find by
  staring at the code — it only shows up on specific inputs.
- **`slow == next_index(slow)` is the length-1 guard.** Without it a self-loop makes
  both pointers park on one index and compare equal, returning `True` on an invalid
  cycle.
- **Python's `%` is already non-negative** — `(0 + -2) % 5 == 3`. In C, C++ or Java
  you need `((i + nums[i]) % n + n) % n`. Mention this; it's an easy silent failure
  when porting and interviewers in those languages will look for it.
- **You must try every start.** The valid cycle may be unreachable from index 0. One
  outer loop, no shortcuts.
- The problem guarantees `nums[i] != 0`, so no jump is ever a stay-put. If a variant
  allows zero, a zero *is* a self-loop and needs the same rejection.

## 🎤 Interview talking points
- *"It's Floyd's with a modular next-function, plus rejection rules. The pattern gives
  me the skeleton; the problem's constraints become early-exit guards."*
- *"The self-loop check exists because the meeting test can't distinguish a cycle of
  length one from a real cycle — both make the pointers equal."*
- *"O(n²) read-only, or O(n) if I can mark visited indices as zero. I'd ask which the
  caller cares about."*

## 🔗 Transfer
This closes Pattern 02. What carries forward is the habit, not the code: **when a
problem gives you `next = f(current)` over a finite domain, you have a linked list.**
That reframing shows up again in Pattern 12 (Recursion and Backtracking, where the
state graph is implicit) and Pattern 14 (Graphs, where it becomes explicit). Next up
is Pattern 03 — Sliding Window — the other great "stop recomputing what you already
know" family.

## 📹 Metadata
- **Title:** `Circular Array Loop — Floyd's with three extra rules | Fast & Slow #8`
- **Thumbnail:** `NOT EVERY LOOP COUNTS` (teal block)
- **Short:** The `[-2,1,-1,-2,-2]` case — "there IS a cycle, and the answer is still false." 50s.
