"""The read-out: calibration plus a ridge classifier on the final hidden state, expressed as an edit of the
label rows of the output table.

Notation. At the answer position the model holds a final-norm state h (d numbers). The output table U scores
token t as U[t] . h. With labels t_0 .. t_{K-1} the model answers the label whose row scores highest.
  Calibration:  U[t_k] += shift_k * mu_hat, mu_hat = unit mean of h, chosen so every label has the same mean
                log-probability on the fit set (h . mu_hat is nearly constant = p_mean after the final norm).
  Read-out:     one ridge (w_k, b_k) per label, from h to +1 for that label's items and -1 for the rest;
                U[t_k] += alpha w_k + (alpha b_k / p_mean) mu_hat.
  Strength:     alpha = alpha_mult x spread of the calibrated score differences / spread of the read-out's, both as
                the root mean square over label pairs of sd(score_k - score_j), the read-out's halved.
For two labels this is exactly the two-row edit of lmreadout 0.1 (w_0 = -w_1, b_0 = -b_1; the new gap is
gap_calibrated(h) + 2 alpha (w_1 . h + b_1)). Every step is closed form. Only the label rows change.
"""
from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np
import torch


# ----------------------------------------------------------------------------------------------- model access

def load_model(model_id: str, device: str | None = None, dtype=torch.float32):
    from transformers import AutoModelForCausalLM, AutoTokenizer
    device = device or ("cuda" if torch.cuda.is_available() else "cpu")
    model = AutoModelForCausalLM.from_pretrained(model_id, dtype=dtype).to(device).eval()
    tok = AutoTokenizer.from_pretrained(model_id)
    return model, tok


def label_token_ids(tok, labels: list[str], prefix: str = " ") -> list[int]:
    ids = []
    for lab in labels:
        t = tok(prefix + lab, add_special_tokens=False)["input_ids"]
        if len(t) != 1:
            raise ValueError(f"label {lab!r} is {len(t)} tokens ({t}); the read-out needs one-token labels "
                             f"(use a different prefix or spelling, or the first-token variant)")
        ids.append(t[0])
    if len(set(ids)) != len(ids):
        raise ValueError("label tokens are not distinct")
    return ids


def answer_tokens(tok, labels: list[str], prefix: str = " ") -> tuple[list[int], str]:
    """The row each answer is read from, as on LegalBench: the first token of prefix + answer. Answers of several
    tokens are allowed as long as their first tokens differ. When every answer is a shared lone prefix token plus one
    more token (Qwen writes " 3" as " " then "3"), the prefix goes at the end of the prompt and the second tokens are
    the rows. Returns (token ids, text to append to the prompt)."""
    toks = [tok(prefix + str(lab), add_special_tokens=False)["input_ids"] for lab in labels]
    if any(len(t) == 0 for t in toks):
        raise ValueError("an answer tokenises to nothing")
    ft, suffix = [t[0] for t in toks], ""
    if (len(labels) > 1 and len(set(ft)) == 1 and all(len(t) == 2 for t in toks) and prefix
            and tok.decode([ft[0]]) == prefix):
        ft, suffix = [t[1] for t in toks], prefix
    if len(set(ft)) != len(ft):
        clash = {}
        for lab, t in zip(labels, ft):
            clash.setdefault(t, []).append(lab)
        raise ValueError("answers share their first token, so the read-out cannot tell them apart: "
                         + "; ".join(" / ".join(map(repr, v)) for v in clash.values() if len(v) > 1))
    return ft, suffix


def template_fields(template: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"\{\{(\w+)\}\}", template)))


def fill_template(template: str, row: dict) -> str:
    return re.sub(r"\{\{(\w+)\}\}", lambda m: str(row.get(m.group(1), "")), template)


def _final_state_fn(model):
    """Returns f(out, ids) -> h at the last position such that lm_head(h) == logits[-1]. Checks it once."""
    dec = model.get_decoder() if hasattr(model, "get_decoder") else getattr(model, "model", None)
    norm = None
    for name in ("norm", "ln_f", "final_layer_norm", "final_norm"):
        if dec is not None and hasattr(dec, name):
            norm = getattr(dec, name); break
    candidates = [lambda hs: hs[-1][:, -1]]
    if norm is not None:
        candidates.append(lambda hs: norm(hs[-1][:, -1]))
    return candidates


