# EP087 · P10E17 · Book Allocation   [Medium]

**Pattern:** Binary Search · **Link:** https://www.geeksforgeeks.org/problems/allocate-minimum-number-of-pages0937/1

---

## 🎬 Hook
> "Share books among students so the busiest student reads as little as possible. If
> that sounds like yesterday's shipping problem, it is. **Packages became pages, days
> became students, and the code is character-for-character the same.** The skill today
> is noticing that before you start typing."

## 📋 Problem, in your words
```
arr[i] is the page count of book i. Give the books to k students:
  - every student gets at least one book
  - each student gets a CONTIGUOUS run of books (in order)
  - every book goes to exactly one student

Minimise the maximum pages any one student reads. Return -1 if k > n.
```

## 🔢 The example
```
Input:  arr = [12, 34, 67, 90], k = 2
Output: 113
Why:    [12, 34, 67] | [90]   -> 113 and 90, the max is 113.
        [12, 34] | [67, 90]   -> 46 and 157, worse.
        [12] | [34, 67, 90]   -> 12 and 191, worse.

Input:  arr = [15, 17, 20], k = 5  -> -1   (5 students, 3 books)
Input:  arr = [22, 23, 67], k = 1  -> 112  (one student reads everything)
```

## 🧸 ELI5
> The teacher sets a **reading limit**: "nobody reads more than `L` pages." Then she walks
> down the shelf handing books to the first student until the next book would break the
> limit, then starts on the next student.
>
> ```
> shelf: 12  34  67  90         k = 2 students
>
> limit 146:  [12 34 67] [90]         2 students  ✓
> limit 113:  [12 34 67] [90]         2 students  ✓
> limit 112:  [12 34] [67] [90]       3 students  ✗ we only have 2
> ```
>
> A generous limit needs few students, a strict limit needs many. "Enough students?"
> goes **no, no, yes, yes** as `L` grows. The strictest limit that still works is the
> answer.

## 🐌 Brute force (say it, don't type it)
Try every way to place `k - 1` dividers among the `n - 1` gaps between books, compute
the max for each, keep the smallest. That's **C(n−1, k−1)** splits, exponential in
general. A DP over (book, students) gets it to O(k · n²). Both work harder than needed,
because checking one limit is a single greedy pass.

## 💡 The pattern reveal
**Signal:** "**minimise the maximum**" · contiguous, in-order groups · checking one
limit is a greedy walk.
**Therefore:** Shape C, minimise flavour. And the recognition that matters more than
the pattern: **this is EP86.**

| EP86 Ship Packages | EP87 Book Allocation |
|---|---|
| packages, in order | books, in order |
| ship capacity | reading limit |
| days | students |
| `days_needed(cap) <= days` | `students_needed(L) <= k` |
| `[max(weights), sum(weights)]` | `[max(arr), sum(arr)]` |

**The one real difference:** every student must get at least one book, so if `k > n`
it's impossible, return `-1`. When `k <= n`, the greedy's "fewer than k students" is
always fixable (split a group to give an idle student a book, which never raises the
max), so `<= k` is still the right check.

## 🔍 Dry run: `[12, 34, 67, 90]`, `k = 2`
Range `[90, 203]`.

| step | lo | hi | mid | groups | students | ≤ 2? | new range |
|---|---|---|---|---|---|---|---|
| 1 | 90 | 203 | 146 | [12,34,67] [90] | 2 | ✓ | `hi = 146` |
| 2 | 90 | 146 | 118 | [12,34,67] [90] | 2 | ✓ | `hi = 118` |
| 3 | 90 | 118 | 104 | [12,34] [67] [90] | 3 | ✗ | `lo = 105` |
| 4 | 105 | 118 | 111 | [12,34] [67] [90] | 3 | ✗ | `lo = 112` |
| 5 | 112 | 118 | 115 | [12,34,67] [90] | 2 | ✓ | `hi = 115` |
| 6 | 112 | 115 | 113 | [12,34,67] [90] | 2 | ✓ | `hi = 113` |
| 7 | 112 | 113 | 112 | [12,34] [67] [90] | 3 | ✗ | `lo = 113` |
| - | 113 | 113 | stop | | | | answer **113** ✓ |

Only two groupings ever appear. The search is homing in on the exact limit where
`12 + 34 + 67 = 113` stops fitting, and the answer is that sum, a real group total.

## ✅ Optimal solution
```python
def find_pages(arr: list[int], k: int) -> int:
    """Minimum possible maximum pages per student, contiguous allocation.

    Time:  O(n log S), S = sum(arr): log S greedy passes.
    Space: O(1).
    """
    if k > len(arr):
        return -1                           # someone would get no book

    def students_needed(limit: int) -> int:
        students, pages = 1, 0
        for p in arr:
            if pages + p > limit:           # this book starts the next student
                students += 1
                pages = 0
            pages += p
        return students

    lo, hi = max(arr), sum(arr)             # someone reads the biggest book; one reads all
    while lo < hi:
        mid = (lo + hi) // 2
        if students_needed(mid) <= k:
            hi = mid                        # limit works; try stricter
        else:
            lo = mid + 1
    return lo
```
**Time:** O(n log S) · **Space:** O(1)

## ⚠️ Gotchas
- **`k > n` → `-1` before anything else.** It's the only line that isn't EP86.
- **`<= k`, not `== k`.** Fewer students than k at a given limit still means k can do it
  (hand an idle student one book off someone's pile). Writing `== k` breaks the
  monotonic predicate and gives wrong answers.
- **`lo = max(arr)`**, same reason as EP86: below it, some book fits nobody.
- **Contiguous.** If the books could be shuffled this would be a different, much harder
  problem (multiway partition, NP-hard). The shelf order is what makes the greedy valid.
- **Say the recognition out loud.** "This is Ship Packages with a different story" is
  worth more on camera than re-deriving it.

## 🎤 Interview talking points
- *"Minimise the maximum over contiguous groups, so I binary search the maximum. The
  check is a greedy walk: fill a student until the next book would exceed the limit."*
- *"Monotonic: a bigger limit never needs more students."*
- *"Range `[max(arr), sum(arr)]`, straight from the data."*
- *"It's the same algorithm as Capacity to Ship Packages; the only extra case is
  `k > n`."* ← the interviewer is often checking whether you know that.

## 🔗 Transfer
EP86 in costume, and tomorrow EP88, Split Array Largest Sum, is EP87 in another
costume, the LeetCode version. Three problems, one loop. Watch for the same shape later
in Painter's Partition and "minimise the largest segment" questions: any time the groups
are contiguous and you minimise the worst one.

## 📹 Metadata
- **Title:** `Book Allocation is Ship Packages in disguise | Binary Search #17`
- **Thumbnail:** `SAME CODE` (red block)
- **Short:** the side-by-side EP86 / EP87 table filling in row by row. 40s.
