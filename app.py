"""Entry point:  uv run streamlit run app.py

Tools are auto-discovered from `converter_hub/tools/`. To add a tool you only
create a new file there - this file never changes."""
import streamlit as st

from converter_hub.core.registry import discover_tools
from converter_hub.core.ui import make_tool_page

st.set_page_config(page_title="Converter Hub", page_icon="🧰", layout="wide")


def build_navigation() -> st.navigation:
    tools = discover_tools()

    tool_pages = [
        st.Page(
            make_tool_page(tool),
            title=tool.title,
            icon=tool.icon,
            url_path=tool.slug,
        )
        for tool in tools
    ]

    def home() -> None:
        st.title("🧰 Converter Hub")
        st.write("Pick a tool from the sidebar or below.")
        for tool, page in zip(tools, tool_pages):
            with st.container(border=True):
                st.page_link(page, label=f"**{tool.title}**", icon=tool.icon)
                st.caption(tool.description)

    home_page = st.Page(home, title="Home", icon="🏠", url_path="home", default=True)
    return st.navigation([home_page, *tool_pages])


build_navigation().run()
