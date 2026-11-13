"""Make a small language model better at a classification task from a few labelled examples, without training.

  lmreadout fit     --model ID --data items.jsonl --template t.txt --out task.npz [--labels A B ...] [--task NAME] [--auto]
  lmreadout sweep   --model ID --data items.jsonl --template t.txt [--labels A B ...] [--sizes 15 30 60 120] [--draws 20] [--auto]
  lmreadout eval    --model ID --readout task.npz --data heldout.jsonl
  lmreadout patch   --model ID --readout task.npz --out edited-model/
  lmreadout predict --model ID --readout a.npz [b.npz ...] --data items.jsonl [--out preds.jsonl]

  fit      work out the correction from your examples, print an honest score, save it
  sweep    show how it does with fewer examples, beside the untouched model and plain word counts
  eval     score a saved correction on new items
  patch    save a copy of the model with the correction written in
  predict  answer items with one or more saved corrections, leaving the model as it is

Your files:
  items.jsonl   one JSON object per line: the fields your prompt uses, plus "answer" (for fit, sweep and eval)
  t.txt         your prompt, with {{field}} where each field goes; it must end exactly where the answer goes

Answers: without --labels, every distinct "answer" in the data is used. Each answer is recognised by its first
token, so answers of several words are fine as long as they start differently.

--auto picks the settings from your examples and may decide to leave the model alone. It tries each combination of:
  lean      how much of the model's bias towards one answer to remove: none, half or all
  strength  how hard the correction overrides the model's own answer: 0, 0.5, 1, 2 or 4
  ridge     how much the correction is smoothed: n/4, n or 4n, for n examples
and keeps the one that scores best on examples held back from the fit. Ties go to a gentler strength on bigger
models. If some answer has fewer than two examples it cannot choose, so it only removes the bias.
"""
from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path

import numpy as np

from .core import (Readout, _rates, answer_tokens, collect, fill_template, fit, fit_auto, load_model, patch,
                   predict_items, sweep, template_fields, twofold)


def read_jsonl(path: str, limit: int = 0) -> list[dict]:
    with open(path) as fh:
        return [json.loads(line) for line in fh if line.strip()][: limit or None]


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


def _load(a, paths):
    """The model, its tokenizer and the read-outs, each checked against the model."""
    model, tok = load_model(a.model, a.device)
    readouts = [Readout.load(p) for p in paths]
    for r in readouts:
        check_model(model, r, a.model)
    return model, tok, readouts


def _task_inputs(a, tok, rows, template):
    """Answers, their rows, the prompt template as used, prompts, gold indices and the item texts (for word counts)."""
    if not all("answer" in r for r in rows):
        sys.exit("every item needs an 'answer' field")
    answers = [str(r["answer"]) for r in rows]
    labels = [str(x) for x in a.labels] if a.labels else sorted(set(answers))
    missing = sorted(set(answers) - set(labels))
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
    gold = np.array([labels.index(x) for x in answers])
    fields = template_fields(template)
    texts = [" ".join(str(r.get(f, "")) for f in fields) for r in rows]
    return labels, ids, used, prompts, gold, texts


def _collect_task(a):
    """fit / sweep: load the model, read the items, collect the states. Returns model, labels, ids, the template as
    used, gold, item texts, H, LAB, LSE."""
    model, tok = load_model(a.model, a.device)
    rows = read_jsonl(a.data, a.max_items)
    labels, ids, used, prompts, gold, texts = _task_inputs(a, tok, rows, read_template(a.template))
    print(f"collecting {len(prompts)} items", flush=True)
    H, LAB, LSE = collect(model, tok, prompts, ids, max_len=a.max_len, progress=True)
    return model, labels, ids, used, gold, texts, H, LAB, LSE


def _scores_lines(d, K):
    return (f"  accuracy:          commonest answer={d['majority']:.3f} as shipped={d['shipped']:.3f} "
            f"calibrated={d['calibrated']:.3f} edited={d['edited']:.3f}\n"
            f"  balanced accuracy: guessing={1 / K:.3f} as shipped={d['bal_shipped']:.3f} "
            f"calibrated={d['bal_calibrated']:.3f} edited={d['bal_edited']:.3f}")


def _settings(a, auto=False):
    """--lam / --alpha-mult, or none with fit --auto (which chooses them itself)."""
    if auto:
        if a.lam is not None or a.alpha_mult is not None:
            sys.exit("--auto chooses the ridge and strength itself; drop --lam / --alpha-mult, or drop --auto")
        return {}
    return dict(lam=a.lam, alpha_mult=2.0 if a.alpha_mult is None else a.alpha_mult)


def _n_params(model):
    return int(sum(p.numel() for p in model.parameters()))


