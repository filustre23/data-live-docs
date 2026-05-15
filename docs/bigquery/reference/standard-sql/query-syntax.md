* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Query syntax Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL is the new name for Google Standard SQL!
New name, same great SQL dialect.

Query statements scan one or more tables or expressions and return the computed
result rows. This topic describes the syntax for SQL queries in
GoogleSQL for BigQuery.

## SQL syntax notation rules

The following table lists and describes the syntax notation rules that GoogleSQL
documentation commonly uses.

| Notation | Example | Description |
| --- | --- | --- |
| Square brackets | `[ ]` | Optional clauses |
| Parentheses | `( )` | Literal parentheses |
| Vertical bar | `|` | Logical `XOR` (exclusive `OR`) |
| Curly braces | `{ }` | A set of options, such as `{ a | b | c }`. Select one option. |
| Ellipsis | `...` | The preceding item can repeat. |
| Comma | `,` | Literal comma |
| Comma followed by an ellipsis | `, ...` | The preceding item can repeat in a comma-separated list. |
| Item list | `item [, ...]` | One or more items |
| `[item, ...]` | Zero or more items |
| Double quotes | `""` | The enclosed syntax characters (for example, `"{"..."}"`) are literal and required. |
| Angle brackets | `<>` | Literal angle brackets |

## SQL syntax

```
query_statement:
  query_expr

query_expr:
  [ WITH [ RECURSIVE ] { non_recursive_cte | recursive_cte }[, ...] ]
  { select | ( query_expr ) | set_operation }
  [ ORDER BY expression [{ ASC | DESC }] [, ...] ]
  [ LIMIT count [ OFFSET skip_rows ] ]

select:
  SELECT
    [ WITH differential_privacy_clause ]
    [ { ALL | DISTINCT } ]
    [ AS { STRUCT | VALUE } ]
    select_list
  [ FROM from_clause[, ...] ]
  [ WHERE bool_expression ]
  [ GROUP BY group_by_specification ]
  [ HAVING bool_expression ]
  [ QUALIFY bool_expression ]
  [ WINDOW window_clause ]
```

## `SELECT` statement

```
SELECT
  [ WITH differential_privacy_clause ]
  [ { ALL | DISTINCT } ]
  [ AS { STRUCT | VALUE } ]
  select_list

select_list:
  { select_all | select_expression } [, ...]

select_all:
  [ expression. ]*
  [ EXCEPT ( column_name [, ...] ) ]
  [ REPLACE ( expression AS column_name [, ...] ) ]

select_expression:
  expression [ [ AS ] alias ]
```

The `SELECT` list defines the columns that the query will return. Expressions in
the `SELECT` list can refer to columns in any of the `from_item`s in its
corresponding `FROM` clause.

Each item in the `SELECT` list is one of:

* `*`
* `expression`
* `expression.*`

### `SELECT *`

`SELECT *`, often referred to as *select star*, produces one output column for
each column that's visible after executing the full query.

```
SELECT * FROM (SELECT "apple" AS fruit, "carrot" AS vegetable);

/*-------+-----------+
 | fruit | vegetable |
 +-------+-----------+
 | apple | carrot    |
 +-------+-----------*/
```

### `SELECT expression`

Items in a `SELECT` list can be expressions. These expressions evaluate to a
single value and produce one output column, with an optional explicit `alias`.

