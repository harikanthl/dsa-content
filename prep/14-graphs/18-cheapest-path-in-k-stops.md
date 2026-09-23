# EP169 · P14E18 · Cheapest Flights Within K Stops   [Medium]

**Pattern:** Graphs · **Link:** https://leetcode.com/problems/cheapest-flights-within-k-stops/description/

---

## 🎬 Hook
> "Cheapest flight from A to B, but with **at most K stops**. Plain Dijkstra gets this
> wrong: it happily finds a cheap route with too many layovers and throws away the
> pricier direct one you actually needed. Yesterday's Bellman-Ford already has the fix
> built in. Round `i` means 'at most `i` flights'. So run **exactly K + 1 rounds**, and
> copy the array every round, or it quietly breaks."

## 📋 Problem, in your words
```
n cities, flights[i] = [from, to, price] (DIRECTED).
Return the cheapest price from src to dst using at most k STOPS,
or -1 if no such route exists.

  - k stops = k intermediate cities = at most k + 1 flights
```

## 🔢 The example
```
n = 4, flights = [[0,1,100], [1,2,100], [2,0,100], [1,3,600], [2,3,200]]
src = 0, dst = 3, k = 1

    0 --100--> 1 --600--> 3
    ^          |          ^
    100       100         |
    |          v          |
    +--------- 2 ---200---+

Output: 700      <- 0 -> 1 -> 3, one stop (city 1)
                    0 -> 1 -> 2 -> 3 costs only 400, but that's TWO stops

n = 3, flights = [[0,1,100], [1,2,100], [0,2,500]], src = 0, dst = 2
    k = 1  ->  200     (0 -> 1 -> 2, one stop allowed)
    k = 0  ->  500     (direct flight only)
```

## 🧸 ELI5
> You're booking flights and you refuse more than K layovers. So you plan in **rounds**:
>
> - Round 1: what's the cheapest way to everywhere using **1 flight**?
> - Round 2: using **at most 2 flights**? Take every flight once more, starting from
>   round 1's prices.
> - Stop after K + 1 rounds.
>
> The key word is *round 1's prices*. In round 2 you're only allowed to extend trips
> that were already booked **at the end of round 1**, not ones you booked a second ago
> in round 2, otherwise one round could chain two flights together and you'd sneak an
> extra layover in.
>
> ```
> k = 0 (one round), flights listed 0->1, 1->2, 0->2:
>   with a snapshot:   0->1 = 100, 1->2 uses OLD price of 1 (∞) -> skip, 0->2 = 500   ✓
>   without snapshot:  0->1 = 100, 1->2 uses NEW price of 1 (100) -> 200            ✗ two flights
> ```

## 🐌 Brute force (say it, don't type it)
DFS/BFS over every route of at most k + 1 flights and keep the cheapest: the number of
routes grows like (out-degree)^(k+1), exponential in k. The waste: two routes that
reach the same city with the same number of flights are both extended, even though only
the cheaper one matters. Bellman-Ford keeps exactly one price per city per round.

## 💡 The pattern reveal
**Signal:** shortest path **with a limit on the number of edges** ("at most K stops").
**Therefore:** Shape E: Bellman-Ford, **K + 1 rounds, from a snapshot**.

**Key insight:** in Bellman-Ford with a snapshot, after round `i`, `dist[v]` is the
cheapest route to `v` using at most `i` edges. So the answer is `dist[dst]` after
exactly **K + 1** rounds. No more (too many flights), no fewer.

```python
for _ in range(k + 1):                 # k stops = k + 1 flights
    prev = dist[:]                     # MANDATORY here
    for u, v, w in flights:
        if prev[u] + w < dist[v]:
            dist[v] = prev[u] + w
```

**Why not Dijkstra?** Dijkstra keeps one best price per city, regardless of how many
flights it took. Example 1: city 2 is reached for 200 in 2 flights, and that's what gets
stored. From there `2 → 3` gives 400 with 3 flights, over the limit. Dijkstra *can* be
fixed by making the state `(city, flights used)`, but that's a different, bigger
algorithm.

