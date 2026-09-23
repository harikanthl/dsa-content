# EP050 · P06E06 · Maximum CPU Load   [Hard]

**Pattern:** Merge Intervals · **Link:** https://www.geeksforgeeks.org/maximum-cpu-load-from-the-given-list-of-jobs/

---

## 🎬 Hook
> "Same heap as yesterday, one change: every job now carries a **load**. So instead of
> asking how many jobs run at once, you ask how much CPU they're burning at once, and
> `len(heap)` stops being the answer. It becomes a running sum. This is the episode that
> shows why the heap version was worth learning: the payload rides along with the end
> time."

## 📋 Problem, in your words
```
Given n jobs, each [start, end, cpu_load], all running on one machine,
find the MAXIMUM CPU load at any moment in time.

Jobs overlap freely. The load at a moment is the sum of the loads of
every job running at that moment.

Half-open [start, end): a job ending at 4 has released its load before
a job starting at 4 claims any.
```

## 🔢 The example
```
Input:  [[1,4,3], [2,5,4], [7,9,6]]
Output: 7            <- between 2 and 4, jobs 1 and 2 both run: 3 + 4

Input:  [[6,7,10], [2,4,11], [8,12,15]]
Output: 15           <- nothing overlaps; the answer is just the biggest single load

Input:  [[1,4,2], [2,4,1], [3,6,5]]
Output: 8            <- all THREE overlap between 3 and 4: 2 + 1 + 5
```
The second example is the sanity check people skip: with no overlap at all, the answer
is `max(load)`, not `0` and not the sum. If your code returns something else there, the
bug is in the initialisation.

## 🧸 ELI5
> Yesterday you handed out room keys and counted them. Today each meeting brings a
> **weight** into the room, and you're asking how heavy the building ever gets.
>
> ```
> job [1,4,3]   ###(3)
> job [2,5,4]     ####(4)
> job [7,9,6]              ###(6)
> time:         1 2 3 4 5   7 8 9
> load:         3 7 7 4 0   6 6 6
>                 ^ peak 7
> ```
>
> Walk the jobs in start order carrying a running total:
>
> - Before a job starts, **retire** everything that has already finished, subtract its
>   load.
> - Add the new job's load.
> - The running total is the load right now. Remember the largest you ever see.
>
> "Everything that has already finished" is the min-heap again, keyed on end time, but
> now each entry is a pair `(end, load)`, so when you pop it you know exactly how much
> to subtract.

## 🐌 Brute force (say it, don't type it)
For every job's start time, sum the loads of all jobs covering it. **O(n²)**, and it's
the definition of the answer, so it's the right thing to say before optimising. It also
names the key fact: the peak can only happen at a **start** time, because load only ever
goes up when a job begins.

## 💡 The pattern reveal
**Signal:** intervals · each with a **value** · "maximum concurrent / total at once".
**Therefore:** sort by start, min-heap of `(end, load)`, running sum, track the peak.

**Key insight:** EP49 got away with `len(heap)` because every meeting weighed exactly 1.
Attach a load, and the size of the heap stops meaning anything, you need the **sum of
what's in it**. Two consequences, and both are code changes:

| | EP49 rooms | EP50 CPU load |
|---|---|---|
| heap entry | `end` | `(end, load)` |
| retire expired | `if`, at most one room is needed | **`while`**: retire *all* of them |
| the answer | `len(heap)` at the end | `best = max(best, cur)` **inside** the loop |

**Why `while` and not `if`:** yesterday one meeting needed at most one room, so one pop
sufficed. Here, three jobs can finish before the next one starts, and every one of them
must give its load back or the running sum stays permanently inflated. A single `if`
under-retires and reports a peak that never happened.

**Why track `best` inside the loop:** the running sum goes up *and down*, so unlike the
heap's size there is no "it never shrank below its peak" argument to lean on. Read the
maximum as you go or lose it.

## 🔍 Dry run: `[[1,4,3], [2,5,4], [7,9,6]]`
Sorted by start (already). `heap = []`, `cur = 0`, `best = 0`.

