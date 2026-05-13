* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Pipe query syntax Stay organized with collections Save and categorize content based on your preferences.

Pipe query syntax is an extension to GoogleSQL that's simpler and more
concise than [standard query syntax](/bigquery/docs/reference/standard-sql/query-syntax). Pipe syntax supports the
same operations as standard syntax, and improves some areas of SQL query
functionality and usability.

For more background and details on pipe syntax design, see the research paper
[SQL Has Problems. We Can Fix Them: Pipe Syntax In SQL](https://research.google/pubs/sql-has-problems-we-can-fix-them-pipe-syntax-in-sql/).
For an introduction to pipe syntax, see
[Work with pipe syntax](/bigquery/docs/pipe-syntax-guide).
To see examples of more complex queries written in pipe syntax,
see [Analyze data using pipe syntax](/bigquery/docs/analyze-data-pipe-syntax).

## Pipe syntax

Pipe syntax has the following key characteristics:

* Each pipe operator in pipe syntax consists of the pipe symbol, `|>`,
  an operator name, and any arguments:   
  `|> operator_name argument_list`
* Pipe operators can be added to the end of any valid query.
* Pipe syntax works anywhere standard syntax is supported: in queries, views,
  table-valued functions (TVFs), and other contexts.
* Pipe syntax can be mixed with standard syntax in the same query. For
  example, subqueries can use different syntax from the parent query.
* A pipe operator can see every alias that exists in the table
  preceding the pipe.
* A query can [start with a `FROM` clause](#from_queries), and pipe
  operators can optionally be added after the `FROM` clause.

### Query comparison

Consider the following table called `Produce`:

```
CREATE OR REPLACE TABLE Produce AS (
  SELECT 'apples' AS item, 2 AS sales, 'fruit' AS category
  UNION ALL
  SELECT 'carrots' AS item, 8 AS sales, 'vegetable' AS category
  UNION ALL
  SELECT 'apples' AS item, 7 AS sales, 'fruit' AS category
  UNION ALL
  SELECT 'bananas' AS item, 5 AS sales, 'fruit' AS category
);

SELECT * FROM Produce;

/*---------+-------+-----------+
 | item    | sales | category  |
 +---------+-------+-----------+
 | apples  | 2     | fruit     |
 | carrots | 8     | vegetable |
 | apples  | 7     | fruit     |
 | bananas | 5     | fruit     |
 +---------+-------+-----------*/
```

Compare the following equivalent queries that compute the number and total
amount of sales for each item in the `Produce` table:

**Standard syntax**

```
SELECT item, COUNT(*) AS num_items, SUM(sales) AS total_sales
FROM Produce
WHERE
  item != 'bananas'
  AND category IN ('fruit', 'nut')
GROUP BY item
ORDER BY item DESC;

/*--------+-----------+-------------+
 | item   | num_items | total_sales |
 +--------+-----------+-------------+
 | apples | 2         | 9           |
 +--------+-----------+-------------*/
```

**Pipe syntax**

```
FROM Produce
|> WHERE
    item != 'bananas'
    AND category IN ('fruit', 'nut')
|> AGGREGATE COUNT(*) AS num_items, SUM(sales) AS total_sales
   GROUP BY item
|> ORDER BY item DESC;

/*--------+-----------+-------------+
 | item   | num_items | total_sales |
 +--------+-----------+-------------+
 | apples | 2         | 9           |
 +--------+-----------+-------------*/
```

## Pipe operator semantics

Pipe operators have the following semantic behavior:

* Each pipe operator performs a self-contained operation.
* A pipe operator consumes the input table passed to it through the pipe
  symbol, `|>`, and produces a new table as output.
* A pipe operator can reference only columns from its immediate input table.
  Columns from earlier in the same query aren't visible. Inside subqueries,
  correlated references to outer columns are still allowed.

## `FROM` queries

In pipe syntax, a query can start with a standard [`FROM` clause](/bigquery/docs/reference/standard-sql/query-syntax#from_clause)
and use any standard `FROM` syntax, including tables, joins, subqueries,
and
table-valued functions (TVFs). Table aliases can be
assigned to each input item using the [`AS alias` clause](/bigquery/docs/reference/standard-sql/query-syntax#using_aliases).

A query with only a `FROM` clause, like `FROM table_name`, is allowed in pipe
syntax and returns all rows from the table. For tables with columns,
`FROM table_name` in pipe syntax is similar to
[`SELECT * FROM table_name`](/bigquery/docs/reference/standard-sql/query-syntax#select_) in standard syntax.

**Examples**

The following queries use the [`Produce` table](#query_comparison):

```
FROM Produce;

/*---------+-------+-----------+
 | item    | sales | category  |
 +---------+-------+-----------+
 | apples  | 2     | fruit     |
 | carrots | 8     | vegetable |
 | apples  | 7     | fruit     |
 | bananas | 5     | fruit     |
 +---------+-------+-----------*/
```

```
-- Join tables in the FROM clause and then apply pipe operators.
FROM
  Produce AS p1
  JOIN Produce AS p2
    USING (item)
|> WHERE item = 'bananas'
|> SELECT p1.item, p2.sales;

/*---------+-------+
 | item    | sales |
 +---------+-------+
 | bananas | 5     |
 +---------+-------*/
```

## Pipe operators

GoogleSQL supports the following pipe operators. For operators that
correspond or relate to similar operations in standard syntax, the operator
descriptions highlight similarities and differences and link to more detailed
documentation on the corresponding syntax.

### Pipe operator list

| Name | Summary |
| --- | --- |
| [`SELECT`](#select_pipe_operator) | Produces a new table with the listed columns. |
| [`EXTEND`](#extend_pipe_operator) | Propagates the existing table and adds computed columns. |
| [`SET`](#set_pipe_operator) | Replaces the values of columns in the input table. |
| [`DROP`](#drop_pipe_operator) | Removes listed columns from the input table. |
| [`RENAME`](#rename_pipe_operator) | Renames specified columns. |
| [`AS`](#as_pipe_operator) | Introduces a table alias for the input table. |
| [`WHERE`](#where_pipe_operator) | Filters the results of the input table. |
| [`AGGREGATE`](#aggregate_pipe_operator) | Performs aggregation on data across groups of rows or the full input table. |
| [`DISTINCT`](#distinct_pipe_operator) | Returns distinct rows from the input table, while preserving table aliases. |
| [`JOIN`](#join_pipe_operator) | Joins rows from the input table with rows from a second table provided as an argument. |
| [`CALL`](#call_pipe_operator) | Calls a table-valued function (TVF), passing the pipe input table as a table argument. |
| [`ORDER BY`](#order_by_pipe_operator) | Sorts results by a list of expressions. |
| [`LIMIT`](#limit_pipe_operator) | Limits the number of rows to return in a query, with an optional `OFFSET` clause to skip over rows. |
| [`UNION`](#union_pipe_operator) | Returns the combined results of the input queries to the left and right of the pipe operator. |
| [`INTERSECT`](#intersect_pipe_operator) | Returns rows that are found in the results of both the input query to the left of the pipe operator and all input queries to the right of the pipe operator. |
| [`EXCEPT`](#except_pipe_operator) | Returns rows from the input query to the left of the pipe operator that aren't present in any input queries to the right of the pipe operator. |
| [`TABLESAMPLE`](#tablesample_pipe_operator) | Selects a random sample of rows from the input table. |
| [`WITH`](#with_pipe_operator) | Introduces one or more common table expressions (CTEs). |
| [`PIVOT`](#pivot_pipe_operator) | Rotates rows into columns. |
| [`UNPIVOT`](#unpivot_pipe_operator) | Rotates columns into rows. |
| [`MATCH_RECOGNIZE`](#match_recognize_pipe_operator) | Filters and aggregates rows based on matches. |

### `SELECT` pipe operator

```
|> SELECT expression [[AS] alias] [, ...]
   [WINDOW name AS window_spec, ...]
```

**Description**

Produces a new table with the listed columns, similar to the outermost
[`SELECT` clause](/bigquery/docs/reference/standard-sql/query-syntax#select_list) in a table subquery in standard syntax. The
`SELECT` operator supports standard output modifiers like `SELECT AS STRUCT` and
`SELECT DISTINCT`. The `SELECT` operator
also supports [window functions](/bigquery/docs/reference/standard-sql/window-function-calls),
including [named windows](/bigquery/docs/reference/standard-sql/window-function-calls#def_use_named_window). Named windows are defined using the
`WINDOW` keyword and are only visible to the current pipe `SELECT` operator.
The `SELECT` operator doesn't support aggregations or anonymization.

In pipe syntax, the `SELECT` operator in a query is optional. The `SELECT`
operator can be used near the end of a query to specify the list of output
columns. The final query result contains the columns returned from the last pipe
operator. If the `SELECT` operator isn't used to select specific columns, the
output includes the full row, similar to what the
[`SELECT *` statement](/bigquery/docs/reference/standard-sql/query-syntax#select_) in standard syntax produces.

In pipe syntax, the `SELECT` clause doesn't perform aggregation. Use the
[`AGGREGATE` operator](#aggregate_pipe_operator) instead.

For cases where `SELECT` would be used in standard syntax to rearrange columns,
pipe syntax supports other operators:

* The [`EXTEND` operator](#extend_pipe_operator) adds columns.
* The [`SET` operator](#set_pipe_operator) updates the value of an existing
  column.
* The [`DROP` operator](#drop_pipe_operator) removes columns.
* The [`RENAME` operator](#rename_pipe_operator) renames columns.

**Examples**

```
FROM (SELECT 'apples' AS item, 2 AS sales)
|> SELECT item AS fruit_name;

/*------------+
 | fruit_name |
 +------------+
 | apples     |
 +------------*/
```

```
-- Window function with a named window
FROM Produce
|> SELECT item, sales, category, SUM(sales) OVER item_window AS category_total
   WINDOW item_window AS (PARTITION BY category);

/*---------+-------+-----------+----------------+
 | item    | sales | category  | category_total |
 +---------+-------+-----------+----------------+
 | apples  | 2     | fruit     | 14             |
 | apples  | 7     | fruit     | 14             |
 | bananas | 5     | fruit     | 14             |
 | carrots | 8     | vegetable | 8              |
 +---------+-------+-----------+----------------*/
```

### `EXTEND` pipe operator

```
|> EXTEND expression [[AS] alias] [, ...]
   [WINDOW name AS window_spec, ...]
```

**Description**

Propagates the existing table and adds computed columns, similar to
[`SELECT *, new_column`](/bigquery/docs/reference/standard-sql/query-syntax#select_) in standard syntax. The `EXTEND` operator supports
[window functions](/bigquery/docs/reference/standard-sql/window-function-calls)
, including [named windows](/bigquery/docs/reference/standard-sql/window-function-calls#def_use_named_window). Named windows are defined using the
`WINDOW` keyword and are only visible to the current `EXTEND` operator.

**Examples**

```
(
  SELECT 'apples' AS item, 2 AS sales
  UNION ALL
  SELECT 'bananas' AS item, 8 AS sales
)
|> EXTEND item IN ('bananas', 'lemons') AS is_yellow;

/*---------+-------+------------+
 | item    | sales | is_yellow  |
 +---------+-------+------------+
 | apples  | 2     | FALSE      |
 | bananas | 8     | TRUE       |
 +---------+-------+------------*/
```

```
-- Window function, with `OVER`
(
  SELECT 'apples' AS item, 2 AS sales
  UNION ALL
  SELECT 'bananas' AS item, 5 AS sales
  UNION ALL
  SELECT 'carrots' AS item, 8 AS sales
)
|> EXTEND SUM(sales) OVER() AS total_sales;

/*---------+-------+-------------+
 | item    | sales | total_sales |
 +---------+-------+-------------+
 | apples  | 2     | 15          |
 | bananas | 5     | 15          |
 | carrots | 8     | 15          |
 +---------+-------+-------------*/
```

```
-- Window function with a named window
FROM Produce
|> EXTEND SUM(sales) OVER item_window AS category_total
   WINDOW item_window AS (PARTITION BY category);

/*-----------+-----------+----------------+
 | item      | category  | category_total |
 +----------------------------------------+
 | apples    | fruit     | 14             |
 | apples    | fruit     | 14             |
 | bananas   | fruit     | 14             |
 | carrots   | vegetable | 8              |
 +----------------------------------------*/
```

### `SET` pipe operator

```
|> SET column = expression [, ...]
```

**Description**

Replaces the value of a column in the input table, similar to
[`SELECT * REPLACE (expression AS column)`](/bigquery/docs/reference/standard-sql/query-syntax#select_replace) in standard syntax.
Each referenced column must exist exactly once in the input table.

After a `SET` operation, the referenced top-level columns (like `x`) are
updated, but table aliases (like `t`) still refer to the original row values.
Therefore, `t.x` will still refer to the original value.

**Example**

```
(
  SELECT 1 AS x, 11 AS y
  UNION ALL
  SELECT 2 AS x, 22 AS y
)
|> SET x = x * x, y = 3;

/*---+---+
 | x | y |
 +---+---+
 | 1 | 3 |
 | 4 | 3 |
 +---+---*/
```

```
FROM (SELECT 2 AS x, 3 AS y) AS t
|> SET x = x * x, y = 8
|> SELECT t.x AS original_x, x, y;

/*------------+---+---+
 | original_x | x | y |
 +------------+---+---+
 | 2          | 4 | 8 |
 +------------+---+---*/
```

### `DROP` pipe operator

```
|> DROP column [, ...]
```

**Description**

Removes listed columns from the input table, similar to
[`SELECT * EXCEPT (column)`](/bigquery/docs/reference/standard-sql/query-syntax#select_except) in standard syntax. Each
referenced column must exist at least once in the input table.

After a `DROP` operation, the referenced top-level columns (like `x`) are
removed, but table aliases (like `t`) still refer to the original row values.
Therefore, `t.x` will still refer to the original value.

**Example**

```
SELECT 'apples' AS item, 2 AS sales, 'fruit' AS category
|> DROP sales, category;

/*--------+
 | item   |
 +--------+
 | apples |
 +--------*/
```

```
FROM (SELECT 1 AS x, 2 AS y) AS t
|> DROP x
|> SELECT t.x AS original_x, y;

/*------------+---+
 | original_x | y |
 +------------+---+
 | 1          | 2 |
 +------------+---*/
```

### `RENAME` pipe operator

```
|> RENAME old_column_name [AS] new_column_name [, ...]
```

**Description**

Renames specified columns. Each column to be renamed must exist exactly once in
the input table. The `RENAME` operator can't rename value table fields,
pseudo-columns, range variables, or objects that aren't columns in the input
table.

After a `RENAME` operation, the referenced top-level columns (like `x`) are
renamed, but table aliases (like `t`) still refer to the original row
values. Therefore, `t.x` will still refer to the original value.

**Example**

```
SELECT 1 AS x, 2 AS y, 3 AS z
|> AS t
|> RENAME y AS renamed_y
|> SELECT *, t.y AS t_y;

/*---+-----------+---+-----+
 | x | renamed_y | z | t_y |
 +---+-----------+---+-----+
 | 1 | 2         | 3 | 2   |
 +---+-----------+---+-----*/
```

### `AS` pipe operator

```
|> AS alias
```

**Description**

Introduces a table alias for the input table, similar to applying the
[`AS alias` clause](/bigquery/docs/reference/standard-sql/query-syntax#using_aliases) on a table subquery in standard syntax. Any
existing table aliases are removed and the new alias becomes the table alias for
all columns in the row.

The `AS` operator can be useful after operators like
[`SELECT`](#select_pipe_operator), [`EXTEND`](#extend_pipe_operator), or
[`AGGREGATE`](#aggregate_pipe_operator) that add columns but can't give table
aliases to them. You can use the table alias
to disambiguate columns after the `JOIN` operator.

**Example**

```
(
  SELECT "000123" AS id, "apples" AS item, 2 AS sales
  UNION ALL
  SELECT "000456" AS id, "bananas" AS item, 5 AS sales
) AS sales_table
|> AGGREGATE SUM(sales) AS total_sales GROUP BY id, item
-- AGGREGATE creates an output table, so the sales_table alias is now out of
-- scope. Add a t1 alias so the join can refer to its id column.
|> AS t1
|> JOIN (SELECT 456 AS id, "yellow" AS color) AS t2
   ON CAST(t1.id AS INT64) = t2.id
|> SELECT t2.id, total_sales, color;

/*-----+-------------+--------+
 | id  | total_sales | color  |
 +-----+-------------+--------+
 | 456 | 5           | yellow |
 +-----+-------------+--------*/
```