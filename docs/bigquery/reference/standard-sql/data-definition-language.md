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