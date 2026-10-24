* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Date functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following date functions.

## Function list

| Name | Summary |
| --- | --- |
| [`CURRENT_DATE`](/bigquery/docs/reference/standard-sql/date_functions#current_date) | Returns the current date as a `DATE` value. |
| [`DATE`](/bigquery/docs/reference/standard-sql/date_functions#date) | Constructs a `DATE` value. |
| [`DATE_ADD`](/bigquery/docs/reference/standard-sql/date_functions#date_add) | Adds a specified time interval to a `DATE` value. |
| [`DATE_DIFF`](/bigquery/docs/reference/standard-sql/date_functions#date_diff) | Gets the number of unit boundaries between two `DATE` values at a particular time granularity. |
| [`DATE_FROM_UNIX_DATE`](/bigquery/docs/reference/standard-sql/date_functions#date_from_unix_date) | Interprets an `INT64` expression as the number of days since 1970-01-01. |
| [`DATE_SUB`](/bigquery/docs/reference/standard-sql/date_functions#date_sub) | Subtracts a specified time interval from a `DATE` value. |
| [`DATE_TRUNC`](/bigquery/docs/reference/standard-sql/date_functions#date_trunc) | Truncates a `DATE`, `DATETIME`, or `TIMESTAMP` value at a particular granularity. |
| [`EXTRACT`](/bigquery/docs/reference/standard-sql/date_functions#extract) | Extracts part of a date from a `DATE` value. |
| [`FORMAT_DATE`](/bigquery/docs/reference/standard-sql/date_functions#format_date) | Formats a `DATE` value according to a specified format string. |
| [`GENERATE_DATE_ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#generate_date_array) | Generates an array of dates in a range.  For more information, see [Array functions](/bigquery/docs/reference/standard-sql/array_functions). |
| [`LAST_DAY`](/bigquery/docs/reference/standard-sql/date_functions#last_day) | Gets the last day in a specified time period that contains a `DATE` value. |
| [`PARSE_DATE`](/bigquery/docs/reference/standard-sql/date_functions#parse_date) | Converts a `STRING` value to a `DATE` value. |
| [`UNIX_DATE`](/bigquery/docs/reference/standard-sql/date_functions#unix_date) | Converts a `DATE` value to the number of days since 1970-01-01. |

## `CURRENT_DATE`

```
CURRENT_DATE()
```

```
CURRENT_DATE(time_zone_expression)
```

```
CURRENT_DATE
```

**Description**

Returns the current date as a `DATE` object. Parentheses are optional when
called with no arguments.

This function supports the following arguments:

* `time_zone_expression`: A `STRING` expression that represents a
  [time zone](/bigquery/docs/reference/standard-sql/timestamp_functions#timezone_definitions). If no time zone is specified, the
  default time zone, UTC, is used. If this expression is
  used and it evaluates to `NULL`, this function returns `NULL`.

The current date value is set at the start of the query statement that contains
this function. All invocations of `CURRENT_DATE()` within a query statement
yield the same value.

**Return Data Type**

`DATE`

**Examples**

The following query produces the current date in the default time zone:

```
SELECT CURRENT_DATE() AS the_date;

/*--------------+
 | the_date     |
 +--------------+
 | 2016-12-25   |
 +--------------*/
```

The following queries produce the current date in a specified time zone:

```
SELECT CURRENT_DATE('America/Los_Angeles') AS the_date;

/*--------------+
 | the_date     |
 +--------------+
 | 2016-12-25   |
 +--------------*/
```

```
SELECT CURRENT_DATE('-08') AS the_date;

/*--------------+
 | the_date     |
 +--------------+
 | 2016-12-25   |
 +--------------*/
```

The following query produces the current date in the default time zone.
Parentheses aren't needed if the function has no arguments.

```
SELECT CURRENT_DATE AS the_date;

/*--------------+
 | the_date     |
 +--------------+
 | 2016-12-25   |
 +--------------*/
```

## `DATE`

```
DATE(year, month, day)
```

```
DATE(timestamp_expression)
```

```
DATE(timestamp_expression, time_zone_expression)
```

```
DATE(datetime_expression)
```

**Description**

Constructs or extracts a date.

This function supports the following arguments:

* `year`: The `INT64` value for year.
* `month`: The `INT64` value for month.
* `day`: The `INT64` value for day.
* `timestamp_expression`: A `TIMESTAMP` expression that contains the date.
* `time_zone_expression`: A `STRING` expression that represents a
  [time zone](/bigquery/docs/reference/standard-sql/timestamp_functions#timezone_definitions). If no time zone is specified with
  `timestamp_expression`, the default time zone, UTC, is
  used.
* `datetime_expression`: A `DATETIME` expression that contains the date.

**Return Data Type**

`DATE`

**Example**

```
SELECT
  DATE(2016, 12, 25) AS date_ymd,
  DATE(DATETIME '2016-12-25 23:59:59') AS date_dt,
  DATE(TIMESTAMP '2016-12-25 05:30:00+07', 'America/Los_Angeles') AS date_tstz;

/*------------+------------+------------+
 | date_ymd   | date_dt    | date_tstz  |
 +------------+------------+------------+
 | 2016-12-25 | 2016-12-25 | 2016-12-24 |
 +------------+------------+------------*/
```

## `DATE_ADD`

```
DATE_ADD(date_expression, INTERVAL step_size step_unit)
```

**Description**

Adds a specified time interval to a `DATE` object.

`DATE_ADD` supports the following `step_unit` values:

* `DAY`
* `WEEK`. Equivalent to 7 `DAY`s.
* `MONTH`
* `QUARTER`
* `YEAR`

Special handling is required for MONTH, QUARTER, and YEAR parts when
the date is at (or near) the last day of the month. If the resulting
month has fewer days than the original `DATE` object's day, then the resulting
date is the last date of that month.

**Return Data Type**

DATE

**Example**

```
SELECT DATE_ADD(DATE '2008-12-25', INTERVAL 5 DAY) AS five_days_later;

/*--------------------+
 | five_days_later    |
 +--------------------+
 | 2008-12-30         |
 +--------------------*/
```

## `DATE_DIFF`

```
DATE_DIFF(end_date, start_date, granularity)
```

**Description**

Gets the number of unit boundaries between two `DATE` values (`end_date` -
`start_date`) at a particular time granularity.

**Definitions**

* `start_date`: The starting `DATE` value.
* `end_date`: The ending `DATE` value.
* `granularity`: The date part that represents the granularity. If
  you have passed in `DATE` values for the first arguments, `granularity` can
  be:

  + `DAY`
  + `WEEK` This date part begins on Sunday.
  + `WEEK(<WEEKDAY>)`: This date part begins on `WEEKDAY`. Valid values for
    `WEEKDAY` are `SUNDAY`, `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`,
    `FRIDAY`, and `SATURDAY`.
  + `ISOWEEK`: Uses [ISO 8601 week](https://en.wikipedia.org/wiki/ISO_week_date) boundaries. ISO weeks
    begin on Monday.
  + `MONTH`
  + `QUARTER`
  + `YEAR`
  + `ISOYEAR`: Uses the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) week-numbering year boundary.
    The ISO year boundary is the Monday of the first week whose Thursday
    belongs to the corresponding Gregorian calendar year.

**Details**

If `end_date` is earlier than `start_date`, the output is 0 or negative.
Decimals are always truncated rather than rounded. For example, both 3.9 and 3.1
become 3, while -3.9 and -3.1 become -3 (instead of -4).

**Note:** The behavior of the this function follows the type of arguments passed in.
For example, `DATE_DIFF(TIMESTAMP, TIMESTAMP, PART)`
behaves like `TIMESTAMP_DIFF(TIMESTAMP, TIMESTAMP, PART)`.

**Return Data Type**

`INT64`

**Examples**

```
SELECT DATE_DIFF(DATE '2010-07-07', DATE '2008-12-25', DAY) AS days_diff;

/*-----------+
 | days_diff |
 +-----------+
 | 559       |
 +-----------*/
```

In the following example, `DATE_DIFF` truncates the output rather than rounding
it. Both 3 years 11 months (3.9 years) and 3 years 1 month (3.1 years)
truncate to 3 years, and their negative counterparts truncate to -3 years:

```
SELECT
  DATE_DIFF(DATE '2023-11-30', DATE '2020-01-01', YEAR) AS diff_3_9,
  DATE_DIFF(DATE '2023-02-01', DATE '2020-01-01', YEAR) AS diff_3_1,
  DATE_DIFF(DATE '2020-01-01', DATE '2023-11-30', YEAR) AS diff_negative_3_9,
  DATE_DIFF(DATE '2020-01-01', DATE '2023-02-01', YEAR) AS diff_negative_3_1;

/*----------+----------+-------------------+-------------------+
 | diff_3_9 | diff_3_1 | diff_negative_3_9 | diff_negative_3_1 |
 +----------+----------+-------------------+-------------------+
 | 3        | 3        | -3                | -3                |
 +----------+----------+-------------------+-------------------*/
```

```
SELECT
  DATE_DIFF(DATE '2017-10-15', DATE '2017-10-14', DAY) AS days_diff,
  DATE_DIFF(DATE '2017-10-15', DATE '2017-10-14', WEEK) AS weeks_diff;

/*-----------+------------+
 | days_diff | weeks_diff |
 +-----------+------------+
 | 1         | 1          |
 +-----------+------------*/
```

The example above shows the result of `DATE_DIFF` for two days in succession.
`DATE_DIFF` with the date part `WEEK` returns 1 because `DATE_DIFF` counts the
number of date part boundaries in this range of dates. Each `WEEK` begins on
Sunday, so there is one date part boundary between Saturday, 2017-10-14
and Sunday, 2017-10-15.

The following example shows the result of `DATE_DIFF` for two dates in different
years. `DATE_DIFF` with the date part `YEAR` returns 3 because it counts the
number of Gregorian calendar year boundaries between the two dates. `DATE_DIFF`
with the date part `ISOYEAR` returns 2 because the second date belongs to the
ISO year 2015. The first Thursday of the 2015 calendar year was 2015-01-01, so
the ISO year 2015 begins on the preceding Monday, 2014-12-29.

```
SELECT
  DATE_DIFF('2017-12-30', '2014-12-30', YEAR) AS year_diff,
  DATE_DIFF('2017-12-30', '2014-12-30', ISOYEAR) AS isoyear_diff;

/*-----------+--------------+
 | year_diff | isoyear_diff |
 +-----------+--------------+
 | 3         | 2            |
 +-----------+--------------*/
```

The following example shows the result of `DATE_DIFF` for two days in
succession. The first date falls on a Monday and the second date falls on a
Sunday. `DATE_DIFF` with the date part `WEEK` returns 0 because this date part
uses weeks that begin on Sunday. `DATE_DIFF` with the date part `WEEK(MONDAY)`
returns 1. `DATE_DIFF` with the date part `ISOWEEK` also returns 1 because
ISO weeks begin on Monday.

```
SELECT
  DATE_DIFF('2017-12-18', '2017-12-17', WEEK) AS week_diff,
  DATE_DIFF('2017-12-18', '2017-12-17', WEEK(MONDAY)) AS week_weekday_diff,
  DATE_DIFF('2017-12-18', '2017-12-17', ISOWEEK) AS isoweek_diff;

/*-----------+-------------------+--------------+
 | week_diff | week_weekday_diff | isoweek_diff |
 +-----------+-------------------+--------------+
 | 0         | 1                 | 1            |
 +-----------+-------------------+--------------*/
```

## `DATE_FROM_UNIX_DATE`

```
DATE_FROM_UNIX_DATE(int64_expression)
```

**Description**

Interprets `int64_expression` as the number of days since 1970-01-01.

**Return Data Type**

DATE

**Example**

```
SELECT DATE_FROM_UNIX_DATE(14238) AS date_from_epoch</
```