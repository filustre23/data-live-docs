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
* When the value expression is `DEFAULT`, the
  [default value](/bigquery/docs/default-values) for the column
  is used. If the column has no default value, the value defaults to `NULL`.

### Omitting column names

When the column names are omitted, all columns in the target table are included
in ascending order based on their ordinal positions. If an omitted column has
a default value, then that value is used. Otherwise, the column value is `NULL`.
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

If you set a default value for a column, then you can use the `DEFAULT` keyword
in place of a value to insert the default value:

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
| top load washer   |       10 |              false | [{"created":"2021-02-09","comment":"comment1"}] | {"color":"white","warranty":"1 year","dimensions":{"depth":"30.0","height":"40.0","width":"28.0"}} |
+-------------------+----------+--------------------+-------------------------------------------------+----------------------------------------------------------------------------------------------------+
```

#### `INSERT` with `ARRAY` types

The following example show how to insert a row into a table, where one of the
fields is an [`ARRAY` type](/bigquery/docs/arrays).

```
CREATE TABLE IF NOT EXISTS dataset.table1 (names ARRAY<STRING>);

INSERT INTO dataset.table1 (names)
VALUES (["name1","name2"])
```

Here is the table after you run the query:

```
+-------------------+
|       names       |
+-------------------+
| ["name1","name2"] |
+-------------------+
```

#### `INSERT` with `RANGE` types

The following example shows how to insert rows into a table, where the
fields are [`RANGE` type](/bigquery/docs/reference/standard-sql/range-functions).

```
INSERT mydataset.my_range_table (emp_id, dept_id, duration)
VALUES(10, 1000, RANGE<DATE> '[2010-01-10, 2010-03-10)'),
      (10, 2000, RANGE<DATE> '[2010-03-10, 2010-07-15)'),
      (10, 2000, RANGE<DATE> '[2010-06-15, 2010-08-18)'),
      (20, 2000, RANGE<DATE> '[2010-03-10, 2010-07-20)'),
      (20, 1000, RANGE<DATE> '[2020-05-10, 2020-09-20)');

SELECT * FROM mydataset.my_range_table ORDER BY emp_id;

/*--------+---------+--------------------------+
 | emp_id | dept_id | duration                 |
 +--------+---------+--------------------------+
 | 10     | 1000    | [2010-01-10, 2010-03-10) |
 | 10     | 2000    | [2010-03-10, 2010-07-15) |
 | 10     | 2000    | [2010-06-15, 2010-08-18) |
 | 20     | 2000    | [2010-03-10, 2010-07-20) |
 | 20     | 1000    | [2020-05-10, 2020-09-20) |
 +--------+---------+--------------------------*/
```

## `DELETE` statement

Use the `DELETE` statement when you want to delete rows from a table.

```
DELETE [FROM] target_name [alias]
WHERE condition
```

To delete all rows in a table, use the
[TRUNCATE TABLE](#truncate_table_statement) statement.

To delete all rows in a partition without scanning bytes or consuming slots,
see [Using DML DELETE to delete partitions](/bigquery/docs/using-dml-with-partitioned-tables#using_dml_delete_to_delete_partitions).

### `WHERE` keyword

Each time you construct a `DELETE` statement, you must use the `WHERE` keyword,
followed by a condition.

The `WHERE` keyword is mandatory for any `DELETE` statement.

### `DELETE` examples

#### `DELETE` with `WHERE` clause

```
DELETE dataset.Inventory
WHERE quantity = 0
```

Before:

```
+-------------------+----------+--------------------+
|      product      | quantity | supply_constrained |
+-------------------+----------+--------------------+
| dishwasher        |       20 |               NULL |
| dryer             |       30 |               NULL |
| front load washer |       10 |               NULL |
| microwave         |       20 |               NULL |
| oven              |        5 |               NULL |
| refrigerator      |       10 |               NULL |
| top load washer   |        0 |               NULL |
+-------------------+----------+--------------------+
```

After:

```
+-------------------+----------+--------------------+
|      product      | quantity | supply_constrained |
+-------------------+----------+--------------------+
| dishwasher        |       20 |               NULL |
| dryer             |       30 |               NULL |
| front load washer |       10 |               NULL |
| microwave         |       20 |               NULL |
| oven              |        5 |               NULL |
| refrigerator      |       10 |               NULL |
+-------------------+----------+--------------------+
```

#### `DELETE` with subquery

```
DELETE dataset.Inventory i
WHERE i.product NOT IN (SELECT product from dataset.NewArrivals)
```

Before:

```
Inventory
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
NewArrivals
+-----------------+----------+--------------+
|     product     | quantity |  warehouse   |
+-----------------+----------+--------------+
| dryer           |      200 | warehouse #2 |
| oven            |      300 | warehouse #3 |
| top load washer |      100 | warehouse #1 |
+-----------------+----------+--------------+
```

After:

```
Inventory
+-----------------+----------+--------------------+
|     product     | quantity | supply_constrained |
+-----------------+----------+--------------------+
| dryer           |       30 |               NULL |
| oven            |        5 |               NULL |
| top load washer |       10 |               NULL |
+-----------------+----------+--------------------+
```

Alternately, you can use `DELETE` with the `EXISTS` clause:

```
DELETE dataset.Inventory
WHERE NOT EXISTS
  (SELECT * from dataset.NewArrivals
   WHERE Inventory.product = NewArrivals.product)