def cmd_fit(a):
    kw = _settings(a, a.auto)                                    # before loading anything: a clash fails at once
    model, labels, ids, used, gold, _, H, LAB, LSE = _collect_task(a)
    npar = _n_params(model)
    try:
        tf = twofold(H, LAB, LSE, gold, auto=a.auto, n_params=npar, **kw)
    except ValueError as e:
        hint = " Each answer needs at least two labelled items." if "only one answer" in str(e) else ""
        sys.exit(f"cannot score on held-out halves: {e}.{hint}")
    if a.auto:
        print("two-fold with --auto: in each half the settings are chosen from that half alone", flush=True)
    print(f"two-fold (every item scored by a read-out that never saw it), n={tf['n']}\n" + _scores_lines(tf, len(labels)),
          flush=True)
    if tf["bal_edited"] < tf["bal_shipped"]:
        print("WARNING: on held-out items the edit scores below the model as shipped (balanced accuracy); check with "
              "`sweep` and more labelled items before using it.", flush=True)
    if tf["edited"] <= tf["majority"] + 0.02:
        print("WARNING: the read-out is at the commonest-answer rate on held-out items; the model does not know this "
              "task in a linearly readable form at the answer position. The saved read-out is not useful.", flush=True)
    meta = dict(task=a.task or Path(a.out).stem, twofold=tf, label_prefix=a.label_prefix)
    common = dict(model_id=a.model, labels=labels, label_ids=ids, template=used, meta=meta)
    if a.auto:
        r, t = fit_auto(H, LAB, LSE, gold, n_params=npar, **common)
        if t["fallback"]:
            print(f"--auto: fewer than two labelled items of {[labels[k] for k in t['fallback']]}, so no settings can "
                  "be chosen: removing the lean only (needs no labels), no read-out. Label more items of those answers "
                  "to let --auto choose.", flush=True)
        else:
            print(f"--auto on all {len(gold)} items ({t['folds']} folds; model {npar / 1e9:.2f}B parameters, ties go "
                  f"to strength {t['preferred_strength']}): lean {t['lean']}, strength {t['alpha_mult']}, ridge "
                  f"{t['lam_factor']} x n; cross-validated balanced accuracy {t['cv_bal']:.3f} "
                  f"(model unchanged {t['cv_unchanged']:.3f})", flush=True)
        if r is None:
            print("no setting beat the model unchanged on the labelled items: leave the model as it is. "
                  f"Nothing written to {a.out}.", flush=True)
            return
    else:
        r = fit(H, LAB, LSE, gold, **kw, **common)
    r.save(a.out)
    print(f"saved {a.out}", flush=True)


def cmd_sweep(a):
    model, labels, _, _, gold, texts, H, LAB, LSE = _collect_task(a)
    try:
        res = sweep(H, LAB, LSE, gold, texts=texts, sizes=a.sizes, draws=a.draws, seed=a.seed, **_settings(a),
                    auto=a.auto, n_params=_n_params(model))
    except ValueError as e:
        sys.exit(str(e))
    K = len(labels)
    print(f"each size N: {a.draws} random draws of N labelled items, every other item scored, mean over draws\n"
          f"balanced accuracy (guessing = {1 / K:.3f}), accuracy in brackets", flush=True)
    head = f"{'N':>6} {'as shipped':>16} {'calibrated':>16} {'word counts':>16} {'edited':>16}"
    print(head + (f" {'auto':>16}  fallback draws" if a.auto else ""))
    for r in res:
        cell = lambda k: f"{r['bal_' + k]:.3f} ({r[k]:.3f})"
        line = f"{r['n_fit']:>6} {cell('shipped'):>16} {cell('calibrated'):>16} {cell('wordcount'):>16} {cell('edited'):>16}"
        print(line + (f" {cell('auto'):>16}  {r['auto_fallback_draws']}" if a.auto else ""))
    if a.auto:
        print("edited = the fixed settings (all the lean, strength --alpha-mult, ridge --lam); auto = settings chosen "
              "from the N items alone. Fallback draws (an answer with under two of the N items): lean removed only, "
              "no read-out.\nsettings auto chose (lean / strength / ridge), count over the draws:", flush=True)
        for r in res:
            print(f"{r['n_fit']:>6}  {r['auto_choices']}")
    if a.csv and res:
        with open(a.csv, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(res[0]))
            w.writeheader(); w.writerows(res)
        print(f"wrote {a.csv}", flush=True)


