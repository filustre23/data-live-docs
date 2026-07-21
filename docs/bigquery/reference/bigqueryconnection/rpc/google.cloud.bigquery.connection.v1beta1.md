* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Package google.cloud.bigquery.connection.v1beta1 Stay organized with collections Save and categorize content based on your preferences.

## Index

* `ConnectionService` (interface)
* `CloudSqlCredential` (message)
* `CloudSqlProperties` (message)
* `CloudSqlProperties.DatabaseType` (enum)
* `Connection` (message)
* `ConnectionCredential` (message)
* `CreateConnectionRequest` (message)
* `DeleteConnectionRequest` (message)
* `GetConnectionRequest` (message)
* `ListConnectionsRequest` (message)
* `ListConnectionsResponse` (message)
* `UpdateConnectionCredentialRequest` (message)
* `UpdateConnectionRequest` (message)

## ConnectionService

Manages external data source connections and credentials.

| CreateConnection |
| --- |
| `rpc CreateConnection(CreateConnectionRequest) returns (Connection)`  Creates a new connection.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| DeleteConnection |
| --- |
| `rpc DeleteConnection(DeleteConnectionRequest) returns (Empty)`  Deletes connection and associated credential.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetConnection |
| --- |
| `rpc GetConnection(GetConnectionRequest) returns (Connection)`  Returns specified connection.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| GetIamPolicy |
| --- |
| `rpc GetIamPolicy(GetIamPolicyRequest) returns (Policy)`  Gets the access control policy for a resource. Returns an empty policy if the resource exists and does not have a policy set.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| ListConnections |
| --- |
| `rpc ListConnections(ListConnectionsRequest) returns (ListConnectionsResponse)`  Returns a list of connections in the given project.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| SetIamPolicy |
| --- |
| `rpc SetIamPolicy(SetIamPolicyRequest) returns (Policy)`  Sets the access control policy on the specified resource. Replaces any existing policy.  Can return `NOT_FOUND`, `INVALID_ARGUMENT`, and `PERMISSION_DENIED` errors.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| TestIamPermissions |
| --- |
| `rpc TestIamPermissions(TestIamPermissionsRequest) returns (TestIamPermissionsResponse)`  Returns permissions that a caller has on the specified resource. If the resource does not exist, this will return an empty set of permissions, not a `NOT_FOUND` error.  Note: This operation is designed to be used for building permission-aware UIs and command-line tools, not for authorization checking. This operation may "fail open" without warning.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| UpdateConnection |
| --- |
| `rpc UpdateConnection(UpdateConnectionRequest) returns (Connection)`  Updates the specified connection. For security reasons, also resets credential if connection properties are in the update field mask.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

