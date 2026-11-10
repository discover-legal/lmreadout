"""The read-out: calibration plus a ridge classifier on the final hidden state, expressed as an edit of the two
label rows of the output table.

Notation. At the answer position the model holds a final-norm state h (d numbers). The output table U scores
token t as U[t] . h. For labels (t0, t1) the model answers t1 when gap = U[t1].h - U[t0].h > 0.
  Calibration:  U[t] += shift_t * mu_hat, mu_hat = unit mean of h, chosen so both labels have equal mean
                log-probability on the fit set (h . mu_hat is nearly constant = p_mean after the final norm).
  Read-out:     ridge w, b from h to y in {-1, +1}; U[t1] += alpha w + (alpha b / p_mean) mu_hat, U[t0] -= same.
  New gap:      gap_calibrated(h) + 2 alpha (w . h + b).
Every step is closed form. Only the two label rows change.
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
def collect(model, tok, prompts: list[str], label_ids: list[int], max_len: int = 1024, progress: bool = False):
    """For each prompt: final-norm state h [d], the label logits [2] and log-sum-exp of all logits (so label
    log-probabilities are lab - lse). Returns (H [n, d], LAB [n, 2], LSE [n]) as float64 numpy arrays."""
    device = next(model.parameters()).device
    H, LAB, LSE = [], [], []
    picker = None
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
        if progress and (i + 1) % 50 == 0:
            print(f"  {i + 1}/{len(prompts)}", flush=True)
    return (torch.stack(H).double().numpy(), torch.stack(LAB).double().numpy(), torch.stack(LSE).double().numpy())


# ----------------------------------------------------------------------------------------------- the read-out

def ridge(X: np.ndarray, y: np.ndarray, lam: float):
    """Standardised ridge with intercept; returns (w in raw feature units, b)."""
    mu, sd = X.mean(0), X.std(0) + 1e-6
    Z = (X - mu) / sd
    w_z = np.linalg.solve(Z.T @ Z + lam * np.eye(Z.shape[1]), Z.T @ (y - y.mean()))
    w = w_z / sd
    return w, float(y.mean() - mu @ w)


@dataclass
class Readout:
    model_id: str
    labels: list[str]
    label_ids: list[int]
    template: str
    mu_hat: np.ndarray
    p_mean: float
    shift: np.ndarray            # [2] per-label calibration along mu_hat
    w: np.ndarray                # [d]
    b: float
    alpha: float
    meta: dict = field(default_factory=dict)

    # --- arithmetic
    def gap(self, H: np.ndarray, LAB: np.ndarray) -> np.ndarray:
        """Edited logit gap (label 1 minus label 0). Exactly what the patched model computes."""
        proj = H @ self.mu_hat
        g = (LAB[:, 1] - LAB[:, 0]) + (self.shift[1] - self.shift[0]) * proj
        # the intercept rides along mu_hat in the rows, so it scales with proj / p_mean (nearly 1 after the final norm)
        return g + 2.0 * self.alpha * (H @ self.w + self.b * proj / self.p_mean)

    def predict(self, H: np.ndarray, LAB: np.ndarray) -> np.ndarray:
        return (self.gap(H, LAB) > 0).astype(int)

    def row_deltas(self) -> dict[int, np.ndarray]:
        """What to add to each label row of lm_head.weight."""
        out = {}
        for j, t in enumerate(self.label_ids):
            sgn = (-1.0, 1.0)[j]
            out[t] = self.shift[j] * self.mu_hat + sgn * self.alpha * self.w + sgn * self.alpha * self.b / self.p_mean * self.mu_hat
        return out

    # --- io
    def save(self, path: str | Path) -> None:
        path = Path(path)
        meta = dict(model_id=self.model_id, labels=self.labels, label_ids=self.label_ids, template=self.template,
                    p_mean=self.p_mean, b=self.b, alpha=self.alpha, meta=self.meta, format="lmreadout-1")
        np.savez(path, mu_hat=self.mu_hat, shift=self.shift, w=self.w, meta=json.dumps(meta))

    @classmethod
    def load(cls, path: str | Path) -> "Readout":
        z = np.load(path, allow_pickle=False)
        m = json.loads(str(z["meta"]))
        return cls(model_id=m["model_id"], labels=m["labels"], label_ids=m["label_ids"], template=m["template"],
                   mu_hat=z["mu_hat"], p_mean=m["p_mean"], shift=z["shift"], w=z["w"], b=m["b"], alpha=m["alpha"], meta=m.get("meta", {}))


def fit(H: np.ndarray, LAB: np.ndarray, LSE: np.ndarray, gold: np.ndarray, *, model_id: str = "", labels=("0", "1"),
        label_ids=(0, 1), template: str = "", lam: float | None = None, alpha_mult: float = 2.0, meta: dict | None = None) -> Readout:
    """Calibration + ridge read-out from (H, LAB, LSE, gold). gold in {0, 1} indexes `labels`."""
    n, d = H.shape
    mu_hat = H.mean(0); mu_hat = mu_hat / (np.linalg.norm(mu_hat) + 1e-12)
    proj = H @ mu_hat
    p_mean = float(proj.mean())
    mean_lp = (LAB - LSE[:, None]).mean(0)                      # mean log-prob of each label
    shift = -(mean_lp - mean_lp.mean()) / p_mean
    gap1 = (LAB[:, 1] - LAB[:, 0]) + (shift[1] - shift[0]) * proj
    w, b = ridge(H, 2.0 * gold - 1.0, lam=float(n) if lam is None else lam)
    alpha = float(alpha_mult * gap1.std() / ((H @ w + b).std() + 1e-9))
    return Readout(model_id=model_id, labels=list(labels), label_ids=list(label_ids), template=template, mu_hat=mu_hat,
                   p_mean=p_mean, shift=shift, w=w, b=b, alpha=alpha, meta=dict(n_fit=int(n), d=int(d), lam=float(n) if lam is None else lam,
                   alpha_mult=alpha_mult, **(meta or {})))


def twofold(H, LAB, LSE, gold, **kw) -> dict:
    """Fit on one half (by item parity), score the other, both ways. Returns majority / shipped / calibrated / edited
    accuracies, every item scored by a read-out that never saw it."""
    n = len(gold); fold = np.arange(n) % 2
    p0 = (LAB[:, 1] > LAB[:, 0]).astype(int)
    p1, p2 = np.zeros(n, int), np.zeros(n, int)
    for f in (0, 1):
        fit_m, ev = fold != f, fold == f
        r = fit(H[fit_m], LAB[fit_m], LSE[fit_m], gold[fit_m], **kw)
        proj = H[ev] @ r.mu_hat
        p1[ev] = (((LAB[ev, 1] - LAB[ev, 0]) + (r.shift[1] - r.shift[0]) * proj) > 0).astype(int)
        p2[ev] = r.predict(H[ev], LAB[ev])
    return dict(n=int(n), majority=float(max(gold.mean(), 1 - gold.mean())), shipped=float((p0 == gold).mean()),
                calibrated=float((p1 == gold).mean()), edited=float((p2 == gold).mean()))


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
        g = r.gap(H, LAB)
        name = r.meta.get("task", "readout")
        for o, gi in zip(out, g):
            o[name] = r.labels[int(gi > 0)]; o[name + "_margin"] = float(gi)
    return out
