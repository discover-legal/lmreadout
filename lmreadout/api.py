"""The read-out as something you call: a Classifier object around a model, and a decorator that turns a function
writing a prompt into a function returning the answer.

    from lmreadout import Classifier, classifier

    clf = Classifier.fit("Qwen/Qwen3.5-0.8B", examples, template="Clause: {{text}}\\nGoverning law clause?")
    clf("This Agreement is governed by the laws of Delaware.")        # -> "Yes"

    @classifier("Qwen/Qwen3.5-0.8B", examples=[("Either party may terminate.", "No"), ...], cache="law.npz")
    def governing_law(clause):
        return f"Clause: {clause}\\nGoverning law clause?"
    governing_law("This Agreement is governed by the laws of Delaware.")   # -> "Yes"

By default the settings are chosen from the examples (core.fit_auto), which may leave the model as it is; the
Classifier then gives the model's own answer among the labels. The model's weights are not touched unless you call
patch(), patched() or export().
"""
from __future__ import annotations

import functools
import hashlib
import inspect
import json
import threading
import warnings
from pathlib import Path

import numpy as np

from .core import (Readout, answer_tokens, collect, fill_template, fit, fit_auto, load_model, patch, patched, sweep,
                   template_fields, twofold)

_MODELS: dict = {}                       # (model id, device) -> (model, tokenizer): tasks on one model share it
_LOCK = threading.Lock()


def _resolve_model(model, tokenizer=None, device=None):
    """(model, tokenizer, model id) from a model id, a (model, tokenizer) pair, or a loaded model plus tokenizer."""
    if isinstance(model, (str, Path)):
        key = (str(model), device)
        with _LOCK:
            if key not in _MODELS:
                _MODELS[key] = load_model(str(model), device)
            m, tok = _MODELS[key]
        return m, tokenizer or tok, str(model)
    if isinstance(model, tuple):
        model, tokenizer = model
    if tokenizer is None:
        raise ValueError("a loaded model needs its tokenizer: pass (model, tokenizer) or tokenizer=...")
    return model, tokenizer, str(getattr(model, "name_or_path", "") or "")


def _read_examples(examples, answer_field):
    """[(item, answer)] from a .jsonl path, dicts holding the answer, or (item, answer) pairs."""
    if isinstance(examples, (str, Path)):
        with open(examples) as fh:
            examples = [json.loads(line) for line in fh if line.strip()]
    out = []
    for e in examples:
        if isinstance(e, dict):
            if answer_field not in e:
                raise ValueError(f"an example has no {answer_field!r} field: {e!r}")
            out.append(({k: v for k, v in e.items() if k != answer_field}, str(e[answer_field])))
        elif isinstance(e, (tuple, list)) and len(e) == 2:
            out.append((e[0], str(e[1])))
        else:
            raise ValueError(f"an example must be a dict with {answer_field!r} or an (item, answer) pair: {e!r}")
    if not out:
        raise ValueError("no examples")
    return out


