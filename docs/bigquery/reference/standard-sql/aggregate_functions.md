* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Aggregate functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following general aggregate functions.
To learn about the syntax for aggregate function calls, see
[Aggregate function calls](/bigquery/docs/reference/standard-sql/aggregate-function-calls).

## Function list

| Name | Summary |
| --- | --- |
| [`AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#agg) | Aggregates a measure type. |
| [`ANY_VALUE`](/bigquery/docs/reference/standard-sql/aggregate_functions#any_value) | Gets an expression for some row. |
| [`APPROX_COUNT_DISTINCT`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_count_distinct) | Gets the approximate result for `COUNT(DISTINCT expression)`.  For more information, see [Approximate aggregate functions](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions). |
| [`APPROX_QUANTILES`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_quantiles) | Gets the approximate quantile boundaries.  For more information, see [Approximate aggregate functions](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions). |
| [`APPROX_TOP_COUNT`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_top_count) | Gets the approximate top elements and their approximate count.  For more information, see [Approximate aggregate functions](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions). |
| [`APPROX_TOP_SUM`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_top_sum) | Gets the approximate top elements and sum, based on the approximate sum of an assigned weight.  For more information, see [Approximate aggregate functions](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions). |
| [`ARRAY_AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#array_agg) | Gets an array of values. |
| [`ARRAY_CONCAT_AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#array_concat_agg) | Concatenates arrays and returns a single array as a result. |
| [`AVG`](/bigquery/docs/reference/standard-sql/aggregate_functions#avg) | Gets the average of non-`NULL` values. |
| [`AVG` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_avg) | `DIFFERENTIAL_PRIVACY`-supported `AVG`.   Gets the differentially-private average of non-`NULL`, non-`NaN` values in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`BIT_AND`](/bigquery/docs/reference/standard-sql/aggregate_functions#bit_and) | Performs a bitwise AND operation on an expression. |
| [`BIT_OR`](/bigquery/docs/reference/standard-sql/aggregate_functions#bit_or) | Performs a bitwise OR operation on an expression. |
| [`BIT_XOR`](/bigquery/docs/reference/standard-sql/aggregate_functions#bit_xor) | Performs a bitwise XOR operation on an expression. |
| [`CORR`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#corr) | Computes the Pearson coefficient of correlation of a set of number pairs.  For more information, see [Statistical aggregate functions](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions). |
| [`COUNT`](/bigquery/docs/reference/standard-sql/aggregate_functions#count) | Gets the number of rows in the input, or the number of rows with an expression evaluated to any value other than `NULL`. |
| [`COUNT` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_count) | `DIFFERENTIAL_PRIVACY`-supported `COUNT`.   Signature 1: Gets the differentially-private count of rows in a query with a `DIFFERENTIAL_PRIVACY` clause.     Signature 2: Gets the differentially-private count of rows with a non-`NULL` expression in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`COUNTIF`](/bigquery/docs/reference/standard-sql/aggregate_functions#countif) | Gets the number of `TRUE` values for an expression. |
| [`COVAR_POP`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#covar_pop) | Computes the population covariance of a set of number pairs.  For more information, see [Statistical aggregate functions](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions). |
| [`COVAR_SAMP`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#covar_samp) | Computes the sample covariance of a set of number pairs.  For more information, see [Statistical aggregate functions](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions). |
| [`GROUPING`](/bigquery/docs/reference/standard-sql/aggregate_functions#grouping) | Checks if a groupable value in the `GROUP BY` clause is aggregated. |
| [`LOGICAL_AND`](/bigquery/docs/reference/standard-sql/aggregate_functions#logical_and) | Gets the logical AND of all non-`NULL` expressions. |
| [`LOGICAL_OR`](/bigquery/docs/reference/standard-sql/aggregate_functions#logical_or) | Gets the logical OR of all non-`NULL` expressions. |
| [`MAX`](/bigquery/docs/reference/standard-sql/aggregate_functions#max) | Gets the maximum non-`NULL` value. |
| [`MAX_BY`](/bigquery/docs/reference/standard-sql/aggregate_functions#max_by) | Synonym for `ANY_VALUE(x HAVING MAX y)`. |
| [`MIN`](/bigquery/docs/reference/standard-sql/aggregate_functions#min) | Gets the minimum non-`NULL` value. |
| [`MIN_BY`](/bigquery/docs/reference/standard-sql/aggregate_functions#min_by) | Synonym for `ANY_VALUE(x HAVING MIN y)`. |
| [`PERCENTILE_CONT`](/bigquery/docs/reference/standard-sql/navigation_functions#percentile_cont) | Computes the specified percentile for a value, using linear interpolation.  For more information, see [Navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions). |
| [`PERCENTILE_CONT` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_percentile_cont) | `DIFFERENTIAL_PRIVACY`-supported `PERCENTILE_CONT`.   Computes a differentially-private percentile across privacy unit columns in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`PERCENTILE_DISC`](/bigquery/docs/reference/standard-sql/navigation_functions#percentile_disc) | Computes the specified percentile for a discrete value.  For more information, see [Navigation functions](/bigquery/docs/reference/standard-sql/navigation_functions). |
| [`ST_CENTROID_AGG`](/bigquery/docs/reference/standard-sql/geography_functions#st_centroid_agg) | Gets the centroid of a set of `GEOGRAPHY` values.  For more information, see [Geography functions](/bigquery/docs/reference/standard-sql/geography_functions). |
| [`ST_EXTENT`](/bigquery/docs/reference/standard-sql/geography_functions#st_extent) | Gets the bounding box for a group of `GEOGRAPHY` values.  For more information, see [Geography functions](/bigquery/docs/reference/standard-sql/geography_functions). |
| [`ST_UNION_AGG`](/bigquery/docs/reference/standard-sql/geography_functions#st_union_agg) | Aggregates over `GEOGRAPHY` values and gets their point set union.  For more information, see [Geography functions](/bigquery/docs/reference/standard-sql/geography_functions). |
| [`STDDEV`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#stddev) | An alias of the `STDDEV_SAMP` function.  For more information, see [Statistical aggregate functions](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions). |
| [`STDDEV_POP`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#stddev_pop) | Computes the population (biased) standard deviation of the values.  For more information, see [Statistical aggregate functions](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions). |
| [`STDDEV_SAMP`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#stddev_samp) | Computes the sample (unbiased) standard deviation of the values.  For more information, see [Statistical aggregate functions](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions). |
| [`STRING_AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#string_agg) | Concatenates non-`NULL` `STRING` or `BYTES` values. |
| [`SUM`](/bigquery/docs/reference/standard-sql/aggregate_functions#sum) | Gets the sum of non-`NULL` values. |
| [`SUM` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_sum) | `DIFFERENTIAL_PRIVACY`-supported `SUM`.   Gets the differentially-private sum of non-`NULL`, non-`NaN` values in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`VAR_POP`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#var_pop) | Computes the population (biased) variance of the values.  For more information, see [Statistical aggregate functions](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions). |
| [`VAR_SAMP`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#var_samp) | Computes the sample (unbiased) variance of the values.  For more information, see [Statistical aggregate functions](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions). |
| [`VARIANCE`](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions#variance) | An alias of `VAR_SAMP`.  For more information, see [Statistical aggregate functions](/bigquery/docs/reference/standard-sql/statistical_aggregate_functions). |

## `AGG`

**Preview**

This product or feature is subject to the "Pre-GA Offerings Terms"
in the General Service Terms section of the
[Service Specific Terms](https://cloud.google.com/terms/service-terms).
Pre-GA products and features are available "as is" and might have
limited support. For more information, see the
[launch stage descriptions](https://cloud.google.com/products#product-launch-stages).

**Note:** To provide feedback or request support for this feature, send an email to
[bq-graph-preview-support@google.com](mailto:bq-graph-preview-support@google.com).

```
AGG(measure_expression)
```

**Description**

Aggregates a [measure type](/bigquery/docs/reference/standard-sql/data-types#measure_type). A measure type encapsulates an
aggregate calculation to perform, locked to a specific granularity defined by
a key. The `AGG` function invokes the calculation exactly once per key
with the guarantee of avoiding overcounting. Measures are useful for defining
business metrics. You can perform aggregation using the `AGG`
function instead of complex aggregation queries.

For more information and examples of using the `AGG` function
with measures, see [work with measures](/bigquery/docs/graph-measures).

**Supported Argument Types**

A single `MEASURE` type

**Returned Data Types**

The type returned by the expression associated with the measure.

**Examples**

The following example creates a graph called `StoreGraph` based on the
`Stores` and `Locations` tables. The node table defined by location data has
a measure property called `total_population`. The measure is defined by the
aggregate calculation `SUM(population)` and the key `id`.

```
CREATE OR REPLACE TABLE mydataset.Stores (
  name STRING PRIMARY KEY NOT ENFORCED,
  location_id INT64 REFERENCES mydataset.Locations(id) NOT ENFORCED
) AS (
  SELECT 'Store 1' AS name, 101 AS location_id
  UNION ALL
  SELECT 'Store 2' AS name, 101 AS location_id
);

CREATE OR REPLACE TABLE mydataset.Locations (
  id INT64 PRIMARY KEY NOT ENFORCED,
  name STRING,
  population INT64
) AS (
  SELECT 101 AS id, 'Anytown' AS name, 1000 AS population
);

CREATE OR REPLACE PROPERTY GRAPH mydataset.StoreGraph
  NODE TABLES (
    mydataset.Stores AS S,
    mydataset.Locations AS L
    PROPERTIES(id, name, population, MEASURE(SUM(population)) AS total_population)
  )
  EDGE TABLES (
    mydataset.Stores AS SL
    SOURCE KEY (location_id) REFERENCES L (id)
    DESTINATION KEY (name) REFERENCES S (name)
  );
```

To access measures defined on a graph, you must call the
[`GRAPH_EXPAND` TVF](/bigquery/docs/reference/standard-sql/graph-sql-queries#graph_expand), which performs a series of `LEFT JOIN`
operations on your graph's input tables to produce a flattened version of
the graph.

The following query calls the `GRAPH_EXPAND` function and omits the
`L_total_population` column from the output because
you can't directly select a column for a property defined by a measure without
using the `AGG` function:

```
SELECT * EXCEPT(L_total_population)
FROM GRAPH_EXPAND('mydataset.StoreGraph');

/*---------------+---------+------+---------+--------------+
 | S_location_id | S_name  | L_id | L_name  | L_population |
 +---------------+---------+------+---------+--------------+
 | 101           | Store 2 | 101  | Anytown | 1000         |
 | 101           | Store 1 | 101  | Anytown | 1000         |
 +---------------+---------+------+---------+--------------*/
```

The following query shows the difference between aggregating a measure and
a regular value. When you apply the `AGG` function to the `L_total_population`
measure, the population of a location is counted exactly once per distinct
`location_id` value.
If you call the `SUM` function on `L_population`, then the `L_population`
column contributes the population for every row in the table with a given
location ID.

```
SELECT
  S_location_id,
  AGG(L_total_population) AS true_total_population,
  SUM(L_population) AS overcounted_population
FROM GRAPH_EXPAND('mydataset.StoreGraph')
GROUP BY S_location_id;

/*---------------+-----------------------+------------------------+
 | S_location_id | true_total_population | overcounted_population |
 +---------------+-----------------------+------------------------+
 | 101           | 1000                  | 2000                   |
 +---------------+-----------------------+------------------------*/
```

## `ANY_VALUE`

```
ANY_VALUE(
  expression
  [ HAVING { MAX | MIN } having_expression ]
)
[ OVER over_clause ]

over_clause:
  { named_window | ( [ window_specification ] ) }

window_specification:
  [ named_window ]
  [ PARTITION BY partition_expression [, ...] ]
  [ ORDER BY expression [ { ASC | DESC }  ] [, ...] ]
  [ window_frame_clause ]
```

**Description**

Returns `expression` for some row chosen from the group. Which row is chosen is
nondeterministic, not random. Returns `NULL` when the input produces no
rows. Returns `NULL` when `expression`
or `having_expression` is
`NULL` for all rows in the group.

If `expression` contains any non-NULL values, then `ANY_VALUE` behaves as if
`IGNORE NULLS` is specified;
rows for which `expression` is `NULL` aren't considered and won't be
selected.

If the `HAVING` clause is included in the `ANY_VALUE` function, the
`OVER` clause can't be used with this function.

To learn more about the optional aggregate clauses that you can pass
into this function, see
[Aggregate function calls](/bigquery/docs/reference/standard-sql/aggregate-function-calls).



To learn more about the `OVER` clause and how to use it, see
[Window function calls](/bigquery/docs/reference/standard-sql/window-function-calls).



**Supported Argument Types**

Any

**Returned Data Types**

Matches the input data type.

**Examples**

```
SELECT ANY_VALUE(fruit) as any_value
FROM UNNEST(["apple", "banana", "pear"]) as fruit;

/*-----------+
 | any_value |
 +-----------+
 | apple     |
 +-----------*/
```

```
SELECT
  fruit,
  ANY_VALUE(fruit) OVER (ORDER BY LENGTH(fruit) ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) AS any_value
FROM UNNEST(["apple", "banana", "pear"]) as fruit;

/*--------+-----------+
 | fruit  | any_value |
 +--------+-----------+
 | pear   | pear      |
 | apple  | pear      |
 | banana | apple     |
 +--------+-----------*/
```

```
WITH
  Store AS (
    SELECT 20 AS sold, "apples" AS fruit
    UNION ALL
    SELECT 30 AS sold, "pears" AS fruit
    UNION ALL
    SELECT 30 AS sold, "bananas" AS fruit
    UNION ALL
    SELECT 10 AS sold, "oranges" AS fruit
  )
SELECT ANY_VALUE(fruit HAVING MAX sold) AS a_highest_selling_fruit FROM Store;

/*-------------------------+
 | a_highest_selling_fruit |
 +-------------------------+
 | pears                   |
 +-------------------------*/
```

```
WITH
  Store AS (
    SELECT 20 AS sold, "apples" AS fruit
    UNION ALL
    SELECT 30 AS sold, "pears" AS fruit
    UNION ALL
    SELECT 30 AS sold, "bananas" AS fruit
    UNION ALL
    SELECT 10 AS sold, "oranges" AS fruit
  )
SELECT ANY_VALUE(fruit HAVING MIN sold) AS a_lowest_selling_fruit FROM Store;

/*-------------------------+
 | a_lowest_selling_fruit  |
 +-------------------------+
 | oranges                 |
 +-------------------------*/
```

## `ARRAY_AGG`

```
ARRAY_AGG(
  [ DISTINCT ]
  expression
  [ { IGNORE | RESPECT } NULLS ]
  [ ORDER BY key [ { ASC | DESC } ] [, ... ] ]
  [ LIMIT n ]
)
[ OVER over_clause ]

over_clause:
  { named_window | ( [ window_specification ] ) }

window_specification:
  [ named_window ]
  [ PARTITION BY partition_expression [, ...] ]
  [ ORDER BY expression [ { ASC | DESC }  ] [, ...] ]
  [ window_frame_clause ]
```

**Description**

Returns an ARRAY of `expression` values.

To learn more about the optional aggregate clauses that you can pass
into this function, see
[Aggregate function calls](/bigquery/docs/reference/standard-sql/aggregate-function-calls).



If this function is used with the `OVER` clause, it's part of a
window function call. In a window function call,
aggregate function clauses can't be used.
To learn more about the `OVER` clause and how to use it, see
[Window function calls](/bigquery/docs/reference/standard-sql/window-function-calls).



An error is raised if an array in the final query result contains a `NULL`
element.

**Supported Argument Types**

All data types except ARRAY.

**Returned Data Types**

ARRAY

If there are zero input rows, this function returns `NULL`.

**Examples**

```
SELECT ARRAY_AGG(x) AS array_agg FROM UNNEST([2, 1,-2, 3, -2, 1, 2]) AS x;

/*-------------------------+
 | array_agg               |
 +-------------------------+
 | [2, 1, -2, 3, -2, 1, 2] |
 +-------------------------*/
```

```
SELECT ARRAY_AGG(DISTINCT x) AS array_agg
FROM UNNEST([2, 1, -2, 3, -2, 1, 2]) AS x;

/*---------------+
 | array_agg     |
 +---------------+
 | [2, 1, -2, 3] |
 +---------------*/
```

```
SELECT ARRAY_AGG(x IGNORE NULLS) AS array_agg
FROM
```