"""lmreadout: pull a classifier (two or more labels) out of a causal language model's final hidden state and write
it into the model's own output rows: closed form, no gradient training.

    from lmreadout import Classifier, classifier                      # an object you call, or a decorator
    from lmreadout import collect, fit, fit_auto, twofold, patch, Readout   # the pieces
"""
from .api import Classifier, classifier
from .core import (Readout, collect, fit, twofold, patch, patched, load_model, predict_items, accuracy,
                   balanced_accuracy, answer_tokens, sweep, wordcount_predict, tune, fit_auto, candidates,
                   preferred_strength)

__all__ = ["Classifier", "classifier", "Readout", "collect", "fit", "twofold", "patch", "patched", "load_model",
           "predict_items", "accuracy", "balanced_accuracy", "answer_tokens", "sweep", "wordcount_predict", "tune",
           "fit_auto", "candidates", "preferred_strength"]
__version__ = "0.5.0"
