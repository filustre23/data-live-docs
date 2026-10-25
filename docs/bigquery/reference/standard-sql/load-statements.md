* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# Load statements in GoogleSQL

## `LOAD DATA` statement

Loads data from one or more files into a table. The statement can create a new
table, append data into an existing table or partition, or overwrite an existing
table or partition. If the `LOAD DATA` statement fails, the table into which you
are loading data remains unchanged.

### Syntax

```
LOAD DATA {OVERWRITE|INTO}  [{TEMP|TEMPORARY} TABLE]
[[project_name.]dataset_name.]table_name
[(
  column_list
)]
[[OVERWRITE] PARTITIONS (partition_column_name=partition_value)]
[PARTITION BY partition_expression]
[CLUSTER BY clustering_column_list]
[OPTIONS (table_option_list)]
FROM FILES(load_option_list)
[WITH PARTITION COLUMNS
  [(partition_column_list)]
]
[WITH CONNECTION connection_name]

column_list: column[, ...]

partition_column_list: partition_column_name, partition_column_type[, ...]
```

### Arguments

* `INTO`: If a table with this name already exists, the statement appends data
  to the table. You must use `INTO` instead of `OVERWRITE` if your statement
  includes the `PARTITIONS` clause.
* `OVERWRITE`: If a table with this name already exists, the statement
  overwrites the table.
* `{TEMP|TEMPORARY} TABLE`: Use this clause to create or write to a temporary
  table.
* `project_name`: The name of the project for the table. The value
  defaults to the project that runs this DDL query.
* `dataset_name`: The name of the dataset for the table.
* `table_name`: The name of the table.
* `column_list`: Contains the table's schema information as a list of table
  columns. For more information about table schemas, see
  [Specifying a schema](/bigquery/docs/schemas). If you don't specify a schema,
  BigQuery uses
  [schema auto-detection](/bigquery/docs/schema-detect) to infer the schema.

  When you load hive-partitioned data into a new table or overwrite an existing
  table, then that table
  schema contains the hive-partitioned columns and the columns in the
  `column_list`.

  If you append hive-partitioned data to an existing table, then the
  hive-partitioned columns and `column_list` can be a subset of the existing
  columns. If the combined list of columns in not a subset of the existing
  columns, then the following rules apply:

  + If your data is self-describing, such as ORC, PARQUET, or AVRO, then
    columns in the source file that are omitted from the `column_list`
    are ignored. Columns in the `column_list` that don't exist in the source
    file are written with `NULL` values. If a column is in the `column_list`
    and the source file, then their types must match.
  + If your data is not self-describing, such as CSV or JSON, then columns
    in the source file that are omitted from the `column_list` are only
    ignored if you set `ignore_unknown_values` to `TRUE`. Otherwise this
    statement returns an error. You can't list
    columns in the `column_list` that don't exist in the source file.
* `[OVERWRITE] PARTITIONS`: Use this clause to write to or
  overwrite exactly one partition. When you use this clause, the statement
  must begin with `LOAD DATA INTO`.
* `partition_column_name`: The name of the partitioned column to write to.
  If you use both the `PARTITIONS` and the `PARTITION BY` clauses, then the
  column names must match.
* `partition_value`: The `partition_id` of the partition to append or
  overwrite.
  To find the `partition_id` values of a table, query the
  [`INFORMATION_SCHEMA.PARTITIONS` view](/bigquery/docs/information-schema-partitions).
  You can't set the `partition_value` to `__NULL__` or `__UNPARTITIONED__`.
  You can only append to or overwrite one partition. If your data contains
  values that belong to multiple partitions, then the statement
  fails with an error. This `partition_value` must be literal value.
* `partition_expression`: Specifies the table partitioning when creating a
  new table.
* `clustering_column_list`: Specifies table clustering when creating a new
  table. The value is a comma-separated list of column names, with up to four
  columns.
