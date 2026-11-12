"""Tests of the arithmetic with no model: a planted direction in synthetic states, and the identity between the
offline gap and the row edit (what a patched model would compute)."""
import numpy as np
import torch

from lmreadout.core import Readout, fit, twofold, patch


def synthetic(n=400, d=64, seed=0):
    rng = np.random.default_rng(seed)
    gold = (rng.random(n) < 0.4).astype(int)
    common = rng.normal(size=d); common /= np.linalg.norm(common)
    signal = rng.normal(size=d); signal -= signal @ common * common; signal /= np.linalg.norm(signal)
    H = 8.0 * common[None, :] + rng.normal(size=(n, d)) + 3.0 * (2 * gold - 1)[:, None] * signal[None, :]
    H = H / np.linalg.norm(H, axis=1, keepdims=True) * np.sqrt(d)          # post-norm: constant length
    V = 50
    U = rng.normal(size=(V, d)) * 0.3
    U[1] += 0.5 * common                                                     # the model leans to label 1
    LOG = H @ U.T
    LAB = LOG[:, [0, 1]]; LSE = np.logaddexp.reduce(LOG, axis=1)
    return H, LAB, LSE, gold, U


def test_twofold_recovers_planted_direction():
    H, LAB, LSE, gold, _ = synthetic()
    tf = twofold(H, LAB, LSE, gold)
    assert tf["edited"] > 0.9 and tf["edited"] > tf["shipped"] + 0.2


def test_row_edit_matches_offline_gap():
    H, LAB, LSE, gold, U = synthetic()
    r = fit(H, LAB, LSE, gold, labels=("a", "b"), label_ids=(0, 1))
    U2 = U.copy()
    for t, dr in r.row_deltas().items():
        U2[t] += dr
    gap_rows = H @ U2[1] - H @ U2[0]
    assert np.allclose(gap_rows, r.gap(H, LAB), atol=1e-6)


def test_save_load_roundtrip(tmp_path):
    H, LAB, LSE, gold, _ = synthetic()
    r = fit(H, LAB, LSE, gold, model_id="m", labels=("a", "b"), label_ids=(0, 1), template="{{text}}\nLabel:", meta=dict(task="t"))
    r.save(tmp_path / "r.npz"); r2 = Readout.load(tmp_path / "r.npz")
    assert np.array_equal(r.predict(H, LAB), r2.predict(H, LAB)) and r2.labels == ["a", "b"] and r2.meta["task"] == "t"


class _Head(torch.nn.Module):
    def __init__(self, U):
        super().__init__(); self.lm_head = torch.nn.Linear(U.shape[1], U.shape[0], bias=False)
        self.lm_head.weight.data.copy_(torch.as_tensor(U, dtype=torch.float32)); self.config = type("C", (), dict(tie_word_embeddings=False))()

    def get_output_embeddings(self):
        return self.lm_head


def test_patch_changes_only_label_rows():
    H, LAB, LSE, gold, U = synthetic()
    r = fit(H, LAB, LSE, gold, labels=("a", "b"), label_ids=(0, 1))
    m = _Head(U); W0 = m.lm_head.weight.detach().clone()
    patch(m, r)
    W1 = m.lm_head.weight.detach()
    changed = (W1 != W0).any(1).nonzero().flatten().tolist()
    assert changed == [0, 1]
    g = (torch.as_tensor(H, dtype=torch.float32) @ (W1[1] - W1[0])).numpy()
    assert ((g > 0).astype(int) == r.predict(H, LAB)).mean() > 0.99


# ------------------------------------------------------------------------------------------- more than two labels

def synthetic_k(K=4, n=600, d=64, seed=1):
    rng = np.random.default_rng(seed)
    gold = rng.choice(K, size=n, p=np.array([0.4, 0.3, 0.2, 0.1])[:K] / np.array([0.4, 0.3, 0.2, 0.1])[:K].sum())
    common = rng.normal(size=d); common /= np.linalg.norm(common)
    C = rng.normal(size=(K, d)); C -= (C @ common)[:, None] * common[None, :]
    C /= np.linalg.norm(C, axis=1, keepdims=True)
    H = 8.0 * common[None, :] + rng.normal(size=(n, d)) + 3.0 * C[gold]
    H = H / np.linalg.norm(H, axis=1, keepdims=True) * np.sqrt(d)
    V = 50
    U = rng.normal(size=(V, d)) * 0.3
    U[0] += 0.5 * common                                                     # the model leans to label 0
    LOG = H @ U.T
    return H, LOG[:, :K], np.logaddexp.reduce(LOG, axis=1), gold, U


