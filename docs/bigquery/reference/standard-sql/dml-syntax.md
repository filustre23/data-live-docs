* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# Data manipulation language (DML) statements in GoogleSQL

The BigQuery data manipulation language (DML) enables you to
update, insert, and delete data from your BigQuery tables.

For information about how to use DML statements, see
[Transform data with data manipulation language](/bigquery/docs/data-manipulation-language)
and [Update partitioned table data using DML](/bigquery/docs/using-dml-with-partitioned-tables).

## On-demand query size calculation

If you use on-demand billing, BigQuery charges for data
manipulation language (DML) statements based on the number of bytes processed by
the statement.

For more information about cost estimation, see [Estimate and control costs](/bigquery/docs/best-practices-costs).

### Non-partitioned tables

For non-partitioned tables, the number of bytes processed is calculated as
follows:

* *q* = The sum of bytes processed by the DML statement itself, including any
  columns referenced in tables scanned by the DML statement.
* *t* = The size of the table being updated by the DML statement before any
  modifications are made.

| DML statement | Bytes processed |
| --- | --- |
| `INSERT` | *q* |
| `UPDATE` | *q* + *t* |
| `DELETE` | *q* + *t* |
| `MERGE` | If there are only `INSERT` clauses: *q*.  If there is an `UPDATE` or `DELETE` clause: *q* + *t*. |

