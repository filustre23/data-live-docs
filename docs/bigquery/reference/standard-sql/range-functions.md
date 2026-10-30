* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Range functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following range functions.

## Function list

| Name | Summary |
| --- | --- |
| [`APPENDS`](/bigquery/docs/reference/standard-sql/time-series-functions#appends) | Returns all rows appended to a table for a given time range.  For more information, see [Time series functions](/bigquery/docs/reference/standard-sql/time-series-functions). |
| [`CHANGES`](/bigquery/docs/reference/standard-sql/time-series-functions#changes) | Returns all rows that have changed in a table for a given time range.  For more information, see [Time series functions](/bigquery/docs/reference/standard-sql/time-series-functions). |
| [`GENERATE_RANGE_ARRAY`](/bigquery/docs/reference/standard-sql/range-functions#generate_range_array) | Splits a range into an array of subranges. |
| [`RANGE`](/bigquery/docs/reference/standard-sql/range-functions#range) | Constructs a range of `DATE`, `DATETIME`, or `TIMESTAMP` values. |
| [`RANGE_BUCKET`](/bigquery/docs/reference/standard-sql/mathematical_functions#range_bucket) | Scans through a sorted array and returns the 0-based position of a point's upper bound.  For more information, see [Mathematical functions](/bigquery/docs/reference/standard-sql/mathematical_functions). |
| [`RANGE_CONTAINS`](/bigquery/docs/reference/standard-sql/range-functions#range_contains) | Signature 1: Checks if one range is in another range.    Signature 2: Checks if a value is in a range. |
| [`RANGE_END`](/bigquery/docs/reference/standard-sql/range-functions#range_end) | Gets the upper bound of a range. |
| [`RANGE_INTERSECT`](/bigquery/docs/reference/standard-sql/range-functions#range_intersect) | Gets a segment of two ranges that intersect. |
| [`RANGE_OVERLAPS`](/bigquery/docs/reference/standard-sql/range-functions#range_overlaps) | Checks if two ranges overlap. |
| [`RANGE_SESSIONIZE`](/bigquery/docs/reference/standard-sql/range-functions#range_sessionize) | Produces a table of sessionized ranges. |
| [`RANGE_START`](/bigquery/docs/reference/standard-sql/range-functions#range_start) | Gets the lower bound of a range. |

## `GENERATE_RANGE_ARRAY`

```
GENERATE_RANGE_ARRAY(range_to_split, step_interval)
```

```
GENERATE_RANGE_ARRAY(range_to_split, step_interval, include_last_partial_range)
```

**Description**

Splits a range into an array of subranges.

**Definitions**

* `range_to_split`: The `RANGE<T>` value to split.
* `step_interval`: The `INTERVAL` value, which determines the maximum size of
  each subrange in the resulting array. An
  [interval single date and time part](/bigquery/docs/reference/standard-sql/data-types#single_datetime_part_interval)
  is supported, but an interval range of date and time parts isn't.

  + If `range_to_split` is `RANGE<DATE>`, these interval
    date parts are supported: `YEAR` to `DAY`.
  + If `range_to_split` is `RANGE<DATETIME>`, these interval
    date and time parts are supported: `YEAR` to `SECOND`.
  + If `range_to_split` is `RANGE<TIMESTAMP>`, these interval
    date and time parts are supported: `DAY` to `SECOND`.
* `include_last_partial_range`: A `BOOL` value, which determines whether or
  not to include the last subrange if it's a partial subrange.
  If this argument isn't specified, the default value is `TRUE`.

  + `TRUE` (default): The last subrange is included, even if it's
    smaller than `step_interval`.
  + `FALSE`: Exclude the last subrange if it's smaller than
    `step_interval`.

**Details**

Returns `NULL` if any input is`NULL`.

**Return type**

`ARRAY<RANGE<T>>`

**Examples**

In the following example, a date range between `2020-01-01` and `2020-01-06`
is split into an array of subranges that are one day long. There are
no partial ranges.

```
SELECT GENERATE_RANGE_ARRAY(
  RANGE(DATE '2020-01-01', DATE '2020-01-06'),
  INTERVAL 1 DAY) AS results;

/*----------------------------+
 | results                    |
 +----------------------------+
 | [                          |
 |  [2020-01-01, 2020-01-02), |
 |  [2020-01-02, 2020-01-03), |
 |  [2020-01-03, 2020-01-04), |
 |  [2020-01-04, 2020-01-05), |
 |  [2020-01-05, 2020-01-06), |
 | ]                          |
 +----------------------------*/
```

In the following examples, a date range between `2020-01-01` and `2020-01-06`
is split into an array of subranges that are two days long. The final subrange
is smaller than two days:

```
SELECT GENERATE_RANGE_ARRAY(
  RANGE(DATE '2020-01-01', DATE '2020-01-06'),
  INTERVAL 2 DAY) AS results;

/*----------------------------+
 | results                    |
 +----------------------------+
 | [                          |
 |  [2020-01-01, 2020-01-03), |
 |  [2020-01-03, 2020-01-05), |
 |  [2020-01-05, 2020-01-06)  |
 | ]                          |
 +----------------------------*/
```

```
SELECT GENERATE_RANGE_ARRAY(
  RANGE(DATE '2020-01-01', DATE '2020-01-06'),
  INTERVAL 2 DAY,
  TRUE) AS results;

/*----------------------------+
 | results                    |
 +----------------------------+
 | [                          |
 |  [2020-01-01, 2020-01-03), |
 |  [2020-01-03, 2020-01-05), |
 |  [2020-01-05, 2020-01-06)  |
 | ]                          |
 +----------------------------*/
```

In the following example, a date range between `2020-01-01` and `2020-01-06`
is split into an array of subranges that are two days long, but the final
subrange is excluded because it's smaller than two days:

```
SELECT GENERATE_RANGE_ARRAY(
  RANGE(DATE '2020-01-01', DATE '2020-01-06'),
  INTERVAL 2 DAY,
  FALSE) AS results;

/*----------------------------+
 | results                    |
 +----------------------------+
 | [                          |
 |  [2020-01-01, 2020-01-03), |
 |  [2020-01-03, 2020-01-05)  |
 | ]                          |
 +----------------------------*/
```

## `RANGE`

```
RANGE(lower_bound, upper_bound)
```

**Description**

Constructs a range of [`DATE`](/bigquery/docs/reference/standard-sql/data-types#date_type), [`DATETIME`](/bigquery/docs/reference/standard-sql/data-types#datetime_type), or
[`TIMESTAMP`](/bigquery/docs/reference/standard-sql/data-types#timestamp_type) values.

**Definitions**

* `lower_bound`: The range starts from this value. This can be a
  `DATE`, `DATETIME`, or `TIMESTAMP` value. If this value is `NULL`, the range
  doesn't include a lower bound.
* `upper_bound`: The range ends before this value. This can be a
  `DATE`, `DATETIME`, or `TIMESTAMP` value. If this value is `NULL`, the range
  doesn't include an upper bound.

**Details**

`lower_bound` and `upper_bound` must be of the same data type.

Produces an error if `lower_bound` is greater than or equal to `upper_bound`.
To return `NULL` instead, add the `SAFE.` prefix to the function name.

**Return type**

`RANGE<T>`, where `T` is the same data type as the input.

**Examples**

The following query constructs a date range:

```
SELECT RANGE(DATE '2022-12-01', DATE '2022-12-31') AS results;

/*--------------------------+
 | results                  |
 +--------------------------+
 | [2022-12-01, 2022-12-31) |
 +--------------------------*/
```

The following query constructs a datetime range:

```
SELECT RANGE(DATETIME '2022-10-01 14:53:27',
             DATETIME '2022-10-01 16:00:00') AS results;

/*---------------------------------------------+
 | results                                     |
 +---------------------------------------------+
 | [2022-10-01T14:53:27, 2022-10-01T16:00:00)  |
 +---------------------------------------------*/
```

The following query constructs a timestamp range:

```
SELECT RANGE(TIMESTAMP '2022-10-01 14:53:27 America/Los_Angeles',
             TIMESTAMP '2022-10-01 16:00:00 America/Los_Angeles') AS results;

-- Results depend upon where this query was executed.
/*------------------------------------------------------------------+
 | results                                                          |
 +------------------------------------------------------------------+
 | [2022-10-01 21:53:27.000000 UTC, 2022-10-01 23:00:00.000000 UTC) |
 +------------------------------------------------------------------*/
```

The following query constructs a date range with no lower bound:

```
SELECT RANGE(NULL, DATE '2022-12-31') AS results;

/*-------------------------+
 | results                 |
 +-------------------------+
 | [UNBOUNDED, 2022-12-31) |
 +-------------------------*/
```

The following query constructs a date range with no upper bound:

```
SELECT RANGE(DATE '2022-10-01', NULL) AS results;

/*--------------------------+
 | results                  |
 +--------------------------+
 | [2022-10-01, UNBOUNDED)  |
 +--------------------------*/
```

## `RANGE_CONTAINS`

* [Signature 1](#signature_1): Checks if every value in one range is
  in another range.
* [Signature 2](#signature_2): Checks if a value is in a range.

#### Signature 1

```
RANGE_CONTAINS(outer_range, inner_range)
```

**Description**

Checks if the inner range is in the outer range.

**Definitions**

* `outer_range`: The `RANGE<T>` value to search within.
* `inner_range`: The `RANGE<T>` value to search for in `outer_range`.

**Details**

Returns `TRUE` if `inner_range` exists in `outer_range`.
Otherwise, returns `FALSE`.

`T` must be of the same type for all inputs.

**Return type**

`BOOL`

**Examples**

In the following query, the inner range is in the outer range:

```
SELECT RANGE_CONTAINS(
  RANGE<DATE> '[2022-01-01, 2023-01-01)',
  RANGE<DATE> '[2022-04-01, 2022-07-01)') AS results;

/*---------+
 | results |
 +---------+
 | TRUE    |
 +---------*/
```

In the following query, the inner range isn't in the outer range:

```
SELECT RANGE_CONTAINS(
  RANGE<DATE> '[2022-01-01, 2023-01-01)',
  RANGE<DATE> '[2023-01-01, 2023-04-01)') AS results;

/*---------+
 | results |
 +---------+
 | FALSE   |
 +---------*/
```

#### Signature 2

```
RANGE_CONTAINS(range_to_search, value_to_find)
```

**Description**

Checks if a value is in a range.

**Definitions**

* `range_to_search`: The `RANGE<T>` value to search within.
* `value_to_find`: The value to search for in `range_to_search`.

**Details**

Returns `TRUE` if `value_to_find` exists in `range_to_search`.
Otherwise, returns `FALSE`.

The data type for `value_to_find` must be the same data type as `T`in
`range_to_search`.

**Return type**

`BOOL`

**Examples**

In the following query, the value `2022-04-01` is found in the range
`[2022-01-01, 2023-01-01)`:

```
SELECT RANGE_CONTAINS(
  RANGE<DATE> '[2022-01-01, 2023-01-01)',
  DATE '2022-04-01') AS results;

/*---------+
 | results |
 +---------+
 | TRUE    |
 +---------*/
```

In the following query, the value `2023-04-01` isn't found in the range
`[2022-01-01, 2023-01-01)`:

```
SELECT RANGE_CONTAINS(
  RANGE<DATE> '[2022-01-01, 2023-01-01)',
  DATE '2023-04-01') AS results;

/*---------+
 | results |
 +---------+
 | FALSE   |
 +---------*/
```

## `RANGE_END`

```
RANGE_END(range_to_check)
```

**Description**

Gets the upper bound of a range.

**Definitions**

* `range_to_check`: The `RANGE<T>` value.

**Details**

Returns `NULL` if the upper bound in `range_value` is `UNBOUNDED`.

Returns `NULL` if `range_to_check` is `NULL`.

**Return type**

`T` in `range_value`

**Examples**

In the following query, the upper bound of the range is retrieved:

```
SELECT RANGE_END(RANGE<DATE> '[2022-12-01, 2022-12-31)') AS results;

/*------------+
 | results    |
 +------------+
 | 2022-12-31 |
 +------------*/
```

In the following query, the upper bound of the