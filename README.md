# lmreadout

Pull a classifier out of a causal language model's own hidden state and write it into the model's output rows.
No gradient training: a label-bias calibration and one ridge regression per answer, fitted in closed form on a few
labelled examples and written into the rows of the answer tokens. The plain model then answers the task without a
wrapper, a prompt trick or a separate classifier. Two answers (Yes / No) or more (World / Sports / Business /
Science). It helps on some tasks and hurts on others, so measure it on yours (`sweep`, below) before relying on it.

Both halves are known tools: calibrating a model's lean towards one answer (Zhao et al. 2021; Zhou et al. 2024) and
a linear probe on its hidden state (Alain & Bengio 2016; with tens of labels, Buckmann & Hill 2024). What this
package adds is writing the two into the model's own output table, so the unmodified inference code gives the
probe's answer. See "Prior work" at the end.

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
  counts, and beats word counts on 105 of them. The calibration step alone, which needs no labels for its answer
  choice, already gives 0.66; the read-out adds the rest. It also lifts Phi-4-mini from 0.68 to 0.76 (calibration
  alone 0.71). It does best on contract clauses and worst on long merger agreements.
- **Bigger models gain less.** With 15 examples the edit adds 0.19 to Qwen3.5-0.8B, 0.09 to the 2B and 0.01 to the
  4B, which already answers well as shipped (mean over the 98 two-answer tasks all three finished).
- **More than two answers:** on 21 LegalBench tasks with three to eight answers it beats word counts on the six
  non-merger tasks at every number of examples tried, and is no better than word counts on the 15 merger-agreement
  (MAUD) tasks.

## Tried on six tasks, two of them legal

Qwen3.5-0.8B, installed from this repository into a clean environment, run through `lmreadout sweep`: for 15 and 120
labelled items, 20 random draws each, all the remaining items scored. Balanced accuracy (each answer weighted
equally; guessing = 1 / number of answers), mean over the draws. Up to 1,000 items per task. The tweet task was
chosen and run by a separate agent that had only this README, with its plan written down before any score.

| Task | Answers | Guessing | As shipped | Calibration only, 15 / 120 | Word counts, 15 / 120 | Edited, 15 / 120 |
|---|---|---|---|---|---|---|
| News topic (AG News) | 4 | 0.25 | 0.27 | 0.59 / 0.61 | 0.31 / 0.59 | **0.67 / 0.81** |
| Overruling (LegalBench) | 2 | 0.50 | 0.69 | 0.83 / 0.85 | 0.69 / 0.87 | **0.89 / 0.94** |
| Function of a decision section (LegalBench) | 7 | 0.14 | 0.19 | 0.28 / 0.28 | 0.19 / 0.36 | 0.27 / **0.40** |
| Emotion in a message (dair-ai/emotion) | 6 | 0.17 | 0.21 | **0.49 / 0.50** | 0.17 / 0.20 | 0.35 / 0.47 |
| Tweet sentiment (tweet_eval) | 3 | 0.33 | 0.44 | **0.44** / 0.46 | 0.34 / 0.36 | 0.40 / **0.48** |
| Yes/no question on a passage (BoolQ) | 2 | 0.50 | **0.65** | 0.65 / 0.65 | 0.51 / 0.51 | 0.57 / 0.61 |

What it shows:

- **Strong where the answer is a kind of text:** a topic, or whether a sentence overrules a case. On news topics the
  edit with 15 labels beats word counts with 120.
- **With 15 labels it can make things worse:** below calibration alone on emotion and tweets (on the seven-way legal
  task the two are level), and below the model as shipped on tweets and BoolQ. On tweets it passes the model as shipped from 60 labels
  (0.45; 0.48 at 120; on 400 test items after fitting on 300: 0.51 shipped, 0.53 edited).
- **Why it hurts** (our reading of these runs, not a tested account): the read-out is added at a fixed strength
  whatever its quality, so with few labels on a label the final state carries weakly it adds mostly noise on top of
  the model's own answer; it improves steadily with more labels on every task. With uneven answers (emotion, tweets)
  it also learns the common ones, so plain accuracy rises while balanced accuracy falls (emotion at 15 labels:
  accuracy 0.48 edited vs 0.47 calibrated, balanced 0.35 vs 0.49). And on BoolQ the answer depends on the question
  and passage together: word counts stay at guessing (0.51) and 120 labels are not enough for the read-out to beat
  the model's own answer.
- **Only `sweep` shows the harm reliably.** On BoolQ the score `fit` prints (fitted on 250, scored on the other 250)
  is level with the model as shipped (0.643 shipped, 0.646 edited, with 0.3.1's split), and so is `eval` on 500 new items (0.652,
  0.661); the drop appears with 15 to 120 labels. `fit` warns when its held-out score falls below the model as
  shipped.

