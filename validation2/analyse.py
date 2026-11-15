"""Tabulates the sweep results of the second held-out test and applies the four rules of PLAN.md. Written before
any result was read.

Usage (from the repository root):  python validation2/analyse.py
Reads validation2/results/<task>.<model>.csv (lmreadout 0.6.0) and <task>.<model>.v050.csv (lmreadout 0.5.0) for
every command in PLAN.md and prints a Markdown report. A command with no results file is listed as "no result" and is
never replaced or left out.
"""
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SIZES = (15, 30, 60, 120)
# (results file, column in it, heading). The columns that do not depend on --auto are taken from the 0.6.0 run and
# checked against the 0.5.0 run below (same data, same draws: they should agree).
COLS = [("new", "shipped", "As shipped"), ("new", "calibrated", "Calibration only"), ("new", "wordcount", "Word counts"),
        ("new", "edited", "Fixed edit"), ("old", "auto", "0.5.0 `--auto`"), ("new", "auto", "0.6.0 `--auto`")]
MODELS = [("qwen08", "Qwen3.5-0.8B (primary, 12 tasks)"), ("phi4mini", "Phi-4-mini (secondary, 4 tasks)")]


def planned(model):
    """Task slugs for a model, in the order of the commands in PLAN.md."""
    out = []
    for line in (ROOT / "PLAN.md").read_text().splitlines():
        m = re.match(rf"lmreadout sweep .*validation2/results/([a-z_]+)\.{model}\.csv", line)
        if m:
            out.append(m.group(1))
    return out


def n_answers(task):
    with open(ROOT / "data" / f"{task}.jsonl") as fh:
        return len({json.loads(x)["answer"] for x in fh if x.strip()})


def load(task, model, suffix=""):
    p = ROOT / "results" / f"{task}.{model}{suffix}.csv"
    if not p.exists():
        return None
    with open(p) as fh:
        return {int(r["n_fit"]): r for r in csv.DictReader(fh)}


def f(r, k):
    return float(r["bal_" + k])


def rules123(name, key, R, tasks15, tasks120, note):
    """Rules 1 to 3 for one version's --auto. R[t][N] = {"new": row, "old": row}. Returns the three verdicts."""
    d1 = {t: f(R[t][15][key], "auto") - f(R[t][15]["new"], "shipped") for t in tasks15}
    bad1 = {t for t, d in d1.items() if d < -0.02}
    print(f"**Rule 1 (no real harm at 15), {name}: {'FAIL' if bad1 else 'PASS'}.**{note} `--auto` minus as shipped, "
          "per task:")
    for t, d in d1.items():
        print(f"- `{t}`: {d:+.3f}" + ("  <- more than 0.02 below" if t in bad1 else ""))
    print()
    d2 = {t: f(R[t][120][key], "auto") - f(R[t][120]["new"], "edited") for t in tasks120}
    bad2 = {t for t, d in d2.items() if d < -0.005}
    print(f"**Rule 2 (matches the fixed edit at 120), {name}: {'FAIL' if bad2 else 'PASS'}.**{note} `--auto` minus "
          "fixed edit, per task:")
    for t, d in d2.items():
        print(f"- `{t}`: {d:+.3f}" + ("  <- more than 0.005 below" if t in bad2 else ""))
    print()
    d3 = {t: f(R[t][15][key], "auto") - max(f(R[t][15]["new"], "shipped"), f(R[t][15]["new"], "calibrated"))
          for t in tasks15}
    m3 = sum(d3.values()) / len(d3) if d3 else float("nan")
    print(f"**Rule 3 (level with the better safe choice at 15), {name}: {'FAIL' if m3 < -0.01 else 'PASS'}.**{note} "
          f"Mean over {len(d3)} tasks of `--auto` minus the better of as shipped and calibration only: {m3:+.4f}. "
          "Per task:")
    for t, d in d3.items():
        print(f"- `{t}`: {d:+.3f}")
    print()
    return (not bad1, not bad2, not m3 < -0.01)


