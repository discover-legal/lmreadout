# lmreadout

Pull a two-label classifier out of a causal language model's own hidden state and write it into the model's
output rows. No training step: two averages and one ridge regression, written into the rows for the two label
tokens. The plain model then answers the task without a wrapper, a prompt trick or a separate classifier.

Where it came from: on Qwen3.5-0.8B and ten LegalBench tasks this took the mean accuracy from 0.57 (as shipped) to
0.78, and to 0.94, 0.98 and 1.00 on overruling, definition classification and governing-law clauses scored on
items the read-out never saw. Deleting the stock phrases from the clauses ("governed by the laws of") left it at
0.997. The experiment and its numbers are in the Handi report: https://github.com/discover-legal/Handi.

## Install

```
pip install git+https://github.com/discover-legal/lmreadout
```

Needs `torch`, `transformers`, `numpy`. Any Hugging Face causal LM whose weights you can load; an 8 GB GPU is
enough for 1B-class models, CPU works for small ones.

## Use

Items are JSON lines with the fields your prompt template uses and an `answer`:

```
{"text": "This Agreement shall be governed by the laws of the State of Delaware.", "answer": "Yes"}
{"text": "Either party may terminate on thirty days' notice.", "answer": "No"}
```

The template ends exactly where the answer goes:

```
Does the clause specify which state/country's law governs the contract?

Clause: {{text}}
Label:
```

Fit (prints the honest two-fold score, then saves a read-out fitted on everything):

```
lmreadout fit --model Qwen/Qwen3.5-0.8B --data governing_law.jsonl --template governing_law.txt \
              --labels No Yes --out governing_law.npz --task governing_law
```

Score on items the fit never saw:

```
lmreadout eval --model Qwen/Qwen3.5-0.8B --readout governing_law.npz --data heldout.jsonl
```

Ship it either way:

```
# a patched copy of the model: two rows of lm_head changed, nothing else
lmreadout patch --model Qwen/Qwen3.5-0.8B --readout governing_law.npz --out qwen-governing-law/

# or as side heads on the unchanged model: several tasks at once, a few KB each
lmreadout predict --model Qwen/Qwen3.5-0.8B --readout governing_law.npz definitions.npz --data clauses.jsonl
```

From Python:

```python
from lmreadout import load_model, label_token_ids, collect, fit, twofold, patch, Readout
model, tok = load_model("Qwen/Qwen3.5-0.8B")
ids = label_token_ids(tok, ["No", "Yes"])
H, LAB, LSE = collect(model, tok, prompts, ids)          # final state + label logits per prompt
print(twofold(H, LAB, LSE, gold))                        # majority / shipped / calibrated / edited, held-out
r = fit(H, LAB, LSE, gold, labels=["No", "Yes"], label_ids=ids, template=template)
patch(model, r)                                          # or r.predict(H, LAB) without touching the model
```

## How it works

At the answer position the model holds a vector `h` (the final-norm hidden state). The output table `U` scores
token `t` as `U[t] . h`; the answer is `Yes` when `U[Yes] . h > U[No] . h`. The read-out changes only those two
rows:

1. **Calibration.** Shift each label row along the unit mean state `mu` so the two labels have equal mean
   log-probability on the fit items (`h . mu` is nearly constant after the final norm, so this is a clean per-label
   offset). Removes the model's lean towards one answer.
2. **Read-out.** Ridge regression from `h` to the label (+1 / -1), regularisation = number of items on standardised
   features. Scaled so its spread is twice the calibrated gap's, added to the Yes row and subtracted from the No row,
   intercept carried along `mu`.

The new gap is `gap_calibrated(h) + 2 alpha (w . h + b)`. Everything is closed form.

## What to check, every time

- **Held-out first.** `fit` prints a two-fold score where every item is scored by a read-out that never saw it; the
  in-sample number is not reported anywhere because it is meaningless (0.89 to 1.00 on every task we tried).
- **If the held-out score is at the majority rate, stop.** The model does not know the task in a linearly readable
  form at the answer position. `fit` warns. No output-row edit can create what is not there.
- **One task per label pair when patching.** The Yes and No rows are read by every Yes/No prompt, so a patched
  model's Yes/No behaviour changes on other tasks (2% to 97% of answers in our test) and two tasks patched into the
  same rows mostly cancel. For several tasks use `predict` (side heads) or give each task its own label tokens.
- **Check what it is reading.** Delete or paraphrase the stock phrases in your held-out items and re-run `eval`. If
  the score collapses, the read-out is a phrase detector.
- **Verify the patch.** After `patch`, score the held-out items with your ordinary pipeline; it should match `eval`
  to a few decimals. `collect` checks once that it has found the hidden state `lm_head` actually reads and refuses
  architectures where it cannot.

## Limits

- Two labels, one token each after the prefix (default a space). Multi-token labels: pick spellings whose first
  tokens differ, or use `--label-prefix`.
- The read-out sits at the final layer. Linear probes a few layers earlier are usually a little better (0.84 vs
  0.78 mean in our runs); reaching them needs an edit inside the network, which this tool does not do.
- It adds no knowledge.

## Tests

```
pip install -e .[dev] && pytest
```

The tests use synthetic states and check the arithmetic (planted direction recovered; the row edit reproduces
the offline gap exactly; save/load; patch touches only the two rows). No model download.

## Licence

MIT. See `LICENSE`.
