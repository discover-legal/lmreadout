"""Command line: fit a read-out, evaluate it on held-out items, patch a model, or predict with side heads.

  lmreadout fit     --model ID --data items.jsonl --template t.txt --labels No Yes [MORE ...] --out task.npz [--task NAME]
  lmreadout eval    --model ID --readout task.npz --data heldout.jsonl
  lmreadout patch   --model ID --readout task.npz --out edited-model/
  lmreadout predict --model ID --readout a.npz [b.npz ...] --data items.jsonl [--out preds.jsonl]

items.jsonl: one JSON object per line with the template's fields and, for fit/eval, an "answer" field equal to
one of the labels. The template is a text file ending where the answer goes, with {{field}} placeholders.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import numpy as np

from .core import (Readout, accuracy, balanced_accuracy, collect, fill_template, fit, label_token_ids, load_model, patch,
                   predict_items, twofold)


def read_jsonl(path: str) -> list[dict]:
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()]


def _prep(a, labels, tok, rows, template):
    ids = label_token_ids(tok, labels, a.label_prefix)
    prompts = [fill_template(template, r) for r in rows]
    gold = np.array([labels.index(str(r["answer"])) for r in rows]) if all("answer" in r for r in rows) else None
    return ids, prompts, gold


def cmd_fit(a):
    model, tok = load_model(a.model, a.device)
    rows = read_jsonl(a.data)[: a.max_items or None]
    template = Path(a.template).read_text()
    ids, prompts, gold = _prep(a, a.labels, tok, rows, template)
    if gold is None:
        sys.exit("fit needs an 'answer' field on every item")
    if len(a.labels) < 2:
        sys.exit("fit needs at least two labels")
    print(f"collecting {len(prompts)} items", flush=True)
    H, LAB, LSE = collect(model, tok, prompts, ids, max_len=a.max_len, progress=True)
    tf = twofold(H, LAB, LSE, gold, lam=a.lam, alpha_mult=a.alpha_mult)
    print(f"two-fold (every item scored by a read-out that never saw it), n={tf['n']}, {len(a.labels)} labels\n"
          f"  accuracy:          commonest label={tf['majority']:.3f} as shipped={tf['shipped']:.3f} "
          f"calibrated={tf['calibrated']:.3f} edited={tf['edited']:.3f}\n"
          f"  balanced accuracy: guessing={1 / len(a.labels):.3f} as shipped={tf['bal_shipped']:.3f} "
          f"calibrated={tf['bal_calibrated']:.3f} edited={tf['bal_edited']:.3f}", flush=True)
    if tf["edited"] <= tf["majority"] + 0.02:
        print("WARNING: the read-out is at the majority rate on held-out items; the model does not know this task in a "
              "linearly readable form at the answer position. The saved read-out is not useful.", flush=True)
    r = fit(H, LAB, LSE, gold, model_id=a.model, labels=a.labels, label_ids=ids, template=template, lam=a.lam,
            alpha_mult=a.alpha_mult, meta=dict(task=a.task or Path(a.out).stem, twofold=tf))
    r.save(a.out)
    print(f"saved {a.out}", flush=True)


def cmd_eval(a):
    model, tok = load_model(a.model, a.device)
    r = Readout.load(a.readout)
    rows = read_jsonl(a.data)[: a.max_items or None]
    ids, prompts, gold = _prep(a, r.labels, tok, rows, r.template)
    if ids != r.label_ids:
        sys.exit(f"label tokens differ from the read-out's ({ids} vs {r.label_ids}); same model and tokenizer?")
    H, LAB, _ = collect(model, tok, prompts, ids, max_len=a.max_len, progress=True)
    if gold is None:
        sys.exit("eval needs an 'answer' field on every item")
    p0 = LAB.argmax(1); p1 = r.predict(H, LAB)
    maj = np.bincount(gold, minlength=len(r.labels)).max() / len(gold)
    print(f"held-out n={len(gold)}, {len(r.labels)} labels\n"
          f"  accuracy:          commonest label={maj:.3f} as shipped={accuracy(p0, gold):.3f} edited={accuracy(p1, gold):.3f}\n"
          f"  balanced accuracy: guessing={1 / len(r.labels):.3f} as shipped={balanced_accuracy(p0, gold):.3f} "
          f"edited={balanced_accuracy(p1, gold):.3f}", flush=True)


def cmd_patch(a):
    model, tok = load_model(a.model, a.device)
    r = Readout.load(a.readout)
    patch(model, r)
    model.save_pretrained(a.out); tok.save_pretrained(a.out)
    print(f"saved patched model to {a.out} (rows {r.label_ids} of lm_head changed; everything else identical)", flush=True)


def cmd_predict(a):
    model, tok = load_model(a.model, a.device)
    readouts = [Readout.load(p) for p in a.readout]
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
    common.add_argument("--device", default=None)
    common.add_argument("--max-len", type=int, default=1024, help="prompts are left-truncated to this many tokens")
    common.add_argument("--max-items", type=int, default=0)
    common.add_argument("--label-prefix", default=" ", help="text put before each label when tokenising (default: a space)")
    f = sub.add_parser("fit", parents=[common]); f.add_argument("--data", required=True); f.add_argument("--template", required=True)
    f.add_argument("--labels", nargs="+", required=True, help="two or more answer labels, each one token after --label-prefix"); f.add_argument("--out", required=True)
    f.add_argument("--task", default=None); f.add_argument("--lam", type=float, default=None, help="ridge strength (default: number of items)")
    f.add_argument("--alpha-mult", type=float, default=2.0); f.set_defaults(fn=cmd_fit)
    e = sub.add_parser("eval", parents=[common]); e.add_argument("--readout", required=True); e.add_argument("--data", required=True); e.set_defaults(fn=cmd_eval)
    p = sub.add_parser("patch", parents=[common]); p.add_argument("--readout", required=True); p.add_argument("--out", required=True); p.set_defaults(fn=cmd_patch)
    q = sub.add_parser("predict", parents=[common]); q.add_argument("--readout", nargs="+", required=True); q.add_argument("--data", required=True)
    q.add_argument("--out", default=None); q.set_defaults(fn=cmd_predict)
    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
