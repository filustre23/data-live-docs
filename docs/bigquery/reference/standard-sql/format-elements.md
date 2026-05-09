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
| `%F` | `DATE` `DATETIME` `TIMESTAMP` | The date in the format %Y-%m-%d. | `2021-01-20` |
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
| `%Y` | `DATE` `DATETIME` `TIMESTAMP` | The year with century as a decimal number. | `2021` |
| `%y` | `DATE` `DATETIME` `TIMESTAMP` | The year without century as a decimal number (00-99), with an optional leading zero. Can be mixed with %C. If %C isn't specified, years 00-68 are 2000s, while years 69-99 are 1900s. | `21` |
| `%Z` | `TIMESTAMP` | The time zone name. | `UTC-5` |
| `%z` | `TIMESTAMP` | The offset from the Prime Meridian in the format +HHMM or -HHMM as appropriate, with positive values representing locations east of Greenwich. | `-0500` |
| `%%` | All | A single % character. | `%` |
| `%Ez` | `TIMESTAMP` | RFC 3339-compatible numeric time zone (+HH:MM or -HH:MM). | `-05:00` |
| `%E<number>S` | `TIME` `DATETIME` `TIMESTAMP` | Seconds with <number> digits of fractional precision. | `00.000 for %E3S` |
| `%E*S` | `TIME` `DATETIME` `TIMESTAMP` | Seconds with full fractional precision (a literal '\*'). | `00.123456` |
| `%E4Y` | `DATE` `DATETIME` `TIMESTAMP` | Four-character years (0001 ... 9999). Note that %Y produces as many characters as it takes to fully render the year. | `2021` |

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
SELECT CAST(b'\x48\x65\x6c\x6c\x6f' AS STRING FORMAT 'ASCII') AS bytes_to_string;

/*-----------------+
 | bytes_to_string |
 +-----------------+
 | Hello           |
 +-----------------*/
```

### Format string as bytes

```
CAST(string_expression AS BYTES FORMAT format_string_expression)
```

You can cast a string to bytes with a format element in the
format string. If the string can't be formatted with the
format element, an error is returned. Format elements are case-insensitive.

In the string expression, whitespace characters, such as `\n`, are ignored
if the `BASE64` or `BASE64M` format element is used.

**Note:** The bytes output value is displayed as a base64-encoded string. For
example, `b'\x00\x01\xEF\xFF'` is displayed as `0001efff` when you use the
`HEX` format element.

| Format element | Returns | Example |
| --- | --- | --- |
| HEX | Converts a hexadecimal-encoded string to bytes. If the input contains characters that aren't part of the HEX encoding alphabet (0~9, case-insensitive a~f), an error is returned. | Input: '0001efff'  Output: b'\x00\x01\xEF\xFF' |
| BASEX | Converts a [BASEX](#about_basex_encoding)-encoded string to bytes. X represents one of these numbers: 2, 8, 16, 32, 64. An error is returned if the input contains characters that aren't part of the BASEX encoding alphabet, except whitespace characters if the format element is `BASE64`. | Input as BASE8: '00410473'  Output: b'\x02\x11\x3B' |
| BASE64M | Converts a [base64](#about_basex_encoding)-encoded string to bytes. If the input contains characters that aren't whitespace and not part of the base64 encoding alphabet defined at [rfc 2045](https://tools.ietf.org/html/rfc2045#section-6.8), an error is returned. `BASE64M` and `BASE64` decoding have the same behavior. | Input: '3q2+7w=='  Output: b'\xde\xad\xbe\xef' |
| ASCII | Converts a string with only ASCII characters to bytes. If the input contains characters that aren't ASCII characters, an error is returned. | Input: 'Hello'  Output: b'\x48\x65\x6c\x6c\x6f' |
| UTF-8 | Converts a string to a sequence of UTF-8 bytes. | Input: '$'  Output: b'\x24' |
| UTF8 | Same behavior as UTF-8. |  |

**Return type**

`BYTES`

**Example**

```
SELECT CAST('Hello' AS BYTES FORMAT 'ASCII') AS string_to_bytes

-- Displays the bytes output value (b'\x48\x65\x6c\x6c\x6f').

/*-------------------------+
 | string_to_bytes         |
 +-------------------------+
 | b'\x48\x65\x6c\x6c\x6f' |
 +-------------------------*/
