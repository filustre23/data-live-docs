* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Security functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following security functions.

## Function list

| Name | Summary |
| --- | --- |
| [`SECURE_CONTEXT`](/bigquery/docs/reference/standard-sql/security_functions#secure_context) | Returns the value of a request-scoped secure context parameter provided at query run time. |
| [`SESSION_USER`](/bigquery/docs/reference/standard-sql/security_functions#session_user) | Get the email address or principal identifier of the user that's running the query. |

## `SECURE_CONTEXT`

**Preview**

This product or feature is subject to the "Pre-GA Offerings Terms"
in the General Service Terms section of the
[Service Specific Terms](https://cloud.google.com/terms/service-terms).
Pre-GA products and features are available "as is" and might have
limited support. For more information, see the
[launch stage descriptions](https://cloud.google.com/products#product-launch-stages).

**Note:** To provide feedback or request support for this feature, send an email to
[bigquery-sql-preview-support@googlegroups.com](mailto:bigquery-sql-preview-support@googlegroups.com).

```
SECURE_CONTEXT(key)
```

**Description**

Returns the value of a request-scoped secure context parameter provided at query
run time. You can use `SECURE_CONTEXT` in logical views to
dynamically filter and evaluate data based on context variables—such as user
attributes, department IDs, or tenant identifiers—passed in the query request
body, without creating separate static views for each attribute value.

**Caution:** In `SECURE_CONTEXT`, *secure* means that a trusted backend application
supplies parameters in the API request payload rather than in SQL text, and that
parameters bound to a session can't be modified after session creation. Unlike
SQL session variables, untrusted SQL can't override the values passed in
`secureContext`, and unlike `SESSION_USER()`, `secureContext` can carry
per-request end-user attributes when a shared backend service account runs the
query. Omitting `secureContext` from job metadata and clearing query execution
plans provide defense in depth, not a standalone security boundary—an untrusted
logical view that your query references can still read and return any key from
`secureContext`.

**Definitions**

* `key`: A constant, non-`NULL` `STRING` literal or query
  parameter representing the name of the
  secure context parameter to retrieve. `key` isn't coercible.

**Details**

* **Passing secure context in query requests**: Pass secure context parameters
  in the `secureContext` field of the BigQuery
  [`jobs.query`](/bigquery/docs/reference/rest/v2/jobs/query) request payload, or in
  `configuration.query.secureContext` for [`jobs.insert`](/bigquery/docs/reference/rest/v2/jobs/insert).
  For example, the following `jobs.query` payload passes two parameters:

  ```
  {
    "query": "SELECT * FROM my_dataset.sales_view",
    "useLegacySql": false,
    "secureContext": {
      "secureParameterEntries": {
        "user_dept": "Sales",
        "user_region": "US"
      }
    }
  }
  ```

  To pass multiple values in a single parameter, serialize the values as a
  JSON array string or a delimited string, and parse them in the view by using
  [`JSON_VALUE_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_value_array) or [`SPLIT`](/bigquery/docs/reference/standard-sql/string_functions#split).
* **Parameter and request limits**:

  + Parameter keys must be 1 to 127 characters long and match the regular
    expression `^[a-zA-Z_][a-zA-Z0-9_]*$`. The key should start with an
    ASCII letter or underscore, followed only by ASCII letters, digits, or
    underscores.
  + Each parameter value must be a `STRING` of up to 1 MiB (1,048,576 UTF-8
    bytes). Non-string JSON values—such as numbers, booleans, arrays,
    objects, or `NULL`—are rejected.
  + A request can include up to 10,000 entries in `secureParameterEntries`,
    and up to 10 MiB (10,485,760 UTF-8 bytes) combined across all parameter
    values. The request is subject to the overall 10 MB
    [API request size limit](/bigquery/quotas#query_jobs).
* **Sessions**: When you use multi-statement query sessions, you must supply
  secure context parameters when you create the session by specifying
  `createSession: true`. After a session is created, subsequent queries in the
  same session automatically inherit the initial session context and can't
  modify or supply new `secureContext` parameters.
* **Job metadata, execution plans, and audit logs**:

  + BigQuery omits `secureContext` entries from job metadata
    returned by `jobs.get`, `jobs.list`, and
    [`INFORMATION_SCHEMA.JOBS*`](/bigquery/docs/information-schema-jobs) views.
  + When a query evaluates `SECURE_CONTEXT`, BigQuery clears
    execution plan stage details (`statistics.query.queryPlan`) from job
    statistics.
  + Omitting `secureContext` from job metadata and clearing execution plan
    details provide defense in depth against leaking parameter values
    through job history and query plans, rather than preventing an untrusted
    logical view from reading `secureContext`.
  + Parameter names and values are recorded in BigQuery Data Access
    audit logs in the [`secureContextValues`](/bigquery/docs/reference/auditlogs/rest/Shared.Types/BigQueryAuditMetadata#BigQueryAuditMetadata.SecureContextValue)
    field. They might be truncated if the log entry exceeds audit log size
    limits. If you pass sensitive attributes in `secureContext`, restrict
    access to Data Access audit logs by granting a predefined role such as
    [Private Logs Viewer](/iam/docs/roles-permissions/logging#logging.privateLogViewer)
    (`roles/logging.privateLogViewer`). For more information, see
    [Control access to logs](/logging/docs/access-control).
* **Query caching**: Queries that evaluate `SECURE_CONTEXT` aren't cached,
  even when `useQueryCache` is set to `true`. For more information, see
  [Use cached query results](/bigquery/docs/cached-results).
* **Security and architecture best practices**: Dynamic context
  parameterization with `SECURE_CONTEXT` is intended for large-scale
  multi-tenant systems and dynamic, attribute-based access control where
  maintaining separate tables or datasets per tenant is impractical due to
  data scale.

  `SECURE_CONTEXT` evaluates parameters supplied in the API request payload
  rather than in SQL text, and session parameters remain immutable after
  creation. Allow only trusted applications or middle-tier services to set
  `secureContext` parameters. The trusted application must authenticate the
  client and supply the verified context parameters on its behalf. Don't let
  untrusted end users, clients, or AI agents set or modify these parameters
  directly, because doing so lets them spoof context attributes and bypass the
  view's access controls.

  Any logical view that a query can access can call `SECURE_CONTEXT` and
  return the resolved parameter values in query results—including views in
  other projects or datasets that the backend service account can read. When
  you run untrusted or AI-generated SQL, apply the following controls in
  addition to `SECURE_CONTEXT`:

  + **Enforce view allowlists deterministically in middleware**: Don't rely
    on AI prompt instructions alone to restrict which views a query
    references. Use parameterized query templates or a semantic layer, or
    validate every referenced resource against an allowlist of
    administrator-authored views before running the query by parsing the SQL
    abstract syntax tree (AST) or inspecting
    `statistics.query.referencedLogicalViews` (and
    `statistics.query.referencedTables` for base tables) from a
    [dry run](/bigquery/docs/running-queries#dry-run).
  + **Restrict cross-project access and view creation or updates**: Enforce
    a [VPC Service Controls](/bigquery/docs/vpc-sc) perimeter and IAM
    [Principal Access Boundary (PAB) policies](/iam/docs/principal-access-boundary-policies) to prevent the
    backend service account from reading views in untrusted external
    projects. Don't grant `bigquery.tables.create` or
    `bigquery.tables.update` permissions to untrusted principals on any
    dataset that your backend service account can read. These permissions
    shouldn't be granted through custom roles or by using predefined roles
    such as BigQuery Data Editor (`roles/bigquery.dataEditor`).

  For most multi-tenant architecture workloads, standardized table-level
  or dataset-level tenant isolation combined with IAM-based access control,
  Row-Level Security (RLS) policies, and Column-Level Security (CLS) remain
  Google's recommended best practices to ensure strict tenant isolation and
  prevent data leakage.

  For more information about multi-tenant architectures and access control,
  see the following resources:

  + [Best practices for multi-tenant workloads on BigQuery](/bigquery/docs/best-practices-for-multi-tenant-workloads-on-bigquery)
  + [Introduction to BigQuery access control](/bigquery/docs/access-control)
  + [Introduction to row-level security](/bigquery/docs/row-level-security-intro)

**Limitations**

* **View and statement support**:
  + `SECURE_CONTEXT` is only supported within logical view definitions.
    Calling `SECURE_CONTEXT` directly at the top level of an ad hoc query,
    within materialized views, within temporary session views, or within
    user-defined functions (UDFs) and table-valued functions (TVFs) returns
    an error.
  + Running `CREATE VIEW` or `ALTER VIEW` statements while `secureContext`
    is set on the request or session returns an error.
  + Calling the [`ERROR`](/bigquery/docs/reference/standard-sql/debugging_functions#error) function in a query that evaluates a
    `SECURE_CONTEXT` view returns an error.
* **Supported types**: Values supplied in the secure context must be `STRING`
  values.
* **Error mode**: `SECURE_CONTEXT` doesn't support the `SAFE.` prefix.
  Calling `SAFE.SECURE_CONTEXT(key)` returns an analysis error.
* **Missing parameter handling**: If a query evaluates
  `SECURE_CONTEXT('my_param')` and `my_param` isn't provided in the request's
  secure context, the query fails and returns an error.
* **Side-channel exposure**: A `SECURE_CONTEXT` filter is evaluated inside a
  view and isn't a hard isolation boundary. A caller that can submit arbitrary
  SQL against the view might infer the existence or values of rows that the
  filter excludes—through crafted expressions that fail on filtered-out rows,
  query statistics such as bytes processed, or query duration. Don't rely on a
  view filter alone to separate tenants when the SQL reaching the view is
  untrusted, such as SQL generated by an AI agent.

  For a comparison of the isolation strength of authorized views, row-level
  security, and separate tables, see the following resources:

  + [Comparison of authorized views, row-level security, and separate
    tables](/bigquery/docs/row-level-security-intro#comparison_of_authorized_views_row-level_security_and_separate_tables)
  + [Best practices for multi-tenant workloads on BigQuery](/bigquery/docs/best-practices-for-multi-tenant-workloads-on-bigquery)

**Return type**

`STRING`

**Examples**

The following example creates a logical view `my_dataset.sales_view` that
filters rows using the `SECURE_CONTEXT` function:

```
CREATE OR REPLACE VIEW my_dataset.sales_view AS
WITH
  Orders AS (
    SELECT 1001 AS order_id, 'Sales' AS department, 250.00 AS amount
    UNION ALL
    SELECT 1002 AS order_id, 'Engineering' AS department, 500.00 AS amount
    UNION ALL
    SELECT 1004 AS order_id, 'Sales' AS department, 430.50 AS amount
  )
SELECT
  order_id,
  department,
  amount
FROM Orders
WHERE department = SECURE_CONTEXT('user_dept');
```

The following example queries `my_dataset.sales_view` when the API request
payload contains
`secureContext: {"secureParameterEntries": {"user_dept": "Sales"}}`. The view
evaluates `SECURE_CONTEXT('user_dept')` as `'Sales'`:

```
SELECT * FROM my_dataset.sales_view;

/*----------+------------+--------+
 | order_id | department | amount |
 +----------+------------+--------+
 | 1001     | Sales      | 250.00 |
 | 1004     | Sales      | 430.50 |
 +----------+------------+--------*/
```

The following example filters rows against multiple allowed values by passing
`"[\"US\", \"EU\"]"` for `allowed_regions` in
`secureContext.secureParameterEntries`. The query parses the regions in the
view by using the [`JSON_VALUE_ARRAY` function](/bigquery/docs/reference/standard-sql/json_functions#json_value_array):

```
CREATE OR REPLACE VIEW my_dataset.regional_sales_view AS
WITH
  RegionalOrders AS (
    SELECT 1001 AS order_id, 'US' AS region, 250.00 AS amount
    UNION ALL
    SELECT 1002 AS order_id, 'APAC' AS region, 500.00 AS amount
    UNION ALL
    SELECT 1003 AS order_id, 'EU' AS region, 310.00 AS amount
  )
SELECT
  order_id,
  region,
  amount
FROM RegionalOrders
WHERE region IN UNNEST(JSON_VALUE_ARRAY(SECURE_CONTEXT('allowed_regions')));
```

```
SELECT * FROM my_dataset.regional_sales_view;

/*----------+--------+--------+
 | order_id | region | amount |
 +----------+--------+--------+
 | 1001     | US     | 250.00 |
 | 1003     | EU     | 310.00 |
 +----------+--------+--------*/
```

## `SESSION_USER`

```
SESSION_USER()
```

**Description**

For first-party users, returns the email address of the user that's running the
query.
For third-party users, returns the
[principal identifier](https://cloud.google.com/iam/docs/principal-identifiers)
of the user that's running the query.
For more information about identities, see
[Principals](https://cloud.google.com/docs/authentication#principal).

**Return Data Type**

`STRING`

**Example**

```
SELECT SESSION_USER() as user;

/*----------------------+
 | user                 |
 +----------------------+
 | jdoe@example.com     |
 +----------------------*/
```




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the