"""Check the prepared data and templates with the two tokenizers. Tokenizers only: no model weights are loaded
and no score of any kind is computed.

For every task and both tokenizers it fills the template for every item and prints: the number of items, how
often each answer occurs, the longest filled prompt in tokens (it must be at most 1,024), and the id of the first
token of (space + answer) for each answer (they must all differ, because the package tells answers apart by that
first token).

Prompts and answers are tokenized the way the package README shows: no special tokens are added, and each answer
is read from the first token of a space followed by the answer.

Run from anywhere:  python validation/check_prompts.py
"""

import collections
import json
import re
from pathlib import Path

from transformers import AutoTokenizer

HERE = Path(__file__).resolve().parent
TOKENIZERS = ["Qwen/Qwen3.5-0.8B", "microsoft/Phi-4-mini-instruct"]
MAX_LEN = 1024
MIN_ITEMS = 400
MIN_PER_ANSWER = 10
FIELD = re.compile(r"\{\{(\w+)\}\}")


def load(slug):
    template = (HERE / "templates" / f"{slug}.txt").read_text(encoding="utf-8")
    assert not template.endswith("\n"), f"{slug}: template must end exactly where the answer goes"
    with open(HERE / "data" / f"{slug}.jsonl", encoding="utf-8") as f:
        items = [json.loads(line) for line in f]
    fields = FIELD.findall(template)
    assert fields, slug
    prompts = []
    for item in items:
        for name in fields:
            assert isinstance(item[name], str) and "{{" not in item[name], (slug, name)
        prompts.append(FIELD.sub(lambda m: item[m.group(1)], template))
    return items, prompts


def main():
    slugs = sorted(p.stem for p in (HERE / "templates").glob("*.txt"))
    assert slugs == sorted(p.stem for p in (HERE / "data").glob("*.jsonl")), "data and templates do not match"
    assert len(slugs) == 12, slugs
    tokenizers = {name: AutoTokenizer.from_pretrained(name) for name in TOKENIZERS}
    for slug in slugs:
        items, prompts = load(slug)
        counts = collections.Counter(item["answer"] for item in items)
        answers = sorted(counts)
        assert len(items) >= MIN_ITEMS, (slug, len(items))
        assert min(counts.values()) >= MIN_PER_ANSWER, (slug, counts)
        print(f"== {slug}: {len(items)} items, {len(answers)} answers")
        print("   answer counts: " + ", ".join(f"{a} {counts[a]}" for a in answers))
        for name, tok in tokenizers.items():
            lengths = [len(ids) for ids in tok(prompts, add_special_tokens=False)["input_ids"]]
            first = {a: tok(" " + a, add_special_tokens=False)["input_ids"][0] for a in answers}
            assert max(lengths) <= MAX_LEN, (slug, name, max(lengths))
            assert len(set(first.values())) == len(answers), (slug, name, first)
            print(f"   {name}: longest prompt {max(lengths)} tokens (mean {sum(lengths) / len(lengths):.0f}); "
                  f"first tokens all different: "
                  + ", ".join(f"{a} = {first[a]} {tok.decode([first[a]])!r}" for a in answers))
    print("All checks passed: 12 tasks, every prompt at most 1,024 tokens, first tokens distinct, "
          "under both tokenizers.")


if __name__ == "__main__":
    main()