## 🔍 Dry run: example 1, `k = 1` → 2 rounds
`dist = [0, ∞, ∞, ∞]`. Flights in order: `0→1 (100)`, `1→2 (100)`, `2→0 (100)`,
`1→3 (600)`, `2→3 (200)`.

| round | snapshot `prev` | improvements (read from `prev`) | dist after |
|---|---|---|---|
| 1 | `[0, ∞, ∞, ∞]` | `0→1`: 0+100 = 100. `1→2`, `1→3`: prev[1] is ∞, skip | `[0, 100, ∞, ∞]` |
| 2 | `[0, 100, ∞, ∞]` | `1→2`: 100+100 = 200; `1→3`: 100+600 = **700**; `2→3`: prev[2] is ∞, skip | `[0, 100, 200, 700]` |

Stop after 2 rounds: `dist[3] = 700` ✓.

The cheaper 400 (`0→1→2→3`) would appear in round 3. It never runs. And in round 2,
`2→3` looks at `prev[2] = ∞`, not the 200 just written, which is the snapshot doing its
job.

## ✅ Optimal solution
```python
class Solution:
    def findCheapestPrice(self, n: int, flights: List[List[int]],
                          src: int, dst: int, k: int) -> int:
        """Cheapest src -> dst price using at most k stops (k + 1 flights), or -1.

        Time:  O(k * E), k + 1 rounds over every flight.
        Space: O(n), dist and the per-round snapshot.
        """
        INF = float('inf')
        dist = [INF] * n
        dist[src] = 0

        for _ in range(k + 1):                          # k stops = k + 1 flights
            prev = dist[:]                              # extend LAST round's routes only
            for u, v, w in flights:
                if prev[u] + w < dist[v]:
                    dist[v] = prev[u] + w

        return dist[dst] if dist[dst] < INF else -1
```
**Time:** O(k · E) · **Space:** O(n)

## ⚠️ Gotchas
- **The snapshot is mandatory.** Relax in place and one round can chain several flights,
  as in the ELI5: `k = 0` returns 200 instead of 500. Pattern card gotcha #3.
- **K + 1 rounds, not K.** K counts **stops** (cities in between); rounds count
  **flights**. Off by one here passes some tests and fails others.
- **Compare against `dist[v]`, read from `prev[u]`.** `dist[v]` may already have been
  improved this round by another flight; comparing against it keeps the better one.
- **`float('inf')` is safe here** because all prices are positive; `inf + w` is still
  `inf`. With negative weights you'd need the `!= INF` guard from EP168.
- **Unreachable within k → -1.** `dist[dst]` still infinite after the rounds.
- **src == dst** returns 0, which is correct: zero flights.

## 🎤 Interview talking points
- *"A limit on the number of edges is Bellman-Ford's round structure: after round i,
  dist is the best with at most i edges. K stops means K + 1 rounds."*
- *"I copy dist at the start of each round, so every round adds exactly one flight."*
  ← the line they're testing.
- *"Plain Dijkstra fails because it keeps one best price per city and forgets how many
  flights it took. A Dijkstra over (city, stops) states works, but this is simpler."*
- *"O(k · E) time, O(n) space."*

## 🔗 Transfer
EP168 relaxed V − 1 times to reach every simple path; today you stopped early on purpose.
"Best answer using at most `i` of something, built from the best using `i − 1`" is the
DP mindset of Pattern 15, and Bellman-Ford is really a DP over path length. Tomorrow
(EP170) goes back to the heap for a different question: not the cheapest *path*, but the
cheapest way to *connect everything*.

## 📹 Metadata
- **Title:** `Cheapest Flights Within K Stops, why Dijkstra fails | Graphs #18`
- **Thumbnail:** `prev = dist[:]` (orange block)
- **Short:** k = 0 returning 200 without the snapshot and 500 with it. 40s.
