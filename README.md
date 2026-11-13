# lmreadout

Make a small language model better at a classification task, using a few labelled examples and no training.

You give it a model, a prompt and some examples with the right answers. It works out a small correction and writes
it into the model's output layer, changing only the rows for your answer words (say "Yes" and "No"). The model then
answers your task with its normal inference code: no wrapper, no prompt trick, no separate classifier. It works for
two answers or more.

It does not always help. With fixed settings it improves some tasks and hurts others. With `--auto` it picks the
settings from your examples, and may decide to leave the model alone; in our tests that never did more than slight
harm. Either way, measure it on your own task before you rely on it. The `sweep` command does that.

Neither half of the method is new. Correcting a model's bias towards one answer is known (Zhao et al. 2021; Zhou et
al. 2024), and so is fitting a linear classifier on a model's internal state (Alain & Bengio 2016; Buckmann & Hill
2024). What this package adds is writing both into the model's own output layer. See "Prior work" at the end.

## Install

```
pip install git+https://github.com/discover-legal/lmreadout
```

From a checkout, use `pip install .`, or `pip install -e ".[dev]"` to work on it. `python -m build` makes a wheel
in `dist/`. You get the `lmreadout` command and the `lmreadout` Python package.

It needs `torch`, `numpy` and `transformers` 5.2 or later (the first version with Qwen3.5). On a machine with no
GPU, install the CPU build of torch first, or pip may download the much larger GPU build:

```
pip install torch --index-url https://download.pytorch.org/whl/cpu
```

What to expect:

- This package has been run on real tasks with Qwen3.5 only. Other model families pass the unit tests but are untested on
  real tasks. If it cannot work with a model's architecture it says so and stops.
- An 8 GB GPU is enough for models around 1B parameters.
- On CPU, Qwen3.5-0.8B takes under a second per short item. `transformers` will warn about slower kernels; that is
  expected.

## Quick start in Python

Give it a model and labelled examples, and you get back something you can call. The settings are chosen from your
examples by default. Nothing is written into the model unless you ask.

```python
from lmreadout import Classifier

clf = Classifier.fit(
    "Qwen/Qwen3.5-0.8B",                       # a model id or path, or (model, tokenizer) you already loaded
    "governing_law.jsonl",                     # or a list of dicts, or (item, answer) pairs
    template="Does the clause say which law governs the contract?\n\nClause: {{text}}\nLabel:",
)
clf("This Agreement shall be governed by the laws of the State of Delaware.")     # "Yes"
clf.predict(["...", "..."])                   # a list of answers
clf.scores(["..."])                           # [{"No": 0.08, "Yes": 0.92}]
clf.report                                    # scores on examples it was not fitted on
clf.settings, clf.unchanged                   # what was chosen; True if the model was left alone
clf.sweep(sizes=(15, 30, 60))                 # how it does with fewer examples

clf.save("governing_law.npz")                 # saves the correction only; the command line can read it too
clf = Classifier.load("governing_law.npz")    # loads the model it was fitted on, or pass one
```

Or as a decorator. Your function writes the prompt, and the decorated function returns the answer:

```python
from lmreadout import classifier

@classifier("Qwen/Qwen3.5-0.8B", examples="governing_law.jsonl", cache="governing_law.npz")
def governing_law(text):
    return f"Does the clause say which law governs the contract?\n\nClause: {text}\nLabel:"

governing_law("Either party may terminate on thirty days' notice.")    # "No"
governing_law.scores("...")                   # {"No": 0.9, "Yes": 0.1}
governing_law.map(["...", "..."])             # many at once
governing_law.classifier                      # the Classifier object above
governing_law.prompt("...")                   # your original function
```

Notes on the decorator:

- It fits the first time you call it.
- With `cache=`, the fit is saved to that file and reused. It refits if the model, the prompts, the answers or the
  settings change.