@torch.no_grad()
def collect(model, tok, prompts: list[str], label_ids: list[int], max_len: int = 1024, progress: bool = False,
            other_max: bool = False):
    """For each prompt: final-norm state h [d], the label logits [K] and log-sum-exp of all logits (so label
    log-probabilities are lab - lse). Returns (H [n, d], LAB [n, K], LSE [n]) as float64 numpy arrays; with
    other_max=True also OM [n], the highest logit of any token that is not an answer (the model's free next token is
    an answer when LAB.max(1) >= OM)."""
    device = next(model.parameters()).device
    H, LAB, LSE, OM = [], [], [], []
    picker = None
    mask = None
    for i, p in enumerate(prompts):
        ids = tok(p, add_special_tokens=False)["input_ids"][-max_len:]
        x = torch.tensor([ids], device=device)
        out = model(x, output_hidden_states=True)
        logits = out.logits[:, -1].float()
        if picker is None:
            for cand in _final_state_fn(model):
                h = cand(out.hidden_states).float()
                test = model.lm_head(h).float()
                if torch.allclose(test, logits, atol=1e-2 * logits.abs().max().item()):
                    picker = cand; break
            if picker is None:
                raise RuntimeError("could not find the hidden state that lm_head reads; this architecture applies "
                                   "something between the last hidden state and lm_head that lmreadout does not know")
        h = picker(out.hidden_states).float()
        H.append(h[0].cpu()); LAB.append(logits[0, label_ids].cpu()); LSE.append(torch.logsumexp(logits[0], -1).cpu())
        if other_max:
            if mask is None:
                mask = torch.zeros(logits.shape[-1], dtype=torch.bool, device=logits.device); mask[label_ids] = True
            OM.append(logits[0].masked_fill(mask, float("-inf")).max().cpu())
        if progress and (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(prompts)}", flush=True)
    out = (torch.stack(H).double().numpy(), torch.stack(LAB).double().numpy(), torch.stack(LSE).double().numpy())
    return out + (torch.stack(OM).double().numpy(),) if other_max else out


# ----------------------------------------------------------------------------------------------- the read-out

def ridge(X: np.ndarray, y: np.ndarray, lam: float):
    """Standardised ridge with intercept; returns (w in raw feature units, b). Solved in the n x n form when there are
    more features than items (the same solution: (Z'Z + lam I)^-1 Z' = Z' (ZZ' + lam I)^-1)."""
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Z = (X - mu) / sd
    yc = y - y.mean()
    if Z.shape[1] <= Z.shape[0]:
        w_z = np.linalg.solve(Z.T @ Z + lam * np.eye(Z.shape[1]), Z.T @ yc)
    else:
        w_z = Z.T @ np.linalg.solve(Z @ Z.T + lam * np.eye(Z.shape[0]), yc)
    w = w_z / sd
    return w, float(y.mean() - mu @ w)


def accuracy(pred: np.ndarray, gold: np.ndarray) -> float:
    return float((pred == gold).mean())


def balanced_accuracy(pred: np.ndarray, gold: np.ndarray) -> float:
    """Mean over the labels present in gold of the share of that label's items answered correctly. Always answering
    one label scores 1/K, however lopsided the data."""
    return float(np.mean([(pred[gold == c] == c).mean() for c in np.unique(gold)]))


@dataclass
class Readout:
    model_id: str
    labels: list[str]
    label_ids: list[int]
    template: str
    mu_hat: np.ndarray
    p_mean: float
    shift: np.ndarray            # [K] per-label calibration along mu_hat
    W: np.ndarray                # [K, d] one ridge direction per label
    B: np.ndarray                # [K] one intercept per label
    alpha: float
    meta: dict = field(default_factory=dict)

    # --- arithmetic
    def deltas(self) -> np.ndarray:
        """[K, d]: what is added to each label row of lm_head.weight."""
        return (self.shift[:, None] * self.mu_hat[None, :] + self.alpha * self.W
                + (self.alpha * self.B / self.p_mean)[:, None] * self.mu_hat[None, :])

    def scores(self, H: np.ndarray, LAB: np.ndarray) -> np.ndarray:
        """[n, K] edited label logits. Exactly what the patched model computes for the label tokens."""
        return LAB + H @ self.deltas().T

    def calibrated(self, H: np.ndarray, LAB: np.ndarray) -> np.ndarray:
        """[n, K] label logits after the calibration step alone."""
        return LAB + (H @ self.mu_hat)[:, None] * self.shift[None, :]

    def predict(self, H: np.ndarray, LAB: np.ndarray) -> np.ndarray:
        return self.scores(H, LAB).argmax(1)

    def gap(self, H: np.ndarray, LAB: np.ndarray) -> np.ndarray:
        """Two labels only: edited logit gap (label 1 minus label 0)."""
        if len(self.labels) != 2:
            raise ValueError("gap() is for two-label read-outs; use scores()")
        S = self.scores(H, LAB)
        return S[:, 1] - S[:, 0]

    def row_deltas(self) -> dict[int, np.ndarray]:
        return {t: d for t, d in zip(self.label_ids, self.deltas())}

    # --- io
    def save(self, path: str | Path) -> None:
        path = Path(path)
        meta = dict(model_id=self.model_id, labels=self.labels, label_ids=self.label_ids, template=self.template,
                    p_mean=self.p_mean, alpha=self.alpha, meta=self.meta, format="lmreadout-2")
        np.savez(path, mu_hat=self.mu_hat, shift=self.shift, W=self.W, B=self.B, meta=json.dumps(meta))

    @classmethod
    def load(cls, path: str | Path) -> "Readout":
        z = np.load(path, allow_pickle=False)
        m = json.loads(str(z["meta"]))
        if m.get("format") == "lmreadout-1":       # two-label file of 0.1: one direction w and intercept b
            W = np.stack([-z["w"], z["w"]]); B = np.array([-m["b"], m["b"]])
        else:
            W, B = z["W"], z["B"] - z["B"].mean()   # 0.3.0 files kept uncentred intercepts; same answers, centred
        return cls(model_id=m["model_id"], labels=m["labels"], label_ids=m["label_ids"], template=m["template"],
                   mu_hat=z["mu_hat"], p_mean=m["p_mean"], shift=z["shift"], W=W, B=B, alpha=m["alpha"],
                   meta=m.get("meta", {}))


