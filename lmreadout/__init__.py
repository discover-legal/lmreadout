"""lmreadout: pull a two-label classifier out of a causal language model's final hidden state and write it into
the model's own output rows, with no training step.

    from lmreadout import collect, fit, twofold, patch, Readout
"""
from .core import Readout, collect, fit, twofold, patch, load_model, predict_items, label_token_ids

__all__ = ["Readout", "collect", "fit", "twofold", "patch", "load_model", "predict_items", "label_token_ids"]
__version__ = "0.1.0"