The overruling numbers match the Handi run on the same task within 0.03. On AG News, fitted on 1,000 training
stories and scored on 1,000 test stories, the edit scores 0.88, and the patched copy saved by `lmreadout patch` and
reloaded with plain `transformers` gives the same 0.876.

## Does it stay on script?

The edit decides between the answer tokens. Whether the model, left to write freely, says one of the answers at all
is a separate question; `eval` reports it ("free next token is one of the answers"):

| Task | As shipped | Edited, 0.3.0 | Edited, 0.3.1 |
|---|---|---|---|
| Overruling (worked examples in the prompt) | 100% | 100% | 100% |
| AG News, four worked examples in the prompt | 100% | 99.8% | 100% |
| AG News, no examples | 56.5% | 66.5% | 91.9% |
| BoolQ, no examples | 19.0% | 58.6% | 58.6% |
| Tweet sentiment, no examples | 48.0% | | 58.2% |
| Emotion, no examples | 92.6% | 35.6% | 92.8% |
| Function of a decision section (worked examples) | 100% | 59.2% | 100% |

Two things decide it. **Worked examples in the prompt** keep the model answering in the expected words; LegalBench's
prompts all have them, which is why the Handi runs never went off script. And **the intercepts**: each answer's
read-out is fitted as that answer against all the others, so up to 0.3.0 the intercepts summed to 2 minus the number
of answers and lowered every answer row together, letting other tokens overtake all of them. Since 0.3.1 they are
centred (their mean removed). That changes no difference between answers, so every chosen answer and every score
above is the same as in 0.3.0; with two answers they already cancelled, so two-answer read-outs are unchanged.
Read-outs saved by 0.2 or 0.3.0 are centred when loaded. Without worked examples the model can still wander (BoolQ
above), so read the answer tokens' scores, as `eval` and `predict` do, or restrict generation to the answers.

## Install

```
pip install git+https://github.com/discover-legal/lmreadout
```

Needs `torch`, `numpy` and `transformers` 5.2 or later (the first with Qwen3.5). For a CPU-only machine, install
torch from its CPU index first (`pip install torch --index-url https://download.pytorch.org/whl/cpu`), or pip may pull
the much larger CUDA build.

Tested on Qwen3.5-0.8B. The code checks once that it has found the hidden state the output table reads and refuses
models where it cannot; other architectures pass the unit tests on tiny random models but have not been run on a
task. Models are loaded in float32: an 8 GB GPU is enough for 1B-class models; on CPU expect under a second per short
item for Qwen3.5-0.8B (transformers warns that it falls back to slower kernels; that is expected).

## Use

Items are JSON lines with the fields your prompt template uses and an `answer` (other fields are ignored, and
`predict` passes them through):

```
{"text": "This Agreement shall be governed by the laws of the State of Delaware.", "answer": "Yes"}
{"text": "Either party may terminate on thirty days' notice.", "answer": "No"}
```

The template ends exactly where the answer goes (a line break at the very end of the file is removed, with a
note):

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

How many labelled items do you need? `sweep` fits on N items drawn at random, scores all the remaining items,
repeats for several draws and prints the mean beside the model as shipped, calibration alone, and word counts fitted
on the same N items. Word counts are the control: the same per-answer ridge fed a count of each word (words in at
least two of the N items) instead of the model's state. If they do as well, the score comes from your labels, not
from the model:

```
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data news.jsonl --template news.txt --sizes 15 30 60 120 --draws 20 \
                --csv news_sweep.csv
```

Score on items the fit never saw:

```
lmreadout eval --model Qwen/Qwen3.5-0.8B --readout governing_law.npz --data heldout.jsonl
```

`fit` and `eval` print accuracy beside the share of the commonest answer, and balanced accuracy beside guessing, for
the model as shipped, calibration alone and the full edit; `eval` also prints how often the free next token is one
of the answers. `sweep` prints balanced accuracy with accuracy in brackets.
Balanced accuracy is the mean, over the answers, of the share of that answer's items answered correctly, so a model
that always gives one answer scores 1/K however lopsided the data.

Ship it either way:

```
# a patched copy of the model: the answer rows of lm_head changed, nothing else
lmreadout patch --model Qwen/Qwen3.5-0.8B --readout governing_law.npz --out qwen-governing-law/

# or as side heads on the unchanged model: several tasks at once, a few KB each
lmreadout predict --model Qwen/Qwen3.5-0.8B --readout governing_law.npz definitions.npz --data clauses.jsonl
```

