On this page

# Connect to RDS (AWS)

Securely connect your Hex workspace to Amazon RDS (AWS).

info

* Users need the **Admin** [workspace role](/docs/collaborate/sharing-and-permissions/roles) to create a shared **workspace data connection**.
* Users need **Can Edit** or higher [project permissions](/docs/collaborate/sharing-and-permissions/project-sharing#project-permissions) to create **project data connections**.
* Hex's RDS connection supports the **PostgreSQL** and **MySQL** database engines only.

[Amazon RDS](https://aws.amazon.com/rds/) (Relational Database Service) is an Amazon Web Services (AWS) managed relational database service that runs and operates relational database engines for you, handling provisioning, patching, backups, and scaling. RDS hosts engines such as PostgreSQL and MySQL, so it's a common home for operational data in AWS-native environments.

RDS is a good fit for connecting to Hex when your operational data already lives there and you need direct access for queries and visualizations. Because the underlying engines (e.g. Postgres, MySQL) are optimized for transactional processing (OLTP) rather than analytics (OLAP), performance can degrade with very large datasets and complex analytical queries.

## How to get set up[​](#how-to-get-set-up "Direct link to How to get set up")

1. Sign in to the [AWS RDS](https://aws.amazon.com/rds/) console, or create an account if you don't have one, and identify the RDS instance you want to connect to.
2. Set up the credentials Hex will use to access RDS. RDS connections authenticate with an **IAM role** that Hex assumes to obtain temporary credentials, so no long-lived secrets are stored in Hex. See [IAM role authentication](#iam-role-authentication) below.
3. In Hex, go to **Settings** → **Data sources**.
4. Click **+ Connection**, select **RDS**, then choose either **MySQL** or **Postgres** for your database engine.
5. Fill out the required fields.

## Basic settings[​](#basic-settings "Direct link to Basic settings")

1. **Name and Description** - Set a display name and optional description to help identify your data connection.
2. **Host** - The endpoint address of your RDS instance.
3. **Port** - The port used for secure native connections to your RDS instance.
4. **Database** - The name of the database you're connecting to.
5. **AWS region** - The AWS region your RDS instance runs in.

RDS connections authenticate with an IAM role. See [IAM role authentication](#iam-role-authentication) for the authentication fields and full setup.

## IAM role authentication[​](#iam-role-authentication "Direct link to IAM role authentication")

RDS connections authenticate with an IAM role. With IAM role authentication, you don't store long-lived AWS credentials in Hex. Instead, you create an IAM role in your AWS account and grant Hex's AWS principal permission to assume it. Hex calls `sts:AssumeRole` to obtain temporary credentials, scoped by an external ID.

1. **Create an IAM role in AWS**  
   In the AWS IAM console, create a new role with a policy granting the appropriate RDS access for your data connection and a placeholder trust policy. Copy the role's ARN.
2. **Save a draft connection in Hex**  
   In the RDS connection form, enter the **Role ARN** for the IAM role Hex should assume and the **database user** Hex connects as, then save the connection as a draft.
3. **Update the trust policy in AWS**  
   Hex generates the **external ID** and **IAM trust policy** when you save the draft. Copy them into your role's trust policy in AWS.
4. **Finalize the connection in Hex**  
   Return to the draft in Hex and complete the setup.

caution

Hex includes the external ID on `sts:AssumeRole` but **not** on `sts:TagSession`. If your trust policy applies an `sts:ExternalId` condition to *both* actions, validation fails with an `AccessDenied` error on `TagSession`. Split your trust policy into separate statements (with distinct SIDs) and apply the external ID condition to `sts:AssumeRole` only.

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
* [IAM role authentication](#iam-role-authentication)
* [Additional settings](#additional-settings)