- Several tasks on the same model id share one loaded copy of the model.
- Examples are dicts (or JSON lines) holding the function's arguments by name plus `answer`, or `(input, answer)`
  pairs.

Both forms accept `labels=`, `auto=`, `lam=`, `alpha_mult=`, `device=`, `label_prefix=` and `max_len=`. Setting
`lam` or `alpha_mult` yourself turns the automatic choice off.

To put the correction into the model itself, so your existing `generate` or logits code gives the corrected answer:

```python
model = clf.patch()                           # permanently, in memory; returns the model
with clf.patched() as model:                  # or only inside this block; undone afterwards
    ...
clf.export("qwen-governing-law/")             # or save a corrected copy of the model to disk
```

Read "What to check, every time" below before you rely on any of this.

## Quick start on the command line

Your examples go in a file with one JSON object per line. Each has the fields your prompt uses, plus an `answer`.
Other fields are ignored.

```
{"text": "This Agreement shall be governed by the laws of the State of Delaware.", "answer": "Yes"}
{"text": "Either party may terminate on thirty days' notice.", "answer": "No"}
```

Your prompt goes in a text file, with `{{field}}` where each field belongs. It must end exactly where the answer
goes. (A line break at the very end of the file is removed for you, with a note.)

```
Does the clause specify which state/country's law governs the contract?

Clause: {{text}}
Label:
```

**Fit.** This prints an honest score, then saves the correction. Use `--auto`: it chooses the settings, tells you
which, and saves nothing if the model is best left alone.

```
lmreadout fit --model Qwen/Qwen3.5-0.8B --data governing_law.jsonl --template governing_law.txt \
              --labels No Yes --out governing_law.npz --task governing_law --auto
```

**More than two answers.** Leave out `--labels` and every distinct `answer` in the data is used, or list them
yourself.

```
lmreadout fit --model Qwen/Qwen3.5-0.8B --data news.jsonl --template news.txt --out news.npz --task topic
```

Each answer is recognised by its first token, so answers of several words are fine as long as they start
differently. "Procedural History" and "Rule" work. "Unilateral change" and "Unilateral termination" do not, and
`fit` tells you. Digits work too, even though Qwen writes " 3" as a space followed by "3".

**Find out how many examples you need.** `sweep` fits on N examples picked at random, scores all the others, and
repeats. It prints the result beside three things to compare against: the model untouched, the bias correction
alone, and plain word counts fitted on the same N examples.

```
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data news.jsonl --template news.txt --sizes 15 30 60 120 --draws 20 \
                --csv news_sweep.csv
```

Word counts are the sanity check. They use the same formula but look only at which words appear in each item, not
at the model. If word counts do as well, the score comes from your examples and the model is adding nothing.

**Score on new items.**

```
lmreadout eval --model Qwen/Qwen3.5-0.8B --readout governing_law.npz --data heldout.jsonl
```

**Ship it,** one of two ways:

```
# a corrected copy of the model: only the answer rows of the output layer differ
lmreadout patch --model Qwen/Qwen3.5-0.8B --readout governing_law.npz --out qwen-governing-law/

# or keep the model as it is and apply the corrections on the side: several tasks at once, a few KB each
lmreadout predict --model Qwen/Qwen3.5-0.8B --readout governing_law.npz definitions.npz --data clauses.jsonl
```

### How the scores are reported

`fit` and `eval` print two kinds of score for the model untouched, the bias correction alone, and the full
correction:

- **Accuracy**, beside the share of the most common answer (what you would get by always giving that answer).
- **Balanced accuracy**, beside the guessing rate. Balanced accuracy is the share answered correctly within each
  answer, averaged over the answers. A model that always gives the same answer scores 1 / (number of answers), no
  matter how lopsided the data is.

`eval` also prints how often the model, left to write freely, says one of your answers at all. `sweep` prints
balanced accuracy with plain accuracy in brackets.

### Options

Every command takes:

- `--model`: a Hugging Face id or a local path.
- `--device cuda|cpu`: default is cuda when available.

