# lmreadout

Pull a classifier out of a causal language model's own hidden state and write it into the model's output rows.
No training step: a few averages and one ridge regression per answer, written into the rows of the answer tokens.
The plain model then answers the task without a wrapper, a prompt trick or a separate classifier. Two answers
(Yes / No) or more (World / Sports / Business / Science).

## Where it came from

The method was developed in the Handi experiment (https://github.com/discover-legal/Handi), on LegalBench:

- **Ten tasks, Qwen3.5-0.8B, a few hundred labelled examples:** mean accuracy 0.57 as shipped, 0.78 after the edit.
  On examples the edit never saw: overruling 0.94, definition classification 0.98, governing-law clauses 1.00.
- **But check it against plain word counts.** The same formula fed a count of the words in each item, instead of the
  model's state, scores 0.91, 0.86 and 0.997 on those three tasks. Governing law is solved by the words alone, so a
  perfect score there says nothing about what the model knows. Even an untrained model with random weights gets
  most of the way with a few hundred labels: at that size the formula does most of the work.
- **Where the model's state pays off is with few labels.** On the 132 two-answer LegalBench tasks, with 15 labelled
  examples each, the edit lifts Qwen from 0.56 to 0.73 balanced accuracy (guessing is 0.50), against 0.65 for word
  counts, and beats word counts on 105 of them. It also lifts Phi-4-mini from 0.68 to 0.76. It does best on contract
  clauses and worst on long merger agreements.
- **Bigger models gain less.** With 15 examples the edit adds 0.19 to Qwen3.5-0.8B, 0.09 to the 2B and 0.01 to the
  4B, which already answers well as shipped (mean over the 98 two-answer tasks all three finished).
- **More than two answers:** on 21 LegalBench tasks with three to eight answers it beats word counts on the six
  non-merger tasks at every number of examples tried, and is no better than word counts on the 15 merger-agreement
  (MAUD) tasks.

## Tried on five tasks, two of them legal

Qwen3.5-0.8B, installed from this repository into a clean environment, run through `lmreadout sweep`: for 15 and 120
labelled items, 20 random draws each, every other item scored. Balanced accuracy (each answer weighted equally;
guessing = 1 / number of answers), mean over the draws. Up to 1,000 items per task.

| Task | Answers | Guessing | As shipped | Word counts, 15 / 120 | Edited, 15 / 120 |
|---|---|---|---|---|---|
| News topic (AG News) | 4 | 0.25 | 0.27 | 0.31 / 0.59 | **0.67 / 0.81** |
| Overruling (LegalBench) | 2 | 0.50 | 0.69 | 0.69 / 0.87 | **0.89 / 0.94** |
| Function of a decision section (LegalBench) | 7 | 0.14 | 0.19 | 0.19 / 0.36 | **0.27 / 0.40** |
| Emotion in a message (dair-ai/emotion) | 6 | 0.17 | 0.21 | 0.17 / 0.20 | 0.35 / 0.47 |
| Yes/no question on a passage (BoolQ) | 2 | 0.50 | 0.65 | 0.51 / 0.51 | 0.57 / 0.61 |

What it shows:

- **Strong where the answer is a kind of text:** a topic, or whether a sentence overrules a case. On news topics the
  edit with 15 labels beats word counts with 120.
- **Weak on the seven-way legal task**, as in the Handi runs: above word counts, far from solved.
- **Emotion:** the calibration step alone does better on balanced accuracy (0.49 with 15 labels, 0.50 with 120) than
  the full edit, which leans towards the common emotions (accuracy 0.48 / 0.59, against 0.47 / 0.48 calibrated).
- **It hurts on BoolQ.** Whether a passage answers yes depends on the question and the passage together, and the
  final state does not carry that in a form this edit can read: below the model as shipped at every size. The fit
  command's held-out score shows this before you rely on it.

The overruling numbers match the Handi run on the same task within 0.03. On AG News, fitted on 1,000 training
stories and scored on 1,000 test stories, the edit scores 0.88, and the patched copy saved by `lmreadout patch` and
reloaded with plain `transformers` gives the same 0.876.

## Does it stay on script?

The edit decides between the answer tokens. Whether the model, left to write freely, says one of the answers at all
is a separate question; `eval` reports it ("free next token is one of the answers"):

| Task | As shipped | Edited |
|---|---|---|
| Overruling (worked examples in the prompt) | 100% | 100% |
| AG News, four worked examples in the prompt | 100% | 99.8% |
| AG News, no examples | 56.5% | 66.5% |
| BoolQ, no examples | 19.0% | 58.6% |
| Emotion, no examples | 92.6% | 35.6% |
| Function of a decision section (worked examples) | 100% | 59.2% |

Two things decide it. **Worked examples in the prompt** keep the model answering in the expected words; LegalBench's
prompts all have them, which is why the Handi runs never went off script. And **with more than two answers the
edit lowers every answer row together**: each answer's read-out is fitted as that answer against all the others, so
the intercepts sum to 2 minus the number of answers, which does not change which answer wins but lets other tokens
overtake all of them. With two answers the intercepts cancel. Either way, read the answer tokens' scores, as `eval`
and `predict` do, or restrict generation to the answers.

## Install

```
pip install git+https://github.com/hordruma/lmreadout
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

More than two answers: leave out `--labels` and every distinct `answer` in the data is used (sorted), or list them.
Each answer is read from the row of its first token after the prefix (a space by default), so answers of several
words work as long as their first tokens differ ("Procedural History" and "Rule" do; "Unilateral change" and
"Unilateral termination" do not, and `fit` says so). When every answer is a lone space token plus one more, as Qwen
writes the digits " 0" to " 9", the space goes at the end of the prompt and the digits are the rows.

```
lmreadout fit --model Qwen/Qwen3.5-0.8B --data news.jsonl --template news.txt --out news.npz --task topic
```

How many labelled items do you need? `sweep` fits on N items drawn at random, scores every other item, repeats for
several draws and prints the mean beside the model as shipped, calibration alone, and word counts fitted on the same
N items:

```
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data news.jsonl --template news.txt --sizes 15 30 60 120 --draws 20 \
                --csv news_sweep.csv
```

Score on items the fit never saw:

```
lmreadout eval --model Qwen/Qwen3.5-0.8B --readout governing_law.npz --data heldout.jsonl
```

Both commands print accuracy beside the share of the commonest answer, and balanced accuracy beside guessing;
`eval` also prints how often the free next token is one of the answers.
Balanced accuracy is the mean, over the answers, of the share of that answer's items answered correctly, so a model
that always gives one answer scores 1/K however lopsided the data.

Ship it either way:

```
# a patched copy of the model: the answer rows of lm_head changed, nothing else
lmreadout patch --model Qwen/Qwen3.5-0.8B --readout governing_law.npz --out qwen-governing-law/

# or as side heads on the unchanged model: several tasks at once, a few KB each
lmreadout predict --model Qwen/Qwen3.5-0.8B --readout governing_law.npz definitions.npz --data clauses.jsonl
```

From Python:

```python
from lmreadout import load_model, label_token_ids, collect, fit, twofold, patch, Readout
model, tok = load_model("Qwen/Qwen3.5-0.8B")
ids = label_token_ids(tok, ["No", "Yes"])
H, LAB, LSE = collect(model, tok, prompts, ids)          # final state + answer logits per prompt
print(twofold(H, LAB, LSE, gold))                        # commonest / shipped / calibrated / edited, held-out
r = fit(H, LAB, LSE, gold, labels=["No", "Yes"], label_ids=ids, template=template)
patch(model, r)                                          # or r.predict(H, LAB) without touching the model
```

## How it works

At the answer position the model holds a vector `h` (the final-norm hidden state). The output table `U` scores
token `t` as `U[t] . h`, and the model's answer is the answer token whose row scores highest. The read-out changes
only those rows:

1. **Calibration.** Shift each answer row along the unit mean state `mu` so every answer has the same mean
   log-probability on the fit items (`h . mu` is nearly constant after the final norm, so this is a clean per-answer
   offset). Removes the model's lean towards one answer.
2. **Read-out.** One ridge regression per answer, from `h` to +1 for that answer's items and -1 for the rest,
   regularisation = number of items on standardised features. Scaled so the spread of the differences between
   answers is twice the calibrated model's, and added to that answer's row, intercept carried along `mu`.

For two answers this is a single direction added to one row and subtracted from the other. Everything is closed
form; the defaults (regularisation = number of items, strength x2) are fixed, not tuned per task.

## What to check, every time

- **Held-out first.** `fit` prints a two-fold score where every item is scored by a read-out that never saw it; the
  in-sample number is not reported anywhere because it is meaningless (0.89 to 1.00 on every task we tried).
- **If the held-out score is at the commonest-answer rate, stop.** The model does not know the task in a linearly
  readable form at the answer position. `fit` warns. No output-row edit can create what is not there.
- **Compare against plain word counts.** Fit any bag-of-words classifier on the same labelled items and score it on
  the same held-out items. If it does as well, the score comes from your labels, not from the model.
- **One task per set of answer rows when patching.** The Yes and No rows are read by every Yes/No prompt, so a
  patched model's Yes/No behaviour changes on other tasks (2% to 97% of answers in our test) and two tasks patched
  into the same rows mostly cancel. For several tasks use `predict` (side heads) or give each task its own answer
  tokens.
- **Verify the patch.** After `patch`, score the held-out items with your ordinary pipeline; it should match `eval`
  to a few decimals. `collect` checks once that it has found the hidden state `lm_head` actually reads and refuses
  architectures where it cannot.

## Limits

- Answers are read by their first token, so answers that share it (for example "Unilateral change" and
  "Unilateral termination") cannot be told apart.
- Fixed answer sets only: not free text copied from the item, not sets of answers.
- The edit decides between the answer tokens; it does not stop the model preferring some other token (see "Does it
  stay on script?").
- Tasks that need the item and the question combined, like BoolQ, can get worse. Check the held-out score.
- The read-out sits at the final layer. Linear probes a few layers earlier are usually a little better (0.84 vs
  0.78 mean in our runs); reaching them needs an edit inside the network, which this tool does not do.
- It adds no knowledge.

## Tests

```
pip install -e .[dev] && pytest
```

The tests use synthetic states and a toy tokenizer and check: answers read by first token, digits after a space,
clashing first tokens refused; the sweep and the word-count control; a planted direction recovered for two and four
answers; the row edit reproduces the offline scores exactly; the two-answer edit is identical to version 0.1's;
save/load, including 0.1 files; patch touches only the answer rows. No model download.

## Licence

MIT. See `LICENSE`.
