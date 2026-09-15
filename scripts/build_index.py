#!/usr/bin/env python3
"""Regenerate CURRICULUM.md and progress.csv from curriculum/curriculum.json."""
import json, csv, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data = json.load(open(f"{ROOT}/curriculum/curriculum.json"))

# stable pattern order + folder mapping
FOLDERS = {
 "Two Pointers":"01-two-pointers","Fast & Slow pointers":"02-fast-slow",
 "Sliding Window":"03-sliding-window","Kadane":"04-kadane","Prefix Sum":"05-prefix-sum",
 "Merge Intervals":"06-merge-intervals","In-place Reversal of a LinkedList":"07-linkedlist-reversal",
 "Stack":"08-stack","Hash Maps":"09-hash-maps","Binary Search":"10-binary-search",
 "Heap":"11-heap","Recursion and Backtracking":"12-recursion-backtracking",
 "Tree":"13-tree","Graphs":"14-graphs","DP (Dynamic Programming)":"15-dp",
}
order = list(FOLDERS)
pat_idx = {p: i+1 for i, p in enumerate(order)}

# assign per-pattern episode numbers
counters = {}
for d in data:
    p = d["pattern"]
    counters[p] = counters.get(p, 0) + 1
    d["pat_no"] = pat_idx[p]
    d["pat_ep"] = counters[p]
    d["code"] = f"P{d['pat_no']:02d}E{d['pat_ep']:02d}"
    d["folder"] = FOLDERS[p]
    d["prep"] = f"prep/{FOLDERS[p]}/{d['pat_ep']:02d}-{d['slug']}.md"
json.dump(data, open(f"{ROOT}/curriculum/curriculum.json","w"), indent=1)

# ---- CURRICULUM.md ----
L = ["# The 186-Episode DSA Curriculum",
     "",
     "One video per problem. One problem per day. Source: *DSA Patterns Cheat Sheet*.",
     "",
     f"**{len(data)} episodes · {len(order)} patterns · 15 YouTube playlists**",
     "",
     "`EP` = global upload order (daily cadence). `CODE` = playlist position (P=pattern, E=episode).",
     ""]
for p in order:
    eps = [d for d in data if d["pattern"] == p]
    L += [f"## {pat_idx[p]:02d}. {p}  ·  {len(eps)} videos",
          "",
          "| EP | CODE | Problem | Diff | Prep sheet | Link |",
          "|---:|:---|:---|:---|:---|:---|"]
    for d in eps:
        link = f"[practice]({d['links'][0]})" if d["links"] else "—"
        extra = f" *(+{len(d['links'])-1} variants)*" if len(d["links"]) > 1 else ""
        sub = f" <sub>{d['subgroup']}</sub>" if d.get("subgroup") else ""
        L.append(f"| {d['ep']} | {d['code']} | {d['title']}{sub}{extra} | {d['difficulty'] or '—'} "
                 f"| [`sheet`]({d['prep']}) | {link} |")
    L.append("")
open(f"{ROOT}/curriculum/CURRICULUM.md","w").write("\n".join(L))

# ---- progress.csv ----
with open(f"{ROOT}/curriculum/progress.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["ep","code","pattern","problem","difficulty","prep_ready",
                "solved_clean","recorded","edited","uploaded","youtube_url","reps","last_rep_date"])
    for d in data:
        w.writerow([d["ep"], d["code"], d["pattern"], d["title"], d["difficulty"],
                    "N","N","N","N","N","","0",""])
print(f"wrote CURRICULUM.md ({len(data)} eps) and progress.csv")
