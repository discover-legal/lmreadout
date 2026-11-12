"""lmreadout: pull a classifier (two or more labels) out of a causal language model's final hidden state and write
it into the model's own output rows: closed form, no gradient training.

    from lmreadout import collect, fit, fit_auto, twofold, patch, Readout
"""
from .core import (Readout, collect, fit, twofold, patch, load_model, predict_items, accuracy,
                   balanced_accuracy, answer_tokens, sweep, wordcount_predict, tune, fit_auto, candidates,
                   preferred_strength)

__all__ = ["Readout", "collect", "fit", "twofold", "patch", "load_model", "predict_items", "accuracy",
           "balanced_accuracy", "answer_tokens", "sweep", "wordcount_predict", "tune", "fit_auto", "candidates",
           "preferred_strength"]
__version__ = "0.4.0"
