# Held-out test of lmreadout 0.5.0: the plan

## Purpose

This is a test of `lmreadout --auto` on twelve classification tasks the package has not been run on, with the
tasks, the prompts and the pass/fail rules written down here before any model is run. Nobody has computed a score
of any kind for these tasks yet (not even the untouched model's), so nothing below could have been chosen to make
the result look good or bad.

## The 12 tasks

Every task is a public Hugging Face dataset, pinned to one exact version (the "revision"). "Items" is how many
examples are in the test file; the answers keep the proportions they have in the dataset.

| Task | Dataset, config, split, revision | Legal? | Answers | Answer words, exactly as in the data | Items | Why it was picked |
|---|---|---|---|---|---|---|
| `law_topic` | `jonathanli/law-stack-exchange`, default, test, `baa2e9a0a5d19ff2838e9cfbceb85b81d7a06f8e` | legal | 16 | Business, Civil law, Constitutional law, Contract law, Contracts, Copyright, Criminal law, Employment, Intellectual property, Internet, Liability, Licensing, Privacy, Software, Tax law, Trademark | 1,000 of 1,596 | Topic: which area of law a question (its title) is about. |
| `law_exam` | `cais/mmlu`, `professional_law`, test, `c30699e8356da336a370243923dbaf21066bb9fe` | legal | 4 | A, B, C, D | 1,000 of 1,534 | Legal reasoning: pick the right one of four answers to a law exam question. |
| `legal_support` | `lighteval/LegalSupport`, default, test, `a85189d679727140e8c5fdda07ef27aded168258` | legal | 2 | A, B | 1,000 of 3,047 | Comparing two texts against a third: which of two cited cases backs a passage more strongly. |
| `german_argument` | `joelniklaus/german_argument_mining`, default, test, `576b52004ed78dd747c0f9858fa6dacc7e4196e2` | legal | 4 | Conclusion, Definition, Subsumption, Other | 1,000 of 3,078 | The part a sentence plays in a court's reasoning, and the only task not in English (German sentences, English prompt). |
| `acceptability` | `nyu-mll/glue`, `cola`, validation, `bcdcba79d07bc864c1c254ccfcedcce55bcc9a8c` | no | 2 | Yes, No | 1,000 of 1,043 | Acceptability: is a sentence grammatical English. |
| `nli` | `nyu-mll/multi_nli`, default, validation_matched, `da70db2af9d09693783c3320c4249840212ee221` | no | 3 | True, False, Neither | 1,000 of 9,815 | Inference between two texts: does one sentence follow from another. |
| `stance` | `ibm-research/argument_quality_ranking_30k`, `argument_quality_ranking`, test, `590726b3765b1b90c5e53a17e3b1f77d92d3aa8a` | no | 2 | Pro, Con | 1,000 of 6,315 | Stance: is an argument for or against a debate topic. |
| `paraphrase` | `google-research-datasets/paws`, `labeled_final`, test, `161ece9501cf0a11f3e48bd356eaa82de46d6a09` | no | 2 | Yes, No | 1,000 of 8,000 | Same meaning or not, for two sentences that share most of their words. |
| `word_sense` | `aps/super_glue`, `wic`, validation, `3de24cf8022e94f4ee4b9d55a6f539891524d646` | no | 2 | Yes, No | 638 of 638 | Word meaning: is one word used in the same sense in two sentences. |
| `request_domain` | `mteb/MTOPDomainClassification`, `en`, test, `a76d16fae880597b9c73047b50159220a441cb54` | no | 11 | Alarm, Calling, Event, Messaging, Music, News, People, Recipes, Reminder, Timer, Weather | 1,000 of 4,386 | Intent: what a spoken request to a voice assistant is about. |
| `citation_intent` | `allenai/scicite`, default, test, `f6a02e9afbd45c39b5ee6caf38e110466e36b650` (the parquet copy under the same repo's `refs/convert/parquet`) | no | 3 | Background, Method, Result | 1,000 of 1,859 | Intent of a citation in a scientific paper. |
| `wiki_category` | `fancyzhx/dbpedia_14`, `dbpedia_14`, test, `9abd46cf7fc8b4c64290f26993c540b92aa145ac` | no | 14 | Company, Educational institution, Artist, Athlete, Office holder, Means of transportation, Building, Natural place, Village, Animal, Plant, Album, Film, Written work | 1,000 of 70,000 | Topic outside news: what kind of thing a Wikipedia text describes. |

The mix: 4 legal and 8 not legal; 5 tasks with two answers and 7 with three or more.

Note, 13 November 2026: `case_hold` was in the first draft of this plan and was replaced before any score was
computed, because it had been run during the method's development. `law_exam` took its place. The other 11
tasks, their data, prompts and answer words are unchanged from the first draft.

How the items were drawn (the same for every task, done by `validation/prepare.py`): where the split has more
than 1,000 items, 1,000 were picked at random with seed 0; where it has fewer, all were used. Nothing was dropped,
shortened or rebalanced. Running `prepare.py` again gives exactly the same files.

Each task has one prompt, in `validation/templates/<task>.txt`, written once and not to be changed.

## The 4 tasks also run on Phi-4-mini

`law_topic` (legal, 16 answers), `legal_support` (legal, 2 answers), `acceptability` (not legal, 2 answers) and
`request_domain` (not legal, 11 answers).

That is one task of each combination (legal or not, two answers or more), and within each combination the task
with the shortest prompts on average, because this model runs on the CPU.

## The run commands

Run from `/home/hd/Documents/GitHub/lmreadout`, unchanged. No command uses `--labels`: the README says that
without it every distinct answer in the data is used, and it does not say `--labels` is needed for any kind of
task.

Primary: the 12 tasks on Qwen3.5-0.8B.

```
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/law_topic.jsonl --template validation/templates/law_topic.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/law_topic.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/law_exam.jsonl --template validation/templates/law_exam.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/law_exam.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/legal_support.jsonl --template validation/templates/legal_support.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/legal_support.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/german_argument.jsonl --template validation/templates/german_argument.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/german_argument.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/acceptability.jsonl --template validation/templates/acceptability.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/acceptability.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/nli.jsonl --template validation/templates/nli.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/nli.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/stance.jsonl --template validation/templates/stance.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/stance.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/paraphrase.jsonl --template validation/templates/paraphrase.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/paraphrase.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/word_sense.jsonl --template validation/templates/word_sense.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/word_sense.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/request_domain.jsonl --template validation/templates/request_domain.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/request_domain.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/citation_intent.jsonl --template validation/templates/citation_intent.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/citation_intent.qwen08.csv
lmreadout sweep --model Qwen/Qwen3.5-0.8B --data validation/data/wiki_category.jsonl --template validation/templates/wiki_category.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/wiki_category.qwen08.csv
```

Secondary: the 4 tasks on Phi-4-mini.

```
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation/data/law_topic.jsonl --template validation/templates/law_topic.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/law_topic.phi4mini.csv --device cpu
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation/data/legal_support.jsonl --template validation/templates/legal_support.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/legal_support.phi4mini.csv --device cpu
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation/data/acceptability.jsonl --template validation/templates/acceptability.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/acceptability.phi4mini.csv --device cpu
lmreadout sweep --model microsoft/Phi-4-mini-instruct --data validation/data/request_domain.jsonl --template validation/templates/request_domain.txt --sizes 15 30 60 120 --draws 20 --auto --csv validation/results/request_domain.phi4mini.csv --device cpu
```

## Rules fixed before any score

All scores are balanced accuracy, the mean over the 20 draws, as `sweep` reports them. Primary: the 12 tasks on Qwen3.5-0.8B. Secondary, judged by the same rules and reported separately: the 4 tasks on Phi-4-mini.

- **Rule 1 (no real harm at 15):** on every task, `--auto` with 15 examples is at most 0.02 below the model as shipped. Fails if any task is more than 0.02 below.
- **Rule 2 (matches the fixed edit at 120):** on every task, `--auto` with 120 examples is at most 0.005 below the fixed edit with 120 examples. Fails if any task is more than 0.005 below.
- **Rule 3 (level with the better safe choice at 15):** per task take the better of "as shipped" and "calibration only" at 15 examples; the mean over tasks of (`--auto` minus that) is at least -0.01. Fails if it is below -0.01.
- **Reported whatever the outcome, for every task, model and size (15/30/60/120):** as shipped, calibration only, word counts, fixed edit, `--auto`, with the spread over draws; guessing rate; the settings `--auto` chose; and counts of tasks where `--auto` is above/below each other column. No task, size or model may be dropped after scores are seen; a run that crashes or is refused by the package is reported as such, not replaced.

## Check of the prompts and answers

Output of `validation/check_prompts.py`. It loads the two tokenizers only (no model). For each task it shows the
number of items, how often each answer occurs, the longest filled prompt in tokens (the limit is 1,024), and the
first token of each answer, which is what the package reads; these must all differ within a task.

```
== acceptability: 1000 items, 2 answers
   answer counts: No 311, Yes 689
   Qwen/Qwen3.5-0.8B: longest prompt 52 tokens (mean 29); first tokens all different: No = 2233 ' No', Yes = 7179 ' Yes'
   microsoft/Phi-4-mini-instruct: longest prompt 49 tokens (mean 26); first tokens all different: No = 3004 ' No', Yes = 11377 ' Yes'
== citation_intent: 1000 items, 3 answers
   answer counts: Background 540, Method 328, Result 132
   Qwen/Qwen3.5-0.8B: longest prompt 299 tokens (mean 100); first tokens all different: Background = 24016 ' Background', Method = 6519 ' Method', Result = 5536 ' Result'
   microsoft/Phi-4-mini-instruct: longest prompt 278 tokens (mean 93); first tokens all different: Background = 39236 ' Background', Method = 11109 ' Method', Result = 9112 ' Result'
== german_argument: 1000 items, 4 answers
   answer counts: Conclusion 32, Definition 204, Other 185, Subsumption 579
   Qwen/Qwen3.5-0.8B: longest prompt 811 tokens (mean 82); first tokens all different: Conclusion = 71366 ' Conclusion', Definition = 19107 ' Definition', Other = 6728 ' Other', Subsumption = 3593 ' Sub'
   microsoft/Phi-4-mini-instruct: longest prompt 699 tokens (mean 78); first tokens all different: Conclusion = 98264 ' Conclusion', Definition = 42046 ' Definition', Other = 10473 ' Other', Subsumption = 5934 ' Sub'
== law_exam: 1000 items, 4 answers
   answer counts: A 251, B 243, C 267, D 239
   Qwen/Qwen3.5-0.8B: longest prompt 793 tokens (mean 279); first tokens all different: A = 357 ' A', B = 417 ' B', C = 351 ' C', D = 414 ' D'
   microsoft/Phi-4-mini-instruct: longest prompt 745 tokens (mean 269); first tokens all different: A = 355 ' A', B = 418 ' B', C = 363 ' C', D = 415 ' D'
== law_topic: 1000 items, 16 answers
   answer counts: Business 32, Civil law 20, Constitutional law 33, Contract law 105, Contracts 42, Copyright 267, Criminal law 115, Employment 59, Intellectual property 34, Internet 56, Liability 17, Licensing 37, Privacy 53, Software 27, Tax law 48, Trademark 55
   Qwen/Qwen3.5-0.8B: longest prompt 92 tokens (mean 68); first tokens all different: Business = 7773 ' Business', Civil law = 15917 ' Civil', Constitutional law = 60090 ' Constitutional', Contract law = 18605 ' Contract', Contracts = 68175 ' Contracts', Copyright = 2861 ' Copyright', Criminal law = 31651 ' Criminal', Employment = 39503 ' Employment', Intellectual property = 74228 ' Intellectual', Internet = 7779 ' Internet', Liability = 86946 ' Liability', Licensing = 69869 ' Licensing', Privacy = 18304 ' Privacy', Software = 4236 ' Software', Tax law = 14748 ' Tax', Trademark = 14627 ' Trad'
   microsoft/Phi-4-mini-instruct: longest prompt 87 tokens (mean 65); first tokens all different: Business = 8084 ' Business', Civil law = 21595 ' Civil', Constitutional law = 134373 ' Constitutional', Contract law = 25875 ' Contract', Contracts = 98045 ' Contracts', Copyright = 6075 ' Copyright', Criminal law = 56887 ' Criminal', Employment = 60588 ' Employment', Intellectual property = 124235 ' Intellectual', Internet = 7380 ' Internet', Liability = 119939 ' Liability', Licensing = 129803 ' Licensing', Privacy = 25695 ' Privacy', Software = 7564 ' Software', Tax law = 18489 ' Tax', Trademark = 125003 ' Trademark'
== legal_support: 1000 items, 2 answers
   answer counts: A 514, B 486
   Qwen/Qwen3.5-0.8B: longest prompt 372 tokens (mean 162); first tokens all different: A = 357 ' A', B = 417 ' B'
   microsoft/Phi-4-mini-instruct: longest prompt 364 tokens (mean 158); first tokens all different: A = 355 ' A', B = 418 ' B'
== nli: 1000 items, 3 answers
   answer counts: False 325, Neither 320, True 355
   Qwen/Qwen3.5-0.8B: longest prompt 190 tokens (mean 68); first tokens all different: False = 3439 ' False', Neither = 23472 ' Neither', True = 2912 ' True'
   microsoft/Phi-4-mini-instruct: longest prompt 185 tokens (mean 64); first tokens all different: False = 7983 ' False', Neither = 49579 ' Neither', True = 6432 ' True'
== paraphrase: 1000 items, 2 answers
   answer counts: No 523, Yes 477
   Qwen/Qwen3.5-0.8B: longest prompt 155 tokens (mean 82); first tokens all different: No = 2233 ' No', Yes = 7179 ' Yes'
   microsoft/Phi-4-mini-instruct: longest prompt 140 tokens (mean 76); first tokens all different: No = 3004 ' No', Yes = 11377 ' Yes'
== request_domain: 1000 items, 11 answers
   answer counts: Alarm 79, Calling 145, Event 40, Messaging 78, Music 73, News 91, People 82, Recipes 69, Reminder 157, Timer 78, Weather 108
   Qwen/Qwen3.5-0.8B: longest prompt 65 tokens (mean 48); first tokens all different: Alarm = 44742 ' Alarm', Calling = 31226 ' Calling', Event = 3539 ' Event', Messaging = 70681 ' Messaging', Music = 10401 ' Music', News = 5230 ' News', People = 8586 ' People', Recipes = 42732 ' Recipes', Reminder = 92585 ' Reminder', Timer = 17229 ' Timer', Weather = 21926 ' Weather'
   microsoft/Phi-4-mini-instruct: longest prompt 63 tokens (mean 46); first tokens all different: Alarm = 64536 ' Alarm', Calling = 66982 ' Calling', Event = 6400 ' Event', Messaging = 125028 ' Messaging', Music = 12878 ' Music', News = 5984 ' News', People = 12598 ' People', Recipes = 70616 ' Recipes', Reminder = 159156 ' Reminder', Timer = 34957 ' Timer', Weather = 32492 ' Weather'
== stance: 1000 items, 2 answers
   answer counts: Con 501, Pro 499
   Qwen/Qwen3.5-0.8B: longest prompt 77 tokens (mean 49); first tokens all different: Con = 1160 ' Con', Pro = 1253 ' Pro'
   microsoft/Phi-4-mini-instruct: longest prompt 76 tokens (mean 47); first tokens all different: Con = 1532 ' Con', Pro = 1258 ' Pro'
== wiki_category: 1000 items, 14 answers
   answer counts: Album 71, Animal 68, Artist 75, Athlete 87, Building 66, Company 71, Educational institution 77, Film 71, Means of transportation 68, Natural place 70, Office holder 65, Plant 77, Village 69, Written work 65
   Qwen/Qwen3.5-0.8B: longest prompt 279 tokens (mean 120); first tokens all different: Album = 24847 ' Album', Animal = 20637 ' Animal', Artist = 27436 ' Artist', Athlete = 19096 ' Ath', Building = 16366 ' Building', Company = 7931 ' Company', Educational institution = 44317 ' Educational', Film = 16142 ' Film', Means of transportation = 57691 ' Means', Natural place = 17898 ' Natural', Office holder = 7988 ' Office', Plant = 17305 ' Plant', Village = 23316 ' Village', Written work = 32770 ' Written'
   microsoft/Phi-4-mini-instruct: longest prompt 261 tokens (mean 112); first tokens all different: Album = 42336 ' Album', Animal = 32472 ' Animal', Artist = 42257 ' Artist', Athlete = 199952 ' Athlete', Building = 22478 ' Building', Company = 9709 ' Company', Educational institution = 65312 ' Educational', Film = 18571 ' Film', Means of transportation = 125152 ' Means', Natural place = 23735 ' Natural', Office holder = 11360 ' Office', Plant = 23279 ' Plant', Village = 27912 ' Village', Written work = 54393 ' Written'
== word_sense: 638 items, 2 answers
   answer counts: No 319, Yes 319
   Qwen/Qwen3.5-0.8B: longest prompt 90 tokens (mean 52); first tokens all different: No = 2233 ' No', Yes = 7179 ' Yes'
   microsoft/Phi-4-mini-instruct: longest prompt 86 tokens (mean 49); first tokens all different: No = 3004 ' No', Yes = 11377 ' Yes'
All checks passed: 12 tasks, every prompt at most 1,024 tokens, first tokens distinct, under both tokenizers.
```

The longest prompt of all is 811 tokens (`german_argument`, Qwen tokenizer), so no prompt will be cut.

## Gaps

Could not be done exactly as specified:

1. **"Never used with this package before" could not be checked from here.** The package's history and the
   Handi repository were off limits; only the README could be read, and it names AG News, LegalBench,
   dair-ai/emotion, tweet_eval, BoolQ and Rotten Tomatoes. After the first draft the project coordinator confirmed
   that 11 of the tasks had never been run with the package and that `case_hold` had; it was replaced (see the
   note under the task table). Everything in `coastalcph/lex_glue` is now excluded as well. The replacement,
   `law_exam`, has so far been checked only against the README and these exclusions.
2. **Three tasks use a validation split although a test split is named in the design.** For `acceptability` and
   `word_sense` the test split exists but its answers are not public. For `nli` the dataset has no test split.
3. **Only four suitable legal tasks were found, and each needs a remark.** Public legal classification sets that
   are not LegalBench, have short texts and have a test split are scarce.
   - `law_exam` and `legal_support` are multiple-choice: the answers are the letters A to D and A or B, not words
     with a fixed meaning.
   - `german_argument` is in German.
   - `law_topic` uses the question's title only, because with the full question some items would be longer than
     1,024 tokens. The dataset has two tags, "contract-law" and "contract", that would start with the same token;
     they are written "Contract law" and "Contracts".
   - Three have a distant relative in LegalBench with different data: `law_topic` (the "learned hands" topic
     tasks), `german_argument` ("function of a decision section"), `legal_support` ("citation prediction").
     `legal_support` shares no passage with that LegalBench task (checked).
   - A fifth legal candidate, the purpose of a privacy-policy sentence (`alzoubi36/policy_ie_a`), was left out as
     too close to LegalBench's OPP-115 tasks: same kind of task, and 22 of its 765 longer sentences also appear
     word for word in LegalBench's privacy texts.
   - Other legal candidates looked at for the replacement and not used: Brazilian court decisions
     (`joelniklaus/brazilian_court_decisions`) and the LEXam law exams (`LEXam-Benchmark/LEXam`) have items longer
     than 1,024 tokens; ECHR argument questions (`AUEB-NLP/lar-echr`) and LegalLens (`darrow-ai/LegalLensNLI`)
     have fewer than 400 items; `reglab/barexam_qa`, `reglab/housing_qa` and `pile-of-law/eoir_privacy` need a
     loading script and have no parquet copy; several others have no test or validation split; health-insurance
     appeal outcomes (`Persius/imr-appeals`) fit but are medical rather than legal.
4. **The check cannot prove the package fills and counts prompts exactly as `check_prompts.py` does,** because
   the package source was off limits. The check follows the README (no special tokens added; answers read from
   the first token of a space plus the answer). The longest prompt is 213 tokens under the limit.

Choices made beyond the brief, for the owner to accept or change before this plan is committed:

5. **At 15 examples, four tasks mostly test the fallback, not the full choice of settings.** The README says
   that when some answer has fewer than two examples, `--auto` only removes the lean. Three tasks have more
   answers than 15 examples can cover twice (`request_domain` 11, `wiki_category` 14, `law_topic` 16), so this
   happens in every draw of 15 and in many draws of 30. In `german_argument` the answer "Conclusion" is 3% of the
   items, so it happens in about nine draws of 15 out of ten. Two of these tasks are among the four Phi-4-mini
   tasks.
6. **The four Phi-4-mini tasks** were chosen as one of each combination, shortest prompts first. Going by
   shortest prompts alone, without one of each combination, would give `law_topic`, `german_argument`,
   `acceptability` and `stance` instead.
7. **Where the copies came from.** `legal_support` is the copy of the HELM benchmark's data published by
   `lighteval` (Hugging Face's evaluation team); it has no description page. `request_domain` is the MTEB
   benchmark's copy of Facebook's MTOP data; it stores answers as numbers, and the names were taken from the
   same organisation's source copy (`mteb/mtop_domain`). `citation_intent` is read from the parquet copy that
   the hub publishes under the same repository, because the main version needs a loading script.
8. **Answer words.** Where the dataset's own label is a natural word it is used with a capital letter. Where it
   is not, it was written as ordinary words: `wiki_category` ("OfficeHolder" became "Office holder", and so on),
   `law_topic` ("criminal-law" became "Criminal law"), `nli` (entailment, neutral, contradiction became True,
   Neither, False), `stance` (1 and -1 became Pro and Con), and Yes/No for `acceptability`, `paraphrase` and
   `word_sense`.
9. **The 1,000 picked items are kept in the dataset's own order,** and each line carries an `idx` field (its row
   number in the dataset) for tracing, which the package ignores.
