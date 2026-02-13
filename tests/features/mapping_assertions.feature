Feature: XML to mapping expectation assertions
  As a pipeline tester
  I want to build expected values from XML and mapping rules
  So that I can assert DB writes in a BDD style

  Scenario: Build expected values for insert and upsert mappings
    Given the sample mapping file "config/mappings.xls"
    And the sample XML file "testdata/xml/customer_insert.xml"
    When I build expected assertions from mapping and XML
    Then I should have an "insert" assertion for table "CUSTOMER" with values
      | column         | value         |
      | CUSTOMER_ID    | 101           |
      | CUSTOMER_NAME  | ALICE JOHNSON |
    And I should have an "upsert" assertion for table "CUSTOMER" with values
      | column          | value   |
      | CUSTOMER_STATUS | ACTIVE  |
      | CREDIT_LIMIT    | 1000.50 |
