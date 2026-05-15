* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Package google.cloud.bigquery.connection.v1 Stay organized with collections Save and categorize content based on your preferences.

## Index

* `ConnectionService` (interface)
* `AwsAccessRole` (message)
* `AwsProperties` (message)
* `AzureProperties` (message)
* `CloudResourceProperties` (message)
* `CloudSpannerProperties` (message)
* `CloudSqlCredential` (message)
* `CloudSqlProperties` (message)
* `CloudSqlProperties.DatabaseType` (enum)
* `Connection` (message)
* `ConnectorConfiguration` (message)
* `ConnectorConfiguration.Asset` (message)
* `ConnectorConfiguration.Authentication` (message)
* `ConnectorConfiguration.Endpoint` (message)
* `ConnectorConfiguration.Network` (message)
* `ConnectorConfiguration.PrivateServiceConnect` (message)
* `ConnectorConfiguration.Secret` (message)
* `ConnectorConfiguration.Secret.SecretType` (enum)
* `ConnectorConfiguration.UsernamePassword` (message)
* `CreateConnectionRequest` (message)
* `DeleteConnectionRequest` (message)
* `GetConnectionRequest` (message)
* `ListConnectionsRequest` (message)
* `ListConnectionsResponse` (message)
* `MetastoreServiceConfig` (message)
* `SalesforceDataCloudProperties` (message)
* `SparkHistoryServerConfig` (message)
* `SparkProperties` (message)
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

## AwsAccessRole

Authentication method for Amazon Web Services (AWS) that uses Google owned Google service account to assume into customer's AWS IAM Role.

| Fields | |
| --- | --- |
| `iam_role_id` | `string`  The user’s AWS IAM Role that trusts the Google-owned AWS IAM user Connection. |
| `identity` | `string`  A unique Google-owned and Google-generated identity for the Connection. This identity will be used to access the user's AWS IAM Role. |

## AwsProperties

Connection properties specific to Amazon Web Services (AWS).

| Fields | |
| --- | --- |
| Union field `authentication_method`. Authentication method chosen at connection creation. `authentication_method` can be only one of the following: | |
| `access_role` | `AwsAccessRole`  Authentication using Google owned service account to assume into customer's AWS IAM Role. |

## AzureProperties

Container for connection properties specific to Azure.

| Fields | |
| --- | --- |
| `application` | `string`  Output only. The name of the Azure Active Directory Application. |
| `client_id` | `string`  Output only. The client id of the Azure Active Directory Application. |
| `object_id` | `string`  Output only. The object id of the Azure Active Directory Application. |
| `customer_tenant_id` | `string`  The id of customer's directory that host the data. |
| `redirect_uri` | `string`  The URL user will be redirected to after granting consent during connection setup. |
| `federated_application_client_id` | `string`  The client ID of the user's Azure Active Directory Application used for a federated connection. |
| `identity` | `string`  Output only. A unique Google-owned and Google-generated identity for the Connection. This identity will be used to access the user's Azure Active Directory Application. |

## CloudResourceProperties

Container for connection properties for delegation of access to GCP resources.

| Fields | |
| --- | --- |
| `service_account_id` | `string`  Output only. The account ID of the service created for the purpose of this connection.  The service account does not have any permissions associated with it when it is created. After creation, customers delegate permissions to the service account. When the connection is used in the context of an operation in BigQuery, the service account will be used to connect to the desired resources in GCP.  The account ID is in the form of: @gcp-sa-bigquery-cloudresource.iam.gserviceaccount.com |

## CloudSpannerProperties

Connection properties specific to Cloud Spanner.

