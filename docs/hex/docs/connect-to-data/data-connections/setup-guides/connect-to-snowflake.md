On this page

# Connect to Snowflake

Securely connect your Hex workspace to your Snowflake data warehouse.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

You can authenticate with a **key pair** (steps below) or with **OAuth** for per-user warehouse credentials.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Sign up for a [Snowflake account](https://signup.snowflake.com/) if you don't already have one.
2. Create a Snowflake user for usage by Hex.
3. Set up keypair authentication for your Snowflake user. See [Snowflake documentation on key pair authentication](https://docs.snowflake.com/en/user-guide/key-pair-auth#generate-the-private-keys).
4. In Hex, go to **Settings** → **Data sources**.
5. Select **+ Connection**, select **Snowflake**, and fill out the fields below.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.

2. **Account identifier** - Your Snowflake account identifier ([instructions to locate](https://docs.snowflake.com/en/user-guide/admin-account-identifier#finding-the-organization-and-account-name-for-an-account)). which can be found in the Snowflake URL, e.g. `account_identifier.snowflakecomputing.com`. If connecting via a proxy, specify the full proxy address and check the "proxy" box.
3. **Warehouse (optional for OAuth)** - Specifies the warehouse used to execute queries. If left blank, a default warehouse must be set for the user, which will then be used.
4. **Default database (optional)** - Specifying a default database allows you to reference schema and table names in your queries without needing to type the database name.
5. **Default schema (optional)** - Specifying a default schema allows you to reference table names in your queries without needing type the schema name.
6. **Username** - The username for the Snowflake user created for usage by Hex.
7. **Private key** - Must be a PEM encoded PKCS8 private key. Copy and paste the entire contents of your private key file.
8. **Private key passphrase (optional)** - Must match the passphrase of the private key. Leave this blank if no passphrase is set.
9. **User role (optional)** - If not specified, this will default to the Snowflake User's default role, if one exists.

tip

Paste the entire multi-line private key, including "-----BEGIN PRIVATE KEY-----" and "-----END PRIVATE KEY-----", in the **Private Key** box.

caution

As of April 2025, Snowflake will begin the first phase of [enforcing mandatory multi-factor authentication](https://www.snowflake.com/en/blog/blocking-single-factor-password-authentification/) on top of username & password.

Existing data connections authenticated using username & password authentication will fail once mandatory MFA is enabled for all Snowflake account types. To ensure seamless user access to Hex, it is highly recommended to switch to Key Pair authentication (username + private key).

## Additional settings[​](#additional-settings "Direct link to Additional settings")

The data connection form includes several optional sections:

* **Advanced** - Optional settings like [custom SQL formatting](/docs/explore-data/cells/sql-cells/sql-formatting) and including schema data for AI.
* **Access** - Optional [data connection permissions](/docs/connect-to-data/data-connections/data-connections-introduction#workspace-data-connection-permissions).
* **Schema browsing** - Recommended settings like [scheduling schema browser refreshes](/docs/connect-to-data/data-connections/data-connections-introduction#schema-refresh-schedules) and [schema filtering](/docs/connect-to-data/data-connections/data-connections-introduction#schema-filtering), both of which are recommended for performance and AI agent accuracy.

tip

If you use a firewall to restrict database access, you'll need to [add Hex's IP addresses to your allowlist](/docs/connect-to-data/data-connections/allow-connections-from-hex-ip-addresses).

## OAuth setup[​](#snowflake-oauth-setup "Direct link to OAuth setup")

info

* Available on the **Enterprise** [plan](https://hex.tech/pricing).
* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to configure OAuth data connections.

OAuth requires each Hex user to authenticate to Snowflake with their own credentials. Create the security integration in Snowflake, add the client credentials in Hex to create a workspace OAuth token, then set a data connection's authentication type to **OAuth Token**.

Connections with OAuth enabled can affect product behavior — [learn more](/docs/connect-to-data/data-connections/oauth-data-connections).

### Step 1: Create the security integration in Snowflake[​](#step-1-create-the-security-integration-in-snowflake "Direct link to Step 1: Create the security integration in Snowflake")

A Snowflake Account Admin must run the following SQL and retrieve the `CLIENT_ID` and `CLIENT_SECRET`.

```
USE ROLE ACCOUNTADMIN;



CREATE SECURITY INTEGRATION OAUTH_HEX



TYPE=OAUTH



ENABLED=TRUE



OAUTH_CLIENT = CUSTOM



OAUTH_CLIENT_TYPE='CONFIDENTIAL'



OAUTH_REDIRECT_URI='https://app.hex.tech/snowflake-oauth-success'



OAUTH_ISSUE_REFRESH_TOKENS = TRUE



OAUTH_REFRESH_TOKEN_VALIDITY = 7776000



OAUTH_ENFORCE_PKCE = TRUE;



select system$show_oauth_client_secrets('OAUTH_HEX');
```

Optionally allow default secondary roles in OAuth sessions:

```
OAUTH_USE_SECONDARY_ROLES = IMPLICIT
```

Notes:

* `OAUTH_REFRESH_TOKEN_VALIDITY` is set to 90 days in this example. Change it if you want users to re-authenticate on a different interval.
* If your Hex workspace is not hosted at `app.hex.tech`, update the host in `OAUTH_REDIRECT_URI`.
* The security integration name must match in both the `CREATE` statement and `system$show_oauth_client_secrets` (both `OAUTH_HEX` in this example).

See [Snowflake's OAuth documentation](https://docs.snowflake.com/en/user-guide/oauth-custom.html) for more detail.

### Step 2: Create the OAuth connection in Hex[​](#step-2-create-the-oauth-connection-in-hex "Direct link to Step 2: Create the OAuth connection in Hex")

1. Go to **Workspace Settings → Data sources**.
2. Find **Snowflake OAuth Connections** and select **+ Connection**.
3. Enter the Client ID and Client Secret from step 1, then follow the prompts to authenticate. You are redirected to the Snowflake login screen. After you authenticate, setup is complete.

caution

When authenticating with Snowflake, use an account whose default role is not `ACCOUNTADMIN`, `SECURITYADMIN`, or `ORGADMIN`. Snowflake blocks those roles from security integrations such as OAuth. See [Snowflake's documentation](https://docs.snowflake.com/en/user-guide/oauth-custom#blocking-specific-roles-from-using-the-integration).

### Step 3: Update a data connection[​](#step-3-update-a-data-connection "Direct link to Step 3: Update a data connection")

Edit a Snowflake data connection and set **Authentication type** to **OAuth Token**. Configure [OAuth permissions](/docs/connect-to-data/data-connections/oauth-data-connections#credential-sharing) on the connection as needed.

### Snowflake roles[​](#snowflake-roles "Direct link to Snowflake roles")

For Snowflake OAuth connections, you can set a **Snowflake role** on the data connection so only users who can assume that role in Snowflake can use it. Role names are case-sensitive.

In a project, the current role appears in the data connection details menu in the **Data sources** tab of the left sidebar. If no role is set in workspace settings, users can select **Switch Snowflake role...** to use a role they have already authenticated with, or authenticate with a new role.

[](/assets/medias/switch-snowflake-role-2896c7b8a172f4220d9f2511bff91ea2.mp4)

### Configure a service account[​](#creating-a-service-account-for-snowflake-oauth-connections "Direct link to Configure a service account")

Admins can attach a service account used for schema refreshes. A scoped service account keeps schema data consistent and controls how much metadata Hex syncs. Without a service account, schema data reflects the permissions of whoever last ran a [schema refresh](/docs/connect-to-data/data-connections/data-connections-introduction#configure-schema-browsing-settings).

info

A service account is required to [apply OAuth permissions to schema data](#applying-oauth-permissions-to-schema-data).

A Snowflake admin should:

1. Create a new user for the service account.
2. Assign roles with view access to every database, schema, table, and column you want synced to Hex (`USAGE` or higher).
3. Create a key pair for authentication.

tip

Depending on how Snowflake roles are structured, granting the service account access to existing roles may be enough. Otherwise, create additional roles so the account can see the full schema surface you want in Hex.

See [Snowflake access control](https://docs.snowflake.com/en/user-guide/security-access-control-overview) for more detail.

### Apply OAuth permissions to schema data[​](#applying-oauth-permissions-to-schema-data "Direct link to Apply OAuth permissions to schema data")

For Snowflake OAuth connections, you can apply each user's OAuth permissions to schema metadata. In the Data browser, users then only see schemas they can access.

To enable this, Admins must:

1. Turn on **Apply OAuth permissions to schema data**.
2. [Configure a service account](#creating-a-service-account-for-snowflake-oauth-connections) with `USAGE` (or higher) on every database, schema, table, and column you want synced.

Hex uses the service account's schema bounds as the outer set of objects, then filters that set per user based on their warehouse permissions.

tip

If a user has multiple Snowflake roles, the Data browser shows the combined privileges of their primary and secondary roles. Query access still depends on the role they authenticated with.

### No active warehouse error[​](#no-active-warehouse-error "Direct link to No active warehouse error")

When an Admin sets a warehouse on a Snowflake connection, every user who authenticates must have access to that warehouse. If a user's current Snowflake role cannot use that warehouse, SQL cells fail with a "no active warehouse" error.

If the warehouse field is blank, each user needs a default warehouse assigned in Snowflake, or they see the same error.

If the user lacks access to the warehouse on the data connection:

1. Have them run `select current_role()` to confirm the role in use.
2. Confirm which role is set on the Snowflake connection in **Settings → Data sources**.
3. Have a Snowflake admin grant that role access to the warehouse ([Snowflake docs](https://docs.snowflake.com/en/sql-reference/sql/grant-privilege)).

If the user has no default warehouse:

1. As the Snowflake user:
   * Run `select current_user` if you are unsure of the username.
   * Run `describe <my_user>` (for example, `describe helly_r`) to check for a default warehouse.
   * If none is set, run `alter user <my_user> set default_warehouse <my_warehouse>` (for example, `alter user helly_r set default_warehouse refining`).
2. Or ask a Snowflake admin to set a default warehouse for the user ([Snowflake docs](https://docs.snowflake.com/en/sql-reference/sql/alter-user)). Consider setting defaults for all users so individuals do not have to manage this themselves.

`use warehouse` statements inside a project do not fix this. Each SQL cell is a separate Snowflake session so queries can run in parallel.

#### On this page

* [How to get set up](#how-to-get-set-up)
* [Basic settings](#basic-settings)
* [Additional settings](#additional-settings)
* [OAuth setup](#snowflake-oauth-setup)
  + [Step 1: Create the security integration in Snowflake](#step-1-create-the-security-integration-in-snowflake)
  + [Step 2: Create the OAuth connection in Hex](#step-2-create-the-oauth-connection-in-hex)
  + [Step 3: Update a data connection](#step-3-update-a-data-connection)
  + [Snowflake roles](#snowflake-roles)
  + [Configure a service account](#creating-a-service-account-for-snowflake-oauth-connections)
  + [Apply OAuth permissions to schema data](#applying-oauth-permissions-to-schema-data)
  + [No active warehouse error](#no-active-warehouse-error)