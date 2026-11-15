"""Prepare the data for the second pre-registered held-out test of lmreadout (0.6.0 beside 0.5.0).

Downloads 12 public Hugging Face datasets (each pinned to a repo id, config, split and revision hash) and writes
validation2/data/<task>.jsonl, one JSON object per line: the fields the task's template uses, plus "answer".

No language model and no tokenizer is loaded here, and no score of any kind is computed.

Sampling rule (the same for every task): take one evaluation split. If it has more than 1,000 items, pick 1,000
uniformly at random without replacement with random.Random(0).sample(range(n), 1000) and keep them in the
split's original order; otherwise use every item. No item is dropped, cut or rebalanced.

Ten datasets are read with datasets.load_dataset. Two (housing_law, contract_type) have a loading script that
this version of the datasets library refuses to run and no parquet copy, so their data file is downloaded as it
is from the same repository, at the pinned revision, and read with the standard library; the split is the one
the repository's own loading script gives that file. See PLAN.md, "Gaps".

Run from anywhere:  python validation2/prepare.py
Running it twice gives byte-identical files.
"""

import collections
import json
import random
import zipfile
from pathlib import Path

import datasets
from huggingface_hub import hf_hub_download

HERE = Path(__file__).resolve().parent
DATA = HERE / "data"
SEED = 0
MAX_ITEMS = 1000
MIN_ITEMS = 400
MIN_PER_ANSWER = 10


# ---- how each split is read: returns a list-like of rows (dicts), in the dataset's own order ---------------------

def hub_split(repo, config, split, revision):
    return datasets.load_dataset(repo, config, split=split, revision=revision)


def hub_parquet_dir(repo, config, split, revision):
    # for a parquet conversion (refs/convert/parquet) of a dataset with several configs: one folder per config
    return datasets.load_dataset(repo, data_dir=config, split=split, revision=revision)


def raw_file(repo, filename, revision):
    return hf_hub_download(repo, filename, repo_type="dataset", revision=revision)


def housing_rows(repo, config, split, revision):
    # config "questions", split "test" in the repository's loading script: data/questions.json.zip
    assert (config, split) == ("questions", "test")
    with zipfile.ZipFile(raw_file(repo, "data/questions.json.zip", revision)) as z:
        return json.loads(z.read("questions.json").decode("utf-8"))


def legal_lama_rows(repo, config, split, revision):
    # config "contract_types", split "test" (the only split) in the repository's loading script: contract_types.jsonl
    assert (config, split) == ("contract_types", "test")
    with open(raw_file(repo, "contract_types.jsonl", revision), encoding="utf-8") as f:
        return [json.loads(line) for line in f]


# ---- one function per task: dataset row -> {template fields..., "answer": ...} ------------------------------------

def unfair_clause(r):
    # ClassLabel names: KLAUZULA_ABUZYWNA (abusive clause), BEZPIECZNE_POSTANOWIENIE_UMOWNE (safe contract term)
    return {"text": r["text"], "answer": {0: "Abusive", 1: "Safe"}[r["label"]]}


def housing_law(r):
    assert r["answer"] in ("Yes", "No")
    return {"state": r["state"], "question": r["question"], "answer": r["answer"]}


CONTRACT_TYPES = {"Award", "Consulting", "Credit", "Employment", "Indemnity", "Letter", "License", "Loan",
                  "Purchase", "Security", "Separation", "Services", "Settlement", "Supply", "Voting"}


def contract_type(r):
    sentences = r["masked_sentences"]  # a list holding one string
    assert isinstance(sentences, list) and len(sentences) == 1 and "<mask>" in sentences[0]
    assert r["obj_label"] in CONTRACT_TYPES
    return {"text": sentences[0], "answer": r["obj_label"]}


LANGUAGES = {"ar": "Arabic", "bg": "Bulgarian", "de": "German", "el": "Greek", "en": "English", "es": "Spanish",
             "fr": "French", "hi": "Hindi", "it": "Italian", "ja": "Japanese", "nl": "Dutch", "pl": "Polish",
             "pt": "Portuguese", "ru": "Russian", "sw": "Swahili", "th": "Thai", "tr": "Turkish", "ur": "Urdu",
             "vi": "Vietnamese", "zh": "Chinese"}


def language_id(r):
    return {"text": r["text"], "answer": LANGUAGES[r["labels"]]}


PATENT = ["Human necessities", "Performing operations", "Chemistry", "Textiles", "Fixed constructions",
          "Mechanical engineering", "Physics", "Electricity", "General tagging"]
# ClassLabel names, same order: Human Necessities | Performing Operations; Transporting | Chemistry; Metallurgy |
# Textiles; Paper | Fixed Constructions | Mechanical Engineering; Lightning; Heating; Weapons; Blasting | Physics |
# Electricity | General tagging of new or cross-sectional technology. Each is cut to its first words.


def patent_section(r):
    return {"text": r["text"], "answer": PATENT[r["label"]]}