def fit(H: np.ndarray, LAB: np.ndarray, LSE: np.ndarray, gold: np.ndarray, *, model_id: str = "", labels=None,
        label_ids=None, template: str = "", lam: float | None = None, alpha_mult: float = 2.0, meta: dict | None = None) -> Readout:
    """Calibration + ridge read-out from (H [n, d], LAB [n, K], LSE [n], gold [n] in 0..K-1 indexing `labels`)."""
    n, d = H.shape
    K = LAB.shape[1]
    labels = list(labels) if labels is not None else [str(k) for k in range(K)]
    label_ids = list(label_ids) if label_ids is not None else list(range(K))
    if len(labels) != K or len(label_ids) != K:
        raise ValueError(f"{K} label columns but {len(labels)} labels / {len(label_ids)} label ids")
    lam = float(n) if lam is None else float(lam)
    mu_hat = H.mean(0); mu_hat = mu_hat / (np.linalg.norm(mu_hat) + 1e-12)
    proj = H @ mu_hat
    p_mean = float(proj.mean())
    mean_lp = (LAB - LSE[:, None]).mean(0)                      # mean log-prob of each label
    shift = -(mean_lp - mean_lp.mean()) / p_mean
    cal = LAB + proj[:, None] * shift[None, :]
    W, B = np.zeros((K, d)), np.zeros(K)
    for k in range(K):
        W[k], B[k] = ridge(H, 2.0 * (gold == k) - 1.0, lam=lam)
    # Each one-vs-rest intercept is about 2 * share - 1, so they sum to about 2 - K: every answer row lowered together,
    # letting other tokens overtake all the answers. Removing the mean changes no difference between answers (so no
    # chosen answer); with two answers the intercepts already cancel and this changes nothing.
    B = B - B.mean()
    R = H @ W.T + B
    pairs = [(j, k) for j in range(K) for k in range(j + 1, K)]
    s_cal = np.sqrt(np.mean([(cal[:, k] - cal[:, j]).std() ** 2 for j, k in pairs]))
    s_read = np.sqrt(np.mean([((R[:, k] - R[:, j]).std() / 2.0) ** 2 for j, k in pairs]))
    alpha = float(alpha_mult * s_cal / (s_read + 1e-9))
    return Readout(model_id=model_id, labels=labels, label_ids=label_ids, template=template, mu_hat=mu_hat,
                   p_mean=p_mean, shift=shift, W=W, B=B, alpha=alpha,
                   meta=dict(n_fit=int(n), d=int(d), lam=lam, alpha_mult=alpha_mult, **(meta or {})))


def twofold(H, LAB, LSE, gold, **kw) -> dict:
    """Fit on one half (by item parity), score the other, both ways. Returns accuracy and balanced accuracy for always
    giving the commonest label, the model as shipped, calibrated only, and edited; every item scored by a read-out
    that never saw it."""
    n = len(gold); fold = np.arange(n) % 2
    p0 = LAB.argmax(1)
    p1, p2 = np.zeros(n, int), np.zeros(n, int)
    for f in (0, 1):
        fit_m, ev = fold != f, fold == f
        r = fit(H[fit_m], LAB[fit_m], LSE[fit_m], gold[fit_m], **kw)
        p1[ev] = r.calibrated(H[ev], LAB[ev]).argmax(1)
        p2[ev] = r.predict(H[ev], LAB[ev])
    out = dict(n=int(n), majority=float(np.bincount(gold).max() / n))
    for name, p in (("shipped", p0), ("calibrated", p1), ("edited", p2)):
        out[name] = accuracy(p, gold); out["bal_" + name] = balanced_accuracy(p, gold)
    return out