Every command takes `--model` and `--device cuda|cpu` (default: cuda when available). All but `patch` take
`--max-len` (prompts are cut to their last N tokens, default 1024, with a warning saying how many were cut) and
`--max-items` (use only the first N items). `fit` and `sweep` also take `--labels`, `--label-prefix` (text put
before each answer when tokenising, default a space; `eval` and `predict` reuse the one saved in the read-out),
`--lam`, `--alpha-mult` and `--auto`; `sweep` takes `--sizes` (at least 2), `--draws` (at least 1), `--seed` and
`--csv`. `lmreadout <command> --help` lists them.

Check a patched copy with plain `transformers` (answers are read from the first token of " " + answer):

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
m = AutoModelForCausalLM.from_pretrained("qwen-governing-law/"); tok = AutoTokenizer.from_pretrained("qwen-governing-law/")
ids = [tok(" " + a, add_special_tokens=False)["input_ids"][0] for a in ["No", "Yes"]]
logits = m(**tok(prompt, return_tensors="pt", add_special_tokens=False)).logits[0, -1]
answer = ["No", "Yes"][int(logits[ids].argmax())]       # should match `eval` / `predict` item for item
```

From Python:

```python
from lmreadout import load_model, answer_tokens, collect, fit, fit_auto, twofold, patch, Readout
model, tok = load_model("Qwen/Qwen3.5-0.8B")
ids, suffix = answer_tokens(tok, ["No", "Yes"])         # suffix: text to add to the prompt (usually "")
H, LAB, LSE = collect(model, tok, prompts, ids)          # final state + answer logits per prompt
size = model.num_parameters()                           # sets which strength ties go to
print(twofold(H, LAB, LSE, gold, auto=True, n_params=size))   # commonest / shipped / calibrated / edited, held-out
r, choice = fit_auto(H, LAB, LSE, gold, n_params=size, labels=["No", "Yes"], label_ids=ids, template=template)
if r is not None:                                        # None: leave the model as it is
    patch(model, r)                                      # or r.predict(H, LAB) without touching the model
