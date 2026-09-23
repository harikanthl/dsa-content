# EP051 · P06E07 · Employee Free Time   [Hard]

**Pattern:** Merge Intervals · **Link:** https://www.codertrain.co/employee-free-time

---

## 🎬 Hook
> "Find the times when *everybody* is free. It's rated Hard, and it is EP45 with one
> line moved: run the same merge sweep, but instead of collecting the intervals you
> merge, collect the **gaps between them**. The hard part of this problem is realising
> you already solved it a week ago."

## 📋 Problem, in your words
```
Given a schedule: a list of employees, each a list of NON-OVERLAPPING
intervals sorted by start time, return the finite list of intervals
during which ALL employees are free.

"Free" means no employee is busy. The answer excludes the time before
everyone's first meeting and after everyone's last -- only the gaps in
between are finite, so only those count.

Zero-length gaps are not intervals: if one meeting ends exactly when
the next begins, there is no free time there.
```

## 🔢 The example
```
Input:  [[[1,2], [5,6]], [[1,3]], [[4,10]]]
Output: [[3,4]]
Why:    busy = [1,3] (employees 1 and 2) then [4,10]. The only gap is 3 to 4.
        The [5,6] meeting sits INSIDE [4,10] and changes nothing.

Input:  [[[1,3], [6,7]], [[2,4]], [[2,5], [9,12]]]
Output: [[5,6], [7,9]]

Input:  [[[1,2]], [[2,3]]]
Output: []           <- touching. No gap, so no free time.
```

## 🧸 ELI5
> Forget who owns which meeting. Tip every employee's calendar into one pile:
>
> ```
> employee 1:  [1--3]      [6-7]
> employee 2:    [2--4]
> employee 3:    [2----5]        [9----12]
>
> all of it:   [1--3][2--4][2----5][6-7]  [9----12]
> sorted:      (1,3) (2,4) (2,5)   (6,7)  (9,12)
> ```
>
> Now press them flat exactly as in EP45, and watch the *holes*:
>
> ```
> busy:        ############         ##     #######
> time:        1    3 4 5  6  7  8  9      12
> free:                    ^^^^ 5-6   ^^^^ 7-9
> ```
>
> Every time the next meeting starts **after** everything you're holding has finished,
> the space between them is a moment when nobody is busy. That's the answer. Same loop
> as merging; you just keep the other half of it.

## 🐌 Brute force (say it, don't type it)
Mark every busy minute on a timeline and read off the unmarked stretches. **O(range)**,
not O(n), it depends on the size of the numbers rather than how many intervals there
are, which makes it useless for large timestamps. It's still the clearest statement of
what the answer *means*, so say it, then discard it for that exact reason.

## 💡 The pattern reveal
**Signal:** intervals from **several** sources · "free" / "gaps" / "available".
**Therefore:** flatten, sort by start, sweep, and emit what's **between** the merges.

**Key insight:** the per-employee structure is a decoy. Free-for-everyone means
free-in-the-union, and the union doesn't care who contributed what. Once flattened, the
question is the EP45 sweep with the output inverted:

```python
end = flat[0][1]                    # the running "busy until"
for s, e in flat[1:]:
    if s > end:                     # STRICTLY: a zero-length gap is not free time
        free.append([end, s])       # ...the gap is the answer
    end = max(end, e)               # ...and the max is still the max
```

`max(end, e)` is the containment guard from EP45, and it matters more here: a contained
meeting like `[5,6]` inside `[4,10]` would otherwise drag `end` backwards to 6 and
invent a free slot from 6 to 9 that nobody has.

**`s > end`, strictly.** Touching meetings leave a gap of length zero, which isn't an
interval. `[[1,2]], [[2,3]]` must return `[]`.

**🧨 The trap: flattening throws away the one thing that makes this "Hard".** Sorting
everything is O(n log n) where n is the total number of intervals. But each employee's
list **is already sorted**, so this is k sorted lists being merged, a min-heap does it
in **O(n log k)**. With 10 000 employees and 3 meetings each, that's the difference
between sorting 30 000 items and merging with a heap of 10 000. Interviewers who rate
this Hard are waiting for that observation, so volunteer it even if you write the simple
version.

## 🔍 Dry run: `[[[1,3], [6,7]], [[2,4]], [[2,5], [9,12]]]`
Flatten and sort by start: `(1,3), (2,4), (2,5), (6,7), (9,12)`.

Seed `end = 3` from the first interval.

| next | `s > end`? | gap emitted | `end = max(end, e)` |
|---|---|---|---|
| `(2,4)` | 2 > 3 ✗ | - | max(3, 4) = **4** |
| `(2,5)` | 2 > 4 ✗ | - | max(4, 5) = **5** |
| `(6,7)` | **6 > 5 ✓** | **`[5,6]`** | max(5, 7) = **7** |
| `(9,12)` | **9 > 7 ✓** | **`[7,9]`** | max(7, 12) = **12** |

Answer **`[[5,6], [7,9]]`** ✓

