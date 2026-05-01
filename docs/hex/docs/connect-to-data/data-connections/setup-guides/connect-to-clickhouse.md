On this page

# Connect to ClickHouse

Securely connect your Hex workspace to your ClickHouse database.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

[ClickHouse](https://clickhouse.com/) is an open-source column-oriented database management system (DBMS) optimized for online analytical processing (OLAP). It's designed to enable fast, real-time data analysis. ClickHouse achieves its speed and efficiency by employing column-based storage, vectorized query execution, and a range of other data processing optimizations.

You might want to use ClickHouse in scenarios that involve querying and processing large volumes of data. This could include analyzing logs, performing real-time analytical processing, processing time-series data, and running full-text searches, among other uses. It is often used in cases where real-time data analysis is critical.

If you have relatively small data or are very early, using something lightweight like Postgres or uploading csvs or parquet files to our DuckDB integration could also be good options.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Set up a ClickHouse database, either by hosting it on your own infrastructure or signing up for [ClickHouse Cloud](https://clickhouse.com/).
2. Set up a Clickhouse username and password for usage by Hex.
3. In Hex, go to **Settings** → **Data sources**.
4. Click **+ Connection**, select **ClickHouse**, and fill out the fields below.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.

2. **Host** - The address of your Clickhouse database.
3. **Port** - The port used for secure native connections to your ClickHouse database. This is usually 9440 (see [Clickhouse documentation](https://clickhouse.com/docs/guides/sre/network-ports)).
4. **Username** - The Clickhouse username set up for usage by Hex.
5. **Password** - The Clickhouse password.

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