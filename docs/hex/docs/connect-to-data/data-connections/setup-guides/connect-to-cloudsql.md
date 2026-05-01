On this page

# Connect to CloudSQL

Securely connect your Hex workspace to your CloudSQL (GCP) data warehouse.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

[CloudSQL](https://cloud.google.com/sql) Google Cloud Platform (GCP)'s fully managed relational database service that supports MySQL, PostgreSQL, and SQL Server. It's designed primarily for transactional workloads—think web applications, e-commerce sites, and line-of-business applications—rather than large-scale analytics. Cloud SQL handles routine database management tasks like backups, replication, and patches automatically, making it easy to run traditional relational databases in the cloud without managing infrastructure.

CloudSQL is a good fit if you're running operational applications on GCP and need to query or visualize transactional data in Hex. However, it has some limitations with analytics workflows:

1. Performance can degrade significantly with large datasets or complex analytical queries since it's built for transactional processing;
2. You're limited by the compute and storage of a single database instance, unlike purpose-built data warehouses that scale horizontally.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Sign up for free [GCP / CloudSQL](https://cloud.google.com/sql) account if you don't have one.
2. Set up a Service User Account in Google Cloud.
3. In Hex, go to **Settings** → **Data sources**.
4. Click **+ Connection**, select **CloudSQL**, and fill out the fields below.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1.**Database type** - Select your database type

2. **Name and Description** - Set a display name and optional description to help identify your data connection.

2. **Host** - The address of your CloudSQL database.
3. **Port** - The port used for secure native connections to your CloudSQL database.
4. **Authentication** - Choose your authentication method, if applicable (username and password, or certificate). Then fill out the required fields.

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