def test_k_labels_recover_planted_directions():
    H, LAB, LSE, gold, _ = synthetic_k()
    tf = twofold(H, LAB, LSE, gold)
    # guessing is 0.25; with the fixed defaults (lam = n, alpha x2) the read-out lands near 0.8 here
    assert tf["bal_edited"] > 0.7 and tf["bal_edited"] > tf["bal_shipped"] + 0.3


def test_k_row_edit_matches_offline_scores():
    H, LAB, LSE, gold, U = synthetic_k()
    r = fit(H, LAB, LSE, gold, labels=list("abcd"), label_ids=[0, 1, 2, 3])
    U2 = U.copy()
    for t, dr in r.row_deltas().items():
        U2[t] += dr
    assert np.allclose(H @ U2[:4].T, r.scores(H, LAB), atol=1e-6)
    m = _Head(U); W0 = m.lm_head.weight.detach().clone(); patch(m, r)
    assert (m.lm_head.weight.detach() != W0).any(1).nonzero().flatten().tolist() == [0, 1, 2, 3]


def test_k_intercepts_centred_same_answers():
    H, LAB, LSE, gold, _ = synthetic_k()
    r = fit(H, LAB, LSE, gold, labels=list("abcd"), label_ids=[0, 1, 2, 3])
    assert abs(r.B.sum()) < 1e-9
    off = Readout(**{**r.__dict__, "B": r.B - 0.5})            # the 0.3.0 intercepts sat lower by a common amount
    assert np.array_equal(off.predict(H, LAB), r.predict(H, LAB))
    assert (r.scores(H, LAB) > off.scores(H, LAB)).all()       # centred: every answer row higher, none reordered


def _fit_v01(H, LAB, LSE, gold, lam=None, alpha_mult=2.0):
    """The two-label formula exactly as lmreadout 0.1 shipped it; returns the row deltas for labels 0 and 1."""
    from lmreadout.core import ridge
    n = len(gold)
    mu_hat = H.mean(0); mu_hat = mu_hat / np.linalg.norm(mu_hat)
    proj = H @ mu_hat; p_mean = proj.mean()
    mean_lp = (LAB - LSE[:, None]).mean(0)
    shift = -(mean_lp - mean_lp.mean()) / p_mean
    gap1 = (LAB[:, 1] - LAB[:, 0]) + (shift[1] - shift[0]) * proj
    w, b = ridge(H, 2.0 * gold - 1.0, lam=float(n) if lam is None else lam)
    alpha = alpha_mult * gap1.std() / ((H @ w + b).std() + 1e-9)
    return [shift[j] * mu_hat + s * alpha * w + s * alpha * b / p_mean * mu_hat for j, s in ((0, -1.0), (1, 1.0))]


def test_two_labels_identical_to_v01():
    H, LAB, LSE, gold, _ = synthetic()
    old = _fit_v01(H, LAB, LSE, gold)
    new = fit(H, LAB, LSE, gold, labels=("a", "b"), label_ids=(0, 1)).deltas()
    for j in (0, 1):
        assert np.allclose(new[j], old[j], rtol=1e-9, atol=1e-12)


def test_loads_v01_file(tmp_path):
    import json
    H, LAB, LSE, gold, _ = synthetic()
    r = fit(H, LAB, LSE, gold, model_id="m", labels=("a", "b"), label_ids=(0, 1), template="t")
    meta = dict(model_id="m", labels=["a", "b"], label_ids=[0, 1], template="t", p_mean=r.p_mean, b=float(r.B[1]),
                alpha=r.alpha, meta={}, format="lmreadout-1")
    np.savez(tmp_path / "old.npz", mu_hat=r.mu_hat, shift=r.shift, w=r.W[1], meta=json.dumps(meta))
    r1 = Readout.load(tmp_path / "old.npz")
    assert np.allclose(r1.deltas(), r.deltas()) and np.array_equal(r1.predict(H, LAB), r.predict(H, LAB))


# ------------------------------------------------------------------------------------------- answers, sweeps, word counts

class _Tok:
    """A toy tokenizer: a space is its own token before a digit, words are one token each, ids from a table."""
    def __init__(self):
        self.vocab = {}

    def _id(self, piece):
        return self.vocab.setdefault(piece, len(self.vocab))

    def __call__(self, text, add_special_tokens=False):
        import re as _re
        pieces = _re.findall(r" \d| ?[A-Za-z]+", text)
        ids = []
        for p in pieces:
            if p.startswith(" ") and p[1:].isdigit():
                ids += [self._id(" "), self._id(p[1:])]
            else:
                ids.append(self._id(p))
        return {"input_ids": ids}

    def decode(self, ids):
        inv = {v: k for k, v in self.vocab.items()}
        return "".join(inv[i] for i in ids)