If the expression doesn't have an explicit alias, it receives an implicit alias
according to the rules for [implicit aliases](#implicit_aliases), if possible.
Otherwise, the column is anonymous and you can't refer to it by name elsewhere
in the query.

### `SELECT expression.*`

An item in a `SELECT` list can also take the form of `expression.*`. This
produces one output column for each column or top-level field of `expression`.
The expression must either be a table alias or evaluate to a single value of a
data type with fields, such as a STRUCT.

**Note:** The `*` or `.*` wildcard preserves the order of the fields in the
data structure on which they're operating.

The following query produces one output column for each column in the table
`groceries`, aliased as `g`.

```
WITH groceries AS
  (SELECT "milk" AS dairy,
   "eggs" AS protein,
   "bread" AS grain)
SELECT g.*
FROM groceries AS g;

/*-------+---------+-------+
 | dairy | protein | grain |
 +-------+---------+-------+
 | milk  | eggs    | bread |
 +-------+---------+-------*/
```

More examples:

```
WITH locations AS
  (SELECT STRUCT("Seattle" AS city, "Washington" AS state) AS location
  UNION ALL
  SELECT STRUCT("Phoenix" AS city, "Arizona" AS state) AS location)
SELECT l.location.*
FROM locations l;

/*---------+------------+
 | city    | state      |
 +---------+------------+
 | Seattle | Washington |
 | Phoenix | Arizona    |
 +---------+------------*/
```

```
WITH locations AS
  (SELECT ARRAY<STRUCT<city STRING, state STRING>>[("Seattle", "Washington"),
    ("Phoenix", "Arizona")] AS location)
SELECT l.LOCATION[offset(0)].*
FROM locations l;

/*---------+------------+
 | city    | state      |
 +---------+------------+
 | Seattle | Washington |
 +---------+------------*/
```

### `SELECT * EXCEPT`

A `SELECT * EXCEPT` statement specifies the names of one or more columns to
exclude from the result. All matching column names are omitted from the output.

```
WITH orders AS
  (SELECT 5 as order_id,
  "sprocket" as item_name,
  200 as quantity)
SELECT * EXCEPT (order_id)
FROM orders;

/*-----------+----------+
 | item_name | quantity |
 +-----------+----------+
 | sprocket  | 200      |
 +-----------+----------*/
```

**Note:** `SELECT * EXCEPT` doesn't exclude columns that don't have names.

### `SELECT * REPLACE`

A `SELECT * REPLACE` statement specifies one or more
`expression AS identifier` clauses. Each identifier must match a column name
from the `SELECT *` statement. In the output column list, the column that
matches the identifier in a `REPLACE` clause is replaced by the expression in
that `REPLACE` clause.

A `SELECT * REPLACE` statement doesn't change the names or order of columns.
However, it can change the value and the value type.

```
WITH orders AS
  (SELECT 5 as order_id,
  "sprocket" as item_name,
  200 as quantity)
SELECT * REPLACE ("widget" AS item_name)
FROM orders;

/*----------+-----------+----------+
 | order_id | item_name | quantity |
 +----------+-----------+----------+
 | 5        | widget    | 200      |
 +----------+-----------+----------*/

WITH orders AS
  (SELECT 5 as order_id,
  "sprocket" as item_name,
  200 as quantity)
SELECT * REPLACE (quantity/2 AS quantity)
FROM orders;

/*----------+-----------+----------+
 | order_id | item_name | quantity |
 +----------+-----------+----------+
 | 5        | sprocket  | 100      |
 +----------+-----------+----------*/
```

**Note:** `SELECT * REPLACE` doesn't replace columns that don't have names.

### `SELECT DISTINCT`

A `SELECT DISTINCT` statement discards duplicate rows and returns only the
remaining rows. `SELECT DISTINCT` can't return columns of the following types:

* `GRAPH_ELEMENT`
* `GRAPH_PATH`

In the following example, `SELECT DISTINCT` is used to produce distinct arrays:

```
WITH PlayerStats AS (
  SELECT ['Coolidge', 'Adams'] as Name, 3 as PointsScored UNION ALL
  SELECT ['Adams', 'Buchanan'], 0 UNION ALL
  SELECT ['Coolidge', 'Adams'], 1 UNION ALL
  SELECT ['Kiran', 'Noam'], 1)
SELECT DISTINCT Name
FROM PlayerStats;

/*------------------+
 | Name             |
 +------------------+
 | [Coolidge,Adams] |
 | [Adams,Buchanan] |
 | [Kiran,Noam]     |
 +------------------*/
```

In the following example, `SELECT DISTINCT` is used to produce distinct structs:

```
WITH
  PlayerStats AS (
    SELECT
      STRUCT<last_name STRING, first_name STRING, age INT64>(
        'Adams', 'Noam', 20) AS Player,
      3 AS PointsScored UNION ALL
    SELECT ('Buchanan', 'Jie', 19), 0 UNION ALL
    SELECT ('Adams', 'Noam', 20), 4 UNION ALL
    SELECT ('Buchanan', 'Jie', 19), 13
  )
SELECT DISTINCT Player
FROM PlayerStats;

/*--------------------------+
 | player                   |
 +--------------------------+
 | {                        |
 |   last_name: "Adams",    |
 |   first_name: "Noam",    |
 |   age: 20                |
 |  }                       |
 +--------------------------+
 | {                        |
 |   last_name: "Buchanan", |
 |   first_name: "Jie",     |
 |   age: 19                |
 |  }                       |
 +---------------------------*/
```

### `SELECT ALL`

A `SELECT ALL` statement returns all rows, including duplicate rows.
`SELECT ALL` is the default behavior of `SELECT`.

### `SELECT AS STRUCT`

```
SELECT AS STRUCT expr [[AS] struct_field_name1] [,...]
```

This produces a [value table](#value_tables) with a
STRUCT row type, where the
STRUCT field names and types match the column names
and types produced in the `SELECT` list.

Example:

```
SELECT ARRAY(SELECT AS STRUCT 1 a, 2 b)
```

`SELECT AS STRUCT` can be used in a scalar or array subquery to produce a single
STRUCT type grouping multiple values together. Scalar
and array subqueries (see [Subqueries](/bigquery/docs/reference/standard-sql/subqueries)) are normally not
allowed to return multiple columns, but can return a single column with
STRUCT type.

### `SELECT AS VALUE`

`SELECT AS VALUE` produces a [value table](#value_tables) from any
`SELECT` list that produces exactly one column. Instead of producing an
output table with one column, possibly with a name, the output will be a
value table where the row type is just the value type that was produced in the
one `SELECT` column. Any alias the column had will be discarded in the
value table.

Example:

```
SELECT AS VALUE STRUCT(1 AS a, 2 AS b) xyz
```

The query above produces a table with row type `STRUCT<a int64, b int64>`.

## `FROM` clause

```
FROM from_clause[, ...]

from_clause:
  from_item
  [ { pivot_operator | unpivot_operator | match_recognize_clause } ]
  [ tablesample_operator ]

from_item:
  {
    table_name [ as_alias ] [ FOR SYSTEM_TIME AS OF timestamp_expression ] 
    | { join_operation | ( join_operation ) }
    | ( query_expr ) [ as_alias ]
    | field_path
    | unnest_operator
    | cte_name [ as_alias ]
    | graph_table_operator [ as_alias ]
  }

as_alias:
  [ AS ] alias
```

The `FROM` clause indicates the table or tables from which to retrieve rows,
and specifies how to join those rows together to produce a single stream of
rows for processing in the rest of the query.

#### `pivot_operator`

See [PIVOT operator](#pivot_operator).

#### `unpivot_operator`

See [UNPIVOT operator](#unpivot_operator).

#### `tablesample_operator`

See [TABLESAMPLE operator](#tablesample_operator).

#### `match_recognize_clause`

See [MATCH\_RECOGNIZE clause](#match_recognize_clause).

#### `graph_table_operator`

See [GRAPH\_TABLE operator](/bigquery/docs/reference/standard-sql/graph-sql-queries#graph_table_operator).

#### `table_name`

The name (optionally qualified) of an existing table.

```
SELECT * FROM Roster;
SELECT * FROM dataset.Roster;
SELECT * FROM project.dataset.Roster;
```

#### `FOR SYSTEM_TIME AS OF`

`FOR SYSTEM_TIME AS OF` references the historical versions of the table
definition and rows that were current at `timestamp_expression`.

Limitations:

The source table in the `FROM` clause containing `FOR SYSTEM_TIME AS OF` must
not be any of the following:

* An array scan, including a
  [flattened array](/bigquery/docs/arrays#flattening_arrays) or the output
  of the `UNNEST` operator.
* A common table expression defined by a `WITH` clause.
* The source table in a `CREATE TABLE FUNCTION`
  statement creating a new table-valued function

`timestamp_expression` must be a constant expression. It can't
contain the following:

* Subqueries.
* Correlated references (references to columns of a table that appear at
  a higher level of the query statement, such as in the `SELECT` list).
* User-defined functions (UDFs).

The value of `timestamp_expression` can't fall into the following ranges:

* After the current timestamp (in the future).
* More than seven (7) days before the current timestamp.

A single query statement can't reference a single table at more than one point
in time, including the current time. That is, a query can reference a table
multiple times at the same timestamp, but not the current version and a
historical version, or two different historical versions.

**Note:** DML statements always operate on the current version of the destination
table, so if the destination table is used multiple times in the query, all of
them must use the current version.

The default time zone for `timestamp_expression` in a
`FOR SYSTEM_TIME AS OF` expression is `America/Los_Angeles`, even though the
default time zone for timestamp literals is `UTC`.

Examples:

The following query returns a historical version of the table from one hour ago.

```
SELECT *
FROM t
  FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 HOUR);
```

The following query returns a historical version of the table at an absolute
point in time.

```
SELECT *
FROM t
  FOR SYSTEM_TIME AS OF '2017-01-01 10:00:00-07:00';
```

The following query returns an error because the `timestamp_expression` contains
a correlated reference to a column in the containing query.

```
SELECT *
FROM t1
WHERE t1.a IN (SELECT t2.a
               FROM t2 FOR SYSTEM_TIME AS OF t1.timestamp_column);
```

The following operations show accessing a historical version of the table before
table is replaced.

```
DECLARE before_replace_timestamp TIMESTAMP;

-- Create table books.
CREATE TABLE books AS
SELECT 'Hamlet' title, 'William Shakespeare' author;

-- Get current timestamp before table replacement.
SET before_replace_timestamp = CURRENT_TIMESTAMP();

-- Replace table with different schema(title and release_date).
CREATE OR REPLACE TABLE books AS
SELECT 'Hamlet' title, DATE '1603-01-01' release_date;

-- This query returns Hamlet, William Shakespeare as result.
SELECT * FROM books FOR SYSTEM_TIME AS OF before_replace_timestamp;
```

The following operations show accessing a historical version of the table
before a DML job.

```
DECLARE JOB_START_TIMESTAMP TIMESTAMP;

-- Create table books.
CREATE OR REPLACE TABLE books AS
SELECT 'Hamlet' title, 'William Shakespeare' author;

-- Insert two rows into the books.
INSERT books (title, author)
VALUES('The Great Gatsby', 'F. Scott Fizgerald'),
      ('War and Peace', 'Leo Tolstoy');

SELECT * FROM books;

SET JOB_START_TIMESTAMP = (
  SELECT start_time
  FROM `region-us`.INFORMATION_SCHEMA.JOBS_BY_USER
  WHERE job_type="QUERY"
    AND statement_type="INSERT"
  ORDER BY start_time DESC
  LIMIT 1
 );

-- This query only returns Hamlet, William Shakespeare as result.
SELECT * FROM books FOR SYSTEM_TIME AS OF JOB_START_TIMESTAMP;
```

The following query returns an error because the DML operates on the current
version of the table, and a historical version of the table from one day ago.

```
INSERT INTO t1
SELECT * FROM t1
  FOR SYSTEM_TIME AS OF TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 1 DAY);
```

#### `join_operation`

See [Join operation](#join_types).

#### `query_expr`

`( query_expr ) [ [ AS ] alias ]` is a [table subquery](/bigquery/docs/reference/standard-sql/subqueries#table_subquery_concepts).

#### `field_path`

In the `FROM` clause, `field_path` is any path that
resolves to a field within a data type. `field_path` can go
arbitrarily deep into a nested data structure.

Some examples of valid `field_path` values include:

```
SELECT * FROM T1 t1, t1.array_column;

SELECT * FROM T1 t1, t1.struct_column.array_field;

SELECT (SELECT ARRAY_AGG(c) FROM t1.array_column c) FROM T1 t1;

SELECT a.struct_field1 FROM T1 t1, t1.array_of_structs a;

SELECT (SELECT STRING_AGG(a.struct_field1) FROM t1.array_of_structs a)
```