# lmreadout

Pull a classifier out of a causal language model's own hidden state and write it into the model's output rows.
No gradient training: a label-bias calibration and one ridge regression per answer, fitted in closed form on a few
labelled examples and written into the rows of the answer tokens. The plain model then answers the task without a
wrapper, a prompt trick or a separate classifier. Two answers (Yes / No) or more (World / Sports / Business /
Science). With fixed settings it helps on some tasks and hurts on others; `--auto` chooses the settings from your
labelled examples and may leave the model alone, and in our tests it never did more than slight harm (below). Still
measure it on your task (`sweep`) before relying on it.

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
  The fixed strength was since checked in part: choosing it per task (`--auto`, next section) removes most of the
  harm on these tasks, which supports that reading without proving it.
- **Only `sweep` shows the harm reliably.** On BoolQ the score `fit` prints (fitted on 250, scored on the other 250)
  is level with the model as shipped (0.643 shipped, 0.646 edited, with 0.3.1's split), and so is `eval` on 500 new items (0.652,
  0.661); the drop appears with 15 to 120 labels. `fit` warns when its held-out score falls below the model as
  shipped.

The overruling numbers match the Handi run on the same task within 0.03. On AG News, fitted on 1,000 training
stories and scored on 1,000 test stories, the edit scores 0.88, and the patched copy saved by `lmreadout patch` and
reloaded with plain `transformers` gives the same 0.876.

## Letting it choose its settings (`--auto`)

Three settings decide how the edit behaves: how much of the model's lean to remove (none, half, all), how hard the
read-out overrides the model's own answer (strength 0, 0.5, 1, 2 or 4; the fixed default is 2) and how much the
read-out is smoothed (ridge n/4, n or 4n, with n the number of labelled items). `fit --auto` tries every
combination, scores each by cross-validation on your labelled items alone (leave one out up to 50 items, ten folds
above), and keeps the best by balanced accuracy. It leaves the model unchanged unless some edit scores strictly
higher, and says so. Ties between edits go to a strength that steps down with model size (2 below 3B parameters, 1
below 7B, 0.5 from 7B), because bigger models' own answers deserve more weight. When some answer has fewer than two
labelled items nothing can be cross-validated, so it removes the lean only (that needs no labels) and tells you which
answers to label more of. `sweep --auto` adds an "auto" column, chosen inside each draw from the N items alone.

Why: in the Handi runs the fixed strength was too strong for bigger models. With 15 labels the fixed edit took
Qwen3.5-9B below the model as shipped on LegalBench's two-answer tasks; at half strength it would have helped.

Tested the same way as the table above (a separate agent, installing from GitHub, 20 draws per size), plus a task
never used before, chosen with its plan written before any score (Rotten Tomatoes movie reviews), and Qwen3.5-4B on
two tasks. Balanced accuracy, 15 / 120 labelled items:

| Task, model | As shipped | Calibration only | Fixed edit | `--auto` |
|---|---|---|---|---|
| AG News, 0.8B | 0.27 | 0.59 / 0.61 | **0.67** / 0.81 | 0.65 / **0.82** |
| Overruling, 0.8B | 0.69 | 0.83 / 0.85 | **0.89 / 0.94** | **0.89 / 0.94** |
| Function of a decision section, 0.8B | 0.19 | **0.28** / 0.28 | 0.27 / 0.40 | **0.28 / 0.41** |
| Emotion, 0.8B | 0.21 | **0.49 / 0.50** | 0.35 / 0.47 | **0.49 / 0.50** |
| Tweet sentiment, 0.8B | 0.44 | 0.44 / 0.46 | 0.40 / 0.48 | **0.45 / 0.51** |
| BoolQ, 0.8B | **0.65** | **0.65 / 0.65** | 0.57 / 0.61 | 0.63 / 0.64 |
| Rotten Tomatoes (new), 0.8B | 0.82 | **0.86 / 0.88** | 0.85 / 0.86 | 0.85 / 0.87 |
| Tweet sentiment, 4B | 0.57 | **0.63 / 0.64** | 0.53 / 0.59 | 0.62 / 0.62 |
| Rotten Tomatoes (new), 4B | 0.82 | **0.88 / 0.89** | 0.87 / 0.88 | 0.87 / **0.89** |

