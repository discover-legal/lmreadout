"""Prepare the data for the pre-registered held-out test of lmreadout 0.5.0.

Downloads 12 public Hugging Face datasets (each pinned to a repo id, config, split and revision hash) and writes
validation/data/<task>.jsonl, one JSON object per line: the fields the task's template uses, plus "answer".

No language model and no tokenizer is loaded here, and no score of any kind is computed.

Sampling rule (the same for every task): take one evaluation split. If it has more than 1,000 items, pick 1,000
uniformly at random without replacement with random.Random(0).sample(range(n), 1000) and keep them in the
split's original order; otherwise use every item. No item is dropped, cut or rebalanced.

Run from anywhere:  python validation/prepare.py
Running it twice gives byte-identical files.
"""

import collections
import json
import random
from pathlib import Path

import datasets

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
SEED = 0
MAX_ITEMS = 1000
MIN_ITEMS = 400
MIN_PER_ANSWER = 10

LETTERS = ["A", "B", "C", "D"]


# ---- one function per task: dataset row -> {template fields..., "answer": ...} ------------------------------------

LAW_TOPIC = {
    "copyright": "Copyright",
    "criminal-law": "Criminal law",
    "contract-law": "Contract law",
    "employment": "Employment",
    "trademark": "Trademark",
    "internet": "Internet",
    "privacy": "Privacy",
    "tax-law": "Tax law",
    "contract": "Contracts",  # the site has both a "contract-law" and a "contract" tag; see PLAN.md
    "intellectual-property": "Intellectual property",
    "business": "Business",
    "licensing": "Licensing",
    "constitutional-law": "Constitutional law",
    "software": "Software",
    "liability": "Liability",
    "civil-law": "Civil law",
}


def law_topic(r):
    return {"title": r["title"], "answer": LAW_TOPIC[r["text_label"]]}


def law_exam(r):
    out = {"question": r["question"]}
    assert len(r["choices"]) == 4
    for letter, choice in zip(LETTERS, r["choices"]):
        out[letter.lower()] = choice
    out["answer"] = LETTERS[r["answer"]]  # ClassLabel names: A, B, C, D
    return out


def legal_support(r):
    return {
        "context": r["context"],
        "a": r["citation_a"]["parenthetical"],
        "b": r["citation_b"]["parenthetical"],
        "answer": {"a": "A", "b": "B"}[r["label"]],
    }


GERMAN = {"conclusion": "Conclusion", "definition": "Definition", "subsumption": "Subsumption", "other": "Other"}


def german_argument(r):
    return {"text": r["input_sentence"], "answer": GERMAN[r["label"]]}


def acceptability(r):
    return {"text": r["sentence"], "answer": {1: "Yes", 0: "No"}[r["label"]]}  # 1 = acceptable


def nli(r):
    # 0 entailment, 1 neutral, 2 contradiction
    return {"premise": r["premise"], "hypothesis": r["hypothesis"], "answer": {0: "True", 1: "Neither", 2: "False"}[r["label"]]}


def stance(r):
    return {"topic": r["topic"], "argument": r["argument"], "answer": {1: "Pro", -1: "Con"}[r["stance_WA"]]}


def paraphrase(r):
    return {"sentence1": r["sentence1"], "sentence2": r["sentence2"], "answer": {1: "Yes", 0: "No"}[r["label"]]}


def word_sense(r):
    # 1 = the word has the same meaning in both sentences
    return {"word": r["word"], "sentence1": r["sentence1"], "sentence2": r["sentence2"],
            "answer": {1: "Yes", 0: "No"}[r["label"]]}


MTOP = {0: "Messaging", 1: "Calling", 2: "Event", 3: "Timer", 4: "Music", 5: "Weather", 6: "Alarm", 7: "People",
        8: "Reminder", 9: "Recipes", 10: "News"}
# Label names from the source repo mteb/mtop_domain (en/test.jsonl, fields label and label_text).


def request_domain(r):
    return {"text": r["text"], "answer": MTOP[r["label"]]}


SCICITE = {0: "Method", 1: "Background", 2: "Result"}  # ClassLabel names: method, background, result


def citation_intent(r):
    return {"text": r["string"], "answer": SCICITE[r["label"]]}