| Fields | |
| --- | --- |
| `database` | `string`  Cloud Spanner database in the form `project/instance/database' |
| `use_parallelism` | `bool`  If parallelism should be used when reading from Cloud Spanner |
| `max_parallelism` | `int32`  Allows setting max parallelism per query when executing on Spanner independent compute resources. If unspecified, default values of parallelism are chosen that are dependent on the Cloud Spanner instance configuration.  REQUIRES: `use_parallelism` must be set.  REQUIRES: `use_data_boost` must be set. |
| `use_data_boost` | `bool`  If set, the request will be executed via Spanner independent compute resources.  REQUIRES: `use_parallelism` must be set. |
| `database_role` | `string`  Optional. Cloud Spanner database role for fine-grained access control. The Cloud Spanner admin should have provisioned the database role with appropriate permissions, such as `SELECT` and `INSERT`. Other users should only use roles provided by their Cloud Spanner admins.  For more details, see [About fine-grained access control](https://cloud.google.com/spanner/docs/fgac-about).  REQUIRES: The database role name must start with a letter, and can only contain letters, numbers, and underscores. |

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
| `name` | `string`  Output only. The resource name of the connection in the form of: `projects/{project_id}/locations/{location_id}/connections/{connection_id}` |
| `friendly_name` | `string`  User provided display name for the connection. |
| `description` | `string`  User provided description. |
| `configuration` | `ConnectorConfiguration`  Optional. Connector configuration. |
| `creation_time` | `int64`  Output only. The creation timestamp of the connection. |
| `last_modified_time` | `int64`  Output only. The last update timestamp of the connection. |
| `has_credential` | `bool`  Output only. True, if credential is configured for this connection. |
| `kms_key_name` | `string`  Optional. The Cloud KMS key that is used for credentials encryption.  If omitted, internal Google owned encryption keys are used.  Example: `projects/[kms_project_id]/locations/[region]/keyRings/[key_region]/cryptoKeys/[key]` |
| Union field `properties`. Properties specific to the underlying data source. `properties` can be only one of the following: | |
| `cloud_sql` | `CloudSqlProperties`  Cloud SQL properties. |
| `aws` | `AwsProperties`  Amazon Web Services (AWS) properties. |
| `azure` | `AzureProperties`  Azure properties. |
| `cloud_spanner` | `CloudSpannerProperties`  Cloud Spanner properties. |
| `cloud_resource` | `CloudResourceProperties`  Cloud Resource properties. |
| `spark` | `SparkProperties`  Spark properties. |
| `salesforce_data_cloud` | `SalesforceDataCloudProperties`  Optional. Salesforce DataCloud properties. This field is intended for use only by Salesforce partner projects. This field contains properties for your Salesforce DataCloud connection. |

## ConnectorConfiguration

Represents concrete parameter values for Connector Configuration.

| Fields | |
| --- | --- |
| `connector_id` | `string`  Required. Immutable. The ID of the Connector these parameters are configured for. |
| `endpoint` | `Endpoint`  Specifies how to reach the remote system this connection is pointing to. |
| `authentication` | `Authentication`  Client authentication. |
| `network` | `Network`  Networking configuration. |
| `asset` | `Asset`  Data asset. |

## Asset

Data Asset - a resource within instance of the system, reachable under specified endpoint. For example a database name in a SQL DB.

| Fields | |
| --- | --- |
| `database` | `string`  Name of the database. |
| `google_cloud_resource` | `string`  Full Google Cloud resource name - <https://cloud.google.com/apis/design/resource_names#full_resource_name>. Example: `//library.googleapis.com/shelves/shelf1/books/book2` |

## Authentication

Client authentication.

| Fields | |
| --- | --- |
| `username_password` | `UsernamePassword`  Username/password authentication. |
| `service_account` | `string`  Output only. Google-managed service account associated with this connection, e.g., `service-{project_number}@gcp-sa-bigqueryconnection.iam.gserviceaccount.com`. BigQuery jobs using this connection will act as `service_account` identity while connecting to the datasource. |

## Endpoint

Remote endpoint specification.

| Fields | |
| --- | --- |
| Union field `endpoint`.  `endpoint` can be only one of the following: | |
| `host_port` | `string`  Host and port in a format of `hostname:port` as defined in <https://www.ietf.org/rfc/rfc3986.html#section-3.2.2> and <https://www.ietf.org/rfc/rfc3986.html#section-3.2.3>. |

## Network

Network related configuration.

| Fields | |
| --- | --- |
| Union field `network`.  `network` can be only one of the following: | |
| `private_service_connect` | `PrivateServiceConnect`  Private Service Connect networking configuration. |

## PrivateServiceConnect

Private Service Connect configuration.

| Fields | |
| --- | --- |
| `network_attachment` | `string`  Required. Network Attachment name in the format of `projects/{project}/regions/{region}/networkAttachments/{networkattachment}`. |

## Secret

Secret value parameter.