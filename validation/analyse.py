"""Tabulates the sweep results and applies the three rules of PLAN.md. Written before any result was read.

Usage (from the repository root):  python validation/analyse.py
Reads validation/results/<task>.<model>.csv for every command in PLAN.md and prints a Markdown report. A command with
no results file is listed as "no result" and is never replaced or left out.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SIZES = (15, 30, 60, 120)
COLS = [("shipped", "As shipped"), ("calibrated", "Calibration only"), ("wordcount", "Word counts"),
        ("edited", "Fixed edit"), ("auto", "`--auto`")]
MODELS = [("qwen08", "Qwen3.5-0.8B (primary, 12 tasks)"), ("phi4mini", "Phi-4-mini (secondary, 4 tasks)")]


def planned(model):
    """Task slugs for a model, in the order of the commands in PLAN.md."""
    out = []
    for line in (ROOT / "PLAN.md").read_text().splitlines():
        m = re.match(rf"lmreadout sweep .*validation/results/([a-z_]+)\.{model}\.csv", line)
        if m:
            out.append(m.group(1))
    return out


def n_answers(task):
    with open(ROOT / "data" / f"{task}.jsonl") as fh:
        return len({json.loads(x)["answer"] for x in fh if x.strip()})


def load(task, model):
    p = ROOT / "results" / f"{task}.{model}.csv"
    if not p.exists():
        return None
    with open(p) as fh:
        return {int(r["n_fit"]): r for r in csv.DictReader(fh)}


def f(r, k):
    return float(r["bal_" + k])


def report(model, title):
    tasks = planned(model)
    res = {t: load(t, model) for t in tasks}
    print(f"\n## {title}\n")
    missing = [t for t in tasks if res[t] is None]
    if missing:
        print("**No result (crashed or refused; see the log):** " + ", ".join(f"`{t}`" for t in missing) + "\n")
    have = [t for t in tasks if res[t] is not None]

    for N in SIZES:
        print(f"### {N} examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)\n")
        print("| Task | Answers | Guessing | " + " | ".join(n for _, n in COLS) + " | Fallback draws of 20 |")
        print("|---|---|---|" + "---|" * (len(COLS) + 1))
        for t in tasks:
            K = n_answers(t)
            r = (res[t] or {}).get(N)
            if r is None:
                print(f"| `{t}` | {K} | {1 / K:.3f} | " + " | ".join("no result" for _ in COLS) + " | |")
                continue
            cells = [f"{f(r, k):.3f} ({float(r['bal_' + k + '_sd']):.3f})" for k, _ in COLS]
            print(f"| `{t}` | {K} | {1 / K:.3f} | " + " | ".join(cells) + f" | {r['auto_fallback_draws']} |")
        rows = [res[t][N] for t in have if N in res[t]]
        if rows:
            print("| **Mean over tasks with a result** | | | "
                  + " | ".join(f"**{sum(f(r, k) for r in rows) / len(rows):.3f}**" for k, _ in COLS) + " | |")
            print()
            for k, name in COLS[:-1]:
                above = sum(f(r, "auto") > f(r, k) + 1e-9 for r in rows)
                below = sum(f(r, "auto") < f(r, k) - 1e-9 for r in rows)
                print(f"- `--auto` against {name}: above on {above}, below on {below}, level on "
                      f"{len(rows) - above - below} of {len(rows)} tasks.")
        print()

    print("### Settings `--auto` chose (count over the 20 draws)\n")
    for t in have:
        for N in SIZES:
            if N in res[t]:
                print(f"- `{t}`, {N}: {res[t][N]['auto_choices']}")
    print()

    print("### The three rules\n")
    r15 = {t: res[t][15] for t in have if 15 in res[t]}
    r120 = {t: res[t][120] for t in have if 120 in res[t]}
    note = f" ({len(missing)} planned task(s) have no result and could not be judged.)" if missing else ""

    d1 = {t: f(r, "auto") - f(r, "shipped") for t, r in r15.items()}
    bad1 = {t: d for t, d in d1.items() if d < -0.02}
    print(f"**Rule 1 (no real harm at 15): {'FAIL' if bad1 else 'PASS'}.**{note} `--auto` minus as shipped, per task:")
    for t, d in d1.items():
        print(f"- `{t}`: {d:+.3f}" + ("  <- more than 0.02 below" if t in bad1 else ""))
    print()

    d2 = {t: f(r, "auto") - f(r, "edited") for t, r in r120.items()}
    bad2 = {t: d for t, d in d2.items() if d < -0.005}
    print(f"**Rule 2 (matches the fixed edit at 120): {'FAIL' if bad2 else 'PASS'}.**{note} `--auto` minus fixed "
          "edit, per task:")
    for t, d in d2.items():
        print(f"- `{t}`: {d:+.3f}" + ("  <- more than 0.005 below" if t in bad2 else ""))
    print()

    d3 = {t: f(r, "auto") - max(f(r, "shipped"), f(r, "calibrated")) for t, r in r15.items()}
    if d3:
        m3 = sum(d3.values()) / len(d3)
        print(f"**Rule 3 (level with the better safe choice at 15): {'FAIL' if m3 < -0.01 else 'PASS'}.**{note} "
              f"Mean over {len(d3)} tasks of `--auto` minus the better of as shipped and calibration only: "
              f"{m3:+.4f}. Per task:")
        for t, d in d3.items():
            print(f"- `{t}`: {d:+.3f}")
        print()

    # An extra view, not a rule: the same three numbers without the tasks where --auto fell back in most draws of 15.
    fb = [t for t, r in r15.items() if int(r["auto_fallback_draws"]) >= 10]
    if fb:
        keep = [t for t in r15 if t not in fb]
        print(f"### Extra view, not a rule: without the tasks where `--auto` fell back in at least 10 of 20 draws "
              f"of 15 ({', '.join('`' + t + '`' for t in fb)})\n")
        if keep:
            print(f"- Rule 1 quantity, worst task: {min(d1[t] for t in keep):+.3f} "
                  f"(`{min(keep, key=lambda t: d1[t])}`).")
            print(f"- Rule 3 quantity, mean over {len(keep)} tasks: {sum(d3[t] for t in keep) / len(keep):+.4f}.")
            print(f"- Fallback tasks only, Rule 3 quantity, mean over {len(fb)} tasks: "
                  f"{sum(d3[t] for t in fb) / len(fb):+.4f}.")
        print()


if __name__ == "__main__":
    print("# Held-out test of lmreadout 0.5.0: results")
    for model, title in MODELS:
        report(model, title)
