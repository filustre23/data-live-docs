On this page

# Connect to Databricks

Securely connect your Hex workspace to your Databricks database.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.
* Hex currently only supports the [legacy JDBC driver](https://docs.databricks.com/en/integrations/jdbc/legacy.html#legacy-databricks-jdbc-driver) where the JDBC URL starts with `jdbc:spark`.

[Databricks](https://www.databricks.com/) is a data analytics platform built on top of Apache Spark.

Databricks allows you to combine the robustness of a data warehouse with the flexibility of a data lake via their [lakehouse architecture](https://www.databricks.com/product/data-lakehouse). It provides a unified platform that offers a wide variety of services, allowing you to store and process large amounts of data quickly and efficiently, including real-time analytics.

Databricks can be especially useful for machine learning/artificial intelligence, data engineering, and data science applications.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Set up a [Databricks account](https://docs.databricks.com/aws/en/getting-started) and create a workspace if you don't already have one.
2. Create and configure a [Databricks warehouse](https://docs.databricks.com/en/compute/sql-warehouse/create-sql-warehouse.html).
3. Locate your [JDBC URL](https://docs.databricks.com/aws/en/integrations/jdbc/legacy#legacy-databricks-jdbc-driver).
4. Generate an [access token](https://docs.databricks.com/dev-tools/api/latest/authentication.html) in Databricks for a user with access to the data you want to query.
5. In Hex, go to **Settings** → **Data sources**.
6. Select **+ Connection**, select **Databricks**, and fill out the fields below.

You can authenticate with an **access token** (steps above) or with **OAuth** for per-user warehouse credentials.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.

2. **JDBC URL** ([instructions to locate](https://docs.databricks.com/aws/en/integrations/jdbc/legacy#legacy-databricks-jdbc-driver))
3. **Access token** ([instructions to generate](https://docs.databricks.com/dev-tools/api/latest/authentication.html))

## Additional settings[​](#additional-settings "Direct link to Additional settings")

The data connection form includes several optional sections:

* **Advanced** - Optional settings like [custom SQL formatting](/docs/explore-data/cells/sql-cells/sql-formatting), including schema data for AI, and [connecting via SSH](/docs/connect-to-data/data-connections/data-connections-introduction#database-security).
* **Access** - Optional [data connection permissions](/docs/connect-to-data/data-connections/data-connections-introduction#workspace-data-connection-permissions).
* **Schema browsing** - Recommended settings like [scheduling schema browser refreshes](/docs/connect-to-data/data-connections/data-connections-introduction#schema-refresh-schedules) and [schema filtering](/docs/connect-to-data/data-connections/data-connections-introduction#schema-filtering), both of which are recommended for performance and AI agent accuracy.

tip

If you use a firewall to restrict database access, you'll need to [add Hex's IP addresses to your allowlist](/docs/connect-to-data/data-connections/allow-connections-from-hex-ip-addresses).

## OAuth setup[​](#databricks-oauth-setup "Direct link to OAuth setup")

info

* Available on the **Enterprise** [plan](https://hex.tech/pricing).
* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to register OAuth apps and configure OAuth data connections.

OAuth requires each Hex user to authenticate to Databricks with their own credentials. Create a custom OAuth application in Databricks, register those client credentials in Hex as an OAuth app, then set a data connection's authentication type to **OAuth Token**. The host on the data connection must match the host on the app.

Connections with OAuth enabled can affect product behavior — [learn more](/docs/connect-to-data/data-connections/oauth-data-connections).

### Step 1: Create a custom OAuth application in Databricks[​](#step-1-create-a-custom-oauth-application-in-databricks "Direct link to Step 1: Create a custom OAuth application in Databricks")

A Databricks Admin enables a custom OAuth application and creates a `CLIENT_ID` and `CLIENT_SECRET`. Follow the [Databricks OAuth documentation](https://docs.databricks.com/en/integrations/enable-disable-oauth.html#enable-custom-oauth-applications-using-the-databricks-ui).

Set the allowed redirect URL to:

* Multi-tenant: `https://app.hex.tech/databricks-oauth-success`
* Single-tenant, EU, or HIPAA: `https://<YOUR-HEX-DOMAIN-NAME>/databricks-oauth-success`

### Step 2: Register the OAuth app in Hex[​](#step-2-register-the-oauth-app-in-hex "Direct link to Step 2: Register the OAuth app in Hex")

1. Go to **Settings → Data sources → OAuth apps**.
2. Select **App**, then **Databricks**.
3. Enter an **App name**, the **Databricks host** (`https://<your-databricks-instance>.cloud.databricks.com`), the **OAuth Client ID**, and the **OAuth Client secret**.
4. Select **Add app**. Hex opens the Databricks sign-in screen. After you sign in, the app is registered.

### Step 3: Update your data connection[​](#step-3-update-your-data-connection "Direct link to Step 3: Update your data connection")

Edit your Databricks data connection and set **Authentication type** to **OAuth Token**. The host on the data connection must match the host on the OAuth app. Configure [OAuth permissions](/docs/connect-to-data/data-connections/oauth-data-connections#credential-sharing) on the connection as needed.

#### On this page

* [How to get set up](#how-to-get-set-up)
* [Basic settings](#basic-settings)
* [Additional settings](#additional-settings)
* [OAuth setup](#databricks-oauth-setup)
  + [Step 1: Create a custom OAuth application in Databricks](#step-1-create-a-custom-oauth-application-in-databricks)
  + [Step 2: Register the OAuth app in Hex](#step-2-register-the-oauth-app-in-hex)
  + [Step 3: Update your data connection](#step-3-update-your-data-connection)