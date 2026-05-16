* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# Data control language (DCL) statements in GoogleSQL

The BigQuery data control language (DCL) statements let you set up
and control BigQuery resources using
[GoogleSQL](/bigquery/docs/reference/standard-sql) query syntax.

Use these statements to give or remove access to BigQuery resources.

For more information on controlling access to specific BigQuery resources,
see:

* [Controlling access to datasets](/bigquery/docs/dataset-access-controls)
* [Controlling access to tables](/bigquery/docs/table-access-controls)
* [Controlling access to views](/bigquery/docs/authorized-views)

## Permissions required

The following permissions are required to run `GRANT` and `REVOKE` statements.

| Resource Type | Permissions |
| --- | --- |
| Dataset | `bigquery.datasets.update` |
| Table | `bigquery.tables.setIamPolicy` |
| View | `bigquery.tables.setIamPolicy` |
| Project | `resourcemanager.projects.setIamPolicy` |

## `GRANT` statement

Grants roles to users on BigQuery resources.

### Syntax

```
GRANT role_list
  ON resource_type resource_name
  TO user_list
```

### Arguments

* `role_list`: A role or list of comma separated roles that contains the
  permissions you want to grant. For more information on the types of roles available,
  see [Roles and permissions](/iam/docs/roles-overview).
* `resource_type`: The type of resource the role is applied to. Supported values include:
  `SCHEMA` (equivalent to dataset), `TABLE`, `VIEW`,
  `EXTERNAL TABLE`, and `PROJECT`.
* `resource_name`: The name of the resource you want to grant the permission on.
* [`user_list`](#user_list): A comma separated list of users that the role is granted to.

### `user_list`

Specify users using the following formats:

| User Type | Syntax | Example |
| --- | --- | --- |
| Google account | `user:$user@$domain` | `user:first.last@example.com` |
| Google group | `group:$group@$domain` | `group:my-group@example.com` |
| Service account | `serviceAccount:$user@$project.iam.gserviceaccount.com` | `serviceAccount:robot@example.iam.gserviceaccount.com` |
| Google domain | `domain:$domain` | `domain:example.com` |
| All Google accounts | `specialGroup:allAuthenticatedUsers` | `specialGroup:allAuthenticatedUsers` |
| All users | `specialGroup:allUsers` | `specialGroup:allUsers` |
| Connection | `connection:[$project_id.]$location.$connection_id`  If `$project_id` is omitted, the project where you run this DCL statement is used. | `connection:my-bq-project.us.my-connection` |

For more information about each type of user in the table, see
[Concepts related to identity](/iam/docs/overview#concepts_related_identity).

### Examples

The following example grants the `bigquery.dataViewer` role to the users
`raha@example-pet-store.com` and `sasha@example-pet-store.com` on a dataset named
`myDataset`:

```
GRANT `roles/bigquery.dataViewer` ON SCHEMA `myProject`.myDataset
TO "user:raha@example-pet-store.com", "user:sasha@example-pet-store.com"
```

The following example grants the `aiplatform.user` and `run.invoker` roles to
the `my-connection` and `other-connection` connections on the
`my-vertex-project` project:

```
GRANT `roles/aiplatform.user`, `roles/run.invoker`
ON PROJECT `my-vertex-project`
TO "connection:my-bq-project.us.my-connection", "connection:another-bq-project.eu.other-connection";
```

## `REVOKE` statement

Removes roles from a list of users on BigQuery resources.

### Syntax

```
REVOKE role_list
  ON resource_type resource_name
  FROM user_list
```

### Arguments

* `role_list`: A role or list of comma separated roles that contains the
  permissions you want to remove. For more information on the types of roles available,
  see [Roles and permissions](/iam/docs/roles-overview).
* `resource_type`: The type of resource that the role will be removed from. Supported values include:
  `SCHEMA` (equivalent to dataset), `TABLE`, `VIEW`,
  `EXTERNAL TABLE`, and `PROJECT`.
* `resource_name`: The name of the resource you want to revoke the role on.
* [`user_list`](#user_list): A comma separated list of users that the role is revoked from.

### Examples

The following example removes the `bigquery.admin` role on the `myDataset`
dataset from the `example-team@example-pet-store.com` group and a service
account:

```
REVOKE `roles/bigquery.admin` ON SCHEMA `myProject`.myDataset
FROM "group:example-team@example-pet-store.com", "serviceAccount:user@test-project.iam.gserviceaccount.com"
```

The following example revokes the `run.invoker` role on the `my-vertex-project`
project from the `my-connection` connection:

```
REVOKE `roles/run.invoker`
ON PROJECT `my-vertex-project`
FROM "connection:my-bq-project.us.my-connection";
```




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-15 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-15 UTC."],[],[]]