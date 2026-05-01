On this page

# Data connections introduction

Data connections are secure integrations between your database and your Hex workspace.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create workspace data connections.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create project data connections.

Hex makes it easy to securely connect to your database. Once you establish a data connection, you can query, transform, visualize, writeback, and use AI agents to analyze your data.

## Supported databases[​](#supported-databases "Direct link to Supported databases")

| Database | Setup Guide | OAuth | Support Tier |
| --- | --- | --- | --- |
| [AlloyDB (GCP)](https://cloud.google.com/products/alloydb) | [Connect to AlloyDB](/docs/connect-to-data/data-connections/setup-guides/connect-to-alloydb) | N/A | [3](/docs/connect-to-data/data-connections/data-connections-introduction#tier-3) |
| [Athena (AWS)](https://aws.amazon.com/athena/) | [Connect to Athena](/docs/connect-to-data/data-connections/setup-guides/connect-to-amazon-athena) | N/A | [2](/docs/connect-to-data/data-connections/data-connections-introduction#tier-2) |
| [BigQuery](https://cloud.google.com/bigquery) | [Connect to BigQuery](/docs/connect-to-data/data-connections/setup-guides/connect-to-bigquery) | [Supported](/docs/connect-to-data/data-connections/oauth-data-connections#bigquery-oauth-setup) | [1](/docs/connect-to-data/data-connections/data-connections-introduction#tier-1) |
| [Clickhouse](https://clickhouse.com/) | [Connect to Clickhouse](/docs/connect-to-data/data-connections/setup-guides/connect-to-clickhouse) | N/A | [1](/docs/connect-to-data/data-connections/data-connections-introduction#tier-1) |
| [CloudSQL (GCP)](https://cloud.google.com/sql) | [Connect to CloudSQL](/docs/connect-to-data/data-connections/setup-guides/connect-to-cloudsql) | N/A | [2](/docs/connect-to-data/data-connections/data-connections-introduction#tier-2) |
| [Databricks](https://www.databricks.com/) | [Connect to Databricks](/docs/connect-to-data/data-connections/setup-guides/connect-to-databricks) | [Supported](/docs/connect-to-data/data-connections/oauth-data-connections#databricks-oauth-setup) | [1](/docs/connect-to-data/data-connections/data-connections-introduction#tier-1) |
| [MariaDB](https://mariadb.org/) | [Connect to MariaDB](/docs/connect-to-data/data-connections/setup-guides/connect-to-mariadb) | N/A | [3](/docs/connect-to-data/data-connections/data-connections-introduction#tier-3) |
| [Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server) | [Connect to Microsoft SQL Server](/docs/connect-to-data/data-connections/setup-guides/connect-to-microsoft-sql-server) | N/A | [2](/docs/connect-to-data/data-connections/data-connections-introduction#tier-2) |
| [MotherDuck](https://motherduck.com/) | [Connect to MotherDuck](/docs/connect-to-data/data-connections/setup-guides/connect-to-motherduck) | N/A | [2](/docs/connect-to-data/data-connections/data-connections-introduction#tier-2) |
| [MySQL](https://www.mysql.com/) | [Connect to MySQL](/docs/connect-to-data/data-connections/setup-guides/connect-to-mysql) | N/A | [2](/docs/connect-to-data/data-connections/data-connections-introduction#tier-2) |
| [Postgres](https://www.postgresql.org/) | [Connect to Postgres](/docs/connect-to-data/data-connections/setup-guides/connect-to-postgres) | N/A | [2](/docs/connect-to-data/data-connections/data-connections-introduction#tier-2) |
| [Presto](https://prestodb.io/) | [Connect to Presto](/docs/connect-to-data/data-connections/setup-guides/connect-to-presto) | N/A | [3](/docs/connect-to-data/data-connections/data-connections-introduction#tier-3) |
| [Redshift (AWS)](https://aws.amazon.com/redshift/) | [Connect to Redshift](/docs/connect-to-data/data-connections/setup-guides/connect-to-amazon-redshift) | N/A | [2](/docs/connect-to-data/data-connections/data-connections-introduction#tier-2) |
| [Snowflake](https://www.snowflake.com/) | [Connect to Snowflake](/docs/connect-to-data/data-connections/setup-guides/connect-to-snowflake) | [Supported](/docs/connect-to-data/data-connections/oauth-data-connections#snowflake-oauth-setup) | [1](/docs/connect-to-data/data-connections/data-connections-introduction#tier-1) |
| [Starburst](https://www.starburst.io/) | [Connect to Starburst](/docs/connect-to-data/data-connections/setup-guides/connect-to-starburst) | N/A | [3](/docs/connect-to-data/data-connections/data-connections-introduction#tier-3) |
| [Trino](https://trino.io/) | [Connect to Trino](/docs/connect-to-data/data-connections/setup-guides/connect-to-trino) | N/A | [2](/docs/connect-to-data/data-connections/data-connections-introduction#tier-2) |

## Data connection support tiers[​](#data-connection-support-tiers "Direct link to Data connection support tiers")

To improve reliability, maintainability, and to bring clarity to users, Hex classifies all data connections into three tiers. These tiers help set expectations around support levels, stability, and feature completeness for each integration.

#### Tier 1[​](#tier-1 "Direct link to Tier 1")

Tier 1 data connectors are fully supported and actively maintained by Hex. They are tightly integrated into the Hex platform and are suitable for all production workflows. We prioritize improvements and bug fixes for Tier 1 data connectors.

#### Tier 2[​](#tier-2 "Direct link to Tier 2")

Tier 2 data connectors are stable, reliable, and fully supported by Hex, but they may not receive new features at the same time as Tier 1 data connectors. Feature support for these integrations can land after general availability (GA), based on feasibility and demand.

#### Tier 3[​](#tier-3 "Direct link to Tier 3")

Tier 3 data connectors are officially supported by Hex and usable in production, but we do not guarantee support of all platform features, like chart cells. There will be reduced coverage if any bugs or issues arise.

## Workspace and project data connections[​](#workspace-and-project-data-connections "Direct link to Workspace and project data connections")

Hex data connections can be created at the workspace level, or the project level.

* **Workspace data connections** can be used across multiple projects and are shared with all workspace members by default. Only Admins can create workspace-level data connections.
* **Project data connections** can be used only on the project from which they are created. Admins, Managers and Editors can create project-level data connections.

In general, we recommend using **workspace data connections** over project data connections. Workspace data connections can be reused across projects and are centrally managed by Admins, removing the need for non-Admins to have database credentials. Workspace data connections also support [automated schema refreshes](#schema-refresh-schedules) and [data connection permissions](#workspace-data-connection-permissions).

Admins on the [Enterprise plan](https://hex.tech/pricing) can [disable project-level data connections](/docs/administration/workspace_settings/workspace-security#project-data-connections).

## Create a data connection[​](#create-a-data-connection "Direct link to Create a data connection")

### Start a new data connection[​](#start-a-new-data-connection "Direct link to Start a new data connection")

Admins can create a workspace data connection from **Settings** → **Data sources** → **+ Connection**.

Alternatively, create a data connection from within your project by navigating to the **Data browser sidebar** → **Warehouse tab** in the Notebook view, and selecting **Add a data connection**.

Admins creating a data connection from a project will see the **Share with workspace** setting enabled by default, creating a workspace-level data connection. Non-Admins can create only project-level data connections.

### Enter database credentials[​](#enter-database-credentials "Direct link to Enter database credentials")

To create your Hex data connection you will need database credentials. If you don't have credentials, ask your database administrator for assistance.

1. Choose your database from the menu.
2. Fill in the required fields ([Find your database setup guide here](#supported-databases)).
3. Click **Create connection**.
4. If you use a firewall to restrict database access, you'll also need to [add Hex's IP addresses to your allowlist](/docs/connect-to-data/data-connections/allow-connections-from-hex-ip-addresses).

tip

Admins can save in-progress workspace data connections as a draft. Draft data connections can be accessed from **Settings** → **Data sources**.

### Configure schema browsing settings[​](#configure-schema-browsing-settings "Direct link to Configure schema browsing settings")

We recommend configuring **Schema browsing** settings to ensure the best performance and data discoverability for your workspace users and for AI.

#### Schema refresh schedules[​](#schema-refresh-schedules "Direct link to Schema refresh schedules")

info

* Scheduled refreshes are available only for [workspace data connections](#Workspace-and-project-data-connections).
* Schemas can also be refreshed manually by any user with [permissions](#can-refresh-schema) to do so.

Toggling on **Refresh data schema on a schedule** sets up a recurring refresh of the database, schema, table, and column metadata that will be visible in the [Data browser](/docs/explore-data/data-browser) to users and discoverable by AI agents. On refresh, Hex adds any new schema data available, and removes anything that was deleted. This helps ensure your workspaces users and AI agents have access to up-to-date metadata.

caution

Automated refreshes query your data connection's entire schema. Consider query costs and your data warehouse load when deciding on a cadence schedule.

#### Schema filtering[​](#schema-filtering "Direct link to Schema filtering")

**Schema filtering** limits the databases, schemas, and/or tables that are made visible to users and to AI agents in the [Data browser](/docs/explore-data/data-browser). This helps focus your workspace users on the relevant data assets, and helps improve AI agent accuracy. Filtering your schema also reduces the time required for schema refreshes, since schema refreshes will only sync non-filtered data objects.

caution

Filtering your connection does not affect the underlying permissions set in your data connection. Even if a database, schema, and/or table is hidden from the Data browser, it can still be queried from if the user has proper permissions to do so.

## Use data connections to query your database[​](#use-data-connections-to-query-your-database "Direct link to Use data connections to query your database")

Once your data connection is configured, you can query it using a [SQL cell](/docs/explore-data/cells/sql-cells/sql-cells-introduction#querying-data-with-sql-cells), explore your data with AI [threads](/docs/explore-data/threads), or analyze it with AI using the [notebook agent](/docs/connect-to-data/data-connections/docs/explore-data/notebook-view/notebook-agent). Note that new data connections will automatically kick off a schema refresh, which must complete before Hex agents can analyze it.

tip

Some Hex-native functionality, including [Query Mode](/docs/explore-data/cells/sql-cells/sql-cells-introduction#query-mode), [Pivot cells](/docs/explore-data/cells/transform-cells/pivot-cells), and [Table display cells](/docs/explore-data/cells/visualization-cells/table-display-cells), rely on modern CTE functionality when operating on data directly in your warehouse.

If you are using an older version of some data sources (such as `PostgreSQL<8.4`, `MySQL<8.0`, or `MS Sql Server<2005`), you will need to query your data into Hex and utilize these features locally, rather than pointing them directly to your warehouse.

## Workspace data connection permissions[​](#workspace-data-connection-permissions "Direct link to Workspace data connection permissions")

Workspace data connections offer additional permissions that can be used to restrict access to sensitive information.

### Can query[​](#can-query "Direct link to Can query")

This permission determines who can use the connection to author queries. By default, all members of a workspace are granted **Can query** access to a data connection.

This permission can be set to a list of [groups](/docs/administration/workspace_settings/overview#groups) to explicitly define which users can use this connection to author queries.

If this connection is imported in a project where a user with **Can edit** project access does not have **Can query** access to the data connection, the user will be prevented from authoring queries by being downgraded to **Can explore** project access.

If this connection is imported in a project where a user with **Can explore** project access does not have **Can query** access to the data connection, the user will not be able to explore from any cells in the published app. See [here](/docs/collaborate/sharing-and-permissions/project-sharing#unable-to-explore-from-a-published-app-due-to-missing-data-connection-permissions) for more details.

Users with **Can query** access to a data connection will be able to view the data connection and all its associated metadata in the [data browser](/docs/explore-data/data-browser).

Admins always have **Can query** access to data connections.

### Can view results[​](#can-view-results "Direct link to Can view results")

info

**Can view results** data permissions are only available on the Enterprise [plan](https://hex.tech/pricing).

This permission determines who can view the results of projects where this connection is imported, and can effectively be used to lock users out from projects.

By default, all users are granted **Can view results** access to a data connection, including any anonymous users if the project is [shared with the web](/docs/collaborate/sharing-and-permissions/project-sharing#share-to-web).

This permission can be set to a list of [groups](/docs/administration/workspace_settings/overview#groups) to explicitly define which users can view results when this data connection is used. Limiting **Can view results** access to any groups prevents users from attaching [screenshots](/docs/share-insights/app-notifications#attaching-screenshots) or [CSVs](/docs/share-insights/app-notifications#attaching-csv-data-exports) to notifications.

If this connection is imported in a project where a user with access to the project *does not* have **Can view results** access to the data connection, the user will be prevented from accessing the project.

Admins, and any groups that are granted **Can query** access always have **Can view results** access to a data connection.

### Can refresh schema[​](#can-refresh-schema "Direct link to Can refresh schema")

By default, all users that have [can query access](#can-query-access) can [manually refresh the data connection schema](/docs/explore-data/data-browser#refresh-the-data-browser) via the **Refresh** button in the data browser. To restrict this ability and only allow Admins to manually refresh the data browser, update the "Can refresh schema" setting in your data connection configuration to "Admins only".

## Database security[​](#database-security "Direct link to Database security")

For each data connection, it's possible to [configure SSH](/docs/connect-to-data/data-connections/connect-via-ssh) or [SSL/TLS](https://en.wikipedia.org/wiki/Transport_Layer_Security) for a more secure connection and encryption in transit.
For some data connection types, SSL/TLS is required.

Using Secure Socket Layer (SSL) or Transport Layer Security (TLS) provides an additional layer of security by encrypting data in transit that moves from Hex to your database instance. Some data connection types have SSL/TLS configured by default.

In the table below, `Enabled by default` indicates that creating a data connection with that database will have encryption in transit enabled by default, and no further action is required. If `Configurable`, please reference the documentation linked in the first column for instructions on how to configure SSL/TLS for that specific database.
`Required` means that Hex only supports connecting to an instance of the connection type if it has SSL enabled.

| Data Connection | SSL/TLS |
| --- | --- |
| [Postgres](https://www.postgresql.org/docs/current/encryption-options.html) | Required |
| [Athena](https://docs.aws.amazon.com/athena/latest/ug/encryption-in-transit.html) | Enabled by default |
| [BigQuery](https://cloud.google.com/bigquery/docs/reference/libraries-overview) | Enabled by default |
| [Databricks](https://docs.databricks.com/security/index.html) | Enabled by default |
| [Presto](https://prestodb.io/docs/current/security/internal-communication.html) | Enabled by default |
| [Redshift](https://docs.aws.amazon.com/redshift/latest/mgmt/connecting-ssl-support.html) | Enabled by default |
| [Snowflake](https://docs.snowflake.com/en/user-guide/security-encryption.html) | Enabled by default |
| [MotherDuck](https://motherduck.com/docs/authenticating-to-motherduck) | Enabled by default |
| [AlloyDB](https://cloud.google.com/alloydb/docs/auth-proxy/overview) | Configurable |
| [Clickhouse](https://clickhouse.com/docs/en/guides/sre/configuring-ssl/) | Configurable |
| [Cloud SQL (MySQL)](https://cloud.google.com/sql/docs/mysql/configure-ssl-instance) | Configurable |
| [Cloud SQL (PostgreSQL)](https://cloud.google.com/sql/docs/postgres/configure-ssl-instance) | Configurable |
| [Cloud SQL (SQL Server)](https://cloud.google.com/sql/docs/mysql/configure-ssl-instance) | Configurable |
| [MariaDB](https://mariadb.com/kb/en/securing-connections-for-client-and-server/) | Configurable |
| [MS SQL Server](https://learn.microsoft.com/en-US/sql/database-engine/configure-windows/configure-sql-server-encryption?view=sql-server-ver16) | Configurable |
| [MySQL](https://dev.mysql.com/doc/refman/8.0/en/encrypted-connections.html) | Configurable |
| [Trino](https://trino.io/docs/current/security/tls.html) | Configurable |
| [Starburst](https://docs.starburst.io/latest/security/tls.html) | Configurable |

#### On this page

* [Supported databases](#supported-databases)
* [Data connection support tiers](#data-connection-support-tiers)
* [Workspace and project data connections](#workspace-and-project-data-connections)
* [Create a data connection](#create-a-data-connection)
  + [Start a new data connection](#start-a-new-data-connection)
  + [Enter database credentials](#enter-database-credentials)
  + [Configure schema browsing settings](#configure-schema-browsing-settings)
* [Use data connections to query your database](#use-data-connections-to-query-your-database)
* [Workspace data connection permissions](#workspace-data-connection-permissions)
  + [Can query](#can-query)
  + [Can view results](#can-view-results)
  + [Can refresh schema](#can-refresh-schema)
* [Database security](#database-security)