- **It does no real harm.** With 15 labels it is never more than 0.02 below the model as shipped (worst: BoolQ,
  0.632 against 0.648; the fixed edit lost 0.075 there; at any number of labels tried the worst is BoolQ at 60,
  0.623 against 0.647), and on average it is level with the better of the model as
  shipped and calibration alone (+0.01), which you would not know in advance.
- **With 120 labels it matches or beats the fixed edit on every task** (worst: overruling, 0.001 below).
- **It is not always the best choice.** With 15 labels cross-validation is noisy, so on some tasks it lands a little
  below calibration alone (Rotten Tomatoes 0.85 against 0.86; tweets on the 4B 0.62 against 0.63, and 0.61 against
  0.63 at 60 labels).
- **Balanced, not plain, accuracy.** It optimises balanced accuracy; with uneven answers (tweets, emotion) plain
  accuracy can fall while balanced accuracy rises.

On LegalBench (the Handi runs' saved states, 98 two-answer tasks, 15 labels), `--auto` gives 0.80 / 0.84 / 0.86 for
Qwen3.5-2B / 4B / 9B, against 0.81 / 0.82 / 0.83 for the fixed edit and 0.72 / 0.81 / 0.84 as shipped. These are the
tasks the method was developed on, so they are not a clean test.

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

or, from a checkout, `pip install .` (`pip install -e ".[dev]"` to work on it). `python -m build` makes a wheel and
a source archive in `dist/`. This installs the `lmreadout` command and the `lmreadout` Python package.

Needs `torch`, `numpy` and `transformers` 5.2 or later (the first with Qwen3.5). For a CPU-only machine, install
torch from its CPU index first (`pip install torch --index-url https://download.pytorch.org/whl/cpu`), or pip may pull
the much larger CUDA build.

Tested on Qwen3.5-0.8B. The code checks once that it has found the hidden state the output table reads and refuses
models where it cannot; other architectures pass the unit tests on tiny random models but have not been run on a
task. Models are loaded in float32: an 8 GB GPU is enough for 1B-class models; on CPU expect under a second per short
item for Qwen3.5-0.8B (transformers warns that it falls back to slower kernels; that is expected).

## In your code

Give it a model and labelled examples; get back something you call. By default the settings are chosen from the
examples (`--auto`, above), which can mean leaving the model alone: the classifier then gives the model's own answer
among the labels. Nothing is written into the model unless you ask.

```python
from lmreadout import Classifier

clf = Classifier.fit(
    "Qwen/Qwen3.5-0.8B",                       # a model id or path, or (model, tokenizer) you already loaded
    "governing_law.jsonl",                     # or a list of dicts, or (item, answer) pairs
    template="Does the clause say which law governs the contract?\n\nClause: {{text}}\nLabel:",
)
clf("This Agreement shall be governed by the laws of the State of Delaware.")     # "Yes"
clf.predict(["...", "..."])                   # a list of answers
clf.scores(["..."])                           # [{"No": 0.08, "Yes": 0.92}]: probabilities among the answers
clf.report                                    # the held-out two-fold scores, as `fit` prints them
clf.settings, clf.unchanged                   # what was chosen; True when the model was left alone
clf.sweep(sizes=(15, 30, 60))                 # how it does at fewer examples, beside word counts

clf.save("governing_law.npz")                 # the read-out alone; works with the command line too
clf = Classifier.load("governing_law.npz")    # loads the model the read-out names, or pass one
```

As a decorator: the function writes the prompt, the decorated function returns the answer. It is fitted on the
first call; with `cache=` the fit is saved and reused while the model, the prompts, the answers and the settings
stay the same. Tasks on the same model id share one loaded copy.

```python
from lmreadout import classifier

@classifier("Qwen/Qwen3.5-0.8B", examples="governing_law.jsonl", cache="governing_law.npz")
def governing_law(text):
    return f"Does the clause say which law governs the contract?\n\nClause: {text}\nLabel:"

governing_law("Either party may terminate on thirty days' notice.")    # "No"
governing_law.scores("...")                   # {"No": 0.9, "Yes": 0.1}
governing_law.map(["...", "..."])             # many at once
governing_law.classifier                      # the Classifier above
governing_law.prompt("...")                   # the original function
```

Examples for the decorator are dicts or JSON lines holding the function's arguments by name plus `answer`, or
`(input, answer)` pairs. Both forms take `labels=`, `auto=`, `lam=`, `alpha_mult=`, `device=`, `label_prefix=` and
`max_len=`; giving `lam` or `alpha_mult` turns the automatic choice off.

To put the read-out into the model itself, so your existing `generate` or logits code gives its answer:

```python
model = clf.patch()                           # for good, in memory; returns the model
with clf.patched() as model:                  # or only inside the block; the rows are put back on exit
    ...
clf.export("qwen-governing-law/")             # or save a patched copy for plain transformers; memory unchanged
```

The cautions under "What to check, every time" apply here as well: one task per set of answer rows when patching,
and look at `clf.report` and `clf.sweep()` before relying on it.

## Use from the command line

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

Fit (prints the honest two-fold score, then saves a read-out fitted on everything). `--auto` is the recommended
way: it chooses the settings, says which, and saves nothing when the model is best left alone:

```
lmreadout fit --model Qwen/Qwen3.5-0.8B --data governing_law.jsonl --template governing_law.txt \
              --labels No Yes --out governing_law.npz --task governing_law --auto
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

The pieces behind `Classifier`, from Python:

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

Just before it answers, the model holds a list of numbers, its state, that sums up what it has read. To choose the
next word it scores every word in its vocabulary against that state, using one row of numbers per word, and the
highest score wins. This tool changes only the rows of your answer words (say "Yes" and "No"), in two steps:

1. **Remove the lean.** Small models often favour one answer whatever the question. We measure by how much on your
   examples and shift each answer's row so that, on average, no answer is favoured. This is the calibration step.
2. **Add what the model knows but does not say.** The state often tells Yes items from No items better than the
   model's actual answer does. For each answer we fit a simple linear classifier (a ridge regression) on your
   examples that separates that answer's items from the rest, and add it to that answer's row. From then on the
   model's ordinary scoring does the classifying.

How hard step 2 pushes is the "strength". At the default of 2, the read-out's vote counts about four times as much
as the model's own, so it wins most disagreements. With few examples that is often too much, which is why `--auto`
chooses the strength (and the other two settings) from your examples instead.

There is no training loop. Both steps are solved by a formula in one pass, which is why it takes seconds once the
model has read your examples. The exact arithmetic is in the comment at the top of `lmreadout/core.py`.

## What to check, every time

- **Held-out first.** `fit` prints a two-fold score where every item is scored by a read-out that never saw it; the
  in-sample number is not reported anywhere because it is meaningless (0.89 to 1.00 on all ten of the Handi tasks
  where it was measured).
- **Run `sweep` at the number of labels you have.** With few labels the fixed edit can score below calibration
  alone or the model as shipped (see the tables above); `fit`'s two-fold score uses half your items and can hide
  that. Use `--auto`, and `sweep --auto` to see what it would have chosen.
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
- Without `--auto` the read-out's strength is fixed (x2), not tuned to how reliable it is; with few labels that is
  often too much. `--auto` chooses it from the labelled items, which with 15 of them is itself noisy.
- `--auto`'s size rule was set from Qwen3.5 at 0.8B to 9B; other model families have not been tested with it.
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
no draws, predictions that would overwrite a field, fixed settings passed with auto, and reserved meta keys; and for
the `Classifier` and the decorator, on a tiny random model: its answers are the patched model's own, `patched()`
puts the rows (and a tied embedding) back exactly, an exported copy reloaded with plain `transformers` agrees,
save and load, and the decorator fits on first call, reuses its cache and refits when the examples change. No model
download.

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
