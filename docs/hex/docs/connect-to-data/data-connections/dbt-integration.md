On this page

# dbt Integrations

Hex pulls in your metadata and semantic models from dbt, enabling analytics engineers and business users to work closer together than ever.

## dbt Metadata integration[​](#dbt-metadata-integration "Direct link to dbt Metadata integration")

If you use dbt Cloud, Hex can use metadata from your [dbt](https://www.getdbt.com/) project to enrich the [Data browser](/docs/explore-data/data-browser) with additional information.

Hex will fetch the following information from your scheduled jobs in dbt Cloud:

* Model, source and column [descriptions](https://docs.getdbt.com/reference/resource-properties/description) and [tests](https://docs.getdbt.com/docs/building-a-dbt-project/tests)
* When the model was last updated
* Any source [freshness](https://docs.getdbt.com/docs/dbt-cloud/using-dbt-cloud/cloud-snapshotting-source-freshness) tests
* Links to the relevant page of your deployed docs site in dbt Cloud

Once the dbt integration is configured, tables in the Data browser that are part of a model or defined as a source in dbt will display their most recent job execution date, source freshness, and the status of any tests configured on the model.

This metadata will be refreshed automatically for all tables in a data connection associated with dbt models or sources whenever you perform a schema refresh, and only needs to be configured once per connection.

[](/assets/medias/new-schema-dbt-f6ef788e3bbba0b59acb132167a56ec1.mp4)

tip

If a new table has been added to a data connection, you will need to [refresh the Data browser](/docs/explore-data/data-browser#refresh-the-data-browser) in order to see the new table.

### Configure the dbt Metadata integration[​](#configure-the-dbt-metadata-integration "Direct link to Configure the dbt Metadata integration")

Compatibility Notice

Hex does not currently support Postgres with dbt 1.6+

Each data connection can be individually configured to integrate with dbt. From the [connection settings](/docs/connect-to-data/data-connections/data-connections-introduction), you can toggle on the **dbt Metadata** integration and provide your credentials. Hex will automatically find the relevant schemas and tables as modeled in dbt.

**Account ID**, **Project ID** and **Environment ID** can be most easily found in the URL of the "Environment" page for your project, following this structure: `https://cloud.getdbt.com/#/accounts/<ACCOUNT_ID>/projects/<PROJECT_ID>/jobs/environments/<ENVIRONMENT_ID>/`

For **dbt version 1.6+**, the Environment ID is required.

The service token must have both the "Metadata Only" and "Job Admin" permissions. To generate a service token:

1. Head to the Account Settings view in dbt Cloud.
2. Click the Service Account tokens page and select "New Token".
3. Name the token ("Hex dbt integration" is a good starting point), and add the "Metadata Only" and "Job Admin" permissions.
4. Add the the token to the Hex connection.

Note: After a token is generated, it won't be able to be viewed again so either add it to Hex immediately, or store it somewhere very safe!

### Supported connection types[​](#supported-connection-types "Direct link to Supported connection types")

* BigQuery
* Databricks
* PostgreSQL
* Redshift
* Snowflake

### Troubleshooting[​](#troubleshooting "Direct link to Troubleshooting")

If you're experiencing errors, check the error message by hovering over the warning icon in the Data browser.

| Error type | Troubleshooting |
| --- | --- |
| No jobs found for this project | The dbt Cloud integration pulls information from jobs invoked via the dbt Cloud Scheduler. Check that at least one job in dbt Cloud has the "generate docs" checkbox enabled ([more info](https://docs.getdbt.com/docs/dbt-cloud/using-dbt-cloud/cloud-generating-documentation)), and that it has been run successfully. |
| 401 Unauthorized | This error message often means the token provided on the connection is invalid, or does not have the correct permissions. To fix this, follow the steps in the above section on [Configuring the dbt integration](#configuring-the-dbt-integration) to create a new token. |
| All other errors | For all other errors, first check the [dbt Cloud status page](https://status.getdbt.com/) to see if there is an active issue. Then [contact dbt support](/cdn-cgi/l/email-protection#b4c7c1c4c4dbc6c0f4d3d1c0d0d6c09ad7dbd9) for more assistance. |

If you receive no errors on the dbt integration but don't see any dbt data coming through to the Data browser, check that:

* At least one job has been set up via the dbt Cloud scheduler
* At least one job meets the following criteria:
  + The "generate docs" checkbox is ticked
  + The job uses a command other than `dbt docs generate` (if you want to use a command that doesn't build anything in your warehouse, consider using `dbt list` or `dbt compile`)
  + The job has run successfully at least once, and docs have been produced as a result

## dbt Semantic layer integration (legacy)[​](#dbt-semantic-layer-integration-legacy "Direct link to dbt Semantic layer integration (legacy)")

warning

This is a legacy integration. Check out our new [integration with dbt MetricFlow](/docs/connect-to-data/semantic-models/semantic-model-sync/intro) to learn more about exploring your models in Hex.

Hex also integrates with dbt's MetricFlow integration to unlock the [dbt Semantic layer cell](/docs/explore-data/cells/data-cells/dbt-metrics-cells) and allow users to write SQL directly against their semantic layer. dbt now supports using their semantic layer for the following connection types:

* Snowflake
* BigQuery
* Redshift
* Databricks

### Configuring the dbt Semantic layer[​](#configuring-the-dbt-semantic-layer "Direct link to Configuring the dbt Semantic layer")

To turn on the dbt Semantic layer for your data connection:

1. First toggle on the **dbt** integration on your data connection configuration page and select what version you are using (1.5 & below, or 1.6+).
2. Follow the setup steps enumerated [here](https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl), making sure to save the service token generated in step 6.
3. In Hex, toggle on the **Use dbt Semantic layer** option and fill in access url, environment id, and service token as created above.

tip

If your data is behind a firewall, you'll need to configure your connection to allow traffic from dbt's [IP addresses](https://docs.getdbt.com/docs/cloud/about-cloud/regions-ip-addresses).

### Migrating from dbt's legacy semantic layer[​](#migrating-from-dbts-legacy-semantic-layer "Direct link to Migrating from dbt's legacy semantic layer")

dbt has made significant changes from v1.5 to 1.6 to accommodate for their new MetricFlow integration. Their legacy semantic layer integration will be deprecated later in 2023. Hex will continue to support legacy Metric cells with dbt Cloud versions <1.5 until dbt deprecates this functionality completely.

1. We recommend that you follow the migration guidelines provided by dbt for how to move from v1.5 to 1.6 in your dbt environment. See <https://docs.getdbt.com/guides/migration/sl-migration> for detailed instructions.
2. Create your new dbt deploy environment using dbt version 1.6 and generate the appropriate keys, as described above.
3. **Instead of updating any existing Hex data connection in place to use version 1.6 we recommend that you create a new data connection** using your dbt semantic layer 1.6+ details. dbt has made significant changes on how the semantic layer API works, thus if you update your data connections in place it is possible your existing SQL & Metric cells which reference that data connection will break. See the **known limitations** section below for more details on breaking changes associated with this migration.

### Known limitations when using v1.6+ dbt Semantic layer[​](#known-limitations-when-using-v16-dbt-semantic-layer "Direct link to Known limitations when using v1.6+ dbt Semantic layer")

* For dbt Cloud v1.6+, dbt uses their own JDBC driver to pass queries on to your database and that driver does not currently support prepared statements. This means that SQL parameterization is *not* supported for connections with the v1.6+ dbt Semantic layer enabled.
* The above limitation on parameterized SQL queries means that `ref` and source macros defined in your 1.6+ dbt environments are no longer supported in Hex SQL cells that use a data connection with the dbt Semantic layer integration enabled.
* The dbt Semantic layer cannot be enabled on connections using OAuth as the database authentication method.
* Snowpark and dbt Semantic layer cannot be enabled simultaneously on the same data connection. If you need to use both services you will need to configure two different data connections to the same database in order to access the functionalities of both features.

## FAQs[​](#faqs "Direct link to FAQs")

### Does Hex have an integration with dbt Core?[​](#does-hex-have-an-integration-with-dbt-core "Direct link to Does Hex have an integration with dbt Core?")

Not currently. Both the dbt Metadata and dbt Semantic layer integrations rely on features that are part of dbt Cloud (the [Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api) and [Semantic layer](https://docs.getdbt.com/docs/use-dbt-semantic-layer/dbt-sl) respectively).

However, the schema browser does pick up table and column descriptions from your data warehouse. One way to have the descriptions from your dbt project appear in Hex is to:

1. Set the `persist_docs` config to `true` in your dbt project ([docs](https://docs.getdbt.com/reference/resource-configs/persist_docs)). This will write your descriptions to your database as table and column comments.
2. Run your dbt project from any orchestrator.
3. Refresh the schema browser in a Hex project. Your descriptions should now appear in the schema browser.

Note that this will **not** populate other information about your dbt project, like tests and their statuses, and model build times.

#### On this page

* [dbt Metadata integration](#dbt-metadata-integration)
  + [Configure the dbt Metadata integration](#configure-the-dbt-metadata-integration)
  + [Supported connection types](#supported-connection-types)
  + [Troubleshooting](#troubleshooting)
* [dbt Semantic layer integration (legacy)](#dbt-semantic-layer-integration-legacy)
  + [Configuring the dbt Semantic layer](#configuring-the-dbt-semantic-layer)
  + [Migrating from dbt's legacy semantic layer](#migrating-from-dbts-legacy-semantic-layer)
  + [Known limitations when using v1.6+ dbt Semantic layer](#known-limitations-when-using-v16-dbt-semantic-layer)
* [FAQs](#faqs)
  + [Does Hex have an integration with dbt Core?](#does-hex-have-an-integration-with-dbt-core)