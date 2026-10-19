"""ZIP -> Markdown: dumps every text file of a ZIP into one Markdown document."""
from __future__ import annotations

import zipfile
from io import BytesIO
from pathlib import Path, PurePosixPath

from converter_hub.core.models import ConversionResult, Tool

MAX_FILE_BYTES = 2 * 1024 * 1024  # skip single files bigger than 2 MB
IGNORED_PARTS = {"__MACOSX", ".git", "__pycache__", "node_modules", ".venv", ".DS_Store"}


def _is_ignored(name: str) -> bool:
    return any(part in IGNORED_PARTS for part in PurePosixPath(name).parts)


def _is_binary(content: bytes) -> bool:
    return b"\x00" in content[:8192]


def _safe_decode(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1")


def _detect_language(file_path: str) -> str:
    return Path(file_path).suffix.lstrip(".")


def _fence_for(text: str) -> str:
    """Use a fence longer than any backtick run inside the file, so files that
    themselves contain ``` (e.g. README.md) do not break the Markdown."""
    longest = run = 0
    for ch in text:
        run = run + 1 if ch == "`" else 0
        longest = max(longest, run)
    return "`" * max(3, longest + 1)


def zip_bytes_to_markdown(data: bytes) -> str:
    parts: list[str] = ["# ZIP Content Dump\n\n"]

    try:
        archive = zipfile.ZipFile(BytesIO(data), "r")
    except zipfile.BadZipFile as exc:
        raise ValueError("This is not a valid ZIP file.") from exc

    with archive:
        for info in archive.infolist():
            if info.is_dir() or _is_ignored(info.filename):
                continue

            parts.append("\n---\n")
            parts.append(f"## 📄 {info.filename}\n")

            if info.file_size > MAX_FILE_BYTES:
                parts.append(f"`Skipped: file is larger than {MAX_FILE_BYTES // 1024 // 1024} MB`\n")
                continue

            try:
                content = archive.read(info)
            except Exception as exc:
                parts.append(f"`Error reading file: {exc}`\n")
                continue

            if _is_binary(content):
                parts.append("`Skipped: binary file`\n")
                continue

            text = _safe_decode(content)
            fence = _fence_for(text)
            lang = _detect_language(info.filename)
            parts.append(f"{fence}{lang}\n{text}\n{fence}\n")

    return "".join(parts)


def convert(data: bytes, filename: str) -> ConversionResult:
    markdown = zip_bytes_to_markdown(data)
    return ConversionResult(
        data=markdown,
        filename=f"{Path(filename).stem}.md",
        mime="text/markdown",
        preview=markdown,
    )


TOOL = Tool(
    slug="zip-to-markdown",
    title="ZIP → Markdown",
    icon="📦",
    description="Dump all text files inside a ZIP into a single Markdown file.",
    file_types=("zip",),
    convert=convert,
    order=10,
)
