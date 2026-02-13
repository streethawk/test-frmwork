from __future__ import annotations

from framework.models import ExpectedAssertion


def assert_db_contains_expected(
    actual_rows: list[dict[str, object]],
    expected: ExpectedAssertion,
) -> None:
    if not actual_rows:
        raise AssertionError(f"No rows found for expected table {expected.target_table}")

    matches = []
    expected_keys = set(expected.values.keys())
    for row in actual_rows:
        comparable = {k: row.get(k) for k in expected_keys}
        if comparable == expected.values:
            matches.append(row)

    if not matches:
        raise AssertionError(
            f"No matching row found for table {expected.target_table}. "
            f"Expected subset={expected.values}, got rows={actual_rows}"
        )
