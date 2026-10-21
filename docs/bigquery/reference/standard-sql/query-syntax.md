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

**Note:** `SELECT * EXCEPT` doesn't exclude columns that don't have names. Also,
`SELECT * EXCEPT` and the [`EXCEPT`](/bigquery/docs/reference/standard-sql/query-syntax#except) set operator have different use
cases and rules.

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
SELECT AS STRUCT
```