# XML to Oracle Test Framework (Option A)

This repository provides a Python-based test framework to validate an existing data pipeline that:

1. Reads XML files.
2. Applies Excel-defined mappings.
3. Writes/upserts to Oracle DB.

## Technology choices implemented

- `pytest` for test orchestration.
- `lxml` for XPath extraction from XML.
- `pandas` + `openpyxl` for mapping Excel parsing.
- `oracledb` for Oracle validation queries.

## Mapping schema expectations

The mapping Excel sheet must contain these columns:

- `xpath`
- `sql mode`
- `target table`
- `column name`
- `node type`
- `transformation`

## Project layout

- `framework/mapping_loader.py`: parse mapping rules.
- `framework/xml_reader.py`: XML parsing and XPath extraction.
- `framework/transformations.py`: transformation registry.
- `framework/expectation_builder.py`: derive expected DB values from XML + mapping.
- `framework/oracle_client.py`: Oracle query helper.
- `framework/assertions.py`: DB result assertions.
- `framework/pipeline_trigger.py`: executes pipeline command.
- `tests/test_e2e_template.py`: integration template (env-driven).

## Getting started

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pytest
```

## Running integration test template

Set variables then run integration marker:

```bash
export TEST_MAPPING_XLSX=/path/to/mapping.xlsx
export TEST_INPUT_XML=/path/to/input.xml
export PIPELINE_TRIGGER_CMD="/path/to/trigger --arg value"
export VERIFY_QUERY="SELECT * FROM CUSTOMER WHERE CUSTOMER_ID = '101'"
export ORACLE_USER=user
export ORACLE_PASSWORD=password
export ORACLE_DSN=host/service
pytest -m integration
```
