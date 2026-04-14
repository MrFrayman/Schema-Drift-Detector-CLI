import json
from pathlib import Path
from typing import Any


def load_json_file(path: str | Path) -> Any:
    file_path = Path(path)
    with file_path.open("r", encoding="utf-8") as f:
        return json.load(f)
    

def save_json_file(path: str | Path, data: Any) -> None:
    file_path = Path(path)
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")

    