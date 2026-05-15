* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Navigation functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports navigation functions.
Navigation functions are a subset of window functions. To create a
window function call and learn about the syntax for window functions,
see [Window function\_calls](/bigquery/docs/reference/standard-sql/window-function-calls).

Navigation functions generally compute some
`value_expression` over a different row in the window frame from the
current row. The `OVER` clause syntax varies across navigation functions.

For all navigation functions, the result data type is the same type as
`value_expression`.

## Function list

| Name | Summary |
| --- | --- |
| [`FIRST_VALUE`](/bigquery/docs/reference/standard-sql/navigation_functions#first_value) | Gets a value for the first row in the current window frame. |
| [`LAG`](/bigquery/docs/reference/standard-sql/navigation_functions#lag) | Gets a value for a preceding row. |
| [`LAST_VALUE`](/bigquery/docs/reference/standard-sql/navigation_functions#last_value) | Gets a value for the last row in the current window frame. |
| [`LEAD`](/bigquery/docs/reference/standard-sql/navigation_functions#lead) | Gets a value for a subsequent row. |
| [`NTH_VALUE`](/bigquery/docs/reference/standard-sql/navigation_functions#nth_value) | Gets a value for the Nth row of the current window frame. |
| [`PERCENTILE_CONT`](/bigquery/docs/reference/standard-sql/navigation_functions#percentile_cont) | Computes the specified percentile for a value, using linear interpolation. |
| [`PERCENTILE_DISC`](/bigquery/docs/reference/standard-sql/navigation_functions#percentile_disc) | Computes the specified percentile for a discrete value. |

## `FIRST_VALUE`

```
FIRST_VALUE (value_expression [{RESPECT | IGNORE} NULLS])
OVER over_clause

over_clause:
  { named_window | ( [ window_specification ] ) }

window_specification:
  [ named_window ]
  [ PARTITION BY partition_expression [, ...] ]
  ORDER BY expression [ { ASC | DESC }  ] [, ...]
  [ window_frame_clause ]
```

**Description**

Returns the value of the `value_expression` for the first row in the current
window frame.

This function includes `NULL` values in the calculation unless `IGNORE NULLS` is
present. If `IGNORE NULLS` is present, the function excludes `NULL` values from
the calculation.

To learn more about the `OVER` clause and how to use it, see
[Window function calls](/bigquery/docs/reference/standard-sql/window-function-calls).



**Supported Argument Types**

`value_expression` can be any data type that an expression can return.

**Return Data Type**

Same type as `value_expression`.

**Examples**

The following example computes the fastest time for each division.

```
WITH finishers AS
 (SELECT 'Sophia Liu' as name,
  TIMESTAMP '2016-10-18 2:51:45' as finish_time,
  'F30-34' as division
  UNION ALL SELECT 'Lisa Stelzner', TIMESTAMP '2016-10-18 2:54:11', 'F35-39'
  UNION ALL SELECT 'Nikki Leith', TIMESTAMP '2016-10-18 2:59:01', 'F30-34'
  UNION ALL SELECT 'Lauren Matthews', TIMESTAMP '2016-10-18 3:01:17', 'F35-39'
  UNION ALL SELECT 'Desiree Berry', TIMESTAMP '2016-10-18 3:05:42', 'F35-39'
  UNION ALL SELECT 'Suzy Slane', TIMESTAMP '2016-10-18 3:06:24', 'F35-39'
  UNION ALL SELECT 'Jen Edwards', TIMESTAMP '2016-10-18 3:06:36', 'F30-34'
  UNION ALL SELECT 'Meghan Lederer', TIMESTAMP '2016-10-18 3:07:41', 'F30-34'
  UNION ALL SELECT 'Carly Forte', TIMESTAMP '2016-10-18 3:08:58', 'F25-29'
  UNION ALL SELECT 'Lauren Reasoner', TIMESTAMP '2016-10-18 3:10:14', 'F30-34')
SELECT name,
  FORMAT_TIMESTAMP('%X', finish_time) AS finish_time,
  division,
  FORMAT_TIMESTAMP('%X', fastest_time) AS fastest_time,
  TIMESTAMP_DIFF(finish_time, fastest_time, SECOND) AS delta_in_seconds
FROM (
  SELECT name,
  finish_time,
  division,
  FIRST_VALUE(finish_time)
    OVER (PARTITION BY division ORDER BY finish_time ASC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING) AS fastest_time
  FROM finishers);

/*-----------------+-------------+----------+--------------+------------------+
 | name            | finish_time | division | fastest_time | delta_in_seconds |
 +-----------------+-------------+----------+--------------+------------------+
 | Carly Forte     | 03:08:58    | F25-29   | 03:08:58     | 0                |
 | Sophia Liu      | 02:51:45    | F30-34   | 02:51:45     | 0                |
 | Nikki Leith     | 02:59:01    | F30-34   | 02:51:45     | 436              |
 | Jen Edwards     | 03:06:36    | F30-34   | 02:51:45     | 891              |
 | Meghan Lederer  | 03:07:41    | F30-34   | 02:51:45     | 956              |
 | Lauren Reasoner | 03:10:14    | F30-34   | 02:51:45     | 1109             |
 | Lisa Stelzner   | 02:54:11    | F35-39   | 02:54:11     | 0                |
 | Lauren Matthews | 03:01:17    | F35-39   | 02:54:11     | 426              |
 | Desiree Berry   | 03:05:42    | F35-39   | 02:54:11     | 691              |
 | Suzy Slane      | 03:06:24    | F35-39   | 02:54:11     | 733              |
 +-----------------+-------------+----------+--------------+------------------*/
```

## `LAG`

```
LAG (value_expression[, offset [, default_expression]])
OVER over_clause

over_clause:
  { named_window | ( [ window_specification ] ) }

window_specification:
  [ named_window ]
  [ PARTITION BY partition_expression [, ...] ]
  ORDER BY expression [ { ASC | DESC }  ] [, ...]
```

**Description**

Returns the value of the `value_expression` on a preceding row. Changing the
`offset` value changes which preceding row is returned; the default value is
`1`, indicating the previous row in the window frame. An error occurs if
`offset` is NULL or a negative value.

The optional `default_expression` is used if there isn't a row in the window
frame at the specified offset. This expression must be a constant expression and
its type must be implicitly coercible to the type of `value_expression`. If left
unspecified, `default_expression` defaults to NULL.

To learn more about the `OVER` clause and how to use it, see
[Window function calls](/bigquery/docs/reference/standard-sql/window-function-calls).



**Supported Argument Types**

* `value_expression` can be any data type that can be returned from an
  expression.
* `offset` must be a non-negative integer literal or parameter.
* `default_expression` must be compatible with the value expression type.

**Return Data Type**

Same type as `value_expression`.

**Examples**

The following example illustrates a basic use of the `LAG` function.

```
WITH finishers AS
 (SELECT 'Sophia Liu' as name,
  TIMESTAMP '2016-10-18 2:51:45' as finish_time,
  'F30-34' as division
  UNION ALL SELECT 'Lisa Stelzner', TIMESTAMP '2016-10-18 2:54:11', 'F35-39'
  UNION ALL SELECT 'Nikki Leith', TIMESTAMP '2016-10-18 2:59:01', 'F30-34'
  UNION ALL SELECT 'Lauren Matthews', TIMESTAMP '2016-10-18 3:01:17', 'F35-39'
  UNION ALL SELECT 'Desiree Berry', TIMESTAMP '2016-10-18 3:05:42', 'F35-39'
  UNION ALL SELECT 'Suzy Slane', TIMESTAMP '2016-10-18 3:06:24', 'F35-39'
  UNION ALL SELECT 'Jen Edwards', TIMESTAMP '2016-10-18 3:06:36', 'F30-34'
  UNION ALL SELECT 'Meghan Lederer', TIMESTAMP '2016-10-18 3:07:41', 'F30-34'
  UNION ALL SELECT 'Carly Forte', TIMESTAMP '2016-10-18 3:08:58', 'F25-29'
  UNION ALL SELECT 'Lauren Reasoner', TIMESTAMP '2016-10-18 3:10:14', 'F30-34')
SELECT name,
  finish_time,
  division,
  LAG(name)
    OVER (PARTITION BY division ORDER BY finish_time ASC) AS preceding_runner
FROM finishers;

/*-----------------+-------------+----------+------------------+
 | name            | finish_time | division | preceding_runner |
 +-----------------+-------------+----------+------------------+
 | Carly Forte     | 03:08:58    | F25-29   | NULL             |
 | Sophia Liu      | 02:51:45    | F30-34   | NULL             |
 | Nikki Leith     | 02:59:01    | F30-34   | Sophia Liu       |
 | Jen Edwards     | 03:06:36    | F30-34   | Nikki Leith      |
 | Meghan Lederer  | 03:07:41    | F30-34   | Jen Edwards      |
 | Lauren Reasoner | 03:10:14    | F30-34   | Meghan Lederer   |
 | Lisa Stelzner   | 02:54:11    | F35-39   | NULL             |
 | Lauren Matthews | 03:01:17    | F35-39   | Lisa Stelzner    |
 | Desiree Berry   | 03:05:42    | F35-39   | Lauren Matthews  |
 | Suzy Slane      | 03:06:24    | F35-39   | Desiree Berry    |
 +-----------------+-------------+----------+------------------*/
```

This next example uses the optional `offset` parameter.

```
WITH finishers AS
 (SELECT 'Sophia Liu' as name,
  TIMESTAMP '2016-10-18 2:51:45' as finish_time,
  'F30-34' as division
  UNION ALL SELECT 'Lisa Stelzner', TIMESTAMP '2016-10-18 2:54:11', 'F35-39'
  UNION ALL SELECT 'Nikki Leith', TIMESTAMP '2016-10-18 2:59:01', 'F30-34'
  UNION ALL SELECT 'Lauren Matthews', TIMESTAMP '2016-10-18 3:01:17', 'F35-39'
  UNION ALL SELECT 'Desiree Berry', TIMESTAMP '2016-10-18 3:05:42', 'F35-39'
  UNION ALL SELECT 'Suzy Slane', TIMESTAMP '2016-10-18 3:06:24', 'F35-39'
  UNION ALL SELECT 'Jen Edwards', TIMESTAMP '2016-10-18 3:06:36', 'F30-34'
  UNION ALL SELECT 'Meghan Lederer', TIMESTAMP '2016-10-18 3:07:41', 'F30-34'
  UNION ALL SELECT 'Carly Forte', TIMESTAMP '2016-10-18 3:08:58', 'F25-29'
  UNION ALL SELECT 'Lauren Reasoner', TIMESTAMP '2016-10-18 3:10:14', 'F30-34')
SELECT name,
  finish_time,
  division,
  LAG(name, 2)
    OVER (PARTITION BY division ORDER BY finish_time ASC) AS two_runners_ahead
FROM finishers;

/*-----------------+-------------+----------+-------------------+
 | name            | finish_time | division | two_runners_ahead |
 +-----------------+-------------+----------+-------------------+
 | Carly Forte     | 03:08:58    | F25-29   | NULL              |
 | Sophia Liu      | 02:51:45    | F30-34   | NULL              |
 | Nikki Leith     | 02:59:01    | F30-34   | NULL              |
 | Jen Edwards     | 03:06:36    | F30-34   | Sophia Liu        |
 | Meghan Lederer  | 03:07:41    | F30-34   | Nikki Leith       |
 | Lauren Reasoner | 03:10:14    | F30-34   | Jen Edwards       |
 | Lisa Stelzner   | 02:54:11    | F35-39   | NULL              |
 | Lauren Matthews | 03:01:17    | F35-39   | NULL              |
 | Desiree Berry   | 03:05:42    | F35-39   | Lisa Stelzner     |
 | Suzy Slane      | 03:06:24    | F35-39   | Lauren Matthews   |
 +-----------------+-------------+----------+-------------------*/
```

The following example replaces NULL values with a default value.

```
WITH finishers AS
 (SELECT 'Sophia Liu' as name,
  TIMESTAMP '2016-10-18 2:51:45' as finish_time,
  'F30-34' as division
  UNION ALL SELECT 'Lisa Stelzner', TIMESTAMP '2016-10-18 2:54:11', 'F35-39'
  UNION ALL SELECT 'Nikki Leith', TIMESTAMP '2016-10-18 2:59:01', 'F30-34'
  UNION ALL SELECT 'Lauren Matthews', TIMESTAMP '2016-10-18 3:01:17', 'F35-39'
  UNION ALL SELECT 'Desiree Berry', TIMESTAMP '2016-10-18 3:05:42', 'F35-39'
  UNION ALL SELECT 'Suzy Slane', TIMESTAMP '2016-10-18 3:06:24', 'F35-39'
  UNION ALL SELECT 'Jen Edwards', TIMESTAMP '2016-10-18 3:06:36', 'F30-34'
  UNION ALL SELECT 'Meghan Lederer', TIMESTAMP '2016-10-18 3:07:41', 'F30-34'
  UNION ALL SELECT 'Carly Forte', TIMESTAMP '2016-10-18 3:08:58', 'F25-29'
  UNION ALL SELECT 'Lauren Reasoner', TIMESTAMP '2016-10-18 3:10:14', 'F30-34')
SELECT name,
  finish_time,
  division,
  LAG(name, 2, 'Nobody')
    OVER (PARTITION BY division ORDER BY finish_time ASC) AS two_runners_ahead
FROM finishers;

/*-----------------+-------------+----------+-------------------+
 | name            | finish_time | division | two_runners_ahead |
 +-----------------+-------------+----------+-------------------+
 | Carly Forte     | 03:08:58    | F25-29   | Nobody            |
 | Sophia Liu      | 02:51:45    | F30-34   | Nobody            |
 | Nikki Leith     | 02:59:01    | F30-34   | Nobody            |
 | Jen Edwards     | 03:06:36    | F30-34   | Sophia Liu        |
 | Meghan Lederer  | 03:07:41    | F30-34   | Nikki Leith       |
 | Lauren Reasoner | 03:10:14    | F30-34   | Jen Edwards       |
 | Lisa Stelzner   | 02:54:11    | F35-39   | Nobody            |
 | Lauren Matthews | 03:01:17    | F35-39   | Nobody            |
 | Desiree Berry   | 03:05:42    | F35-39   | Lisa Stelzner     |
 | Suzy Slane      | 03:06:24    | F35-39   | Lauren Matthews   |
 +-----------------+-------------+----------+-------------------*/
```

## `LAST_VALUE`

```
LAST_VALUE (value_expression [{RESPECT | IGNORE} NULLS])
OVER over_clause

over_clause:
  { named_window | ( [ window_specification ] ) }

window_specification:
  [ named_window ]
  [ PARTITION BY partition_expression [, ...] ]
  ORDER BY expression [ { ASC | DESC }  ] [, ...]
  [ window_frame_clause ]
```

**Description**

Returns the value of the `value_expression` for the last row in the current
window frame.

This function includes `NULL` values in the calculation unless `IGNORE NULLS` is
present. If `IGNORE NULLS` is present, the function excludes `NULL` values from
the calculation.

To learn more about the `OVER` clause and how to use it, see
[Window function calls](/bigquery/docs/reference/standard-sql/window-function-calls).



**Supported Argument Types**

`value_expression` can be any data type that an expression can return.

**Return Data Type**

Same type as `value_expression`.

**Examples**

The following example computes the slowest time for each division.

```
WITH finishers AS
 (SELECT 'Sophia Liu' as name,
  TIMESTAMP '2016-10-18 2:51:45' as finish_time,
  'F30-34' as division
  UNION ALL SELECT 'Lisa Stelzner', TIMESTAMP '2016-10-18 2:54:11
```