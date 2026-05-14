* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Approximate aggregate functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports approximate aggregate functions.
To learn about the syntax for aggregate function calls, see
[Aggregate function calls](/bigquery/docs/reference/standard-sql/aggregate-function-calls).

Approximate aggregate functions are scalable in terms of memory usage and time,
but produce approximate results instead of exact results. These functions
typically require less memory than [exact aggregation functions](/bigquery/docs/reference/standard-sql/aggregate_functions)
like `COUNT(DISTINCT ...)`, but also introduce statistical uncertainty.
This makes approximate aggregation appropriate for large data streams for
which linear memory usage is impractical, as well as for data that is
already approximate.

The approximate aggregate functions in this section work directly on the
input data, rather than an intermediate estimation of the data. These functions
*don't allow* users to specify the precision for the estimation with
sketches. If you would like to specify precision with sketches, see:

* [HyperLogLog++ functions](/bigquery/docs/reference/standard-sql/hll_functions) to estimate cardinality.
* [KLL functions](/bigquery/docs/reference/standard-sql/kll_functions) to estimate quantile values.

## Function list

| Name | Summary |
| --- | --- |
| [`APPROX_COUNT_DISTINCT`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_count_distinct) | Gets the approximate result for `COUNT(DISTINCT expression)`. |
| [`APPROX_QUANTILES`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_quantiles) | Gets the approximate quantile boundaries. |
| [`APPROX_TOP_COUNT`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_top_count) | Gets the approximate top elements and their approximate count. |
| [`APPROX_TOP_SUM`](/bigquery/docs/reference/standard-sql/approximate_aggregate_functions#approx_top_sum) | Gets the approximate top elements and sum, based on the approximate sum of an assigned weight. |

## `APPROX_COUNT_DISTINCT`

```
APPROX_COUNT_DISTINCT(
  expression
)
```

**Description**

Returns the approximate result for `COUNT(DISTINCT expression)`. The value
returned is a statistical estimate, not necessarily the actual value.

This function is less accurate than `COUNT(DISTINCT expression)`, but performs
better on huge input.

**Supported Argument Types**

Any data type **except**:

* `ARRAY`
* `STRUCT`
* `INTERVAL`

**Returned Data Types**

`INT64`

**Examples**

```
SELECT APPROX_COUNT_DISTINCT(x) as approx_distinct
FROM UNNEST([0, 1, 1, 2, 3, 5]) as x;

/*-----------------+
 | approx_distinct |
 +-----------------+
 | 5               |
 +-----------------*/
```

## `APPROX_QUANTILES`

```
APPROX_QUANTILES(
  [ DISTINCT ]
  expression, number
  [ { IGNORE | RESPECT } NULLS ]
)
```

**Description**

Returns the approximate boundaries for a group of `expression` values, where
`number` represents the number of quantiles to create. This function returns an
array of `number` + 1 elements, sorted in ascending order, where the
first element is the approximate minimum and the last element is the approximate
maximum.

Returns `NULL` if there are zero input rows or `expression` evaluates to
`NULL` for all rows.

To learn more about the optional aggregate clauses that you can pass
into this function, see
[Aggregate function calls](/bigquery/docs/reference/standard-sql/aggregate-function-calls).



**Supported Argument Types**

* `expression`: Any supported data type **except**:

  + `ARRAY`
  + `STRUCT`
  + `INTERVAL`
* `number`: `INT64` literal or query parameter.

**Returned Data Types**

`ARRAY<T>` where `T` is the type specified by `expression`.

**Examples**

```
SELECT APPROX_QUANTILES(x, 2) AS approx_quantiles
FROM UNNEST([1, 1, 1, 4, 5, 6, 7, 8, 9, 10]) AS x;

/*------------------+
 | approx_quantiles |
 +------------------+
 | [1, 5, 10]       |
 +------------------*/
```

```
SELECT APPROX_QUANTILES(x, 100)[OFFSET(90)] AS percentile_90
FROM UNNEST([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]) AS x;

/*---------------+
 | percentile_90 |
 +---------------+
 | 9             |
 +---------------*/
```

```
SELECT APPROX_QUANTILES(DISTINCT x, 2) AS approx_quantiles
FROM UNNEST([1, 1, 1, 4, 5, 6, 7, 8, 9, 10]) AS x;

/*------------------+
 | approx_quantiles |
 +------------------+
 | [1, 6, 10]       |
 +------------------*/
```

```
SELECT FORMAT("%T", APPROX_QUANTILES(x, 2 RESPECT NULLS)) AS approx_quantiles
FROM UNNEST([NULL, NULL, 1, 1, 1, 4, 5, 6, 7, 8, 9, 10]) AS x;

/*------------------+
 | approx_quantiles |
 +------------------+
 | [NULL, 4, 10]    |
 +------------------*/
```

```
SELECT FORMAT("%T", APPROX_QUANTILES(DISTINCT x, 2 RESPECT NULLS)) AS approx_quantiles
FROM UNNEST([NULL, NULL, 1, 1, 1, 4, 5, 6, 7, 8, 9, 10]) AS x;

/*------------------+
 | approx_quantiles |
 +------------------+
 | [NULL, 6, 10]    |
 +------------------*/
```

## `APPROX_TOP_COUNT`

```
APPROX_TOP_COUNT(
  expression, number
)
```

**Description**

Returns the approximate top elements of `expression` as an array of `STRUCT`s.
The `number` parameter specifies the number of elements returned.

Each `STRUCT` contains two fields. The first field (named `value`) contains an
input value. The second field (named `count`) contains an `INT64` specifying the
number of times the value was returned.

Returns `NULL` if there are zero input rows.

To learn more about the optional aggregate clauses that you can pass
into this function, see
[Aggregate function calls](/bigquery/docs/reference/standard-sql/aggregate-function-calls).



**Supported Argument Types**

* `expression`: Any data type that the `GROUP BY` clause supports.
* `number`: `INT64` literal or query parameter.

**Returned Data Types**

`ARRAY<STRUCT>`

**Examples**

```
SELECT APPROX_TOP_COUNT(x, 2) as approx_top_count
FROM UNNEST(["apple", "apple", "pear", "pear", "pear", "banana"]) as x;

/*-------------------------+
 | approx_top_count        |
 +-------------------------+
 | [{pear, 3}, {apple, 2}] |
 +-------------------------*/
```

**NULL handling**

`APPROX_TOP_COUNT` doesn't ignore `NULL`s in the input. For example:

```
SELECT APPROX_TOP_COUNT(x, 2) as approx_top_count
FROM UNNEST([NULL, "pear", "pear", "pear", "apple", NULL]) as x;

/*------------------------+
 | approx_top_count       |
 +------------------------+
 | [{pear, 3}, {NULL, 2}] |
 +------------------------*/
```

## `APPROX_TOP_SUM`

```
APPROX_TOP_SUM(
  expression, weight, number
)
```

**Description**

Returns the approximate top elements of `expression`, ordered by the sum of the
`weight` values provided for each unique value of `expression`. The `number`
parameter specifies the number of elements returned.

If the `weight` input is negative or `NaN`, this function returns an error.

The elements are returned as an array of `STRUCT`s.
Each `STRUCT` contains two fields: `value` and `sum`.
The `value` field contains the value of the input expression. The `sum` field is
the same type as `weight`, and is the approximate sum of the input weight
associated with the `value` field.

Returns `NULL` if there are zero input rows.

To learn more about the optional aggregate clauses that you can pass
into this function, see
[Aggregate function calls](/bigquery/docs/reference/standard-sql/aggregate-function-calls).



**Supported Argument Types**

* `expression`: Any data type that the `GROUP BY` clause supports.
* `weight`: One of the following:

  + `INT64`
  + `NUMERIC`
  + `BIGNUMERIC`
  + `FLOAT64`
* `number`: `INT64` literal or query parameter.

**Returned Data Types**

`ARRAY<STRUCT>`

**Examples**

```
SELECT APPROX_TOP_SUM(x, weight, 2) AS approx_top_sum FROM
UNNEST([
  STRUCT("apple" AS x, 3 AS weight),
  ("pear", 2),
  ("apple", 0),
  ("banana", 5),
  ("pear", 4)
]);

/*--------------------------+
 | approx_top_sum           |
 +--------------------------+
 | [{pear, 6}, {banana, 5}] |
 +--------------------------*/
```

**NULL handling**

`APPROX_TOP_SUM` doesn't ignore `NULL` values for the `expression` and `weight`
parameters.

```
SELECT APPROX_TOP_SUM(x, weight, 2) AS approx_top_sum FROM
UNNEST([STRUCT("apple" AS x, NULL AS weight), ("pear", 0), ("pear", NULL)]);

/*----------------------------+
 | approx_top_sum             |
 +----------------------------+
 | [{pear, 0}, {apple, NULL}] |
 +----------------------------*/
```

```
SELECT APPROX_TOP_SUM(x, weight, 2) AS approx_top_sum FROM
UNNEST([STRUCT("apple" AS x, 0 AS weight), (NULL, 2)]);

/*-------------------------+
 | approx_top_sum          |
 +-------------------------+
 | [{NULL, 2}, {apple, 0}] |
 +-------------------------*/
```

```
SELECT APPROX_TOP_SUM(x, weight, 2) AS approx_top_sum FROM
UNNEST([STRUCT("apple" AS x, 0 AS weight), (NULL, NULL)]);

/*----------------------------+
 | approx_top_sum             |
 +----------------------------+
 | [{apple, 0}, {NULL, NULL}] |
 +----------------------------*/
```




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-13 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-13 UTC."],[],[]]