Every command except `patch` takes:

- `--max-len`: prompts longer than this many tokens lose their start (default 1024). You get a warning saying how
  many were cut.
- `--max-items`: use only the first N items.

`fit` and `sweep` also take:

- `--labels`: the answers.
- `--label-prefix`: text put before each answer when it is turned into tokens (default: a space). `eval` and
  `predict` reuse the one saved by `fit`.
- `--auto`, or the fixed settings `--lam` and `--alpha-mult`.

`sweep` also takes `--sizes` (each at least 2), `--draws` (at least 1), `--seed` and `--csv`.

`lmreadout <command> --help` lists them all.

### Checking a corrected model with plain `transformers`

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
m = AutoModelForCausalLM.from_pretrained("qwen-governing-law/"); tok = AutoTokenizer.from_pretrained("qwen-governing-law/")
ids = [tok(" " + a, add_special_tokens=False)["input_ids"][0] for a in ["No", "Yes"]]
logits = m(**tok(prompt, return_tensors="pt", add_special_tokens=False)).logits[0, -1]
answer = ["No", "Yes"][int(logits[ids].argmax())]       # should match `eval` / `predict` item for item
```

### The lower-level Python functions

`Classifier` is built from these, and you can use them directly:

```python
from lmreadout import load_model, answer_tokens, collect, fit, fit_auto, twofold, patch, Readout
model, tok = load_model("Qwen/Qwen3.5-0.8B")
ids, suffix = answer_tokens(tok, ["No", "Yes"])         # suffix: text to add to the prompt (usually "")
H, LAB, LSE = collect(model, tok, prompts, ids)          # the model's state and answer scores for each prompt
size = model.num_parameters()                           # used by auto to break ties
print(twofold(H, LAB, LSE, gold, auto=True, n_params=size))   # scores on examples it was not fitted on
r, choice = fit_auto(H, LAB, LSE, gold, n_params=size, labels=["No", "Yes"], label_ids=ids, template=template)
if r is not None:                                        # None means: leave the model as it is
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
   model's ordinary scoring does the classifying. We call this part the read-out.

How hard step 2 pushes is the "strength". At the default of 2, the read-out's vote counts about four times as much
as the model's own, so it wins most disagreements. With few examples that is often too much, which is why `--auto`
chooses the strength (and the other two settings) from your examples instead.

There is no training loop. Both steps are solved by a formula in one pass, which is why it takes seconds once the
model has read your examples. The exact arithmetic is in the comment at the top of `lmreadout/core.py`.

## Letting it choose its settings (`--auto`)

Three settings decide how the correction behaves:

- **Lean:** how much of the model's bias to remove. None, half or all.
- **Strength:** how hard the read-out overrides the model's own answer. 0, 0.5, 1, 2 or 4. The fixed default is 2.
- **Ridge:** how much the read-out is smoothed. n/4, n or 4n, where n is the number of examples.

`fit --auto` tries every combination. It scores each one on your examples by cross-validation: hold some examples
back, fit on the rest, score the ones held back, and repeat. (Up to 50 examples it holds back one at a time; above
that, a tenth at a time.) It keeps the combination with the best balanced accuracy.

Three rules sit on top:

- **It leaves the model alone unless a correction scores strictly higher,** and tells you when it does.
- **Ties go to a gentler strength on bigger models:** 2 below 3B parameters, 1 below 7B, 0.5 from 7B up. A bigger
  model's own answer deserves more trust.
- **If some answer has fewer than two examples,** nothing can be cross-validated. It then removes the lean only,
  which needs no labels, and tells you which answers need more examples.

`sweep --auto` adds an "auto" column, with the settings chosen afresh from each random set of N examples.

Why we added it: in the Handi runs the fixed strength was too strong for bigger models. With 15 examples, the fixed
correction made Qwen3.5-9B worse than the untouched model on LegalBench's two-answer tasks. At half strength it
would have helped.

