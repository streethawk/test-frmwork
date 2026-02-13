from __future__ import annotations

from pathlib import Path

from framework.models import MappingRule

REQUIRED_COLUMNS = {
    "xpath",
    "sql mode",
    "target table",
    "column name",
    "node type",
    "transformation",
}


def _read_mapping_file(mapping_path: str, sheet_name: str | int = 0):
    import pandas as pd

    path = Path(mapping_path)
    suffix = path.suffix.lower()

    if suffix in {".csv", ".tsv"}:
        separator = "\t" if suffix == ".tsv" else ","
        return pd.read_csv(path, sep=separator)

    try:
        return pd.read_excel(path, sheet_name=sheet_name)
    except Exception:
        # Useful for `.xls` files that are actually delimiter-separated sample files.
        return pd.read_csv(path, sep=None, engine="python")


def load_mapping_rules(mapping_path: str, sheet_name: str | int = 0) -> list[MappingRule]:
    import pandas as pd

    frame = _read_mapping_file(mapping_path, sheet_name=sheet_name)
    normalized = {c.strip().lower() for c in frame.columns}
    missing = REQUIRED_COLUMNS.difference(normalized)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(f"Missing required mapping columns: {missing_cols}")

    rename_map = {c: c.strip().lower() for c in frame.columns}
    frame = frame.rename(columns=rename_map)

    rules: list[MappingRule] = []
    for row in frame.to_dict(orient="records"):
        rules.append(
            MappingRule(
                xpath=str(row["xpath"]).strip(),
                sql_mode=str(row["sql mode"]).strip().lower(),
                target_table=str(row["target table"]).strip().upper(),
                column_name=str(row["column name"]).strip().upper(),
                node_type=str(row["node type"]).strip().lower(),
                transformation=(
                    str(row["transformation"]).strip().lower()
                    if pd.notna(row.get("transformation")) and str(row.get("transformation")).strip()
                    else None
                ),
            )
        )
    return rules
