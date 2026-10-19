"""CSV -> Excel (.xlsx)."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path

import pandas as pd

from converter_hub.core.models import ConversionResult, Tool

XLSX_MIME = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"


def _read_csv(data: bytes) -> pd.DataFrame:
    try:
        return pd.read_csv(BytesIO(data), encoding="utf-8-sig")  # also strips BOM
    except UnicodeDecodeError:
        return pd.read_csv(BytesIO(data), encoding="latin1")


def csv_bytes_to_excel(data: bytes) -> bytes:
    df = _read_csv(data)
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Sheet1")
    return output.getvalue()


def convert(data: bytes, filename: str) -> ConversionResult:
    return ConversionResult(
        data=csv_bytes_to_excel(data),
        filename=f"{Path(filename).stem}.xlsx",
        mime=XLSX_MIME,
    )


TOOL = Tool(
    slug="csv-to-excel",
    title="CSV → Excel",
    icon="📄",
    description="Convert CSV files into Excel (.xlsx) workbooks.",
    file_types=("csv",),
    convert=convert,
    order=30,
)
