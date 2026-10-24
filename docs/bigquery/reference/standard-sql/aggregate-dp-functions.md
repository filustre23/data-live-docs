* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Differentially private aggregate functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports differentially private aggregate functions.
For an explanation of how aggregate functions work, see
[Aggregate function calls](/bigquery/docs/reference/standard-sql/aggregate-function-calls).

You can only use differentially private aggregate functions with
[differentially private queries](/bigquery/docs/differential-privacy) in a
[differential privacy clause](/bigquery/docs/reference/standard-sql/query-syntax#dp_clause).

**Note:** In this topic, the privacy parameters in the examples aren't
recommendations. You should work with your privacy or security officer to
determine the optimal privacy parameters for your dataset and organization.

## Function list

| Name | Summary |
| --- | --- |
| [`AVG` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_avg) | `DIFFERENTIAL_PRIVACY`-supported `AVG`.   Gets the differentially-private average of non-`NULL`, non-`NaN` values in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`COUNT` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_count) | `DIFFERENTIAL_PRIVACY`-supported `COUNT`.   Signature 1: Gets the differentially-private count of rows in a query with a `DIFFERENTIAL_PRIVACY` clause.     Signature 2: Gets the differentially-private count of rows with a non-`NULL` expression in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`PERCENTILE_CONT` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_percentile_cont) | `DIFFERENTIAL_PRIVACY`-supported `PERCENTILE_CONT`.   Computes a differentially-private percentile across privacy unit columns in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`SUM` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_sum) | `DIFFERENTIAL_PRIVACY`-supported `SUM`.   Gets the differentially-private sum of non-`NULL`, non-`NaN` values in a query with a `DIFFERENTIAL_PRIVACY` clause. |

## `AVG` (`DIFFERENTIAL_PRIVACY`)

```
WITH DIFFERENTIAL_PRIVACY ...
  AVG(
    expression,
    [ contribution_bounds_per_group => (lower_bound, upper_bound) ]
  )
```

**Description**

Returns the average of non-`NULL`, non-`NaN` values in the expression.
This function first computes the average per privacy unit column, and then
computes the final result by averaging these averages.

