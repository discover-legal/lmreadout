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
        Hs, LABs, LSEs, gs, _ = synthetic(n=60, d=32)
        r = fit(Hs, LABs, LSEs, gs, label_ids=(3, 5))
        before = m.get_output_embeddings().weight.detach().float().clone()
        patch(m, r)
        after = m.get_output_embeddings().weight.detach().float()
        D = torch.as_tensor(r.deltas(), dtype=torch.float32)
        tol = 1e-5 if dt == torch.float32 else 0.02 * (before[[3, 5]].abs().max() + D.abs().max())
        assert torch.allclose(after[[3, 5]] - before[[3, 5]], D, atol=float(tol))   # the two answer rows moved
        others = [i for i in range(after.shape[0]) if i not in (3, 5)]
        assert torch.equal(after[others], before[others])                          # nothing else did
        assert after.dtype == torch.float32 and m.get_output_embeddings().weight.dtype == dt


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


def test_twofold_with_a_rare_answer_and_sweep_with_one_answer():
    import pytest
    from lmreadout.core import sweep
    H, LAB, LSE, gold, _ = synthetic()
    idx = np.concatenate([np.flatnonzero(gold == 0)[:38], np.flatnonzero(gold == 1)[:2]])   # two Yes in 40
    for seed in range(5):
        tf = twofold(H[idx], LAB[idx], LSE[idx], gold[idx], seed=seed)
        assert 0.0 <= tf["bal_edited"] <= 1.0
    z = np.flatnonzero(gold == 0)[:60]
    with pytest.raises(ValueError):
        sweep(H[z], LAB[z], LSE[z], gold[z], sizes=(15,), draws=2)


# ------------------------------------------------------------------------------------------- choosing the settings

from lmreadout.core import candidates, fit_auto, preferred_strength, sweep, tune  # noqa: E402


def test_preferred_strength_steps_down_with_size():
    assert preferred_strength(None) == 2.0
    assert preferred_strength(0.9e9) == 2.0 and preferred_strength(2.3e9) == 2.0
    assert preferred_strength(4.7e9) == 1.0 and preferred_strength(9.6e9) == 0.5


def test_candidates_grid_and_tie_order():
    for npar, s in ((1e9, 2.0), (4e9, 1.0), (9e9, 0.5)):
        c = candidates(npar)
        assert len(c) == 3 + 4 * 3 * 3                          # strength 0: ridge does not matter
        assert c[0] == dict(lean=1.0, strength=s, lam_factor=1.0)
        assert sum(x["lean"] == 0 and x["strength"] == 0 for x in c) == 1


def test_lean_scales_the_calibration():
    H, LAB, LSE, gold, _ = synthetic()
    r0 = fit(H, LAB, LSE, gold, lean=0.0, alpha_mult=0.0)
    assert np.allclose(r0.scores(H, LAB), LAB)                  # no lean removed, no read-out: the model as is
    r1 = fit(H, LAB, LSE, gold, lean=1.0, alpha_mult=0.0)
    assert np.allclose(r1.scores(H, LAB), r1.calibrated(H, LAB))
    rh = fit(H, LAB, LSE, gold, lean=0.5, alpha_mult=0.0)
    assert np.allclose(rh.shift, 0.5 * r1.shift)
    rd = fit(H, LAB, LSE, gold)                                  # defaults unchanged: lean 1, strength 2
    assert rd.meta["lean"] == 1.0 and rd.meta["alpha_mult"] == 2.0


def test_tune_uses_a_planted_direction():
    H, LAB, LSE, gold, _ = synthetic(n=40)
    t = tune(H, LAB, LSE, gold)
    assert not t["unchanged"] and t["alpha_mult"] > 0 and t["cv_bal"] > t["cv_unchanged"]
    r, t2 = fit_auto(H, LAB, LSE, gold)
    assert r is not None and r.meta["auto"]["alpha_mult"] == t2["alpha_mult"]


def test_tune_leaves_a_model_that_is_already_right():
    H, _, LSE, gold, _ = synthetic(n=30)
    LAB = np.column_stack([-3.0 * (2 * gold - 1), 3.0 * (2 * gold - 1)]).astype(float)   # answers every item right
    r, t = fit_auto(H, LAB, LSE, gold)
    assert r is None and t["unchanged"] and t["cv_unchanged"] == 1.0


def test_tune_falls_back_to_the_lean_when_an_answer_is_short():
    H, LAB, LSE, gold, _ = synthetic(n=30)
    gold = np.zeros(30, int); gold[0] = 1
    r, t = fit_auto(H, LAB, LSE, gold)
    assert t["fallback"] == [1] and t["lean"] == 1.0 and t["alpha_mult"] == 0.0 and not t["unchanged"]
    assert np.allclose(r.scores(H, LAB), r.calibrated(H, LAB))   # lean removed, no read-out
    r1, t1 = fit_auto(H, LAB, LSE, np.zeros(30, int))              # one answer only: still the lean, no read-out
    assert t1["fallback"] == [1] and np.allclose(r1.scores(H, LAB), r1.calibrated(H, LAB))


def test_tune_uses_folds_above_fifty_items():
    H, LAB, LSE, gold, _ = synthetic(n=120)
    assert tune(H, LAB, LSE, gold)["folds"] == 10


def test_sweep_and_twofold_with_auto():
    H, LAB, LSE, gold, _ = synthetic(n=200)
    res = sweep(H, LAB, LSE, gold, sizes=(15, 40), draws=3, auto=True, n_params=int(1e9))
    assert all("bal_auto" in r and "auto_fallback_draws" in r and r["auto_choices"] for r in res)
    gold2 = gold.copy(); gold2[np.flatnonzero(gold2 == 1)[2:]] = 0              # two items of answer 1 in all
    r2 = sweep(H, LAB, LSE, gold2, sizes=(15,), draws=3, auto=True)[0]
    assert r2["auto_fallback_draws"] == 3 and r2["auto_choices"] == "fallback (lean only): 3"
    tf = twofold(H, LAB, LSE, gold, auto=True)
    assert tf["bal_edited"] > tf["bal_shipped"]


def test_sweep_refuses_tiny_sizes_and_no_draws():
    import pytest
    H, LAB, LSE, gold, _ = synthetic(n=50)
    for kw in (dict(sizes=(1,)), dict(sizes=(15,), draws=0)):
        with pytest.raises(ValueError):
            sweep(H, LAB, LSE, gold, **kw)


def test_predict_refuses_names_that_overwrite():
    import pytest
    from lmreadout.core import predict_items
    H, LAB, LSE, gold, _ = synthetic(n=60)
    a = fit(H, LAB, LSE, gold, meta=dict(task="answer"))
    b1, b2 = (fit(H, LAB, LSE, gold, meta=dict(task="t")) for _ in range(2))
    for ros in ([a], [b1, b2]):
        with pytest.raises(ValueError, match="overwrite"):
            predict_items(None, None, ros, [dict(text="x", answer="No")])


def test_auto_refuses_fixed_settings_and_fit_refuses_reserved_meta():
    import pytest
    H, LAB, LSE, gold, _ = synthetic(n=60)
    with pytest.raises(ValueError, match="auto chooses"):
        twofold(H, LAB, LSE, gold, auto=True, lam=10.0)
    with pytest.raises(ValueError, match="set by fit"):
        fit(H, LAB, LSE, gold, meta=dict(lam=3))
