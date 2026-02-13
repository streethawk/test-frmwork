import pytest

pytest.importorskip("lxml")

from framework.expectation_builder import build_expected_assertions
from framework.models import MappingRule
from framework.xml_reader import read_xml


def test_build_expected_assertions_groups_by_table_and_mode(tmp_path):
    xml_file = tmp_path / "sample.xml"
    xml_file.write_text(
        """
        <root>
          <customer>
            <id> 101 </id>
            <name>alice</name>
          </customer>
        </root>
        """.strip(),
        encoding="utf-8",
    )

    rules = [
        MappingRule(
            xpath="/root/customer/id/text()",
            sql_mode="insert",
            target_table="CUSTOMER",
            column_name="CUSTOMER_ID",
            node_type="element",
            transformation="strip",
        ),
        MappingRule(
            xpath="/root/customer/name/text()",
            sql_mode="insert",
            target_table="CUSTOMER",
            column_name="CUSTOMER_NAME",
            node_type="element",
            transformation="upper",
        ),
    ]

    root = read_xml(str(xml_file))
    expected = build_expected_assertions(root, rules)

    assert len(expected) == 1
    entry = expected[0]
    assert entry.target_table == "CUSTOMER"
    assert entry.values == {"CUSTOMER_ID": "101", "CUSTOMER_NAME": "ALICE"}
