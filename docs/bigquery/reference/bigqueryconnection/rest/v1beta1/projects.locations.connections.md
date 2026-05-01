* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# REST Resource: projects.locations.connections Stay organized with collections Save and categorize content based on your preferences.

* [Resource: Connection](#Connection)
  + [JSON representation](#Connection.SCHEMA_REPRESENTATION)
* [CloudSqlProperties](#CloudSqlProperties)
  + [JSON representation](#CloudSqlProperties.SCHEMA_REPRESENTATION)
* [DatabaseType](#DatabaseType)
* [CloudSqlCredential](#CloudSqlCredential)
  + [JSON representation](#CloudSqlCredential.SCHEMA_REPRESENTATION)
* [Methods](#METHODS_SUMMARY)

## Resource: Connection

Configuration parameters to establish connection with an external data source, except the credential attributes.

| JSON representation |
| --- |
| ``` {   "name": string,   "friendlyName": string,   "description": string,   "creationTime": string,   "lastModifiedTime": string,   "hasCredential": boolean,    // Union field properties can be only one of the following:   "cloudSql": {     object (CloudSqlProperties)   }   // End of list of possible types for union field properties. } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  The resource name of the connection in the form of: `projects/{projectId}/locations/{locationId}/connections/{connectionId}` |
| `friendlyName` | `string`  User provided display name for the connection. |
| `description` | `string`  User provided description. |
| `creationTime` | `string (int64 format)`  Output only. The creation timestamp of the connection. |
| `lastModifiedTime` | `string (int64 format)`  Output only. The last update timestamp of the connection. |
| `hasCredential` | `boolean`  Output only. True, if credential is configured for this connection. |
| Union field `properties`. Properties specific to the underlying data source. `properties` can be only one of the following: | |
| `cloudSql` | `object (CloudSqlProperties)`  Cloud SQL properties. |

## CloudSqlProperties

Connection properties specific to the Cloud SQL.

| JSON representation |
| --- |
| ``` {   "instanceId": string,   "database": string,   "type": enum (DatabaseType),   "credential": {     object (CloudSqlCredential)   },   "serviceAccountId": string } ``` |

| Fields | |
| --- | --- |
| `instanceId` | `string`  Cloud SQL instance ID in the form `project:location:instance`. |
| `database` | `string`  Database name. |
| `type` | `enum (DatabaseType)`  Type of the Cloud SQL database. |
| `credential` | `object (CloudSqlCredential)`  Input only. Cloud SQL credential. |
| `serviceAccountId` | `string`  Output only. The account ID of the service used for the purpose of this connection.  When the connection is used in the context of an operation in BigQuery, this service account will serve as the identity being used for connecting to the CloudSQL instance specified in this connection. |

## DatabaseType

Supported Cloud SQL database types.

| Enums | |
| --- | --- |
| `DATABASE_TYPE_UNSPECIFIED` | Unspecified database type. |
| `POSTGRES` | Cloud SQL for PostgreSQL. |
| `MYSQL` | Cloud SQL for MySQL. |

## CloudSqlCredential

Credential info for the Cloud SQL.

| JSON representation |
| --- |
| ``` {   "username": string,   "password": string } ``` |

| Fields | |
| --- | --- |
| `username` | `string`  The username for the credential. |
| `password` | `string`  The password for the credential. |

| Methods | |
| --- | --- |
| `create` | Creates a new connection. |
| `delete` | Deletes connection and associated credential. |
| `get` | Returns specified connection. |
| `getIamPolicy` | Gets the access control policy for a resource. |
| `list` | Returns a list of connections in the given project. |
| `patch` | Updates the specified connection. |
| `setIamPolicy` | Sets the access control policy on the specified resource. |
| `testIamPermissions` | Returns permissions that a caller has on the specified resource. |
| `updateCredential` | Sets the credential for the specified connection. |




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2025-07-02 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2025-07-02 UTC."],[],[]]