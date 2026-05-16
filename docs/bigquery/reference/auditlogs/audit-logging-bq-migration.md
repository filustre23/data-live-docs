* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Guides](https://docs.cloud.google.com/bigquery/docs/introduction)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# BigQuery Migration Service audit logging

This document describes audit logging for BigQuery Migration Service. Google Cloud services
generate audit logs that record administrative and access activities within your Google Cloud resources.
For more information about Cloud Audit Logs, see the following:

* [Types of audit logs](/logging/docs/audit#types)
* [Audit log entry structure](/logging/docs/audit#audit_log_entry_structure)
* [Storing and routing audit logs](/logging/docs/audit#storing_and_routing_audit_logs)
* [Cloud Logging pricing summary](/stackdriver/pricing#logs-pricing-summary)
* [Enable Data Access audit logs](/logging/docs/audit/configure-data-access)

## Service name

BigQuery Migration Service audit logs use the service name `bigquerymigration.googleapis.com`.
Filter for this service:

```
    protoPayload.serviceName="bigquerymigration.googleapis.com"
```

## Methods by permission type

Each IAM permission has a `type` property, whose value is an enum
that can be one of four values: `ADMIN_READ`, `ADMIN_WRITE`,
`DATA_READ`, or `DATA_WRITE`. When you call a method,
BigQuery Migration Service generates an audit log whose category is dependent on the
`type` property of the permission required to perform the method.
Methods that require an IAM permission with the `type` property value
of `DATA_READ`, `DATA_WRITE`, or `ADMIN_READ` generate
[Data Access](/logging/docs/audit#data-access) audit logs.
Methods that require an IAM permission with the `type` property value
of `ADMIN_WRITE` generate
[Admin Activity](/logging/docs/audit#admin-activity) audit logs.

API methods in the following list that are marked with (LRO) are long-running operations (LROs).
These methods usually generate two audit log entries: one when the operation starts and
another when it ends. For more information see [Audit logs for long-running operations](/logging/docs/audit/understanding-audit-logs#lro).

| Permission type | Methods |
| --- | --- |
| `DATA_READ` | `google.cloud.bigquery.migration.v2.MigrationService.GetMigrationSubtask` `google.cloud.bigquery.migration.v2.MigrationService.GetMigrationWorkflow` `google.cloud.bigquery.migration.v2.MigrationService.ListMigrationSubtasks` `google.cloud.bigquery.migration.v2.MigrationService.ListMigrationWorkflows` `google.cloud.bigquery.migration.v2.SqlTranslationService.TranslateQuery` `google.cloud.bigquery.migration.v2alpha.MigrationService.GetMigrationSubtask` `google.cloud.bigquery.migration.v2alpha.MigrationService.GetMigrationWorkflow` `google.cloud.bigquery.migration.v2alpha.MigrationService.ListMigrationSubtasks` `google.cloud.bigquery.migration.v2alpha.MigrationService.ListMigrationWorkflows` `google.cloud.bigquery.migration.v2alpha.SqlTranslationService.TranslateQuery` |
| `DATA_WRITE` | `google.cloud.bigquery.migration.v2.MigrationService.CreateMigrationWorkflow` `google.cloud.bigquery.migration.v2.MigrationService.DeleteMigrationWorkflow` `google.cloud.bigquery.migration.v2.MigrationService.StartMigrationWorkflow` `google.cloud.bigquery.migration.v2alpha.MigrationService.CreateMigrationWorkflow` `google.cloud.bigquery.migration.v2alpha.MigrationService.DeleteMigrationWorkflow` `google.cloud.bigquery.migration.v2alpha.MigrationService.StartMigrationWorkflow` |

## API interface audit logs

For information about how and which permissions are evaluated for each method,
see the Identity and Access Management documentation for BigQuery Migration Service.

### `google.cloud.bigquery.migration.v2.MigrationService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.migration.v2.MigrationService`.

#### `CreateMigrationWorkflow`

* **Method**: `google.cloud.bigquery.migration.v2.MigrationService.CreateMigrationWorkflow`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.workflows.create - DATA_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2.MigrationService.CreateMigrationWorkflow"`

#### `DeleteMigrationWorkflow`

* **Method**: `google.cloud.bigquery.migration.v2.MigrationService.DeleteMigrationWorkflow`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.workflows.delete - DATA_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2.MigrationService.DeleteMigrationWorkflow"`

#### `GetMigrationSubtask`

* **Method**: `google.cloud.bigquery.migration.v2.MigrationService.GetMigrationSubtask`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.subtasks.get - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2.MigrationService.GetMigrationSubtask"`

#### `GetMigrationWorkflow`

* **Method**: `google.cloud.bigquery.migration.v2.MigrationService.GetMigrationWorkflow`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.workflows.get - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2.MigrationService.GetMigrationWorkflow"`

#### `ListMigrationSubtasks`

* **Method**: `google.cloud.bigquery.migration.v2.MigrationService.ListMigrationSubtasks`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.subtasks.list - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2.MigrationService.ListMigrationSubtasks"`

#### `ListMigrationWorkflows`

* **Method**: `google.cloud.bigquery.migration.v2.MigrationService.ListMigrationWorkflows`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.workflows.list - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2.MigrationService.ListMigrationWorkflows"`

#### `StartMigrationWorkflow`

* **Method**: `google.cloud.bigquery.migration.v2.MigrationService.StartMigrationWorkflow`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.workflows.update - DATA_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2.MigrationService.StartMigrationWorkflow"`

### `google.cloud.bigquery.migration.v2.SqlTranslationService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.migration.v2.SqlTranslationService`.

#### `TranslateQuery`

* **Method**: `google.cloud.bigquery.migration.v2.SqlTranslationService.TranslateQuery`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.translation.translate - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2.SqlTranslationService.TranslateQuery"`

### `google.cloud.bigquery.migration.v2alpha.MigrationService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.migration.v2alpha.MigrationService`.

#### `CreateMigrationWorkflow`

* **Method**: `google.cloud.bigquery.migration.v2alpha.MigrationService.CreateMigrationWorkflow`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.workflows.create - DATA_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2alpha.MigrationService.CreateMigrationWorkflow"`

#### `DeleteMigrationWorkflow`

* **Method**: `google.cloud.bigquery.migration.v2alpha.MigrationService.DeleteMigrationWorkflow`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.workflows.delete - DATA_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2alpha.MigrationService.DeleteMigrationWorkflow"`

#### `GetMigrationSubtask`

* **Method**: `google.cloud.bigquery.migration.v2alpha.MigrationService.GetMigrationSubtask`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.subtasks.get - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2alpha.MigrationService.GetMigrationSubtask"`

#### `GetMigrationWorkflow`

* **Method**: `google.cloud.bigquery.migration.v2alpha.MigrationService.GetMigrationWorkflow`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.workflows.get - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2alpha.MigrationService.GetMigrationWorkflow"`

#### `ListMigrationSubtasks`

* **Method**: `google.cloud.bigquery.migration.v2alpha.MigrationService.ListMigrationSubtasks`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.subtasks.list - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2alpha.MigrationService.ListMigrationSubtasks"`

#### `ListMigrationWorkflows`

* **Method**: `google.cloud.bigquery.migration.v2alpha.MigrationService.ListMigrationWorkflows`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.workflows.list - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2alpha.MigrationService.ListMigrationWorkflows"`

#### `StartMigrationWorkflow`

* **Method**: `google.cloud.bigquery.migration.v2alpha.MigrationService.StartMigrationWorkflow`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.workflows.update - DATA_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2alpha.MigrationService.StartMigrationWorkflow"`

### `google.cloud.bigquery.migration.v2alpha.SqlTranslationService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.migration.v2alpha.SqlTranslationService`.

#### `TranslateQuery`

* **Method**: `google.cloud.bigquery.migration.v2alpha.SqlTranslationService.TranslateQuery`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquerymigration.translation.translate - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.migration.v2alpha.SqlTranslationService.TranslateQuery"`




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-15 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-15 UTC."],[],[]]