"""TEMPLATE - copy this file to add a new tool (e.g. `json_to_csv.py`).

Rules:
  * File name must NOT start with "_" (those are ignored by the registry).
  * Expose a module-level `TOOL = Tool(...)`.
  * `convert()` is a plain function: bytes in, ConversionResult out.
    Do not import streamlit here - that keeps it unit-testable.
That's it. No change needed in app.py.
"""
from __future__ import annotations

from pathlib import Path

from converter_hub.core.models import ConversionResult, Tool


def convert(data: bytes, filename: str) -> ConversionResult:
    text = data.decode("utf-8", errors="replace")
    return ConversionResult(
        data=text,
        filename=f"{Path(filename).stem}.txt",
        mime="text/plain",
        preview=text,
    )


TOOL = Tool(
    slug="my-new-tool",
    title="My New Tool",
    icon="🆕",
    description="One line about what this tool does.",
    file_types=("txt",),
    convert=convert,
    order=100,
)
