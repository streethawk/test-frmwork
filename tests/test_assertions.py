import pytest

from framework.assertions import assert_db_contains_expected
from framework.models import ExpectedAssertion


def test_assert_db_contains_expected_passes_on_subset_match():
    actual = [{"CUSTOMER_ID": "101", "CUSTOMER_NAME": "ALICE", "STATUS": "A"}]
    expected = ExpectedAssertion(
        target_table="CUSTOMER",
        sql_mode="insert",
        values={"CUSTOMER_ID": "101", "CUSTOMER_NAME": "ALICE"},
    )

    assert_db_contains_expected(actual, expected)


def test_assert_db_contains_expected_raises_on_mismatch():
    actual = [{"CUSTOMER_ID": "101", "CUSTOMER_NAME": "BOB"}]
    expected = ExpectedAssertion(
        target_table="CUSTOMER",
        sql_mode="insert",
        values={"CUSTOMER_ID": "101", "CUSTOMER_NAME": "ALICE"},
    )

    with pytest.raises(AssertionError):
        assert_db_contains_expected(actual, expected)