class Classifier:
    """A model, its tokenizer and a read-out, callable on items. Build with Classifier.fit or Classifier.load."""

    def __init__(self, model, tokenizer, readout: Readout, prompt=None, max_len: int = 1024):
        self.model, self.tokenizer, self.readout, self.max_len = model, tokenizer, readout, max_len
        self._prompt_fn = prompt
        self._fit_data = None
        if prompt is None and not readout.template:
            raise ValueError("this read-out was fitted with a prompt function, not a template: pass prompt=")
        d = model.get_output_embeddings().weight.shape[1]
        if readout.mu_hat.shape[0] != d:
            raise ValueError(f"the read-out was fitted on a model with hidden size {readout.mu_hat.shape[0]}, this "
                             f"one has {d} (read-out fitted on {readout.model_id!r})")

    # --- building
    @classmethod
    def fit(cls, model, examples, *, template: str | None = None, prompt=None, labels=None, auto: bool | None = None,
            lam: float | None = None, alpha_mult: float | None = None, tokenizer=None, device: str | None = None,
            answer_field: str = "answer", label_prefix: str = " ", task: str | None = None, max_len: int = 1024,
            seed: int = 0, progress: bool = False, meta: dict | None = None) -> "Classifier":
        """Fit a read-out on labelled examples.

        model:     a Hugging Face id or path, a (model, tokenizer) pair, or a loaded model with tokenizer=.
        examples:  a .jsonl path, a list of dicts holding the answer under answer_field, or (item, answer) pairs.
        template:  prompt text with {{field}} placeholders, ending where the answer goes; items are dicts of fields
                   (or plain strings when the template has one field). Or
        prompt:    a function from an item to the prompt text.
        labels:    the answers, in order (default: every distinct answer in the examples, sorted).
        auto:      choose lean, strength and ridge from the examples (default, unless lam or alpha_mult is given).
        The held-out two-fold scores are kept in .report."""
        if (template is None) == (prompt is None):
            raise ValueError("give either template= or prompt=")
        if auto is None:
            auto = lam is None and alpha_mult is None
        elif auto and (lam is not None or alpha_mult is not None):
            raise ValueError("auto chooses the ridge and strength itself; drop lam / alpha_mult, or auto")
        m, tok, model_id = _resolve_model(model, tokenizer, device)
        pairs = _read_examples(examples, answer_field)
        answers = [a for _, a in pairs]
        labels = [str(x) for x in labels] if labels is not None else sorted(set(answers))
        missing = sorted(set(answers) - set(labels))
        if missing:
            raise ValueError(f"answers in the examples that are not in labels: {missing}")
        if len(labels) < 2:
            raise ValueError("need at least two answers")
        ids, suffix = answer_tokens(tok, labels, label_prefix)
        meta = dict(meta or {}, task=task or getattr(prompt, "__name__", None) or "readout", label_prefix=label_prefix)
        if template is not None:
            template += suffix
        else:
            meta["prompt_suffix"] = suffix
        self = cls.__new__(cls)                                   # prompts are built the way predict builds them
        self._prompt_fn, self.readout = prompt, Readout(model_id, labels, ids, template or "", np.zeros(0), 1.0,
                                                        np.zeros(0), np.zeros(0), np.zeros(0), 0.0, meta)
        prompts = [self._prompt(item) for item, _ in pairs]
        gold = np.array([labels.index(a) for a in answers])
        H, LAB, LSE = collect(m, tok, prompts, ids, max_len=max_len, progress=progress)
        npar = int(sum(p.numel() for p in m.parameters()))
        kw = {} if auto else dict(lam=lam, alpha_mult=2.0 if alpha_mult is None else alpha_mult)
        try:
            meta["twofold"] = twofold(H, LAB, LSE, gold, seed=seed, auto=auto, n_params=npar, **kw)
        except ValueError:                                        # an answer with one example: nothing to hold out
            meta["twofold"] = None
        common = dict(model_id=model_id, labels=labels, label_ids=ids, template=template or "")
        if auto:
            r, t = fit_auto(H, LAB, LSE, gold, n_params=npar, seed=seed, meta=meta, **common)
            if r is None:                                         # leave the model alone: a read-out that adds nothing
                r = fit(H, LAB, LSE, gold, lean=0.0, alpha_mult=0.0, **common,
                        meta=dict(meta, auto={k: v for k, v in t.items() if k != "table"}))
        else:
            r = fit(H, LAB, LSE, gold, meta=meta, **kw, **common)
        tf = meta["twofold"]
        if tf and tf["bal_edited"] < tf["bal_shipped"]:
            warnings.warn("on held-out examples the edit scores below the model as shipped (balanced accuracy "
                          f"{tf['bal_edited']:.3f} against {tf['bal_shipped']:.3f}); check with .sweep() and more "
                          "examples before using it", stacklevel=2)
        out = cls(m, tok, r, prompt=prompt, max_len=max_len)
        texts = [" ".join(str(item.get(f, "")) for f in template_fields(template)) if isinstance(item, dict)
                 else str(item) for item, _ in pairs] if template is not None else prompts
        out._fit_data = (H, LAB, LSE, gold, texts, npar)
        return out

    @classmethod
    def load(cls, path, model=None, *, prompt=None, tokenizer=None, device: str | None = None,
             max_len: int = 1024) -> "Classifier":
        """A read-out saved by .save() or `lmreadout fit`, on the model it names (or the one you pass)."""
        r = Readout.load(path)
        m, tok, model_id = _resolve_model(model if model is not None else r.model_id, tokenizer, device)
        if r.model_id and model_id and r.model_id != model_id:
            warnings.warn(f"the read-out was fitted on {r.model_id!r}, not {model_id!r}; it is only meaningful on "
                          "the same weights", stacklevel=2)
        ids, _ = answer_tokens(tok, r.labels, r.meta.get("label_prefix", " "))
        if ids != list(r.label_ids):
            raise ValueError(f"answer tokens differ from the read-out's ({ids} vs {r.label_ids}); same tokenizer?")
        return cls(m, tok, r, prompt=prompt, max_len=max_len)

    def save(self, path) -> None:
        """The read-out alone (a few KB to a few MB), for Classifier.load or the command line."""
        self.readout.save(path)

    # --- answering
    def _prompt(self, item) -> str:
        r = self.readout
        if self._prompt_fn is not None:
            return str(self._prompt_fn(item)) + r.meta.get("prompt_suffix", "")
        if isinstance(item, str):
            fields = template_fields(r.template)
            if len(fields) != 1:
                raise TypeError(f"the template has fields {fields}; pass a dict of them, not a string")
            item = {fields[0]: item}
        return fill_template(r.template, item)

    def _scores(self, items) -> np.ndarray:
        if not len(items):
            return np.zeros((0, len(self.labels)))
        H, LAB, _ = collect(self.model, self.tokenizer, [self._prompt(x) for x in items], self.readout.label_ids,
                            max_len=self.max_len)
        return self.readout.scores(H, LAB)

    def predict(self, items) -> list[str]:
        """The answer for each item."""
        return [self.labels[int(k)] for k in self._scores(list(items)).argmax(1)]

    def scores(self, items) -> list[dict[str, float]]:
        """For each item, {answer: probability among the answers} (a softmax over the edited answer logits)."""
        S = self._scores(list(items))
        P = np.exp(S - S.max(1, keepdims=True)); P /= P.sum(1, keepdims=True)
        return [dict(zip(self.labels, map(float, p))) for p in P]

    def __call__(self, item=None, **fields) -> str:
        """One item: clf("text"), clf({"text": ...}) or clf(text=...)."""
        if (item is None) == (not fields):
            raise TypeError("pass one item, or its fields as keywords")
        return self.predict([fields if item is None else item])[0]

    # --- inspecting
    @property
    def labels(self) -> list[str]:
        return self.readout.labels

    @property
    def report(self) -> dict | None:
        """Held-out two-fold scores from the fit (see core.twofold); None when an answer had a single example."""
        return self.readout.meta.get("twofold")

    @property
    def settings(self) -> dict:
        """lean, alpha_mult and lam of the read-out, and, when chosen automatically, the choice's details."""
        m = self.readout.meta
        return {k: m[k] for k in ("lean", "alpha_mult", "lam", "auto") if k in m}

    @property
    def unchanged(self) -> bool:
        """True when the read-out adds nothing: auto found no edit better than the model as it is."""
        return not np.any(self.readout.deltas())

    def sweep(self, sizes=(15, 30, 60, 120), draws: int = 20, seed: int = 0) -> list[dict]:
        """core.sweep on the examples this classifier was fitted on (kept in memory, so not after load): how the
        model as shipped, calibration, word counts, the fixed edit and auto score at each number of examples."""
        if self._fit_data is None:
            raise RuntimeError("sweep needs the fit examples; it is available on a Classifier made by fit, not load")
        H, LAB, LSE, gold, texts, npar = self._fit_data
        return sweep(H, LAB, LSE, gold, texts=texts, sizes=sizes, draws=draws, seed=seed, auto=True, n_params=npar)

    # --- writing it into the model
    def patch(self):
        """Write the read-out into the model's answer rows for good and return the model: plain generate / logits
        then give the read-out's answer. The model is shared by every Classifier on it, so do this once per set of
        answers."""
        with _LOCK:
            for k in [k for k, v in _MODELS.items() if v[0] is self.model]:
                del _MODELS[k]                                    # no longer the model as shipped: do not hand it out
        return patch(self.model, self.readout)

    def patched(self):
        """`with clf.patched() as model:` the same, undone on exit."""
        return patched(self.model, self.readout)

    def export(self, path) -> None:
        """Save a patched copy of the model and tokenizer for plain transformers; the model in memory is unchanged."""
        with self.patched() as m:
            m.save_pretrained(path)
        self.tokenizer.save_pretrained(path)

    def __repr__(self):
        r = self.readout
        return (f"Classifier(task={r.meta.get('task')!r}, model={r.model_id!r}, labels={r.labels}, "
                f"n_fit={r.meta.get('n_fit')}{', unchanged' if self.unchanged else ''})")


