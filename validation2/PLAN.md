# Second held-out test of lmreadout (0.6.0 beside 0.5.0): the plan

## Purpose

This is a test of the changed `lmreadout --auto` (version 0.6.0) on twelve classification tasks the package has
not been run on, side by side with version 0.5.0 on the same tasks, with the tasks, the prompts and the pass/fail
rules written down here before any model is run. Nobody has computed a score of any kind for these tasks yet (not
even the untouched model's), so nothing below could have been chosen to make the result look good or bad.

## The 12 tasks

Every task is a public Hugging Face dataset, pinned to one exact version (the "revision"). "Items" is how many
examples are in the test file; the answers keep the proportions they have in the dataset. None of the twelve
datasets of the first held-out test (`validation/PLAN.md`) is used again, and no task name is reused.

| Task | Dataset, config, split, revision | Legal? | Answers | Answer words, exactly as in the data | Items | Why it was picked |
|---|---|---|---|---|---|---|
| `unfair_clause` | `laugustyniak/abusive-clauses-pl`, default, test, `ea52f5ce905e44ad88b20bacb180f635400948a0` (the parquet copy under the same repo's `refs/convert/parquet`) | legal | 2 | Abusive, Safe | 1,000 of 3,453 | Is a clause from a Polish consumer contract unfair to the consumer; the only task with Polish text (English prompt). |
| `housing_law` | `reglab/housing_qa`, `questions`, test, `761550cc974fa1d9141ffd39014db89efa2a7230` (data file read directly, see Gaps 2) | legal | 2 | Yes, No | 1,000 of 6,853 | Knowledge of the law: a yes/no question about the housing law of one US state, with no passage to read. |
| `contract_type` | `lexlms/legal_lama`, `contract_types`, test, `e62bb3d77ac4797e86ad9779ced416a33db0fe96` (data file read directly, see Gaps 2) | legal | 15 | Award, Consulting, Credit, Employment, Indemnity, Letter, License, Loan, Purchase, Security, Separation, Services, Settlement, Supply, Voting | 1,000 of 1,062 | Fill in a hidden word: which kind of agreement the opening paragraph of a contract belongs to. |
| `language_id` | `papluca/language-identification`, default, test, `aa56583bf2bc52b0565770607d6fc3faebecf9e2` | no | 20 | Arabic, Bulgarian, Chinese, Dutch, English, French, German, Greek, Hindi, Italian, Japanese, Polish, Portuguese, Russian, Spanish, Swahili, Thai, Turkish, Urdu, Vietnamese | 1,000 of 10,000 | Which language a text is written in; the texts are in 20 languages. |
| `patent_section` | `ccdv/patent-classification`, `abstract`, test, `17bd94cd6594bac1b82a697e811fb7cf34a7af35` | no | 9 | Human necessities, Performing operations, Chemistry, Textiles, Fixed constructions, Mechanical engineering, Physics, Electricity, General tagging | 1,000 of 5,000 | Technical field of a patent abstract, by the top-level sections patent offices use. |
| `abstract_role` | `armanc/pubmed-rct20k`, default, test, `091aec1e2384a20b2b36eb96177755ca13dd0b42` | no | 5 | Background, Objective, Methods, Results, Conclusions | 1,000 of 29,578 | Which part of the abstract of a medical research paper a sentence comes from. |
| `fed_stance` | `gtfintechlab/fomc_communication`, default, test, `6b0283f55f0005a6d38d49f271d795c21fccc1a3` | no | 3 | Dovish, Hawkish, Neutral | 496 of 496 | Finance: does a sentence from the US central bank lean towards easier or tighter monetary policy. |
| `climate_claim` | `tdiggelm/climate_fever`, default, test, `ae61ccb9320a78109a246414139ff3a2bd677b8b` | no | 4 | Supported, Refuted, Not enough information, Disputed | 1,000 of 1,535 | Fact-checking: does the evidence support a claim about the climate (only the claim is shown). |
| `hate_speech` | `Paul/hatecheck`, default, test, `9d2ac89df04254e5c427bcc8d61b6d6c83a1f59b` | no | 2 | Hateful, Non-hateful | 1,000 of 3,728 | Hate speech: short sentences written to catch out detectors (the data contains offensive text by design). |
| `counterfactual` | `mteb/amazon_counterfactual`, `en-ext`, test, `b9867e02b01002698f60c07fb8efdce8c5020ee8` | no | 2 | Yes, No | 666 of 666 | Does a sentence from a product review describe something that did not happen; one answer is rare (1 in 10). |
| `appeal_outcome` | `Persius/imr-appeals`, default, test, `c68b70e0faf74cd2b5731ea02ad7ba7d99a11b8b` | no | 2 | Upheld, Overturned | 1,000 of 9,920 | Predicting an outcome: was a health insurer's refusal to pay upheld or overturned on independent review. |
| `fair_reason` | `hendrycks/ethics`, `justice`, test, `6deab74c03e30f13540266e373ce31f8466169f8` (the parquet copy under the same repo's `refs/convert/parquet`) | no | 2 | Yes, No | 1,000 of 2,052 | Moral judgement: is the reason someone gives for how they treat another person a fair one. |

The mix: 3 legal and 9 not legal (the design asked for at least 4 legal; see Gaps 1); 6 tasks with two answers
and 6 with three or more, of which 3 have eight or more (`contract_type` 15, `language_id` 20, `patent_section` 9).

Kinds of task: nine of the twelve are kinds the first test did not have (unfair clause, legal yes/no question,
hidden word, language, fact-checking, hate speech, counterfactual, outcome of an appeal, moral judgement). Three
are kinds it did have, on different data: `patent_section` (topic of a text), `abstract_role` (the part a sentence
plays in a document) and `fed_stance` (stance). The design allows at most four.

How the items were drawn (the same for every task, done by `validation2/prepare.py`): where the split has more
than 1,000 items, 1,000 were picked at random with seed 0; where it has fewer, all were used. Nothing was dropped,
shortened or rebalanced. Running `prepare.py` again gives exactly the same files (checked).

Each task has one prompt, in `validation2/templates/<task>.txt`, written once and not to be changed.

## The 4 tasks also run on Phi-4-mini

`housing_law` (legal, 2 answers), `contract_type` (legal, 15 answers), `hate_speech` (not legal, 2 answers) and
`climate_claim` (not legal, 4 answers).

That is one task of each combination (legal or not, two answers or more), and within each combination the task
with the shortest prompts on average, because this model runs on the CPU. The averages are in the check output
below; the choice is the same whichever of the two tokenizers is used to count. `contract_type` is the only legal
task with more than two answers, so it had no competitor.

## The run commands

Run from the repository root, unchanged. Every command is run twice: once with lmreadout 0.6.0 installed and
once with lmreadout 0.5.0 installed. The two differ only in the name of the results file. No command uses
`--labels`: the README says that without it every distinct answer in the data is used, and it does not say
`--labels` is needed for any kind of task. The seed is the default.

### With 0.6.0 installed

Primary: the 12 tasks on Qwen3.5-0.8B.

```
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/unfair_clause.jsonl --template validation2/templates/unfair_clause.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/unfair_clause.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/housing_law.jsonl --template validation2/templates/housing_law.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/housing_law.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/contract_type.jsonl --template validation2/templates/contract_type.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/contract_type.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/language_id.jsonl --template validation2/templates/language_id.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/language_id.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/patent_section.jsonl --template validation2/templates/patent_section.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/patent_section.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/abstract_role.jsonl --template validation2/templates/abstract_role.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/abstract_role.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/fed_stance.jsonl --template validation2/templates/fed_stance.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/fed_stance.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/climate_claim.jsonl --template validation2/templates/climate_claim.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/climate_claim.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/hate_speech.jsonl --template validation2/templates/hate_speech.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/hate_speech.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/counterfactual.jsonl --template validation2/templates/counterfactual.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/counterfactual.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/appeal_outcome.jsonl --template validation2/templates/appeal_outcome.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/appeal_outcome.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/fair_reason.jsonl --template validation2/templates/fair_reason.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/fair_reason.qwen08.csv
```

Secondary: the 4 tasks on Phi-4-mini.

```
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation2/data/housing_law.jsonl --template validation2/templates/housing_law.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/housing_law.phi4mini.csv --device cpu
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation2/data/contract_type.jsonl --template validation2/templates/contract_type.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/contract_type.phi4mini.csv --device cpu
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation2/data/hate_speech.jsonl --template validation2/templates/hate_speech.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/hate_speech.phi4mini.csv --device cpu
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation2/data/climate_claim.jsonl --template validation2/templates/climate_claim.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/climate_claim.phi4mini.csv --device cpu
```

### With 0.5.0 installed

Primary: the 12 tasks on Qwen3.5-0.8B.

```
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/unfair_clause.jsonl --template validation2/templates/unfair_clause.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/unfair_clause.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/housing_law.jsonl --template validation2/templates/housing_law.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/housing_law.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/contract_type.jsonl --template validation2/templates/contract_type.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/contract_type.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/language_id.jsonl --template validation2/templates/language_id.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/language_id.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/patent_section.jsonl --template validation2/templates/patent_section.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/patent_section.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/abstract_role.jsonl --template validation2/templates/abstract_role.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/abstract_role.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/fed_stance.jsonl --template validation2/templates/fed_stance.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/fed_stance.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/climate_claim.jsonl --template validation2/templates/climate_claim.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/climate_claim.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/hate_speech.jsonl --template validation2/templates/hate_speech.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/hate_speech.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/counterfactual.jsonl --template validation2/templates/counterfactual.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/counterfactual.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/appeal_outcome.jsonl --template validation2/templates/appeal_outcome.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/appeal_outcome.qwen08.v050.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation2/data/fair_reason.jsonl --template validation2/templates/fair_reason.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/fair_reason.qwen08.v050.csv
```

Secondary: the 4 tasks on Phi-4-mini.

```
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation2/data/housing_law.jsonl --template validation2/templates/housing_law.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/housing_law.phi4mini.v050.csv --device cpu
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation2/data/contract_type.jsonl --template validation2/templates/contract_type.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/contract_type.phi4mini.v050.csv --device cpu
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation2/data/hate_speech.jsonl --template validation2/templates/hate_speech.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/hate_speech.phi4mini.v050.csv --device cpu
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation2/data/climate_claim.jsonl --template validation2/templates/climate_claim.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation2/results/climate_claim.phi4mini.v050.csv --device cpu
```

## Rules fixed before any score

All scores are balanced accuracy, the mean over the 20 draws, as `sweep` reports them. "`--auto`" without a version means lmreadout 0.6.0's. Primary: the 12 tasks on Qwen3.5-0.8B. Secondary, judged by the same rules and reported separately: the 4 tasks on Phi-4-mini.

- **Rule 1 (no real harm at 15):** on every task, `--auto` with 15 examples is at most 0.02 below the model as shipped. Fails if any task is more than 0.02 below.
- **Rule 2 (matches the fixed edit at 120):** on every task, `--auto` with 120 examples is at most 0.005 below the fixed edit with 120 examples. Fails if any task is more than 0.005 below.
- **Rule 3 (level with the better safe choice at 15):** per task take the better of "as shipped" and "calibration only" at 15 examples; the mean over tasks of (`--auto` minus that) is at least -0.01. Fails if it is below -0.01.
- **Rule 4 (not worse than 0.5.0):** at each of 15, 30, 60 and 120 examples, the mean over tasks of (0.6.0's `--auto` minus 0.5.0's `--auto`) is at least 0. Fails if it is below 0 at any of the four sizes.
- **Reported whatever the outcome, for every task, model and size (15/30/60/120):** as shipped, calibration only, word counts, fixed edit, 0.6.0's `--auto`, 0.5.0's `--auto`, with the spread over draws; guessing rate; the settings each `--auto` chose; counts of tasks where 0.6.0's `--auto` is above/below each other column; and Rules 1 to 3 applied to 0.5.0's `--auto` as well, for comparison. No task, size or model may be dropped after scores are seen; a run that crashes or is refused by the package is reported as such, not replaced.

## Check of the prompts and answers

Output of `validation2/check_prompts.py`. It loads the two tokenizers only (no model). For each task it shows the
number of items, how often each answer occurs, the longest and the average filled prompt in tokens (the limit is
1,024), and the first token of each answer, which is what the package reads; these must all differ within a task.

```
== abstract_role: 1000 items, 5 answers
   answer counts: Background 102, Conclusions 162, Methods 326, Objective 58, Results 352
   Qwen/Qwen3.5-0.8B: longest prompt 177 tokens (mean 64.3); first tokens all different: Background = 24016 ' Background', Conclusions = 1160 ' Con', Methods = 18233 ' Methods', Objective = 52465 ' Objective', Results = 17560 ' Results'
   microsoft/Phi-4-mini-instruct: longest prompt 173 tokens (mean 60.9); first tokens all different: Background = 39236 ' Background', Conclusions = 158120 ' Conclusions', Methods = 33276 ' Methods', Objective = 95517 ' Objective', Results = 26676 ' Results'
== appeal_outcome: 1000 items, 2 answers
   answer counts: Overturned 486, Upheld 514
   Qwen/Qwen3.5-0.8B: longest prompt 524 tokens (mean 178.2); first tokens all different: Overturned = 5875 ' Over', Upheld = 95484 ' Uph'
   microsoft/Phi-4-mini-instruct: longest prompt 497 tokens (mean 170.7); first tokens all different: Overturned = 7931 ' Over', Upheld = 4686 ' Up'
== climate_claim: 1000 items, 4 answers
   answer counts: Disputed 93, Not enough information 305, Refuted 163, Supported 439
   Qwen/Qwen3.5-0.8B: longest prompt 118 tokens (mean 62.8); first tokens all different: Disputed = 3957 ' Dis', Not enough information = 2717 ' Not', Refuted = 8288 ' Ref', Supported = 47338 ' Supported'
   microsoft/Phi-4-mini-instruct: longest prompt 114 tokens (mean 60.2); first tokens all different: Disputed = 3946 ' Dis', Not enough information = 4037 ' Not', Refuted = 14132 ' Ref', Supported = 96841 ' Supported'
== contract_type: 1000 items, 15 answers
   answer counts: Award 21, Consulting 57, Credit 177, Employment 351, Indemnity 27, Letter 84, License 31, Loan 39, Purchase 22, Security 35, Separation 54, Services 20, Settlement 39, Supply 20, Voting 23
   Qwen/Qwen3.5-0.8B: longest prompt 452 tokens (mean 204.3); first tokens all different: Award = 16808 ' Award', Consulting = 44865 ' Consulting', Credit = 15788 ' Credit', Employment = 39503 ' Employment', Indemnity = 2190 ' Ind', Letter = 25807 ' Letter', License = 1811 ' License', Loan = 33920 ' Loan', Purchase = 29971 ' Purchase', Security = 7977 ' Security', Separation = 32001 ' Separ', Services = 8049 ' Services', Settlement = 66711 ' Settlement', Supply = 28835 ' Supply', Voting = 61000 ' Voting'
   microsoft/Phi-4-mini-instruct: longest prompt 420 tokens (mean 193.2); first tokens all different: Award = 18779 ' Award', Consulting = 58679 ' Consulting', Credit = 20807 ' Credit', Employment = 60588 ' Employment', Indemnity = 2761 ' Ind', Letter = 36718 ' Letter', License = 3312 ' License', Loan = 41690 ' Loan', Purchase = 37646 ' Purchase', Security = 13516 ' Security', Separation = 172201 ' Separation', Services = 9705 ' Services', Settlement = 127690 ' Settlement', Supply = 43268 ' Supply', Voting = 130843 ' Voting'
== counterfactual: 666 items, 2 answers
   answer counts: No 599, Yes 67
   Qwen/Qwen3.5-0.8B: longest prompt 128 tokens (mean 56.4); first tokens all different: No = 2233 ' No', Yes = 7179 ' Yes'
   microsoft/Phi-4-mini-instruct: longest prompt 112 tokens (mean 53.8); first tokens all different: No = 3004 ' No', Yes = 11377 ' Yes'
== fair_reason: 1000 items, 2 answers
   answer counts: No 494, Yes 506
   Qwen/Qwen3.5-0.8B: longest prompt 84 tokens (mean 44.7); first tokens all different: No = 2233 ' No', Yes = 7179 ' Yes'
   microsoft/Phi-4-mini-instruct: longest prompt 80 tokens (mean 42.2); first tokens all different: No = 3004 ' No', Yes = 11377 ' Yes'
== fed_stance: 496 items, 3 answers
   answer counts: Dovish 135, Hawkish 114, Neutral 247
   Qwen/Qwen3.5-0.8B: longest prompt 296 tokens (mean 79.3); first tokens all different: Dovish = 203072 ' Dov', Hawkish = 53466 ' Hawk', Neutral = 56710 ' Neutral'
   microsoft/Phi-4-mini-instruct: longest prompt 287 tokens (mean 79.8); first tokens all different: Dovish = 415 ' D', Hawkish = 103029 ' Hawk', Neutral = 109756 ' Neutral'
== hate_speech: 1000 items, 2 answers
   answer counts: Hateful 696, Non-hateful 304
   Qwen/Qwen3.5-0.8B: longest prompt 47 tokens (mean 35.1); first tokens all different: Hateful = 462 ' H', Non-hateful = 11248 ' Non'
   microsoft/Phi-4-mini-instruct: longest prompt 45 tokens (mean 33.8); first tokens all different: Hateful = 487 ' H', Non-hateful = 13763 ' Non'
== housing_law: 1000 items, 2 answers
   answer counts: No 647, Yes 353
   Qwen/Qwen3.5-0.8B: longest prompt 124 tokens (mean 54.3); first tokens all different: No = 2233 ' No', Yes = 7179 ' Yes'
   microsoft/Phi-4-mini-instruct: longest prompt 124 tokens (mean 52.4); first tokens all different: No = 3004 ' No', Yes = 11377 ' Yes'
== language_id: 1000 items, 20 answers
   answer counts: Arabic 45, Bulgarian 40, Chinese 52, Dutch 44, English 57, French 47, German 46, Greek 44, Hindi 46, Italian 61, Japanese 57, Polish 49, Portuguese 46, Russian 45, Spanish 56, Swahili 54, Thai 57, Turkish 48, Urdu 59, Vietnamese 47
   Qwen/Qwen3.5-0.8B: longest prompt 275 tokens (mean 89.8); first tokens all different: Arabic = 32988 ' Arabic', Bulgarian = 85573 ' Bulgarian', Chinese = 8193 ' Chinese', Dutch = 22510 ' Dutch', English = 6163 ' English', French = 8323 ' French', German = 5753 ' German', Greek = 17326 ' Greek', Hindi = 42524 ' Hindi', Italian = 14382 ' Italian', Japanese = 10452 ' Japanese', Polish = 30931 ' Polish', Portuguese = 40790 ' Portuguese', Russian = 8260 ' Russian', Spanish = 14712 ' Spanish', Swahili = 4344 ' Sw', Thai = 25548 ' Thai', Turkish = 22992 ' Turkish', Urdu = 90120 ' Urdu', Vietnamese = 46862 ' Vietnamese'
   microsoft/Phi-4-mini-instruct: longest prompt 271 tokens (mean 89.0); first tokens all different: Arabic = 57978 ' Arabic', Bulgarian = 161056 ' Bulgarian', Chinese = 13999 ' Chinese', Dutch = 36714 ' Dutch', English = 7725 ' English', French = 12911 ' French', German = 15913 ' German', Greek = 29511 ' Greek', Hindi = 38232 ' Hindi', Italian = 20605 ' Italian', Japanese = 18938 ' Japanese', Polish = 58531 ' Polish', Portuguese = 69919 ' Portuguese', Russian = 19225 ' Russian', Spanish = 21619 ' Spanish', Swahili = 6529 ' Sw', Thai = 33035 ' Thai', Turkish = 52662 ' Turkish', Urdu = 110563 ' Urdu', Vietnamese = 83833 ' Vietnamese'
== patent_section: 1000 items, 9 answers
   answer counts: Chemistry 94, Electricity 206, Fixed constructions 34, General tagging 97, Human necessities 149, Mechanical engineering 65, Performing operations 129, Physics 214, Textiles 12
   Qwen/Qwen3.5-0.8B: longest prompt 615 tokens (mean 190.4); first tokens all different: Chemistry = 40368 ' Chemistry', Electricity = 70859 ' Electricity', Fixed constructions = 19536 ' Fixed', General tagging = 3146 ' General', Human necessities = 10774 ' Human', Mechanical engineering = 48881 ' Mechanical', Performing operations = 67288 ' Performing', Physics = 26432 ' Physics', Textiles = 2824 ' Text'
   microsoft/Phi-4-mini-instruct: longest prompt 606 tokens (mean 185.9); first tokens all different: Chemistry = 68251 ' Chemistry', Electricity = 71181 ' Electricity', Fixed constructions = 42962 ' Fixed', General tagging = 5694 ' General', Human necessities = 16296 ' Human', Mechanical engineering = 79780 ' Mechanical', Performing operations = 97482 ' Performing', Physics = 48711 ' Physics', Textiles = 4564 ' Text'
== unfair_clause: 1000 items, 2 answers
   answer counts: Abusive 326, Safe 674
   Qwen/Qwen3.5-0.8B: longest prompt 374 tokens (mean 82.3); first tokens all different: Abusive = 3554 ' Ab', Safe = 21600 ' Safe'
   microsoft/Phi-4-mini-instruct: longest prompt 389 tokens (mean 84.9); first tokens all different: Abusive = 3483 ' Ab', Safe = 28304 ' Safe'
All checks passed: 12 tasks, every prompt at most 1,024 tokens, first tokens distinct, under both tokenizers.
```

The longest prompt of all is 615 tokens (`patent_section`, Qwen tokenizer), so no prompt will be cut.

## Gaps

Could not be done exactly as specified:

1. **Only three clearly legal tasks were found; the design asks for at least four.** The first test used up the
   legal sets that are short, public and have a test split, and LegalBench and LexGLUE are excluded. No fourth
   legal task was invented. Two of the nine non-legal tasks are near the border and are counted as not legal:
   - `appeal_outcome` is the outcome of a formal review of a health insurer's refusal. The first plan looked at the
     same dataset and called it "medical rather than legal", so it is counted as not legal here too. If the owner
     counts it as legal, the mix becomes 4 legal and 8 not, and nothing else in this plan changes (the four
     Phi-4-mini tasks stay the same).
   - `patent_section` uses patent documents, but its answers are fields of technology. If the owner counts it as
     legal instead, it would replace `contract_type` among the Phi-4-mini tasks (its prompts are shorter on
     average).

   Legal candidates looked at and left out, with the reason:
   - Immigration decisions, should a name be hidden (`pile-of-law/eoir_privacy`): prepared, then removed, because
     its longest prompt is 1,445 tokens.
   - Unfair terms of service in four languages (`joelniklaus/online_terms_of_service`, also in `lighteval/lextreme`):
     partly a copy of LexGLUE's unfair_tos. 1,617 of its 4,054 longer English training sentences, and 46 of 834
     in its test split, are in unfair_tos word for word.
   - Two more parts of LegalLAMA (`lexlms/legal_lama`): `contract_sections` is cut from LEDGAR (all 400 items
     checked contain LEDGAR text), and `us_terms` and `us_crimes` have items of up to about 21,700 tokens.
   - Topic of a question on Reddit's legal advice forum (`jonathanli/legal-advice-reddit`): the same kind of task
     as the first test's `law_topic`, from the forum that LegalBench's "learned hands" tasks are drawn from.
   - German terms and conditions (`d4br4/agb-de`): its longest item is 1,576 tokens.
   - Brazilian court decisions (`lighteval/lextreme`, `brazilian_court_decisions_judgment`): longest item 1,232
     tokens. Emergency laws (`covid19_emergency_event`, same collection): items can have several answers at once.
   - Chinese law exam (`hails/agieval-jec-qa-kd`): more than half the questions have several correct answers.
   - Korean sets: `lbox/lbox_open` (civil claims: one answer occurs 9 times, and some items are very long) and
     `lbox/kbl` (every part has fewer than 400 items).
   - No test or validation split: `joelniklaus/german_rental_agreements`, `biglam/on_the_books`,
     `LawInformedAI/mpre`, `darrow-ai/LegalLensNLI` (312 items), `darrow-ai/USClassActions`, and the two
     `alea-institute` sets looked at.
   - Policy area of a US bill (`hheiden/us-congress-117-bills`): several answers would occur fewer than 10 times.
   - Need an account approval to download: `opennyaiorg/InRhetoricalRoles`, `Exploration-Lab/IL-TUR`.
   - Did not load: `mila-ai4h/AIMS.au`. US bar exam questions (`reglab/barexam_qa`) need a loading script, have
     no parquet copy, and are the same kind of task as the first test's `law_exam`.
2. **Two of the three legal tasks are read from the dataset's own data file, not through the usual loader.**
   `reglab/housing_qa` and `lexlms/legal_lama` each need a loading script, which this version of the `datasets`
   library refuses to run, and neither has a parquet copy. `prepare.py` downloads the data file from the same
   repository at the pinned revision (`data/questions.json.zip` and `contract_types.jsonl`) and reads it as it
   is. No mirror or third-party copy is involved, and the split named in the table is the one the repository's
   own script gives that file. The brief says to pick a different task when a dataset fails to load; that was
   not done for these two, because without them only one legal task would be left. For the owner to accept or
   refuse.
3. **"Never used with this package before" could not be checked from here.** The package's history and the Handi
   repository were off limits. The twelve were checked against the README, the first plan and the exclusion
   list only.
4. **Two tasks use the parquet copy of a dataset that needs a loading script** (`unfair_clause`, `fair_reason`),
   which the brief allows. For `fair_reason` the copy's "test" split is the dataset's harder test file
   (`test_hard.csv`, 2,052 items); its easier test file is stored there as "validation" and is not used.
5. **The check cannot prove the package fills and counts prompts exactly as `check_prompts.py` does,** because
   the package source was off limits. The check follows the README (no special tokens added; answers read from
   the first token of a space plus the answer). The longest prompt is 409 tokens under the limit.

Choices made beyond the brief, for the owner to accept or change before this plan is committed:

6. **At 15 examples, several tasks mostly test the fallback, not the full choice of settings.** The README says
   that when some answer has fewer than two examples, `--auto` only removes the lean. `contract_type` (15
   answers), `language_id` (20) and `patent_section` (9) have more answers than 15 examples can cover twice, so
   this happens in every draw of 15 and of 30. Counting answers only (no model), it also happens in nearly
   every draw of 15 for `abstract_role`, about three in four for `climate_claim`, about half for
   `counterfactual` and about one in six for `fed_stance`. Two of these tasks (`contract_type`,
   `climate_claim`) are among the four Phi-4-mini tasks.
7. **Where the copies came from.** `counterfactual` is the MTEB benchmark's copy of Amazon's data; its `en-ext`
   part is used because the `en` part has only 335 test items. `language_id` was built by its author from
   product reviews and from two sets of translated sentence pairs, one of which (XNLI) is related to MultiNLI,
   used in the first test; none of the English items drawn here is a MultiNLI sentence (checked). The page of
   `appeal_outcome` says little beyond that the cases are real appeal decisions from US health insurance.
8. **`contract_type` and LEDGAR come from the same public source** (contracts filed with the US securities
   regulator), and LEDGAR is excluded. They are different texts: 6 of the 1,000 items share one stock phrase
   with a LEDGAR clause, and none is a LEDGAR clause.
9. **Answer words.** Where the dataset's own label is a natural word it is used with a capital letter
   (`contract_type`, `abstract_role`, `appeal_outcome`, `hate_speech`, `housing_law`). Where it is not, it was
   written as ordinary words: `unfair_clause` (the Polish labels became Abusive and Safe), `language_id` ("de"
   became German, and so on), `patent_section` (each section name cut to its first words, for example
   "Chemistry; Metallurgy" became Chemistry), `fed_stance` (0, 1, 2 became Dovish, Hawkish, Neutral, as the
   dataset's page defines them), `climate_claim` (SUPPORTS, REFUTES, NOT_ENOUGH_INFO, DISPUTED became Supported,
   Refuted, Not enough information, Disputed), and Yes/No for `counterfactual` and `fair_reason`.
10. **The picked items are kept in the dataset's own order, with their text exactly as stored** (including line
    breaks and spaces at the ends), and each line carries an `idx` field (its row number in the dataset) for
    tracing, which the package ignores. Some datasets repeat themselves: 11 of the `language_id` texts occur
    twice among the 1,000 items, the 1,000 `housing_law` items use 208 question wordings asked of different
    states, and `hate_speech` is built from sentence patterns.

## Notes added by the project coordinator before this plan was committed (15 November 2026)

The plan above was written by an agent that could read only the README and the first test's plan. These notes
were added afterwards by the coordinator, who could see the rest. No score of any kind had been computed for any
of the twelve tasks when they were written.

- **Gap 3 is closed.** None of the twelve datasets was run with the package before: the Handi repository uses only
  LegalBench and LexGLUE, and the earlier work on this package used only the tasks named in the README and the
  first test's twelve. Two of the twelve (`housing_law`, `appeal_outcome`) had been looked at as candidates for
  the first test and left out without any run.
- **Gaps 1 and 2 stand as written.** The test goes ahead with three legal tasks, and with `housing_law` and
  `contract_type` read from their repositories' own data files at the pinned revisions. Both are reported to the
  owner with the results.
- **The two versions.** "0.6.0" is the package at commit `735bcc6` of this repository (branch `auto-fixes-0.6.0`),
  committed before this plan. "0.5.0" is the package at commit `bb90606` (the `main` branch, the version of the
  first test). Each is installed from the repository at that commit into its own clean environment, with the
  same versions of torch (2.15.0) and transformers (5.23.0).
- **What 0.6.0 was developed on.** The change to `--auto` was developed on the twelve tasks of the first test and
  on six public tasks the README already names (AG News, dair-ai/emotion, tweet_eval sentiment, BoolQ, Rotten
  Tomatoes, LegalBench overruling), on Qwen3.5-0.8B, Qwen3.5-2B and Phi-4-mini. None of the twelve tasks in this
  plan was used.
- **Choice 6 describes 0.5.0.** In 0.6.0, `--auto` no longer switches the read-out off when an answer has fewer
  than two examples; it still chooses its settings. The results tables therefore count, for each task and size,
  the draws in which some answer had fewer than two examples, which is the same number for both versions.
- **Order of the runs.** The Qwen3.5-0.8B commands run on the GPU, all of 0.6.0's and then all of 0.5.0's. The
  Phi-4-mini commands run on the CPU. The results are tabulated by `validation2/analyse.py`, committed with this
  plan before any result exists.
