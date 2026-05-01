On this page

# Connect to MotherDuck

Securely connect your Hex workspace to your MotherDuck database.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

[MotherDuck](https://motherduck.com/) is a serverless analytics platform built on DuckDB. It combines DuckDB's exceptional speed for analytical queries with cloud-based storage and compute, allowing you to run analytics on data in cloud object storage (S3, GCS) or MotherDuck's managed storage. The key advantage is inheriting DuckDB's performance and rich SQL features while adding collaboration capabilities and automatic scaling without managing infrastructure.

MotherDuck is ideal for ad-hoc analysis and data exploration on moderately sized datasets (up to several terabytes) at lower cost than traditional cloud warehouses. It's best suited for analytical workloads, not high-concurrency transactions or real-time data ingestion at scale.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Create a free [MotherDuck](https://motherduck.com/) account if you don't already have one.
2. Generate a MotherDuck access token ([instructions to generate](https://motherduck.com/docs/key-tasks/authenticating-and-connecting-to-motherduck/authenticating-to-motherduck/#creating-an-access-token)).
3. In Hex, go to **Settings** → **Data sources**.
4. Click **+ Connection**, select **MotherDuck**, and fill out the fields below.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.
2. **MotherDuck Token** - Your MotherDuck access token ([instructions to generate](https://motherduck.com/docs/key-tasks/authenticating-and-connecting-to-motherduck/authenticating-to-motherduck/#creating-an-access-token)).
3. **Default database (optional)** - This allows you to query schemas and tables from Hex without needing to type the default database name in your SQL query.

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