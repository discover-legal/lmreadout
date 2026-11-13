"""Tests of the Classifier object and the decorator on a tiny randomly initialised model (no download). The model
knows nothing, so these check the plumbing: the object's answers are the patched model's answers, the weights are
put back, and a saved fit is reused."""
import json

import numpy as np
import pytest
import torch

import lmreadout.api as api
from lmreadout import Classifier, classifier, collect, patched


def _tiny(tied=False):
    from transformers import LlamaConfig, LlamaForCausalLM
    torch.manual_seed(0)
    cfg = LlamaConfig(vocab_size=64, hidden_size=32, intermediate_size=64, num_hidden_layers=2, num_attention_heads=4,
                      num_key_value_heads=4, max_position_embeddings=128, tie_word_embeddings=tied)
    return LlamaForCausalLM(cfg).eval()


class _Tok:
    """One token per character (its code modulo 64); a space is the lone token 32."""
    def __call__(self, text, add_special_tokens=False):
        return {"input_ids": [ord(c) % 64 for c in text]}

    def decode(self, ids):
        return "".join(chr(i) if i >= 32 else chr(i + 64) for i in ids)

    def save_pretrained(self, path):
        pass


TEMPLATE = "Q: {{text}}\nA:"
WORDS = ["apple pie", "stone wall", "red kite", "cold soup", "tall tree", "old boat", "blue door", "warm hat"]
EXAMPLES = [dict(text=f"{w} {i}", answer="a" if i % 2 else "b") for i, w in enumerate(WORDS * 3)]


def _model_answers(m, tok, prompts, ids):
    return [int(m(torch.tensor([tok(p)["input_ids"]])).logits[0, -1, ids].argmax()) for p in prompts]


def test_classifier_answers_are_the_patched_models():
    m, tok = _tiny(), _Tok()
    clf = Classifier.fit((m, tok), EXAMPLES, template=TEMPLATE, alpha_mult=2.0)
    assert clf.labels == ["a", "b"] and clf.readout.template.endswith("A: ")   # the space moved into the prompt
    items = [e["text"] for e in EXAMPLES[:6]]
    got = clf.predict(items)
    assert clf(items[0]) == got[0] == clf(text=items[0]) == clf({"text": items[0]})
    probs = clf.scores(items)
    assert all(abs(sum(p.values()) - 1) < 1e-9 and max(p, key=p.get) == g for p, g in zip(probs, got))
    before = m.get_output_embeddings().weight.detach().clone()
    prompts = [clf._prompt(x) for x in items]
    with clf.patched() as pm:                                    # the plain model, edited, gives the same answers
        assert [clf.labels[k] for k in _model_answers(pm, tok, prompts, clf.readout.label_ids)] == got
        assert not torch.equal(pm.get_output_embeddings().weight, before)
    assert torch.equal(m.get_output_embeddings().weight, before)  # and is put back exactly
    assert clf.report["n"] == len(EXAMPLES) and clf.settings["alpha_mult"] == 2.0


def test_patched_restores_a_tied_embedding():
    m, tok = _tiny(tied=True), _Tok()
    clf = Classifier.fit((m, tok), EXAMPLES, template=TEMPLATE, alpha_mult=2.0)
    emb = m.get_input_embeddings().weight
    assert m.get_output_embeddings().weight is emb
    before = emb.detach().clone()
    with patched(m, clf.readout):
        assert m.get_output_embeddings().weight is not emb
    assert m.get_output_embeddings().weight is emb and torch.equal(emb, before) and m.config.tie_word_embeddings


def test_save_load_and_export(tmp_path):
    m, tok = _tiny(), _Tok()
    clf = Classifier.fit((m, tok), EXAMPLES, template=TEMPLATE, alpha_mult=2.0, task="fruit")
    items = [e["text"] for e in EXAMPLES]
    clf.save(tmp_path / "r.npz")
    again = Classifier.load(tmp_path / "r.npz", (m, tok))
    assert again.predict(items) == clf.predict(items) and again.readout.meta["task"] == "fruit"
    with pytest.raises(RuntimeError):
        again.sweep()
    before = m.get_output_embeddings().weight.detach().clone()
    clf.export(tmp_path / "model")
    assert torch.equal(m.get_output_embeddings().weight, before)
    from transformers import AutoModelForCausalLM
    m2 = AutoModelForCausalLM.from_pretrained(tmp_path / "model")
    prompts = [clf._prompt(x) for x in items]
    assert [clf.labels[k] for k in _model_answers(m2, tok, prompts, clf.readout.label_ids)] == clf.predict(items)


