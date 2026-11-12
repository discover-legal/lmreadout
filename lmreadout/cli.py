"""Command line: fit a read-out, sweep the number of labelled examples, evaluate on held-out items, patch a model, or
predict with side heads.

  lmreadout fit     --model ID --data items.jsonl --template t.txt [--labels A B ...] --out task.npz [--task NAME]
  lmreadout sweep   --model ID --data items.jsonl --template t.txt [--labels A B ...] [--sizes 15 30 60 120] [--draws 20]
  lmreadout eval    --model ID --readout task.npz --data heldout.jsonl
  lmreadout patch   --model ID --readout task.npz --out edited-model/
  lmreadout predict --model ID --readout a.npz [b.npz ...] --data items.jsonl [--out preds.jsonl]

items.jsonl: one JSON object per line with the template's fields and, for fit/sweep/eval, an "answer" field. The
template is a text file ending where the answer goes, with {{field}} placeholders. Without --labels the answers are
read from the data (every distinct "answer", sorted). Each answer is read from the row of its first token after
--label-prefix, so answers of several words work as long as their first tokens differ.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

from .core import (Readout, accuracy, answer_tokens, balanced_accuracy, collect, fill_template, fit, load_model, patch,
                   predict_items, sweep, template_fields, twofold)


def read_jsonl(path: str) -> list[dict]:
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def read_template(path: str) -> str:
    """The template file, without the line break(s) most editors add at the end: the answer goes right after the
    last character, so a trailing newline would move it to a new line."""
    t = Path(path).read_text()
    s = t.rstrip("\r\n")
    if s != t:
        print("note: removed the line break at the end of the template; the answer goes right after "
              f"{s[-20:]!r}", flush=True)
    return s


def check_model(model, r: Readout, model_id: str):
    d = model.get_output_embeddings().weight.shape[1]
    if r.mu_hat.shape[0] != d:
        sys.exit(f"the read-out was fitted on a model with hidden size {r.mu_hat.shape[0]}, this one has {d} "
                 f"(read-out fitted on {r.model_id!r})")
    if r.model_id and r.model_id != model_id:
        print(f"WARNING: the read-out was fitted on {r.model_id!r}, not {model_id!r}; it is only meaningful on the "
              "same weights", flush=True)


def _task_inputs(a, tok, rows, template):
    """Answers, their rows, the prompt template as used, prompts, gold indices and the item texts (for word counts)."""
    if not all("answer" in r for r in rows):
        sys.exit("every item needs an 'answer' field")
    labels = [str(x) for x in a.labels] if a.labels else sorted({str(r["answer"]) for r in rows})
    missing = sorted({str(r["answer"]) for r in rows} - set(labels))
    if missing:
        sys.exit(f"answers in the data that are not in --labels: {missing}")
    if len(labels) < 2:
        sys.exit("need at least two answers")
    try:
        ids, suffix = answer_tokens(tok, labels, a.label_prefix)
    except ValueError as e:
        sys.exit(str(e))
    whole = 2 if suffix else 1
    multi = [lab for lab in labels if len(tok(a.label_prefix + lab, add_special_tokens=False)["input_ids"]) > whole]
    print(f"{len(labels)} answers: {labels}" + (f"; read by their first token: {multi}" if multi else "")
          + (f"; the prompt ends with {suffix!r}" if suffix else ""), flush=True)
    used = template + suffix
    prompts = [fill_template(used, r) for r in rows]
    gold = np.array([labels.index(str(r["answer"])) for r in rows])
    fields = template_fields(template)
    texts = [" ".join(str(r.get(f, "")) for f in fields) for r in rows]
    return labels, ids, used, prompts, gold, texts


def _scores_lines(d, K):
    return (f"  accuracy:          commonest answer={d['majority']:.3f} as shipped={d['shipped']:.3f} "
            f"calibrated={d['calibrated']:.3f} edited={d['edited']:.3f}\n"
            f"  balanced accuracy: guessing={1 / K:.3f} as shipped={d['bal_shipped']:.3f} "
            f"calibrated={d['bal_calibrated']:.3f} edited={d['bal_edited']:.3f}")


def cmd_fit(a):
    model, tok = load_model(a.model, a.device)
    rows = read_jsonl(a.data)[: a.max_items or None]
    labels, ids, used, prompts, gold, _ = _task_inputs(a, tok, rows, read_template(a.template))
    print(f"collecting {len(prompts)} items", flush=True)
    H, LAB, LSE = collect(model, tok, prompts, ids, max_len=a.max_len, progress=True)
    try:
        tf = twofold(H, LAB, LSE, gold, lam=a.lam, alpha_mult=a.alpha_mult)
    except ValueError as e:
        sys.exit(f"cannot score on held-out halves: {e}. Each answer needs at least two labelled items.")
    print(f"two-fold (every item scored by a read-out that never saw it), n={tf['n']}\n" + _scores_lines(tf, len(labels)),
          flush=True)
    if tf["bal_edited"] < tf["bal_shipped"]:
        print("WARNING: on held-out items the edit scores below the model as shipped (balanced accuracy); check with "
              "`sweep` and more labelled items before using it.", flush=True)
    if tf["edited"] <= tf["majority"] + 0.02:
        print("WARNING: the read-out is at the commonest-answer rate on held-out items; the model does not know this "
              "task in a linearly readable form at the answer position. The saved read-out is not useful.", flush=True)
    r = fit(H, LAB, LSE, gold, model_id=a.model, labels=labels, label_ids=ids, template=used, lam=a.lam,
            alpha_mult=a.alpha_mult, meta=dict(task=a.task or Path(a.out).stem, twofold=tf, label_prefix=a.label_prefix))
    r.save(a.out)
    print(f"saved {a.out}", flush=True)


def cmd_sweep(a):
    model, tok = load_model(a.model, a.device)
    rows = read_jsonl(a.data)[: a.max_items or None]
    labels, ids, used, prompts, gold, texts = _task_inputs(a, tok, rows, read_template(a.template))
    print(f"collecting {len(prompts)} items", flush=True)
    H, LAB, LSE = collect(model, tok, prompts, ids, max_len=a.max_len, progress=True)
    try:
        res = sweep(H, LAB, LSE, gold, texts=texts, sizes=a.sizes, draws=a.draws, seed=a.seed, lam=a.lam,
                    alpha_mult=a.alpha_mult)
    except ValueError as e:
        sys.exit(str(e))
    K = len(labels)
    print(f"each size N: {a.draws} random draws of N labelled items, every other item scored, mean over draws\n"
          f"balanced accuracy (guessing = {1 / K:.3f}), accuracy in brackets", flush=True)
    print(f"{'N':>6} {'as shipped':>16} {'calibrated':>16} {'word counts':>16} {'edited':>16}")
    for r in res:
        cell = lambda k: f"{r['bal_' + k]:.3f} ({r[k]:.3f})"
        print(f"{r['n_fit']:>6} {cell('shipped'):>16} {cell('calibrated'):>16} {cell('wordcount'):>16} {cell('edited'):>16}")
    if a.csv and res:
        with open(a.csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(res[0]))
            w.writeheader(); w.writerows(res)
        print(f"wrote {a.csv}", flush=True)


def cmd_eval(a):
    model, tok = load_model(a.model, a.device)
    r = Readout.load(a.readout)
    check_model(model, r, a.model)
    rows = read_jsonl(a.data)[: a.max_items or None]
    if not all("answer" in x for x in rows):
        sys.exit("eval needs an 'answer' field on every item")
    ids, _ = answer_tokens(tok, r.labels, r.meta.get("label_prefix", " "))
    if ids != r.label_ids:
        sys.exit(f"answer tokens differ from the read-out's ({ids} vs {r.label_ids}); same model and tokenizer?")
    unknown = sorted({str(x["answer"]) for x in rows} - set(r.labels))
    if unknown:
        sys.exit(f"answers in the data that the read-out does not know: {unknown}")
    gold = np.array([r.labels.index(str(x["answer"])) for x in rows])
    prompts = [fill_template(r.template, x) for x in rows]
    H, LAB, _, OM = collect(model, tok, prompts, r.label_ids, max_len=a.max_len, progress=True, other_max=True)
    S = r.scores(H, LAB)
    p0, pc, p1 = LAB.argmax(1), r.calibrated(H, LAB).argmax(1), S.argmax(1)
    K = len(r.labels)
    maj = np.bincount(gold, minlength=K).max() / len(gold)
    print(f"held-out n={len(gold)}, {K} answers\n"
          f"  accuracy:          commonest answer={maj:.3f} as shipped={accuracy(p0, gold):.3f} "
          f"calibrated={accuracy(pc, gold):.3f} edited={accuracy(p1, gold):.3f}\n"
          f"  balanced accuracy: guessing={1 / K:.3f} as shipped={balanced_accuracy(p0, gold):.3f} "
          f"calibrated={balanced_accuracy(pc, gold):.3f} edited={balanced_accuracy(p1, gold):.3f}\n"
          f"  free next token is one of the answers: as shipped {(LAB.max(1) >= OM).mean():.1%}, "
          f"edited {(S.max(1) >= OM).mean():.1%}", flush=True)


def cmd_patch(a):
    model, tok = load_model(a.model, a.device)
    r = Readout.load(a.readout)
    check_model(model, r, a.model)
    patch(model, r)
    model.save_pretrained(a.out); tok.save_pretrained(a.out)
    print(f"saved patched model to {a.out} (rows {r.label_ids} of the output table changed; everything else "
          "identical; saved in float32 with the output table untied)", flush=True)


def cmd_predict(a):
    model, tok = load_model(a.model, a.device)
    readouts = [Readout.load(p) for p in a.readout]
    for r in readouts:
        check_model(model, r, a.model)
    rows = read_jsonl(a.data)[: a.max_items or None]
    out = predict_items(model, tok, readouts, rows, max_len=a.max_len)
    fh = open(a.out, "w") if a.out else sys.stdout
    for o in out:
        fh.write(json.dumps(o) + "\n")
    if a.out:
        fh.close(); print(f"wrote {a.out}", flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="lmreadout", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--model", required=True, help="Hugging Face model id or local path")
    common.add_argument("--device", default=None, help="cuda or cpu (default: cuda when available)")
    common.add_argument("--max-len", type=int, default=1024, help="prompts are left-truncated to this many tokens")
    common.add_argument("--max-items", type=int, default=0)
    common.add_argument("--label-prefix", default=" ", help="text put before each answer when tokenising (default: a space)")
    task = argparse.ArgumentParser(add_help=False)
    task.add_argument("--data", required=True); task.add_argument("--template", required=True)
    task.add_argument("--labels", nargs="+", default=None, help="the answers (default: every distinct answer in the data)")
    task.add_argument("--lam", type=float, default=None, help="ridge strength (default: number of fit items)")
    task.add_argument("--alpha-mult", type=float, default=2.0)
    f = sub.add_parser("fit", parents=[common, task]); f.add_argument("--out", required=True)
    f.add_argument("--task", default=None); f.set_defaults(fn=cmd_fit)
    s = sub.add_parser("sweep", parents=[common, task])
    s.add_argument("--sizes", nargs="+", type=int, default=[15, 30, 60, 120], help="numbers of labelled items to fit on")
    s.add_argument("--draws", type=int, default=20, help="random draws per size")
    s.add_argument("--seed", type=int, default=0); s.add_argument("--csv", default=None); s.set_defaults(fn=cmd_sweep)
    e = sub.add_parser("eval", parents=[common]); e.add_argument("--readout", required=True); e.add_argument("--data", required=True); e.set_defaults(fn=cmd_eval)
    p = sub.add_parser("patch", parents=[common]); p.add_argument("--readout", required=True); p.add_argument("--out", required=True); p.set_defaults(fn=cmd_patch)
    q = sub.add_parser("predict", parents=[common]); q.add_argument("--readout", nargs="+", required=True); q.add_argument("--data", required=True)
    q.add_argument("--out", default=None); q.set_defaults(fn=cmd_predict)
    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
