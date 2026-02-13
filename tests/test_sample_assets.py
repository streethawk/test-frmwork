from pathlib import Path


def test_sample_mapping_file_exists_with_expected_headers():
    mapping_file = Path("config/mappings.xls")
    assert mapping_file.exists()
    header = mapping_file.read_text(encoding="utf-8").splitlines()[0]
    assert header == "xpath,sql mode,target table,column name,node type,transformation"


def test_sample_xml_files_exist():
    assert Path("testdata/xml/customer_insert.xml").exists()
    assert Path("testdata/xml/customer_upsert.xml").exists()