# ----------------------------------------------------------------------------------------------- the decorator

class _Task:
    """A prompt function turned into a classifier. Fitted on first use (or loaded from its cache file)."""

    def __init__(self, fn, model, examples, cache, kw):
        functools.update_wrapper(self, fn)
        self.prompt, self._model, self._examples, self._cache, self._kw = fn, model, examples, cache, kw
        self._sig, self._clf, self._lock = inspect.signature(fn), None, threading.Lock()

    def _row(self, args, kwargs) -> dict:
        b = self._sig.bind(*args, **kwargs); b.apply_defaults()
        return dict(b.arguments)

    def _from_row(self, row) -> str:
        return self.prompt(*self._sig.bind(**row).args, **self._sig.bind(**row).kwargs)

    def _pairs(self):
        out = []
        for item, ans in _read_examples(self._examples, self._kw.get("answer_field", "answer")):
            args, kwargs = ((), item) if isinstance(item, dict) else (item, {}) if isinstance(item, tuple) else ((item,), {})
            out.append((self._row(args, kwargs), ans))
        return out

    @property
    def classifier(self) -> Classifier:
        with self._lock:
            if self._clf is None:
                self._clf = self._build()
        return self._clf

    def _build(self) -> Classifier:
        pairs = self._pairs()
        kw = dict(self._kw, task=self._kw.get("task") or self.prompt.__name__)
        m, tok, model_id = _resolve_model(self._model, kw.pop("tokenizer", None), kw.pop("device", None))
        mark = hashlib.sha256(json.dumps([model_id, [self._from_row(r) for r, _ in pairs], [a for _, a in pairs],
                                          {k: repr(v) for k, v in sorted(kw.items())}]).encode()).hexdigest()
        if self._cache and Path(self._cache).exists():
            r = Readout.load(self._cache)
            if r.meta.get("fingerprint") == mark:                 # same model, prompts, answers and settings
                return Classifier(m, tok, r, prompt=self._from_row, max_len=kw.get("max_len", 1024))
        clf = Classifier.fit((m, tok), pairs, prompt=self._from_row, meta=dict(fingerprint=mark), **kw)
        clf.readout.model_id = clf.readout.model_id or model_id
        if self._cache:
            clf.save(self._cache)
        return clf

    def __call__(self, *args, **kwargs) -> str:
        return self.classifier.predict([self._row(args, kwargs)])[0]

    def scores(self, *args, **kwargs) -> dict[str, float]:
        """{answer: probability among the answers} for one call's arguments."""
        return self.classifier.scores([self._row(args, kwargs)])[0]

    def map(self, inputs) -> list[str]:
        """The answer for each input: a dict of keyword arguments, a tuple of positional ones, or a single value."""
        rows = [self._row(*(((), x) if isinstance(x, dict) else (x, {}) if isinstance(x, tuple) else ((x,), {})))
                for x in inputs]
        return self.classifier.predict(rows)


