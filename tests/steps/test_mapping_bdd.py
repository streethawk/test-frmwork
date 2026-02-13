from decimal import Decimal

import pytest

pytest_bdd = pytest.importorskip("pytest_bdd")
parsers = pytest_bdd.parsers
scenarios = pytest_bdd.scenarios

given = pytest_bdd.given
when = pytest_bdd.when
then = pytest_bdd.then

from framework.expectation_builder import build_expected_assertions
from framework.mapping_loader import load_mapping_rules
from framework.xml_reader import read_xml

scenarios("../features/mapping_assertions.feature")


@pytest.fixture
def context():
    return {}


@given(parsers.parse('the sample mapping file "{mapping_path}"'))
def given_mapping_file(context, mapping_path):
    context["mapping_path"] = mapping_path


@given(parsers.parse('the sample XML file "{xml_path}"'))
def given_xml_file(context, xml_path):
    context["xml_path"] = xml_path


@when("I build expected assertions from mapping and XML")
def when_build_expected(context):
    rules = load_mapping_rules(context["mapping_path"])
    root = read_xml(context["xml_path"])
    context["expected_assertions"] = build_expected_assertions(root, rules)


@then(parsers.parse('I should have an "{sql_mode}" assertion for table "{table}" with values'))
def then_have_assertion(context, sql_mode, table, datatable):
    expected_map = {
        row["column"].strip().upper(): row["value"].strip()
        for row in datatable
    }

    candidates = [
        item
        for item in context["expected_assertions"]
        if item.sql_mode == sql_mode and item.target_table == table
    ]
    assert candidates, f"No assertion found for mode={sql_mode} table={table}"

    target = candidates[0].values

    for column, expected_value in expected_map.items():
        actual = target.get(column)
        if isinstance(actual, Decimal):
            assert str(actual) == expected_value
        else:
            assert str(actual) == expected_value