To preview how many bytes a statement processes,
[Check the estimated cost before running a query](/bigquery/docs/best-practices-costs#check-query-cost).

### Partitioned tables

For partitioned tables, the number of bytes processed is calculated as
follows:

* *q'* = The sum of bytes processed by the DML statement itself, including any
  columns referenced in all partitions scanned by the DML statement.
* *t'* = The total size of all partitions being updated by the DML statement
  before any modifications are made.

| DML statement | Bytes processed |
| --- | --- |
| `INSERT` | *q'* |
| `UPDATE` | *q'* + *t'* |
| `DELETE` | *q'* + *t'* |
| `MERGE` | If there are only `INSERT` clauses in the `MERGE` statement: *q'*.  If there is an `UPDATE` or `DELETE` clause in the `MERGE` statement: *q'* + *t'*. |

To preview how many bytes a statement processes,
[Check the estimated cost before running a query](/bigquery/docs/best-practices-costs#check-query-cost).

## `INSERT` statement

Use the `INSERT` statement when you want to add new rows to a table.

```
INSERT [INTO] target_name
 [(column_1 [, ..., column_n ] )]
 input

input ::=
 VALUES (expr_1 [, ..., expr_n ] )
        [, ..., (expr_k_1 [, ..., expr_k_n ] ) ]
| SELECT_QUERY

expr ::= value_expression | DEFAULT
```

`INSERT` statements must comply with the following rules:

* Column names are optional if the target table is not an
  [ingestion-time partitioned table](/bigquery/docs/partitioned-tables#ingestion_time).
* Duplicate names are not allowed in the list of target columns.
* Values must be added in the same order as the specified columns.
* The number of values added must match the number of specified columns.
* Values must have a type that is compatible with the target column.
* When the value expression is `DEFAULT`, either the
  [default value](/bigquery/docs/default-values) or a system-generated
  value for an [identity column](/bigquery/docs/identity-columns)
  is used. Otherwise, the value defaults to `NULL`.

### Omitting column names

When the column names are omitted, all columns in the target table are included
in ascending order based on their ordinal positions. If an omitted column has
a default value, then that value is used. If the omitted column is an
[identity column](/bigquery/docs/identity-columns), then a new ID is
generated. Otherwise, the column value is `NULL`.
If the target
table is an
[ingestion-time partitioned table](/bigquery/docs/partitioned-tables#ingestion_time),
column names must be specified.

### Value type compatibility

Values added with an `INSERT` statement must be compatible with the target
column's type. A value's type is considered compatible with the target column's
type if one of the following criteria are met:

* The value type matches the column type exactly. For example, inserting a
  value of type INT64 in a column that also has a type of INT64.
* The value type is one that can be implicitly coerced into another type.

### `INSERT` examples

#### `INSERT` using explicit values

```
INSERT dataset.Inventory (product, quantity)
VALUES('top load washer', 10),
      ('front load washer', 20),
      ('dryer', 30),
      ('refrigerator', 10),
      ('microwave', 20),
      ('dishwasher', 30),
      ('oven', 5)
```

```
+-------------------+----------+--------------------+
|      product      | quantity | supply_constrained |
+-------------------+----------+--------------------+
| dishwasher        |       30 |               NULL |
| dryer             |       30 |               NULL |
| front load washer |       20 |               NULL |
| microwave         |       20 |               NULL |
| oven              |        5 |               NULL |
| refrigerator      |       10 |               NULL |
| top load washer   |       10 |               NULL |
+-------------------+----------+--------------------+
```

If you set a default value for a column, then you can use the `DEFAULT`
keyword in place of a value to insert the default value:

```
ALTER TABLE dataset.NewArrivals ALTER COLUMN quantity SET DEFAULT 100;

INSERT dataset.NewArrivals (product, quantity, warehouse)
VALUES('top load washer', DEFAULT, 'warehouse #1'),
      ('dryer', 200, 'warehouse #2'),
      ('oven', 300, 'warehouse #3');
```

```
+-----------------+----------+--------------+
|     product     | quantity |  warehouse   |
+-----------------+----------+--------------+
| dryer           |      200 | warehouse #2 |
| oven            |      300 | warehouse #3 |
| top load washer |      100 | warehouse #1 |
+-----------------+----------+--------------+
```

If your table has an [identity column](/bigquery/docs/identity-columns), then you can use the `DEFAULT` keyword to insert a generated ID value:

```
CREATE TABLE dataset.Products (
  id INT64 GENERATED ALWAYS AS IDENTITY(INCREMENT BY 2),
  product STRING);

INSERT dataset.Products (id, product)
VALUES (DEFAULT, 'dryer'),
       (DEFAULT, 'top load washer');
```

```
+----+-----------------+
| id | product         |
+----+-----------------+
| 1  | dryer           |
| 3  | top load washer |
+----+-----------------+
```

#### `INSERT SELECT` statement

```
INSERT dataset.Warehouse (warehouse, state)
SELECT *
FROM UNNEST([('warehouse #1', 'WA'),
      ('warehouse #2', 'CA'),
      ('warehouse #3', 'WA')])
```

```
+--------------+-------+
|  warehouse   | state |
+--------------+-------+
| warehouse #1 | WA    |
| warehouse #2 | CA    |
| warehouse #3 | WA    |
+--------------+-------+
```

You can also use `WITH` when using `INSERT SELECT`. For example, you can
rewrite the previous query using `WITH`:

```
INSERT dataset.Warehouse (warehouse, state)
WITH w AS (
  SELECT ARRAY<STRUCT<warehouse string, state string>>
      [('warehouse #1', 'WA'),
       ('warehouse #2', 'CA'),
       ('warehouse #3', 'WA')] col
)
SELECT warehouse, state FROM w, UNNEST(w.col)
```

The following example shows how to copy a table's contents into another table:

```
INSERT dataset.DetailedInventory (product, quantity, supply_constrained)
SELECT product, quantity, false
FROM dataset.Inventory
```

```
+----------------------+----------+--------------------+----------+----------------+
|       product        | quantity | supply_constrained | comments | specifications |
+----------------------+----------+--------------------+----------+----------------+
| dishwasher           |       30 |              false |       [] |           NULL |
| dryer                |       30 |              false |       [] |           NULL |
| front load washer    |       20 |              false |       [] |           NULL |
| microwave            |       20 |              false |       [] |           NULL |
| oven                 |        5 |              false |       [] |           NULL |
| refrigerator         |       10 |              false |       [] |           NULL |
| top load washer      |       10 |              false |       [] |           NULL |
+----------------------+----------+--------------------+----------+----------------+
```

#### `INSERT VALUES` with subquery

The following example shows how to insert a row into a table, where one of the
values is computed using a subquery:

```
INSERT dataset.DetailedInventory (product, quantity)
VALUES('countertop microwave',
  (SELECT quantity FROM dataset.DetailedInventory
   WHERE product = 'microwave'))
```

```
+----------------------+----------+--------------------+----------+----------------+
|       product        | quantity | supply_constrained | comments | specifications |
+----------------------+----------+--------------------+----------+----------------+
| countertop microwave |       20 |               NULL |       [] |           NULL |
| dishwasher           |       30 |              false |       [] |           NULL |
| dryer                |       30 |              false |       [] |           NULL |
| front load washer    |       20 |              false |       [] |           NULL |
| microwave            |       20 |              false |       [] |           NULL |
| oven                 |        5 |              false |       [] |           NULL |
| refrigerator         |       10 |              false |       [] |           NULL |
| top load washer      |       10 |              false |       [] |           NULL |
+----------------------+----------+--------------------+----------+----------------+
```

#### `INSERT` without column names

```
INSERT dataset.Warehouse VALUES('warehouse #4', 'WA'), ('warehouse #5', 'NY')
```

This is the `Warehouse` table before you run the query:

```
+--------------+-------+
|  warehouse   | state |
+--------------+-------+
| warehouse #1 | WA    |
| warehouse #2 | CA    |
| warehouse #3 | WA    |
+--------------+-------+
```

This is the `Warehouse` table after you run the query:

```
+--------------+-------+
|  warehouse   | state |
+--------------+-------+
| warehouse #1 | WA    |
| warehouse #2 | CA    |
| warehouse #3 | WA    |
| warehouse #4 | WA    |
| warehouse #5 | NY    |
+--------------+-------+
```

#### `INSERT` with `STRUCT` types

The following example shows how to insert a row into a table, where some of
the fields are
[`STRUCT` types](/bigquery/docs/reference/standard-sql/data-types#struct_type).

```
INSERT dataset.DetailedInventory
VALUES('top load washer', 10, FALSE, [(CURRENT_DATE, "comment1")], ("white","1 year",(30,40,28))),
      ('front load washer', 20, FALSE, [(CURRENT_DATE, "comment1")], ("beige","1 year",(35,45,30)))
```

Here is the `DetailedInventory` table after you run the query:

```
+-------------------+----------+--------------------+-------------------------------------------------+----------------------------------------------------------------------------------------------------+
|      product      | quantity | supply_constrained |                    comments                     |                                           specifications                                           |
+-------------------+----------+--------------------+-------------------------------------------------+----------------------------------------------------------------------------------------------------+
| front load washer |       20 |              false | [{"created":"2021-02-09","comment":"comment1"}] | {"color":"beige","warranty":"1 year","dimensions":{"depth":"35.0","height":"45.0","width":"30.0"}} |
| top load w
```