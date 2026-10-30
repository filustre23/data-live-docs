* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Aggregate function calls Stay organized with collections Save and categorize content based on your preferences.

An aggregate function summarizes the rows of a group into a single value.
When an aggregate function is used with
the `OVER` clause, it becomes a window function, which computes values over a
group of rows and then returns a single result for each row.

## Aggregate function call syntax

```
function_name(
  [ DISTINCT ]
  function_arguments
  [ { IGNORE | RESPECT } NULLS ]
  [ WHERE where_expression ]
  [ { HAVING { MAX | MIN } having_expression | GROUP BY grouping_expression [, ... ] [ HAVING having_expression ] } ]
  [ ORDER BY key [ { ASC | DESC } ] [, ... ] ]
  [ LIMIT n ]
)
[ OVER over_clause ]
```

**Description**

Each aggregate function supports all or a subset of the aggregate function call
syntax. To build an aggregate function, use the following syntax:

* `DISTINCT`: Aggregate each distinct value of an expression only once into the
  result.
* `function_arguments`: Specify the input values, columns, or expressions that
  the aggregate function evaluates and summarizes across the rows of a group.
* `IGNORE NULLS` or `RESPECT NULLS`: If `IGNORE NULLS` is
  specified, the `NULL` values are excluded from the result. If
  `RESPECT NULLS` is specified, both `NULL` and non-`NULL` values can be
  included in the result.

  If neither `IGNORE NULLS` nor `RESPECT NULLS` is specified, most functions
  default to `IGNORE NULLS` behavior but in a few cases `NULL` values are
  respected.
