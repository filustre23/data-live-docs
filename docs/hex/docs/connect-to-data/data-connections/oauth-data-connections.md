On this page

# OAuth data connections

Require users to authenticate to your data warehouse with their own credentials using OAuth data connections.

info

* Available on the **Enterprise** [plan](https://hex.tech/pricing).
* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to configure OAuth data connections.

OAuth data connections require each Hex user to sign in to the warehouse with their own credentials on a regular basis. Hex stores an access token per user and uses it when that person runs queries, allowing data warehouse admins to understand who ran which query, and enforce warehouse permissions.

Supported warehouses:

* [Snowflake](/docs/connect-to-data/data-connections/setup-guides/connect-to-snowflake#snowflake-oauth-setup)
* [Databricks](/docs/connect-to-data/data-connections/setup-guides/connect-to-databricks#databricks-oauth-setup)
* [BigQuery](/docs/connect-to-data/data-connections/setup-guides/connect-to-bigquery#bigquery-oauth-setup)

Warehouse-specific setup instructions can be found in the above guides. This page covers how OAuth behaves in Hex: how Admins configure it, and how Editors and app viewers use it day to day.

tip

You should only enable OAuth for a data connection if each Hex user who will run queries against that connection has their own user account in the warehouse.

If some Viewers do not have warehouse accounts, you can [allow embedding publisher credentials](#published-app-view) so they can still open published apps. If Explorers or Editors also lack warehouse accounts, use a shared service-account connection instead.

## How OAuth works in Hex[​](#how-oauth-works-in-hex "Direct link to How OAuth works in Hex")

When OAuth is enabled for a connection, users will have to authenticate to your data warehouse before running queries.

OAuth connections can run each query under a user's warehouse identity, so warehouse permissions apply in Hex. Connections can also be configured so that results are scoped to a user, preventing outputs leaking between users. However this impacts collaboration, sharing, and performance.

## Configure OAuth permissions[​](#credential-sharing "Direct link to Configure OAuth permissions")

On each OAuth data connection, the **OAuth permissions** section controls who runs queries and how results can be shared.

### Authoring queries[​](#notebook-view "Direct link to Authoring queries")

Choose whose warehouse identity is used when people author and run queries in a draft project or Thread:

* **Require personal credentials**: Everyone must use their own credentials when running the draft project or Thread.
* **Use owner's credentials**: Everyone authors and runs queries as the project or Thread owner and sees the same outputs.

We strongly recommend **requiring personal credentials**, as using the owner's credentials can lead to users authoring queries that return data the user doesn't normally have access to.

info

In the past, this setting (labeled **notebook credential sharing**) impacted how users collaborated when building and sharing notebooks and Threads. Going forward, this setting only determines whose credentials are used when running queries — restrictions on collaboration are instead determined by whether [user-scoped results](#user-scoped-results) is enabled.

**Use owner's credentials** will be deprecated in the near-future.

### Running published apps[​](#published-app-view "Direct link to Running published apps")

Choose whose credentials are used when someone opens a published app:

* **Require personal credentials**: Everyone must use their own credentials when running the published app.
* **Allow embedding publisher credentials**: Users with **Can Edit** permissions can choose whether to embed their credentials when publishing. When credentials are embedded, app viewers run queries as the publisher.

When embedding is allowed, the publisher chooses whether to include credentials under **Published app → Run settings**. That choice can change on every republish. The default is **Off** (do not embed publisher credentials).

When publisher credentials are embedded:

* App viewers can open and run the app without authenticating to the warehouse.
* Runs use the publisher's token.
* If that token expires, viewers see an error asking them to contact the publisher. See [Expired app credentials](#expired-app-credentials).

When the connection **requires personal credentials** for published apps:

* Every viewer must authenticate and use their own token.
* Viewers without an active token are prompted to sign in when they open the app.

info

In the past, this setting (labeled **app credential sharing**) impacted sharing of app results, and performance. Going forward, this setting only determines whose credentials are used when running apps — restrictions on sharing are instead determined by whether [user-scoped results](#user-scoped-results) is enabled.

We recommend **requiring personal credentials** unless some viewers in your workspace do not have access to your warehouse.

### User-scoped results[​](#user-scoped-results "Direct link to User-scoped results")

By default, Hex is a collaborative, multiplayer product. However, when users authenticating to the same data connection have different levels of access in the warehouse, you may decide to lock down collaboration and sharing so that sensitive data does not leak between these users.

When personal credentials are required, you can set **User-scoped results** to:

* **Off** (default): Users keep personal warehouse credentials, and outputs can be viewed and reused across users.
* **On**: Results are isolated between users, and outputs are not shared, cached, or reused across users.

This setting only applies when using personal credentials. If credentials are being shared, results will **not** be scoped to the user, regardless of this setting.

warning

Enabling user-scoped results impacts many of the collaboration, sharing and performance features of Hex, as described below.

#### Impacts of user-scoped results[​](#impacts-of-user-scoped-results "Direct link to Impacts of user-scoped results")

**Notebooks**

* Only one editor can be active at a time.
* Other users with **Can Edit** can select **Take over session** from the banner at the top of the project. Taking over restarts the kernel so the new user's token is used, and the previous editor's results are not accessible.
* While one editor is active, other users do not see cell outputs.

**Threads**

* Threads cannot be shared with other users in the workspace. See [OAuth and Threads](/docs/explore-data/threads#oauth-and-threads).

**Published apps**

* App results and default states are **per user**, not shared across viewers.
  + The first time a user visits an app (or visits after a new version is published), the app runs in their session and a background run populates that user's cache. Later visits use that user's cached state.
  + This leads to overall slower execution times since there is no shared cached state.
* App session links are not shareable.
* Users cannot create snapshots.
* The run log only shows each user's own app runs, including scheduled runs.
* Scheduled runs only update that schedule owner's cached results — not other users' caches. See [Scheduled runs](#scheduled-runs).

**Caching**

* [Query caching](/docs/explore-data/cells/sql-cells/query-caching#adjusting-cache-settings) is per user/token. One user's cached results are not reused for another user. This results in overall slower execution as there are fewer cache hits.

### Recommended configuration[​](#recommended-configuration "Direct link to Recommended configuration")

For better visibility into who ran queries, and to ensure users do not author queries against data they don't normally have access to in the warehouse, we recommend **requiring personal credentials**.

To enable collaboration and easier sharing in Hex, we recommend disabling **user-scoped results**.

If you are sensitive to results being shared between users that have varying access in the warehouse, we then recommend that:

1. Each user authenticating into the data connection has access to the same set of tables in your warehouse. For Snowflake OAuth connections, you can often achieve this by setting a role as part of the connection details. **This will add a restriction such that only users who can authenticate with Snowflake using the specified role can use the data connection.** This will likely result in you configuring multiple data connections for a workspace.
2. Leverage data connection permissions to limit the connection to users who have access to those tables. If you use a SCIM provider to configure your warehouse permissions, consider pulling that group through to Hex and using it for data connection permissions.

With this setup:

* Collaboration, sharing, and performance are better than when results are scoped to individual users.
* Users cannot gain access to data they don't have access to in the warehouse, as a result of data connection permissions.
* Users will not hit errors due to missing warehouse permissions when running apps, since they have the same access as other users that can use the app.
* Users will not hit "expired credential" error states that they can't resolve, as credentials will not be embedded.
* Warehouse admins have full visibility into who ran queries, and users authenticate at a regular frequency.

### Support access[​](#support-access "Direct link to Support access")

When you share a project with Hex support via **? → Share with support**, the support user inherits the project owner's OAuth credentials regardless of OAuth permission settings. Support uses those credentials only to help your users when requested.

### Roll out OAuth[​](#roll-out-oauth "Direct link to Roll out OAuth")

After you choose OAuth permission settings, pick how to cut over:

1. **Update an existing connection in place**  
   Projects keep using the same connection and pick up OAuth automatically. Expect temporary failures until users authenticate for the first time. Scheduled runs may fail until the owner refreshes credentials. If published apps require personal credentials, app viewers must authenticate on their next visit.
2. **Create a new OAuth connection**  
   New projects can default to the OAuth connection while existing projects keep working on the old service account connection. Migrating older projects means updating SQL cell sources to the new connection. The old connection remains available unless you restrict or remove it.

Use the **Usage** links on a data source in **Settings → Data sources** to see which projects use a connection.

## Using an OAuth connection as a Hex user[​](#using-an-oauth-connection-as-a-hex-user "Direct link to Using an OAuth connection as a Hex user")

### Sign in and refresh tokens[​](#sign-in-and-refresh-tokens "Direct link to Sign in and refresh tokens")

If you run a query against an OAuth connection without a valid token, Hex shows an **Expired** header on the SQL cell and prompts you to authenticate.

Review, refresh, and revoke tokens in **Settings → Connected Apps**, including when each token was created and when it expires. For Snowflake connections with credentials embedded in a published app, Hex also sends email and/or Slack warnings before expiry (typically 72 hours and again 24 hours beforehand). See [Expired app credentials](#expired-app-credentials).

### Checking OAuth settings for a notebook or app[​](#checking-oauth-settings-for-a-notebook-or-app "Direct link to Checking OAuth settings for a notebook or app")

Editors can open an OAuth summary in the notebook for connections in use.

App viewers can open an OAuth summary from the app menu to see whose token is in use.

### Take over a notebook session[​](#take-over-a-notebook-session "Direct link to Take over a notebook session")

When personal credentials are required and **User-scoped results** is **On**, only one editor can be active at a time. Select **Take over session** from the banner at the top of the project to restart the kernel with your token. The previous editor's results are not accessible after a take-over.

### Published apps: sign in vs embedded credentials[​](#published-apps-sign-in-vs-embedded-credentials "Direct link to Published apps: sign in vs embedded credentials")

When the connection **requires personal credentials** for published apps, viewers without an active token are prompted to sign in when they open the app.

When publisher credentials are embedded, viewers can run the app without signing in to the warehouse. If those credentials expire, users can hit an error state — see [expired app credentials](#expired-app-credentials).

### Threads, and AI features[​](#threads-and-ai-features "Direct link to Threads, and AI features")

* **Threads** — Threads follow the connection's authoring setting. Sharing is restricted when personal credentials are required and **User-scoped results** is **On**. See [OAuth and Threads](/docs/explore-data/threads#oauth-and-threads).
* **Hex's AI features** — AI features do not filter schema suggestions to the user's permissions. They may propose a query that references a table the user cannot access; that query errors and returns no results. For highly sensitive schemas, use a private data connection instead.

### Scheduled runs[​](#scheduled-runs "Direct link to Scheduled runs")

When an app uses personal credentials, and **User-scoped results** is **On**:

* The run log only shows each user's own scheduled runs.
* Scheduled runs only update the schedule owner's cached results — not other users' caches.
* Scheduled run notifications do not include screenshots.

When **User-scoped results** is **Off**, scheduled runs behave like other data connections: they can update shared published results, and notifications can include screenshots.

### Query caching[​](#query-caching "Direct link to Query caching")

* When users share owner or publisher credentials, or when **User-scoped results** is **Off**, [query caching](/docs/explore-data/cells/sql-cells/query-caching#adjusting-cache-settings) behaves like any other data connection.
* When personal credentials are required and **User-scoped results** is **On**, cache is per user/token.

## Known limitations[​](#known-limitations "Direct link to Known limitations")

* **Data browser** — Without per-user schema filtering, schema metadata can be shared across users. Someone with more restrictive warehouse permissions may see table names they cannot query if another user with broader access refreshed the [Data browser](/docs/explore-data/data-browser#refresh-the-data-browser). They still cannot query that data. For Snowflake, [apply OAuth permissions to schema data](/docs/connect-to-data/data-connections/setup-guides/connect-to-snowflake#applying-oauth-permissions-to-schema-data) and [configure a service account](/docs/connect-to-data/data-connections/setup-guides/connect-to-snowflake#creating-a-service-account-for-snowflake-oauth-connections) so refreshes stay consistent.
* **Notion embedded project previews** — Embedding a project that uses a restricted Snowflake OAuth connection can expose project results to anyone who opens the Notion page. See [Notion embed permissions](/docs/share-insights/embedding/public-and-private-embedding#how-do-permissions-work-for-notion-link-previews).
* **Hex's AI features** — Schema suggestions are not filtered to the user's permissions. Queries still fail if the user cannot access the underlying tables. Prefer a private connection for highly sensitive schemas.
* **Importing OAuth connections** — When authoring uses the owner's credentials, only the project owner can import OAuth connections. Editors need the owner to add the connection or transfer ownership first.

## Troubleshooting and FAQ[​](#troubleshooting-and-faq "Direct link to Troubleshooting and FAQ")

### Errors due to warehouse access[​](#errors-due-to-warehouse-access "Direct link to Errors due to warehouse access")

When personal credentials are required, each query runs with that user's warehouse permissions. This can result in errors if the authenticated user cannot read one or more tables, schemas, or columns referenced by the query.

Common causes:

* The project or app was authored by someone with broader warehouse access than the person running it.
* Warehouse roles or grants differ across users (or the connection does not pin a shared role).
* [Hex's AI features](#threads-and-ai-features) suggested a table the user cannot access.
* The [Data browser](/docs/explore-data/data-browser#refresh-the-data-browser) showed a table name from another user's schema refresh that this user cannot query.

What to do:

1. Confirm you are signed in with the expected warehouse account under **Settings → Connected Apps**.
2. Check whose token is in use from the [OAuth summary](#checking-oauth-settings-for-a-notebook-or-app).
3. Ask a warehouse admin to grant the missing access, or rewrite the query to use objects you can access.
4. If this happens often on shared apps or projects, ask a Hex Admin to follow the [recommended configuration](#recommended-configuration): align warehouse access for users on the connection, and restrict the connection with [data connection permissions](/docs/connect-to-data/data-connections/data-connections-introduction#workspace-data-connection-permissions).

If users should not share results when their warehouse access differs, enable [user-scoped results](#user-scoped-results) so outputs stay isolated. That does not remove permission denied errors for users who lack access, but it prevents one user's results from being visible to another.

### Expired app credentials[​](#expired-app-credentials "Direct link to Expired app credentials")

OAuth tokens expire after a set period (based on how the warehouse OAuth integration is configured).

If a publisher's credentials are embedded in an app and those credentials expire, the app stops working.

For Snowflake OAuth, the publisher receives email and/or Slack warnings before expiry (typically 72 hours and again 24 hours beforehand).

To fix this, ask the publisher to refresh their credentials in **Settings → Connected Apps** (or by re-authenticating when prompted).

If the publisher is unavailable, ask another user with **Can Edit** permissions to republish the project with their credentials embedded instead. You may need to ask an Admin to grant another user **Can Edit** access first.

### No active warehouse error[​](#no-active-warehouse-error "Direct link to No active warehouse error")

For Snowflake OAuth connections, see [No active warehouse error](/docs/connect-to-data/data-connections/setup-guides/connect-to-snowflake#no-active-warehouse-error).

#### On this page

* [How OAuth works in Hex](#how-oauth-works-in-hex)
* [Configure OAuth permissions](#credential-sharing)
  + [Authoring queries](#notebook-view)
  + [Running published apps](#published-app-view)
  + [User-scoped results](#user-scoped-results)
  + [Recommended configuration](#recommended-configuration)
  + [Support access](#support-access)
  + [Roll out OAuth](#roll-out-oauth)
* [Using an OAuth connection as a Hex user](#using-an-oauth-connection-as-a-hex-user)
  + [Sign in and refresh tokens](#sign-in-and-refresh-tokens)
  + [Checking OAuth settings for a notebook or app](#checking-oauth-settings-for-a-notebook-or-app)
  + [Take over a notebook session](#take-over-a-notebook-session)
  + [Published apps: sign in vs embedded credentials](#published-apps-sign-in-vs-embedded-credentials)
  + [Threads, and AI features](#threads-and-ai-features)
  + [Scheduled runs](#scheduled-runs)
  + [Query caching](#query-caching)
* [Known limitations](#known-limitations)
* [Troubleshooting and FAQ](#troubleshooting-and-faq)
  + [Errors due to warehouse access](#errors-due-to-warehouse-access)
  + [Expired app credentials](#expired-app-credentials)
  + [No active warehouse error](#no-active-warehouse-error)