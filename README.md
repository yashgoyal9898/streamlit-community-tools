# 🧰 Converter Hub

One Streamlit app, many small converters. Tools are auto-discovered, so adding a new one means adding **one file**.

| Tool | Input | Output |
|---|---|---|
| ZIP → Markdown | `.zip` | `.md` |
| Excel → Markdown | `.xlsx` | `.md` |
| CSV → Excel | `.csv` | `.xlsx` |

## Run locally (uv)

```bash
uv sync                      # creates .venv and installs dependencies
uv run pytest                # optional: run tests
uv run streamlit run app.py  # opens http://localhost:8501
```

## Project structure

```
converter-hub/
├── app.py                      # entry point (never needs editing)
├── pyproject.toml / uv.lock    # dependencies
├── .streamlit/config.toml
├── converter_hub/
│   ├── core/
│   │   ├── models.py           # Tool + ConversionResult dataclasses
│   │   ├── registry.py         # auto-discovers tools/*.py
│   │   └── ui.py               # shared upload -> convert -> preview -> download UI
│   └── tools/
│       ├── _template.py        # copy this to make a new tool
│       ├── zip_to_markdown.py
│       ├── excel_to_markdown.py
│       └── csv_to_excel.py
└── tests/
```

## Add a new tool

1. Copy `converter_hub/tools/_template.py` to e.g. `converter_hub/tools/json_to_csv.py`.
2. Write `convert(data: bytes, filename: str) -> ConversionResult` and fill in `TOOL = Tool(...)` (unique `slug`).
3. Add any new library with `uv add <package>`.
4. `uv run streamlit run app.py` - it shows up in the sidebar automatically.

## Deploy on Streamlit Community Cloud

1. Push this folder to a GitHub repo (commit `uv.lock` too).
2. Go to <https://share.streamlit.io> -> **Create app** -> pick the repo and branch.
3. **Main file path:** `app.py`
4. *Advanced settings* -> choose Python 3.12 (or newer) -> **Deploy**.
