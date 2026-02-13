from __future__ import annotations

from collections import defaultdict

from framework.models import ExpectedAssertion, MappingRule
from framework.transformations import apply_transformation
from framework.xml_reader import extract_xpath_value


def build_expected_assertions(root, rules: list[MappingRule]) -> list[ExpectedAssertion]:
    grouped_values: dict[tuple[str, str], dict[str, object]] = defaultdict(dict)

    for rule in rules:
        raw_value = extract_xpath_value(root, rule.xpath)
        if raw_value is None:
            continue
        value = apply_transformation(raw_value, rule.transformation)
        grouped_values[(rule.target_table, rule.sql_mode)][rule.column_name] = value

    assertions: list[ExpectedAssertion] = []
    for (table, mode), values in grouped_values.items():
        assertions.append(ExpectedAssertion(target_table=table, sql_mode=mode, values=values))
    return assertions
