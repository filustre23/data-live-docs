* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# BigQuery audit logs overview

Cloud Audit Logs are a collection of logs provided by Google Cloud
that provide insight into operational concerns related to your use of
Google Cloud services. This page provides details about
BigQuery specific log information, and it demonstrates how
to use BigQuery to analyze logged activity. For more information, see
[Introduction to audit logs in BigQuery](/bigquery/docs/introduction-audit-workloads).

This document lists the audited methods for BigQuery. Google Cloud services
generate audit logs that record administrative and access activities within your Google Cloud resources.
For more information about Cloud Audit Logs, see the following:

* [Types of audit logs](/logging/docs/audit#types)
* [Audit log entry structure](/logging/docs/audit#audit_log_entry_structure)
* [Storing and routing audit logs](/logging/docs/audit#storing_and_routing_audit_logs)
* [Cloud Logging pricing summary](/stackdriver/pricing#logs-pricing-summary)
* [Enable Data Access audit logs](/logging/docs/audit/configure-data-access)

## Service name

To view the BigQuery audit logs, do the following:

1. In the Google Cloud console, go to the Logs Explorer page:

   [Go to Logs Explorer](https://console.cloud.google.com/logs/query)
2. Copy and paste the following query into the **Query** field of the
   Logs Explorer, and then click **Run query**.

   ```
       protoPayload.serviceName="bigquery.googleapis.com"
   ```

## Methods by permission type

Each IAM permission has a `type` property, whose value is an enum
that can be one of four values: `ADMIN_READ`, `ADMIN_WRITE`,
`DATA_READ`, or `DATA_WRITE`. When you call a method,
BigQuery generates an audit log whose category is dependent on the
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
| `ADMIN_WRITE` | `datasetservice.delete` `datasetservice.insert` `datasetservice.update` `google.cloud.bigquery.v2.DatasetService.DeleteDataset` `google.cloud.bigquery.v2.DatasetService.InsertDataset` `google.cloud.bigquery.v2.DatasetService.PatchDataset` `google.cloud.bigquery.v2.DatasetService.UndeleteDataset` `google.cloud.bigquery.v2.DatasetService.UpdateDataset` `google.cloud.bigquery.v2.JobService.CancelJob` `google.cloud.bigquery.v2.JobService.InsertJob` (LRO) `google.cloud.bigquery.v2.JobService.Query` (LRO) `google.cloud.bigquery.v2.RoutineService.DeleteRoutine` `google.cloud.bigquery.v2.RoutineService.InsertRoutine` `google.cloud.bigquery.v2.RowAccessPolicyService.BatchDeleteRowAccessPolicies` `google.cloud.bigquery.v2.RowAccessPolicyService.CreateRowAccessPolicy` `google.cloud.bigquery.v2.RowAccessPolicyService.DeleteRowAccessPolicy` `google.cloud.bigquery.v2.RowAccessPolicyService.UpdateRowAccessPolicy` `google.cloud.bigquery.v2.TableService.DeleteTable` `google.cloud.bigquery.v2.TableService.InsertTable` `google.cloud.bigquery.v2.TableService.PatchTable` `google.cloud.bigquery.v2.TableService.UpdateTable` `google.iam.v1.IAMPolicy.SetIamPolicy` `jobservice.getqueryresults` `jobservice.insert` `jobservice.query` `tabledataservice.list` `tableservice.delete` `tableservice.insert` `tableservice.update` |
| `DATA_READ` | `google.cloud.bigquery.v2.JobService.GetQueryResults` `google.cloud.bigquery.v2.TableDataService.List` |

## API interface audit logs

For information about how and which permissions are evaluated for each method,
see the Identity and Access Management documentation for BigQuery.

### `datasetservice`

The following audit logs are associated with methods belonging to
`datasetservice`.

#### `delete`

* **Method**: `datasetservice.delete`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.datasets.delete - ADMIN_WRITE`
  + `bigquery.models.delete - ADMIN_WRITE`
  + `bigquery.routines.delete - ADMIN_WRITE`
  + `bigquery.tables.delete - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="datasetservice.delete"`

#### `insert`

* **Method**: `datasetservice.insert`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.datasets.create - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="datasetservice.insert"`

#### `update`

* **Method**: `datasetservice.update`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.datasets.update - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="datasetservice.update"`

### `google.cloud.bigquery.v2.DatasetService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.v2.DatasetService`.

#### `DeleteDataset`

* **Method**: `google.cloud.bigquery.v2.DatasetService.DeleteDataset`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.datasets.delete - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.DatasetService.DeleteDataset"`

#### `InsertDataset`

* **Method**: `google.cloud.bigquery.v2.DatasetService.InsertDataset`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.datasets.create - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.DatasetService.InsertDataset"`

#### `PatchDataset`

* **Method**: `google.cloud.bigquery.v2.DatasetService.PatchDataset`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.datasets.update - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.DatasetService.PatchDataset"`

#### `UndeleteDataset`

* **Method**: `google.cloud.bigquery.v2.DatasetService.UndeleteDataset`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.datasets.create - ADMIN_WRITE`
  + `bigquery.datasets.get - ADMIN_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.DatasetService.UndeleteDataset"`

#### `UpdateDataset`

* **Method**: `google.cloud.bigquery.v2.DatasetService.UpdateDataset`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.datasets.update - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.DatasetService.UpdateDataset"`

### `google.cloud.bigquery.v2.JobService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.v2.JobService`.

#### `CancelJob`

* **Method**: `google.cloud.bigquery.v2.JobService.CancelJob`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquery.jobs.create - ADMIN_WRITE`
  + `bigquery.jobs.update - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.JobService.CancelJob"`

#### `DeleteJob`

* **Method**: `google.cloud.bigquery.v2.JobService.DeleteJob`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.JobService.DeleteJob"`

#### `GetQueryResults`

* **Method**: `google.cloud.bigquery.v2.JobService.GetQueryResults`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquery.tables.getData - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.JobService.GetQueryResults"`

#### `InsertJob`

* **Method**: `google.cloud.bigquery.v2.JobService.InsertJob`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquery.jobs.create - ADMIN_WRITE`
  + `bigquery.tables.getData - DATA_READ`
  + `bigquery.tables.updateData - DATA_WRITE`
* **Method is a long-running or streaming operation**:
  [**Long-running operation**](/logging/docs/audit/understanding-audit-logs#lro)
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.JobService.InsertJob"`

#### `Query`

* **Method**: `google.cloud.bigquery.v2.JobService.Query`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquery.jobs.create - ADMIN_WRITE`
  + `bigquery.tables.getData - DATA_READ`
* **Method is a long-running or streaming operation**:
  [**Long-running operation**](/logging/docs/audit/understanding-audit-logs#lro)
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.JobService.Query"`

### `google.cloud.bigquery.v2.ModelService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.v2.ModelService`.

#### `DeleteModel`

* **Method**: `google.cloud.bigquery.v2.ModelService.DeleteModel`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.ModelService.DeleteModel"`

#### `PatchModel`

* **Method**: `google.cloud.bigquery.v2.ModelService.PatchModel`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.ModelService.PatchModel"`

### `google.cloud.bigquery.v2.RoutineService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.v2.RoutineService`.

#### `DeleteRoutine`

* **Method**: `google.cloud.bigquery.v2.RoutineService.DeleteRoutine`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.routines.delete - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.RoutineService.DeleteRoutine"`

#### `InsertRoutine`

* **Method**: `google.cloud.bigquery.v2.RoutineService.InsertRoutine`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.routines.create - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.RoutineService.InsertRoutine"`

#### `UpdateRoutine`

* **Method**: `google.cloud.bigquery.v2.RoutineService.UpdateRoutine`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.RoutineService.UpdateRoutine"`

### `google.cloud.bigquery.v2.RowAccessPolicyService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.v2.RowAccessPolicyService`.

#### `BatchDeleteRowAccessPolicies`

* **Method**: `google.cloud.bigquery.v2.RowAccessPolicyService.BatchDeleteRowAccessPolicies`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.rowAccessPolicies.delete - ADMIN_WRITE`
  + `bigquery.rowAccessPolicies.setIamPolicy - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.RowAccessPolicyService.BatchDeleteRowAccessPolicies"`

#### `CreateRowAccessPolicy`

* **Method**: `google.cloud.bigquery.v2.RowAccessPolicyService.CreateRowAccessPolicy`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.rowAccessPolicies.create - ADMIN_WRITE`
  + `bigquery.rowAccessPolicies.setIamPolicy - ADMIN_WRITE`
  + `bigquery.tables.getData - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.RowAccessPolicyService.CreateRowAccessPolicy"`

#### `DeleteRowAccessPolicy`

* **Method**: `google.cloud.bigquery.v2.RowAccessPolicyService.DeleteRowAccessPolicy`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.rowAccessPolicies.delete - ADMIN_WRITE`
  + `bigquery.rowAccessPolicies.setIamPolicy - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.RowAccessPolicyService.DeleteRowAccessPolicy"`

#### `UpdateRowAccessPolicy`

* **Method**: `google.cloud.bigquery.v2.RowAccessPolicyService.UpdateRowAccessPolicy`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.rowAccessPolicies.setIamPolicy - ADMIN_WRITE`
  + `bigquery.rowAccessPolicies.update - ADMIN_WRITE`
  + `bigquery.tables.getData - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.RowAccessPolicyService.UpdateRowAccessPolicy"`

### `google.cloud.bigquery.v2.TableDataService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.v2.TableDataService`.

#### `List`

* **Method**: `google.cloud.bigquery.v2.TableDataService.List`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquery.tables.getData - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.TableDataService.List"`

### `google.cloud.bigquery.v2.TableService`

The following audit logs are associated with methods belonging to
`google.cloud.bigquery.v2.TableService`.

#### `DeleteTable`

* **Method**: `google.cloud.bigquery.v2.TableService.DeleteTable`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.tables.delete - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.TableService.DeleteTable"`

#### `InsertTable`

* **Method**: `google.cloud.bigquery.v2.TableService.InsertTable`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.tables.create - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.TableService.InsertTable"`

#### `PatchTable`

* **Method**: `google.cloud.bigquery.v2.TableService.PatchTable`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.tables.update - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.TableService.PatchTable"`

#### `UpdateTable`

* **Method**: `google.cloud.bigquery.v2.TableService.UpdateTable`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.tables.update - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.cloud.bigquery.v2.TableService.UpdateTable"`

### `google.iam.v1.IAMPolicy`

The following audit logs are associated with methods belonging to
`google.iam.v1.IAMPolicy`.

#### `SetIamPolicy`

* **Method**: `google.iam.v1.IAMPolicy.SetIamPolicy`
* **Audit log type**: [Admin activity](/logging/docs/audit#admin-activity)
* **Permissions**:
  + `bigquery.datasets.update - ADMIN_WRITE`
  + `bigquery.tables.setIamPolicy - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="google.iam.v1.IAMPolicy.SetIamPolicy"`

### `jobservice`

The following audit logs are associated with methods belonging to
`jobservice`.

#### `cancel`

* **Method**: `jobservice.cancel`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquery.jobs.create - ADMIN_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="jobservice.cancel"`

#### `getqueryresults`

* **Method**: `jobservice.getqueryresults`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquery.jobs.create - ADMIN_WRITE`
  + `bigquery.tables.getData - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="jobservice.getqueryresults"`

#### `insert`

* **Method**: `jobservice.insert`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquery.jobs.create - ADMIN_WRITE`
  + `bigquery.tables.create - ADMIN_WRITE`
  + `bigquery.tables.getData - DATA_READ`
  + `bigquery.tables.update - ADMIN_WRITE`
  + `bigquery.tables.updateData - DATA_WRITE`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="jobservice.insert"`

#### `jobcompleted`

* **Method**: `jobservice.jobcompleted`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="jobservice.jobcompleted"`

#### `query`

* **Method**: `jobservice.query`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquery.jobs.create - ADMIN_WRITE`
  + `bigquery.tables.getData - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="jobservice.query"`

### `tabledataservice`

The following audit logs are associated with methods belonging to
`tabledataservice`.

#### `list`

* **Method**: `tabledataservice.list`
* **Audit log type**: [Data access](/logging/docs/audit#data-access)
* **Permissions**:
  + `bigquery.jobs.create - ADMIN_WRITE`
  + `bigquery.tables.getData - DATA_READ`
* **Method is a long-running or streaming operation**:
  No.
* **Filter for this method**: `protoPayload.methodName="tabledataservice.list"`

### `tableservice`

The following audit logs are associated with methods belonging to
`tableservice`.

#### `delete</`