Row 2 is worth pausing on: `(2,5)` starts *before* `(2,4)` ends and extends *past* it.
It contributes no gap and it pushes `end` out to 5, which is what makes the next gap
start at 5 rather than 4. Sorting by start does not sort by end, once again.

## 🔍 Dry run: `[[[1,2], [5,6]], [[1,3]], [[4,10]]]` (the containment case)
Flattened: `(1,2), (1,3), (4,10), (5,6)`.

| next | `s > end`? | gap | `end` |
|---|---|---|---|
| - | - | - | seed `end = 2` |
| `(1,3)` | 1 > 2 ✗ | - | max(2, 3) = **3** |
| `(4,10)` | **4 > 3 ✓** | **`[3,4]`** | max(3, 10) = **10** |
| `(5,6)` | 5 > 10 ✗ | - | max(10, **6**) = **10** ← not 6 |

Answer **`[[3,4]]`** ✓

That last row is the whole reason `max` is there. Write `end = e` instead and the sweep
believes everyone is free from 6 onwards, inventing a gap that the `[4,10]` meeting
plainly contradicts.

## ✅ Optimal solution: flatten and sweep
```python
class Solution:
    def employeeFreeTime(self, schedule: List[List[List[int]]]) -> List[List[int]]:
        """Intervals where every employee is free.

        Time:  O(n log n), n = total intervals, dominated by the sort.
        Space: O(n), the flattened list.
        """
        flat = sorted((s, e) for employee in schedule for s, e in employee)

        free = []
        end = flat[0][1]                    # busy until here, so far

        for s, e in flat[1:]:
            if s > end:                     # strictly: a zero-length gap isn't free time
                free.append([end, s])       # the HOLE is the answer
            end = max(end, e)               # containment guard -- never just `e`

        return free
```

## ✅ Alternative: heap merge, O(n log k)
```python
from heapq import heapify, heappop, heapreplace

class Solution:
    def employeeFreeTime(self, schedule: List[List[List[int]]]) -> List[List[int]]:
        """Same sweep, but merging k already-sorted lists with a heap.

        Time:  O(n log k), k = number of employees.
        Space: O(k), one entry per employee.
        """
        # (start, end, which employee, index within that employee's list)
        heap = [(emp[0][0], emp[0][1], i, 0) for i, emp in enumerate(schedule) if emp]
        heapify(heap)

        free = []
        end = heap[0][1]

        while heap:
            s, e, who, idx = heap[0]
            if s > end:
                free.append([end, s])
            end = max(end, e)

            idx += 1
            if idx < len(schedule[who]):    # that employee has another meeting
                nxt = schedule[who][idx]
                heapreplace(heap, (nxt[0], nxt[1], who, idx))
            else:
                heappop(heap)

        return free
```
**Time:** O(n log n) or O(n log k) · **Space:** O(n) or O(k)

## ⚠️ Gotchas
- **`max(end, e)`.** Third episode of this pattern where this is the bug. Here it
  doesn't shrink an output interval, it *fabricates* free time that doesn't exist.
- **`s > end`, not `s >= end`.** Back-to-back meetings leave no free time.
  `[[[1,2]], [[2,3]]]` → `[]`.
- **Seed `end` from the first interval, then iterate from the second.** Seeding `end =
  0` invents a free slot from 0 to the first meeting, which the problem explicitly
  excludes.
- **Nothing before the first meeting or after the last.** Both are infinite, so the
  answer is finite by construction, no trailing append.
- **Don't merge per employee first.** Each employee's list is already disjoint; the
  union across employees is all you need.
- **Empty employees.** `schedule` can contain an empty list; the flatten version ignores
  it naturally, the heap version needs the `if emp` filter. Check that rather than
  assume.
- **The heap version's tuple must carry the employee index**, or you can't find their
  next meeting. Carrying `(end, start)` and losing the owner is the classic wrong
  first draft.

## 🎤 Interview talking points
- *"Free for everyone means free in the union of all the meetings, so I flatten,
  merge as usual, and return the gaps instead of the merged intervals."* ← lead here.
- *"I keep `max(end, e)` because a contained meeting would otherwise pull the busy
  boundary backwards and invent free time."*
- *"Flattening and sorting is O(n log n), but each employee's list is already sorted,
  merging k sorted lists with a heap is O(n log k), which matters when there are many
  employees with few meetings each."* ← the Hard part of this Hard problem.
- *"Strictly greater, so touching meetings produce no free interval."*

## 🔗 Transfer
That closes Pattern 06, and it closes it on the observation that the *gaps* of a sweep
are as much an answer as the sweep's output. The k-sorted-lists heap you just wrote is
the same machine as Merge K Sorted Lists, which returns in **Pattern 11 (Heap)** with
the intervals stripped away. Next is **Pattern 07 (In-place Reversal of a LinkedList,
EP52–57)**, which leaves arrays behind entirely: no sorting, no sweeping, just three
pointers and a very careful order of assignment.

## 📹 Metadata
- **Title:** `Employee Free Time, the gaps are the answer | Merge Intervals #7`
- **Thumbnail:** `KEEP THE HOLES` (green block)
- **Short:** the flattened timeline with the two holes highlighted. 45s.
