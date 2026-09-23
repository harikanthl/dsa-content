# EP104 · P11E11 · Task Scheduler   [Medium]

**Pattern:** Heap (greedy + heap) · **Link:** https://leetcode.com/problems/task-scheduler/description/

---

## 🎬 Hook
> "Last Stone Weight pushed the leftover straight back into the heap. Here the leftover
> has to **cool down** first: it can't come back for n turns. So there are two
> containers: the heap for tasks that are **ready**, and a queue for tasks that are
> **cooling**. Most people only draw the heap, and that's why their code is wrong."

## 📋 Problem, in your words
```
A CPU runs tasks labelled A-Z, one per time unit, in any order.
Two runs of the SAME task must be at least n units apart.
The CPU may sit idle for a unit.

Return the minimum number of time units to finish every task.
```

## 🔢 The example
```
Input:  tasks = [A, A, A, B, B, B], n = 2
Output: 8
Why:    A B _ A B _ A B      (_ = idle)

Input:  tasks = [A, C, A, B, D, B], n = 1
Output: 6          <- A B A B C D, never idle

Input:  tasks = [A, A, A, B, B, B], n = 0
Output: 6          <- no cooldown at all
```

## 🧸 ELI5
> A kitchen with one stove and orders for pancakes and eggs. After you cook a pancake,
> the pancake pan needs **2 minutes to cool** before it can be used again.
>
> Each minute: cook whichever dish has the **most orders left** (so the big pile doesn't
> get stuck at the end), then put its pan on the **cooling rack** with a timer. When a
> pan's timer rings, it goes back to the stove area. If every pan is on the rack, you
> stand around for a minute: that's an idle.
>
> ```
> min 1: A        rack: A(ready after min 3)
> min 2: B        rack: A, B(ready after min 4)
> min 3: idle     A's timer rings, A back
> min 4: A        B back
> ...
> ```
>
> Why the most orders first? Because the dish with the most orders is the one that
> forces the idles; you want it started as early and as often as possible.

## 🐌 Brute force (say it, don't type it)
Simulate minute by minute, and each minute scan all 26 letters for "the one with the
most remaining that isn't cooling". That's **O(T · 26)** for T total time units, which
is actually fine since 26 is a constant. The heap version is the same simulation with
the "pick" step made O(log 26). The episode is about **structure**, the cooling queue,
not raw speed.

## 💡 The pattern reveal
**Signal:** "each unit, pick a task" · "same task must wait n" · minimise time.
**Therefore:** Shape D, greedy + heap, with a **cooling queue** next to the heap.

**Key insight:** each tick:
1. If the heap has something, pop the **highest remaining count**, run it, and if it
   still has copies left, park it in the queue with its **ready time** `time + n`.
2. If the front of the queue is ready now, move it back into the heap.
3. If the heap was empty, that tick was idle, and the clock still moved.

```python
time += 1
if heap:
    left = heapq.heappop(heap) + 1          # counts are negated: +1 means one fewer
    if left < 0:
        cooling.append((left, time + n))    # back in the heap after tick time + n
if cooling and cooling[0][1] == time:
    heapq.heappush(heap, cooling.popleft()[0])
```

The queue is FIFO and every task waits the same n, so the front is always the next to
be ready. That's why a plain `deque` is enough, no second heap needed.

**The heap holds counts only.** Which letter is which never matters for the *length* of
the schedule, only how many copies are left.

## 🔍 Dry run: `[A, A, A, B, B, B]`, `n = 2`
Heap starts `{A:3, B:3}` (as counts).

| time | run | its count after | cooling queue (count, ready at) | returned to heap | heap after |
|---|---|---|---|---|---|
| 1 | A | 2 | [(A2, 3)] | - | {B3} |
| 2 | B | 2 | [(A2, 3), (B2, 4)] | - | {} |
| 3 | **idle** | - | [(B2, 4)] | A2 | {A2} |
| 4 | A | 1 | [(A1, 6)] | B2 | {B2} |
| 5 | B | 1 | [(A1, 6), (B1, 7)] | - | {} |
| 6 | **idle** | - | [(B1, 7)] | A1 | {A1} |
| 7 | A | 0, done | [] | B1 | {B1} |
| 8 | B | 0, done | [] | - | {} |

Heap and queue both empty → **`8`** ✓. Schedule: `A B _ A B _ A B`.

## ✅ Optimal solution
```python
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        """Minimum time units to run every task with cooldown n between repeats.

        Time:  O(T log 26) = O(T), T = total time units; at most 26 heap entries.
        Space: O(26) = O(1), the heap and the cooling queue.
        """
        heap = [-c for c in Counter(tasks).values()]    # MAX-heap of remaining counts
        heapq.heapify(heap)
        cooling = deque()                               # (count, tick it's ready after)

        time = 0
        while heap or cooling:
            time += 1
            if heap:
                left = heapq.heappop(heap) + 1          # run one copy
                if left < 0:                            # copies remain: cool it
                    cooling.append((left, time + n))
            # else: nothing ready, this tick is idle

            if cooling and cooling[0][1] == time:
                heapq.heappush(heap, cooling.popleft()[0])

        return time
```
**Time:** O(T) · **Space:** O(1)

## ⚠️ Gotchas
- **Ready at `time + n`, return at the end of that tick.** A task run at tick 1 with
  n = 2 can run again at tick 4. It re-enters the heap at the end of tick 3. Off by one
  here gives 6 (`time + n - 1`, cooldown violated) or 10 (`time + n + 1`, one idle too
  many per gap) for the first example.
- **`+ 1` on a negated count** means "one fewer". Writing `- 1` makes counts grow and
  the loop never ends.
- **`while heap or cooling`.** `while heap` stops at tick 2 above, with A and B still on
  the rack.
- **n = 0.** Parked at `time + 0`, returned in the same tick. Answer = len(tasks). Test it.
- **Don't push back a finished task.** `if left < 0` guards it; pushing a 0 creates
  phantom work.

## 🎤 Interview talking points
- *"Greedy: always run the task with the most copies left, because it's the one that
  forces idles. A max-heap for ready tasks, and a FIFO queue for cooling tasks, since
  they all cool for the same n."*
- *"O(T) with at most 26 heap entries."*
- *"There's a closed form too: `max(len(tasks), (maxCount - 1) * (n + 1) + numberOfTasksWithMaxCount)`.
  The most frequent task makes maxCount - 1 frames of size n + 1, plus one final row."*
  ← derive it from the `A B _ | A B _ | A B` picture.
- *"The simulation generalises (e.g. if they ask for the actual schedule); the formula
  doesn't."*

## 🔗 Transfer
Tomorrow (EP105, Reorganize String) is this problem with **n = 1** and a twist: instead
of counting time, you must actually **output** the arrangement, and if it's impossible,
say so. The cooling queue shrinks to a single held-out variable.

## 📹 Metadata
- **Title:** `Task Scheduler, the heap needs a cooling rack | Heap #11`
- **Thumbnail:** `heap + queue` (green block)
- **Short:** the kitchen stove with pans on the cooling rack, idle minute highlighted.
  50s.