```

### Format date and time as string

You can format these date and time parts as a string:

* [Format year part as string](#format_year_as_string)
* [Format month part as string](#format_month_as_string)
* [Format day part as string](#format_day_as_string)
* [Format hour part as string](#format_hour_as_string)
* [Format minute part as string](#format_minute_as_string)
* [Format second part as string](#format_second_as_string)
* [Format meridian indicator as string](#format_meridian_as_string)
* [Format time zone as string](#format_tz_as_string)
* [Format literal as string](#format_literal_as_string)

Case matching is supported when you format some date or time parts as a string
and the output contains letters. To learn more,
see [Case matching](#case_matching_date_time).

#### Case matching

When the output of some format element contains letters, the letter cases of
the output is matched with the letter cases of the format element,
meaning the words in the output are capitalized according to how the
format element is capitalized. This is called case matching. The rules are:

* If the first two letters of the element are both upper case, the words in
  the output are capitalized. For example `DAY` = `THURSDAY`.
* If the first letter of the element is upper case, and the second letter is
  lowercase, the first letter of each word in the output is capitalized and
  other letters are lowercase. For example `Day` = `Thursday`.
* If the first letter of the element is lowercase, then all letters in the
  output are lowercase. For example, `day` = `thursday`.

#### Format year part as string

```
CAST(expression AS STRING FORMAT format_string_expression)
```

Casts a data type that contains the year part to a string. Includes
format elements, which provide instructions for how to conduct the cast.

* `expression`: This expression contains the data type with the year
  that you need to format.
* `format_string_expression`: A string which contains format elements, including
  the year format element.

These data types include a year part:

* `DATE`
* `DATETIME`
* `TIMESTAMP`

If `expression` or `format_string_expression` is `NULL` the return value is
`NULL`. If `format_string_expression` is an empty string, the output is an
empty string. An error is generated if a value that isn't a supported
format element appears in `format_string_expression` or `expression` doesn't
contain a value specified by a format element.

| Format element | Returns | Example |
| --- | --- | --- |
| YYYY | Year, 4 or more digits. | Input: DATE '2018-01-30'  Output: 2018  ---  Input: DATE '76-01-30'  Output: 0076  ---  Input: DATE '10000-01-30'  Output: 10000 |
| YYY | Year, last 3 digits only. | Input: DATE '2018-01-30'  Output: 018  ---  Input: DATE '98-01-30'  Output: 098 |
| YY | Year, last 2 digits only. | Input: DATE '2018-01-30'  Output: 18  ---  Input: DATE '8-01-30'  Output: 08 |
| Y | Year, last digit only. | Input: DATE '2018-01-30'  Output: 8 |
| RRRR | Same behavior as YYYY. |  |
| RR | Same behavior as YY. |  |

**Return type**

`STRING`

**Example**

```
SELECT CAST(DATE '2018-01-30' AS STRING FORMAT 'YYYY') AS date_time_to_string;

/*---------------------+
 | date_time_to_string |
 +---------------------+
 | 2018                |
 +---------------------*/
```

#### Format month part as string

```
CAST(expression AS STRING FORMAT format_string_expression)
```

Casts a data type that contains the month part to a string. Includes
format elements, which provide instructions for how to conduct the cast.

* `expression`: This expression contains the data type with the month
  that you need to format.
* `format_string_expression`: A string which contains format elements, including
  the month format element.

These data types include a month part:

* `DATE`
* `DATETIME`
* `TIMESTAMP`

If `expression` or `format_string_expression` is `NULL` the return value is
`NULL`. If `format_string_expression` is an empty string, the output is an
empty string. An error is generated if a value that isn't a supported
format element appears in `format_string_expression` or `expression` doesn't
contain a value specified by a format element.

| Format element | Returns | Example |
| --- | --- | --- |
| MM | Month, 2 digits. | Input: DATE '2018-01-30'  Output: 01 |
| MON | Abbreviated, 3-character name of the month. The abbreviated month names for locale en-US are: JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC. [Case matching](#case_matching_date_time) is supported. | Input: DATE '2018-01-30'  Output: JAN |
| MONTH | Name of the month. [Case matching](#case_matching_date_time) is supported. | Input: DATE '2018-01-30'  Output: JANUARY |

**Return type**

`STRING`

**Example**

```
SELECT CAST(DATE '2018-01-30' AS STRING FORMAT 'MONTH') AS date_time_to_string;

/*---------------------+
 | date_time_to_string |
 +---------------------+
 | JANUARY             |
 +---------------------*/
