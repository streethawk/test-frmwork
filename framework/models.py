from dataclasses import dataclass


@dataclass(frozen=True)
class MappingRule:
    xpath: str
    sql_mode: str
    target_table: str
    column_name: str
    node_type: str
    transformation: str | None = None


@dataclass(frozen=True)
class ExpectedAssertion:
    target_table: str
    sql_mode: str
    values: dict[str, object]
