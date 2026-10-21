* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Datetime functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following datetime functions.

All outputs are automatically formatted as per [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601),
separating date and time with a`T`.

## Function list

| Name | Summary |
| --- | --- |
| [`CURRENT_DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#current_datetime) | Returns the current date and time as a `DATETIME` value. |
| [`DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#datetime) | Constructs a `DATETIME` value. |
| [`DATETIME_ADD`](/bigquery/docs/reference/standard-sql/datetime_functions#datetime_add) | Adds a specified time interval to a `DATETIME` value. |
| [`DATETIME_DIFF`](/bigquery/docs/reference/standard-sql/datetime_functions#datetime_diff) | Gets the number of unit boundaries between two `DATETIME` values at a particular time granularity. |
| [`DATETIME_SUB`](/bigquery/docs/reference/standard-sql/datetime_functions#datetime_sub) | Subtracts a specified time interval from a `DATETIME` value. |
| [`DATETIME_TRUNC`](/bigquery/docs/reference/standard-sql/datetime_functions#datetime_trunc) | Truncates a `DATETIME` or `TIMESTAMP` value at a particular granularity. |
| [`EXTRACT`](/bigquery/docs/reference/standard-sql/datetime_functions#extract) | Extracts part of a date and time from a `DATETIME` value. |
| [`FORMAT_DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#format_datetime) | Formats a `DATETIME` value according to a specified format string. |
| [`LAST_DAY`](/bigquery/docs/reference/standard-sql/datetime_functions#last_day) | Gets the last day in a specified time period that contains a `DATETIME` value. |
| [`PARSE_DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#parse_datetime) | Converts a `STRING` value to a `DATETIME` value. |

## `CURRENT_DATETIME`

```
CURRENT_DATETIME([time_zone])
```

```
CURRENT_DATETIME
```

**Description**

Returns the current time as a `DATETIME` object. Parentheses are optional when
called with no arguments.

This function supports an optional `time_zone` parameter.
See [Time zone definitions](/bigquery/docs/reference/standard-sql/timestamp_functions#timezone_definitions) for
information on how to specify a time zone.

The current date and time value is set at the start of the query statement that
contains this function. All invocations of `CURRENT_DATETIME()` within a query
statement yield the same value.

**Return Data Type**

`DATETIME`

**Example**

```
SELECT CURRENT_DATETIME() as now;

/*----------------------------+
 | now                        |
 +----------------------------+
 | 2016-05-19T10:38:47.046465 |
 +----------------------------*/
```

## `DATETIME`

```
1. DATETIME(year, month, day, hour, minute, second)
2. DATETIME(date_expression[, time_expression])
3. DATETIME(timestamp_expression [, time_zone])
```

**Description**

1. Constructs a `DATETIME` object using `INT64` values
   representing the year, month, day, hour, minute, and second.
2. Constructs a `DATETIME` object using a DATE object and an optional `TIME`
   object.
3. Constructs a `DATETIME` object using a `TIMESTAMP` object. It supports an
   optional parameter to
   [specify a time zone](/bigquery/docs/reference/standard-sql/timestamp_functions#timezone_definitions).
   If no time zone is specified, the default time zone, UTC,
   is used.

**Return Data Type**

`DATETIME`

**Example**

```
SELECT
  DATETIME(2008, 12, 25, 05, 30, 00) as datetime_ymdhms,
  DATETIME(TIMESTAMP "2008-12-25 05:30:00+00", "America/Los_Angeles") as datetime_tstz;

/*---------------------+---------------------+
 | datetime_ymdhms     | datetime_tstz       |
 +---------------------+---------------------+
 | 2008-12-25T05:30:00 | 2008-12-24T21:30:00 |
 +---------------------+---------------------*/
```

## `DATETIME_ADD`

```
DATETIME_ADD(datetime_expression, INTERVAL step_size step_unit)
```

**Description**

Adds `step_size` units of `step_unit` to the `DATETIME` object.

`DATETIME_ADD` supports the following values for `step_unit`:

* `MICROSECOND`
* `MILLISECOND`
* `SECOND`
* `MINUTE`
* `HOUR`
* `DAY`
* `WEEK`. Equivalent to 7 `DAY`s.
* `MONTH`
* `QUARTER`
* `YEAR`

Special handling is required for MONTH, QUARTER, and YEAR parts when the
date is at (or near) the last day of the month. If the resulting month has fewer
days than the original `DATETIME` object's day, then the result day is the last day of
the new month.

**Return Data Type**

`DATETIME`

**Example**

```
SELECT
  DATETIME "2008-12-25 15:30:00" as original_date,
  DATETIME_ADD(DATETIME "2008-12-25 15:30:00", INTERVAL 10 MINUTE) as later;

/*-----------------------------+------------------------+
 | original_date               | later                  |
 +-----------------------------+------------------------+
 | 2008-12-25T15:30:00         | 2008-12-25T15:40:00    |
 +-----------------------------+------------------------*/
```

## `DATETIME_DIFF`

```
DATETIME_DIFF(end_datetime, start_datetime, granularity)
```

**Description**

Gets the number of unit boundaries between two `DATETIME` values
(`end_datetime` - `start_datetime`) at a particular time granularity.

**Definitions**

* `start_datetime`: The starting `DATETIME` value.
* `end_datetime`: The ending `DATETIME` value.
* `granularity`: The datetime part that represents the granularity. If
  you have passed in `DATETIME` values for the first arguments, `granularity`
  can be:

  + `MICROSECOND`
  + `MILLISECOND`
  + `SECOND`
  + `MINUTE`
  + `HOUR`
  + `DAY`
  + `WEEK`: This date part begins on Sunday.
  + `WEEK(<WEEKDAY>)`: This date part begins on `WEEKDAY`. Valid values for
    `WEEKDAY` are `SUNDAY`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`,
    `FRIDAY`, and `SATURDAY`.
  + `ISOWEEK`: Uses [ISO 8601 week](https://en.wikipedia.org/wiki/ISO_week_date)
    boundaries. ISO weeks begin on Monday.
  + `MONTH`
  + `QUARTER`
  + `YEAR`
  + `ISOYEAR`: Uses the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
    week-numbering year boundary. The ISO year boundary is the Monday of the
    first week whose Thursday belongs to the corresponding Gregorian calendar
    year.

**Details**

If `end_datetime` is earlier than `start_datetime`, the output is 0 or negative.
Decimals are always truncated rather than rounded. For example, both 3.9 and 3.1
become 3, while -3.9 and -3.1 become -3 (instead of -4).

Produces an error if the computation overflows, such as if the difference
in microseconds
between the two `DATETIME` values overflows.

**Note:** The behavior of the this function follows the type of arguments passed in.
For example, `DATETIME_DIFF(TIMESTAMP, TIMESTAMP, PART)`
behaves like `TIMESTAMP_DIFF(TIMESTAMP, TIMESTAMP, PART)`.

**Return Data Type**

`INT64`

**Examples**

```
SELECT
  DATETIME "2010-07-07 10:20:00" as first_datetime,
  DATETIME "2008-12-25 15:30:00" as second_datetime,
  DATETIME_DIFF(DATETIME "2010-07-07 10:20:00",
    DATETIME "2008-12-25 15:30:00", DAY) as difference;

/*----------------------------+------------------------+------------------------+
 | first_datetime             | second_datetime        | difference             |
 +----------------------------+------------------------+------------------------+
 | 2010-07-07T10:20:00        | 2008-12-25T15:30:00    | 559                    |
 +----------------------------+------------------------+------------------------*/
```

In the following example, `DATETIME_DIFF` truncates the output rather than
rounding it. Both 3 hours 54 minutes (3.9 hours) and 3 hours 6 minutes (3.1
hours) truncate to 3 hours, and their negative counterparts truncate to -3
hours:

```
SELECT
  DATETIME_DIFF(DATETIME '2021-05-01 04:54:00',
    DATETIME '2021-05-01 01:00:00', HOUR) AS diff_3_9,
  DATETIME_DIFF(DATETIME '2021-05-01 04:06:00',
    DATETIME '2021-05-01 01:00:00', HOUR) AS diff_3_1,
  DATETIME_DIFF(DATETIME '2021-05-01 01:00:00',
    DATETIME '2021-05-01 04:54:00', HOUR) AS diff_negative_3_9,
  DATETIME_DIFF(DATETIME '2021-05-01 01:00:00',
    DATETIME '2021-05-01 04:06:00', HOUR) AS diff_negative_3_1;

/*----------+----------+-------------------+-------------------+
 | diff_3_9 | diff_3_1 | diff_negative_3_9 | diff_negative_3_1 |
 +----------+----------+-------------------+-------------------+
 | 3        | 3        | -3                | -3                |
 +----------+----------+-------------------+-------------------*/
```

```
SELECT
  DATETIME_DIFF(DATETIME '2017-10-15 00:00:00',
    DATETIME '2017-10-14 00:00:00', DAY) as days_diff,
  DATETIME_DIFF(DATETIME '2017-10-15 00:00:00',
    DATETIME '2017-10-14 00:00:00', WEEK) as weeks_diff;

/*-----------+------------+
 | days_diff | weeks_diff |
 +-----------+------------+
 | 1         | 1          |
 +-----------+------------*/
```

The example above shows the result of `DATETIME_DIFF` for two `DATETIME`s that
are 24 hours apart. `DATETIME_DIFF` with the part `WEEK` returns 1 because
`DATETIME_DIFF` counts the number of part boundaries in this range of
`DATETIME`s. Each `WEEK` begins on Sunday, so there is one part boundary between
Saturday, `2017-10-14 00:00:00` and Sunday, `2017-10-15 00:00:00`.

The following example shows the result of `DATETIME_DIFF` for two dates in
different years. `DATETIME_DIFF` with the date part `YEAR` returns 3 because it
counts the number of Gregorian calendar year boundaries between the two
`DATETIME`s. `DATETIME_DIFF` with the date part `ISOYEAR` returns 2 because the
second `DATETIME` belongs to the ISO year 2015. The first Thursday of the 2015
calendar year was 2015-01-01, so the ISO year 2015 begins on the preceding
Monday, 2014-12-29.

```
SELECT
  DATETIME_DIFF('2017-12-30 00:00:00',
    '2014-12-30 00:00:00', YEAR) AS year_diff,
  DATETIME_DIFF('2017-12-30 00:00:00',
    '2014-12-30 00:00:00', ISOYEAR) AS isoyear_diff;

/*-----------+--------------+
 | year_diff | isoyear_diff |
 +-----------+--------------+
 | 3         | 2            |
 +-----------+--------------*/
```

The following example shows the result of `DATETIME_DIFF` for two days in
succession. The first date falls on a Monday and the second date falls on a
Sunday. `DATETIME_DIFF` with the date part `WEEK` returns 0 because this time
part uses weeks that begin on Sunday. `DATETIME_DIFF` with the date part
`WEEK(MONDAY)` returns 1. `DATETIME_DIFF` with the date part
`ISOWEEK` also returns 1 because ISO weeks begin on Monday.

```
SELECT
  DATETIME_DIFF('2017-12-18', '2017-12-17', WEEK) AS week_diff,
  DATETIME_DIFF('2017-12-18', '2017-12-17', WEEK(MONDAY)) AS week_weekday_diff,
  DATETIME_DIFF('2017-12-18', '2017-12-17', ISOWEEK) AS isoweek_diff;

/*-----------+-------------------+--------------+
 | week_diff | week_weekday_diff | isoweek_diff |
 +-----------+-------------------+--------------+
 | 0         | 1                 | 1            |
 +-----------+-------------------+--------------*/
```

## `DATETIME_SUB`

```
DATETIME_SUB(datetime_expression, INTERVAL step_size step_unit)
```

**Description**

Subtracts `step_size` units of `step_unit` from the `DATETIME` object.

`DATETIME_SUB` supports the following values for `step_unit`:

* `MICROSECOND`
* `MILLISECOND`
* `SECOND`
* `MINUTE`
* `HOUR`
* `DAY`
* `WEEK`. Equivalent to 7 `DAY`s.
* `MONTH`
* `QUARTER`
* `YEAR`

Special handling is required for `MONTH`, `QUARTER`, and `YEAR` parts when the
date is at (or near) the last day of the month. If the resulting month has fewer
days than the original `DATETIME` object's day, then the result day is the last day of
the new month.

**Return Data Type**

`DATETIME`

**Example**