from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int) and not isinstance(value, bool):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return "string"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return "unknown"


@dataclass
class SchemaNode:
    kind: str
    children: dict[str, "SchemaNode"] = field(default_factory=dict)
    item: SchemaNode | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {"kind": self.kind}
        if self.children:
            data["children"] = {k: v.to_dict() for k, v in self.children.items()}
        if self.item is not None:
            data["item"] = self.item.to_dict()
        return data


def infer_schema(value: Any) -> SchemaNode:
    kind = type_name(value)

    if isinstance(value, dict):
        children = {key: infer_schema(child) for key, child in value.items()}
        return SchemaNode(kind="object", children=children)

    if isinstance(value, list):
        if not value:
            return SchemaNode(kind="array", item=SchemaNode(kind="unknown"))
        return SchemaNode(kind="array", item=infer_schema(value[0]))

    return SchemaNode(kind=kind)
