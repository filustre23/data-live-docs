On this page

# Connect to Postgres

Securely connect your Hex workspace to your Postgres database.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

[PostgresSQL](https://www.postgresql.org/) (Postgres) is a powerful open-source relational database designed primarily for transactional workloads like web applications, SaaS products, and operational systems. It's known for its reliability, SQL standards compliance, and support for advanced data types (JSON, arrays, geospatial). Postgres can run anywhere—on-premises, in the cloud, or as a managed service (AWS RDS, Google Cloud SQL, Azure Database)—making it one of the most widely deployed databases in the world.

Postgres is a good fit for connecting to Hex when your operational data already lives there and you need direct access for queries and visualizations. However, some performance limitations Hex users should consider include:

1. It's optimized for transactional processing (OLTP), not analytics (OLAP), so performance degrades with large datasets and complex analytical queries.
2. It scales vertically rather than horizontally, limiting its ability to handle growing analytical workloads.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. In Hex, go to **Settings** → **Data sources**.
2. Click **+ Connection**, select **Postgres**, and fill out the fields below.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.
2. **Host** - The address of your Postgres database.
3. **Port** - The port used for secure native connections to your Postgres database.
4. **Database** - The name of your Postgres database.
5. **Authentication** - Choose Password or Certificate and enter the required fields.

## Additional settings[​](#additional-settings "Direct link to Additional settings")

The data connection form includes several optional sections:

* **Advanced** - Optional settings like [custom SQL formatting](/docs/explore-data/cells/sql-cells/sql-formatting), including schema data for AI, and [connecting via SSH](/docs/connect-to-data/data-connections/data-connections-introduction#database-security).
* **Access** - Optional [data connection permissions](/docs/connect-to-data/data-connections/data-connections-introduction#workspace-data-connection-permissions).
* **Schema browsing** - Recommended settings like [scheduling schema browser refreshes](/docs/connect-to-data/data-connections/data-connections-introduction#schema-refresh-schedules) and [schema filtering](/docs/connect-to-data/data-connections/data-connections-introduction#schema-filtering), both of which are recommended for performance and AI agent accuracy.

tip

If you use a firewall to restrict database access, you'll need to [add Hex's IP addresses to your allowlist](/docs/connect-to-data/data-connections/allow-connections-from-hex-ip-addresses).

#### On this page

* [How to get set up](#how-to-get-set-up)
* [Basic settings](#basic-settings)
* [Additional settings](#additional-settings)