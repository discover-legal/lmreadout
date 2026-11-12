"""lmreadout: pull a classifier (two or more labels) out of a causal language model's final hidden state and write
it into the model's own output rows: closed form, no gradient training.

    from lmreadout import collect, fit, twofold, patch, Readout
"""
from .core import (Readout, collect, fit, twofold, patch, load_model, predict_items, label_token_ids, accuracy,
                   balanced_accuracy, answer_tokens, sweep, wordcount_predict)

__all__ = ["Readout", "collect", "fit", "twofold", "patch", "load_model", "predict_items", "label_token_ids", "accuracy",
           "balanced_accuracy", "answer_tokens", "sweep", "wordcount_predict"]
__version__ = "0.3.3"
