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
* [AwsProperties](#AwsProperties)
  + [JSON representation](#AwsProperties.SCHEMA_REPRESENTATION)
* [AwsAccessRole](#AwsAccessRole)
  + [JSON representation](#AwsAccessRole.SCHEMA_REPRESENTATION)
* [AzureProperties](#AzureProperties)
  + [JSON representation](#AzureProperties.SCHEMA_REPRESENTATION)
* [CloudSpannerProperties](#CloudSpannerProperties)
  + [JSON representation](#CloudSpannerProperties.SCHEMA_REPRESENTATION)
* [CloudResourceProperties](#CloudResourceProperties)
  + [JSON representation](#CloudResourceProperties.SCHEMA_REPRESENTATION)
* [SparkProperties](#SparkProperties)
  + [JSON representation](#SparkProperties.SCHEMA_REPRESENTATION)
* [MetastoreServiceConfig](#MetastoreServiceConfig)
  + [JSON representation](#MetastoreServiceConfig.SCHEMA_REPRESENTATION)
* [SparkHistoryServerConfig](#SparkHistoryServerConfig)
  + [JSON representation](#SparkHistoryServerConfig.SCHEMA_REPRESENTATION)
* [SalesforceDataCloudProperties](#SalesforceDataCloudProperties)
  + [JSON representation](#SalesforceDataCloudProperties.SCHEMA_REPRESENTATION)
* [ConnectorConfiguration](#ConnectorConfiguration)
  + [JSON representation](#ConnectorConfiguration.SCHEMA_REPRESENTATION)
* [Endpoint](#Endpoint)
  + [JSON representation](#Endpoint.SCHEMA_REPRESENTATION)
* [Authentication](#Authentication)
  + [JSON representation](#Authentication.SCHEMA_REPRESENTATION)
* [UsernamePassword](#UsernamePassword)
  + [JSON representation](#UsernamePassword.SCHEMA_REPRESENTATION)
* [Secret](#Secret)
  + [JSON representation](#Secret.SCHEMA_REPRESENTATION)
* [SecretType](#SecretType)
* [Network](#Network)
  + [JSON representation](#Network.SCHEMA_REPRESENTATION)
* [PrivateServiceConnect](#PrivateServiceConnect)
  + [JSON representation](#PrivateServiceConnect.SCHEMA_REPRESENTATION)
* [Asset](#Asset)
  + [JSON representation](#Asset.SCHEMA_REPRESENTATION)
* [Methods](#METHODS_SUMMARY)

## Resource: Connection

Configuration parameters to establish connection with an external data source, except the credential attributes.

| JSON representation |
| --- |
| ``` {   "name": string,   "friendlyName": string,   "description": string,   "configuration": {     object (ConnectorConfiguration)   },   "creationTime": string,   "lastModifiedTime": string,   "hasCredential": boolean,   "kmsKeyName": string,    // Union field properties can be only one of the following:   "cloudSql": {     object (CloudSqlProperties)   },   "aws": {     object (AwsProperties)   },   "azure": {     object (AzureProperties)   },   "cloudSpanner": {     object (CloudSpannerProperties)   },   "cloudResource": {     object (CloudResourceProperties)   },   "spark": {     object (SparkProperties)   },   "salesforceDataCloud": {     object (SalesforceDataCloudProperties)   }   // End of list of possible types for union field properties. } ``` |

| Fields | |
| --- | --- |
| `name` | `string`  Output only. The resource name of the connection in the form of: `projects/{projectId}/locations/{locationId}/connections/{connectionId}` |
| `friendlyName` | `string`  User provided display name for the connection. |
| `description` | `string`  User provided description. |
| `configuration` | `object (ConnectorConfiguration)`  Optional. Connector configuration. |
| `creationTime` | `string (int64 format)`  Output only. The creation timestamp of the connection. |
| `lastModifiedTime` | `string (int64 format)`  Output only. The last update timestamp of the connection. |
| `hasCredential` | `boolean`  Output only. True, if credential is configured for this connection. |
| `kmsKeyName` | `string`  Optional. The Cloud KMS key that is used for credentials encryption.  If omitted, internal Google owned encryption keys are used.  Example: `projects/[kms_project_id]/locations/[region]/keyRings/[key_region]/cryptoKeys/[key]` |
| Union field `properties`. Properties specific to the underlying data source. `properties` can be only one of the following: | |
| `cloudSql` | `object (CloudSqlProperties)`  Cloud SQL properties. |
| `aws` | `object (AwsProperties)`  Amazon Web Services (AWS) properties. |
| `azure` | `object (AzureProperties)`  Azure properties. |
| `cloudSpanner` | `object (CloudSpannerProperties)`  Cloud Spanner properties. |
| `cloudResource` | `object (CloudResourceProperties)`  Cloud Resource properties. |
| `spark` | `object (SparkProperties)`  Spark properties. |
| `salesforceDataCloud` | `object (SalesforceDataCloudProperties)`  Optional. Salesforce DataCloud properties. This field is intended for use only by Salesforce partner projects. This field contains properties for your Salesforce DataCloud connection. |

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

## AwsProperties

Connection properties specific to Amazon Web Services (AWS).

| JSON representation |
| --- |
| ``` {    // Union field authentication_method can be only one of the following:   "accessRole": {     object (AwsAccessRole)   }   // End of list of possible types for union field authentication_method. } ``` |

| Fields | |
| --- | --- |
| Union field `authentication_method`. Authentication method chosen at connection creation. `authentication_method` can be only one of the following: | |
| `accessRole` | `object (AwsAccessRole)`  Authentication using Google owned service account to assume into customer's AWS IAM Role. |

## AwsAccessRole

Authentication method for Amazon Web Services (AWS) that uses Google owned Google service account to assume into customer's AWS IAM Role.

| JSON representation |
| --- |
| ``` {   "iamRoleId": string,   "identity": string } ``` |

| Fields | |
| --- | --- |
| `iamRoleId` | `string`  The user’s AWS IAM Role that trusts the Google-owned AWS IAM user Connection. |
| `identity` | `string`  A unique Google-owned and Google-generated identity for the Connection. This identity will be used to access the user's AWS IAM Role. |

## AzureProperties

Container for connection properties specific to Azure.

| JSON representation |
| --- |
| ``` {   "application": string,   "clientId": string,   "objectId": string,   "customerTenantId": string,   "redirectUri": string,   "federatedApplicationClientId": string,   "identity": string } ``` |

| Fields | |
| --- | --- |
| `application` | `string`  Output only. The name of the Azure Active Directory Application. |
| `clientId` | `string`  Output only. The client id of the Azure Active Directory Application. |
| `objectId` | `string`  Output only. The object id of the Azure Active Directory Application. |
| `customerTenantId` | `string`  The id of customer's directory that host the data. |
| `redirectUri` | `string`  The URL user will be redirected to after granting consent during connection setup. |
| `federatedApplicationClientId` | `string`  The client ID of the user's Azure Active Directory Application used for a federated connection. |
| `identity` | `string`  Output only. A unique Google-owned and Google-generated identity for the Connection. This identity will be used to access the user's Azure Active Directory Application. |

## CloudSpannerProperties

Connection properties specific to Cloud Spanner.

| JSON representation |
| --- |
| ``` {   "database": string,   "useParallelism": boolean,   "maxParallelism": integer,   "useDataBoost": boolean,   "databaseRole": string } ``` |

| Fields | |
| --- | --- |
| `database` | `string`  Cloud Spanner database in the form `project/instance/database' |
| `useParallelism` | `boolean`  If parallelism should be used when reading from Cloud Spanner |
| `maxParallelism` | `integer`  Allows setting max parallelism per query when executing on Spanner independent compute resources. If unspecified, default values of parallelism are chosen that are dependent on the Cloud Spanner instance configuration.  REQUIRES: `useParallelism` must be set.  REQUIRES: `useDataBoost` must be set. |
| `useDataBoost` | `boolean`  If set, the request will be executed via Spanner independent compute resources.  REQUIRES: `useParallelism` must be set. |
| `databaseRole` | `string`  Optional. Cloud Spanner database role for fine-grained access control. The Cloud Spanner admin should have provisioned the database role with appropriate permissions, such as `SELECT` and `INSERT`. Other users should only use roles provided by their Cloud Spanner admins.  For more details, see [About fine-grained access control](https://cloud.google.com/spanner/docs/fgac-about).  REQUIRES: The database role name must start with a letter, and can only contain letters, numbers, and underscores. |

## CloudResourceProperties

Container for connection properties for delegation of access to GCP resources.

| JSON representation |
| --- |
| ``` {   "serviceAccountId": string } ``` |

| Fields | |
| --- | --- |
| `serviceAccountId` | `string`  Output only. The account ID of the service created for the purpose of this connection.  The service account does not have any permissions associated with it when it is created. After creation, customers delegate permissions to the service account. When the connection is used in the context of an operation in BigQuery, the service account will be used to connect to the desired resources in GCP.  The account ID is in the form of: @gcp-sa-bigquery-cloudresource.iam.gserviceaccount.com |

## SparkProperties

Container for connection properties to execute stored procedures for Apache Spark.

| JSON representation |
| --- |
| ``` {   "serviceAccountId": string,   "metastoreServiceConfig": {     object (MetastoreServiceConfig)   },   "sparkHistoryServerConfig": {     object (SparkHistoryServerConfig)   } } ``` |

| Fields | |
| --- | --- |
| `serviceAccountId` | `string`  Output only. The account ID of the service created for the purpose of this connection.  The service account does not have any permissions associated with it when it is created. After creation, customers delegate permissions to the service account. When the connection is used in the context of a stored procedure for Apache Spark in BigQuery, the service account is used to connect to the desired resources in Google Cloud.  The account ID is in the form of: bqcx--@gcp-sa-bigquery-consp.iam.gserviceaccount.com |
| `metastoreServiceConfig` | `object (MetastoreServiceConfig)`  Optional. Dataproc Metastore Service configuration for the connection. |
| `sparkHistoryServerConfig` | `object (SparkHistoryServerConfig)`  Optional. Spark History Server configuration for the connection. |

## MetastoreServiceConfig

Configuration of the Dataproc Metastore Service.

| JSON representation |
| --- |
| ``` {   "metastoreService": string } ``` |

| Fields | |
| --- | --- |
| `metastoreService` | `string`  Optional. Resource name of an existing Dataproc Metastore service.  Example:   * `projects/[projectId]/locations/[region]/services/[serviceId]` |

## SparkHistoryServerConfig

Configuration of the Spark History Server.

| JSON representation |
| --- |
| ``` {   "dataprocCluster": string } ``` |

| Fields | |
| --- | --- |
| `dataprocCluster` | `string`  Optional. Resource name of an existing Dataproc Cluster to act as a Spark History Server for the connection.  Example:   * `projects/[projectId]/regions/[region]/clusters/[cluster_name]` |

## SalesforceDataCloudProperties

Connection properties specific to Salesforce DataCloud. This is intended for use only by Salesforce partner projects.

| JSON representation |
| --- |
| ``` {   "instanceUri": string,   "identity": string,   "tenantId": string } ``` |

| Fields | |
| --- | --- |
| `instanceUri` | `string`  The URL to the user's Salesforce DataCloud instance. |
| `identity` | `string`  Output only. A unique Google-owned and Google-generated service account identity for the connection. |
| `tenantId` | `string`  The ID of the user's Salesforce tenant. |

## ConnectorConfiguration

Represents concrete parameter values for Connector Configuration.

| JSON representation |
| --- |
| ``` {   "connectorId": string,   "endpoint": {     object (Endpoint)   },   "authentication": {     object (Authentication)   },   "network": {     object (Network)   },   "asset": {     object (Asset)   } } ``` |

| Fields | |
| --- | --- |
| `connectorId` | `string`  Required. Immutable. The ID of the Connector these parameters are configured for. |
| `endpoint` | `object (Endpoint)`  Specifies how to reach the remote system this connection is pointing to. |
| `authentication` | `object (Authentication)`  Client authentication. |
| `network` | `object (Network)`  Networking configuration. |
| `asset` | `object (Asset)`  Data asset. |

## Endpoint

Remote endpoint specification.

| JSON representation |
| --- |
| ``` {    // Union field endpoint can be only one of the following:   "hostPort": string   // End of list of possible types for union field endpoint. } ``` |

| Fields | |
| --- | --- |
| Union field `endpoint`.  `endpoint` can be only one of the following: | |
| `hostPort` | `string`  Host and port in a format of `hostname:port` as defined in <https://www.ietf.org/rfc/rfc3986.html#section-3.2.2> and <https://www.ietf.org/rfc/rfc3986.html#section-3.2.3>. |

## Authentication

Client authentication.

| JSON representation |
| --- |
| ``` {   "usernamePassword": {     object (UsernamePassword)   },   "serviceAccount": string } ``` |

| Fields | |
| --- | --- |
| `usernamePassword` | `object (UsernamePassword)`  Username/password authentication. |
| `serviceAccount` | `string`  Output only. Google-managed service account associated with this connection, e.g., `service-{project_number}@gcp-sa-bigqueryconnection.iam.gserviceaccount.com`. BigQuery jobs using this connection will act as `serviceAccount` identity while connecting to the datasource. |

## UsernamePassword

Username and Password authentication.

| JSON representation |
| --- |
| ``` {   "username": string,   "password": {     object (Secret)   } } ``` |

| Fields | |
| --- | --- |
| `username` | `string`  Required. Username. |
| `password` | `object (Secret)`  Required. Password. |

## Secret

Secret value parameter.

| JSON representation |
| --- |
| ``` {   "secretType": ``` |