| job | retire (`end <= start`) | `cur` | `best` | heap after |
|---|---|---|---|---|
| `[1,4,3]` | nothing | 0 + 3 = **3** | **3** | `[(4,3)]` |
| `[2,5,4]` | root end 4 ≤ 2? ✗ | 3 + 4 = **7** | **7** | `[(4,3), (5,4)]` |
| `[7,9,6]` | 4 ≤ 7 ✓ → −3; 5 ≤ 7 ✓ → −4 | 0 + 6 = **6** | 7 | `[(9,6)]` |

Answer **7** ✓

The last row is the `while` loop earning its keep: **two** jobs retire before the third
starts. With an `if`, only `(4,3)` would leave, `cur` would be `0 + 4 + 6 = 10`, and the
function would claim a peak of 10 that no moment in time ever had.

## 🔍 Dry run: `[[1,4,2], [2,4,1], [3,6,5]]` (three at once)

| job | retire | `cur` | `best` | heap after |
|---|---|---|---|---|
| `[1,4,2]` | - | **2** | 2 | `[(4,2)]` |
| `[2,4,1]` | 4 ≤ 2 ✗ | **3** | 3 | `[(4,1), (4,2)]` |
| `[3,6,5]` | 4 ≤ 3 ✗ | **8** | **8** | `[(4,1), (4,2), (6,5)]` |

Answer **8** ✓, all three overlap in `[3, 4)`, and the heap holds all three because
nothing has ended yet. Note the two entries with the same end time `4`: heap order
between them is arbitrary and it does not matter, because they both get retired by the
same comparison.

## ✅ Optimal solution
```python
from heapq import heappush, heappop

class Solution:
    def maxCPULoad(self, jobs: List[List[int]]) -> int:
        """Maximum total CPU load at any instant. Jobs are [start, end, load].

        Time:  O(n log n), sort, then n pushes and at most n pops.
        Space: O(n), the heap.
        """
        jobs.sort(key=lambda j: j[0])

        running = []          # min-heap of (end, load) for jobs currently alive
        current = best = 0

        for start, end, load in jobs:
            # retire EVERY job that has finished -- `while`, not `if`
            while running and running[0][0] <= start:
                current -= heappop(running)[1]

            heappush(running, (end, load))
            current += load
            best = max(best, current)     # the sum goes down too: read the peak here

        return best
```
**Time:** O(n log n) · **Space:** O(n)

## ⚠️ Gotchas
- **`while`, not `if`.** The headline difference from EP49. `[[1,4,3],[2,5,4],[7,9,6]]`
  returns 10 instead of 7 with an `if`, a peak that never existed.
- **Track `best` inside the loop.** `current` falls as jobs retire, so the final value
  is meaningless. There's no `len(heap)` shortcut here.
- **`best = 0` is safe only if loads are non-negative.** They are, by the statement, so
  the no-overlap example returns `max(load)` correctly. If loads could be negative,
  seed with the first job's load instead.
- **Heap entries are `(end, load)`.** Ordering is by end time, which is what `heapq`
  does with the first tuple element. Equal ends compare the loads next, harmless, and
  worth knowing rather than being surprised by.
- **`<= start`**, matching EP49's half-open convention: a job ending exactly when
  another starts has already released its load.
- **Sort by start, not by load.** Sorting by load is a different (greedy scheduling)
  problem and it does not answer this one.

## 🎤 Interview talking points
- *"Same shape as minimum meeting rooms, but each interval carries a weight, so the heap
  stores `(end, load)` and I track a running sum instead of the heap's size."* ← naming
  the reuse is the answer.
- *"I retire every finished job before adding the new one, `while`, not `if`, because
  several can finish in the same gap."*
- *"The peak can only occur at a start time, so checking once per job is enough."*
- *"Minimum meeting rooms is this problem with every load equal to 1."* ← the sentence
  that shows you see the family, not the problem.

## 🔗 Transfer
That's the heap shape complete: count (EP49), then sum (EP50). Tomorrow (EP51) closes
Pattern 06 by going back to merging, but keeping the **gaps** instead of the merged
intervals. Same sweep as EP45, opposite output, and the last thing this pattern has to
teach.

## 📹 Metadata
- **Title:** `Maximum CPU Load, the heap carries a payload | Merge Intervals #6`
- **Thumbnail:** `(END, LOAD)` (green block)
- **Short:** `if` vs `while`, the same input reporting a peak of 10 that never happened. 45s.