def classifier(model, examples, *, cache=None, **kw):
    """Decorator: the function writes the prompt (ending where the answer goes) from its arguments; the decorated
    function returns the answer.

        @classifier("Qwen/Qwen3.5-0.8B", examples=[("Either party may terminate.", "No"), ...], cache="law.npz")
        def governing_law(clause):
            return f"Clause: {clause}\\nDoes it say which law governs the contract?"

        governing_law("...laws of Delaware.")          # "Yes"; fitted on the first call
        governing_law.scores("...")                    # {"No": 0.1, "Yes": 0.9}
        governing_law.map(["...", "..."])              # many at once
        governing_law.classifier                       # the Classifier: .report, .patch(), .export(dir), .sweep()
        governing_law.prompt("...")                    # the original function

    examples: a .jsonl path or dicts (the function's arguments by name, plus "answer"), or (input, answer) pairs
    where input is one value, a tuple of positional arguments or a dict of keyword ones. cache: a .npz file; the fit
    is saved there and reused while the model, the prompts, the answers and the settings stay the same. Other
    keywords go to Classifier.fit (labels, auto, lam, alpha_mult, tokenizer, device, label_prefix, max_len, ...)."""
    def wrap(fn):
        return _Task(fn, model, examples, cache, kw)
    return wrap
