# EP049 · P06E05 · Minimum Meeting Rooms   [Hard]

**Pattern:** Merge Intervals · **Link:** https://www.geeksforgeeks.org/problems/attend-all-meetings-ii/1

---

## 🎬 Hook
> "How many rooms does this calendar need? Yesterday's sweep can't answer it, because
> you no longer care about the *last* meeting — you care about **every meeting still
> running**. The fix is a min-heap of end times, and then the answer isn't something you
> compute at the end. The answer is the size of the heap."

## 📋 Problem, in your words
```
Given n meetings as [start, end], return the MINIMUM number of rooms
needed so that every meeting can happen.

Equivalently: the maximum number of meetings running at the same moment.

Half-open [start, end): a meeting ending at 4 and one starting at 4 can
share a room -- the first is out before the second walks in.
```

## 🔢 The example
```
Input:  [[1,4], [2,5], [7,9]]
Output: 2            <- [1,4] and [2,5] overlap; [7,9] reuses a freed room

Input:  [[6,7], [2,4], [8,12]]
Output: 1            <- sorted, they're end to end; one room does it all

Input:  [[4,5], [2,3], [2,4], [3,5]]
Output: 2            <- the interesting one. Traced below.

Input:  [[1,4], [4,5]]
Output: 1            <- touching. Half-open, so one room.
```

## 🧸 ELI5
> You're the person handing out room keys. A meeting arrives; you ask one question:
>
> > *"Has anybody handed a key back yet?"*
>
> If yes, give that key to the new meeting. If no, cut a **new key** — and the total
> number of keys you ever cut is the answer.
>
> To answer that question fast you need to know the **earliest** time any current
> meeting finishes, and it must stay correct as meetings come and go. That's a min-heap
> of end times: the root is always the next room to free up.
>
> ```
> heap = [4, 5]     ->  root 4: the next room frees at 4
> new meeting starts at 3  ->  3 < 4, nobody's out yet  -> cut a new key
> new meeting starts at 4  ->  4 >= 4, that room is free -> reuse it
> ```
>
> And here's the neat part: **you never need to count the keys.** Every meeting either
> reuses a key (pop, then push — size unchanged) or gets a new one (push — size grows by
> one). So the heap's size *is* the number of rooms in use, and its largest size is the
> answer. Since it never shrinks below its peak, the size at the very end is that peak.

## 🐌 Brute force (say it, don't type it)
For each meeting's start time, count how many meetings contain it:
`max over s of |{m : m.start <= s < m.end}|`. **O(n²)**, no data structures, and it's a
good way to *state* the problem: the answer is the peak concurrency, and the peak can
only occur at a start time.

## 💡 The pattern reveal
**Signal:** intervals · "how many at once" / "minimum rooms" / "maximum concurrent".
**Therefore:** stop merging, start **counting**. Sort by start, min-heap of end times.

**Key insight:** this is the first episode where the sorted sweep alone is not enough.
EP45 and EP48 only ever needed the interval in your hand, because merging collapses the
past into one thing. Counting doesn't collapse: three meetings running at once are three
separate facts, each with its own end time. The heap is the memory that a single
variable can't provide.

```python
for start, end in sorted(meetings):
    if heap and heap[0] <= start:    # the earliest-finishing room is free
        heappop(heap)                #   reuse it
    heappush(heap, end)              # this meeting now occupies a room
# len(heap) == the answer
```

**Why a single `if` and not a `while`:** each meeting takes exactly one room, so you
need at most one free room per meeting. Popping every expired end would shrink the heap
below the peak and lose the answer. (If you'd rather pop them all — the natural thing
when each interval carries a payload, as in EP50 — then track `best = max(best,
len(heap))` explicitly instead of reading the final size.)

**🧨 The convention trap: `heap[0] <= start`, not `<`.** Half-open intervals mean a room
freed at exactly 4 is available to a meeting starting at 4. With `<` the input
`[[1,4],[4,5]]` demands two rooms, which no office would agree with.

## 🔍 Dry run — `[[4,5], [2,3], [2,4], [3,5]]`
Sorted by start: `[2,3], [2,4], [3,5], [4,5]`. `heap = []`.

| meeting | heap root (next free) | root ≤ start? | action | heap after | rooms |
|---|---|---|---|---|---|
| `[2,3]` | — | — | **new room** | `[3]` | 1 |
| `[2,4]` | 3 | 3 ≤ 2 ✗ | **new room** | `[3, 4]` | **2** |
| `[3,5]` | 3 | 3 ≤ 3 ✓ | pop 3, **reuse** | `[4, 5]` | 2 |
| `[4,5]` | 4 | 4 ≤ 4 ✓ | pop 4, **reuse** | `[5, 5]` | 2 |

