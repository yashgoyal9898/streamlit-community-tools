"""Generic Streamlit UI shared by every tool (upload -> convert -> preview -> download)."""
from __future__ import annotations

from typing import Callable

import streamlit as st

from converter_hub.core.models import ConversionResult, Tool
from converter_hub.core.registry import get_tool

MAX_PREVIEW_CHARS = 100_000


@st.cache_data(show_spinner=False, max_entries=32)
def _convert_cached(slug: str, filename: str, data: bytes) -> ConversionResult:
    """Streamlit reruns the script on every click (e.g. download button).
    Caching avoids converting the same file again and again."""
    return get_tool(slug).convert(data, filename)


def render_tool_page(tool: Tool) -> None:
    st.title(f"{tool.icon} {tool.title}")
    st.caption(tool.description)

    uploaded_files = st.file_uploader(
        f"Upload {', '.join(t.upper() for t in tool.file_types)} files",
        type=list(tool.file_types),
        accept_multiple_files=True,
        key=f"upload_{tool.slug}",
    )

    if not uploaded_files:
        st.info("Upload one or more files to get started.")
        return

    st.write(f"Total files uploaded: {len(uploaded_files)}")

    for idx, uploaded in enumerate(uploaded_files):
        st.divider()
        st.subheader(f"{tool.icon} {uploaded.name}")

        try:
            with st.spinner("Converting..."):
                result = _convert_cached(tool.slug, uploaded.name, uploaded.getvalue())
        except Exception as exc:  # show per-file error, keep other files working
            st.error(f"Could not convert this file: {exc}")
            continue

        if result.preview is not None:
            preview = result.preview
            if len(preview) > MAX_PREVIEW_CHARS:
                preview = preview[:MAX_PREVIEW_CHARS]
                st.caption(
                    f"Preview truncated to {MAX_PREVIEW_CHARS:,} characters. "
                    "The download has the full content."
                )
            st.text_area(
                "Preview",
                preview,
                height=300,
                key=f"preview_{tool.slug}_{idx}",
            )

        st.download_button(
            label=f"Download {result.filename}",
            data=result.data,
            file_name=result.filename,
            mime=result.mime,
            key=f"download_{tool.slug}_{idx}",
        )


def make_tool_page(tool: Tool) -> Callable[[], None]:
    """Factory: st.Page needs a zero-argument function per tool."""

    def page() -> None:
        render_tool_page(tool)

    page.__name__ = f"page_{tool.slug.replace('-', '_')}"
    return page