DBPEDIA = ["Company", "Educational institution", "Artist", "Athlete", "Office holder", "Means of transportation",
           "Building", "Natural place", "Village", "Animal", "Plant", "Album", "Film", "Written work"]
# ClassLabel names: Company, EducationalInstitution, Artist, Athlete, OfficeHolder, MeanOfTransportation, Building,
# NaturalPlace, Village, Animal, Plant, Album, Film, WrittenWork (same order, written as ordinary words).


def wiki_category(r):
    return {"text": r["content"], "answer": DBPEDIA[r["label"]]}


# ---- the 12 tasks: slug, repo id, config, split, revision hash, row function -------------------------------------

TASKS = [
    # legal
    ("law_topic", "jonathanli/law-stack-exchange", None, "test",
     "baa2e9a0a5d19ff2838e9cfbceb85b81d7a06f8e", law_topic),
    ("law_exam", "cais/mmlu", "professional_law", "test",
     "c30699e8356da336a370243923dbaf21066bb9fe", law_exam),
    ("legal_support", "lighteval/LegalSupport", None, "test",
     "a85189d679727140e8c5fdda07ef27aded168258", legal_support),
    ("german_argument", "joelniklaus/german_argument_mining", None, "test",
     "576b52004ed78dd747c0f9858fa6dacc7e4196e2", german_argument),
    # not legal
    ("acceptability", "nyu-mll/glue", "cola", "validation",
     "bcdcba79d07bc864c1c254ccfcedcce55bcc9a8c", acceptability),
    ("nli", "nyu-mll/multi_nli", None, "validation_matched",
     "da70db2af9d09693783c3320c4249840212ee221", nli),
    ("stance", "ibm-research/argument_quality_ranking_30k", "argument_quality_ranking", "test",
     "590726b3765b1b90c5e53a17e3b1f77d92d3aa8a", stance),
    ("paraphrase", "google-research-datasets/paws", "labeled_final", "test",
     "161ece9501cf0a11f3e48bd356eaa82de46d6a09", paraphrase),
    ("word_sense", "aps/super_glue", "wic", "validation",
     "3de24cf8022e94f4ee4b9d55a6f539891524d646", word_sense),
    ("request_domain", "mteb/MTOPDomainClassification", "en", "test",
     "a76d16fae880597b9c73047b50159220a441cb54", request_domain),
    # allenai/scicite needs a loading script on its main branch (4c40e64d8eebd9c0a8f27bb630cfbaeffc01c941), so this
    # pins the parquet conversion published under the same repo's refs/convert/parquet.
    ("citation_intent", "allenai/scicite", None, "test",
     "f6a02e9afbd45c39b5ee6caf38e110466e36b650", citation_intent),
    ("wiki_category", "fancyzhx/dbpedia_14", "dbpedia_14", "test",
     "9abd46cf7fc8b4c64290f26993c540b92aa145ac", wiki_category),
]


def main():
    datasets.logging.set_verbosity_error()
    datasets.disable_progress_bars()
    DATA.mkdir(exist_ok=True)
    for slug, repo, config, split, revision, to_item in TASKS:
        ds = datasets.load_dataset(repo, config, split=split, revision=revision)
        n = len(ds)
        if n > MAX_ITEMS:
            picked = sorted(random.Random(SEED).sample(range(n), MAX_ITEMS))
        else:
            picked = list(range(n))
        lines = []
        counts = collections.Counter()
        for i in picked:
            item = to_item(ds[i])
            for key, value in item.items():
                assert isinstance(value, str) and value.strip(), (slug, i, key, value)
            item = {"idx": i, **item}  # row number in the split, for tracing only; the package ignores it
            counts[item["answer"]] += 1
            lines.append(json.dumps(item, ensure_ascii=False))
        assert len(lines) >= MIN_ITEMS, (slug, len(lines))
        assert min(counts.values()) >= MIN_PER_ANSWER, (slug, counts)
        (DATA / f"{slug}.jsonl").write_text("\n".join(lines) + "\n", encoding="utf-8")
        shown = ", ".join(f"{a} {c}" for a, c in sorted(counts.items(), key=lambda x: (-x[1], x[0])))
        print(f"{slug}: {len(lines)} of {n} items from {repo} [{config or 'default'} / {split} @ {revision[:8]}] | {shown}")


if __name__ == "__main__":
    main()