def test_answer_tokens_first_token_and_digits():
    import pytest
    from lmreadout.core import answer_tokens
    tok = _Tok()
    ids, suffix = answer_tokens(tok, ["Unilateral change", "Other"])
    assert suffix == "" and ids == [tok(" Unilateral")["input_ids"][0], tok(" Other")["input_ids"][0]]
    ids, suffix = answer_tokens(tok, ["0", "1", "2"])
    assert suffix == " " and ids == [tok(" 0")["input_ids"][1],
                                      tok(" 1")["input_ids"][1], tok(" 2")["input_ids"][1]]
    with pytest.raises(ValueError, match="share their first token"):
        answer_tokens(tok, ["Unilateral change", "Unilateral termination"])


def test_sweep_scores_held_out_and_beats_shipped():
    from lmreadout.core import sweep
    H, LAB, LSE, gold, _ = synthetic_k()
    texts = [f"topic{g} filler word{i % 7}" for i, g in enumerate(gold)]
    res = sweep(H, LAB, LSE, gold, texts=texts, sizes=(15, 60), draws=5, seed=0)
    assert [r["n_fit"] for r in res] == [15, 60] and res[0]["n_scored"] == len(gold) - 15
    assert res[1]["bal_edited"] > res[1]["bal_shipped"] + 0.2
    assert res[1]["bal_wordcount"] > 0.9                       # the texts name the topic outright


def test_wordcount_predict_learns_a_marker_word():
    from lmreadout.core import wordcount_predict
    tr = ["the cat sat", "a cat ran", "the dog sat", "a dog ran"] * 3
    g = np.array([0, 0, 1, 1] * 3)
    assert wordcount_predict(tr, g, ["my cat", "my dog"], 2).tolist() == [0, 1]


# ------------------------------------------------------------------------------------------- 0.3.2 fixes

def _tiny_llama(dtype):
    from transformers import LlamaConfig, LlamaForCausalLM
    torch.manual_seed(0)
    cfg = LlamaConfig(vocab_size=64, hidden_size=32, intermediate_size=64, num_hidden_layers=2, num_attention_heads=4,
                      num_key_value_heads=4, max_position_embeddings=64)
    return LlamaForCausalLM(cfg).to(dtype).eval()


class _IdTok:
    def __call__(self, text, add_special_tokens=False):
        return {"input_ids": [ord(c) % 64 for c in text]}


def test_collect_and_patch_half_precision():
    from lmreadout.core import collect
    for dt in (torch.float32, torch.bfloat16):
        m = _tiny_llama(dt)
        H, LAB, LSE = collect(m, _IdTok(), ["abc", "hello there", "xy"], [3, 5])
        assert H.shape == (3, 32) and LAB.shape == (3, 2) and np.isfinite(H).all()


def test_collect_warns_when_prompts_are_cut():
    import pytest
    from lmreadout.core import collect
    with pytest.warns(UserWarning, match="1 of 2 prompts"):
        collect(_tiny_llama(torch.float32), _IdTok(), ["a" * 40, "b"], [3, 5], max_len=10)


def test_fit_refuses_single_answer_and_twofold_survives_alternating_order():
    import pytest
    H, LAB, LSE, gold, _ = synthetic()
    with pytest.raises(ValueError):
        fit(H[gold == 1], LAB[gold == 1], LSE[gold == 1], gold[gold == 1])
    alt = np.concatenate([np.flatnonzero(gold == 0)[:120], np.flatnonzero(gold == 1)[:120]])
    alt = alt.reshape(2, 120).T.flatten()                                                 # No, Yes, No, Yes, ...
    tf = twofold(H[alt], LAB[alt], LSE[alt], gold[alt])
    assert tf["bal_edited"] > 0.9


def test_save_accepts_numpy_ids(tmp_path):
    H, LAB, LSE, gold, _ = synthetic()
    r = fit(H, LAB, LSE, gold, labels=np.array(["a", "b"]), label_ids=np.array([0, 1]))
    r.save(tmp_path / "r.npz")
    assert Readout.load(tmp_path / "r.npz").label_ids == [0, 1]


def test_template_trailing_newline_removed(tmp_path):
    from lmreadout.cli import read_template
    (tmp_path / "t.txt").write_text("Clause: {{text}}\nLabel:\n")
    assert read_template(str(tmp_path / "t.txt")) == "Clause: {{text}}\nLabel:"
