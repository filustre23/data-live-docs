* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Format elements Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following format elements.

## Format elements for date and time parts

Many GoogleSQL parsing and formatting functions rely on a format string
to describe the format of parsed or formatted values. A format string represents
the textual form of date and time and contains separate format elements that are
applied left-to-right.

These functions use format strings:

* [`FORMAT_DATE`](/bigquery/docs/reference/standard-sql/date_functions#format_date)
* [`FORMAT_DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#format_datetime)
* [`FORMAT_TIME`](/bigquery/docs/reference/standard-sql/time_functions#format_time)
* [`FORMAT_TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#format_timestamp)
* [`PARSE_DATE`](/bigquery/docs/reference/standard-sql/date_functions#parse_date)
* [`PARSE_DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#parse_datetime)
* [`PARSE_TIME`](/bigquery/docs/reference/standard-sql/time_functions#parse_time)
* [`PARSE_TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#parse_timestamp)

Format strings generally support the following elements:

| Format element | Type | Description | Example |
| --- | --- | --- | --- |
| `%A` | `DATE` `DATETIME` `TIMESTAMP` | The full weekday name (English). | `Wednesday` |
| `%a` | `DATE` `DATETIME` `TIMESTAMP` | The abbreviated weekday name (English). | `Wed` |
| `%B` | `DATE` `DATETIME` `TIMESTAMP` | The full month name (English). | `January` |
| `%b` | `DATE` `DATETIME` `TIMESTAMP` | The abbreviated month name (English). | `Jan` |
| `%C` | `DATE` `DATETIME` `TIMESTAMP` | The century (a year divided by 100 and truncated to an integer) as a decimal number (00-99). | `20` |
| `%c` | `DATETIME` `TIMESTAMP` | The date and time representation (English). | `Wed Jan 20 21:47:00 2021` |
| `%D` | `DATE` `DATETIME` `TIMESTAMP` | The date in the format %m/%d/%y. | `01/20/21` |
| `%d` | `DATE` `DATETIME` `TIMESTAMP` | The day of the month as a decimal number (01-31). | `20` |
| `%e` | `DATE` `DATETIME` `TIMESTAMP` | The day of month as a decimal number (1-31); single digits are preceded by a space. | `20` |
| `%F` | `DATE` `DATETIME` `TIMESTAMP` | The date in the format %Y-%m-%d. When formatting, this element removes leading zeros from the year. | `2021-01-20` |
| `%G` | `DATE` `DATETIME` `TIMESTAMP` | The [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) year with century as a decimal number. Each ISO year begins on the Monday before the first Thursday of the Gregorian calendar year. Note that %G and %Y may produce different results near Gregorian year boundaries, where the Gregorian year and ISO year can diverge. | `2021` |
| `%g` | `DATE` `DATETIME` `TIMESTAMP` | The [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) year without century as a decimal number (00-99). Each ISO year begins on the Monday before the first Thursday of the Gregorian calendar year. Note that %g and %y may produce different results near Gregorian year boundaries, where the Gregorian year and ISO year can diverge. | `21` |
| `%H` | `TIME` `DATETIME` `TIMESTAMP` | The hour (24-hour clock) as a decimal number (00-23). | `21` |
| `%h` | `DATE` `DATETIME` `TIMESTAMP` | The abbreviated month name (English). | `Jan` |
| `%I` | `TIME` `DATETIME` `TIMESTAMP` | The hour (12-hour clock) as a decimal number (01-12). | `09` |
| `%J` | `DATE` `DATETIME` `TIMESTAMP` | The [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) 1-based day of the year (001-364 or 001-371 days). If the ISO year isn't set, this format element is ignored. | `364` |
| `%j` | `DATE` `DATETIME` `TIMESTAMP` | The day of the year as a decimal number (001-366). | `020` |
| `%k` | `TIME` `DATETIME` `TIMESTAMP` | The hour (24-hour clock) as a decimal number (0-23); single digits are preceded by a space. | `21` |
| `%l` | `TIME` `DATETIME` `TIMESTAMP` | The hour (12-hour clock) as a decimal number (1-12); single digits are preceded by a space. | `9` |
| `%M` | `TIME` `DATETIME` `TIMESTAMP` | The minute as a decimal number (00-59). | `47` |
| `%m` | `DATE` `DATETIME` `TIMESTAMP` | The month as a decimal number (01-12). | `01` |
| `%n` | All | A newline character. |  |
| `%P` | `TIME` `DATETIME` `TIMESTAMP` | When formatting, this is either am or pm.   This can't be used with parsing. Instead, use %p. | `pm` |
| `%p` | `TIME` `DATETIME` `TIMESTAMP` | When formatting, this is either AM or PM.  When parsing, this can be used with am, pm, AM, or PM. | `PM` |
| `%Q` | `DATE` `DATETIME` `TIMESTAMP` | The quarter as a decimal number (1-4). | `1` |
| `%R` | `TIME` `DATETIME` `TIMESTAMP` | The time in the format %H:%M. | `21:47` |
| `%S` | `TIME` `DATETIME` `TIMESTAMP` | The second as a decimal number (00-60). | `00` |
| `%s` | `TIME` `DATETIME` `TIMESTAMP` | The number of seconds since 1970-01-01 00:00:00. Always overrides all other format elements, independent of where %s appears in the string. If multiple %s elements appear, then the last one takes precedence. | `1611179220` |
| `%T` | `TIME` `DATETIME` `TIMESTAMP` | The time in the format %H:%M:%S. | `21:47:00` |
| `%t` | All | A tab character. |  |
| `%U` | `DATE` `DATETIME` `TIMESTAMP` | The week number of the year (Sunday as the first day of the week) as a decimal number (00-53). | `03` |
| `%u` | `DATE` `DATETIME` `TIMESTAMP` | The weekday (Monday as the first day of the week) as a decimal number (1-7). | `3` |
| `%V` | `DATE` `DATETIME` `TIMESTAMP` | The [ISO 8601](https://en.wikipedia.org/wiki/ISO_week_date) week number of the year (Monday as the first day of the week) as a decimal number (01-53). If the week containing January 1 has four or more days in the new year, then it's week 1; otherwise it's week 53 of the previous year, and the next week is week 1. | `03` |
| `%W` | `DATE` `DATETIME` `TIMESTAMP` | The week number of the year (Monday as the first day of the week) as a decimal number (00-53). | `03` |
| `%w` | `DATE` `DATETIME` `TIMESTAMP` | The weekday (Sunday as the first day of the week) as a decimal number (0-6). | `3` |
| `%X` | `TIME` `DATETIME` `TIMESTAMP` | The time representation in HH:MM:SS format. | `21:47:00` |
| `%x` | `DATE` `DATETIME` `TIMESTAMP` | The date representation in MM/DD/YY format. | `01/20/21` |
| `%Y` | `DATE` `DATETIME` `TIMESTAMP` | The year with century as a decimal number. When formatting, this element removes leading zeros. To retain leading zeros for four-character years (0001 ... 9999), use `%E4Y`. | `2021` |
| `%y` | `DATE` `DATETIME` `TIMESTAMP` | The year without century as a decimal number (00-99), with an optional leading zero. Can be mixed with %C. If %C isn't specified, years 00-68 are 2000s, while years 69-99 are 1900s. | `21` |
| `%Z` | `TIMESTAMP` | The time zone name. | `UTC-5` |
| `%z` | `TIMESTAMP` | The offset from the Prime Meridian in the format +HHMM or -HHMM as appropriate, with positive values representing locations east of Greenwich. | `-0500` |
| `%%` | All | A single % character. | `%` |
| `%Ez` | `TIMESTAMP` | RFC 3339-compatible numeric time zone (+HH:MM or -HH:MM). | `-05:00` |
| `%E<number>S` | `TIME` `DATETIME` `TIMESTAMP` | Seconds with <number> digits of fractional precision. | `00.000 for %E3S` |
| `%E*S` | `TIME` `DATETIME` `TIMESTAMP` | Seconds with full fractional precision (a literal '\*'). | `00.123456` |
| `%E4Y` | `DATE` `DATETIME` `TIMESTAMP` | Four-character years (0001 ... 9999) that include leading zeros, unlike `%Y` that only uses as many characters as needed to render the year without leading zeros. | `2021` |

Examples:

```
SELECT FORMAT_DATE("%b-%d-%Y", DATE "2008-12-25") AS formatted;

/*-------------+
 | formatted   |
 +-------------+
 | Dec-25-2008 |
 +-------------*/
```

```
SELECT
  FORMAT_DATETIME("%c", DATETIME "2008-12-25 15:30:00")
  AS formatted;

/*--------------------------+
 | formatted                |
 +--------------------------+
 | Thu Dec 25 15:30:00 2008 |
 +--------------------------*/
```

```
SELECT FORMAT_TIME("%R", TIME "15:30:00") as formatted_time;

/*----------------+
 | formatted_time |
 +----------------+
 | 15:30          |
 +----------------*/
```

```
SELECT FORMAT_TIMESTAMP("%b %Y %Ez", TIMESTAMP "2008-12-25 15:30:00+00")
  AS formatted;

/*-----------------+
 | formatted       |
 +-----------------+
 | Dec 2008 +00:00 |
 +-----------------*/
```

```
SELECT PARSE_DATE("%Y%m%d", "20081225") AS parsed;

/*------------+
 | parsed     |
 +------------+
 | 2008-12-25 |
 +------------*/
```

```
SELECT PARSE_DATETIME('%Y-%m-%d %H:%M:%S', '1998-10-18 13:45:55') AS datetime;

/*---------------------+
 | datetime            |
 +---------------------+
 | 1998-10-18T13:45:55 |
 +---------------------*/
```

```
SELECT PARSE_TIME('%I:%M:%S %p', '2:23:38 pm') AS parsed_time

/*-------------+
 | parsed_time |
 +-------------+
 | 14:23:38    |
 +-------------*/
```

```
SELECT PARSE_TIMESTAMP("%c", "Thu Dec 25 07:30:00 2008") AS parsed;

-- Display of results may differ, depending upon the environment and
-- time zone where this query was executed.
/*-------------------------+
 | parsed                  |
 +-------------------------+
 | 2008-12-25 07:30:00 UTC |
 +-------------------------*/
```

## Format clause for CAST

```
format_clause:
  FORMAT format_model

format_model:
  format_string_expression
```

The format clause can be used in some [`CAST` functions](/bigquery/docs/reference/standard-sql/conversion_functions#cast). You
use a format clause to provide instructions for how to conduct a
cast. For example, you could
instruct a cast to convert a sequence of bytes to a base64-encoded string
instead of a UTF-8-encoded string.

The format clause includes a format model. The format model can contain
format elements combined together as a format string.

### Format bytes as string

```
CAST(bytes_expression AS STRING FORMAT format_string_expression)
```

You can cast a sequence of bytes to a string with a format element in the
format string. If the bytes can't be formatted with a
format element, an error is returned. If the sequence of bytes is `NULL`, the
result is `NULL`. Format elements are case-insensitive.

| Format element | Returns | Example |
| --- | --- | --- |
| HEX | Converts a sequence of bytes into a hexadecimal string. | Input: b'\x00\x01\xEF\xFF'  Output: 0001efff |
| BASEX | Converts a sequence of bytes into a [BASEX](#about_basex_encoding) encoded string. X represents one of these numbers: 2, 8, 16, 32, 64. | Input as BASE8: b'\x02\x11\x3B'  Output: 00410473 |
| BASE64M | Converts a sequence of bytes into a [base64](#about_basex_encoding)-encoded string based on [rfc 2045](https://tools.ietf.org/html/rfc2045#section-6.8) for MIME. Generates a newline character ("\n") every 76 characters. | Input: b'\xde\xad\xbe\xef'  Output: 3q2+7w== |
| ASCII | Converts a sequence of bytes that are ASCII values to a string. If the input contains bytes that aren't a valid ASCII encoding, an error is returned. | Input: b'\x48\x65\x6c\x6c\x6f'  Output: Hello |
| UTF-8 | Converts a sequence of bytes that are UTF-8 values to a string. If the input contains bytes that aren't a valid UTF-8 encoding, an error is returned. | Input: b'\x24'  Output: $ |
| UTF8 | Same behavior as UTF-8. |  |

**Return type**

`STRING`

**Example**

```
SELECT CAST(b'\x48\x65\x6c\x6c\x6f' AS STRING FORMAT 'ASCII') AS bytes_to_string</
```