## Does it work? Results

All scores below are balanced accuracy unless stated. The columns mean:

- **As shipped:** the model untouched.
- **Calibration only:** step 1 alone, the bias removed.
- **Word counts:** the sanity check that ignores the model.
- **Edited** or **fixed edit:** both steps at the fixed default settings.
- **`--auto`:** both steps with the settings chosen from the examples.

### Six tasks, fixed settings

Qwen3.5-0.8B, installed from this repository into a clean environment and run through `lmreadout sweep`. For 15
and for 120 examples we made 20 random draws, scored every remaining item, and took the mean. Each task had up to
1,000 items. The tweet task was chosen and run by a separate agent that had only this README, and it wrote its
plan down before seeing any score.

| Task | Answers | Guessing | As shipped | Calibration only, 15 / 120 | Word counts, 15 / 120 | Edited, 15 / 120 |
|---|---|---|---|---|---|---|
| News topic (AG News) | 4 | 0.25 | 0.27 | 0.59 / 0.61 | 0.31 / 0.59 | **0.67 / 0.81** |
| Overruling (LegalBench) | 2 | 0.50 | 0.69 | 0.83 / 0.85 | 0.69 / 0.87 | **0.89 / 0.94** |
| Function of a decision section (LegalBench) | 7 | 0.14 | 0.19 | 0.28 / 0.28 | 0.19 / 0.36 | 0.27 / **0.40** |
| Emotion in a message (dair-ai/emotion) | 6 | 0.17 | 0.21 | **0.49 / 0.50** | 0.17 / 0.20 | 0.35 / 0.47 |
| Tweet sentiment (tweet_eval) | 3 | 0.33 | 0.44 | **0.44** / 0.46 | 0.34 / 0.36 | 0.40 / **0.48** |
| Yes/no question on a passage (BoolQ) | 2 | 0.50 | **0.65** | 0.65 / 0.65 | 0.51 / 0.51 | 0.57 / 0.61 |

What this shows:

- **It is strong when the answer is a kind of text:** a topic, or whether a sentence overrules a case. On news
  topics, the correction with 15 examples beats word counts with 120.
- **With 15 examples it can make things worse.** It falls below calibration alone on emotion and tweets (on the
  seven-way legal task the two are level). It falls below the untouched model on tweets and BoolQ.
- **More examples help.** On tweets it passes the untouched model from 60 examples (0.45, then 0.48 at 120).
  Fitted on 300 tweets and scored on 400 others: 0.51 as shipped, 0.53 edited.
- **Only `sweep` shows the harm reliably.** On BoolQ, the score `fit` prints (fitted on 250, scored on the other
  250) is level with the untouched model: 0.643 shipped, 0.646 edited. So is `eval` on 500 new items: 0.652 and
  0.661. The drop only appears with 15 to 120 examples. `fit` warns when its own score falls below the untouched
  model.

Why it hurts, as far as we can tell. This is our reading of these runs, not a tested explanation:

- **The strength is fixed, however good the read-out is.** With few examples, on a task the model's state carries
  weakly, the read-out is mostly noise, and it is added on top of the model's own answer at full strength. It
  improves steadily with more examples on every task. Choosing the strength per task (`--auto`) removes most of
  the harm, which supports this reading without proving it.
- **With uneven answers it learns the common ones.** Plain accuracy rises while balanced accuracy falls. On emotion
  with 15 examples: accuracy 0.48 edited against 0.47 calibrated, but balanced accuracy 0.35 against 0.49.
- **BoolQ needs the question and the passage together.** Word counts stay at guessing (0.51), and 120 examples are
  not enough for the read-out to beat the model's own answer.

Two cross-checks. The overruling numbers match the Handi run on the same task within 0.03. On AG News, fitted on
1,000 training stories and scored on 1,000 test stories, the correction scores 0.88; the corrected copy saved by
`lmreadout patch` and reloaded with plain `transformers` gives the same 0.876.

