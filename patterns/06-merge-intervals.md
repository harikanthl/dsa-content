# Pattern 06 — Merge Intervals

**7 episodes · EP 45–51**

---

## The one-sentence version

Two intervals have six possible relative positions; **sort by start time** and four of
them become impossible, so each interval only ever has to be compared with **one** thing
— the interval you're currently holding, or the earliest end time in a heap:
**O(n²) → O(n log n)**, and the log n is the sort.

## ELI5

Unsorted, `a` and `b` can sit six ways:

```
a: ---            a: ---           a:  ---          a: ------
b:      ---       b:   ---         b: ---           b:   --
   disjoint          overlap         b first         a contains b
                                                  ... and two mirror images
```

Sort by start, so `a` always begins first, and the mirrors vanish. What's left is a
single question:

> **Does `b` start before `a` ends?**

```
overlap  <=>  b.start <= a.end        (given a.start <= b.start)
```

That's one comparison instead of four, and it's why every episode in this pattern opens
with the same line of code:

```python
intervals.sort(key=lambda iv: iv[0])
```

Sorting isn't a preprocessing step here. **Sorting is the algorithm** — everything after
it is a single left-to-right sweep.

## How to recognise it

| Signal | Example |
|---|---|
| the input is pairs of `[start, end]` | all seven episodes |
| "merge", "overlap", "conflict", "collide" | Merge Intervals (EP45) |
| "how many at the same time" | Minimum Meeting Rooms (EP49) |
| two already-sorted lists of intervals | Intervals Intersection (EP47) |
| "free time", "gaps", "available slots" | Employee Free Time (EP51) |
| meetings, bookings, jobs, flights, lectures | the words the problem dresses it in |

**The question to ask before writing anything:** *are the intervals closed or
half-open?* It decides one character and it decides the answer:

| convention | `[1,4]` and `[4,5]` | test | episodes |
|---|---|---|---|
| **closed** `[s, e]` — the endpoint is included | **touch, so they merge** | `s <= prev_end` | EP45, EP46, EP47, EP51 |
| **half-open** `[s, e)` — the room empties at `e` | **no conflict, same room** | `s < prev_end` | EP48, EP49, EP50 |

Merging schedules and counting rooms genuinely disagree here, and both are right. Say
which one you're assuming out loud — in an interview that sentence is worth more than
the code.

## The shape

```python
def merge(intervals):
    intervals.sort(key=lambda iv: iv[0])       # the algorithm
    out = []
    for start, end in intervals:
        if out and start <= out[-1][1]:        # overlaps what I'm holding
            out[-1][1] = max(out[-1][1], end)  # extend -- MAX, never just `end`
        else:
            out.append([start, end])           # a genuine gap: start a new one
    return out
```

**Why `max(out[-1][1], end)` and not `end`:** a fully contained interval like `[2,3]`
inside `[1,10]` would otherwise *shrink* the merged result to `[1,3]`. Sorting by start
does **not** sort by end, and forgetting that is the bug of this pattern — it survives
every example where the intervals happen to be staircase-shaped and fails the moment
one swallows another.

## The three shapes you need

### 1. One list, one running interval (EP45, EP46, EP48, EP51)

Hold the current merged interval, compare, extend or flush. The *gaps* between the
merged results are as useful as the results — that's EP51's free time, and it's why
this shape answers both "what's busy" and "what's free" with the same sweep.

### 2. Two sorted lists, two pointers (EP47)

The intersection of two intervals is always the same formula, and it's worth memorising
as a shape rather than a line:

```python
lo, hi = max(a.start, b.start), min(a.end, b.end)
if lo <= hi:  # non-empty
    yield [lo, hi]
advance whichever interval ENDS FIRST      # the other one may still meet the next
```

Advancing by *end*, not by start, is the whole trick. The one that ends first is the one
that can never intersect anything later.

### 3. Counting concurrency — a heap of end times (EP49, EP50)

When the question is "how many overlap at once" rather than "what merges", stop merging
and start counting. A min-heap of end times answers *"has anything I'm holding finished
by the time this one starts?"*

```python
for start, end in sorted(meetings):
    while heap and heap[0] <= start:   # everything finished: free it
        heappop(heap)
    heappush(heap, end)
    best = max(best, len(heap))        # or a running sum, for EP50
```

The equivalent **sweep line** — sort starts and ends into two lists, walk both,
`+1` on a start and `−1` on an end — is the same algorithm with the heap replaced by
counting. Know both; the sweep is easier to say, the heap is easier to extend when each
interval carries a payload.

## Complexity

| Problem | Time | Space |
|---|---|---|
| EP45, EP48, EP49, EP50, EP51 | O(n log n) — the sort dominates | O(n) |
| EP46 (input pre-sorted) | **O(n)** — no sort needed | O(n) |
| EP47 (both pre-sorted) | **O(n + m)** | O(1) extra |
| brute force you're beating | O(n²) | O(1) |

If the input is *already sorted*, say so and drop the sort — EP46 and EP47 are on this
list precisely to make you check rather than reflexively sort.

## The episodes

| EP | Problem | Shape | The thing it teaches |
|---|---|---|---|
| 45 | Merge Intervals | one list | Sort by start; `max(end, …)` for the contained case. |
| 46 | Insert Interval | one list, pre-sorted | Three phases, no sort: before, absorb, after. |
| 47 | Intervals Intersection | two pointers | `[max(starts), min(ends)]`; advance the earlier end. |
| 48 | Overlapping Intervals | one list | After sorting, adjacent pairs are enough — and why. |
| 49 | Minimum Meeting Rooms | heap | Counting, not merging. Heap size *is* the answer. |
| 50 | Maximum CPU Load | heap + payload | The heap carries a value, so track a running sum. |
| 51 | Employee Free Time | one list | The **gaps** between merged intervals are the answer. |

## What "knowing this in your sleep" means

1. Why does sorting by start make one comparison enough? *(It kills the mirror cases:
   `b` can no longer start before `a`, so only "does `b` start before `a` ends?"
   remains.)*
2. Why `max(prev_end, end)` when merging? *(Sorting by start doesn't sort by end. A
   contained interval would shrink the result.)*
3. Do `[1,4]` and `[4,5]` overlap? *(Depends on the convention — closed merges them,
   half-open doesn't. Ask, then pick `<=` or `<`.)*
4. In the two-pointer intersection, which pointer advances? *(The interval that ends
   first; it can't meet anything further along.)*
5. When do you stop merging and start counting? *(When the question is "how many at
   once" — then it's a heap of end times, or a ±1 sweep, and the peak is the answer.)*
