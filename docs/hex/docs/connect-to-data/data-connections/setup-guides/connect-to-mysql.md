On this page

# Connect to MySQL

Securely connect your Hex workspace to your MySQL database.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

[MySQL](https://www.mysql.com/) is one of the most popular open-source relational databases, designed primarily for transactional workloads powering web applications, content management systems, and e-commerce platforms. It's known for being fast, reliable, and straightforward to operate, with a massive ecosystem of tools and community support.

MySQL works best for accessing operational data in real-time or lightweight analytical needs. For Hex users with more intensive analytics workflows (e.g. complex queries, large aggregations), MySQL may yield slower performance.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. In Hex, go to **Settings** → **Data sources**.
2. Click **+ Connection**, select **MySQL**, and fill out the fields below.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.
2. **Host** - The address of your MySQL database.
3. **Port** - The port used for secure native connections to your MySQL database.
4. **Database** - The name of the MySQL database you're connecting.
5. **Aurora cluster (optional)** - Enable if connecting to an Aurora MySQL database cluster.
6. **Authentication type** - Choose Password or Certificate and fill out the required fields.

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