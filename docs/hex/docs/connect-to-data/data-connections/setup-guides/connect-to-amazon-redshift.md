On this page

# Connect to Redshift (AWS)

Securely connect your Hex workspace to Redshift (AWS).

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.

[Redshift](https://aws.amazon.com/pm/redshift) is an Amazon Web Services (AWS) cloud data warehouse built for large-scale analytics on structured data. It's a mature, feature-rich platform that integrates deeply with the AWS ecosystem (S3, Glue, QuickSight, etc.) and offers strong price-performance, especially if you're already invested in AWS. Redshift is columnar and optimized for complex analytical queries across petabytes of data, making it an ideal warehouse for intensive analytics workloads, especially if you're already AWS-native.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Sign in to the [AWS Redshift](https://aws.amazon.com/redshift/) console, or a create an account if you don't have one.
2. Create an AWS secret access key for the IAM user with appropriate Athena access for your data connection ([instructions to generate](https://aws.amazon.com/blogs/security/wheres-my-secret-access-key/)).

tip

Currently only AWS users who do not use MFA authentication are supported.

3. In Hex, go to **Settings** → **Data sources**.
4. Click **+ Connection**, select **Redshift**, and fill out the required fields.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.
2. **Host and Port** - The address of your Redshift database, and the port used for secure native connections to your Redshift database. The default port is 5439.
3. **Database** - The name of the Redshift database you're connecting to.
4. **Authentication type** - Choose your authentication type (Password or Certificate) and fill out the required fields.

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