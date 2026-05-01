On this page

# Connect to Athena (AWS)

Securely connect your Hex workspace to Athena (AWS).

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

caution

[Writeback](/docs/explore-data/cells/data-cells/writeback-cells) is not supported for Athena connections.

[Athena](https://aws.amazon.com/athena/) is an Amazon Web Services (AWS) SQL query engine that allows you to do analytics on files stored in S3 (Simple Storage Service). It's not really a database; it's a way to use SQL on CSV and parquet files stored in the cloud. Athena runs on a fork of the open source [Presto](https://prestodb.io/) project that was first developed at Meta (fka Facebook).

The advantage of Athena is that you can start querying data quickly if it's already stored in S3. The disadvantages are:

1. Because Athena is a query engine that can handle many different data formats, queries and reading schema metadata can be slow, which can affect performance in Hex.
2. Athena's query engine is more limited and doesn't support as many analytical features as alternatives like BigQuery, DuckDB or Snowflake (no offset queries, for example).

tip

Athena performance is highly dependent on how you choose to store your data. If you store carefully partitioned parquet files you may get reasonable performance. If you just store data in lots of large CSV files it might take minutes to query, which wouldn't be great for interactive exploration, even with Hex's caching. Amazon has a few good articles on tuning performance in [Athena](https://docs.aws.amazon.com/athena/latest/ug/performance-tuning.html).

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Login to the [AWS Athena](https://aws.amazon.com/athena/) console, or a create an account if you don't have one.
2. Create an AWS secret access key for the IAM user with appropriate Athena access for your data connection ([instructions to generate](https://aws.amazon.com/blogs/security/wheres-my-secret-access-key/)).

tip

* Currently only AWS users who do not use MFA authentication are supported.
* AWS uses the [AWSQuicksightAthenaAccess](https://docs.aws.amazon.com/athena/latest/ug/managed-policies.html#awsquicksightathenaaccess-managed-policy) policy as an example policy for JDBC connections. The IAM user will also need permissions to utilize [prepared statements](https://docs.aws.amazon.com/athena/latest/ug/security-iam-athena-prepared-statements.html).

3. Identify an S3 bucket to write query results to.
4. In Hex, go to **Settings** → **Data sources**.
5. Click **+ Connection**, select **Athena**, and fill out the required fields.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.
2. **Host and Port** - The default port is 443 and the host is `athena.[region].amazonaws.com` (if you're using a VPC to connect then the host address is `[vpc-specific-url].athena.[region].amazonaws.com`).
3. **S3 output path** - The S3 bucket to which results will be written (e.g. `s3://acmeco/athena_results`).
4. **Catalog (optional)** - The default catalog (data source) this connection should use. If no catalog is set, the default AwsDataCatalog will be used.
5. **Workgroup (optional)** - The workgroup to use for the connection. If left blank, the primary workgroup will be used.
6. **AWS secret access key ID** - The id for the secret access key for the IAM account that accesses Athena.
7. **AWS secret access key** - The secret access key for the IAM account that accesses Athena.

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