### The same tasks with `--auto`

Tested the same way: a separate agent, installing from GitHub, 20 draws per size. We added a task never used
before, Rotten Tomatoes movie reviews, with the plan written down before any score. We also ran Qwen3.5-4B on two
tasks. Scores are for 15 / 120 examples.

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

What this shows:

- **It does no real harm.** With 15 examples it is never more than 0.02 below the untouched model. The worst case
  is BoolQ: 0.632 against 0.648, where the fixed edit lost 0.075. Across every number of examples we tried, the
  worst is BoolQ at 60: 0.623 against 0.647.
- **On average it matches the better of two safe choices.** With 15 examples it is level (+0.01) with whichever is
  better of the untouched model and calibration alone. You would not know in advance which of those to pick.
- **With 120 examples it matches or beats the fixed edit on every task.** The worst is overruling, 0.001 below.
- **It is not always the best choice.** With 15 examples cross-validation is noisy, so on some tasks it lands a
  little below calibration alone: Rotten Tomatoes 0.85 against 0.86; tweets on the 4B 0.62 against 0.63, and 0.61
  against 0.63 at 60 examples.
- **It aims at balanced accuracy, not plain accuracy.** With uneven answers (tweets, emotion) plain accuracy can
  fall while balanced accuracy rises.

On LegalBench with 15 examples, `--auto` gives 0.80 / 0.84 / 0.86 for Qwen3.5-2B / 4B / 9B. The fixed edit gives
0.81 / 0.82 / 0.83, and the untouched models 0.72 / 0.81 / 0.84. These are the 98 two-answer tasks from the Handi
runs, which the method was developed on, so this is not a clean test.

### Where it came from: LegalBench