* [`table_option_list`](#table_option_list): Specifies options for creating
  the table. If you include this clause and the table already exists, then the
  options must match the existing table specification.
* `partition_column_list`: A list of external partitioning columns.
* `connection_name`: The connection name that is used to read the source
  files from an [external data source](/bigquery/external-data-sources).
* [`load_option_list`](#load_option_list): Specifies options for loading the
  data.

If no table exists with the specified name, then the statement creates a new
table. If a table already exists with the specified name, then the behavior
depends on the `INTO` or `OVERWRITE` keyword. The `INTO` keyword appends the
data to the table, and the `OVERWRITE` keyword overwrites the table.

If your external data uses a
[hive-partitioned layout](/bigquery/docs/hive-partitioned-queries-gcs#supported_data_layouts),
then include the `WITH PARTITION COLUMNS` clause. If you include the `WITH
PARTITION COLUMNS` clause without `partition_column_list`, then
BigQuery infers the partitioning from the data layout. If you
include both `column_list` and `WITH PARTITION COLUMNS`, then
`partition_column_list` is required.

You can't use the `LOAD DATA` statement to load data into a temporary table.

### `column`

`(column_name column_schema[, ...])` contains the table's
schema information in a comma-separated list.

**Note:** Constraints cannot be specified on `ARRAY` or `STRUCT` elements.

```
column :=
  column_name column_schema

column_schema :=
   {
     simple_type
     | STRUCT<field_list>
     | ARRAY<array_element_schema>
   }
   [PRIMARY KEY NOT ENFORCED | REFERENCES table_name(column_name) NOT ENFORCED]
   [ DEFAULT default_expression |
     embedding_generation |
     identity_column ]
   [NOT NULL]
   [OPTIONS(column_option_list)]

simple_type :=
  { data_type | STRING COLLATE collate_specification }

field_list :=
  field_name column_schema [, ...]

array_element_schema :=
  { simple_type | STRUCT<field_list> }
  [NOT NULL]

embedding_generation :=
  GENERATED ALWAYS AS (generation_expression) STORED OPTIONS(generation_option_list)

identity_column :=
  [ GENERATED { ALWAYS | BY DEFAULT } ] AS IDENTITY (
    [ START WITH start_value ]
    [ INCREMENT BY increment_value ])
```

* [`column_name`](/bigquery/docs/schemas#column_names) is the name of the column.
  A column name:

  + Must contain only letters (a-z, A-Z), numbers (0-9), or underscores (\_)
  + Must start with a letter or underscore
  + Can be up to 300 characters
* `column_schema`: Similar to a
  [data type](/bigquery/docs/schemas#standard_sql_data_types), but supports an
  optional `NOT NULL` constraint for types other than `ARRAY`. `column_schema`
  also supports options on top-level columns and `STRUCT` fields.

  `column_schema` can be used only in the column definition list of
  `CREATE TABLE` statements. It cannot be used as a type in expressions.
* `simple_type`: Any
  [supported data type](/bigquery/docs/reference/standard-sql/data-types)
  aside from `STRUCT` and `ARRAY`.

  If `simple_type` is a `STRING`, it supports an additional clause for
  [collation](/bigquery/docs/reference/standard-sql/collation-concepts#collate_spec_details),
  which defines how a resulting `STRING` can be compared and sorted.
  The syntax looks like this:

  ```
  STRING COLLATE collate_specification
  ```

  If you have `DEFAULT COLLATE collate_specification` assigned to the table,
  the collation specification for a column overrides the specification for the
  table.
* `default_expression`: The [default value](/bigquery/docs/default-values)
  assigned to the column. You cannot specify `DEFAULT` if `GENERATED ALWAYS AS`
  is specified.
* `field_list`: Represents the fields in a struct.
* `field_name`: The name of the struct field. Struct field names have the
  same restrictions as column names.
* `NOT NULL`: When the `NOT NULL` constraint is present for a column or field,
  the column or field is created with `REQUIRED` mode. Conversely, when the
  `NOT NULL` constraint is absent, the column or field is created with
  `NULLABLE` mode.

  Columns and fields of `ARRAY` type do not support the `NOT NULL` modifier. For
  example, a `column_schema` of `ARRAY<INT64> NOT NULL` is invalid, since
  `ARRAY` columns have `REPEATED` mode and can be empty but cannot be `NULL`.
  An array element in a table can never be `NULL`, regardless of whether the
  `NOT NULL` constraint is specified. For example, `ARRAY<INT64>` is equivalent
  to `ARRAY<INT64 NOT NULL>`.

  The `NOT NULL` attribute of a table's `column_schema` does not propagate
  through queries over the table. If table `T` contains a column declared as
  `x INT64 NOT NULL`, for example,
  `CREATE TABLE dataset.newtable AS SELECT x FROM T` creates a table named
  `dataset.newtable` in which `x` is `NULLABLE`.
* `generation_expression`: ([Preview](https://cloud.google.com/products#product-launch-stages))
  An expression for an automatically generated embedding column.
  Setting this field enables
  [autonomous embedding generation](/bigquery/docs/autonomous-embedding-generation)
  on the table. The only
  supported `generation_expression` syntax is a call to the
  [`AI.EMBED` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-embed).

  + You can't specify `GENERATED ALWAYS AS` if `DEFAULT` is specified.
  + The `connection_id` argument to `AI.EMBED` is required when used in a
    generation expression.
  + The type of the column must be
    `STRUCT<result ARRAY<FLOAT64>, status STRING>`.
* `generation_option_list`: The options for a generated column.
  The only supported option is `asynchronous = TRUE`.
* `ALWAYS`: The [identity column](/bigquery/docs/identity-columns)
  can only have generated values. You
  can't manually insert values into the column. This mode is the default mode.
* `BY DEFAULT`: You can manually insert values into the
  [identity column](/bigquery/docs/identity-columns). If
  you add a row to the table and don't specify a value for the column, or
  specify a `NULL` value, then a generated value is used.
* `start_value`: An `INT64` literal that contains the first generated value to
  use for the identity column. The default value is 1.
* `increment_value`: An `INT64` value other than 0 that contains the minimum
  difference between successive values generated for the identity column.
  Some values might be skipped. The difference between successive generated
  values is always a multiple of the `increment_value`. For example,
  if your starting value is 1 and your increment is 2, then the
  generated values can only include odd numbers.
  The default value is 1.

### `column_option_list`

Specify a column option list in the following format:

`NAME=VALUE, ...`

`NAME` and `VALUE` must be one of the following combinations:

| `NAME` | `VALUE` | Details |
| --- | --- | --- |
| `description` | `STRING` | Example: `description="a unique id"`  This property is equivalent to the [schema.fields[].description](/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.description) table resource property. |
| `rounding_mode` | `STRING` | Example: `rounding_mode = "ROUND_HALF_EVEN"`  This specifies the [rounding mode](/bigquery/docs/schemas#rounding_mode) that's used for values written to a `NUMERIC` or `BIGNUMERIC` type column or `STRUCT` field. The following values are supported:   * `"ROUND_HALF_AWAY_FROM_ZERO"`: Halfway cases are   rounded away from zero. For example, 2.25 is rounded to 2.3, and   -2.25 is rounded to -2.3. * `"ROUND_HALF_EVEN"`: Halfway cases are rounded towards   the nearest even digit. For example, 2.25 is rounded to 2.2 and   -2.25 is rounded to -2.2.   This property is equivalent to the [`roundingMode`](/bigquery/docs/reference/rest/v2/tables#TableFieldSchema.FIELDS.rounding_mode) table resource property. |
| `data_policies` | `ARRAY<STRING>` | Applies a [data policy](/bigquery/docs/column-data-masking#create_data_policies) to a column in a table.  Example: `data_policies = ["{'name':'myproject.region-us.data_policy_name1'}", "{'name':'myproject.region-us.data_policy_name2'}"]`  The [`ALTER TABLE ALTER COLUMN`](/bigquery/docs/reference/standard-sql/data-definition-language#alter_column_set_data_type_statement) statement supports the `=` and `+=` operators to add data policies to a specific column.  Example: `data_policies +=["data_policy1", "data_policy2"]` |
| `data_governance_tags` | `ARRAY<STRUCT<STRING, STRING>>` | Applies [data governance tags](/bigquery/docs/tags#data-governance-tags) to a column in a table.  Example: `data_governance_tags = [("myproject/tag_key", "tag_value")]` |

`VALUE` is a constant expression containing only literals, query parameters,
and scalar functions.

The constant expression **cannot** contain:

* A reference to a table
* Subqueries or SQL statements such as `SELECT`, `CREATE`, or `UPDATE`
* User-defined functions, aggregate functions, or analytic functions
* The following scalar functions:
  + `ARRAY_TO_STRING`
  + `REPLACE`
  + `REGEXP_REPLACE`
  + `RAND`
  + `FORMAT`
  + `LPAD`
  + `RPAD`
  + `REPEAT`
  + `SESSION_USER`
  + `GENERATE_ARRAY`
  + `GENERATE_DATE_ARRAY`

Setting the `VALUE` replaces the existing value of that option for the column, if
there was one. Setting the `VALUE` to `NULL` clears the column's value for that
option.

### `partition_expression`

`PARTITION BY` is an optional clause that controls
[table](/bigquery/docs/partitioned-tables) and
[vector index](/bigquery/docs/vector-index#partitions) partitioning.
`partition_expression` is an expression that determines how to partition the
table or vector index. The partition expression can contain the following
values:

* `_PARTITIONDATE`. Partition by ingestion time with daily partitions. This
  syntax cannot be used with the `AS query_statement` clause.
* `DATE(_PARTITIONTIME)`. Equivalent to `_PARTITIONDATE`. This syntax cannot be
  used with the `AS query_statement` clause.
* `<date_column>`. Partition by a `DATE` column with daily partitions.
* `DATE({ <timestamp_column> | <datetime_column> })`. Partition by a `TIMESTAMP`
  or `DATETIME` column with daily partitions.
* `DATETIME_TRUNC(<datetime_column>, { DAY | HOUR | MONTH | YEAR })`. Partition
  by a `DATETIME` column with the specified partitioning type.
* `TIMESTAMP_TRUNC(<timestamp_column>, { DAY | HOUR | MONTH | YEAR })`.
  Partition by a `TIMESTAMP` column with the specified partitioning type.
* `TIMESTAMP_TRUNC(_PARTITIONTIME, { DAY | HOUR | MONTH | YEAR })`. Partition
  by ingestion time with the specified partitioning type. This syntax cannot be
  used with the `AS query_statement` clause.
* `DATE_TRUNC(<date_column>, { MONTH | YEAR })`. Partition by a `DATE` column
  with the specified partitioning type.
* `RANGE_BUCKET(<int64_column>, GENERATE_ARRAY(<start>, <end>[, <interval>]))`.
  Partition by an integer column with the specified range, where:

  + `start` is the start of range partitioning, inclusive.
  + `end` is the end of range partitioning, exclusive.
  + `interval` is the width of each range within the partition. Defaults to 1.

### `table_option_list`

The option list lets you set table options such as a
[label](/bigquery/docs/labels) and an expiration time. You can include multiple
options using a comma-separated list.

Specify a table option list in the following format:

`NAME=VALUE, ...`

`NAME` and `VALUE` must be one of the following combinations:

| `NAME` | `VALUE` | Details |
| --- | --- | --- |
| `expiration_timestamp` | `TIMESTAMP` | Example: `expiration_timestamp=TIMESTAMP "2025-01-01 00:00:00 UTC"`  This property is equivalent to the [expirationTime](/bigquery/docs/reference/rest/v2/tables#Table.FIELDS.expiration_time) table resource property. |
| `partition_expiration_days` | `FLOAT64` | Example: `partition_expiration_days=7`  Sets the partition expiration in days. For more information, see [Set the partition expiration](/bigquery/docs/managing-partitioned-tables#partition-expiration). By default, partitions don't expire.  This property is equivalent to the [timePartitioning.expirationMs](/bigquery/docs/reference/rest/v2/tables#TimePartitioning.FIELDS.expiration_ms) table resource property but uses days instead of milliseconds. One day is equivalent to 86400000 milliseconds, or 24 hours.  This property can only be set if the table is partitioned. |
| `require_partition_filter` | `BOOL` | Example: `require_partition_filter=true`  Specifies whether queries on this table must include a predicate filter that filters on the partitioning column. For more information, see [Set partition filter requirements](/bigquery/docs/managing-partitioned-tables#require-filter). The default value is `false`.  This property is equivalent to the [timePartitioning.requirePartitionFilter](/bigquery/docs/reference/rest/v2/tables#TimePartitioning.FIELDS.require_partition_filter) table resource property.  This property can only be set if the table is partitioned. |
| `friendly_name` | `STRING` | Example: `friendly_name="my_table"`  This property is equivalent to the [friendlyName](/bigquery/docs/reference/rest/v2/tables#Table.FIELDS.friendly_name) table resource property. |
| `description` | `STRING` | Example: `description="a table that expires in 2025"`  This property is equivalent to the [description](/bigquery/docs/reference/rest/v2/tables#Table.FIELDS.description) table resource property. |
| `labels` | `ARRAY<STRUCT<STRING, STRING>>` | Example: `labels=[("org_unit", "development")]`  This property is equivalent to the [labels](/bigquery/docs/reference/rest/v2/tables#Table.FIELDS.labels) table resource property. |
| `default_rounding_mode` | `STRING` | Example: `default_rounding_mode = "ROUND_HALF_EVEN"`  This specifies the default [rounding mode](/bigquery/docs/schemas#rounding_mode) that's used for values written to any new `NUMERIC` or `BIGNUMERIC` type columns or `STRUCT` fields in the table. It does not impact existing fields in the table. The following values are |