You can't use an `AVG` (`DIFFERENTIAL_PRIVACY`) function with
[multi-level aggregation](/bigquery/docs/reference/standard-sql/aggregate-function-calls#multi_level_aggregation).

This function must be used with the [`DIFFERENTIAL_PRIVACY` clause](/bigquery/docs/reference/standard-sql/query-syntax#dp_clause)
and can support the following arguments:

* `expression`: The input expression. This can be any numeric input type,
  such as `INT64`.
* `contribution_bounds_per_group`: A named argument with a
  [contribution bound](#dp_clamped_named).
  Performs clamping for each group separately before performing intermediate
  grouping on the privacy unit column.

**Return type**

`FLOAT64`

**Examples**

The following differentially private query gets the average number of each item
requested per professor. Smaller aggregations might not be included. This query
references a table called [`professors`](/bigquery/docs/reference/standard-sql/query-syntax#dp_example_tables).

```
-- With noise, using the epsilon parameter.
SELECT
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=10, delta=.01, max_groups_contributed=1, privacy_unit_column=id)
    item,
    AVG(quantity, contribution_bounds_per_group => (0,100)) average_quantity
FROM professors
GROUP BY item;

-- These results will change each time you run the query.
-- Smaller aggregations might be removed.
/*----------+------------------+
 | item     | average_quantity |
 +----------+------------------+
 | pencil   | 38.5038356810269 |
 | pen      | 13.4725028762032 |
 +----------+------------------*/
```

```
-- Without noise, using the epsilon parameter.
-- (this un-noised version is for demonstration only)
SELECT
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=1e20, delta=.01, max_groups_contributed=1, privacy_unit_column=id)
    item,
    AVG(quantity) average_quantity
FROM professors
GROUP BY item;

-- These results will not change when you run the query.
/*----------+------------------+
 | item     | average_quantity |
 +----------+------------------+
 | scissors | 8                |
 | pencil   | 40               |
 | pen      | 18.5             |
 +----------+------------------*/
```

**Note:** For more information about when and when not to use
noise, see [Remove noise](/bigquery/docs/reference/standard-sql/query-syntax#eliminate_noise).

## `COUNT` (`DIFFERENTIAL_PRIVACY`)

* [Signature 1](#dp_count_signature1): Returns the number of rows in a
  differentially private `FROM` clause.
* [Signature 2](#dp_count_signature2): Returns the number of non-`NULL`
  values in an expression.

#### Signature 1

```
WITH DIFFERENTIAL_PRIVACY ...
  COUNT(
    *,
    [ contribution_bounds_per_group => (lower_bound, upper_bound) ]
  )
```

**Description**

Returns the number of rows in the
[differentially private](/bigquery/docs/reference/standard-sql/query-syntax#dp_clause) `FROM` clause. The final result
is an aggregation across a privacy unit column.

You can't use a `COUNT` (`DIFFERENTIAL_PRIVACY`) function with
[multi-level aggregation](/bigquery/docs/reference/standard-sql/aggregate-function-calls#multi_level_aggregation).

This function must be used with the [`DIFFERENTIAL_PRIVACY` clause](/bigquery/docs/reference/standard-sql/query-syntax#dp_clause)
and can support the following arguments:

* `contribution_bounds_per_group`: A named argument with a
  [contribution bound](#dp_clamped_named).
  Performs clamping for each group separately before performing intermediate
  grouping on the privacy unit column.

**Return type**

`INT64`

**Examples**

The following differentially private query counts the number of requests for
each item. This query references a table called
[`professors`](/bigquery/docs/reference/standard-sql/query-syntax#dp_example_tables).

```
-- With noise, using the epsilon parameter.
SELECT
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=10, delta=.01, max_groups_contributed=1, privacy_unit_column=id)
    item,
    COUNT(*, contribution_bounds_per_group=>(0, 100)) times_requested
FROM professors
GROUP BY item;

-- These results will change each time you run the query.
-- Smaller aggregations might be removed.
/*----------+-----------------+
 | item     | times_requested |
 +----------+-----------------+
 | pencil   | 5               |
 | pen      | 2               |
 +----------+-----------------*/
```

```
-- Without noise, using the epsilon parameter.
-- (this un-noised version is for demonstration only)
SELECT
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=1e20, delta=.01, max_groups_contributed=1, privacy_unit_column=id)
    item,
    COUNT(*, contribution_bounds_per_group=>(0, 100)) times_requested
FROM professors
GROUP BY item;

-- These results will not change when you run the query.
/*----------+-----------------+
 | item     | times_requested |
 +----------+-----------------+
 | scissors | 1               |
 | pencil   | 4               |
 | pen      | 3               |
 +----------+-----------------*/
```

**Note:** For more information about when and when not to use
noise, see [Remove noise](/bigquery/docs/reference/standard-sql/query-syntax#eliminate_noise).

#### Signature 2

```
WITH DIFFERENTIAL_PRIVACY ...
  COUNT(
    expression,
    [ contribution_bounds_per_group => (lower_bound, upper_bound) ]
  )
```

**Description**

Returns the number of non-`NULL` expression values. The final result is an
aggregation across a privacy unit column.

This function must be used with the [`DIFFERENTIAL_PRIVACY` clause](/bigquery/docs/reference/standard-sql/query-syntax#dp_clause)
and can support these arguments:

* `expression`: The input expression. This expression can be any
  numeric input type, such as `INT64`.
* `contribution_bounds_per_group`: A named argument with a
  [contribution bound](#dp_clamped_named).
  Performs clamping per each group separately before performing intermediate
  grouping on the privacy unit column.

**Return type**

`INT64`

**Examples**

The following differentially private query counts the number of requests made
for each type of item. This query references a table called
[`professors`](/bigquery/docs/reference/standard-sql/query-syntax#dp_example_tables).

```
-- With noise, using the epsilon parameter.
SELECT
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=10, delta=.01, max_groups_contributed=1, privacy_unit_column=id)
    item,
    COUNT(item, contribution_bounds_per_group => (0,100)) times_requested
FROM professors
GROUP BY item;

-- These results will change each time you run the query.
-- Smaller aggregations might be removed.
/*----------+-----------------+
 | item     | times_requested |
 +----------+-----------------+
 | pencil   | 5               |
 | pen      | 2               |
 +----------+-----------------*/
```

```
-- Without noise, using the epsilon parameter.
-- (this un-noised version is for demonstration only)
SELECT
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=1e20, delta=.01, max_groups_contributed=1, privacy_unit_column=id)
    item,
    COUNT(item, contribution_bounds_per_group => (0,100)) times_requested
FROM professors
GROUP BY item;

-- These results will not change when you run the query.
/*----------+-----------------+
 | item     | times_requested |
 +----------+-----------------+
 | scissors | 1               |
 | pencil   | 4               |
 | pen      | 3               |
 +----------+-----------------*/
```

**Note:** For more information about when and when not to use
noise, see [Remove noise](/bigquery/docs/reference/standard-sql/query-syntax#eliminate_noise).

## `PERCENTILE_CONT` (`DIFFERENTIAL_PRIVACY`)

```
WITH DIFFERENTIAL_PRIVACY ...
  PERCENTILE_CONT(
    expression,
    percentile,
    contribution_bounds_per_row => (lower_bound, upper_bound)
  )
```

**Description**

Takes an expression and computes a percentile for it. The final result is an
aggregation across privacy unit columns.

You can't use a `PERCENTILE_CONT` (`DIFFERENTIAL_PRIVACY`) function with
[multi-level aggregation](/bigquery/docs/reference/standard-sql/aggregate-function-calls#multi_level_aggregation).

This function must be used with the [`DIFFERENTIAL_PRIVACY` clause](/bigquery/docs/reference/standard-sql/query-syntax#dp_clause)
and can support these arguments:

* `expression`: The input expression. This can be most numeric input types,
  such as `INT64`. `NULL` values are always ignored.
* `percentile`: The percentile to compute. The percentile must be a literal in
  the range `[0, 1]`.
* `contribution_bounds_per_row`: A named argument with a
  [contribution bounds](#dp_clamped_named).
  Performs clamping for each row separately before performing intermediate
  grouping on the privacy unit column.

`NUMERIC` and `BIGNUMERIC` arguments aren't allowed.
If you need them, cast them as the
`FLOAT64` data type first.

**Return type**

`FLOAT64`

**Examples**

The following differentially private query gets the percentile of items
requested. Smaller aggregations might not be included. This query references a
view called [`professors`](/bigquery/docs/reference/standard-sql/query-syntax#dp_example_tables).

```
-- With noise, using the epsilon parameter.
SELECT
  WITH DIFFERENTIAL_PRIVACY
    OPTIONS(epsilon=10, delta=.01, max_groups_contributed=1, privacy_unit_column=id)
    it
```