* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# Data definition language (DDL) statements in GoogleSQL

Data definition language (DDL) statements let you create and modify
BigQuery resources using
[GoogleSQL](/bigquery/docs/reference/standard-sql)
query syntax. You can use DDL commands to create, alter, and delete resources,
such as the following:

* [Datasets](/bigquery/docs/datasets-intro)
* [Tables](/bigquery/docs/tables-intro)
* [Table schemas](/bigquery/docs/managing-table-schemas)
* [Table clones](/bigquery/docs/table-clones-intro)
* [Table snapshots](/bigquery/docs/table-snapshots-intro)
* [Views](/bigquery/docs/views)
* [Connections](/bigquery/docs/connections-api-intro)
* [User-defined functions](#create_function_statement) (UDFs)
* [Indexes](/bigquery/docs/search-intro)
* [Capacity commitments and reservations](/bigquery/docs/reservations-intro)
* [Row-level access policies](/bigquery/docs/managing-row-level-security)
* [Default configuration settings](/bigquery/docs/default-configuration)

## Required permissions

To create a job that runs a DDL statement, you must have the
`bigquery.jobs.create` permission for the project where you are running the job.
Each DDL statement also requires specific permissions on the affected resources,
which are documented under each statement.

### IAM roles

The predefined IAM roles `bigquery.user`,
`bigquery.jobUser`, and `bigquery.admin` include the required
`bigquery.jobs.create` permission.

For more information about IAM roles in BigQuery,
see [Predefined roles and permissions](/bigquery/access-control) or the
[IAM permissions reference](/iam/docs/permissions-reference).

## Run DDL statements

You can run DDL statements by using the Google Cloud console, by using the
bq command-line tool, by calling the
[`jobs.query`](/bigquery/docs/reference/rest/v2/jobs/query) REST API, or
programmatically using the
[BigQuery API client libraries](/bigquery/docs/reference/libraries).

### Console

1. Go to the BigQuery page in the Google Cloud console.

   [Go to BigQuery](https://console.cloud.google.com/bigquery)
2. Click **Compose new query**.
3. Enter the DDL statement into the **Query editor** text area. For example:

   ```
    CREATE TABLE mydataset.newtable ( x INT64 )
   ```
4. Click **Run**.

### bq

Enter the
[`bq query`](/bigquery/docs/reference/bq-cli-reference#bq_query) command
and supply the DDL statement as the query parameter. Set the
`use_legacy_sql` flag to `false`.

```
bq query --use_legacy_sql=false \
  'CREATE TABLE mydataset.newtable ( x INT64 )'
```

### API

Call the [`jobs.query`](/bigquery/docs/reference/rest/v2/jobs/query) method
and supply the DDL statement in the request body's `query` property.

DDL functionality extends the information returned by a
[Jobs resource](/bigquery/docs/reference/rest/v2/jobs#resource).
`statistics.query.statementType` includes the following additional values:

* `CREATE_TABLE`
* `CREATE_TABLE_AS_SELECT`
* `DROP_TABLE`
* `CREATE_VIEW`
* `DROP_VIEW`

`statistics.query` has 2 additional fields:

* `ddlOperationPerformed`: The DDL operation performed, possibly dependent on
  the existence of the DDL target. Current values include:
  + `CREATE`: The query created the DDL target.
  + `SKIP`: No-op. Examples — `CREATE TABLE IF NOT EXISTS` was
    submitted, and the table exists. Or `DROP TABLE IF EXISTS` was submitted, and the
    table does not exist.
  + `REPLACE`: The query replaced the DDL target. Example —
    `CREATE OR REPLACE TABLE` was submitted, and the table already exists.
  + `DROP`: The query deleted the DDL target.* `ddlTargetTable`: When you submit a `CREATE TABLE/VIEW` statement or a
    `DROP TABLE/VIEW` statement, the target table is returned as an object with 3 fields:
  + "projectId": string
  + "datasetId": string
  + "tableId": string

### Java

Call the
[`BigQuery.create()`](/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.BigQuery#com_google_cloud_bigquery_BigQuery_create_com_google_cloud_bigquery_JobInfo_com_google_cloud_bigquery_BigQuery_JobOption____)
method to start a query job. Call the
[`Job.waitFor()`](/java/docs/reference/google-cloud-bigquery/latest/com.google.cloud.bigquery.Job#com_google_cloud_bigquery_Job_waitFor_com_google_cloud_RetryOption____)
method to wait for the DDL query to finish.

Before trying this sample, follow the Java setup instructions in the
[BigQuery quickstart using
client libraries](/bigquery/docs/quickstarts/quickstart-client-libraries).
For more information, see the
[BigQuery Java API
reference documentation](/java/docs/reference/google-cloud-bigquery/latest/overview).

To authenticate to BigQuery, set up Application Default Credentials.
For more information, see
[Set up authentication for client libraries](/bigquery/docs/authentication#client-libs).

```
import com.google.cloud.bigquery.BigQuery;
import com.google.cloud.bigquery.BigQueryException;
import com.google.cloud.bigquery.BigQueryOptions;
import com.google.cloud.bigquery.Job;
import com.google.cloud.bigquery.JobInfo;
import com.google.cloud.bigquery.QueryJobConfiguration;

// Sample to create a view using DDL
public class DDLCreateView {

  public static void runDDLCreateView() {
    // TODO(developer): Replace these variables before running the sample.
    String projectId = "MY_PROJECT_ID";
    String datasetId = "MY_DATASET_ID";
    String tableId = "MY_VIEW_ID";
    String ddl =
        "CREATE VIEW "
            + "`"
            + projectId
            + "."
            + datasetId
            + "."
            + tableId
            + "`"
            + " OPTIONS("
            + " expiration_timestamp=TIMESTAMP_ADD("
            + " CURRENT_TIMESTAMP(), INTERVAL 48 HOUR),"
            + " friendly_name=\"new_view\","
            + " description=\"a view that expires in 2 days\","
            + " labels=[(\"org_unit\", \"development\")]"
            + " )"
            + " AS SELECT name, state, year, number"
            + " FROM `bigquery-public-data.usa_names.usa_1910_current`"
            + " WHERE state LIKE 'W%'`";
    ddlCreateView(ddl);
  }

  public static void ddlCreateView(String ddl) {
    try {
      // Initialize client that will be used to send requests. This client only needs to be created
      // once, and can be reused for multiple requests.
      BigQuery bigquery = BigQueryOptions.getDefaultInstance().getService();

      QueryJobConfiguration config = QueryJobConfiguration.newBuilder(ddl).build();

      // create a view using query and it will wait to complete job.
      Job job = bigquery.create(JobInfo.of(config));
      job = job.waitFor();
      if (job.isDone()) {
        System.out.println("View created successfully");
      } else {
        System.out.println("View was not created");
      }
    } catch (BigQueryException | InterruptedException e) {
      System.out.println("View was not created. \n" + e.toString());
    }
  }
}
```

### Node.js

Before trying this sample, follow the Node.js setup instructions in the
[BigQuery quickstart using
client libraries](/bigquery/docs/quickstarts/quickstart-client-libraries).
For more information, see the
[BigQuery Node.js API
reference documentation](https://googleapis.dev/nodejs/bigquery/latest/index.html).

To authenticate to BigQuery, set up Application Default Credentials.
For more information, see
[Set up authentication for client libraries](/bigquery/docs/authentication#client-libs).

```
// Import the Google Cloud client library and create a client
const {BigQuery} = require('@google-cloud/bigquery');
const bigquery = new BigQuery();

async function ddlCreateView() {
  // Creates a view via a DDL query

  /**
   * TODO(developer): Uncomment the following lines before running the sample.
   */
  // const projectId = "my_project"
  // const datasetId = "my_dataset"
  // const tableId = "my_new_view"

  const query = `
  CREATE VIEW \`${projectId}.${datasetId}.${tableId}\`
  OPTIONS(
      expiration_timestamp=TIMESTAMP_ADD(
          CURRENT_TIMESTAMP(), INTERVAL 48 HOUR),
      friendly_name="new_view",
      description="a view that expires in 2 days",
      labels=[("org_unit", "development")]
  )
  AS SELECT name, state, year, number
      FROM \`bigquery-public-data.usa_names.usa_1910_current\`
      WHERE state LIKE 'W%'`;

  // For all options, see https://cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query
  const options = {
    query: query,
  };

  // Run the query as a job
  const [job] = await bigquery.createQueryJob(options);

  job.on('complete', metadata => {
    console.log(`Created new view ${tableId} via job ${metadata.id}`);
  });
}
```

### Python

Call the
[`Client.query()`](/python/docs/reference/bigquery/latest/google.cloud.bigquery.client.Client#google_cloud_bigquery_client_Client_query)
method to start a query job. Call the
[`QueryJob.result()`](/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJob#google_cloud_bigquery_job_QueryJob_result)
method to wait for the DDL query to finish.

Before trying this sample, follow the Python setup instructions in the
[BigQuery quickstart using
client libraries](/bigquery/docs/quickstarts/quickstart-client-libraries).
For more information, see the
[BigQuery Python API
reference documentation](/python/docs/reference/bigquery/latest).

To authenticate to BigQuery, set up Application Default Credentials.
For more information, see
[Set up authentication for client libraries](/bigquery/docs/authentication#client-libs).

```
# from google.cloud import bigquery
# project = 'my-project'
# dataset_id = 'my_dataset'
# table_id = 'new_view'
# client = bigquery.Client(project=project)

sql = """
CREATE VIEW `{}.{}.{}`
OPTIONS(
    expiration_timestamp=TIMESTAMP_ADD(
        CURRENT_TIMESTAMP(), INTERVAL 48 HOUR),
    friendly_name="new_view",
    description="a view that expires in 2 days",
    labels=[("org_unit", "development")]
)
AS SELECT name, state, year, number
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state LIKE 'W%'
""".format(
    project, dataset_id, table_id
)

job = client.query(sql)  # API request.
job.result()  # Waits for the query to finish.

print(
    'Created new view "{}.{}.{}".'.format(
        job.destination.project,
        job.destination.dataset_id,
        job.destination.table_id,
    )
)
```

## On-demand query size calculation

If you use on-demand billing, BigQuery charges for data definition
language (DDL) queries based on the number of bytes processed by the query.

| DDL statement | Bytes processed |
| --- | --- |
| `CREATE TABLE` | None. |
| `CREATE TABLE ... AS SELECT ...` | The sum of bytes processed for all the columns referenced from the tables scanned by the query. |
| `CREATE VIEW` | None. |
| `DROP TABLE` | None. |
| `DROP VIEW` | None. |

For more information about cost estimation, see [Estimate and control costs](/bigquery/docs/best-practices-costs).

## `CREATE SCHEMA` statement

Creates a new dataset.

**Key Point:** This SQL statement uses the term `SCHEMA` to refer to a logical
collection of tables, views, and other resources. The equivalent concept in
BigQuery is a *dataset*. In this context, `SCHEMA` does not refer
to BigQuery [table schemas](/bigquery/docs/schemas).

### Syntax

```
CREATE SCHEMA [ IF NOT EXISTS ]
[project_name.]dataset_name
[DEFAULT COLLATE collate_specification]
[OPTIONS(schema_option_list)]
```

### Arguments

* `IF NOT EXISTS`: If any dataset exists with the same name, the `CREATE`
  statement has no effect.
* `DEFAULT COLLATE collate_specification`: When a new table is created in the
  dataset, the table inherits a
  default [collation specification](/bigquery/docs/reference/standard-sql/collation-concepts#default_collation)
  unless a collation specification is explicitly specified for a table or a
  [column](#column_name_and_column_schema).

  If you remove or change this collation specification later with the
  `ALTER SCHEMA` statement, this will not change existing
  collation specifications in this dataset. If you want to update an existing
  collation specification in a dataset, you must alter the column that contains
  the specification.
* `project_name`: The name of the project where you are creating the dataset.
  Defaults to the project that runs this DDL statement.
* `dataset_name`: The name of the dataset to create.
* [`schema_option_list`](#schema_option_list): A list of options for creating
  the dataset.

### Details

The dataset is created in the location that you specify in the query settings.
For more information, see
[Specifying your location](/bigquery/docs/locations#specify_locations).

For more information about creating a dataset, see
[Creating datasets](/bigquery/docs/datasets). For information about quotas, see
[Dataset limits](/bigquery/quotas#dataset_limits).

### `schema_option_list`

The option list specifies options for the dataset. Specify the options in the
following format: `NAME=VALUE, ...`

The following options are supported:

| `NAME` | `VALUE` | Details |
| --- | --- | --- |
| `default_kms_key_name` | `STRING` | Specifies the default Cloud KMS key for encrypting table data in this dataset. You can override this value when you create a table. |
| `default_partition_expiration_days` | `FLOAT64` | Specifies the default expiration time, in days, for table partitions in this dataset. You can override this value when you create a table. |
| `default_rounding_mode` | `STRING` | Example: `default_rounding_mode = "ROUND_HALF_EVEN"`  This specifies the [`defaultRoundingMode`](/bigquery/docs/reference/rest/v2/datasets#Dataset.FIELDS.default_rounding_mode) that is used for new tables created in this dataset. It does not impact existing tables. The following values are supported:   * `"ROUND_HALF_AWAY_FROM_ZERO"`: Halfway cases are   rounded away from zero. For example, 2.25 is rounded to 2.3, and   -2.25 is rounded to -2.3. * `"ROUND_HALF_EVEN"`: Halfway cases are rounded towards   the nearest even digit. For example, 2.25 is rounded to 2.2 and   -2.25 is rounded to -2.2. |
| `default_table_expiration_days` | `FLOAT64` | Specifies the default expiration time, in days, for tables in this dataset. You can override this value when you create a table. |
| `description` | `STRING` | The description of the dataset. |
| `failover_reservation` | `STRING` | Associates the dataset to a reservation in the case of a failover scenario. |
| `friendly_name` | `STRING` | A descriptive name for the dataset. |
| `is_case_insensitive` | `BOOL` | `TRUE` if the dataset and its table names are case-insensitive, otherwise `FALSE`. By default, this is `FALSE`, which means the dataset and its table names are case-sensitive.  * Datasets: `mydataset` and `MyDataset` can   coexist in the same project, unless one of them has case-sensitivity   turned off. * Tables: `mytable` and `MyTable` can coexist in   the same dataset if case-sensitivity for the dataset is turned on. |
| `is_primary` | `BOOLEAN` | Declares if the dataset is the primary replica. |
| `labels` | `<ARRAY<STRUCT<STRING, STRING>>>` | An array of labels for the dataset, expressed as key-value pairs. |
| `location` | `STRING` | The location in which to create the dataset. If you don't specify this option, the dataset is created in the location where the query runs. If you specify this option and also explicitly set the location for the query job, the two values must match; otherwise the query fails. |
| `max_time_travel_hours` | `SMALLINT` | Specifies the duration in hours of the [time travel window](/bigquery/docs/time-travel#time_travel) for the dataset. The `max_time_travel_hours` value must be an integer expressed in multiples of 24 (48, 72, 96, 120, 144, 168) between 48 (2 days) and 168 (7 days). 168 hours is the default if this option isn't specified. |
| `primary_replica` | `STRING` | The replica name to set as the [primary replica](/bigquery/docs/data-replication). |
| `storage_billing_model` | `STRING` | Alters the [storage billing model](/bigquery/docs/datasets-intro#dataset_storage_billing_models) for the dataset. Set the `storage_billing_model` value to `PHYSICAL` to use physical bytes when calculating storage charges, or to `LOGICAL` to use logical bytes. `LOGICAL` is the default.  The `storage_billing_model` option is only available for datasets that have been updated after December 1, 2022. For datasets that were last updated before that date, the storage billing model is `LOGICAL`.  When you change a dataset's billing model, it takes 24 hours for the change to take effect.  Once you change a dataset's storage billing model, you must wait 14 days before you can change the storage billing model again. |
| `tags` | `<ARRAY<STRUCT<STRING, STRING>>>` | An array of IAM tags for the dataset, expressed as key-value pairs. The key should be the [namespaced key name](/iam/docs/tags-access-control#definitions), and the value should be the [short name](/iam/docs/tags-access-control#definitions). |

### Required permissions

This statement requires the following
[IAM permissions](/bigquery/docs/access-control#bq-permissions):

| Permission | Resource |
| --- | --- |
| `bigquery.datasets.create` | The project where you create the dataset. |

### Examples

#### Creating a new dataset