* `WHERE`: ([Preview](https://cloud.google.com/products#product-launch-stages)) Filters the aggregate function input using a boolean expression.
* `HAVING MAX` or `HAVING MIN`: Restricts the set of rows that the
  function aggregates by a maximum or minimum value.
  For details, see [HAVING MAX and HAVING MIN clause](#max_min_clause).
* `GROUP BY`: Performs an additional grouping on input rows to the aggregate
  function. Used to define [multi-level aggregates](#multi_level_aggregation).
  The `HAVING` clause in the `GROUP BY` clause filters the grouped output. The
  `HAVING` clause must be a scalar expression or an aggregate expression that
  doesn't use window functions.
* `ORDER BY`: Specifies the order of the values.

  + For each sort key, the default sort direction is `ASC`.
  + `NULL` is the minimum possible value, so `NULL`s appear first
    in `ASC` sorts and last in `DESC` sorts.
  + If you're using floating point data types, see
    [Floating point semantics](/bigquery/docs/reference/standard-sql/data-types#floating_point_semantics)
    on ordering and grouping.
  + The `ORDER BY` clause is supported only for aggregate functions that
    depend on the order of their input. For those functions, if the
    `ORDER BY` clause is omitted, the output is nondeterministic.
  + This `ORDER BY` clause can't be used if the `OVER` clause is used.
  + If `DISTINCT` is also specified, then
    the sort key must be the same as `expression`.
* `LIMIT`: Specifies the maximum number of `expression` inputs in the
  result.

  + If the input is an `ARRAY` value, the limit applies to the number of input
    arrays, not the number of elements in the arrays. An empty array counts
    as `1`. A `NULL` array isn't counted.
  + If the input is a `STRING` value, the limit applies to the number of input
    strings, not the number of characters or bytes in the inputs. An empty
    string counts as `1`. A `NULL` string isn't counted.
  + The limit `n` must be a constant `INT64`.
* `OVER`: If the aggregate function is also a window function, use this clause
  to define a window of rows around the row being evaluated. For each row,
  the aggregate function result is computed using the selected window of rows as
  input. If the `OVER` clause is used, aggregate function
  clauses, such as
  `DISTINCT`, aren't supported, but function call
  modifiers, such as `IGNORE_NULLS`,
  are still supported. To learn more about the `OVER` clause,
  see [Window function calls](/bigquery/docs/reference/standard-sql/window-function-calls).

**Details**

The clauses in an aggregate function call are applied in the following order:

* `OVER`
* `WHERE`
* `HAVING MAX`/`HAVING MIN` or `GROUP BY` with `HAVING`
* `IGNORE NULLS` or `RESPECT NULLS`
* `DISTINCT`
* `ORDER BY`
* `LIMIT`

When used in conjunction with a `GROUP BY` clause, the groups summarized
typically have at least one row. When the associated `SELECT` statement has
no `GROUP BY` clause or when certain aggregate function modifiers filter rows
from the group to be summarized, it's possible that the aggregate function
needs to summarize an empty group.

## Restrict aggregation by a maximum or minimum value

Some aggregate functions support two optional clauses that are called
`HAVING MAX` and `HAVING MIN`. These clauses restrict the set of rows that a
function aggregates to rows that have a maximum or minimum value in a particular
column. These clauses are also
different from the `GROUP BY ... HAVING ...` clauses, which aggregate
specifically grouped output.

### HAVING MAX clause

```
HAVING MAX having_expression
```

`HAVING MAX` restricts the set of input rows that the function aggregates to
only those with the maximum `having_expression` value. The maximum value is
computed as the result of `MAX(having_expression)` across rows in the group.
Only rows whose `having_expression` value is equal to this maximum value (using
SQL equality semantics) are included in the aggregation. All other rows are
ignored in the aggregation.

This clause supports all [orderable data types](/bigquery/docs/reference/standard-sql/data-types#data_type_properties),
except for `ARRAY`.

**Examples**

In the following query, rows with the most inches of precipitation, `4`, are
added to a group, and then the `year` for one of these rows is produced.
Which row is produced is nondeterministic, not random.

```
WITH
  Precipitation AS (
    SELECT 2009 AS year, 'spring' AS season, 3 AS inches
    UNION ALL
    SELECT 2001, 'winter', 4
    UNION ALL
    SELECT 2003, 'fall', 1
    UNION ALL
    SELECT 2002, 'spring', 4
    UNION ALL
    SELECT 2005, 'summer', 1
  )
SELECT ANY_VALUE(year HAVING MAX inches) AS any_year_with_max_inches FROM Precipitation;

/*--------------------------+
 | any_year_with_max_inches |
 +--------------------------+
 | 2001                     |
 +--------------------------*/
```

### HAVING MIN clause

```
HAVING MIN having_expression
```

`HAVING MIN` restricts the set of input rows that the function aggregates to
only those with the minimum `having_expression` value. The minimum value is
computed as the result of `MIN(having_expression)` across rows in the group.
Only rows whose `having_expression` value is equal to this minimum value (using
SQL equality semantics) are included in the aggregation. All other rows are
ignored in the aggregation.

This clause supports all [orderable data types](/bigquery/docs/reference/standard-sql/data-types#data_type_properties),
except for `ARRAY`.

**Examples**

In the following query, rows with the fewest inches of precipitation, `1`,
are added to a group, and then the `year` for one of these rows is produced.
Which row is produced is nondeterministic, not random.

```
WITH
  Precipitation AS (
    SELECT 2009 AS year, 'spring' AS season, 3 AS inches
    UNION ALL
    SELECT 2001, 'winter', 4
    UNION ALL
    SELECT 2003, 'fall', 1
    UNION ALL
    SELECT 2002, 'spring', 4
    UNION ALL
    SELECT 2005, 'summer', 1
  )
SELECT ANY_VALUE(year HAVING MIN inches) AS any_year_with_min_inches FROM Precipitation;

/*--------------------------+
 | any_year_with_min_inches |
 +--------------------------+
 | 2003                     |
 +--------------------------*/
```

## Handle `NULL` values before aggregation

Most aggregate functions, such as `AVG`, `SUM`, `MIN`, `MAX`, and
`COUNT(expression)`, ignore `NULL` values by default. In contrast, `COUNT(*)`
counts all input rows, including rows with `NULL` values.

For example, the following query aggregates a set of values that includes
`NULL`:

```
SELECT
  COUNT(*) AS row_count,
  COUNT(x) AS non_null_rows,
  AVG(x) AS avg_x
FROM UNNEST([1, 2, 3, 4, 5, NULL]) AS x;

/*------------+---------------+-------+
 | row_count | non_null_rows | avg_x |
 +------------+---------------+-------+
 | 6          | 5             | 3     |
 +------------+---------------+-------*/
```

You can also exclude or replace `NULL` values in one of the following ways:

* Add a `WHERE` clause inside the aggregate function call; for example, `COUNT(* WHERE x IS NOT NULL)`.
* Use the `IGNORE NULLS` clause for aggregate functions that include `NULL`
  values by default, such as `ARRAY_AGG(x IGNORE NULLS)`.
* Use [`COALESCE`](/bigquery/docs/reference/standard-sql/conditional_expressions#coalesce) to replace `NULL` values with a default
  value before aggregating, such as `AVG(COALESCE(x, 0))`.

For example, to filter out `NULL` values for an individual aggregate function
call without removing rows from the rest of the query, use a `WHERE` clause
inside the function call:

```
SELECT
  COUNT(*) AS total_rows,
  COUNT(* WHERE x IS NOT NULL) AS filtered_rows,
  AVG(x) AS avg_x
FROM UNNEST([1, 2, 3, 4, 5, NULL]) AS x;

/*------------+---------------+-------+
 | total_rows | filtered_rows | avg_x |
 +------------+---------------+-------+
 | 6          | 5             | 3     |
 +------------+---------------+-------*/
```

## Aggregate function examples

A simple aggregate function call for `COUNT`, `MIN`, and `MAX` looks like this:

```
SELECT
  COUNT(*) AS total_count,
  COUNT(fruit) AS non_null_count,
  MIN(fruit) AS min,
  MAX(fruit) AS max
FROM
  (
    SELECT NULL AS fruit
    UNION ALL
    SELECT 'apple'
```