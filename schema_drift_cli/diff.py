# This is the heart of this project.

from __future__ import annotations

from dataclasses import dataclass, field
from os import path
from typing import Any
from unittest import result

@dataclass
class DiffResult:
    added: list[dict[str, Any]] = field(default_factory=list)
    removed: list[dict[str, Any]] = field(default_factory=list)
    changed_type: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "added": self.added,
            "removed": self.removed,
            "changed_type": self.changed_type,
        }


def diff_schema(old: dict[str, Any], new: dict[str, Any], path: str = "") -> DiffResult:
    result = DiffResult()

    old_kind = old.get("kind")
    new_kind = new.get("kind")

    if old_kind != new_kind:
        result.changed_type.append(
            {"path": path or ".", "from": old_kind, "to": new_kind}
        )
    return result

    if old_kind == "object":
        old_children = old.get("children", {})
        new_children = new.get("children", {})

        for key in old_children:
            child_path = f"{path}.{key}" if path else key
            if key not in new_children:
                result.removed.append({"path": child_path, "type": old_children[key].get("kind")})
            else:
                child_diff = diff_schema(old_children[key], new_children[key], child_path)
                result.added.extend(child_diff.added)
                result.removed.extend(child_diff.removed)
                result.changed_type.extend(child_diff.changed_type)

        for key in new_children:
            if key not in old_children:
                child_path = f"{path}.{key}" if path else key
                result.added.append({"path": child_path, "type": new_children[key].get("kind")})

    elif old_kind == "array":
        old_item = old.get("item", {"kind": "unknown"})
        new_item = new.get("item", {"kind": "unknown"})
        item_diff = diff_schema(old_item, new_item, f"{path}[]")
        result.added.extend(item_diff.added)
        result.removed.extend(item_diff.removed)
        result.changed_type.extend(item_diff.changed_type)

    return result