def test_auto_is_the_default_and_unchanged_means_the_models_own_answer():
    m, tok = _tiny(), _Tok()
    clf = Classifier.fit((m, tok), EXAMPLES, template=TEMPLATE)
    assert "auto" in clf.settings
    if clf.unchanged:
        prompts = [clf._prompt(e["text"]) for e in EXAMPLES]
        _, LAB, _ = collect(m, tok, prompts, clf.readout.label_ids)
        assert clf.predict([e["text"] for e in EXAMPLES]) == [clf.labels[k] for k in LAB.argmax(1)]
    rows = clf.sweep(sizes=(8,), draws=2)
    assert rows[0]["n_fit"] == 8 and "bal_auto" in rows[0] and "bal_wordcount" in rows[0]


def test_examples_from_a_file_pairs_and_refusals(tmp_path):
    m, tok = _tiny(), _Tok()
    p = tmp_path / "ex.jsonl"
    p.write_text("".join(json.dumps(e) + "\n" for e in EXAMPLES))
    a = Classifier.fit((m, tok), p, template=TEMPLATE, alpha_mult=1.0)
    b = Classifier.fit((m, tok), [(e["text"], e["answer"]) for e in EXAMPLES], prompt=lambda t: f"Q: {t}\nA:",
                       alpha_mult=1.0)
    items = [e["text"] for e in EXAMPLES]
    assert a.predict(items) == b.predict(items)
    with pytest.raises(ValueError):
        Classifier.fit((m, tok), EXAMPLES, template=TEMPLATE, prompt=str)
    with pytest.raises(ValueError):
        Classifier.fit((m, tok), EXAMPLES, template=TEMPLATE, auto=True, lam=3.0)
    with pytest.raises(ValueError):
        Classifier.fit((m, tok), EXAMPLES, template=TEMPLATE, labels=["a"])
    with pytest.raises(ValueError):
        Classifier.fit(m, EXAMPLES, template=TEMPLATE)            # a loaded model without its tokenizer
    with pytest.raises(TypeError):
        two = [dict(x=e["text"], y="z", answer=e["answer"]) for e in EXAMPLES]
        Classifier.fit((m, tok), two, template="{{x}} {{y}}", alpha_mult=1.0)("one string")


def test_decorator_fits_lazily_caches_and_refits_when_examples_change(tmp_path, monkeypatch):
    m, tok = _tiny(), _Tok()
    fits = []
    real = api.Classifier.fit.__func__
    monkeypatch.setattr(api.Classifier, "fit", classmethod(lambda cls, *a, **k: fits.append(1) or real(cls, *a, **k)))
    cache = tmp_path / "task.npz"

    def make(examples):
        @classifier((m, tok), examples=examples, cache=cache, alpha_mult=2.0)
        def fruit(text, style="Q"):
            """Is it fruit?"""
            return f"{style}: {text}\nA:"
        return fruit

    pairs = [(e["text"], e["answer"]) for e in EXAMPLES]
    f = make(pairs)
    assert f.__name__ == "fruit" and f.__doc__ == "Is it fruit?" and not fits and not cache.exists()
    ans = f("apple pie 1")
    assert ans in ("a", "b") and fits == [1] and cache.exists()
    assert f(text="apple pie 1") == ans and f.map(["apple pie 1", {"text": "apple pie 1"}, ("apple pie 1", "Q")]) == [ans] * 3
    assert max(f.scores("apple pie 1"), key=f.scores("apple pie 1").get) == ans
    assert f.prompt("x") == "Q: x\nA:" and f.classifier.readout.meta["task"] == "fruit"
    same = Classifier.fit((m, tok), EXAMPLES, template=TEMPLATE, alpha_mult=2.0)
    assert f.map([e["text"] for e in EXAMPLES]) == same.predict([e["text"] for e in EXAMPLES])
    n = len(fits)
    g = make(EXAMPLES)                                           # the same examples as dicts: the saved fit is reused
    assert g("apple pie 1") == ans and len(fits) == n
    h = make(pairs[:-2])                                         # different examples: fitted again
    h("apple pie 1")
    assert len(fits) == n + 1