```

#### Format day part as string

```
CAST(expression AS STRING FORMAT format_string_expression)
```

Casts a data type that contains the day part to a string. Includes
format elements, which provide instructions for how to conduct the cast.

* `expression`: This expression contains the data type with the day
  that you need to format.
* `format_string_expression`: A string which contains format elements, including
  the day format element.

These data types include a day part:

* `DATE`
* `DATETIME`
* `TIMESTAMP`

If `expression` or `format_string_expression` is `NULL` the return value is
`NULL`. If `format_string_expression` is an empty string, the output is an
empty string. An error is generated if a value that isn't a supported
format element appears in `format_string_expression` or `expression` doesn't
contain a value specified by a format element.

| Format element | Returns | Example |
| --- | --- | --- |
| DAY | Name of the day of the week, localized. Spaces are padded on the right side to make the output size exactly 9. [Case matching](#case_matching_date_time) is supported. | Input: DATE '2020-12-31'  Output: THURSDAY |
| DY | Abbreviated, 3-character name of the weekday, localized. The abbreviated weekday names for locale en-US are: MON, TUE, WED, THU, FRI, SAT, SUN. [Case matching](#case_matching_date_time) is supported. | Input: DATE '2020-12-31'  Output: THU |
| D | Day of the week (1 to 7), starting with Sunday as 1. | Input: DATE '2020-12-31'  Output: 4 |
| DD | 2-digit day of the month. | Input: DATE '2018-12-02'  Output: 02 |
| DDD | 3-digit day of the year. | Input: DATE '2018-02-03'  Output: 034 |

**Return type**

`STRING`

**Example**

```
SELECT CAST(DATE '2018-02-15' AS STRING FORMAT 'DD') AS date_time_to_string;

/*---------------------+
 | date_time_to_string |
 +---------------------+
 | 15                  |
 +---------------------*/
```

#### Format hour part as string

```
CAST(expression AS STRING FORMAT format_string_expression)
```

Casts a data type that contains the hour part to a string. Includes
format elements, which provide instructions for how to conduct the cast.

* `expression`: This expression contains the data type with the hour
  that you need to format.
* `format_string_expression`: A string which contains format elements, including
  the hour format element.

These data types include a hour part:

* `TIME`
* `DATETIME`
* `TIMESTAMP`

If `expression` or `format_string_expression` is `NULL` the return value is
`NULL`. If `format_string_expression` is an empty string, the output is an
empty string. An error is generated if a value that isn't a supported
format element appears in `format_string_expression` or `expression` doesn't
contain a value specified by a format element.

| Format element | Returns | Example |
| --- | --- | --- |
| HH | Hour of the day, 12-hour clock, 2 digits. | Input: TIME '21:30:00'  Output: 09 |
| HH12 | Hour of the day, 12-hour clock. | Input: TIME '21:30:00'  Output: 09 |
| HH24 | Hour of the day, 24-hour clock, 2 digits. | Input: TIME '21:30:00'  Output: 21 |

**Return type**

`STRING`

**Examples**

```
SELECT CAST(TIME '21:30:00' AS STRING FORMAT 'HH24') AS date_time_to_string;

/*---------------------+
 | date_time_to_string |
 +---------------------+
 | 21                  |
 +---------------------*/
```

```
SELECT CAST(TIME '21:30:00' AS STRING FORMAT 'HH12') AS date_time_to_string;

/*---------------------+
 | date_time_to_string |
 +---------------------+
 | 09                  |
 +---------------------*/
```

#### Format minute part as string

```
CAST(expression AS STRING FORMAT format_string_expression)
```

Casts a data type that contains the minute part to a string. Includes
format elements, which provide instructions for how to conduct the cast.

* `expression`: This expression contains the data type with the minute
  that you need to format.
* `format_string_expression`: A string which contains format elements, including
  the minute format element.

These data types include a minute part:

* `TIME`
* `DATETIME`
* `TIMESTAMP`

If `expression` or `format_string_expression` is `NULL` the return value is
`NULL`. If `format_string_expression` is an empty string, the output is an
empty string. An error is generated if a value that isn't a supported
format element appears in `format_string_expression` or `expression` doesn't
contain a value specified by a format element.

| Format element | Returns | Example |
| --- | --- | --- |
| MI | Minute, 2 digits. | Input: TIME '01:02:03'  Output: 02 |

**Return type**

`STRING`

**Example**

```
SELECT CAST(TIME '21:30:00' AS STRING FORMAT 'MI') AS date_time_to_string
```