```

## How it works

At the answer position the model holds a vector `h` (the final-norm hidden state). The output table `U` scores
token `t` as `U[t] . h`, and the model's answer is the answer token whose row scores highest. The read-out changes
only those rows:

1. **Calibration.** Shift each answer row along the unit mean state `mu` so every answer has the same mean
   log-probability on the fit items (`h . mu` is nearly constant after the final norm, so this is a clean per-answer
   offset). Removes the model's lean towards one answer.
2. **Read-out.** One ridge regression per answer, from `h` to +1 for that answer's items and -1 for the rest,
   regularisation = number of items on standardised features. Scaled so that half the read-out's difference between
   two answers spreads twice as wide as the calibrated model's difference (so the read-out adds four times that
   spread to the differences between answers; the same scaling as the Handi runs), and added to that answer's row,
   intercept carried along `mu`. The intercepts are centred, so the edit does not lower every answer row together.

For two answers this is a single direction added to one row and subtracted from the other. Everything is closed
form; the defaults (regularisation = number of items, strength x2) are fixed, not tuned per task.

## What to check, every time

- **Held-out first.** `fit` prints a two-fold score where every item is scored by a read-out that never saw it; the
  in-sample number is not reported anywhere because it is meaningless (0.89 to 1.00 on all ten of the Handi tasks
  where it was measured).
- **Run `sweep` at the number of labels you have.** With few labels the edit can score below calibration alone or
  the model as shipped (see the table above); `fit`'s two-fold score uses half your items and can hide that.
- **If the held-out score is at the commonest-answer rate, stop.** The model does not know the task in a linearly
  readable form at the answer position. `fit` warns. No output-row edit can create what is not there.
- **Compare against plain word counts.** Fit any bag-of-words classifier on the same labelled items and score it on
  the same held-out items. If it does as well, the score comes from your labels, not from the model.
- **One task per set of answer rows when patching.** The Yes and No rows are read by every Yes/No prompt, so a
  patched model's Yes/No behaviour changes on other tasks (2% to 97% of answers in our test) and two tasks patched
  into the same rows mostly cancel. For several tasks use `predict` (side heads) or give each task its own answer
  tokens.
- **Verify the patch.** After `patch`, score the held-out items with your ordinary pipeline; it should match `eval`
  to a few decimals. `collect` checks once that it has found the hidden state the output table actually reads and refuses
  architectures where it cannot.

## Limits

- Answers are read by their first token, so answers that share it (for example "Unilateral change" and
  "Unilateral termination") cannot be told apart.
- Fixed answer sets only: not free text copied from the item, not sets of answers.
- The edit decides between the answer tokens; without worked examples in the prompt the model can still prefer some
  other token (see "Does it stay on script?").
- Tasks that need the item and the question combined, like BoolQ, can get worse. So can tasks where the model is
  already decent and labels are few (tweets). Check with `sweep`.
- The read-out's strength is fixed (x2), not tuned to how reliable it is; with few labels that is often too much.
- Prompts are tokenised without special tokens (no beginning-of-sequence token). Qwen uses none; models that expect
  one (Llama 3, Gemma) may score lower than they should.
- The read-out sits at the final layer. Linear probes a few layers earlier are usually a little better (0.84 vs
  0.78 mean in our runs); reaching them needs an edit inside the network, which this tool does not do.
- A patched copy is saved in float32 with its output table untied (about 4 GB for the 0.8B).
- It adds no knowledge: it can only surface what the model's state already carries (compare Takehi et al.'s finding
  that weight edits can uncover an ability but not add one).

## Tests

```
pip install -e ".[dev]" && pytest
```

The tests use synthetic states, a toy tokenizer and tiny randomly initialised models, and check: answers read by
first token, digits after a space, clashing first tokens refused; the sweep and the word-count control; a planted
direction recovered for two and four answers; the row edit reproduces the offline scores exactly; the intercepts are
centred without changing any answer; the two-answer edit is identical to version 0.1's; save/load, including 0.1
files; patch touches only the answer rows, on float32 and bfloat16 models; a warning when prompts are cut; a fit
with one answer refused, and the two-fold split surviving data ordered No, Yes, No, Yes; a line break at the end of
the template removed; `--auto`'s grid, tie order and size rule, its use of a planted direction, leaving a model that
is already right unchanged, and the fallback when an answer is short of items; refusals of sweep sizes under two,
no draws, predictions that would overwrite a field, fixed settings passed with auto, and reserved meta keys. No
model download.

## Prior work

- Takehi, Teoh, Zhang, Khattab, "Sparks of Weight-Space Programming: LLMs can natively read & write neural network
  weights", MIT CSAIL blog post, 2 Nov 2026, https://rikiyat.github.io/blog/weight-space-programming/. GPT-6 Astra
  edits Qwen3.5-0.8B's weights without gradients, and concludes from its Gemma 3 270M edits: "Editing weights could
  remove an obstacle that hid an ability, but it could not add an ability the model lacked." The Handi experiment
  this came from was prompted by it.
- Zhao, Wallace, Feng, Klein, Singh, "Calibrate Before Use: Improving Few-Shot Performance of Language Models",
  ICML 2021, https://arxiv.org/abs/2102.09690 (label-token bias).
- Zhou, Wan, Proleev, Mincu, Chen, Heller, Roy, "Batch Calibration: Rethinking Calibration for In-Context Learning
  and Prompt Engineering", ICLR 2024, https://arxiv.org/abs/2309.17249 (bias estimated from the mean over items,
  closest to the calibration step here).
- Alain, Bengio, "Understanding intermediate layers using linear classifier probes", 2016,
  https://arxiv.org/abs/1610.01644.
- Buckmann, Hill, "Logistic Regression makes small LLMs strong and explainable 'tens-of-shot' classifiers", 2024,
  https://arxiv.org/abs/2408.03414 (a regularised linear classifier on a small LM's states with tens of labels).
- Cho et al., "Prompt-Augmented Linear Probing: Scaling beyond the Limit of Few-shot In-Context Learners", AAAI 2023,
  https://arxiv.org/abs/2212.10873; Abbas et al., "Enhancing In-context Learning via Linear Probe Calibration",
  AISTATS 2024, https://arxiv.org/abs/2401.12406.
- Orgad et al., "LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations", ICLR 2025,
  https://arxiv.org/abs/2410.02707; Burns, Ye, Klein, Steinhardt, "Discovering Latent Knowledge in Language Models
  Without Supervision", ICLR 2023, https://arxiv.org/abs/2212.03827 (hidden states carry more than the output says).
- Li, Patel, Viégas, Pfister, Wattenberg, "Inference-Time Intervention: Eliciting Truthful Answers from a Language
  Model", NeurIPS 2023, https://arxiv.org/abs/2306.03341 (activations steered along probe directions at inference time).
- Guha et al., "LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language
  Models", NeurIPS 2023 Datasets and Benchmarks, https://arxiv.org/abs/2308.11462. Other data: AG News (Zhang, Zhao,
  LeCun 2015), dair-ai/emotion, tweet_eval (Barbieri et al. 2020), BoolQ (Clark et al. 2019).

## Licence

MIT. See `LICENSE`.