def cmd_eval(a):
    model, tok, (r,) = _load(a, [a.readout])
    rows = read_jsonl(a.data, a.max_items)
    if not all("answer" in x for x in rows):
        sys.exit("every item needs an 'answer' field")
    ids, _ = answer_tokens(tok, r.labels, r.meta.get("label_prefix", " "))
    if ids != r.label_ids:
        sys.exit(f"answer tokens differ from the read-out's ({ids} vs {r.label_ids}); same model and tokenizer?")
    unknown = sorted({str(x["answer"]) for x in rows} - set(r.labels))
    if unknown:
        sys.exit(f"answers in the data that the read-out does not know: {unknown}")
    gold = np.array([r.labels.index(str(x["answer"])) for x in rows])
    prompts = [fill_template(r.template, x) for x in rows]
    H, LAB, _, OM = collect(model, tok, prompts, r.label_ids, max_len=a.max_len, progress=True, other_max=True)
    S, K = r.scores(H, LAB), len(r.labels)
    d = _rates(dict(shipped=LAB.argmax(1), calibrated=r.calibrated(H, LAB).argmax(1), edited=S.argmax(1)), gold)
    print(f"held-out n={len(gold)}, {K} answers\n" + _scores_lines(dict(d, majority=np.bincount(gold).max() / len(gold)), K)
          + f"\n  free next token is one of the answers: as shipped {(LAB.max(1) >= OM).mean():.1%}, "
          f"edited {(S.max(1) >= OM).mean():.1%}", flush=True)


def cmd_patch(a):
    model, tok, (r,) = _load(a, [a.readout])
    patch(model, r)
    model.save_pretrained(a.out); tok.save_pretrained(a.out)
    print(f"saved patched model to {a.out} (rows {r.label_ids} of the output table changed; everything else "
          "identical; saved in float32 with the output table untied)", flush=True)


def cmd_predict(a):
    model, tok, readouts = _load(a, a.readout)
    try:
        out = predict_items(model, tok, readouts, read_jsonl(a.data, a.max_items), max_len=a.max_len)
    except ValueError as e:
        sys.exit(str(e))
    fh = open(a.out, "w") if a.out else sys.stdout
    fh.writelines(json.dumps(o) + "\n" for o in out)
    if a.out:
        fh.close(); print(f"wrote {a.out}", flush=True)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="lmreadout", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--model", required=True, help="Hugging Face model id or local path")
    common.add_argument("--device", default=None, help="cuda or cpu (default: cuda when available)")
    items = argparse.ArgumentParser(add_help=False)
    items.add_argument("--max-len", type=int, default=1024, help="longest prompt in tokens; longer ones lose their start (default 1024)")
    items.add_argument("--max-items", type=int, default=0, help="use only the first N items (default: all)")
    task = argparse.ArgumentParser(add_help=False)
    task.add_argument("--label-prefix", default=" ", help="text put before each answer when it is turned into tokens (default: a space)")
    task.add_argument("--data", required=True, help="your examples, one JSON object per line")
    task.add_argument("--template", required=True, help="your prompt, as a text file")
    task.add_argument("--labels", nargs="+", default=None, help="the answers (default: every distinct answer in the data)")
    task.add_argument("--lam", type=float, default=None, help="how much the correction is smoothed (default: the number of examples)")
    task.add_argument("--alpha-mult", type=float, default=None, help="how hard the correction overrides the model's own answer (default 2)")
    task.add_argument("--auto", action="store_true", help="pick the settings from your examples "
                      "(fit: instead of --lam/--alpha-mult; sweep: adds an 'auto' column)")
    f = sub.add_parser("fit", parents=[common, items, task]); f.add_argument("--out", required=True)
    f.add_argument("--task", default=None); f.set_defaults(fn=cmd_fit)
    s = sub.add_parser("sweep", parents=[common, items, task])
    s.add_argument("--sizes", nargs="+", type=int, default=[15, 30, 60, 120], help="numbers of examples to fit on")
    s.add_argument("--draws", type=int, default=20, help="how many random sets of examples to try per size")
    s.add_argument("--seed", type=int, default=0); s.add_argument("--csv", default=None); s.set_defaults(fn=cmd_sweep)
    e = sub.add_parser("eval", parents=[common, items]); e.add_argument("--readout", required=True); e.add_argument("--data", required=True); e.set_defaults(fn=cmd_eval)
    p = sub.add_parser("patch", parents=[common]); p.add_argument("--readout", required=True); p.add_argument("--out", required=True); p.set_defaults(fn=cmd_patch)
    q = sub.add_parser("predict", parents=[common, items]); q.add_argument("--readout", nargs="+", required=True); q.add_argument("--data", required=True)
    q.add_argument("--out", default=None); q.set_defaults(fn=cmd_predict)
    a = ap.parse_args(argv)
    a.fn(a)


if __name__ == "__main__":
    main()
