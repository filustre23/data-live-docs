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

**Preview**

This product or feature is subject to the "Pre-GA Offerings Terms"
in the General Service Terms section of the
[Service Specific Terms](https://cloud.google.com/terms/service-terms).
Pre-GA products and features are available "as is" and might have
limited support. For more information, see the
[launch stage descriptions](https://cloud.google.com/products#product-launch-stages).

**Note:** To provide feedback or request support for this feature, send an email to
[bq-change-history-feedback@google.com](mailto:bq-change-history-feedback@google.com).

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
  [time travel](/bigquery/docs/time-travel), or
  if the table was created earlier than allowed by time travel if the
  `start_timestamp` value is `NULL`. For standard tables, this window is seven days,
  but you can [configure the time travel window](/bigquery/docs/time-travel#configure_the_time_travel_window) to be less than
  that.
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

**Preview**

This product or feature is subject to the "Pre-GA Offerings Terms"
in the General Service Terms section of the
[Service Specific Terms](https://cloud.google.com/terms/service-terms).
Pre-GA products and features are available "as is" and might have
limited support. For more information, see the
[launch stage descriptions](https://cloud.google.com/products#product-launch-stages).

**Note:** To provide feedback or request support for this feature, send an email to
[bq-change-history-feedback@google.com](mailto:bq-change-history-feedback@google.com).

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
  used instead. An error is returned if the time specified is earlier than
  allowed by [time travel](/bigquery/docs/time-travel), or if the table was created earlier
  than allowed by time travel if the `start_timestamp` value is `NULL`. For
  standard tables, this window is seven days, but you can [configure the time
  travel window](/bigquery/docs/time-travel#configure_the_time_travel_window) to be less than that.
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
* Partition pseudo-columns for ingestion-time partitioned tables, such as
  `_PARTITIONTIME` and `_PARTITIONDATE`, aren't included in the function's
  output.
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

Update one row of the table:

```
UPDATE mydataset.Produce
SET inventory = inventory - 10
WHERE product = 'carrots';
```

View the full change history of the changes made to the table:

```
SELECT
  product,
  inventory,
  _CHANGE_TYPE AS change_type,
  _CHANGE_TIMESTAMP AS change_time
FROM
  CHANGES(TABLE mydataset.Produce, NULL, NULL)
ORDER BY change_time, product;
```

The output is similar to the following:

```
+---------+-----------+-------------+---------------------+
| product | inventory | change_type |     change_time     |
+---------+-----------+-------------+---------------------+
| bananas |        20 | INSERT      | 2024-01-09 17:13:58 |
| carrots |        30 | INSERT      | 2024-01-09 17:13:58 |
| bananas |        20 | DELETE      | 2024-01-09 17:14:30 |
| carrots |        30 | DELETE      | 2024-01-09 17:15:24 |
| carrots |        20 | UPDATE      | 2024-01-09 17:15:24 |
+---------+-----------+-------------+---------------------+
```

**Enabling change history for an existing table**

To set the
[`enable_change_history` option](/bigquery/docs/reference/standard-sql/data-definition-language#table_option_list)
to `TRUE` for an existing table, use the
[`ALTER TABLE SET OPTIONS` DDL statement](/bigquery/docs/reference/standard-sql/data-definition-language#alter_table_set_options_statement).
The following example updates the change history option for `my_table` to
`TRUE`:

```
ALTER TABLE `my_dataset.my_table`
SET OPTIONS (enable_change_history = TRUE);
```

## `DATE_BUCKET`

```
DATE_BUCKET(date_in_bucket, bucket_width)
```

```
DATE_BUCKET(date_in_bucket, bucket_width, bucket_origin_date)
```

**Description**

Gets the lower bound of the date bucket that contains a date.

**Definitions**

* `date_in_bucket`: A `DATE` value that you can use to look up a date bucket.
* `bucket_width`: An `INTERVAL` value that represents the width of
  a date bucket. A [single interval](/bigquery/docs/reference/standard-sql/data-types#single_datetime_part_interval) with
  [date parts](/bigquery/docs/reference/standard-sql/data-types#interval_datetime_parts) is supported.
* `bucket_origin_date`: A `DATE` value that represents a point in time. All
  buckets expand left and right from this point. If this argument isn't set,
  `1950-01-01` is used by default.

**Return type**

`DATE`

**Examples**

In the following example, the origin is omitted and the default origin,
`1950-01-01` is used. All buckets expand in both directions from the origin,
and the size of each bucket is two days. The lower bound of the bucket in
which `my_date` belongs is returned.

```
WITH some_dates AS (
  SELECT DATE '1949-12-29' AS my_date UNION ALL
  SELECT DATE '1949-12-30' UNION ALL
  SELECT DATE '1949-12-31' UNION ALL
  SELECT DATE '1950-01-01' UNION ALL
  SELECT DATE '1950-01-02' UNION ALL
  SELECT DATE '1950-01-03'
)
SELECT DATE_BUCKET(my_date, INTERVAL 2 DAY) AS bucket_lower_bound
FROM some_dates;

/*--------------------+
 | bucket_lower_bound |
 +--------------------+
 | 1949-12-28         |
 | 1949-12-30         |
 | 1949-12-30         |
 | 1950-01-01         |
 | 1950-01-01         |
 | 1950-01-03         |
 +--------------------*/

-- Some date buckets that originate from 1950-01-01:
-- + Bucket: ...
-- + Bucket: [1949-12-28, 1949-12-30)
-- + Bucket: [1949-12-30, 1950-01-01)
-- + Origin: [1950-01-01]
-- + Bucket: [1950-01-01, 1950-01-03)
-- + Bucket: [1950-01-03, 1950-01-05)
-- + Bucket: ...
```

In the following example, the origin has been changed to `2000-12-24`,
and all buckets expand in both directions from this point. The size of each
bucket is seven days. The lower bound of the bucket in which `my_date` belongs
is returned:

```
WITH some_dates AS (
  SELECT DATE '2000-12-20' AS my_date UNION ALL
  SELECT DATE '2000-12-21' UNION ALL
  SELECT DATE '2000-12-22' UNION ALL
  SELECT DATE '2000-12-23' UNION ALL
  SELECT DATE '2000-12-24' UNION ALL
  SELECT DATE '2000-12-25'
)
SELECT DATE_BUCKET(
  my_date,
  INTERVAL 7 DAY,
  DATE '2000-12-24') AS bucket_lower_bound
FROM some_dates;

/*--------------------+
 | bucket_lower_bound |
 +--------------------+
 | 2000-12-17         |
 | 2000-12-17         |
 | 2000-12-17         |
 | 2000-12-17         |
 | 2000-12-24         |
 | 2000-12-24         |
 +--------------------*/

-- Some date buckets that originate from 2000-12-24:
-- + Bucket: ...
-- + Bucket: [2000-12-10, 2000-12-17)
-- + Bucket: [2000-12-17, 2000-12-24)
-- + Origin: [2000-12-24]
-- + Bucket: [2000-12-24, 2000-12-31)
-- + Bucket: [2000-12-31, 2000-01-07)
-- + Bucket: ...
```

## `DATETIME_BUCKET`

```
DATETIME_BUCKET(datetime_in_bucket, bucket_width)
```

```
DATETIME_BUCKET(datetime_in_bucket, bucket_width, bucket_origin_datetime)
```

**Description**

Gets the lower bound of the datetime bucket that contains a datetime.

**Definitions**

* `datetime_in_bucket`: A `DATETIME` value that you can use to look up a
  datetime bucket.
* `bucket_width`: An `INTERVAL` value that represents the width of
  a datetime bucket. A [single interval](/bigquery/docs/reference/standard-sql/data-types#single_datetime_part_interval) with
  [date and time parts](/bigquery/docs/reference/standard-sql/data-types#interval_datetime_parts) is supported.
* `bucket_origin_datetime`: A `DATETIME` value that represents a point in
  time. All buckets expand left and right from this point. If this argument
  isn't set, `1950-01-01 00:00:00` is used by default.

**Return type**

`DATETIME`

**Examples**

In the following example, the origin is omitted and the default origin,
`1950-01-01 00:00:00` is used. All buckets expand in both directions from the
origin, and the size of each bucket is 12 hours. The lower bound of the bucket
in which `my_datetime` belongs is returned:

```
WITH some_datetimes AS (
  SELECT DATETIME '1949-12-30 13:00:00' AS my_datetime UNION ALL
  SELECT DATETIME '1949-12-31 00:00:00' UNION ALL
  SELECT DATETIME '1949-12-31 13:00:00' UNION ALL
  SELECT DATETIME '1950-01-01 00:00:00' UNION ALL
  SELECT DATETIME '1950-01-01 13:00:00' UNION ALL
  SELECT DATETIME '1950-01-02 00:00:00'
)
SELECT DATETIME_BUCKET(my_datetime, INTERVAL 12 HOUR) AS bucket_lower_bound
FROM some_datetimes;

/*---------------------+
 | bucket_lower_bound  |
 +---------------------+
 | 1949-12-30T12:00:00 |
 | 1949-12-31T00:00:00 |
 | 1949-12-31T12:00:00 |
 | 1950-01-01T00:00:00 |
 | 1950-01-01T12:00:00 |
 | 1950-01-02T00:00:00 |
 +---------------------*/

-- Some datetime buckets that originate from 1950-01-01 00:00:00:
-- + Bucket: ...
-- + Bucket: [1949-12-30 00:00:00, 1949-12-30 12:00:00)
-- + Bucket: [1949-12-30 12:00:00, 1950-01-01 00:00:00)
-- + Origin: [1950-01-01 00:00:00]
-- + Bucket: [1950-01-01 00:00:00, 1950-01-01 12:00:00)
-- + Bucket: [1950-01-01 12:00:00, 1950-02-00 00:00:00)
-- + Bucket: ...
```

In the following example, the origin has been changed to `2000-12-24 12:00:00`,
and all buckets expand in both directions from this point. The size of each
bucket is seven days. The lower bound of the bucket in which `my_datetime`
belongs is returned:

```
WITH some_datetimes AS (
  SELECT DATETIME '2000-12-20 00:00:00' AS my_datetime UNION ALL
  SELECT DATETIME '2000-12-21 00:00:00' UNION ALL
  SELECT DATETIME '2000-12-22 00:00:00' UNION ALL
  SELECT DATETIME '2000-12-23 00:00:00' UNION ALL
  SELECT DATETIME '2000-12-24 00:00:00' UNION ALL
  SELECT DATETIME '2000-12-25 00:00:00'
)
SELECT DATETIME_BUCKET(
  my_datetime,
  INTERVAL 7 DAY,
  DATETIME '2000-12-22 12:00:00')
```