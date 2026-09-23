# EP106 · P11E13 · Minimum Number of Refueling Stops   [Hard]

**Pattern:** Heap (greedy + heap, retroactive) · **Link:** https://leetcode.com/problems/minimum-number-of-refueling-stops/description/

---

## 🎬 Hook
> "Don't decide at the gas station. **Drive past every one of them**, and only when the
> tank runs dry, reach back in time and say *'I should have stopped at the biggest
> station I passed.'* A heap is what makes that time travel legal."

## 📋 Problem, in your words
```
A car starts at 0 with startFuel litres, 1 litre per mile, and must reach
target. stations[i] = [position, fuel], sorted by position.
At a station you may take ALL its fuel (or skip it).

Return the minimum number of stops to reach target, or -1 if you can't.
Arriving with exactly 0 fuel counts as arriving.
```

## 🔢 The example
```
Input:  target = 100, startFuel = 10,
        stations = [[10, 60], [20, 30], [30, 30], [60, 40]]
Output: 2
Why:    stop at 10 (fuel to reach 70), stop at 60 (reach 110 >= 100)

Input:  target = 1, startFuel = 1, stations = []        -> 0
Input:  target = 100, startFuel = 1, stations = [[10, 100]]  -> -1
```

## 🧸 ELI5
> You're on a road trip and your friend in the passenger seat **writes down every gas
> station you drive past** and how much fuel it has. You never stop. You just keep
> driving.
>
> When the tank hits empty, you don't panic. You look at the list and say *"which
> station would have helped the most?"*, and you pretend you stopped there. That counts
> as one stop, the fuel goes in the tank, and you keep driving. Pretending is fine,
> because you **did** pass that station; you just decided late.
>
> ```
> tank reaches mile 10.     passed: [10: 60]            -> "stop" at 10: reach 70
> tank reaches mile 70.     passed: [20: 30, 30: 30, 60: 40]
>                                                        -> "stop" at 60: reach 110
> 110 >= 100. Two stops.
> ```
>
> Why the biggest? Each stop costs the same (one), so each one should buy as many miles
> as possible.

## 🐌 Brute force (say it, don't type it)
Try every subset of stations: **O(2ⁿ)**. The real alternative is a DP,
`dp[i] = farthest reach using i stops`, updated station by station: **O(n²)**. It's
correct and worth naming; the heap gets **O(n log n)**.

## 💡 The pattern reveal
**Signal:** "**minimum** number of stops" · each stop is a one-off resource · stations
sorted along a line.
**Therefore:** Shape D greedy + heap, the **retroactive** kind from the pattern card.

**Key insight:** think of `fuel` as **the farthest mile you can reach**, not what's in
the tank. Every station at or before that mile is *reachable*, so it goes into a
**max-heap** of fuel amounts. When `fuel < target` and nothing new is reachable, pop the
biggest passed station and add it. If the heap is empty, you're stuck.

```python
while fuel < target:
    while i < len(stations) and stations[i][0] <= fuel:
        heapq.heappush(passed, -stations[i][1])     # drove past it, remember it
        i += 1
    if not passed:
        return -1                                    # nothing left to regret
    fuel += -heapq.heappop(passed)                   # "I stopped there after all"
    stops += 1
```

Why this is safe: a stop at a station you passed is **still physically possible**,
because you were there when you had fuel. Choosing *when* to decide doesn't change which
choices exist, and deciding late means you decide with more information.

## 🔍 Dry run: the example
`fuel = 10` (farthest reachable mile), `stops = 0`, `passed = {}`.

| round | fuel < 100? | stations newly reachable (pos ≤ fuel) | passed heap | pop (refuel) | fuel after | stops |
|---|---|---|---|---|---|---|
| 1 | 10 yes | [10, 60] | {60} | 60 | 70 | 1 |
| 2 | 70 yes | [20, 30], [30, 30], [60, 40] | {40, 30, 30} | 40 | 110 | 2 |
| - | 110 no | stop | {30, 30} unused | - | - | **2** |

Answer **`2`** ✓. Round 2 is the lesson: three stations became reachable at once, and
the heap picked the 40 at mile 60 even though it was the **last** one passed. The two
30s are never used.

## ✅ Optimal solution
```python
class Solution:
    def minRefuelStops(self, target: int, startFuel: int, stations: List[List[int]]) -> int:
        """Fewest refuelling stops to reach target, or -1.

        Time:  O(n log n), each station pushed and popped at most once.
        Space: O(n), the heap of passed stations.
        """
        passed = []                     # MAX-heap of fuel at stations we've driven past
        fuel = startFuel                # farthest mile reachable so far
        stops = i = 0

        while fuel < target:
            # everything up to `fuel` is reachable: remember it, don't decide yet
            while i < len(stations) and stations[i][0] <= fuel:
                heapq.heappush(passed, -stations[i][1])
                i += 1

            if not passed:
                return -1               # dry, and no station behind us to regret

            fuel += -heapq.heappop(passed)      # retroactively stop at the best one
            stops += 1

        return stops
```
**Time:** O(n log n) · **Space:** O(n)

## ⚠️ Gotchas
- **`fuel` is a position, not a tank level.** Since you start at 0 and burn one litre per
  mile, "total fuel ever taken" equals "farthest mile reachable". Treating it as a tank
  and subtracting distances works but adds bugs.
- **`<=` on reachability.** A station exactly at `fuel` is reachable (arriving on empty
  counts). `<` fails `target=100, startFuel=10, stations=[[10,90]]`.
- **`while fuel < target`, not `<=`.** Reaching the target on 0 fuel is success.
- **Pop only when you need to.** Popping greedily at every station is plain greedy and
  gives too many stops. The heap is for the *regret*, not the drive.
- **Stuck check before popping.** `heappop` on an empty heap is an IndexError, and the
  empty heap *is* the -1 case.

## 🎤 Interview talking points
- *"I drive as far as I can, pushing every station I pass into a max-heap. When I can't
  reach the next one or the target, I pop the biggest and count a stop, as if I'd
  stopped there."*
- *"It's safe because I really did pass that station. I'm just deciding later, with
  more information."*
- *"Each stop costs 1, so each should buy the most fuel. That's the exchange argument
  for the greedy."*
- *"O(n log n). The DP alternative, farthest reach with i stops, is O(n²)."*

## 🔗 Transfer
This is the "retroactive greedy" the pattern card calls the deepest idea in the
pattern, and it comes back in EP108 Course Schedule III, where you take every course
and later **drop** the longest one when you run out of days. In between, EP107 IPO
uses the same "reachable things go in a heap" move with **two** heaps: one for
projects you can't afford yet, one for those you can.

## 📹 Metadata
- **Title:** `Refueling Stops, decide at the gas station AFTER you pass it | Heap #13`
- **Thumbnail:** `regret, then refuel` (red block)
- **Short:** the passenger writing down stations, then the tank hitting empty and the
  40 being picked. 50s.
