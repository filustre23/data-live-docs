* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Array functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following array functions.

## Function list

| Name | Summary |
| --- | --- |
| [`ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#array) | Produces an array with one element for each row in a subquery. |
| [`ARRAY_AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#array_agg) | Gets an array of values.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |
| [`ARRAY_CONCAT`](/bigquery/docs/reference/standard-sql/array_functions#array_concat) | Concatenates one or more arrays with the same element type into a single array. |
| [`ARRAY_CONCAT_AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#array_concat_agg) | Concatenates arrays and returns a single array as a result.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |
| [`ARRAY_FIRST`](/bigquery/docs/reference/standard-sql/array_functions#array_first) | Gets the first element in an array. |
| [`ARRAY_LAST`](/bigquery/docs/reference/standard-sql/array_functions#array_last) | Gets the last element in an array. |
| [`ARRAY_LENGTH`](/bigquery/docs/reference/standard-sql/array_functions#array_length) | Gets the number of elements in an array. |
| [`ARRAY_REVERSE`](/bigquery/docs/reference/standard-sql/array_functions#array_reverse) | Reverses the order of elements in an array. |
| [`ARRAY_SLICE`](/bigquery/docs/reference/standard-sql/array_functions#array_slice) | Produces an array containing zero or more consecutive elements from an input array. |
| [`ARRAY_TO_STRING`](/bigquery/docs/reference/standard-sql/array_functions#array_to_string) | Produces a concatenation of the elements in an array as a `STRING` value. |
| [`GENERATE_ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#generate_array) | Generates an array of values in a range. |
| [`GENERATE_DATE_ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#generate_date_array) | Generates an array of dates in a range. |
| [`GENERATE_RANGE_ARRAY`](/bigquery/docs/reference/standard-sql/range-functions#generate_range_array) | Splits a range into an array of subranges.  For more information, see [Range functions](/bigquery/docs/reference/standard-sql/range-functions). |
| [`GENERATE_TIMESTAMP_ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#generate_timestamp_array) | Generates an array of timestamps in a range. |
| [`JSON_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_array) | Creates a JSON array.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`JSON_ARRAY_APPEND`](/bigquery/docs/reference/standard-sql/json_functions#json_array_append) | Appends JSON data to the end of a JSON array.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`JSON_ARRAY_INSERT`](/bigquery/docs/reference/standard-sql/json_functions#json_array_insert) | Inserts JSON data into a JSON array.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`JSON_EXTRACT_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_extract_array) | (Deprecated) Extracts a JSON array and converts it to a SQL `ARRAY<JSON-formatted STRING>` or `ARRAY<JSON>` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`JSON_EXTRACT_STRING_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_extract_string_array) | (Deprecated) Extracts a JSON array of scalar values and converts it to a SQL `ARRAY<STRING>` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`JSON_QUERY_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_query_array) | Extracts a JSON array and converts it to a SQL `ARRAY<JSON-formatted STRING>` or `ARRAY<JSON>` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`JSON_VALUE_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_value_array) | Extracts a JSON array of scalar values and converts it to a SQL `ARRAY<STRING>` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`RANGE_BUCKET`](/bigquery/docs/reference/standard-sql/mathematical_functions#range_bucket) | Scans through a sorted array and returns the 0-based position of a point's upper bound.  For more information, see [Mathematical functions](/bigquery/docs/reference/standard-sql/mathematical_functions). |

## `ARRAY`

```
ARRAY(subquery)
```

**Description**

The `ARRAY` function returns an `ARRAY` with one element for each row in a
[subquery](/bigquery/docs/reference/standard-sql/subqueries).

If `subquery` produces a
SQL table,
the table must have exactly one column. Each element in the output `ARRAY` is
the value of the single column of a row in the table.

If `subquery` produces a
value table,
then each element in the output `ARRAY` is the entire corresponding row of the
value table.

**Constraints**

* Subqueries are unordered, so the elements of the output `ARRAY` aren't
  guaranteed to preserve any order in the source table for the subquery. However,
  if the subquery includes an `ORDER BY` clause, the `ARRAY` function will return
  an `ARRAY` that honors that clause.
* If the subquery returns more than one column, the `ARRAY` function returns an
  error.
* If the subquery returns an `ARRAY` typed column or `ARRAY` typed rows, the
  `ARRAY` function returns an error that GoogleSQL doesn't support
  `ARRAY`s with elements of type
  [`ARRAY`](/bigquery/docs/reference/standard-sql/data-types#array_type).
* If the subquery returns zero rows, the `ARRAY` function returns an empty
  `ARRAY`. It never returns a `NULL` `ARRAY`.

**Return type**

`ARRAY`

**Examples**

```
SELECT ARRAY
  (SELECT 1 UNION ALL
   SELECT 2 UNION ALL
   SELECT 3) AS new_array;

/*-----------+
 | new_array |
 +-----------+
 | [1, 2, 3] |
 +-----------*/
```

To construct an `ARRAY` from a subquery that contains multiple
columns, change the subquery to use `SELECT AS STRUCT`. Now
the `ARRAY` function will return an `ARRAY` of `STRUCT`s. The `ARRAY` will
contain one `STRUCT` for each row in the subquery, and each of these `STRUCT`s
will contain a field for each column in that row.

```
SELECT
  ARRAY
    (SELECT AS STRUCT 1, 2, 3
     UNION ALL SELECT AS STRUCT 4, 5, 6) AS new_array;

/*------------------------+
 | new_array              |
 +------------------------+
 | [{1, 2, 3}, {4, 5, 6}] |
 +------------------------*/
```

Similarly, to construct an `ARRAY` from a subquery that contains
one or more `ARRAY`s, change the subquery to use `SELECT AS STRUCT`.

```
SELECT ARRAY
  (SELECT AS STRUCT [1, 2, 3] UNION ALL
   SELECT AS STRUCT [4, 5, 6]) AS new_array;

/*----------------------------+
 | new_array                  |
 +----------------------------+
 | [{[1, 2, 3]}, {[4, 5, 6]}] |
 +----------------------------*/
```

## `ARRAY_CONCAT`

```
ARRAY_CONCAT(array_expression[, ...])
```

**Description**

Concatenates one or more arrays with the same element type into a single array.

The function returns `NULL` if any input argument is `NULL`.

**Note:** You can also use the [|| concatenation operator](/bigquery/docs/reference/standard-sql/operators)
to concatenate arrays.

**Return type**

`ARRAY`

**Examples**

```
SELECT ARRAY_CONCAT([1, 2], [3, 4], [5, 6]) as count_to_six;

/*--------------------------------------------------+
 | count_to_six                                     |
 +--------------------------------------------------+
 | [1, 2, 3, 4, 5, 6]                               |
 +--------------------------------------------------*/
```

## `ARRAY_FIRST`

```
ARRAY_FIRST(array_expression)
```

**Description**

Takes an array and returns the first element in the array.

Produces an error if the array is empty.

Returns `NULL` if `array_expression` is `NULL`.

**Note:** To get the last element in an array, see [`ARRAY_LAST`](#array_last).

**Return type**

Matches the data type of elements in `array_expression`.

**Example**

```
SELECT ARRAY_FIRST(['a','b','c','d']) as first_element

/*---------------+
 | first_element |
 +---------------+
 | a             |
 +---------------*/
```

## `ARRAY_LAST`

```
ARRAY_LAST(array_expression)
```

**Description**

Takes an array and returns the last element in the array.

Produces an error if the array is empty.

Returns `NULL` if `array_expression` is `NULL`.

**Note:** To get the first element in an array, see [`ARRAY_FIRST`](#array_first).

**Return type**

Matches the data type of elements in `array_expression`.

**Example**

```
SELECT ARRAY_LAST(['a','b','c','d']) as last_element

/*---------------+
 | last_element  |
 +---------------+
 | d             |
 +---------------*/
```

## `ARRAY_LENGTH`

```
ARRAY_LENGTH(array_expression)
```

**Description**

Returns the size of the array. Returns 0 for an empty array. Returns `NULL` if
the `array_expression` is `NULL`.

**Return type**

`INT64`

**Examples**

```
SELECT
  ARRAY_LENGTH(["coffee", NULL, "milk" ]) AS size_a,
  ARRAY_LENGTH(["cake", "pie"]) AS size_b;

/*--------+--------+
 | size_a | size_b |
 +--------+--------+
 | 3      | 2      |
 +--------+--------*/
```

## `ARRAY_REVERSE`

```
ARRAY_REVERSE(value)
```

**Description**

Returns the input `ARRAY` with elements in reverse order.

**Return type**

`ARRAY`

**Examples**

```
SELECT ARRAY_REVERSE([1, 2, 3]) AS reverse_arr

/*-------------+
 | reverse_arr |
 +-------------+
 | [3, 2, 1]   |
 +-------------*/
```

## `ARRAY_SLICE`

```
ARRAY_SLICE(array_to_slice, start_offset, end_offset)
```

**Description**

Returns an array containing zero or more consecutive elements from the
input array.

* `array_to_slice`: The array that contains the elements you want to slice.
* `start_offset`: The inclusive starting offset.
* `end_offset`: The inclusive ending offset.

An offset can be positive or negative. A positive offset starts from the
beginning of the input array and is 0-based. A negative offset starts from
the end of the input array. Out-of-bounds offsets are supported. Here are some
examples:

| Input offset | Final offset in array | Notes |
| --- | --- | --- |
| 0 | [**'a'**, 'b', 'c', 'd'] | The final offset is `0`. |
| 3 | ['a', 'b', 'c', **'d'**] | The final offset is `3`. |
| 5 | ['a', 'b', 'c', **'d'**] | Because the input offset is out of bounds, the final offset is `3` (`array length - 1`). |
| -1 | ['a', 'b', 'c', **'d'**] | Because a negative offset is used, the offset starts at the end of the array. The final offset is `3` (`array length - 1`). |
| -2 | ['a', 'b', **'c'**, 'd'] | Because a negative offset is used, the offset starts at the end of the array. The final offset is `2` (`array length - 2`). |
| -4 | [**'a'**, 'b', 'c', 'd'] | Because a negative offset is used, the offset starts at the end of the array. The final offset is `0` (`array length - 4`). |
| -5 | [**'a'**, 'b', 'c', 'd'] | Because the offset is negative and out of bounds, the final offset is `0` (`array length - array length`). |

Additional details:

* The input array can contain `NULL` elements. `NULL` elements are included
  in the resulting array.
* Returns `NULL` if `array_to_slice`, `start_offset`, or `end_offset` is
  `NULL`.
* Returns an empty array if `array_to_slice` is empty.
* Returns an empty array if the position of the `start_offset` in the array is
  after the position of the `end_offset`.

**Return type**

`ARRAY`

**Examples**

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], 1, 3) AS result

/*-----------+
 | result    |
 +-----------+
 | [b, c, d] |
 +-----------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], -1, 3) AS result

/*-----------+
 | result    |
 +-----------+
 | []        |
 +-----------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], 1, -3) AS result

/*--------+
 | result |
 +--------+
 | [b, c] |
 +--------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], -1, -3) AS result

/*-----------+
 | result    |
 +-----------+
 | []        |
 +-----------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], -3, -1) AS result

/*-----------+
 | result    |
 +-----------+
 | [c, d, e] |
 +-----------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], 3, 3) AS result

/*--------+
 | result |
 +--------+
 | [d]    |
 +--------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], -3, -3) AS result

/*--------+
 | result |
 +--------+
 | [c]    |
 +--------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], 1, 30) AS result

/*--------------+
 | result       |
 +--------------+
 | [b, c, d, e] |
 +--------------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], 1, -30) AS result

/*-----------+
 | result    |
 +-----------+
 | []        |
 +-----------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], -30, 30) AS result

/*-----------------+
 | result          |
 +-----------------+
 | [a, b, c, d, e] |
 +-----------------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], -30, -5) AS result

/*--------+
 | result |
 +--------+
 | [a]    |
 +--------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], 5, 30) AS result

/*--------+
 | result |
 +--------+
 | []     |
 +--------*/
```

```
SELECT ARRAY_SLICE(['a', 'b', 'c', 'd', 'e'], 1, NULL) AS result

/*-----------+
 | result    |
 +-----------+
 | NULL      |
 +-----------*/
```

## `ARRAY_TO_STRING`

```
ARRAY_TO_STRING(array_expression, delimiter[, null_text])
```

**Description**

Returns a concatenation of the elements in `array_expression` as a `STRING`
or `BYTES` value. The value for `array_expression` can
either be an array of `STRING` or `BYTES` data type.

If the `null_text` parameter is used, the function replaces any `NULL` values in
the array with the value of `null_text`.

If the `null_text` parameter isn't used, the function omits the `NULL` value
and its preceding delimiter.

**Return type**

* `STRING` for a function signature with `STRING` input.
* `BYTES` for a function signature with `BYTES` input.

**Examples**

```
SELECT ARRAY_TO_STRING(['coffee', 'tea', 'milk', NULL], '--', 'MISSING') AS text

/*--------------------------------+
 | text                           |
 +--------------------------------+
 | coffee--tea--milk--MISSING     |
 +--------------------------------*/
```

```
SELECT ARRAY_TO_STRING(['cake', 'pie', NULL], '--', 'MISSING') AS text

/*--------------------------------+
 | text                           |
 +--------------------------------+
 | cake--pie--MISSING             |
 +--------------------------------*/
```

```
SELECT ARRAY_TO_STRING([b'prefix', b'middle', b'suffix', b'\x00'], b'--') AS data

/*--------------------------------+
 | data                           |
 +--------------------------------+
 | prefix--middle--suffix--\x00   |
 +--------------------------------*/
```

## `GENERATE_ARRAY`

```
GENERATE_ARRAY(start_expression, end_expression[, step_expression])
```

**Description**

Returns an array of values. The `start_expression` and `end_expression`
parameters determine the inclusive start and end of the array.

The `GENERATE_ARRAY` function accepts the following data types as inputs:

* `INT64`
* `NUMERIC`
* `BIGNUMERIC`
* `FLOAT64`

The `step_expression` parameter determines the increment used to
generate array values. The default value for this parameter is `1`.

This function returns an error if `step_expression` is set to 0, or if any
input is `NaN`.

If any argument is `NULL`, the function will return a `NULL` array.

**Return Data Type**

`ARRAY`

**Examples**

The following returns an array of integers, with a default step of 1.

```
SELECT GENERATE_ARRAY(1, 5) AS example_array;

/*-----------------+
 | example_array   |
 +-----------------+
 | [1, 2, 3, 4, 5] |
 +-----------------*/
```

The following returns an array using a user-specified step size.

```
SELECT GENERATE_ARRAY(0, 10, 3) AS example_array;

/*---------------+
 | example_array |
 +---------------+</
```