ABSTRACT = {"background": "Background", "objective": "Objective", "methods": "Methods", "results": "Results",
            "conclusions": "Conclusions"}


def abstract_role(r):
    return {"text": r["text"], "answer": ABSTRACT[r["label"]]}


def fed_stance(r):
    # dataset card: LABEL_0 Dovish, LABEL_1 Hawkish, LABEL_2 Neutral
    return {"text": r["sentence"], "answer": {0: "Dovish", 1: "Hawkish", 2: "Neutral"}[r["label"]]}


CLIMATE = {0: "Supported", 1: "Refuted", 2: "Not enough information", 3: "Disputed"}
# ClassLabel names: SUPPORTS, REFUTES, NOT_ENOUGH_INFO, DISPUTED


def climate_claim(r):
    return {"claim": r["claim"], "answer": CLIMATE[r["claim_label"]]}


def hate_speech(r):
    return {"text": r["test_case"], "answer": {"hateful": "Hateful", "non-hateful": "Non-hateful"}[r["label_gold"]]}


def counterfactual(r):
    assert r["label_text"] == {1: "counterfactual", 0: "not-counterfactual"}[r["label"]]
    return {"text": r["text"], "answer": {1: "Yes", 0: "No"}[r["label"]]}


def fair_reason(r):
    # 1 = the reason given is reasonable, 0 = it is not
    return {"text": r["scenario"], "answer": {1: "Yes", 0: "No"}[r["label"]]}


def appeal_outcome(r):
    assert r["decision"] in ("Upheld", "Overturned")
    return {"text": r["text"], "answer": r["decision"]}


# ---- the 12 tasks: slug, repo id, config, split, revision hash, reader, row function ------------------------------

TASKS = [
    # legal
    # laugustyniak/abusive-clauses-pl needs a loading script on its main branch
    # (80d0d544f276b7a791dea0676f6c41200f4c8f70), so this pins the parquet conversion published under the same
    # repo's refs/convert/parquet.
    ("unfair_clause", "laugustyniak/abusive-clauses-pl", None, "test",
     "ea52f5ce905e44ad88b20bacb180f635400948a0", hub_split, unfair_clause),
    ("housing_law", "reglab/housing_qa", "questions", "test",
     "761550cc974fa1d9141ffd39014db89efa2a7230", housing_rows, housing_law),
    ("contract_type", "lexlms/legal_lama", "contract_types", "test",
     "e62bb3d77ac4797e86ad9779ced416a33db0fe96", legal_lama_rows, contract_type),
    # not legal
    ("language_id", "papluca/language-identification", None, "test",
     "aa56583bf2bc52b0565770607d6fc3faebecf9e2", hub_split, language_id),
    ("patent_section", "ccdv/patent-classification", "abstract", "test",
     "17bd94cd6594bac1b82a697e811fb7cf34a7af35", hub_split, patent_section),
    ("abstract_role", "armanc/pubmed-rct20k", None, "test",
     "091aec1e2384a20b2b36eb96177755ca13dd0b42", hub_split, abstract_role),
    ("fed_stance", "gtfintechlab/fomc_communication", None, "test",
     "6b0283f55f0005a6d38d49f271d795c21fccc1a3", hub_split, fed_stance),
    ("climate_claim", "tdiggelm/climate_fever", None, "test",
     "ae61ccb9320a78109a246414139ff3a2bd677b8b", hub_split, climate_claim),
    ("hate_speech", "Paul/hatecheck", None, "test",
     "9d2ac89df04254e5c427bcc8d61b6d6c83a1f59b", hub_split, hate_speech),
    ("counterfactual", "mteb/amazon_counterfactual", "en-ext", "test",
     "b9867e02b01002698f60c07fb8efdce8c5020ee8", hub_split, counterfactual),
    ("appeal_outcome", "Persius/imr-appeals", None, "test",
     "c68b70e0faf74cd2b5731ea02ad7ba7d99a11b8b", hub_split, appeal_outcome),
    # hendrycks/ethics needs a loading script on its main branch (b8b47c589f8bee77175b8648e5497278b68da48a), so
    # this pins the parquet conversion published under the same repo's refs/convert/parquet. Its "test" split is
    # the dataset's file test_hard.csv (2,052 items); its "validation" split is test.csv.
    ("fair_reason", "hendrycks/ethics", "justice", "test",
     "6deab74c03e30f13540266e373ce31f8466169f8", hub_parquet_dir, fair_reason),
]


def main():
    datasets.logging.set_verbosity_error()
    datasets.disable_progress_bars()
    DATA.mkdir(exist_ok=True)
    for slug, repo, config, split, revision, read, to_item in TASKS:
        rows = read(repo, config, split, revision)
        n = len(rows)
        if n > MAX_ITEMS:
            picked = sorted(random.Random(SEED).sample(range(n), MAX_ITEMS))
        else:
            picked = list(range(n))
        lines = []
        counts = collections.Counter()
        for i in picked:
            item = to_item(rows[i])
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
