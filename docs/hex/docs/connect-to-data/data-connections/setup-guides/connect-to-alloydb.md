On this page

# Connect to AlloyDB (GCP)

Securely connect your Hex workspace to your AlloyDB (GCP) database.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

[AlloyDB](https://cloud.google.com/alloydb) is Google Cloud Platform (GCP)'s fully managed PostgreSQL-compatible database service designed for demanding transactional and analytical workloads. It's a true operational database (not just a query engine) that offers significantly faster performance than standard PostgreSQL—up to 4x faster for transactional workloads and up to 100x faster for analytical queries—while maintaining full PostgreSQL compatibility. AlloyDB uses a columnar engine for analytics alongside its row-based transactional engine, making it suitable for hybrid transactional/analytical processing (HTAP) use cases.

AlloyDB is ideal if you need PostgreSQL compatibility with enterprise-grade performance, particularly if you're running both operational applications and analytics on the same data. However, it's primarily optimized for transactional workloads with analytical capabilities as a bonus feature. If your primary use case in Hex is pure analytics on large datasets, purpose-built data warehouses like BigQuery, Snowflake, or Databricks may offer better performance and more analytical features. AlloyDB shines when you need to query operational data directly without ETL pipelines, or when PostgreSQL compatibility is a hard requirement for your organization.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Sign up for free [GCP / AlloyDB](https://cloud.google.com/alloydb) account if you don't have one.
2. Set up a Service User Account in Google Cloud.
3. In Hex, go to **Settings** → **Data sources**.
4. Click **+ Connection**, select **AlloyDB**, and fill out the fields below.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.

2. **Host** - The address of your AlloyDB database.
3. **Port** - The port used for secure native connections to your AlloyDB database.
4. **Username** - The AlloyDB service account username set up for usage by Hex.
5. **Password** - The AlloyDB service account password.

## Additional settings[​](#additional-settings "Direct link to Additional settings")

The data connection form includes several optional sections:

* **Advanced** - Optional settings like [custom SQL formatting](/docs/explore-data/cells/sql-cells/sql-formatting) and including schema data for AI.
* **Access** - Optional [data connection permissions](/docs/connect-to-data/data-connections/data-connections-introduction#workspace-data-connection-permissions).
* **Schema browsing** - Recommended settings like [scheduling schema browser refreshes](/docs/connect-to-data/data-connections/data-connections-introduction#schema-refresh-schedules) and [schema filtering](/docs/connect-to-data/data-connections/data-connections-introduction#schema-filtering), both of which are recommended for performance and AI agent accuracy.

tip

If you use a firewall to restrict database access, you'll need to [add Hex's IP addresses to your allowlist](/docs/connect-to-data/data-connections/allow-connections-from-hex-ip-addresses).

#### On this page

* [How to get set up](#how-to-get-set-up)
* [Basic settings](#basic-settings)
* [Additional settings](#additional-settings)