def report(model, title):
    tasks = planned(model)
    new = {t: load(t, model) for t in tasks}
    old = {t: load(t, model, ".v050") for t in tasks}
    print(f"\n## {title}\n")
    for name, res in (("0.6.0", new), ("0.5.0", old)):
        missing = [t for t in tasks if res[t] is None]
        if missing:
            print(f"**No result with {name} (crashed or refused; see the log):** "
                  + ", ".join(f"`{t}`" for t in missing) + "\n")
    have = [t for t in tasks if new[t] is not None and old[t] is not None]
    R = {t: {N: {"new": new[t][N], "old": old[t][N]} for N in SIZES if N in new[t] and N in old[t]} for t in have}
    n_missing = len(tasks) - len(have)
    note = f" ({n_missing} planned task(s) lack a result from one version and could not be judged.)" if n_missing else ""

    # the columns that do not depend on --auto must agree between the two runs
    worst = max((abs(f(R[t][N]["new"], k) - f(R[t][N]["old"], k)) for t in have for N in R[t]
                 for k in ("shipped", "calibrated", "wordcount", "edited")), default=0.0)
    print(f"Check: the largest difference between the two runs in any column that does not depend on `--auto` "
          f"(as shipped, calibration only, word counts, fixed edit) is {worst:.4f}.\n")

    for N in SIZES:
        print(f"### {N} examples (balanced accuracy, mean over 20 draws, spread over draws in brackets)\n")
        print("| Task | Answers | Guessing | " + " | ".join(n for _, _, n in COLS)
              + " | 0.6.0 minus 0.5.0 | Draws of 20 with an answer short of two examples |")
        print("|---|---|---|" + "---|" * (len(COLS) + 2))
        for t in tasks:
            K = n_answers(t)
            if t not in R or N not in R[t]:
                print(f"| `{t}` | {K} | {1 / K:.3f} | " + " | ".join("no result" for _ in COLS) + " | | |")
                continue
            r = R[t][N]
            cells = [f"{f(r[src], k):.3f} ({float(r[src]['bal_' + k + '_sd']):.3f})" for src, k, _ in COLS]
            short = r["new"].get("auto_short_draws", r["old"].get("auto_fallback_draws", ""))
            print(f"| `{t}` | {K} | {1 / K:.3f} | " + " | ".join(cells)
                  + f" | {f(r['new'], 'auto') - f(r['old'], 'auto'):+.3f} | {short} |")
        rows = [R[t][N] for t in have if N in R[t]]
        if rows:
            print("| **Mean over tasks with a result** | | | "
                  + " | ".join(f"**{sum(f(r[src], k) for r in rows) / len(rows):.3f}**" for src, k, _ in COLS)
                  + f" | **{sum(f(r['new'], 'auto') - f(r['old'], 'auto') for r in rows) / len(rows):+.4f}** | |")
            print()
            for src, k, name in COLS[:-1]:
                above = sum(f(r["new"], "auto") > f(r[src], k) + 1e-9 for r in rows)
                below = sum(f(r["new"], "auto") < f(r[src], k) - 1e-9 for r in rows)
                print(f"- 0.6.0 `--auto` against {name}: above on {above}, below on {below}, level on "
                      f"{len(rows) - above - below} of {len(rows)} tasks.")
        print()

    for name, key in (("0.6.0", "new"), ("0.5.0", "old")):
        print(f"### Settings {name} `--auto` chose (count over the 20 draws)\n")
        for t in have:
            for N in SIZES:
                if N in R[t]:
                    print(f"- `{t}`, {N}: {R[t][N][key]['auto_choices']}")
        print()

    print("### The four rules (0.6.0)\n")
    t15 = [t for t in have if 15 in R[t]]
    t120 = [t for t in have if 120 in R[t]]
    rules123("0.6.0", "new", R, t15, t120, note)
    bad4 = []
    print(f"**Rule 4 (not worse than 0.5.0):**{note} mean over tasks of 0.6.0's `--auto` minus 0.5.0's `--auto`:")
    for N in SIZES:
        ds = {t: f(R[t][N]["new"], "auto") - f(R[t][N]["old"], "auto") for t in have if N in R[t]}
        m = sum(ds.values()) / len(ds) if ds else float("nan")
        if m < 0:
            bad4.append(N)
        up = sum(d > 1e-9 for d in ds.values()); down = sum(d < -1e-9 for d in ds.values())
        print(f"- {N} examples: {m:+.4f} over {len(ds)} tasks (0.6.0 above on {up}, below on {down})"
              + ("  <- below 0" if m < 0 else ""))
    print(f"\n**Rule 4: {'FAIL' if bad4 else 'PASS'}.**\n")

    print("### For comparison: Rules 1 to 3 applied to 0.5.0's `--auto` on the same tasks\n")
    rules123("0.5.0", "old", R, t15, t120, note)


if __name__ == "__main__":
    print("# Second held-out test: lmreadout 0.6.0 beside 0.5.0, results")
    for model, title in MODELS:
        report(model, title)
