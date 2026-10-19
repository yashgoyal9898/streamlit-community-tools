"""Shared data models. No Streamlit imports here, so tools stay easy to test."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class ConversionResult:
    """What a tool returns for one uploaded file."""

    data: bytes | str          # content for the download button
    filename: str              # download file name
    mime: str                  # download mime type
    preview: str | None = None  # optional text shown in the preview box


# convert(file_bytes, original_filename) -> ConversionResult
Converter = Callable[[bytes, str], ConversionResult]


@dataclass(frozen=True)
class Tool:
    """Everything the app needs to know about one tool."""

    slug: str                  # unique, used in the URL (e.g. "zip-to-markdown")
    title: str                 # sidebar / page title
    icon: str                  # emoji
    description: str           # one-line help text
    file_types: tuple[str, ...]  # accepted extensions, e.g. ("zip",)
    convert: Converter
    order: int = 100           # lower = earlier in the sidebar
