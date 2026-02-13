import pytest

pd = pytest.importorskip("pandas")

from framework.mapping_loader import load_mapping_rules


def test_load_mapping_rules_happy_path(tmp_path):
    mapping_file = tmp_path / "mapping.xlsx"
    frame = pd.DataFrame(
        [
            {
                "xpath": "/root/customer/id/text()",
                "sql mode": "INSERT",
                "target table": "customer",
                "column name": "customer_id",
                "node type": "attribute",
                "transformation": "strip",
            }
        ]
    )
    frame.to_excel(mapping_file, index=False)

    rules = load_mapping_rules(str(mapping_file))

    assert len(rules) == 1
    assert rules[0].sql_mode == "insert"
    assert rules[0].target_table == "CUSTOMER"
    assert rules[0].column_name == "CUSTOMER_ID"
    assert rules[0].transformation == "strip"


def test_load_mapping_rules_missing_columns(tmp_path):
    mapping_file = tmp_path / "mapping.xlsx"
    pd.DataFrame([{"xpath": "/a"}]).to_excel(mapping_file, index=False)

    with pytest.raises(ValueError, match="Missing required mapping columns"):
        load_mapping_rules(str(mapping_file))
