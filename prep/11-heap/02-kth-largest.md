# EP095 · P11E02 · Kth Largest Element in an Array   [Medium]

**Pattern:** Heap (top-k) · **Link:** https://leetcode.com/problems/kth-largest-element-in-an-array/description/

---

## 🎬 Hook
> "Yesterday's code, one minus sign deleted, and it solves the opposite problem. To keep
> the **largest** k numbers you use a **min**-heap. If that sentence sounds wrong to you,
> this is the episode that makes it sound obvious."

## 📋 Problem, in your words
```
Given an integer array nums and k, return the k-th LARGEST element.

  - k-th largest in SORTED order, not k-th distinct:
    [3, 3, 2], k = 2 -> 3   (both 3s count)
  - 1 <= k <= len(nums)
  - the problem asks: can you do it without sorting?
```

## 🔢 The example
```
Input:  nums = [3, 2, 1, 5, 6, 4], k = 2
Output: 5
Why:    sorted descending [6, 5, 4, 3, 2, 1]; the 2nd is 5

Input:  nums = [3, 2, 3, 1, 2, 4, 5, 5, 6], k = 4
Output: 4          <- descending 6, 5, 5, 4: the two 5s both count
```

## 🧸 ELI5
> A talent show keeps a **top-2 podium**. Each new act performs, and if there are now
> three people on a two-person podium, somebody gets bumped off. Who? **The weakest
> person on the podium.**
>
> So the podium needs one fast question answered: *"who's the weakest one up here?"*
> That's a pile with the smallest on top: a min-heap.
>
> ```
> podium after each act (weakest on the left):
>   3        2 3       2 3  (1 bumped)     3 5  (2 bumped)
>   5 6  (3 bumped)    5 6  (4 bumped)
>                      ^ weakest on the podium = 2nd best overall
> ```
>
> The weakest of the top two is the second best. The answer is sitting on top.

## 🐌 Brute force (say it, don't type it)
`sorted(nums)[-k]`: **O(n log n)**. Works, and in an interview you say it first. Then:
*"I don't need everything in order, I only need to know the k-th, so I'll only keep k
things."*

## 💡 The pattern reveal
**Signal:** "k-th **largest**" · unsorted · "without sorting".
**Therefore:** top-k, Shape A, exactly as written on the pattern card.

**Key insight:** the heap's top is whoever you'd **evict**. Evicting from "the k
largest" means dropping the **smallest** of them. Smallest on top = min-heap = plain
`heapq`, no negation.

| EP | keep the k … | evict the … | heap type | in Python |
|---|---|---|---|---|
| 94 | smallest | largest | max-heap | push `-x` |
| 95 | largest | smallest | min-heap | push `x` |

The table is the entire lesson. Same six lines, flip the sign.

## 🔍 Dry run: `nums = [3, 2, 1, 5, 6, 4]`, `k = 2`

| x | heap after push | size > 2? evict | heap after | top |
|---|---|---|---|---|
| 3 | {3} | - | {3} | 3 |
| 2 | {2, 3} | - | {2, 3} | 2 |
| 1 | {1, 2, 3} | evict **1** | {2, 3} | 2 |
| 5 | {2, 3, 5} | evict **2** | {3, 5} | 3 |
| 6 | {3, 5, 6} | evict **3** | {5, 6} | 5 |
| 4 | {4, 5, 6} | evict **4** | {5, 6} | 5 |

Answer **`5`** ✓. Look at the `x = 1` row: the newcomer is pushed and is immediately the
weakest, so it's the one that leaves. Pushing first and trimming second means you never
write that comparison yourself.

## ✅ Optimal solution
```python
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        """k-th largest element (duplicates count separately).

        Time:  O(n log k), each push/pop is on a heap of at most k + 1.
        Space: O(k).
        """
        heap = []                           # MIN-heap of the k largest so far
        for x in nums:
            heapq.heappush(heap, x)
            if len(heap) > k:
                heapq.heappop(heap)         # evict the weakest of the k + 1

        return heap[0]                      # weakest of the top k = k-th largest
```
**Time:** O(n log k) · **Space:** O(k)

## ⚠️ Gotchas
- **Min-heap for largest.** If you reach for a max-heap here, stop and ask *"what am I
  evicting?"* Then the heap type picks itself.
- **Don't heapify everything and pop k times as your only answer.** `heapify(nums)` then
  `n - k` pops works too, O(n + (n - k) log n), but it holds all n. Mention it as an
  alternative, not the solution.
- **Not k-th distinct.** `[3, 3, 2]`, k = 2 is 3. No `set()`.
- **`heapq.nlargest(k, nums)[-1]`** is a legal one-liner. Know it; write the loop when
  they ask you to "implement it".
- **Quickselect is the follow-up.** Average O(n), worst O(n²) without a random pivot.
  LeetCode has adversarial tests that punish a fixed pivot.

## 🎤 Interview talking points
- *"Min-heap of size k. The top is the smallest thing I'm keeping, which is the one I'd
  evict, and at the end it's the k-th largest."*
- *"O(n log k). Also works on a stream: I never need the whole array."*
- *"Quickselect gets O(n) average by partitioning like quicksort and only recursing into
  one side. I'd pick the heap when I need a guaranteed bound or a stream."*
- *"EP94 is this with a max-heap. The rule is: the heap type is whatever makes the
  **evictee** O(1) to reach."* ← the sentence that shows you understand, not memorise.

## 🔗 Transfer
With EP94 and EP95 you have the template in both directions. Tomorrow (EP96, Top K
Frequent) the heap stops holding the numbers themselves and starts holding
`(frequency, number)` pairs, and the key you compare on comes from a hash map you built
first, straight out of Pattern 9.

## 📹 Metadata
- **Title:** `Kth Largest, the MIN-heap that keeps the biggest | Heap #2`
- **Thumbnail:** `evict the weakest` (green block)
- **Short:** the talent-show podium, with the side-by-side EP94/EP95 table at the end. 40s.
