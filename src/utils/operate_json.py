import json
from pathlib import Path
from typing import Any, Dict


def load_json_as_dict(json_path: Path):
    with open(json_path, "r") as f:
        res: Dict[str, Any] = json.load(f)
    return res