Answer **2** ✓ — `len(heap)` at the end.

Rows 3 and 4 are the half-open convention paying off twice: `3 ≤ 3` and `4 ≤ 4` are both
reuses. Under a closed reading (`<` instead of `<=`) this calendar needs **3** rooms — one
character, one extra room.

## 🔍 Dry run — the sweep-line alternative, `[[1,4], [2,5], [7,9]]`
Same answer, no heap. Split the endpoints into two sorted lists and walk them:

```
starts: 1  2  7
ends:   4  5  9
```

| next event | `cur` | `best` |
|---|---|---|
| start 1 (1 < 4) | 1 | 1 |
| start 2 (2 < 4) | **2** | **2** |
| end 4 (7 ≥ 4) | 1 | 2 |
| end 5 (7 ≥ 5) | 0 | 2 |
| start 7 | 1 | 2 |

Answer **2** ✓

Two solutions, same complexity. The sweep is easier to explain and easier to get right;
the heap generalises to *"what else was true while those meetings ran"* — which is
exactly tomorrow's problem. Know both, and say why you picked the one you picked.

## ✅ Optimal solution — heap of end times
```python
from heapq import heappush, heappop

class Solution:
    def minMeetingRooms(self, meetings: List[List[int]]) -> int:
        """Minimum rooms for all meetings. Half-open [start, end).

        Time:  O(n log n) — sort, then n heap operations.
        Space: O(n) — the heap.
        """
        meetings.sort(key=lambda m: m[0])
        rooms = []                      # min-heap of END times, one per busy room

        for start, end in meetings:
            if rooms and rooms[0] <= start:    # earliest-finishing room is free
                heappop(rooms)                 #   take it back...
            heappush(rooms, end)               # ...and hand it to this meeting

        return len(rooms)               # never shrank below its peak
```

## ✅ Alternative — sweep line
```python
class Solution:
    def minMeetingRooms(self, meetings: List[List[int]]) -> int:
        """Same answer by walking starts and ends in time order.

        Time:  O(n log n) · Space: O(n)
        """
        starts = sorted(m[0] for m in meetings)
        ends = sorted(m[1] for m in meetings)

        i = j = cur = best = 0
        while i < len(starts):
            if starts[i] < ends[j]:     # someone arrives before anyone leaves
                cur += 1
                best = max(best, cur)
                i += 1
            else:                       # `>=`: a room frees exactly in time
                cur -= 1
                j += 1

        return best
```
**Time:** O(n log n) · **Space:** O(n)

## ⚠️ Gotchas
- **`rooms[0] <= start`** (heap) and **`starts[i] < ends[j]`** (sweep). Both encode
  "touching is fine"; both flip if the intervals are closed. Check the statement.
- **`if`, not `while`, in the heap version.** One meeting needs one room. A `while`
  drains the heap and `len(heap)` stops being the peak — if you prefer the `while`, you
  must track `best` yourself.
- **The heap holds end times, not intervals.** Nothing else is needed. Pushing `(end,
  start)` tuples works but signals you haven't decided what the heap is *for*.
- **Sort by start before touching the heap.** Out of order, a later meeting can free a
  room that hasn't been booked yet.
- **Answer is `len(rooms)`, not `max(...)` over anything.** Saying *"the heap size is
  the answer"* out loud is the cleanest possible summary of this solution.
- **The peak occurs at a start time**, never inside an interval — which is why only
  starts drive the loop.

## 🎤 Interview talking points
- *"This isn't a merging question, it's a counting question — the answer is peak
  concurrency."* ← reframe first.
- *"A min-heap of end times tells me the earliest room to free up; if it's free by the
  time the next meeting starts, I reuse it, otherwise I open a new one."*
- *"The heap never shrinks below its peak, so its final size is the answer."*
- *"There's a sweep-line version with the same complexity — sort starts and ends
  separately and walk both with ±1. I'd use the heap when each interval carries a
  payload I need while it's running."* ← names both and picks deliberately.

## 🔗 Transfer
The heap you just built is the same heap as tomorrow's. In EP50 each interval arrives
with a **CPU load** attached, so the heap stores `(end, load)` and you track a running
sum instead of a size — the peak of that sum is the maximum CPU load. Minimum rooms is
that problem with every load equal to 1.

## 📹 Metadata
- **Title:** `Minimum Meeting Rooms — the heap size IS the answer | Merge Intervals #5`
- **Thumbnail:** `HAND BACK THE KEY` (green block)
- **Short:** `[[1,4],[4,5]]` needing 1 room or 2, depending on one character. 45s.