| UpdateConnectionCredential |
| --- |
| `rpc UpdateConnectionCredential(UpdateConnectionCredentialRequest) returns (Empty)`  Sets the credential for the specified connection.  Authorization scopes  Requires one of the following OAuth scopes:   * `https://www.googleapis.com/auth/bigquery` * `https://www.googleapis.com/auth/cloud-platform`   For more information, see the [Authentication Overview](/docs/authentication#authorization-gcp). |

## CloudSqlCredential

Credential info for the Cloud SQL.

| Fields | |
| --- | --- |
| `username` | `string`  The username for the credential. |
| `password` | `string`  The password for the credential. |

## CloudSqlProperties

Connection properties specific to the Cloud SQL.

| Fields | |
| --- | --- |
| `instance_id` | `string`  Cloud SQL instance ID in the form `project:location:instance`. |
| `database` | `string`  Database name. |
| `type` | `DatabaseType`  Type of the Cloud SQL database. |
| `credential` | `CloudSqlCredential`  Input only. Cloud SQL credential. |
| `service_account_id` | `string`  Output only. The account ID of the service used for the purpose of this connection.  When the connection is used in the context of an operation in BigQuery, this service account will serve as the identity being used for connecting to the CloudSQL instance specified in this connection. |

## DatabaseType

Supported Cloud SQL database types.

| Enums | |
| --- | --- |
| `DATABASE_TYPE_UNSPECIFIED` | Unspecified database type. |
| `POSTGRES` | Cloud SQL for PostgreSQL. |
| `MYSQL` | Cloud SQL for MySQL. |

## Connection

Configuration parameters to establish connection with an external data source, except the credential attributes.

| Fields | |
| --- | --- |
| `name` | `string`  The resource name of the connection in the form of: `projects/{project_id}/locations/{location_id}/connections/{connection_id}` |
| `friendly_name` | `string`  User provided display name for the connection. |
| `description` | `string`  User provided description. |
| `creation_time` | `int64`  Output only. The creation timestamp of the connection. |
| `last_modified_time` | `int64`  Output only. The last update timestamp of the connection. |
| `has_credential` | `bool`  Output only. True, if credential is configured for this connection. |
| Union field `properties`. Properties specific to the underlying data source. `properties` can be only one of the following: | |
| `cloud_sql` | `CloudSqlProperties`  Cloud SQL properties. |

## ConnectionCredential

Credential to use with a connection.

| Fields | |
| --- | --- |
| Union field `credential`. Credential specific to the underlying data source. `credential` can be only one of the following: | |
| `cloud_sql` | `CloudSqlCredential`  Credential for Cloud SQL database. |

## CreateConnectionRequest

The request for `ConnectionService.CreateConnection`.

| Fields | |
| --- | --- |
| `parent` | `string`  Required. Parent resource name. Must be in the format `projects/{project_id}/locations/{location_id}`  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.connections.create` |
| `connection_id` | `string`  Optional. Connection id that should be assigned to the created connection. |
| `connection` | `Connection`  Required. Connection to create. |

## DeleteConnectionRequest

The request for [ConnectionService.DeleteConnectionRequest][].

| Fields | |
| --- | --- |
| `name` | `string`  Required. Name of the deleted connection, for example: `projects/{project_id}/locations/{location_id}/connections/{connection_id}`  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `name`:   * `bigquery.connections.delete` |

## GetConnectionRequest

The request for `ConnectionService.GetConnection`.

| Fields | |
| --- | --- |
| `name` | `string`  Required. Name of the requested connection, for example: `projects/{project_id}/locations/{location_id}/connections/{connection_id}`  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `name`:   * `bigquery.connections.get` |

## ListConnectionsRequest

The request for `ConnectionService.ListConnections`.

| Fields | |
| --- | --- |
| `parent` | `string`  Required. Parent resource name. Must be in the form: `projects/{project_id}/locations/{location_id}`  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `parent`:   * `bigquery.connections.list` |
| `max_results` | `UInt32Value`  Required. Maximum number of results per page. |
| `page_token` | `string`  Page token. |

## ListConnectionsResponse

The response for `ConnectionService.ListConnections`.

| Fields | |
| --- | --- |
| `next_page_token` | `string`  Next page token. |
| `connections[]` | `Connection`  List of connections. |

## UpdateConnectionCredentialRequest

The request for `ConnectionService.UpdateConnectionCredential`.

| Fields | |
| --- | --- |
| `name` | `string`  Required. Name of the connection, for example: `projects/{project_id}/locations/{location_id}/connections/{connection_id}/credential`  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `name`:   * `bigquery.connections.update` |
| `credential` | `ConnectionCredential`  Required. Credential to use with the connection. |

## UpdateConnectionRequest

The request for `ConnectionService.UpdateConnection`.

| Fields | |
| --- | --- |
| `name` | `string`  Required. Name of the connection to update, for example: `projects/{project_id}/locations/{location_id}/connections/{connection_id}`  Authorization requires the following [IAM](https://cloud.google.com/iam/docs/) permission on the specified resource `name`:   * `bigquery.connections.update` |
| `connection` | `Connection`  Required. Connection containing the updated fields. |
| `update_mask` | `FieldMask`  Required. Update mask for the connection fields to be updated. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]