```

## `TRUNCATE TABLE` statement

The `TRUNCATE TABLE` statement removes all rows from a table but leaves the
table metadata intact, including the table schema, description, and labels.

**Note:** This statement is a metadata operation and does not incur a charge.

```
TRUNCATE TABLE [[project_name.]dataset_name.]table_name
```

Where:

* **`project_name`** is the name of the project containing the table. Defaults
  to the project that runs this DDL query.
* **`dataset_name`** is the name of the dataset containing the table.
* **`table_name`** is the name of the table to truncate.

Truncating views, materialized views, models, or external tables is not
supported. Quotas and limits for queries apply to `TRUNCATE TABLE` statements.
For more information, see [Quotas and limits](/bigquery/quotas).

### `TRUNCATE TABLE` examples

The following example removes all rows from the table named `Inventory`.

```
TRUNCATE TABLE dataset.Inventory
```

## `UPDATE` statement

Use the `UPDATE` statement when you want to update existing rows within a table.

```
UPDATE target_name [[AS] alias]
SET set_clause
[FROM from_clause]
WHERE condition

set_clause ::= update_item[, ...]

update_item ::= column_name = expression
```

Where:

* `target_name` is the name of a table to update.
* `update_item` is the name of column to update and an expression to evaluate
  for the updated value. The expression may contain the `DEFAULT` keyword,
  which is replaced by the default value for that column.

If the column is a `STRUCT` type, `column_name` can reference a field in the
`STRUCT` using dot notation. For example, `struct1.field1`.

### `WHERE` keyword

Each `UPDATE` statement must include the `WHERE` keyword, followed by a
condition.

To update all rows in the table, use `WHERE true`.

### `FROM` keyword

An `UPDATE` statement can optionally include a `FROM` clause.

You can use the `FROM` clause to specify the rows to update in the target table.
You can also use columns from joined tables in a `SET` clause or `WHERE`
condition.

The `FROM` clause join can be a cross join if no condition is specified in the
`WHERE` clause, otherwise it is an inner join. In either case, rows from the
target table can join with at most one row from the `FROM` clause.

To specify the join predicate between the table to be updated and tables in
the `FROM` clause, use the `WHERE` clause. For an example, see
[`UPDATE` using joins](#update_using_joins).

Caveats:

* The `SET` clause can reference columns from a target table and columns from
  any `FROM` item in the `FROM` clause. If there is a name collision,
  unqualified references are treated as ambiguous.
* If the target table is present in the `FROM` clause as a table name, it
  must have an alias if you would like to perform a self-join.
* If a row in the table to be updated joins with zero rows from the `FROM`
  clause, then the row isn't updated.
* If a row in the table to be updated joins with exactly one row from the `FROM`
  clause, then the row is updated.
* If a row in the table to be updated joins with more than one row from the
  `FROM` clause, then the query generates the following runtime error:
  `UPDATE/MERGE must match at most one source row for each target row.`

### `UPDATE` examples

#### `UPDATE` with `WHERE` clause

The following example updates a table named `Inventory` by reducing the value
of the `quantity` field by 10 for all products that contain the string `washer`.
Assume that the default value for the `supply_constrained` column is set to
`TRUE`.

```
UPDATE dataset.Inventory
SET quantity = quantity - 10,
    supply_constrained = DEFAULT
WHERE product like '%washer%'
```

Before:

```
Inventory
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

After:

```
Inventory
+-------------------+----------+--------------------+
|      product      | quantity | supply_constrained |
+-------------------+----------+--------------------+
| dishwasher        |       20 |               true |
| dryer             |       30 |               NULL |
| front load washer |       10 |               true |
| microwave         |       20 |               NULL |
| oven              |        5 |               NULL |
| refrigerator      |       10 |               NULL |
| top load washer   |        0 |               true |
+-------------------+----------+--------------------+
```

#### `UPDATE` using joins

The following example generates a table with inventory totals that include
existing inventory and inventory from the `NewArrivals` table, and
marks `supply_constrained` as `false`:

```
UPDATE dataset.Inventory
SET quantity = quantity +
  (SELECT quantity FROM dataset.NewArrivals
   WHERE Inventory.product = NewArrivals.product),
    supply_constrained = false
WHERE product IN (SELECT product FROM dataset.NewArrivals)
```

Alternately, you can join the tables:

```
UPDATE dataset.Inventory i
SET quantity = </
```