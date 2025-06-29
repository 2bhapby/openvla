#!/usr/bin/env python3
"""
parse_log.py

Parse a rollout log (txt) into per-task statistics and overall success rates,
and save the summary as JSON in /home/sanghyeok/openvla/outputs/summary.
"""

import os
import re
import json
import argparse
from typing import Dict, Any

def parse_log_to_summary(log_text: str) -> Dict[str, Any]:
    lines = [ln.strip() for ln in log_text.splitlines() if ln.strip()]
    stats: Dict[str, Dict[str, Any]] = {}

    total_success = 0
    total_failures = 0
    total_steps_success = 0
    # Match episode, success flag, and task name (case-insensitive .mp4)
    task_re = re.compile(r"--episode=(\d+)--success=(True|False)--task=(.+?)\.mp4", re.IGNORECASE)

    for i, line in enumerate(lines):
        m = task_re.search(line)
        if not m:
            continue

        episode = int(m.group(1))
        success = (m.group(2).lower() == "true")
        task    = m.group(3)

        # Next line holds "over N steps"
        steps = 0
        if i + 1 < len(lines):
            m2 = re.search(r"over\s+(\d+)\s+steps", lines[i+1], re.IGNORECASE)
            if m2:
                steps = int(m2.group(1))

        if task not in stats:
            stats[task] = {
                "start_episode": episode,
                "successes": 0,
                "failures": 0,
                "sum_steps_success": 0,
                "sum_steps_failure": 0
            }
        else:
            # record earliest episode
            stats[task]["start_episode"] = min(stats[task]["start_episode"], episode)

        if success:
            stats[task]["successes"] += 1
            stats[task]["sum_steps_success"] += steps
            total_steps_success += steps
            total_success += 1
        else:
            stats[task]["failures"] += 1
            stats[task]["sum_steps_failure"] += steps
            total_failures += 1

    # compute averages and success rates
    for task, v in stats.items():
        succ = v["successes"]
        fail = v["failures"]
        v["avg_steps_success"] = (v["sum_steps_success"] / succ) if succ else None
        v["avg_steps_failure"] = (v["sum_steps_failure"] / fail) if fail else None
        total = succ + fail
        v["success_rate"] = (succ / total) if total else None
        # drop intermediate sums
        del v["sum_steps_success"]
        del v["sum_steps_failure"]

    # extract overall rates
    overall_task_rate = None
    overall_total_rate = None
    mt = re.search(r"Current task success rate:\s*([\d.]+)", log_text, re.IGNORECASE)
    if mt:
        overall_task_rate = float(mt.group(1))
    mt2 = re.search(r"Current total success rate:\s*([\d.]+)", log_text, re.IGNORECASE)
    if mt2:
        overall_total_rate = float(mt2.group(1))

    return {
        "tasks": stats,
        "total_success": total_success,
        "total_failures": total_failures,
        "total_success_rate": (total_success / (total_success + total_failures)) if (total_success + total_failures) else None,
        "total_steps_success": total_steps_success / total_success if total_success else None,
    }

def main():
    parser = argparse.ArgumentParser(
        description="Parse rollout log and write summary JSON"
    )
    parser.add_argument("log_file", help="Path to the input log text file")
    parser.add_argument(
        "--summary-dir",
        default="/home/sanghyeok/openvla/outputs/summary",
        help="Directory to save the summary JSON"
    )
    args = parser.parse_args()

    os.makedirs(args.summary_dir, exist_ok=True)

    with open(args.log_file, "r", encoding="utf-8") as f:
        log_text = f.read()

    summary = parse_log_to_summary(log_text)

    base = os.path.splitext(os.path.basename(args.log_file))[0]
    out_path = os.path.join(args.summary_dir, f"{base}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"Saved summary JSON to {out_path}")

if __name__ == "__main__":
    main()
