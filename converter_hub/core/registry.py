"""Auto-discovers tools: every module in `converter_hub/tools/` that exposes a
`TOOL = Tool(...)` object is registered. Files starting with `_` are ignored."""
from __future__ import annotations

import importlib
import pkgutil
from functools import lru_cache

from converter_hub import tools as tools_pkg
from converter_hub.core.models import Tool


@lru_cache(maxsize=1)
def discover_tools() -> tuple[Tool, ...]:
    found: list[Tool] = []

    for module_info in pkgutil.iter_modules(tools_pkg.__path__):
        if module_info.name.startswith("_"):
            continue
        module = importlib.import_module(f"{tools_pkg.__name__}.{module_info.name}")
        tool = getattr(module, "TOOL", None)
        if isinstance(tool, Tool):
            found.append(tool)

    slugs = [t.slug for t in found]
    duplicates = {s for s in slugs if slugs.count(s) > 1}
    if duplicates:
        raise ValueError(f"Duplicate tool slugs: {sorted(duplicates)}")

    return tuple(sorted(found, key=lambda t: (t.order, t.title)))


def get_tool(slug: str) -> Tool:
    for tool in discover_tools():
        if tool.slug == slug:
            return tool
    raise KeyError(f"Unknown tool: {slug}")
