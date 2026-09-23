# EP108 · P11E15 · Course Schedule III   [Hard]

**Pattern:** Heap (greedy + heap, retroactive) · **Link:** https://leetcode.com/problems/course-schedule-iii/description/

---

## 🎬 Hook
> "Take every course. Every single one. The moment you blow a deadline, **drop the
> longest course you've taken so far**, and you're back on time with the same number of
> courses minus one, but with the most days freed. It's EP106's time travel in reverse:
> not 'which past option should I have taken', but **'which past choice should I undo.'**"

## 📋 Problem, in your words
```
courses[i] = [duration, lastDay]. Courses run one at a time, starting
on day 1, and course i must FINISH on or before lastDay.

Return the maximum number of courses you can take.
```

## 🔢 The example
```
Input:  [[100, 200], [200, 1300], [1000, 1250], [2000, 3200]]
Output: 3
Why:    100 (done day 100), 1000 (done 1100), 200 (done 1300).
        The 2000-day course would finish on 3300 > 3200.

Input:  [[5, 5], [4, 6], [2, 6]]
Output: 2          <- take the 4 and the 2, NOT the 5

Input:  [[3, 2], [4, 3]]
Output: 0          <- each is longer than its own deadline
```

## 🧸 ELI5
> Your backpack can only hold what you can carry **by each checkpoint**. You walk the
> trail in order of checkpoints, and at each one you **pick up everything** lying there.
>
> The instant the backpack is too heavy for the checkpoint you're at, you don't stop and
> agonise. You **throw out the heaviest thing in the bag**. You lose one item either way,
> so you might as well lose the one that frees the most room.
>
> ```
> sorted by deadline:  (5 days, by 5)  (4, by 6)  (2, by 6)
>
> take 5    day 5   <= 5 ok     bag [5]
> take 4    day 9   >  6 LATE   throw out the 5 -> day 4, bag [4]
> take 2    day 6   <= 6 ok     bag [4, 2]         -> 2 courses
> ```
>
> Taking the 5 first *looked* right: it was due first. The heap lets you change your
> mind when a better combination shows up.

## 🐌 Brute force (say it, don't type it)
Try every subset, check whether it fits when run in deadline order: **O(2ⁿ · n)**. The
DP over (course, day) is **O(n · maxDay)**, which at 10⁴ courses and days up to 10⁴ is
10⁸, borderline. Greedy + heap: **O(n log n)**.

## 💡 The pattern reveal
**Signal:** "maximum number" · deadlines · durations · you can only do one at a time.
**Therefore:** sort by deadline, then Shape D greedy + heap, the **undo** kind.

**Key insight:** two decisions, and both have a one-line justification:

| decision | why |
|---|---|
| process courses in **deadline order** | if any set of courses fits, it fits when run earliest-deadline-first (exchange argument) |
| when late, **drop the longest taken so far** | the count goes down by one whichever you drop; the longest frees the most days for the future |

The max-heap holds the durations of courses you've taken, so "longest taken so far" is
O(log n) to find and remove.

```python
heapq.heappush(taken, -duration)        # take it, no questions asked
day += duration
if day > last_day:
    day -= -heapq.heappop(taken)        # undo the longest (maybe this very one)
```

Note: the course you just took might itself be the longest. Then you've simply
declined it, and the code doesn't need a special case for that.

## 🔍 Dry run: `[[5, 5], [4, 6], [2, 6]]`
Sorted by deadline: `(5,5) (4,6) (2,6)`. `day = 0`, `taken = {}`.

| course (dur, last) | push, day | day > last? | pop longest | day after | taken |
|---|---|---|---|---|---|
| (5, 5) | day 5 | no | - | 5 | {5} |
| (4, 6) | day 9 | **yes**, 9 > 6 | **5** | 4 | {4} |
| (2, 6) | day 6 | no | - | 6 | {4, 2} |

`len(taken)` = **`2`** ✓.

The LeetCode example, for the "drop yourself" case: after (100,200), (1000,1250),
(200,1300) the day is 1300 with 3 courses. (2000, 3200) pushes the day to 3300 > 3200,
the longest is the 2000 itself, it comes straight back out: **3** ✓.

## ✅ Optimal solution
```python
class Solution:
    def scheduleCourse(self, courses: List[List[int]]) -> int:
        """Maximum number of courses finishable before their deadlines.

        Time:  O(n log n), the sort plus one push and at most one pop per course.
        Space: O(n), the heap.
        """
        courses.sort(key=lambda c: c[1])        # earliest deadline first
        taken = []                              # MAX-heap of durations taken
        day = 0

        for duration, last_day in courses:
            heapq.heappush(taken, -duration)    # take it
            day += duration
            if day > last_day:
                longest = -heapq.heappop(taken) # undo the longest so far
                day -= longest                  # (possibly the one just taken)

        return len(taken)
```
**Time:** O(n log n) · **Space:** O(n)

## ⚠️ Gotchas
- **Sort by deadline, not by duration.** Sorting by duration takes short courses in the
  wrong order and misses deadlines it could have met.
- **`if`, not `while`, when late.** Before this course the schedule was on time; one pop
  of the longest (≥ this course's duration) always restores it. A `while` is harmless
  but signals you haven't seen why.
- **`day -= longest`.** Forgetting to give the days back means every later course looks
  late.
- **Durations longer than their deadline** (`[3, 2]`) are pushed and immediately popped.
  No special case.
- **`courses.sort` mutates the input.** Fine on LeetCode; say `sorted(...)` if they care.

## 🎤 Interview talking points
- *"Earliest deadline first is the right order for any feasible set. Then I take every
  course and, if I'm late, drop the longest course taken so far."*
- *"Dropping any one course costs the same, one course. The longest frees the most time,
  so it's never worse."*
- *"That's a retroactive greedy: the heap remembers my past choices so I can undo the
  worst one. Same idea as refueling stops."*
- *"O(n log n), versus an O(n · maxDay) knapsack-style DP."*

## 🔗 Transfer
That closes the greedy family: EP103 pop-and-push, EP104/105 cooldowns, EP106/108
retroactive greedy, EP107 two heaps for unlock-and-choose. Tomorrow (EP109, Find Median
from Data Stream) the two heaps come back with a completely different job: not "locked
vs available", but **the lower half and the upper half** of everything seen so far.

## 📹 Metadata
- **Title:** `Course Schedule III, take everything, then undo the longest | Heap #15`
- **Thumbnail:** `drop the heaviest` (red block)
- **Short:** the backpack at the checkpoint, the 5 thrown out. 45s.
