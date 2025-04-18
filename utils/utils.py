import re
import json
from typing import Union, List
def load_jsonl(path: str) -> List[dict]:
    with open(path, 'r', encoding='utf-8') as f:
        return [json.loads(line) for line in f if line.strip()]


def save_jsonl(path: str, data: Union[dict, List[dict]], append: bool = False):
    mode = 'a' if append or isinstance(data, dict) else 'w'
    with open(path, mode, encoding="utf-8") as f:
        if isinstance(data, list):
            for item in data:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
        elif isinstance(data, dict):
            f.write(json.dumps(data, ensure_ascii=False) + "\n")
        else:
            raise ValueError("Data must be a dict or a list of dicts")

def extract(response,data):
    thinking_pattern = re.compile(
        r"\*\*Thinking\*\*?:\s*(.*?)(?=\n{2,}|$)",
        re.MULTILINE | re.IGNORECASE
    )
    thinking_matches = thinking_pattern.findall(response)
    thinking = response if not thinking_matches else thinking_matches[0]
    data["Thinking"]=thinking

    answer_pattern = re.compile(
        r"\*\*Answer\*\*?:\s*(.*?)(?=\n{2,}|$)",
        re.MULTILINE | re.IGNORECASE
    )
    answer_matches = answer_pattern.findall(response)
    answer = response if not answer_matches else answer_matches[0]
    data["Answer"]=answer

    return data