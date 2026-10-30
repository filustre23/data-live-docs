* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Timestamp functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following timestamp functions.

**Important:** Before working with these functions, you need to understand
the difference between the formats in which timestamps are stored and displayed,
and how time zones are used for the conversion between these formats.
To learn more, see
[How time zones work with timestamp functions](#timezone_definitions).**Note:** These functions return a runtime error if overflow occurs; result
values are bounded by the defined [`DATE` range](/bigquery/docs/reference/standard-sql/data-types#date_type)
and [`TIMESTAMP` range](/bigquery/docs/reference/standard-sql/data-types#timestamp_type).

## Function list

| Name | Summary |
| --- | --- |
| [`CURRENT_TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#current_timestamp) | Returns the current date and time as a `TIMESTAMP` object. |
| [`EXTRACT`](/bigquery/docs/reference/standard-sql/timestamp_functions#extract) | Extracts part of a `TIMESTAMP` value. |
| [`FORMAT_TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#format_timestamp) | Formats a `TIMESTAMP` value according to the specified format string. |
| [`GENERATE_TIMESTAMP_ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#generate_timestamp_array) | Generates an array of timestamps in a range.  For more information, see [Array functions](/bigquery/docs/reference/standard-sql/array_functions). |
| [`PARSE_TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#parse_timestamp) | Converts a `STRING` value to a `TIMESTAMP` value. |
| [`STRING` (Timestamp)](/bigquery/docs/reference/standard-sql/timestamp_functions#string) | Converts a `TIMESTAMP` value to a `STRING` value. |
| [`TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp) | Constructs a `TIMESTAMP` value. |
| [`TIMESTAMP_ADD`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_add) | Adds a specified time interval to a `TIMESTAMP` value. |
| [`TIMESTAMP_DIFF`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_diff) | Gets the number of unit boundaries between two `TIMESTAMP` values at a particular time granularity. |
| [`TIMESTAMP_MICROS`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_micros) | Converts the number of microseconds since 1970-01-01 00:00:00 UTC to a `TIMESTAMP`. |
| [`TIMESTAMP_MILLIS`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_millis) | Converts the number of milliseconds since 1970-01-01 00:00:00 UTC to a `TIMESTAMP`. |
| [`TIMESTAMP_SECONDS`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_seconds) | Converts the number of seconds since 1970-01-01 00:00:00 UTC to a `TIMESTAMP`. |
| [`TIMESTAMP_SUB`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_sub) | Subtracts a specified time interval from a `TIMESTAMP` value. |
| [`TIMESTAMP_TRUNC`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_trunc) | Truncates a `TIMESTAMP` or `DATETIME` value at a particular granularity. |
| [`UNIX_MICROS`](/bigquery/docs/reference/standard-sql/timestamp_functions#unix_micros) | Converts a `TIMESTAMP` value to the number of microseconds since 1970-01-01 00:00:00 UTC. |
| [`UNIX_MILLIS`](/bigquery/docs/reference/standard-sql/timestamp_functions#unix_millis) | Converts a `TIMESTAMP` value to the number of milliseconds since 1970-01-01 00:00:00 UTC. |
| [`UNIX_SECONDS`](/bigquery/docs/reference/standard-sql/timestamp_functions#unix_seconds) | Converts a `TIMESTAMP` value to the number of seconds since 1970-01-01 00:00:00 UTC. |

## `CURRENT_TIMESTAMP`

```
CURRENT_TIMESTAMP()
```

```
CURRENT_TIMESTAMP
```

**Description**

Returns the current date and time as a timestamp object. The timestamp is
continuous, non-ambiguous, has exactly 60 seconds per minute and doesn't repeat
values over the leap second. Parentheses are optional.

This function handles leap seconds by smearing them across a window of 20 hours
around the inserted leap second.

The current timestamp value is set at the start of the query statement that
contains this function. All invocations of `CURRENT_TIMESTAMP()` within a query
statement yield the same value.

**Supported Input Types**

Not applicable

**Result Data Type**

`TIMESTAMP`

**Examples**

```
SELECT CURRENT_TIMESTAMP() AS now;

/*--------------------------------+
 | now                            |
 +--------------------------------+
 | 2020-06-02 23:57:12.120174 UTC |
 +--------------------------------*/
```

## `EXTRACT`

```
EXTRACT(part FROM timestamp_expression [AT TIME ZONE time_zone])
```

**Description**

Returns a value that corresponds to the specified `part` from
a supplied `timestamp_expression`. This function supports an optional
`time_zone` parameter. See
[Time zone definitions](#timezone_definitions) for information
on how to specify a time zone.

Allowed `part` values are:

* `MICROSECOND`
* `MILLISECOND`
* `SECOND`
* `MINUTE`
* `HOUR`
* `DAYOFWEEK`: Returns values in the range [1,7] with Sunday as the first day of
  of the week.
* `DAY`
* `DAYOFYEAR`
* `WEEK`: Returns the week number of the date in the range [0, 53]. Weeks begin
  with Sunday, and dates prior to the first Sunday of the year are in week
  0.
* `WEEK(<WEEKDAY>)`: Returns the week number of `timestamp_expression` in the
  range [0, 53]. Weeks begin on `WEEKDAY`. `datetime`s prior to the first
  `WEEKDAY` of the year are in week 0. Valid values for `WEEKDAY` are `SUNDAY`,
  `MONDAY`, `TUESDAY`, `WEDNESDAY`, `THURSDAY`, `FRIDAY`, and `SATURDAY`.
* `ISOWEEK`: Returns the [ISO 8601 week](https://en.wikipedia.org/wiki/ISO_week_date)
  number of the `datetime_expression`. `ISOWEEK`s begin on Monday. Return values
  are in the range [1, 53]. The first `ISOWEEK` of each ISO year begins on the
  Monday before the first Thursday of the Gregorian calendar year.
* `MONTH`
* `QUARTER`
* `YEAR`
* `ISOYEAR`: Returns the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601)
  week-numbering year, which is the Gregorian calendar year containing the
  Thursday of the week to which `date_expression` belongs.
* `DATE`
* `DATETIME`
* `TIME`

Returned values truncate lower order time periods. For example, when extracting
seconds, `EXTRACT` truncates the millisecond and microsecond values.

**Return Data Type**

`INT64`, except in the following cases:

* If `part` is `DATE`, the function returns a `DATE` object.

**Examples**

In the following example, `EXTRACT` returns a value corresponding to the `DAY`
time part.

```
SELECT
  EXTRACT(
    DAY
    FROM TIMESTAMP('2008-12-25 05:30:00+00') AT TIME ZONE 'UTC')
    AS the_day_utc,
  EXTRACT(
    DAY
    FROM TIMESTAMP('2008-12-25 05:30:00+00') AT TIME ZONE 'America/Los_Angeles')
    AS the_day_california

/*-------------+--------------------+
 | the_day_utc | the_day_california |
 +-------------+--------------------+
 | 25          | 24                 |
 +-------------+--------------------*/
```

In the following examples, `EXTRACT` returns values corresponding to different
time parts from a column of type `TIMESTAMP`.

```
SELECT
  EXTRACT(ISOYEAR FROM TIMESTAMP("2005-01-03 12:34:56+00")) AS isoyear,
  EXTRACT(ISOWEEK FROM TIMESTAMP("2005-01-03 12:34:56+00")) AS isoweek,
  EXTRACT(YEAR FROM TIMESTAMP("2005-01-03 12:34:56+00")) AS year,
  EXTRACT(WEEK FROM TIMESTAMP("2005-01-03 12:34:56+00")) AS week

-- Display of results may differ, depending upon the environment and
-- time zone where this query was executed.
/*---------+---------+------+------+
 | isoyear | isoweek | year | week |
 +---------+---------+------+------+
 | 2005    | 1       | 2005 | 1    |
 +---------+---------+------+------*/
```

```
SELECT
  TIMESTAMP("2007-12-31 12:00:00+00") AS timestamp_value,
  EXTRACT(ISOYEAR FROM TIMESTAMP("2007-12-31 12:00:00+00")) AS isoyear,
  EXTRACT(ISOWEEK FROM TIMESTAMP("2007-12-31 12:00:00+00")) AS isoweek,
  EXTRACT(YEAR FROM TIMESTAMP("2007-12-31 12:00:00+00")) AS year,
  EXTRACT(WEEK FROM TIMESTAMP("2007-12-31 12:00:00+00")) AS week

-- Display of results may differ, depending upon the environment and time zone
-- where this query was executed.
/*---------+---------+------+------+
 | isoyear | isoweek | year | week |
 +---------+---------+------+------+
 | 2008    | 1       | 2007 | 52    |
 +---------+---------+------+------*/
```

```
SELECT
  TIMESTAMP("2009-01-01 12:00:00+00") AS timestamp_value,
  EXTRACT(ISOYEAR FROM TIMESTAMP("2009-01-01 12:00:00+00")) AS isoyear,
  EXTRACT(ISOWEEK FROM TIMESTAMP("2009-01-01 12:00:00+00")) AS isoweek,
  EXTRACT(YEAR FROM TIMESTAMP("2009-01-01 12:00:00+00")) AS year,
  EXTRACT(WEEK FROM TIMESTAMP("2009-01-01 12:00:00+00")) AS week

-- Display of results may differ, depending upon the environment and time zone
-- where this query was executed.
/*---------+---------+------+------+
 | isoyear | isoweek | year | week |
 +---------+---------+------+------+
 | 2009    | 1       | 2009 | 0    |
 +---------+---------+------+------*/
```

```
SELECT
  TIMESTAMP("2009-12-31 12:00:00+00") AS timestamp_value,
  EXTRACT(ISOYEAR FROM TIMESTAMP("2009-12-31 12:00:00+00")) AS isoyear,
  EXTRACT(ISOWEEK FROM TIMESTAMP("2009-12-31 12:00:00+00")) AS isoweek,
  EXTRACT(YEAR FROM TIMESTAMP("2009-12-31 12:00:00+00")) AS year,
  EXTRACT(WEEK FROM TIMESTAMP("2009-12-31 12:00:00+00")) AS week

-- Display of results may differ, depending upon the environment and time zone
-- where this query was executed.
/*---------+---------+------+------+
 | isoyear | isoweek | year | week |
 +---------+---------+------+------+
 | 2009    | 53      | 2009 | 52   |
 +---------+---------+------+------*/
```

```
SELECT
  TIMESTAMP("2017-01-02 12:00:00+00") AS timestamp_value,
  EXTRACT(ISOYEAR FROM TIMESTAMP("2017-01-02 12:00:00+00")) AS isoyear,
  EXTRACT(ISOWEEK FROM TIMESTAMP("2017-01-02 12:00:00+00")) AS isoweek,
  EXTRACT(YEAR FROM TIMESTAMP("2017-01-02 12:00:00+00")) AS year,
  EXTRACT(WEEK FROM TIMESTAMP("2017-01-02 12:00:00+00")) AS week

-- Display of results may differ, depending upon the environment and time zone
-- where this query was executed.
/*---------+---------+------+------+
 | isoyear | isoweek | year | week |
 +---------+---------+------+------+
 | 2017    | 1       | 2017 | 1    |
 +---------+---------+------+------*/
```

```
SELECT
  TIMESTAMP("2017-05-26 12:00:00+00") AS timestamp_value,
  EXTRACT(ISOYEAR FROM TIMESTAMP("2017-05-26 12:00:00+00")) AS isoyear,
  EXTRACT(ISOWEEK FROM TIMESTAMP("2017-05-26 12:00:00+00")) AS isoweek,
```