The method was developed in the Handi experiment (https://github.com/discover-legal/Handi), on LegalBench.

- **Ten tasks, Qwen3.5-0.8B, a few hundred examples each.** Mean accuracy went from 0.57 as shipped to 0.78 after
  the correction. On examples it never saw: overruling 0.94, definition classification 0.98, governing-law clauses
  1.00.
- **But word counts do nearly as well there.** On those three tasks word counts score 0.91, 0.86 and 0.997.
  Governing law is solved by the words alone, so a perfect score there says nothing about what the model knows.
  Even a model with random weights gets most of the way with a few hundred examples. At that size the formula is
  doing most of the work, not the model.
- **The model pays off when examples are few.** On the 132 two-answer LegalBench tasks, with 15 examples each, the
  correction lifts Qwen from 0.56 to 0.73 (guessing is 0.50). Word counts reach 0.65, and the correction beats them
  on 105 of the tasks. Calibration alone already gives 0.66; the read-out adds the rest. On Phi-4-mini it goes
  from 0.68 to 0.76 (calibration alone 0.71). It does best on contract clauses and worst on long merger
  agreements.
- **Bigger models gain less.** With 15 examples the correction adds 0.19 to Qwen3.5-0.8B, 0.09 to the 2B and 0.01
  to the 4B, which already answers well as shipped. (Mean over the 98 two-answer tasks all three finished.)
- **More than two answers.** On 21 LegalBench tasks with three to eight answers, it beats word counts on the six
  tasks that are not about merger agreements, at every number of examples tried. On the 15 merger-agreement (MAUD)
  tasks it is no better than word counts.

### Does the model still say one of the answers?

The correction decides between your answer words. Whether the model, left to write freely, says one of them at all
is a separate question. `eval` reports it. The table shows how often the model's free next word is one of the
answers:

| Task | As shipped | Edited, 0.3.0 | Edited, 0.3.1 |
|---|---|---|---|
| Overruling (worked examples in the prompt) | 100% | 100% | 100% |
| AG News, four worked examples in the prompt | 100% | 99.8% | 100% |
| AG News, no examples | 56.5% | 66.5% | 91.9% |
| BoolQ, no examples | 19.0% | 58.6% | 58.6% |
| Tweet sentiment, no examples | 48.0% | | 58.2% |
| Emotion, no examples | 92.6% | 35.6% | 92.8% |
| Function of a decision section (worked examples) | 100% | 59.2% | 100% |

Two things decide it:

- **Worked examples in the prompt.** They keep the model answering in the expected words. LegalBench's prompts all
  have them, which is why the Handi runs never had this problem.
- **A bug fixed in 0.3.1.** Up to 0.3.0, with more than two answers, the correction lowered all the answer rows
  together by a constant. That let other words overtake every answer. Since 0.3.1 that constant is removed. It
  changes no difference between answers, so every chosen answer and every score above is the same as before.
  Two-answer corrections were never affected. Files saved by 0.2 or 0.3.0 are fixed when loaded.

Without worked examples the model can still wander, as on BoolQ. So either compare the scores of the answer words
only, which is what `eval`, `predict` and `Classifier` do, or restrict generation to the answers.

## What to check, every time

- **Trust only scores on examples the fit never saw.** `fit` prints one: it fits on half your examples, scores the
  other half, then swaps. The score on the examples it was fitted on is not reported anywhere, because it means
  nothing (0.89 to 1.00 on all ten Handi tasks where we measured it).
- **Run `sweep` at the number of examples you actually have.** With few examples the fixed correction can score
  below calibration alone, or below the untouched model. `fit`'s own score uses half your examples and can hide
  that. Use `--auto`, and `sweep --auto` to see what it would have chosen.
- **If the held-out score is no better than always giving the most common answer, stop.** The model does not hold
  the answer in a form this method can read. `fit` warns. No change to the output rows can create what is not
  there.
- **Compare against word counts.** `sweep` does this for you. If word counts do as well, the score comes from your
  examples, not from the model.
- **One task per set of answer words when you patch.** The Yes and No rows are used by every Yes/No prompt. So a
  patched model answers other Yes/No tasks differently (2% to 97% of answers changed in our test), and two tasks
  patched into the same rows mostly cancel out. For several tasks, use `predict` or `Classifier`, which leave the
  model alone, or give each task its own answer words.
- **Check the patch.** After `patch`, score your held-out items with your ordinary pipeline. It should match `eval`
  to a few decimals.

## Limits

- **Answers are told apart by their first token.** Answers that start the same, like "Unilateral change" and
  "Unilateral termination", cannot be used together.
- **Fixed answer sets only.** Not free text copied from the item, and not several answers at once.
- **The model may still prefer some other word** when the prompt has no worked examples. See "Does the model still
  say one of the answers?".
- **Some tasks get worse.** Tasks that need the item and the question combined, like BoolQ. Tasks where the model
  is already decent and examples are few, like tweets. Check with `sweep`.
- **Without `--auto` the strength is fixed at 2,** whatever the quality of the read-out. With few examples that is
  often too much. `--auto` chooses it from your examples, which with 15 of them is itself noisy.
- **`--auto`'s rule for model size was set on Qwen3.5 from 0.8B to 9B.** Other model families are untested.
- **Prompts get no beginning-of-sequence token.** Qwen uses none. Models that expect one, like Llama 3 and Gemma,
  may score lower than they should.
- **It reads the model's last layer only.** Classifiers fitted a few layers earlier are usually a little better
  (0.84 against 0.78 mean in our runs), but using them means editing inside the network, which this tool does not
  do.
- **A patched copy is large.** It is saved in float32 with its output layer stored separately: about 4 GB for the
  0.8B model.
- **It adds no knowledge.** It can only bring out what the model's state already carries. Takehi et al. found the
  same of weight edits in general: they can uncover an ability but not add one.

## Tests

```
pip install -e ".[dev]" && python -m pytest
```

The tests download no model. They use made-up data, a toy tokenizer and tiny models with random weights. They
cover:

- **Reading the answers:** by first token; digits after a space; answers that start the same are refused.
- **The method:** a signal planted in made-up data is recovered, for two and for four answers. The patched rows
  give exactly the scores computed without patching. Two-answer results are identical to version 0.1.
- **The 0.3.1 fix:** the constant is removed without changing any answer.
- **Files:** save and load, including files from version 0.1.
- **Patching:** only the answer rows change, on float32 and bfloat16 models.
- **`--auto`:** the combinations tried, the tie order and the size rule; it uses a planted signal; it leaves alone
  a model that is already right; it falls back when an answer is short of examples.
- **`sweep`** and the word-count check.
- **Refusals and warnings:** prompts that get cut; a fit with only one answer; sweep sizes under two or no draws;
  predictions that would overwrite a field; fixed settings given together with auto.
- **`Classifier` and the decorator:** its answers are the patched model's own; `patched()` puts everything back
  exactly; an exported copy reloaded with plain `transformers` agrees; save and load; the decorator fits on first
  call, reuses its cache, and refits when the examples change.

## Prior work

- Takehi, Teoh, Zhang, Khattab, "Sparks of Weight-Space Programming: LLMs can natively read & write neural network
  weights", MIT CSAIL blog post, 2 Nov 2026, https://rikiyat.github.io/blog/weight-space-programming/. GPT-6 Astra
  edits Qwen3.5-0.8B's weights without gradients, and concludes from its Gemma 3 270M edits: "Editing weights could
  remove an obstacle that hid an ability, but it could not add an ability the model lacked." The Handi experiment
  this came from was prompted by it.
- Zhao, Wallace, Feng, Klein, Singh, "Calibrate Before Use: Improving Few-Shot Performance of Language Models",
  ICML 2021, https://arxiv.org/abs/2102.09690. On bias towards particular answer words.
- Zhou, Wan, Proleev, Mincu, Chen, Heller, Roy, "Batch Calibration: Rethinking Calibration for In-Context Learning
  and Prompt Engineering", ICLR 2024, https://arxiv.org/abs/2309.17249. Estimates the bias from the mean over
  items; the closest to the calibration step here.
- Alain, Bengio, "Understanding intermediate layers using linear classifier probes", 2016,
  https://arxiv.org/abs/1610.01644.
- Buckmann, Hill, "Logistic Regression makes small LLMs strong and explainable 'tens-of-shot' classifiers", 2024,
  https://arxiv.org/abs/2408.03414. A linear classifier on a small model's states with tens of examples.
- Cho et al., "Prompt-Augmented Linear Probing: Scaling beyond the Limit of Few-shot In-Context Learners", AAAI 2023,
  https://arxiv.org/abs/2212.10873; Abbas et al., "Enhancing In-context Learning via Linear Probe Calibration",
  AISTATS 2024, https://arxiv.org/abs/2401.12406.
- Orgad et al., "LLMs Know More Than They Show: On the Intrinsic Representation of LLM Hallucinations", ICLR 2025,
  https://arxiv.org/abs/2410.02707; Burns, Ye, Klein, Steinhardt, "Discovering Latent Knowledge in Language Models
  Without Supervision", ICLR 2023, https://arxiv.org/abs/2212.03827. Both show a model's internal state carries
  more than its output says.
- Li, Patel, Viégas, Pfister, Wattenberg, "Inference-Time Intervention: Eliciting Truthful Answers from a Language
  Model", NeurIPS 2023, https://arxiv.org/abs/2306.03341. Steers a model's internal state at inference time.
- Guha et al., "LegalBench: A Collaboratively Built Benchmark for Measuring Legal Reasoning in Large Language
  Models", NeurIPS 2023 Datasets and Benchmarks, https://arxiv.org/abs/2308.11462. Other data: AG News (Zhang, Zhao,
  LeCun 2015), dair-ai/emotion, tweet_eval (Barbieri et al. 2020), BoolQ (Clark et al. 2019).

## Licence

MIT. See `LICENSE`.
