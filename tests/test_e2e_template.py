import os

import pytest

from framework.assertions import assert_db_contains_expected
from framework.expectation_builder import build_expected_assertions
from framework.mapping_loader import load_mapping_rules
from framework.oracle_client import OracleClient
from framework.pipeline_trigger import run_pipeline
from framework.xml_reader import read_xml


@pytest.mark.integration
def test_pipeline_to_oracle_contract():
    """Template integration test. Configure env vars and command to enable."""
    mapping_path = os.getenv("TEST_MAPPING_FILE") or os.getenv("TEST_MAPPING_XLSX")
    xml_path = os.getenv("TEST_INPUT_XML")
    trigger = os.getenv("PIPELINE_TRIGGER_CMD")
    verify_query = os.getenv("VERIFY_QUERY")

    if not all([mapping_path, xml_path, trigger, verify_query]):
        pytest.skip("Integration env vars are not configured (TEST_MAPPING_FILE/TEST_MAPPING_XLSX, TEST_INPUT_XML, PIPELINE_TRIGGER_CMD, VERIFY_QUERY)")

    rules = load_mapping_rules(mapping_path)
    root = read_xml(xml_path)
    expected_rows = build_expected_assertions(root, rules)

    run_pipeline(trigger.split(" "))

    client = OracleClient(
        user=os.environ["ORACLE_USER"],
        password=os.environ["ORACLE_PASSWORD"],
        dsn=os.environ["ORACLE_DSN"],
    )
    actual_rows = client.fetch_rows(verify_query)

    for expected in expected_rows:
        assert_db_contains_expected(actual_rows, expected)
