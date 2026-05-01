On this page

# Connect to Microsoft SQL Server

Securely connect your Hex workspace to your Microsoft SQL Server database.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

[Microsoft SQL Server](https://www.microsoft.com/en-us/sql-server) is a traditional relational database management system (RDBMS) designed primarily for transactional workloads like enterprise applications, ERP systems, and line-of-business software. SQL Server can run on-premises, in Azure as Azure SQL Database, or as a managed instance, and includes features for business intelligence, reporting (SQL Server Reporting Services), and data integration (SQL Server Integration Services).

SQL Server is a good choice operational data already lives there and you need to query or visualize it directly, particularly for small to medium-sized datasets or departmental analytics. However, it does have some limitations for analytical use cases:

1. SQL Server is optimized for transactional processing (OLTP), not analytics (OLAP), so performance can suffer with large datasets, complex joins, or heavy aggregations.
2. Unlike modern cloud data warehouses, it doesn't scale elastically. You're constrained by the resources of your database instance, which can impact query performance in Hex when multiple users are running analyses.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Log into Microsoft SQL Server.
2. Set up a service account for usage by Hex ([instructions to create](https://learn.microsoft.com/en-us/sql/database-engine/configure-windows/configure-windows-service-accounts-and-permissions?view=sql-server-ver17)).
3. In Hex, go to **Settings** → **Data sources**.
4. Click **+ Connection**, select **Microsoft SQL Server**, and fill out the fields below.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.
2. **Host** - The address of your Microsoft SQL Server database.
3. **Port** - The port used for secure native connections to your Microsoft SQL Server database.
4. **Username** - The username for the Microsoft SQL Server service account.
5. **Password** - The password for the Microsoft SQL Server service account.

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