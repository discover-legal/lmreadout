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
