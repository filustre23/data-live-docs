* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# BigQueryAuditMetadata.QueryStatementType Stay organized with collections Save and categorize content based on your preferences.

Type of the statement (e.g. SELECT, INSERT, CREATE\_TABLE, CREATE\_MODEL..)

| Enums | |
| --- | --- |
| `QUERY_STATEMENT_TYPE_UNSPECIFIED` | Unknown. |
| `SELECT` | SELECT ... FROM <Table list> ... |
| `ASSERT` | ASSERT <condition> AS 'description' |
| `INSERT` | INSERT INTO <Table> .... |
| `UPDATE` | UPDATE <Table> SET ... |
| `DELETE` | DELETE <Table> ... |
| `MERGE` | MERGE INTO <Table> .... |
| `TRUNCATE_TABLE` | TRUNCATE TABLE <Table> |
| `LOAD_DATA` | LOAD DATA {OVERWRITE|INTO} <Table> .... FROM FILES |
| `CREATE_TABLE` | CREATE TABLE <Table> <column list> |
| `CREATE_TABLE_AS_SELECT` | CREATE TABLE <Table> AS SELECT |
| `CREATE_VIEW` | CREATE VIEW <View> |
| `CREATE_MODEL` | CREATE MODEL <Model> AS <Query> |
| `CREATE_MATERIALIZED_VIEW` | CREATE MATERIALIZED VIEW <View> AS ... |
| `CREATE_APPROX_VIEW` | CREATE APPROX\_VIEW <View> AS ... |
| `CREATE_FUNCTION` | CREATE FUNCTION <Function>(<Signature>) AS ... |
| `CREATE_TABLE_FUNCTION` | CREATE TABLE FUNCTION <Function>(<Signature>) AS ... |
| `CREATE_PROCEDURE` | CREATE PROCEDURE <Procedure> |
| `CREATE_ROW_ACCESS_POLICY` | CREATE ROW ACCESS POLICY <RowAccessPolicy&gt ON <Table> |
| `CREATE_SCHEMA` | CREATE SCHEMA <Schema> |
| `CREATE_SNAPSHOT_TABLE` | CREATE SNAPSHOT TABLE <Snapshot&gt CLONE <Table> |
| `DROP_TABLE` | DROP TABLE <Table> |
| `DROP_EXTERNAL_TABLE` | DROP EXTERNAL TABLE <Table> |
| `DROP_VIEW` | DROP VIEW <View> |
| `DROP_MODEL` | DROP MODEL <Model> |
| `DROP_MATERIALIZED_VIEW` | DROP MATERIALIZED VIEW <View> |
| `DROP_APPROX_VIEW` | DROP APPROX\_VIEW <View> |
| `DROP_FUNCTION` | DROP FUNCTION <Function> |
| `DROP_PROCEDURE` | DROP PROCEDURE <Procedure> |
| `DROP_SCHEMA` | DROP SCHEMA <Schema> |
| `DROP_ROW_ACCESS_POLICY` | DROP ROW ACCESS POLICY <RowAccessPolicy&gt ON <Table>  DROP ALL ROW ACCESS POLICIES ON ON <Table> |
| `DROP_SNAPSHOT_TABLE` | DROP SNAPSHOT TABLE <Snapshot> |
| `ALTER_TABLE` | ALTER TABLE <Table> |
| `ALTER_VIEW` | ALTER VIEW <View> |
| `ALTER_MATERIALIZED_VIEW` | ALTER MATERIALIZED\_VIEW <view> |
| `ALTER_APPROX_VIEW` | ALTER APPROX\_VIEW <view> |
| `ALTER_SCHEMA` | ALTER SCHEMA <Schema> |
| `SCRIPT` | Script |
| `CREATE_EXTERNAL_TABLE` | CREATE EXTERNAL TABLE <TABLE> |
| `EXPORT_DATA` | EXPORT DATA; |
| `CALL` | CALL <stored procedure> |
| `ALTER_RECOMMENDATION` | ALTER RECOMMENDATION state |
| `ALTER_INSIGHT` | ALTER INSIGHT state |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-09-04 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-09-04 UTC."],[],[]]