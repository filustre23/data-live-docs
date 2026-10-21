* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Time series functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following time series functions.

## Function list

| Name | Summary |
| --- | --- |
| [`APPENDS`](/bigquery/docs/reference/standard-sql/time-series-functions#appends) | Returns all rows appended to a table for a given time range. |
| [`CHANGES`](/bigquery/docs/reference/standard-sql/time-series-functions#changes) | Returns all rows that have changed in a table for a given time range. |
| [`DATE_BUCKET`](/bigquery/docs/reference/standard-sql/time-series-functions#date_bucket) | Gets the lower bound of the date bucket that contains a date. |
| [`DATETIME_BUCKET`](/bigquery/docs/reference/standard-sql/time-series-functions#datetime_bucket) | Gets the lower bound of the datetime bucket that contains a datetime. |
| [`GAP_FILL`](/bigquery/docs/reference/standard-sql/time-series-functions#gap_fill) | Finds and fills gaps in a time series. |
| [`TIMESTAMP_BUCKET`](/bigquery/docs/reference/standard-sql/time-series-functions#timestamp_bucket) | Gets the lower bound of the timestamp bucket that contains a timestamp. |

## `APPENDS`

```
APPENDS(
  TABLE table,
  start_timestamp DEFAULT NULL,
  end_timestamp DEFAULT NULL)
```

**Description**

The `APPENDS` function returns all rows appended to a table for a given
time range.

The following operations add rows to the `APPENDS` change history:

* [`CREATE TABLE` DDL statement](/bigquery/docs/reference/standard-sql/data-definition-language#create_table_statement)
* [`INSERT` DML statement](/bigquery/docs/reference/standard-sql/dml-syntax#insert_statement)
* [Data appended as part of a `MERGE` DML statement](/bigquery/docs/reference/standard-sql/dml-syntax#merge_statement)
* [Loading data](/bigquery/docs/loading-data) into BigQuery
* [Streaming ingestion](/bigquery/docs/write-api#use_data_manipulation_language_dml_with_recently_streamed_data)

**Definitions**

* `table`: the BigQuery table name. This must be a regular
  BigQuery table. This argument must be preceded by the word `TABLE`.
* `start_timestamp`: a [`TIMESTAMP`](/bigquery/docs/reference/standard-sql/data-types#timestamp_type)
  value indicating the earliest time at which a
  change is included in the output. If the value is `NULL`, all changes since the
  table creation are returned. If the table was created after the
  `start_timestamp` value, the actual table creation time is used instead. An error
  is returned if the time specified is earlier than allowed by
  [time travel](/bigquery/docs/time-travel).

  **Note:** An error is returned if the `start_timestamp` is older than
  allowed by [time travel](/bigquery/docs/time-travel). An error is also returned if the
  `start_timestamp` value is `NULL` and the table was created earlier than
  allowed by time travel. To get all available appended records,
  specify a `start_timestamp` within your time travel window instead of
  `NULL`. For standard tables, the time travel window is seven days, but you can
  [configure the time travel window](/bigquery/docs/time-travel#configure_the_time_travel_window) to be less than that.
* `end_timestamp`: a `TIMESTAMP` value indicating the latest time at
  which a change is included in the output. `end_timestamp` is exclusive; for
  example, if you specify `2023-12-31 08:00:00` for `start_timestamp` and
  `2023-12-31 12:00:00` for `end_timestamp`, all changes made from
  8 AM December 31, 2023 through 11:59 AM December 31, 2023 are returned.

  If the `end_timestamp` value is `NULL`, all changes made
  up to the start time of the query are included.

  If the `end_timestamp` value is a future date or time, the query fails.

**Details**

Records of inserted rows persist even if that data is later deleted. Deletions
aren't reflected in the `APPENDS` function. If a table
is copied, calling the `APPENDS` function on the copied table returns every row
as inserted at the time of table creation. If a row is modified due to an
`UPDATE` operation, there's no effect.

**Output**

The `APPENDS` function returns a table with the following columns:

* All columns of the input table at the time the query is run. If a column is
  added after the `end_timestamp` value, it appears with `NULL` values populated in any
  of the rows that were inserted before the addition of the column.
* `_CHANGE_TYPE`: a `STRING` value indicating the type of change that produced
  the row. For `APPENDS`, the only supported value is `INSERT`.
* `_CHANGE_TIMESTAMP`: a `TIMESTAMP` value indicating the commit time of the
  transaction that made the change.

**Limitations**

* The data returned by the `APPENDS` function is limited to the time travel
  window of the table.
* The data returned by the `APPENDS` function is limited to the table's current
  schema.
* You can't call the `APPENDS` function within a multi-statement transaction.
* `APPENDS` function may not capture all rows appended within a multi-statement
  transaction if some appended rows are updated or deleted within the same
  transaction.
* You can only use the `APPENDS` function with regular BigQuery
  tables. Clones, snapshots, views, materialized views, external tables, and
  wildcard tables aren't supported.
* Partition pseudo-columns for ingestion-time partitioned tables, such as
  `_PARTITIONTIME` and `_PARTITIONDATE`, aren't included in the function's
  output.
* Rows inserted through the
  [Storage Write API (gRPC) pending stream](/bigquery/docs/write-api#pending_type)
  or
  [Storage Write API (gRPC) buffered stream](/bigquery/docs/write-api#buffered_type)
  can have inconsistent timestamps, so repeatable reads aren't guaranteed. If
  you require repeatable reads for streaming ingestion workloads, use either
  the
  [Storage Write API (gRPC) default stream](/bigquery/docs/write-api#default_stream)
  or the
  [Storage Write API (gRPC) committed stream](/bigquery/docs/write-api#committed_type).
  If you require repeatable reads for batch ingestion workloads, use
  [BigQuery load jobs](/bigquery/docs/loading-data) instead.

**Example**

This example shows the change history returned by the `APPENDS` function as various
changes are made to a table called `Produce`. First, create the table:

```
CREATE TABLE mydataset.Produce (product STRING, inventory INT64) AS (
  SELECT 'apples' AS product, 10 AS inventory);
```

Next, insert two rows into the table:

```
INSERT INTO mydataset.Produce
VALUES
  ('bananas', 20),
  ('carrots', 30);
```

To view the full change history of appends, use `NULL` values to get the full
history within the time travel window:

```
SELECT
  product,
  inventory,
  _CHANGE_TYPE AS change_type,
  _CHANGE_TIMESTAMP AS change_time
FROM
  APPENDS(TABLE mydataset.Produce, NULL, NULL);
```

The output is similar to the following:

```
+---------+-----------+-------------+--------------------------------+
| product | inventory | change_type | change_time                    |
+---------+-----------+-------------+--------------------------------+
| apples  | 10        | INSERT      | 2022-04-15 20:06:00.488000 UTC |
| bananas | 20        | INSERT      | 2022-04-15 20:06:08.490000 UTC |
| carrots | 30        | INSERT      | 2022-04-15 20:06:08.490000 UTC |
+---------+-----------+-------------+--------------------------------+
```

Next, add a column, insert a new row of values, update the inventory, and delete
the `bananas` row:

```
ALTER TABLE mydataset.Produce ADD COLUMN color STRING;
INSERT INTO mydataset.Produce VALUES ('grapes', 40, 'purple');
UPDATE mydataset.Produce SET inventory = inventory + 5 WHERE TRUE;
DELETE mydataset.Produce WHERE product = 'bananas';
```

View the new table:

```
SELECT * FROM mydataset.Produce;
```

The output is similar to the following:

```
+---------+-----------+--------+
| product | inventory | color  |
+---------+-----------+--------+
| apples  | 15        | NULL   |
| carrots | 35        | NULL   |
| grapes  | 45        | purple |
+---------+-----------+--------+
```

View the full change history of appends:

```
SELECT
  product,
  inventory,
  color,
  _CHANGE_TYPE AS change_type,
  _CHANGE_TIMESTAMP AS change_time
FROM
  APPENDS(TABLE mydataset.Produce, NULL, NULL);
```

The output is similar to the following:

```
+---------+-----------+--------+-------------+--------------------------------+
| product | inventory | color  | change_type | change_time                    |
+---------+-----------+--------+-------------+--------------------------------+
| apples  | 10        | NULL   | INSERT      | 2022-04-15 20:06:00.488000 UTC |
| bananas | 20        | NULL   | INSERT      | 2022-04-15 20:06:08.490000 UTC |
| carrots | 30        | NULL   | INSERT      | 2022-04-15 20:06:08.490000 UTC |
| grapes  | 40        | purple | INSERT      | 2022-04-15 20:07:45.751000 UTC |
+---------+-----------+--------+-------------+--------------------------------+
```

The `inventory` column displays the values that were set when the rows were
originally inserted into to the table. It doesn't show the changes from the
`UPDATE` statement. The row with information on bananas is still present because
the `APPENDS` function only captures additions to tables, not deletions.

## `CHANGES`

```
CHANGES(
  TABLE table,
  start_timestamp DEFAULT NULL,
  end_timestamp)
```

**Description**

The `CHANGES` function returns all rows that have changed in a table for a given
time range. To use the `CHANGES` function on a table, you must set the table's
[`enable_change_history` option](/bigquery/docs/reference/standard-sql/data-definition-language#table_option_list)
to `TRUE`.

The following operations add rows to the `CHANGES` change history:

* [`CREATE TABLE` DDL statement](/bigquery/docs/reference/standard-sql/data-definition-language#create_table_statement)
* [`INSERT` DML statement](/bigquery/docs/reference/standard-sql/dml-syntax#insert_statement)
* [Data appended, changed or deleted as part of a `MERGE` DML statement](/bigquery/docs/reference/standard-sql/dml-syntax#merge_statement)
* [`UPDATE` DML statement](/bigquery/docs/reference/standard-sql/dml-syntax#update_statement)
* [`DELETE` DML statement](/bigquery/docs/reference/standard-sql/dml-syntax#delete_statement)
* [Loading data](/bigquery/docs/loading-data) into BigQuery
* [Streaming ingestion](/bigquery/docs/write-api#use_data_manipulation_language_dml_with_recently_streamed_data)
* [`TRUNCATE TABLE` DML statement](/bigquery/docs/reference/standard-sql/dml-syntax#truncate_table_statement)
* [Jobs](/bigquery/docs/reference/rest/v2/Job) configured with a `writeDisposition` of `WRITE_TRUNCATE`
* Individual [table partition deletions](/bigquery/docs/managing-partitioned-tables#delete_a_partition)

**Definitions**

* `table`: the BigQuery table name. This must be a regular
  BigQuery table, and must have the [`enable_change_history`
  option](/bigquery/docs/reference/standard-sql/data-definition-language#table_option_list) set to `TRUE`. Enabling this table option has an
  impact on costs; for more information see
  [Pricing and costs](/bigquery/docs/change-history#pricing_and_costs). This
  argument must be preceded by the word `TABLE`.
* `start_timestamp`: a [`TIMESTAMP`](/bigquery/docs/reference/standard-sql/data-types#timestamp_type) value indicating the earliest
  time at which a change is included in the output. If the value is `NULL`,
  all changes since the table creation are returned. If you set the
  `enable_change_history` option after setting the `start_timestamp` option,
  the history before the enablement time might be incomplete. If the table was
  created after the `start_timestamp` value, the actual table creation time is
  used instead.

  **Note:** An error is returned if the `start_timestamp` is older than
  allowed by [time travel](/bigquery/docs/time-travel). An error is also returned if the
  `start_timestamp` value is `NULL` and the table was created earlier than
  allowed by time travel. To get all available changes,
  specify a `start_timestamp` within your time travel window instead of
  `NULL`. For standard tables, the time travel window is seven days, but you
  can [configure the time travel window](/bigquery/docs/time-travel#configure_the_time_travel_window) to be less than that.
* `end_timestamp`: a `TIMESTAMP` value indicating the latest time at which a
  change is included in the output. `end_timestamp` is exclusive; for example,
  if you specify `2023-12-31 08:00:00` for `start_timestamp` and `2023-12-31
  12:00:00` for `end_timestamp`, all changes made from 8 AM December 31, 2023
  through 11:59 AM December 31, 2023 are returned. The maximum time range
  allowed between `start_timestamp` and `end_timestamp` is one day.

  If the `end_timestamp` value is `NULL`, all changes made up to the start
  time of the query are included.

  If the `end_timestamp` value is a future date or time, the query fails.

**Details**

If a row is inserted, a record of the new row with an `INSERT` change type is
produced.

If a row is deleted, a record of the deleted row with a `DELETE` change type is
produced.

If a row is updated, a record of the old row with a `DELETE` change type and a
record of the new row with an `UPDATE` change type are produced.

**Output**

The `CHANGES` function returns a table with the following columns:

* All columns of the input table at the time that the query is run. If a
  column is added after the `end_timestamp` value, it appears with `NULL` values
  populated in of the any rows that were changed before the addition of
  the column.
* `_CHANGE_TYPE`: a `STRING` value indicating the type of change that produced
  the row. For `CHANGES`, the supported values are `INSERT`, `UPDATE`, and
  `DELETE`.
* `_CHANGE_TIMESTAMP`: a `TIMESTAMP` value indicating the commit time of the
  transaction that made the change.
* `_CHANGE_IS_FOR_UPDATE`: a `BOOL` value that is `TRUE` for a
  `DELETE` event produced by a row update. Otherwise, the value is `FALSE`.

**Limitations**

* The data returned by the `CHANGES` function is limited to the time
  travel window of the table.
* The data returned by the `CHANGES` function is limited to the table's current
  schema.
* The maximum allowed time range between the `start_timestamp` and
  `end_timestamp` arguments you specify for the function is one day.
* You can't call the `CHANGES` function within a multi-statement transaction.
* You can't use the `CHANGES` function with tables that have had multi-statement
  transactions committed to them within the requested time window.
* You can only use the `CHANGES` function with regular BigQuery tables.
  Views, materialized views, external tables, and wildcard tables aren't
  supported.
* For tables that have been cloned or snapshotted, and for tables that are
  restored from a clone or snapshot, change history from the source table isn't
  carried over to the new table, clone, or snapshot.
* You can't use the `CHANGES` function with a table that has
  [change data capture](/bigquery/docs/change-data-capture) enabled.
* If a table is enabled with
  [fine-grained DML](/bigquery/docs/data-manipulation-language#fine-grained_dml),
  and data deletion occurs using either a
  [`TRUNCATE TABLE` statement](/bigquery/docs/reference/standard-sql/dml-syntax#truncate_table_statement),
  [`WRITE_TRUNCATE` write disposition](/bigquery/docs/reference/rest/v2/Job#jobconfigurationquery),
  or a
  [qualifying `DELETE` statement](/bigquery/docs/using-dml-with-partitioned-tables#using_dml_delete_to_delete_partitions)
  that covers all rows in a partition, the `CHANGES` function might return
  additional deleted events.
* Partition pseudo-columns for ingestion-time partitioned tables, such as
  `_PARTITIONTIME` and `_PARTITIONDATE`, aren't included in the function's
  output.
* Rows inserted through the
  [Storage Write API (gRPC) pending stream](/bigquery/docs/write-api#pending_type)
  or
  [Storage Write API (gRPC) buffered stream](/bigquery/docs/write-api#buffered_type)
  can have inconsistent timestamps, so repeatable reads aren't guaranteed. If
  you require repeatable reads for streaming ingestion workloads, use either
  the
  [Storage Write API (gRPC) default stream](/bigquery/docs/write-api#default_stream)
  or the
  [Storage Write API (gRPC) committed stream](/bigquery/docs/write-api#committed_type).
  If you require repeatable reads for batch ingestion workloads, use
  [BigQuery load jobs](/bigquery/docs/loading-data) instead.
* Change history isn't captured for table deletions made due to table partition
  expiration.
* Performing
  [data manipulation language (DML) statements over recently streamed data](/bigquery/docs/write-api#use_data_manipulation_language_dml_with_recently_streamed_data)
  fails on tables that have the `enable_change_history` option set to `TRUE`.

**Example**

This example shows the change history returned by the `CHANGES` function as
various changes are made to a table called `Produce`. First, create the table:

```
CREATE TABLE mydataset.Produce (
  product STRING,
  inventory INT64)
OPTIONS(enable_change_history=true);
```

Insert two rows into the table:

```
INSERT INTO mydataset.Produce
VALUES
  ('bananas', 20),
  ('carrots', 30);
```

Delete one row from the table:

```
DELETE mydataset.Produce
WHERE product = 'bananas';
```