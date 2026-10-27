"""Entry point:  uv run streamlit run app.py

Tools are auto-discovered from `converter_hub/tools/`. To add a tool you only
create a new file there - this file never changes."""
import streamlit as st

from converter_hub.core.registry import discover_tools
from converter_hub.core.ui import make_tool_page

DEFAULT_TOOL_SLUG = "zip-to-markdown"  # this page opens first

st.set_page_config(page_title="Community Tools", page_icon="🧰", layout="wide")


def build_navigation() -> st.navigation:
    tools = discover_tools()

    tool_pages = [
        st.Page(
            make_tool_page(tool),
            title=tool.title,
            icon=tool.icon,
            url_path=tool.slug,
            default=(tool.slug == DEFAULT_TOOL_SLUG),
        )
        for tool in tools
    ]

    return st.navigation(tool_pages)


build_navigation().run()