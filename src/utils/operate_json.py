import json
from typing import Dict, Any
from pathlib import Path


def load_json_as_dict(json_path: Path):
    with open(json_path, "r") as f:
        res: Dict[str, Any] = json.load(f)
    return res
