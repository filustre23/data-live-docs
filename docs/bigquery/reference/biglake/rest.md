As of April 20th, 2026, BigLake is now called Lakehouse for Apache Iceberg. BigLake metastore is now called the Lakehouse runtime catalog. Lakehouse APIs, client libraries, CLI commands, and IAM names remain unchanged and still reference BigLake.

* [Home](https://docs.cloud.google.com/)
* [BigLake API](https://docs.cloud.google.com/lakehouse/docs)

# BigLake API Stay organized with collections Save and categorize content based on your preferences.

The BigLake API provides access to BigLake Metastore, a serverless, fully managed, and highly available metastore for open-source data that can be used for querying Apache Iceberg tables in BigQuery.

* [REST Resource: v1alpha1.projects.locations.catalogs](#v1alpha1.projects.locations.catalogs)
* [REST Resource: v1alpha1.projects.locations.catalogs.databases](#v1alpha1.projects.locations.catalogs.databases)
* [REST Resource: v1alpha1.projects.locations.catalogs.databases.locks](#v1alpha1.projects.locations.catalogs.databases.locks)
* [REST Resource: v1alpha1.projects.locations.catalogs.databases.tables](#v1alpha1.projects.locations.catalogs.databases.tables)
* [REST Resource: [] []](#)
* [REST Resource: deltasharing.v1.projects.catalogs](#deltasharing.v1.projects.catalogs)
* [REST Resource: deltasharing.v1.projects.catalogs.shares](#deltasharing.v1.projects.catalogs.shares)
* [REST Resource: deltasharing.v1.projects.catalogs.shares.schemas](#deltasharing.v1.projects.catalogs.shares.schemas)
* [REST Resource: deltasharing.v1.projects.catalogs.shares.schemas.tables](#deltasharing.v1.projects.catalogs.shares.schemas.tables)
* [REST Resource: deltasharing.v1alpha.projects.catalogs](#deltasharing.v1alpha.projects.catalogs)
* [REST Resource: deltasharing.v1alpha.projects.catalogs.shares](#deltasharing.v1alpha.projects.catalogs.shares)
* [REST Resource: deltasharing.v1alpha.projects.catalogs.shares.schemas](#deltasharing.v1alpha.projects.catalogs.shares.schemas)
* [REST Resource: deltasharing.v1alpha.projects.catalogs.shares.schemas.tables](#deltasharing.v1alpha.projects.catalogs.shares.schemas.tables)
* [REST Resource: hive.v1alpha.projects.catalogs](#hive.v1alpha.projects.catalogs)
* [REST Resource: hive.v1alpha.projects.catalogs.databases](#hive.v1alpha.projects.catalogs.databases)
* [REST Resource: hive.v1alpha.projects.catalogs.databases.tables](#hive.v1alpha.projects.catalogs.databases.tables)
* [REST Resource: hive.v1alpha.projects.catalogs.databases.tables.partitions](#hive.v1alpha.projects.catalogs.databases.tables.partitions)
* [REST Resource: hive.v1beta.projects.catalogs](#hive.v1beta.projects.catalogs)
* [REST Resource: hive.v1beta.projects.catalogs.databases](#hive.v1beta.projects.catalogs.databases)
* [REST Resource: hive.v1beta.projects.catalogs.databases.tables](#hive.v1beta.projects.catalogs.databases.tables)
* [REST Resource: hive.v1beta.projects.catalogs.databases.tables.partitions](#hive.v1beta.projects.catalogs.databases.tables.partitions)
* [REST Resource: iceberg.v1.restcatalog.extensions.projects.catalogs](#iceberg.v1.restcatalog.extensions.projects.catalogs)
* [REST Resource: iceberg.v1.restcatalog.v1](#iceberg.v1.restcatalog.v1)
* [REST Resource: iceberg.v1.restcatalog.v1.projects.catalogs.namespaces](#iceberg.v1.restcatalog.v1.projects.catalogs.namespaces)
* [REST Resource: iceberg.v1.restcatalog.v1.projects.catalogs.namespaces.tables](#iceberg.v1.restcatalog.v1.projects.catalogs.namespaces.tables)
* [REST Resource: iceberg.v1alpha.restcatalog.extensions.projects.catalogs](#iceberg.v1alpha.restcatalog.extensions.projects.catalogs)
* [REST Resource: iceberg.v1alpha.restcatalog.v1](#iceberg.v1alpha.restcatalog.v1)
* [REST Resource: iceberg.v1alpha.restcatalog.v1.projects.catalogs.namespaces](#iceberg.v1alpha.restcatalog.v1.projects.catalogs.namespaces)
* [REST Resource:
  iceberg.v1alpha.restcatalog.v1.projects.catalogs.namespaces.tables](#iceberg.v1alpha.restcatalog.v1.projects.catalogs.namespaces.tables)
* [REST Resource: iceberg.v1beta.restcatalog.extensions.projects.catalogs](#iceberg.v1beta.restcatalog.extensions.projects.catalogs)
* [REST Resource: iceberg.v1beta.restcatalog.v1](#iceberg.v1beta.restcatalog.v1)
* [REST Resource: iceberg.v1beta.restcatalog.v1.projects.catalogs.namespaces](#iceberg.v1beta.restcatalog.v1.projects.catalogs.namespaces)
* [REST Resource:
  iceberg.v1beta.restcatalog.v1.projects.catalogs.namespaces.tables](#iceberg.v1beta.restcatalog.v1.projects.catalogs.namespaces.tables)
* [REST Resource: v1.projects.catalogs](#v1.projects.catalogs)
* [REST Resource: v1.projects.catalogs.namespaces](#v1.projects.catalogs.namespaces)
* [REST Resource: v1.projects.catalogs.namespaces.tables](#v1.projects.catalogs.namespaces.tables)
* [REST Resource: v1.projects.locations.catalogs](#v1.projects.locations.catalogs)
* [REST Resource: v1.projects.locations.catalogs.databases](#v1.projects.locations.catalogs.databases)
* [REST Resource: v1.projects.locations.catalogs.databases.tables](#v1.projects.locations.catalogs.databases.tables)

## Service: biglake.googleapis.com

To call this service, we recommend that you use the Google-provided [client libraries](https://cloud.google.com/apis/docs/client-libraries-explained). If your application needs to use your own libraries to call this service, use the following information when you make the API requests.

### Discovery document

A [Discovery Document](https://developers.google.com/discovery/v1/reference/apis) is a machine-readable specification for describing and consuming REST APIs. It is used to build client libraries, IDE plugins, and other tools that interact with Google APIs. One service may provide multiple discovery documents. This service provides the following discovery documents:

* <https://biglake.googleapis.com/$discovery/rest?version=v1>
* <https://biglake.googleapis.com/$discovery/rest?version=v1alpha1>

### Service endpoint

A [service endpoint](https://cloud.google.com/apis/design/glossary#api_service_endpoint) is a base URL that specifies the network address of an API service. One service might have multiple service endpoints. This service has the following service endpoint and all URIs below are relative to this service endpoint:

* `https://biglake.googleapis.com`

## REST Resource: [v1alpha1.projects.locations.catalogs](/lakehouse/docs/reference/rest/v1alpha1/projects.locations.catalogs)

| Methods | |
| --- | --- |
| `create` | `POST /v1alpha1/{parent=projects/*/locations/*}/catalogs`   Creates a new catalog. |
| `delete` | `DELETE /v1alpha1/{name=projects/*/locations/*/catalogs/*}`   Deletes an existing catalog specified by the catalog ID. |
| `get` | `GET /v1alpha1/{name=projects/*/locations/*/catalogs/*}`   Gets the catalog specified by the resource name. |
| `list` | `GET /v1alpha1/{parent=projects/*/locations/*}/catalogs`   List all catalogs in a specified project. |

## REST Resource: [v1alpha1.projects.locations.catalogs.databases](/lakehouse/docs/reference/rest/v1alpha1/projects.locations.catalogs.databases)

| Methods | |
| --- | --- |
| `create` | `POST /v1alpha1/{parent=projects/*/locations/*/catalogs/*}/databases`   Creates a new database. |
| `delete` | `DELETE /v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*}`   Deletes an existing database specified by the database ID. |
| `get` | `GET /v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*}`   Gets the database specified by the resource name. |
| `list` | `GET /v1alpha1/{parent=projects/*/locations/*/catalogs/*}/databases`   List all databases in a specified catalog. |
| `patch` | `PATCH /v1alpha1/{database.name=projects/*/locations/*/catalogs/*/databases/*}`   Updates an existing database specified by the database ID. |

## REST Resource: [v1alpha1.projects.locations.catalogs.databases.locks](/lakehouse/docs/reference/rest/v1alpha1/projects.locations.catalogs.databases.locks)

| Methods | |
| --- | --- |
| `check` | `POST /v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*/locks/*}:check`   Checks the state of a lock specified by the lock ID. |
| `create` | `POST /v1alpha1/{parent=projects/*/locations/*/catalogs/*/databases/*}/locks`   Creates a new lock. |
| `delete` | `DELETE /v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*/locks/*}`   Deletes an existing lock specified by the lock ID. |
| `list` | `GET /v1alpha1/{parent=projects/*/locations/*/catalogs/*/databases/*}/locks`   List all locks in a specified database. |

## REST Resource: [v1alpha1.projects.locations.catalogs.databases.tables](/lakehouse/docs/reference/rest/v1alpha1/projects.locations.catalogs.databases.tables)

| Methods | |
| --- | --- |
| `create` | `POST /v1alpha1/{parent=projects/*/locations/*/catalogs/*/databases/*}/tables`   Creates a new table. |
| `delete` | `DELETE /v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*/tables/*}`   Deletes an existing table specified by the table ID. |
| `get` | `GET /v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*/tables/*}`   Gets the table specified by the resource name. |
| `list` | `GET /v1alpha1/{parent=projects/*/locations/*/catalogs/*/databases/*}/tables`   List all tables in a specified database. |
| `patch` | `PATCH /v1alpha1/{table.name=projects/*/locations/*/catalogs/*/databases/*/tables/*}`   Updates an existing table specified by the table ID. |
| `rename` | `POST /v1alpha1/{name=projects/*/locations/*/catalogs/*/databases/*/tables/*}:rename`   Renames an existing table specified by the table ID. |

## REST Resource: [] []

| Methods | |
| --- | --- |
| `google.cloud.biglake.v1.IcebergCatalogService.CheckIcebergNamespaceExists` | `NONE /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}`   Returns 204 if the namespace exists, 404 otherwise. |
| `google.cloud.biglake.v1.IcebergCatalogService.CheckIcebergTableExists` | `NONE /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   Returns 204 if the table exists, 404 otherwise. |
| `google.cloud.biglake.v1alpha.IcebergCatalogService.CheckIcebergNamespaceExists` | `NONE /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}`   Returns 204 if the namespace exists, 404 otherwise. |
| `google.cloud.biglake.v1alpha.IcebergCatalogService.CheckIcebergTableExists` | `NONE /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   Returns 204 if the table exists, 404 otherwise. |
| `google.cloud.biglake.v1beta.IcebergCatalogService.CheckIcebergNamespaceExists` | `NONE /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}`   Returns 204 if the namespace exists, 404 otherwise. |
| `google.cloud.biglake.v1beta.IcebergCatalogService.CheckIcebergTableExists` | `NONE /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   Returns 204 if the table exists, 404 otherwise. |

## REST Resource: [deltasharing.v1.projects.catalogs](/lakehouse/docs/reference/rest/v1/deltasharing.v1.projects.catalogs)

| Methods | |
| --- | --- |
| `create` | `POST /deltasharing/v1/{parent=projects/*}/catalogs`   Creates a new DeltaSharing catalog. |
| `delete` | `DELETE /deltasharing/v1/{name=projects/*/catalogs/*}`   Deletes an existing DeltaSharing catalog specified by the resource name. |
| `get` | `GET /deltasharing/v1/{name=projects/*/catalogs/*}`   Gets the catalog specified by the resource name. |
| `list` | `GET /deltasharing/v1/{parent=projects/*}/catalogs`   List all DeltaSharing catalogs in a specified project. |
| `patch` | `PATCH /deltasharing/v1/{deltaSharingCatalog.name=projects/*/catalogs/*}`   Updates an existing DeltaSharing catalog. |

## REST Resource: [deltasharing.v1.projects.catalogs.shares](/lakehouse/docs/reference/rest/v1/deltasharing.v1.projects.catalogs.shares)

| Methods | |
| --- | --- |
| `list` | `GET /deltasharing/v1/{parent=projects/*/catalogs/*}/shares`   Gets a list of Delta Sharing shares available in the upstream Delta Sharing source (e.g., SAP BDC). |

## REST Resource: [deltasharing.v1.projects.catalogs.shares.schemas](/lakehouse/docs/reference/rest/v1/deltasharing.v1.projects.catalogs.shares.schemas)

| Methods | |
| --- | --- |
| `list` | `GET /deltasharing/v1/{parent=projects/*/catalogs/*/shares/*}/schemas`   Gets a list of Delta Sharing schemas available in the upstream SAP BDC source. |

## REST Resource: [deltasharing.v1.projects.catalogs.shares.schemas.tables](/lakehouse/docs/reference/rest/v1/deltasharing.v1.projects.catalogs.shares.schemas.tables)

| Methods | |
| --- | --- |
| `list` | `GET /deltasharing/v1/{parent=projects/*/catalogs/*/shares/*/schemas/*}/tables`   Gets a list of Delta Sharing tables available in the upstream SAP BDC source. |

## REST Resource: [deltasharing.v1alpha.projects.catalogs](/lakehouse/docs/reference/rest/v1/deltasharing.v1alpha.projects.catalogs)

| Methods | |
| --- | --- |
| `create` | `POST /deltasharing/v1alpha/{parent=projects/*}/catalogs`   Creates a new DeltaSharing catalog. |
| `delete` | `DELETE /deltasharing/v1alpha/{name=projects/*/catalogs/*}`   Deletes an existing DeltaSharing catalog specified by the resource name. |
| `get` | `GET /deltasharing/v1alpha/{name=projects/*/catalogs/*}`   Gets the catalog specified by the resource name. |
| `list` | `GET /deltasharing/v1alpha/{parent=projects/*}/catalogs`   List all DeltaSharing catalogs in a specified project. |
| `patch` | `PATCH /deltasharing/v1alpha/{deltaSharingCatalog.name=projects/*/catalogs/*}`   Updates an existing DeltaSharing catalog. |

## REST Resource: [deltasharing.v1alpha.projects.catalogs.shares](/lakehouse/docs/reference/rest/v1/deltasharing.v1alpha.projects.catalogs.shares)

| Methods | |
| --- | --- |
| `list` | `GET /deltasharing/v1alpha/{parent=projects/*/catalogs/*}/shares`   Gets a list of Delta Sharing shares available in the upstream Delta Sharing source (e.g., SAP BDC). |

## REST Resource: [deltasharing.v1alpha.projects.catalogs.shares.schemas](/lakehouse/docs/reference/rest/v1/deltasharing.v1alpha.projects.catalogs.shares.schemas)

| Methods | |
| --- | --- |
| `list` | `GET /deltasharing/v1alpha/{parent=projects/*/catalogs/*/shares/*}/schemas`   Gets a list of Delta Sharing schemas available in the upstream SAP BDC source. |

## REST Resource: [deltasharing.v1alpha.projects.catalogs.shares.schemas.tables](/lakehouse/docs/reference/rest/v1/deltasharing.v1alpha.projects.catalogs.shares.schemas.tables)

| Methods | |
| --- | --- |
| `list` | `GET /deltasharing/v1alpha/{parent=projects/*/catalogs/*/shares/*/schemas/*}/tables`   Gets a list of Delta Sharing tables available in the upstream SAP BDC source. |

## REST Resource: [hive.v1alpha.projects.catalogs](/lakehouse/docs/reference/rest/v1/hive.v1alpha.projects.catalogs)

| Methods | |
| --- | --- |
| `create` | `POST /hive/v1alpha/{parent=projects/*}/catalogs`   Creates a new hive catalog. |
| `delete` | `DELETE /hive/v1alpha/{name=projects/*/catalogs/*}`   Deletes an existing catalog specified by the catalog ID. |
| `get` | `GET /hive/v1alpha/{name=projects/*/catalogs/*}`   Gets the catalog specified by the resource name. |
| `list` | `GET /hive/v1alpha/{parent=projects/*}/catalogs`   List all catalogs in a specified project. |
| `patch` | `PATCH /hive/v1alpha/{hiveCatalog.name=projects/*/catalogs/*}`   Updates an existing catalog. |

## REST Resource: [hive.v1alpha.projects.catalogs.databases](/lakehouse/docs/reference/rest/v1/hive.v1alpha.projects.catalogs.databases)

| Methods | |
| --- | --- |
| `create` | `POST /hive/v1alpha/{parent=projects/*/catalogs/*}/databases`   Creates a new database. |
| `delete` | `DELETE /hive/v1alpha/{name=projects/*/catalogs/*/databases/*}`   Deletes an existing database specified by the database name. |
| `get` | `GET /hive/v1alpha/{name=projects/*/catalogs/*/databases/*}`   Gets the database specified by the resource name. |
| `list` | `GET /hive/v1alpha/{parent=projects/*/catalogs/*}/databases`   List all databases in a specified catalog. |
| `patch` | `PATCH /hive/v1alpha/{hiveDatabase.name=projects/*/catalogs/*/databases/*}`   Updates an existing database specified by the database name. |

## REST Resource: [hive.v1alpha.projects.catalogs.databases.tables](/lakehouse/docs/reference/rest/v1/hive.v1alpha.projects.catalogs.databases.tables)

| Methods | |
| --- | --- |
| `create` | `POST /hive/v1alpha/{parent=projects/*/catalogs/*/databases/*}/tables`   Creates a new hive table. |
| `delete` | `DELETE /hive/v1alpha/{name=projects/*/catalogs/*/databases/*/tables/*}`   Deletes an existing table specified by the table name. |
| `get` | `GET /hive/v1alpha/{name=projects/*/catalogs/*/databases/*/tables/*}`   Gets the table specified by the resource name. |
| `list` | `GET /hive/v1alpha/{parent=projects/*/catalogs/*/databases/*}/tables`   List all hive tables in a specified project under the hive catalog and database. |
| `patch` | `PATCH /hive/v1alpha/{hiveTable.name=projects/*/catalogs/*/databases/*/tables/*}`   Updates an existing table specified by the table name. |

## REST Resource: [hive.v1alpha.projects.catalogs.databases.tables.partitions](/lakehouse/docs/reference/rest/v1/hive.v1alpha.projects.catalogs.databases.tables.partitions)

| Methods | |
| --- | --- |
| `batchCreate` | `POST /hive/v1alpha/{parent=projects/*/catalogs/*/databases/*/tables/*}/partitions:batchCreate`   Adds partitions to a table. |
| `batchDelete` | `POST /hive/v1alpha/{parent=projects/*/catalogs/*/databases/*/tables/*}/partitions:batchDelete`   Deletes partitions from a table. |
| `batchUpdate` | `POST /hive/v1alpha/{parent=projects/*/catalogs/*/databases/*/tables/*}/partitions:batchUpdate`   Updates partitions in a table. |
| `list` | `GET /hive/v1alpha/{parent=projects/*/catalogs/*/databases/*/tables/*}/partitions:list`   Streams list of partitions from a table. |

## REST Resource: [hive.v1beta.projects.catalogs](/lakehouse/docs/reference/rest/v1/hive.v1beta.projects.catalogs)

| Methods | |
| --- | --- |
| `create` | `POST /hive/v1beta/{parent=projects/*}/catalogs`   Creates a new hive catalog. |
| `delete` | `DELETE /hive/v1beta/{name=projects/*/catalogs/*}`   Deletes an existing catalog specified by the catalog ID. |
| `get` | `GET /hive/v1beta/{name=projects/*/catalogs/*}`   Gets the catalog specified by the resource name. |
| `list` | `GET /hive/v1beta/{parent=projects/*}/catalogs`   List all catalogs in a specified project. |
| `patch` | `PATCH /hive/v1beta/{hiveCatalog.name=projects/*/catalogs/*}`   Updates an existing catalog. |

## REST Resource: [hive.v1beta.projects.catalogs.databases](/lakehouse/docs/reference/rest/v1/hive.v1beta.projects.catalogs.databases)

| Methods | |
| --- | --- |
| `create` | `POST /hive/v1beta/{parent=projects/*/catalogs/*}/databases`   Creates a new database. |
| `delete` | `DELETE /hive/v1beta/{name=projects/*/catalogs/*/databases/*}`   Deletes an existing database specified by the database name. |
| `get` | `GET /hive/v1beta/{name=projects/*/catalogs/*/databases/*}`   Gets the database specified by the resource name. |
| `list` | `GET /hive/v1beta/{parent=projects/*/catalogs/*}/databases`   List all databases in a specified catalog. |
| `patch` | `PATCH /hive/v1beta/{hiveDatabase.name=projects/*/catalogs/*/databases/*}`   Updates an existing database specified by the database name. |

## REST Resource: [hive.v1beta.projects.catalogs.databases.tables](/lakehouse/docs/reference/rest/v1/hive.v1beta.projects.catalogs.databases.tables)

| Methods | |
| --- | --- |
| `create` | `POST /hive/v1beta/{parent=projects/*/catalogs/*/databases/*}/tables`   Creates a new hive table. |
| `delete` | `DELETE /hive/v1beta/{name=projects/*/catalogs/*/databases/*/tables/*}`   Deletes an existing table specified by the table name. |
| `get` | `GET /hive/v1beta/{name=projects/*/catalogs/*/databases/*/tables/*}`   Gets the table specified by the resource name. |
| `list` | `GET /hive/v1beta/{parent=projects/*/catalogs/*/databases/*}/tables`   List all hive tables in a specified project under the hive catalog and database. |
| `patch` | `PATCH /hive/v1beta/{hiveTable.name=projects/*/catalogs/*/databases/*/tables/*}`   Updates an existing table specified by the table name. |

## REST Resource: [hive.v1beta.projects.catalogs.databases.tables.partitions](/lakehouse/docs/reference/rest/v1/hive.v1beta.projects.catalogs.databases.tables.partitions)

| Methods | |
| --- | --- |
| `batchCreate` | `POST /hive/v1beta/{parent=projects/*/catalogs/*/databases/*/tables/*}/partitions:batchCreate`   Adds partitions to a table. |
| `batchDelete` | `POST /hive/v1beta/{parent=projects/*/catalogs/*/databases/*/tables/*}/partitions:batchDelete`   Deletes partitions from a table. |
| `batchUpdate` | `POST /hive/v1beta/{parent=projects/*/catalogs/*/databases/*/tables/*}/partitions:batchUpdate`   Updates partitions in a table. |
| `list` | `GET /hive/v1beta/{parent=projects/*/catalogs/*/databases/*/tables/*}/partitions:list`   Streams list of partitions from a table. |

## REST Resource: [iceberg.v1.restcatalog.extensions.projects.catalogs](/lakehouse/docs/reference/rest/v1/iceberg.v1.restcatalog.extensions.projects.catalogs)

| Methods | |
| --- | --- |
| `create` | `POST /iceberg/v1/restcatalog/extensions/{parent=projects/*}/catalogs`   Creates the Iceberg REST Catalog. |
| `delete` | `DELETE /iceberg/v1/restcatalog/extensions/{name=projects/*/catalogs/*}`   Deletes the Iceberg REST Catalog. |
| `failover` | `POST /iceberg/v1/restcatalog/extensions/{name=projects/*/catalogs/*}:failover`   Failover the catalog to a new primary replica region. |
| `get` | `GET /iceberg/v1/restcatalog/extensions/{name=projects/*/catalogs/*}`   Returns the Iceberg REST Catalog configuration options. |
| `list` | `GET /iceberg/v1/restcatalog/extensions/{parent=projects/*}/catalogs`   Lists the Iceberg REST Catalogs. |
| `patch` | `PATCH /iceberg/v1/restcatalog/extensions/{icebergCatalog.name=projects/*/catalogs/*}`   Update the Iceberg REST Catalog configuration options. |

## REST Resource: [iceberg.v1.restcatalog.v1](/lakehouse/docs/reference/rest/v1/iceberg.v1.restcatalog.v1)

| Methods | |
| --- | --- |
| `getConfig` | `GET /iceberg/v1/restcatalog/v1/config`   GetIcebergCatalogConfig lists all catalog configuration settings. |

## REST Resource: [iceberg.v1.restcatalog.v1.projects.catalogs.namespaces](/lakehouse/docs/reference/rest/v1/iceberg.v1.restcatalog.v1.projects.catalogs.namespaces)

| Methods | |
| --- | --- |
| `create` | `POST /iceberg/v1/restcatalog/v1/{parent=projects/*/catalogs/*}/namespaces`   Creates a namespace in the catalog. |
| `delete` | `DELETE /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}`   Returns 204, not 200 on success. |
| `get` | `GET /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}`   Gets an Iceberg namespace in the catalog (or checks if it exists, if the method is HEAD). |
| `list` | `GET /iceberg/v1/restcatalog/v1/{apiParent=projects/*/catalogs/*}/namespaces`   Lists Iceberg namespaces in the catalog. |
| `properties` | `POST /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}/properties`   Updates namespace properties. |
| `register` | `POST /iceberg/v1/restcatalog/v1/{parent=projects/*/catalogs/*/namespaces/*}/register`   Register a table using given metadata file location. |
| `updateProperties` | `PATCH /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}/properties`   Updates namespace properties. |

## REST Resource: [iceberg.v1.restcatalog.v1.projects.catalogs.namespaces.tables](/lakehouse/docs/reference/rest/v1/iceberg.v1.restcatalog.v1.projects.catalogs.namespaces.tables)

| Methods | |
| --- | --- |
| `create` | `POST /iceberg/v1/restcatalog/v1/{parent=projects/*/catalogs/*/namespaces/*}/tables`   Creates a table in the namespace. |
| `credentials` | `GET /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}/credentials`   Loads credentials for a table in the namespace. |
| `delete` | `DELETE /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   Deletes a table in the namespace. |
| `get` | `GET /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   Gets a table in the namespace. |
| `list` | `GET /iceberg/v1/restcatalog/v1/{parent=projects/*/catalogs/*/namespaces/*}/tables`   Lists table identifiers (not *tables*) in the namespace. |
| `metrics` | `POST /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}/metrics`   Reports a metrics report for a table. |
| `updateIcebergTable` | `POST /iceberg/v1/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   This is CommitTable Iceberg API, which maps to `UpdateIcebergTable` in the Google API nomenclature. |

## REST Resource: [iceberg.v1alpha.restcatalog.extensions.projects.catalogs](/lakehouse/docs/reference/rest/v1/iceberg.v1alpha.restcatalog.extensions.projects.catalogs)

| Methods | |
| --- | --- |
| `create` | `POST /iceberg/v1alpha/restcatalog/extensions/{parent=projects/*}/catalogs`   Creates the Iceberg REST Catalog. |
| `delete` | `DELETE /iceberg/v1alpha/restcatalog/extensions/{name=projects/*/catalogs/*}`   Deletes the Iceberg REST Catalog. |
| `failover` | `POST /iceberg/v1alpha/restcatalog/extensions/{name=projects/*/catalogs/*}:failover`   Failover the catalog to a new primary replica region. |
| `get` | `GET /iceberg/v1alpha/restcatalog/extensions/{name=projects/*/catalogs/*}`   Returns the Iceberg REST Catalog configuration options. |
| `list` | `GET /iceberg/v1alpha/restcatalog/extensions/{parent=projects/*}/catalogs`   Lists the Iceberg REST Catalogs. |
| `patch` | `PATCH /iceberg/v1alpha/restcatalog/extensions/{icebergCatalog.name=projects/*/catalogs/*}`   Update the Iceberg REST Catalog configuration options. |

## REST Resource: [iceberg.v1alpha.restcatalog.v1](/lakehouse/docs/reference/rest/v1/iceberg.v1alpha.restcatalog.v1)

| Methods | |
| --- | --- |
| `getConfig` | `GET /iceberg/v1alpha/restcatalog/v1/config`   GetIcebergCatalogConfig lists all catalog configuration settings. |

## REST Resource: [iceberg.v1alpha.restcatalog.v1.projects.catalogs.namespaces](/lakehouse/docs/reference/rest/v1/iceberg.v1alpha.restcatalog.v1.projects.catalogs.namespaces)

| Methods | |
| --- | --- |
| `create` | `POST /iceberg/v1alpha/restcatalog/v1/{parent=projects/*/catalogs/*}/namespaces`   Creates a namespace in the catalog. |
| `delete` | `DELETE /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}`   Returns 204, not 200 on success. |
| `get` | `GET /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}`   Gets an Iceberg namespace in the catalog (or checks if it exists, if the method is HEAD). |
| `list` | `GET /iceberg/v1alpha/restcatalog/v1/{apiParent=projects/*/catalogs/*}/namespaces`   Lists Iceberg namespaces in the catalog. |
| `properties` | `POST /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}/properties`   Updates namespace properties. |
| `register` | `POST /iceberg/v1alpha/restcatalog/v1/{parent=projects/*/catalogs/*/namespaces/*}/register`   Register a table using given metadata file location. |
| `updateProperties` | `PATCH /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}/properties`   Updates namespace properties. |

## REST Resource: [iceberg.v1alpha.restcatalog.v1.projects.catalogs.namespaces.tables](/lakehouse/docs/reference/rest/v1/iceberg.v1alpha.restcatalog.v1.projects.catalogs.namespaces.tables)

| Methods | |
| --- | --- |
| `create` | `POST /iceberg/v1alpha/restcatalog/v1/{parent=projects/*/catalogs/*/namespaces/*}/tables`   Creates a table in the namespace. |
| `credentials` | `GET /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}/credentials`   Loads credentials for a table in the namespace. |
| `delete` | `DELETE /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   Deletes a table in the namespace. |
| `get` | `GET /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   Gets a table in the namespace. |
| `list` | `GET /iceberg/v1alpha/restcatalog/v1/{parent=projects/*/catalogs/*/namespaces/*}/tables`   Lists table identifiers (not *tables*) in the namespace. |
| `metrics` | `POST /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}/metrics`   Reports a metrics report for a table. |
| `updateIcebergTable` | `POST /iceberg/v1alpha/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   This is CommitTable Iceberg API, which maps to `UpdateIcebergTable` in the Google API nomenclature. |

## REST Resource: [iceberg.v1beta.restcatalog.extensions.projects.catalogs](/lakehouse/docs/reference/rest/v1/iceberg.v1beta.restcatalog.extensions.projects.catalogs)

| Methods | |
| --- | --- |
| `create` | `POST /iceberg/v1beta/restcatalog/extensions/{parent=projects/*}/catalogs`   Creates the Iceberg REST Catalog. |
| `delete` | `DELETE /iceberg/v1beta/restcatalog/extensions/{name=projects/*/catalogs/*}`   Deletes the Iceberg REST Catalog. |
| `failover` | `POST /iceberg/v1beta/restcatalog/extensions/{name=projects/*/catalogs/*}:failover`   Failover the catalog to a new primary replica region. |
| `get` | `GET /iceberg/v1beta/restcatalog/extensions/{name=projects/*/catalogs/*}`   Returns the Iceberg REST Catalog configuration options. |
| `list` | `GET /iceberg/v1beta/restcatalog/extensions/{parent=projects/*}/catalogs`   Lists the Iceberg REST Catalogs. |
| `patch` | `PATCH /iceberg/v1beta/restcatalog/extensions/{icebergCatalog.name=projects/*/catalogs/*}`   Update the Iceberg REST Catalog configuration options. |

## REST Resource: [iceberg.v1beta.restcatalog.v1](/lakehouse/docs/reference/rest/v1/iceberg.v1beta.restcatalog.v1)

| Methods | |
| --- | --- |
| `getConfig` | `GET /iceberg/v1beta/restcatalog/v1/config`   GetIcebergCatalogConfig lists all catalog configuration settings. |

## REST Resource: [iceberg.v1beta.restcatalog.v1.projects.catalogs.namespaces](/lakehouse/docs/reference/rest/v1/iceberg.v1beta.restcatalog.v1.projects.catalogs.namespaces)

| Methods | |
| --- | --- |
| `create` | `POST /iceberg/v1beta/restcatalog/v1/{parent=projects/*/catalogs/*}/namespaces`   Creates a namespace in the catalog. |
| `delete` | `DELETE /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}`   Returns 204, not 200 on success. |
| `get` | `GET /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}`   Gets an Iceberg namespace in the catalog (or checks if it exists, if the method is HEAD). |
| `list` | `GET /iceberg/v1beta/restcatalog/v1/{apiParent=projects/*/catalogs/*}/namespaces`   Lists Iceberg namespaces in the catalog. |
| `properties` | `POST /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}/properties`   Updates namespace properties. |
| `register` | `POST /iceberg/v1beta/restcatalog/v1/{parent=projects/*/catalogs/*/namespaces/*}/register`   Register a table using given metadata file location. |
| `updateProperties` | `PATCH /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*}/properties`   Updates namespace properties. |

## REST Resource: [iceberg.v1beta.restcatalog.v1.projects.catalogs.namespaces.tables](/lakehouse/docs/reference/rest/v1/iceberg.v1beta.restcatalog.v1.projects.catalogs.namespaces.tables)

| Methods | |
| --- | --- |
| `create` | `POST /iceberg/v1beta/restcatalog/v1/{parent=projects/*/catalogs/*/namespaces/*}/tables`   Creates a table in the namespace. |
| `credentials` | `GET /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}/credentials`   Loads credentials for a table in the namespace. |
| `delete` | `DELETE /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   Deletes a table in the namespace. |
| `get` | `GET /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   Gets a table in the namespace. |
| `list` | `GET /iceberg/v1beta/restcatalog/v1/{parent=projects/*/catalogs/*/namespaces/*}/tables`   Lists table identifiers (not *tables*) in the namespace. |
| `metrics` | `POST /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}/metrics`   Reports a metrics report for a table. |
| `updateIcebergTable` | `POST /iceberg/v1beta/restcatalog/v1/{name=projects/*/catalogs/*/namespaces/*/tables/*}`   This is CommitTable Iceberg API, which maps to `UpdateIcebergTable` in the Google API nomenclature. |

## REST Resource: [v1.projects.catalogs](/lakehouse/docs/reference/rest/v1/projects.catalogs)

| Methods | |
| --- | --- |
| `getIamPolicy` | `GET /v1/{resource=projects/*/catalogs/*}:getIamPolicy`   Gets the IAM policy for the specified Catalog. |
| `setIamPolicy` | `POST /v1/{resource=projects/*/catalogs/*}:setIamPolicy`   Sets the IAM policy for the specified catalog. |
| `testIamPermissions` | `POST /v1/{resource=projects/*/catalogs/*}:testIamPermissions`   Tests the IAM permissions for the specified catalog. |

## REST Resource: [v1.projects.catalogs.namespaces](/lakehouse/docs/reference/rest/v1/projects.catalogs.namespaces)

| Methods | |
| --- | --- |
| `getIamPolicy` | `GET /v1/{resource=projects/*/catalogs/*/namespaces/*}:getIamPolicy`   Gets the IAM policy for the specified Catalog. |
| `setIamPolicy` | `POST /v1/{resource=projects/*/catalogs/*/namespaces/*}:setIamPolicy`   Sets the IAM policy for the specified catalog. |
| `testIamPermissions` | `POST /v1/{resource=projects/*/catalogs/*/namespaces/*}:testIamPermissions`   Tests the IAM permissions for the specified namespace. |

## REST Resource: [v1.projects.catalogs.namespaces.tables](/lakehouse/docs/reference/rest/v1/projects.catalogs.namespaces.tables)

| Methods | |
| --- | --- |
| `getIamPolicy` | `GET /v1/{resource=projects/*/catalogs/*/namespaces/*/tables/*}:getIamPolicy`   Gets the IAM policy for the specified Catalog. |
| `setIamPolicy` | `POST /v1/{resource=projects/*/catalogs/*/namespaces/*/tables/*}:setIamPolicy`   Sets the IAM policy for the specified catalog. |
| `testIamPermissions` | `POST /v1/{resource=projects/*/catalogs/*/namespaces/*/tables/*}:testIamPermissions`   Tests the IAM permissions for the specified table. |

## REST Resource: [v1.projects.locations.catalogs](/lakehouse/docs/reference/rest/v1/projects.locations.catalogs)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*}/catalogs`   Creates a new catalog. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/catalogs/*}`   Deletes an existing catalog specified by the catalog ID. |
| `get` | `GET /v1/{name=projects/*/locations/*/catalogs/*}`   Gets the catalog specified by the resource name. |
| `list` | `GET /v1/{parent=projects/*/locations/*}/catalogs`   List all catalogs in a specified project. |

## REST Resource: [v1.projects.locations.catalogs.databases](/lakehouse/docs/reference/rest/v1/projects.locations.catalogs.databases)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*/catalogs/*}/databases`   Creates a new database. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/catalogs/*/databases/*}`   Deletes an existing database specified by the database ID. |
| `get` | `GET /v1/{name=projects/*/locations/*/catalogs/*/databases/*}`   Gets the database specified by the resource name. |
| `list` | `GET /v1/{parent=projects/*/locations/*/catalogs/*}/databases`   List all databases in a specified catalog. |
| `patch` | `PATCH /v1/{database.name=projects/*/locations/*/catalogs/*/databases/*}`   Updates an existing database specified by the database ID. |

## REST Resource: [v1.projects.locations.catalogs.databases.tables](/lakehouse/docs/reference/rest/v1/projects.locations.catalogs.databases.tables)

| Methods | |
| --- | --- |
| `create` | `POST /v1/{parent=projects/*/locations/*/catalogs/*/databases/*}/tables`   Creates a new table. |
| `delete` | `DELETE /v1/{name=projects/*/locations/*/catalogs/*/databases/*/tables/*}`   Deletes an existing table specified by the table ID. |
| `get` | `GET /v1/{name=projects/*/locations/*/catalogs/*/databases/*/tables/*}`   Gets the table specified by the resource name. |
| `list` | `GET /v1/{parent=projects/*/locations/*/catalogs/*/databases/*}/tables`   List all tables in a specified database. |
| `patch` | `PATCH /v1/{table.name=projects/*/locations/*/catalogs/*/databases/*/tables/*}`   Updates an existing table specified by the table ID. |
| `rename` | `POST /v1/{name=projects/*/locations/*/catalogs/*/databases/*/tables/*}:rename`   Renames an existing table specified by the table ID. |

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-21 UTC.




[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-21 UTC."],[],[]]