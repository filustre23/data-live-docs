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
  [ { HAVING { MAX | MIN } having_expression | GROUP BY grouping_expression [, ... ] } ]
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
* `HAVING MAX` or `HAVING MIN`: Restricts the set of rows that the
  function aggregates by a maximum or minimum value.
  For details, see [HAVING MAX and HAVING MIN clause](#max_min_clause).
* `GROUP BY`: Performs an additional grouping on input rows to the aggregate
  function. Used to define [multi-level aggregates](#multi_level_aggregation).
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
* `HAVING MAX`/`HAVING MIN` or `GROUP BY`
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
column.

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
    SELECT 'apple' AS fruit
    UNION ALL
    SELECT 'pear' AS fruit
    UNION ALL
    SELECT 'orange' AS fruit
  )

/*-------------+----------------+-------+------+
 | total_count | non_null_count | min   | max  |
 +-------------+----------------+-------+------+
 | 4           | 3              | apple | pear |
 +-------------+----------------+-------+------*/
```

In the following example, the average of `x` over a specified window is returned
for each row. To learn more about windows and how to use them, see
[Window function calls](/bigquery/docs/reference/standard-sql/window-function-calls).

```
SELECT
  x,
  AVG(x) OVER (ORDER BY x ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS avg
FROM UNNEST([0, 2, 4, 4, 5]) AS x;

/*------+------+
 | x    | avg  |
 +------+------+
 | 0    | 0    |
 | 2    | 1    |
 | 4    | 3    |
 | 4    | 4    |
 | 5    | 4.5  |
 +------+------*/
```

## Multi-level aggregation

**Preview**

This product or feature is subject to the "Pre-GA Offerings Terms"
in the General Service Terms section of the
[Service Specific Terms](https://cloud.google.com/terms/service-terms).
Pre-GA products and features are available "as is" and might have
limited support. For more information, see the
[launch stage descriptions](https://cloud.google.com/products#product-launch-stages).

**Note:** To provide feedback or request support for this feature, send an email to
[bigquery-sql-preview-support@googlegroups.com](mailto:bigquery-sql-preview-support@googlegroups.com).

Standard SQL doesn't allow an aggregate function to have other aggregate
functions as arguments. As a result, expressing multi-stage aggregation
typically requires using a subquery.

For example, say you have a table of sales data and want to calculate the
average daily sales by averaging the sums of the rows. You can do this with a
subquery:

```
WITH Sales AS (
  SELECT 'Apples' AS Product, 100 AS revenue, TIMESTAMP '2026-01-01 10:00:00' AS time UNION ALL
  SELECT 'Apples', 150, TIMESTAMP '2026-01-01 12:00:00' UNION ALL
  SELECT 'Apples', 200, TIMESTAMP '2026-01-02 10:00:00' UNION ALL
  SELECT 'Oranges', 50, TIMESTAMP '2026-01-01 10:00:00' UNION ALL
  SELECT 'Oranges', 60, TIMESTAMP '2026-01-02 10:00:00' UNION ALL
  SELECT 'Oranges', 70, TIMESTAMP '2026-01-02 12:00:00'
)
SELECT
  Product,
  AVG(daily_sales) AS avg_daily_sales
FROM
  (
    SELECT
      Product,
      SUM(revenue) AS daily_sales
    FROM Sales
    GROUP BY Product, DATE(time)
  )
GROUP BY Product
ORDER BY Product;

/*---------+-----------------+
 | Product | avg_daily_sales |
 +---------+-----------------+
 | Apples  |             225 |
 | Oranges |              90 |
 +---------+-----------------*/
```

*Multi-level aggregate* syntax removes this restriction by allowing you to add
an aggregate function as an argument to another aggregate function, when the
outer aggregate function has its own `GROUP BY` clause. Using multi-level
aggregation, the previous query can be simplified to the following:

```
WITH Sales AS (
  SELECT 'Apples' AS Product, 100 AS revenue, TIMESTAMP '2026-01-01 10:00:00' AS time UNION ALL
  SELECT 'Apples', 150, TIMESTAMP '2026-01-01 12:00:00' UNION ALL
  SELECT 'Apples', 200, TIMESTAMP '2026-01-02 10:00:00' UNION ALL
  SELECT 'Oranges', 50, TIMESTAMP '2026-01-01 10:00:00' UNION ALL
  SELECT 'Oranges', 60, TIMESTAMP '2026-01-02 10:00:00' UNION ALL
  SELECT 'Oranges', 70, TIMESTAMP '2026-01-02 12:00:00'
)
SELECT
  Product,
  AVG(SUM(revenue) GROUP BY DATE(time)) AS avg_daily_sales
FROM Sales
GROUP BY Product
ORDER BY Product;

/*---------+-----------------+
 | Product | avg_daily_sales |
 +---------+-----------------+
 | Apples  |             225 |
 | Oranges |              90 |
 +---------+-----------------*/
```

When an aggregate function has a `GROUP BY` clause, it becomes a multi-level
aggregate function. Multi-level aggregate functions work by first grouping the
input rows based the `GROUP BY` modifier on the aggregate function, and then
evaluating the inner aggregate function arguments over those groups. The
intermediate inner aggregation results are then passed to the enclosing
aggregate function.

In the previous example, the `SUM(revenue)` aggregation is effectively grouped
by both `Product` and `DATE(time)` to calculate an intermediate aggregation
result. This intermediate result is then averaged while grouping by `Product` to
get the final result per product.

### Multi-level aggregation rules and constraints

The following rules and constraints apply to multi-level aggregation:

* Multi-level aggregation is supported in only function arguments, the
  `DISTINCT` clause, and the `GROUP BY` modifier within the aggregate function
  call.
* You can't use the `HAVING MIN` or `HAVING MAX` clause in addition to a
  `GROUP BY` clause in a multi-level aggregation function.
* You also can't use the following clauses in a multi-aggregation function:

  + `ORDER BY`
  + `LIMIT`
  + `IGNORE NULLS` or `RESPECT NULLS`
* You can't use multi-level aggregate functions in the [`PIVOT`
  operator](/bigquery/docs/reference/standard-sql/query-syntax#pivot_operator).
* You can't use a `GROUPING` function within a multi-level aggregate body, or
  with `GROUP BY` modifiers. For example, the following expressions result in
  an error:

  ```
    SUM(GROUPING(...) GROUP BY Y)   -- Error
    GROUPING(... GROUP BY Y)        -- Error
  ```
* You can't use multi-level aggregation with the [differential privacy
  clause](/bigquery/docs/reference/standard-sql/query-syntax#dp_clause).
* You can't use multi-level aggregation with the [aggregation threshold
  clause](/bigquery/docs/reference/standard-sql/query-syntax#agg_threshold_clause).
* You can't use grouping keys with collation in a multi-level aggregation.
* You can't use multi-level aggregation with continuous queries.
* You can't use an empty aggregate function list in the inner aggregation of a
  multi-level aggregation (for example, `COUNT(* GROUP BY field1)`).
* You can't use more than two nested aggregate functions in a multi-level
  aggregation:

  ```
  SUM(AVG(MIN(X) GROUP BY Y) GROUP BY Z) -- Error; 3 nested aggregate functions.
  ```

### Avoid overcounting with multi-level aggregation

Aggregating over the result of a `JOIN` operation can result in *overcounting*
of the aggregated result. Consider the following query which attempts to
calculate the average salary of employees with at least one dependent child:

```
WITH Employees AS (
  SELECT 1 AS empno, 150000 AS salary UNION ALL
  SELECT 2, 100000 UNION ALL
  SELECT 3, 80000
),
Dependents AS (
  SELECT 1 AS empno, 'Child' AS relationship UNION ALL
  SELECT 2, 'Child' UNION ALL
  SELECT 2, 'Child' UNION ALL
  SELECT 3, 'Child' UNION ALL
  SELECT 3, 'Child'
)
SELECT
  empno,
  salary,
  relationship
FROM Employees
INNER JOIN Dependents
  USING (empno)
WHERE relationship = 'Child'
ORDER BY empno;

/*-------+--------+--------------+
 | empno | salary | relationship |
 +-------+--------+--------------+
 | 1     | 150000 | Child        |
 | 2     | 100000 | Child        |
 | 2     | 100000 | Child        |
 | 3     |  80000 | Child        |
 | 3     |  80000 | Child        |
 +-------+--------+--------------*/
```

The issue is that the `INNER JOIN` operation results in a table where the salary
for a given employee appears more than once if they have more than
one child listed in the `Dependents` table. For example, employees 2 and 3 are
repeated for each dependent child. Taking the average (`AVG`) of salary on this
table *overcounts* those two salaries, leading to an incorrect result.

Overcounting like in the previous example can be avoided with multi-level
aggregation. The following revised version of the previous query uses
multi-level aggregation with an `ANY_VALUE` function to get the correct average
without overcounting:

```
WITH Employees AS (
  SELECT 1 AS empno, 150000 AS salary UNION ALL
```