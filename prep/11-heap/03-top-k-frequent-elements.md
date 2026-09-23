# EP096 · P11E03 · Top K Frequent Elements   [Medium]

**Pattern:** Heap (top-k) · **Link:** https://leetcode.com/problems/top-k-frequent-elements/description/

---

## 🎬 Hook
> "Two patterns glued together. A hash map turns the array into **counts**, then
> yesterday's heap keeps the **k biggest counts**. The only new idea is that you push a
> **pair**, and Python compares pairs by their first element, so the count goes first."

## 📋 Problem, in your words
```
Given an integer array nums and k, return the k values that appear
most often.

  - any order of output is fine
  - the answer is guaranteed unique (no tie at the k-th place)
  - must beat O(n log n)
```

## 🔢 The example
```
Input:  nums = [1, 1, 1, 2, 2, 3], k = 2
Output: [1, 2]
Why:    1 appears 3 times, 2 appears twice, 3 once. Top two: 1 and 2.

Input:  nums = [1], k = 1
Output: [1]

Input:  nums = [4, 4, -1, -1, -1, 7], k = 1
Output: [-1]
```

## 🧸 ELI5
> A class votes for its favourite fruit. First you **tally**: one tick per vote on the
> whiteboard. Then you only need the **top 2 fruits**, so you pick up the tally cards
> one by one and keep two in your hand. When you're holding three, you drop **the one
> with the fewest votes**.
>
> ```
> votes:   apple apple apple  banana banana  cherry
> tally:   apple 3   banana 2   cherry 1
>
> hand:    [apple 3]
>          [banana 2, apple 3]
>          [cherry 1, banana 2, apple 3]  -> drop cherry (fewest)
> answer:  apple, banana
> ```
>
> Two separate jobs: counting (a dictionary), then choosing (the heap from EP95).

## 🐌 Brute force (say it, don't type it)
Count with a dict, then sort the dict's items by count descending and take the first
k. **O(n + u log u)** where u is the number of distinct values: sorting every distinct
value when you only need k of them. Close to optimal already; the heap tightens it to
**O(n + u log k)**.

## 💡 The pattern reveal
**Signal:** "**k most** frequent" · "better than O(n log n)".
**Therefore:** Pattern 9 hash-map count, then Pattern 11 top-k.

**Key insight:** "k most frequent" is "k **largest**" with frequency as the key. From
EP95: keep the k largest in a **min**-heap, evicting the weakest. The only change is
what you push:

```python
heapq.heappush(heap, (freq, val))    # tuples compare on freq first
```

Frequency first, because the tuple's first element is what `heapq` orders by. Value
second, as payload, and as a tie-breaker that is always an int, so comparing it can
never crash (pattern card, "what goes wrong" #2).

## 🔍 Dry run: `nums = [1, 1, 1, 2, 2, 3]`, `k = 2`

Step 1, count: `{1: 3, 2: 2, 3: 1}`.

Step 2, heap of `(freq, val)`, min on freq:

| (freq, val) pushed | heap after push | size > 2? | evicted | heap after |
|---|---|---|---|---|
| (3, 1) | [(3,1)] | no | - | [(3,1)] |
| (2, 2) | [(2,2), (3,1)] | no | - | [(2,2), (3,1)] |
| (1, 3) | [(1,3), (2,2), (3,1)] | yes | **(1, 3)** | [(2,2), (3,1)] |

Read off the values: **`[2, 1]`** ✓ (any order is accepted).

## ✅ Optimal solution
```python
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        """The k most frequent values, any order.

        Time:  O(n + u log k), n to count, u distinct values each pushed once.
        Space: O(u + k), the counter and the heap.
        """
        count = Counter(nums)               # value -> frequency

        heap = []                           # MIN-heap on frequency, size <= k
        for val, freq in count.items():
            heapq.heappush(heap, (freq, val))
            if len(heap) > k:
                heapq.heappop(heap)         # drop the least frequent of the k + 1

        return [val for freq, val in heap]
```
**Time:** O(n + u log k) · **Space:** O(u + k)

## ⚠️ Gotchas
- **`(freq, val)`, not `(val, freq)`.** Swap them and you get the k largest *values*:
  `[1,1,1,2,2,3]` returns `[2, 3]`, the two biggest numbers, not the two most common.
  The first example catches it, so run it.
- **Iterate `count.items()`, not `nums`.** Pushing once per occurrence puts the same
  value in the heap several times and the answer has duplicates.
- **The heap is not sorted.** `[val for _, val in heap]` is in heap order. That's fine
  here ("any order"), and not fine in EP97 where order matters.
- **`Counter.most_common(k)`** is the one-liner, and it uses `heapq.nlargest` inside.
  Mention it, then write the loop.

## 🎤 Interview talking points
- *"Count with a hash map, then top-k over the distinct values with a min-heap of size k
  keyed on frequency."*
- *"O(n + u log k). With u distinct values and k small, that's basically linear."*
- *"There's an O(n) answer too: **bucket sort** by frequency. A value can appear at most
  n times, so make n + 1 buckets, drop each value in bucket[freq], then walk from the
  top bucket down until you've collected k."* ← the follow-up they're fishing for.
- *"I put frequency first in the tuple because that's what `heapq` compares."*

## 🔗 Transfer
The count-then-heap shape comes back tomorrow in EP97 with one nasty addition: **ties
must be broken alphabetically, and the output must be in order**. That's where the
tuple trick gets pushed to its limit. Much later, EP104 Task Scheduler and EP105
Reorganize String start with this exact `Counter`, then use the heap greedily instead of
for top-k.

## 📹 Metadata
- **Title:** `Top K Frequent, count first, heap second | Heap #3`
- **Thumbnail:** `(freq, val)` (green block)
- **Short:** the fruit-vote whiteboard tally becoming three cards in a hand. 45s.
