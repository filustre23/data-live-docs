On this page

# Connect to BigQuery (GCP)

Securely connect your Hex workspace to your BigQuery (GCP) data warehouse.

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

[BigQuery](https://cloud.google.com/bigquery) is a great cloud data warehouse to get started with: they have a free tier, and it feels totally serverless: you don't have to worry about configuring instance or node sizes like you do with snowflake.

BigQuery is also good if you need to be HIPAA compliant and don't want to sign onerous enterprise licenses (for US-based healthcare companies). In short, we recommend using BigQuery if you have moderate amount of data to query and want to set up a cloud data warehouse.

If you have relatively small data and are very early, using something lightweight like Postgres or uploading csvs or parquet files to our DuckDB integration could also be good options.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Sign up for free [GCP / BigQuery](https://cloud.google.com/bigquery) account if you don't have one.
2. Set up a Service User Account in Google Cloud.
3. In Hex, go to **Settings** → **Data sources**.
4. Click **+ Connection**, select **BigQuery**, and fill out the fields below.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

#### 1. **Name** and Description[​](#1-name-and-description "Direct link to 1-name-and-description")

Set a display name and optional description to help identify your data connection.

#### 2. Project ID[​](#2-project-id "Direct link to 2. Project ID")

Enter your Google Cloud Project ID ([instructions to locate](https://support.google.com/googleapi/answer/7014113?hl=en)).

#### 3. Enable Google Drive access (optional)[​](#3-enable-google-drive-access-optional "Direct link to 3. Enable Google Drive access (optional)")

This setting enables querying Google Drive files in Hex via your BigQuery data connection. **Note that the service account you're using for this data connection must also be granted access to the Google Drive files.**

tip

If you see this error message when querying your BigQuery data connection, it could be due to your BigQuery data connection's service account not having the required Google Drive permissions, or due to the **Enable Google Drive access** setting being disabled on your BigQuery data connection.

`Access Denied: BigQuery BigQuery: Permission denied while getting Drive credentials`

#### 4. Use BigQuery Storage API (optional)[​](#4-use-bigquery-storage-api-optional "Direct link to 4. Use BigQuery Storage API (optional)")

This setting is toggled on by default as it drastically improves BigQuery performance in Hex for large queries. **To finish enabling BigQuery Storage API, two additional permissions must be granted to the service account:**

* `bigquery.readsessions.create`
* `bigquery.readsessions.getData`

Note that there may be some BigQuery costs associated with using BigQuery Storage API (See Google pricing details [here.](https://cloud.google.com/bigquery/pricing#data_extraction_pricing)).

#### 5. Service account configuration (JSON)[​](#5-service-account-configuration-json "Direct link to 5. Service account configuration (JSON)")

Paste the entire contents of a JSON Service Account Key file, which can be downloaded when creating the Service Account Key ([instructions to generate](https://cloud.google.com/iam/docs/creating-managing-service-account-keys#creating)).

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