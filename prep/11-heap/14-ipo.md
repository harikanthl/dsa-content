# EP107 · P11E14 · IPO   [Hard]

**Pattern:** Heap (greedy + heap, two heaps) · **Link:** https://leetcode.com/problems/ipo/description/

---

## 🎬 Hook
> "You can do k projects, and each one makes you richer, which unlocks bigger ones. The
> greedy answer is obvious: always do the **most profitable project you can afford**.
> The hard part is that 'what you can afford' **grows** every round. Two heaps: one
> sorted by **cost**, to see what just unlocked, and one sorted by **profit**, to pick."

## 📋 Problem, in your words
```
You start with capital w and may finish at most k distinct projects.
Project i needs capital[i] to START (you don't spend it) and adds
profits[i] to your capital when done.

Return the maximum capital after at most k projects.
```

## 🔢 The example
```
Input:  k = 2, w = 0, profits = [1, 2, 3], capital = [0, 1, 1]
Output: 4
Why:    w = 0: only project 0 is affordable -> do it, w = 1
        w = 1: projects 1 and 2 unlock -> do project 2 (profit 3), w = 4

Input:  k = 3, w = 0, profits = [1, 2, 3], capital = [0, 1, 2]
Output: 6

Input:  k = 1, w = 0, profits = [1], capital = [1]
Output: 0          <- can't afford anything, stay at 0
```

## 🧸 ELI5
> A video game shop where items are **locked** behind a level requirement, and every
> item you use gives you XP. You get k turns.
>
> Two shelves:
> - the **locked shelf**, lined up by level requirement, cheapest-to-unlock at the front;
> - the **unlocked shelf**, where the best item is always at the front.
>
> Each turn: walk along the locked shelf and move everything you can now afford onto the
> unlocked shelf. Then use the best unlocked item. Your level goes up, so next turn more
> things unlock.
>
> ```
> level 0:  locked [0:+1, 1:+2, 1:+3]  -> unlock +1           use +1, level 1
> level 1:  locked [1:+2, 1:+3]        -> unlock +2, +3       use +3, level 4
> ```
>
> Using the +2 is never better than the +3: money doesn't run out when you use it, so
> the only thing that matters each turn is **how much it adds**.

## 🐌 Brute force (say it, don't type it)
Each round, scan every unused project for the most profitable affordable one: **O(k·n)**.
With n and k up to 10⁵ that's 10¹⁰. The two heaps make each project move once and each
round one pop: **O(n log n + k log n)**.

## 💡 The pattern reveal
**Signal:** "at most k picks" · each pick **unlocks** more options · maximise a total.
**Therefore:** Shape D greedy + heap, the **two-heap** variant from the pattern card.

**Key insight:** capital is never spent, only gained, so a project that's affordable now
stays affordable forever. That makes it a one-way flow:

```
locked (MIN-heap by capital)  ──  w grows  ──►  affordable (MAX-heap by profit)  ──►  pop one per round
```

Each round:
1. Move every locked project with `capital <= w` into the affordable heap.
2. If the affordable heap is empty, stop early: nothing will ever unlock.
3. Pop the biggest profit, add it to `w`.

Why greedy is right: taking the most profitable affordable project gives the largest
`w`, and a larger `w` unlocks a **superset** of what a smaller one would. There's no
trade-off to weigh.

## 🔍 Dry run: `k = 2`, `w = 0`, `profits = [1, 2, 3]`, `capital = [0, 1, 1]`
`locked = heapify([(0,1), (1,2), (1,3)])` as `(capital, profit)`.

| round | w before | moved to affordable (cap ≤ w) | affordable (profits) | pop | w after |
|---|---|---|---|---|---|
| 1 | 0 | (0, +1) | {1} | +1 | 1 |
| 2 | 1 | (1, +2), (1, +3) | {3, 2} | +3 | **4** |

k rounds used. Answer **`4`** ✓. The +2 is left unused in the affordable heap.

## ✅ Optimal solution
```python
class Solution:
    def findMaximizedCapital(self, k: int, w: int, profits: List[int], capital: List[int]) -> int:
        """Max capital after at most k projects, each needing capital[i] to start.

        Time:  O(n log n + k log n), each project moves heaps once; one pop per round.
        Space: O(n), the two heaps.
        """
        locked = list(zip(capital, profits))    # MIN-heap by required capital
        heapq.heapify(locked)
        affordable = []                         # MAX-heap by profit (negated)

        for _ in range(k):
            while locked and locked[0][0] <= w:     # everything w now unlocks
                c, p = heapq.heappop(locked)
                heapq.heappush(affordable, -p)

            if not affordable:
                break                           # nothing affordable, and w can't grow

            w += -heapq.heappop(affordable)     # most profitable thing we can start

        return w
```
**Time:** O(n log n + k log n) · **Space:** O(n)

## ⚠️ Gotchas
- **Capital is a threshold, not a cost.** You don't subtract `capital[i]` from `w`. Read
  the statement twice; it's the #1 wrong answer.
- **Break when affordable is empty.** Without it, `heappop` on an empty heap raises, and
  there's no point looping: `w` can't change.
- **`<=` on unlocking.** `capital = 0` with `w = 0` must be affordable.
- **The locked heap could be a sorted list with a pointer.** Nothing is ever added to
  it, so sorting once and walking an index is the same thing, sometimes faster. Say so;
  either is fine.
- **Don't re-scan.** The `while` moves each project across exactly once in total, not
  once per round. That's what makes it O(n log n).

## 🎤 Interview talking points
- *"Capital only grows, so once a project is affordable it stays affordable. I keep a
  min-heap by capital for locked projects and a max-heap by profit for affordable ones."*
- *"Each round, drain everything newly affordable across, then take the top profit."*
- *"Greedy works because more capital unlocks a superset of projects, so the biggest
  profit now can't hurt any future choice."*
- *"O((n + k) log n). The naive scan is O(k·n)."*

## 🔗 Transfer
The "move things across when they become available" loop is the same one as EP106,
where stations moved into the heap as the car's reach grew. Tomorrow (EP108, Course
Schedule III) flips the direction: instead of adding the best thing that's available,
you take **everything** and use the heap to **undo** the worst decision when you run out
of time.

## 📹 Metadata
- **Title:** `IPO, two heaps: unlock by cost, choose by profit | Heap #14`
- **Thumbnail:** `locked → affordable` (green block)
- **Short:** the game shop with two shelves, the +3 picked over the +2. 45s.