# ----------------------------------------------------------------------------------------------- baselines and sweeps

def words(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def wordcount_predict(train_texts: list[str], train_gold: np.ndarray, test_texts: list[str], K: int,
                      lam: float | None = None) -> np.ndarray:
    """The control: the same per-answer ridge fed word counts instead of the model's state. Vocabulary = words in at
    least two training items. Returns predicted answer indices for test_texts."""
    seen: dict[str, int] = {}
    for t in train_texts:
        for x in set(words(t)):
            seen[x] = seen.get(x, 0) + 1
    vocab = {x: i for i, x in enumerate(sorted(x for x, c in seen.items() if c >= 2))}
    if not vocab or len(set(train_gold.tolist())) < 2:
        return np.full(len(test_texts), int(np.bincount(train_gold, minlength=K).argmax()), dtype=int)

    def counts(ts):
        X = np.zeros((len(ts), len(vocab)))
        for i, t in enumerate(ts):
            for x in words(t):
                j = vocab.get(x)
                if j is not None:
                    X[i, j] += 1
        return X
    X, Xe = counts(train_texts), counts(test_texts)
    lam = float(len(train_gold)) if lam is None else lam
    S = np.column_stack([Xe @ w + b for w, b in (ridge(X, 2.0 * (train_gold == k) - 1.0, lam) for k in range(K))])
    return S.argmax(1)


def sweep(H, LAB, LSE, gold, texts: list[str] | None = None, sizes=(15, 30, 60, 120), draws: int = 20, seed: int = 0,
          **kw) -> list[dict]:
    """For each size N: `draws` times, fit on N items drawn at random (not balanced by answer) and score every other
    item. Returns one dict per size with the mean (and sd over draws) of accuracy and balanced accuracy for the
    model as shipped, calibrated only, edited, and, when texts are given, word counts fitted on the same N items."""
    n, K = len(gold), LAB.shape[1]
    rng = np.random.default_rng(seed)
    out = []
    for N in sizes:
        if N >= n:
            continue
        acc_: dict[str, list] = {}
        for _ in range(draws):
            tr = np.zeros(n, bool); tr[rng.choice(n, N, replace=False)] = True
            ev = ~tr
            r = fit(H[tr], LAB[tr], LSE[tr], gold[tr], **kw)
            preds = dict(shipped=LAB[ev].argmax(1), calibrated=r.calibrated(H[ev], LAB[ev]).argmax(1),
                         edited=r.predict(H[ev], LAB[ev]))
            if texts is not None:
                preds["wordcount"] = wordcount_predict([t for t, m in zip(texts, tr) if m], gold[tr],
                                                       [t for t, m in zip(texts, ev) if m], K)
            for name, p in preds.items():
                acc_.setdefault(name, []).append(accuracy(p, gold[ev]))
                acc_.setdefault("bal_" + name, []).append(balanced_accuracy(p, gold[ev]))
        row = dict(n_fit=int(N), n_scored=int(n - N), draws=int(draws))
        for k, v in acc_.items():
            row[k] = float(np.mean(v)); row[k + "_sd"] = float(np.std(v))
        out.append(row)
    return out


# ----------------------------------------------------------------------------------------------- applying it

@torch.no_grad()
def patch(model, readout: Readout):
    """Write the read-out into lm_head.weight (unties the embedding first if it is shared). Returns the model."""
    if getattr(model.config, "tie_word_embeddings", False):
        model.lm_head.weight = torch.nn.Parameter(model.lm_head.weight.detach().clone())
        model.config.tie_word_embeddings = False
    W = model.lm_head.weight
    for t, dr in readout.row_deltas().items():
        W[t] += torch.as_tensor(dr, dtype=W.dtype, device=W.device)
    return model


def predict_items(model, tok, readouts: list[Readout], rows: list[dict], max_len: int = 1024) -> list[dict]:
    """Side-head mode: score each row with every read-out without changing the model. Several read-outs can share
    one model this way, which they cannot when patched into the same label rows."""
    out = [dict(row) for row in rows]
    for r in readouts:
        prompts = [fill_template(r.template, row) for row in rows]
        H, LAB, _ = collect(model, tok, prompts, r.label_ids, max_len=max_len)
        S = np.sort(r.scores(H, LAB), axis=1)
        pred = r.predict(H, LAB)
        name = r.meta.get("task", "readout")
        for o, k, s in zip(out, pred, S):
            o[name] = r.labels[int(k)]; o[name + "_margin"] = float(s[-1] - s[-2])
    return out
