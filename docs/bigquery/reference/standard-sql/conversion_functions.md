* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Conversion functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports conversion functions. These data type
conversions are explicit, but some conversions can happen implicitly. You can
learn more about implicit and explicit conversion [here](/bigquery/docs/reference/standard-sql/conversion_rules).

## Function list

| Name | Summary |
| --- | --- |
| [`ARRAY_TO_STRING`](/bigquery/docs/reference/standard-sql/array_functions#array_to_string) | Produces a concatenation of the elements in an array as a `STRING` value.  For more information, see [Array functions](/bigquery/docs/reference/standard-sql/array_functions). |
| [`BOOL`](/bigquery/docs/reference/standard-sql/json_functions#bool_for_json) | Converts a JSON boolean to a SQL `BOOL` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`CAST`](/bigquery/docs/reference/standard-sql/conversion_functions#cast) | Convert the results of an expression to the given type. |
| [`CHR`](/bigquery/docs/reference/standard-sql/string_functions#chr) | Converts a Unicode code point to a character.  For more information, see [String functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`CODE_POINTS_TO_BYTES`](/bigquery/docs/reference/standard-sql/string_functions#code_points_to_bytes) | Converts an array of extended ASCII code points to a `BYTES` value.  For more information, see [String aggregate functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`CODE_POINTS_TO_STRING`](/bigquery/docs/reference/standard-sql/string_functions#code_points_to_string) | Converts an array of extended ASCII code points to a `STRING` value.  For more information, see [String aggregate functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`DATE_FROM_UNIX_DATE`](/bigquery/docs/reference/standard-sql/date_functions#date_from_unix_date) | Interprets an `INT64` expression as the number of days since 1970-01-01.  For more information, see [Date functions](/bigquery/docs/reference/standard-sql/date_functions). |
| [`FROM_BASE32`](/bigquery/docs/reference/standard-sql/string_functions#from_base32) | Converts a base32-encoded `STRING` value into a `BYTES` value.  For more information, see [String functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`FROM_BASE64`](/bigquery/docs/reference/standard-sql/string_functions#from_base64) | Converts a base64-encoded `STRING` value into a `BYTES` value.  For more information, see [String functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`FROM_HEX`](/bigquery/docs/reference/standard-sql/string_functions#from_hex) | Converts a hexadecimal-encoded `STRING` value into a `BYTES` value.  For more information, see [String functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`INT64`](/bigquery/docs/reference/standard-sql/json_functions#int64_for_json) | Converts a JSON number to a SQL `INT64` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`LAX_BOOL`](/bigquery/docs/reference/standard-sql/json_functions#lax_bool) | Attempts to convert a JSON value to a SQL `BOOL` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`LAX_FLOAT64`](/bigquery/docs/reference/standard-sql/json_functions#lax_double) | Attempts to convert a JSON value to a SQL `FLOAT64` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`LAX_INT64`](/bigquery/docs/reference/standard-sql/json_functions#lax_int64) | Attempts to convert a JSON value to a SQL `INT64` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`LAX_STRING`](/bigquery/docs/reference/standard-sql/json_functions#lax_string) | Attempts to convert a JSON value to a SQL `STRING` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`PARSE_BIGNUMERIC`](/bigquery/docs/reference/standard-sql/conversion_functions#parse_bignumeric) | Converts a `STRING` value to a `BIGNUMERIC` value. |
| [`PARSE_DATE`](/bigquery/docs/reference/standard-sql/date_functions#parse_date) | Converts a `STRING` value to a `DATE` value.  For more information, see [Date functions](/bigquery/docs/reference/standard-sql/date_functions). |
| [`PARSE_DATETIME`](/bigquery/docs/reference/standard-sql/datetime_functions#parse_datetime) | Converts a `STRING` value to a `DATETIME` value.  For more information, see [Datetime functions](/bigquery/docs/reference/standard-sql/datetime_functions). |
| [`PARSE_JSON`](/bigquery/docs/reference/standard-sql/json_functions#parse_json) | Converts a JSON-formatted `STRING` value to a `JSON` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`PARSE_NUMERIC`](/bigquery/docs/reference/standard-sql/conversion_functions#parse_numeric) | Converts a `STRING` value to a `NUMERIC` value. |
| [`PARSE_TIME`](/bigquery/docs/reference/standard-sql/time_functions#parse_time) | Converts a `STRING` value to a `TIME` value.  For more information, see [Time functions](/bigquery/docs/reference/standard-sql/time_functions). |
| [`PARSE_TIMESTAMP`](/bigquery/docs/reference/standard-sql/timestamp_functions#parse_timestamp) | Converts a `STRING` value to a `TIMESTAMP` value.  For more information, see [Timestamp functions](/bigquery/docs/reference/standard-sql/timestamp_functions). |
| [`SAFE_CAST`](/bigquery/docs/reference/standard-sql/conversion_functions#safe_casting) | Similar to the `CAST` function, but returns `NULL` when a runtime error is produced. |
| [`SAFE_CONVERT_BYTES_TO_STRING`](/bigquery/docs/reference/standard-sql/string_functions#safe_convert_bytes_to_string) | Converts a `BYTES` value to a `STRING` value and replace any invalid UTF-8 characters with the Unicode replacement character, `U+FFFD`.  For more information, see [String functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`STRING` (JSON)](/bigquery/docs/reference/standard-sql/json_functions#string_for_json) | Converts a JSON string to a SQL `STRING` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`STRING` (Timestamp)](/bigquery/docs/reference/standard-sql/timestamp_functions#string) | Converts a `TIMESTAMP` value to a `STRING` value.  For more information, see [Timestamp functions](/bigquery/docs/reference/standard-sql/timestamp_functions). |
| [`TIMESTAMP_MICROS`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_micros) | Converts the number of microseconds since 1970-01-01 00:00:00 UTC to a `TIMESTAMP`.  For more information, see [Timestamp functions](/bigquery/docs/reference/standard-sql/timestamp_functions). |
| [`TIMESTAMP_MILLIS`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_millis) | Converts the number of milliseconds since 1970-01-01 00:00:00 UTC to a `TIMESTAMP`.  For more information, see [Timestamp functions](/bigquery/docs/reference/standard-sql/timestamp_functions). |
| [`TIMESTAMP_SECONDS`](/bigquery/docs/reference/standard-sql/timestamp_functions#timestamp_seconds) | Converts the number of seconds since 1970-01-01 00:00:00 UTC to a `TIMESTAMP`.  For more information, see [Timestamp functions](/bigquery/docs/reference/standard-sql/timestamp_functions). |
| [`TO_BASE32`](/bigquery/docs/reference/standard-sql/string_functions#to_base32) | Converts a `BYTES` value to a base32-encoded `STRING` value.  For more information, see [String functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`TO_BASE64`](/bigquery/docs/reference/standard-sql/string_functions#to_base64) | Converts a `BYTES` value to a base64-encoded `STRING` value.  For more information, see [String functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`TO_CODE_POINTS`](/bigquery/docs/reference/standard-sql/string_functions#to_code_points) | Converts a `STRING` or `BYTES` value into an array of extended ASCII code points.  For more information, see [String functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`TO_HEX`](/bigquery/docs/reference/standard-sql/string_functions#to_hex) | Converts a `BYTES` value to a hexadecimal `STRING` value.  For more information, see [String functions](/bigquery/docs/reference/standard-sql/string_functions). |
| [`TO_JSON`](/bigquery/docs/reference/standard-sql/json_functions#to_json) | Converts a SQL value to a JSON value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`TO_JSON_STRING`](/bigquery/docs/reference/standard-sql/json_functions#to_json_string) | Converts a SQL value to a JSON-formatted `STRING` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`UNIX_DATE`](/bigquery/docs/reference/standard-sql/date_functions#unix_date) | Converts a `DATE` value to the number of days since 1970-01-01.  For more information, see [Date functions](/bigquery/docs/reference/standard-sql/date_functions). |
| [`UNIX_MICROS`](/bigquery/docs/reference/standard-sql/timestamp_functions#unix_micros) | Converts a `TIMESTAMP` value to the number of microseconds since 1970-01-01 00:00:00 UTC.  For more information, see [Timestamp functions](/bigquery/docs/reference/standard-sql/timestamp_functions). |
| [`UNIX_MILLIS`](/bigquery/docs/reference/standard-sql/timestamp_functions#unix_millis) | Converts a `TIMESTAMP` value to the number of milliseconds since 1970-01-01 00:00:00 UTC.  For more information, see [Timestamp functions](/bigquery/docs/reference/standard-sql/timestamp_functions). |
| [`UNIX_SECONDS`](/bigquery/docs/reference/standard-sql/timestamp_functions#unix_seconds) | Converts a `TIMESTAMP` value to the number of seconds since 1970-01-01 00:00:00 UTC.  For more information, see [Timestamp functions](/bigquery/docs/reference/standard-sql/timestamp_functions). |

## `CAST`

```
CAST(expression AS typename [format_clause])
```

**Description**

Cast syntax is used in a query to indicate that the result type of an
expression should be converted to some other type.

When using `CAST`, a query can fail if GoogleSQL is unable to perform
the cast. If you want to protect your queries from these types of errors, you
can use [SAFE\_CAST](#safe_casting).

Casts between supported types that don't successfully map from the original
value to the target domain produce runtime errors. For example, casting
`BYTES` to `STRING` where the byte sequence isn't valid UTF-8 results in a
runtime error.

Some casts can include a [format clause](/bigquery/docs/reference/standard-sql/format-elements#formatting_syntax), which provides
instructions for how to conduct the
cast. For example, you could
instruct a cast to convert a sequence of bytes to a BASE64-encoded string
instead of a UTF-8-encoded string.

The structure of the format clause is unique to each type of cast and more
information is available in the section for that cast.

**Examples**

The following query results in `"true"` if `x` is `1`, `"false"` for any other
non-`NULL` value, and `NULL` if `x` is `NULL`.

```
CAST(x=1 AS STRING)
```

### CAST AS ARRAY

```
CAST(expression AS ARRAY<element_type>)
```

**Description**

GoogleSQL supports [casting](#cast) to `ARRAY`. The
`expression` parameter can represent an expression for these data types:

* `ARRAY`

**Conversion rules**

| From | To | Rule(s) when casting `x` |
| --- | --- | --- |
| `ARRAY` | `ARRAY` | Must be the exact same array type. |
| `NULL` | `ARRAY` | Casts a `NULL` value to a specific type of array. For example, `CAST(NULL AS ARRAY<FLOAT64>)` returns a `NULL` literal of type `ARRAY<FLOAT64>`. |

### CAST AS BIGNUMERIC

```
CAST(expression AS BIGNUMERIC)
```

**Description**

GoogleSQL supports [casting](#cast) to `BIGNUMERIC`. The
`expression` parameter can represent an expression for these data types:

* `INT64`
* `FLOAT64`
* `NUMERIC`
* `BIGNUMERIC`
* `STRING`

**Conversion rules**

| From | To | Rule(s) when casting `x` |
| --- | --- | --- |
| FLOAT64 | `BIGNUMERIC` | The floating point number will round [half away from zero](https://en.wikipedia.org/wiki/Rounding#Round_half_away_from_zero). Casting a `NaN`, `+inf` or `-inf` will return an error. Casting a value outside the range of `BIGNUMERIC` returns an overflow error. |
| `STRING` | `BIGNUMERIC` | The numeric literal contained in the string must not exceed the maximum precision or range of the `BIGNUMERIC` type, or an error will occur. If the number of digits after the decimal point exceeds 38, then the resulting `BIGNUMERIC` value will round [half away from zero](https://en.wikipedia.org/wiki/Rounding#Round_half_away_from_zero) to have 38 digits after the decimal point. |

### CAST AS BOOL

```
CAST(expression AS BOOL)
```

**Description**

GoogleSQL supports [casting](#cast) to `BOOL`. The
`expression` parameter can represent an expression for these data types:

* `INT64`
* `BOOL`
* `STRING`

**Conversion rules**

| From | To | Rule(s) when casting `x` |
| --- | --- | --- |
| INT64 | `BOOL` | Returns `FALSE` if `x` is `0`, `TRUE` otherwise. |
| `STRING` | `BOOL` | Returns `TRUE` if `x` is `"true"` and `FALSE` if `x` is `"false"`  All other values of `x` are invalid and throw an error instead of casting to a boolean.  A string is case-insensitive when converting to a boolean. |

### CAST AS BYTES

```
CAST(expression AS BYTES [format_clause])
```

**Description**

GoogleSQL supports [casting](#cast) to `BYTES`. The
`expression` parameter can represent an expression for these data types:

* `BYTES`
* `STRING`

**Format clause**

When an expression of one type is cast to another type, you can use the
[format clause](/bigquery/docs/reference/standard-sql/format-elements#formatting_syntax) to provide instructions for how to conduct
the cast. You can use the format clause in this section if `expression` is a
`STRING`.

* [Format string as bytes](/bigquery/docs/reference/standard-sql/format-elements#format_string_as_bytes)

**Conversion rules**

| From | To | Rule(s) when casting `x` |
| --- | --- | --- |
| `STRING` | `BYTES` | Strings are cast to bytes using UTF-8 encoding. For example, the string "©", when cast to bytes, would become a 2-byte sequence with the hex values C2 and A9. |

### CAST AS DATE

```
CAST(expression AS DATE [format_clause])
```

**Description**

GoogleSQL supports [casting](#cast) to `DATE`. The `expression`
parameter can represent an expression for these data types:

* `STRING`
* `DATETIME`
* `TIMESTAMP`

**Format clause**

When an expression of one type is cast to another type, you can use the
[format clause](/bigquery/docs/reference/standard-sql/format-elements#formatting_syntax) to provide instructions for how to conduct
the cast. You can use the format clause in this section if `expression` is a
`STRING`.

* [Format string as date and time](/bigquery/docs/reference/standard-sql/format-elements#format_string_as_datetime)

**Conversion rules**

| From | To | Rule(s) when casting `x` |
| --- | --- | --- |
| `STRING` | `DATE` | When casting from string to date, the string must conform to the supported date literal format, and is independent of time zone. If the string expression is invalid or represents a date that's outside of the supported min/max range, then an error is produced. |
| `TIMESTAMP` | `DATE` | Casting from a timestamp to date effectively truncates the timestamp as of the default time zone. |

### CAST AS DATETIME

```
CAST(expression AS DATETIME [format_clause])
```

**Description**

GoogleSQL supports [casting](#cast) to `DATETIME`. The
`expression` parameter can represent an expression for these data types:

* `STRING`
* `DATETIME`
* `TIMESTAMP`

**Format clause**

When an expression of one type is cast to another type, you can use the
[format clause](/bigquery/docs/reference/standard-sql/format-elements#formatting_syntax) to provide instructions for how to conduct
the cast. You can use the format clause in this section if `expression` is a
`STRING`.

* [Format string as date and time](/bigquery/docs/reference/standard-sql/format-elements#format_string_as_datetime)

**Conversion rules**

| From | To | Rule(s) when casting `x` |
| --- | --- | --- |
| `STRING` | `DATETIME` | When casting from string to datetime, the string must conform to the supported datetime literal format, and is independent of time zone. If the string expression is invalid or represents a datetime that's outside of the supported min/max range, then an error is produced. |
| `TIMESTAMP` | `DATETIME` | Casting from a timestamp to datetime effectively truncates the timestamp as of the default time zone. |

### CAST AS FLOAT64

```
CAST(expression AS FLOAT64)
```

**Description**

GoogleSQL supports [casting](#cast) to floating point types.
The `expression` parameter can represent an expression for these data types:

* `INT64`
* `FLOAT64`
* `NUMERIC`
* `BIGNUMERIC`
* `STRING`

**Conversion rules**

| From | To | Rule(s) when casting `x` |
| --- | --- | --- |
| INT64 | FLOAT64 | Returns a close but potentially not exact floating point value. |
| `NUMERIC` | FLOAT64 | `NUMERIC` will convert to the closest floating point number with a possible loss of precision. |
| `BIGNUMERIC` | FLOAT64 | `BIGNUMERIC` will convert to the closest floating point number with a possible loss of precision. |
| `STRING` | FLOAT64 | Returns `x` as a floating point value, interpreting it as having the same form as a valid floating point literal. Also supports casts from `"[+,-]inf"` to `[,-]Infinity`, `"[+,-]infinity"` to `[,-]Infinity`, and `"[+,-]nan"` to `NaN`. Conversions are case-insensitive. |

### CAST AS INT64

```
CAST(expression AS INT64)
```

**Description**

GoogleSQL supports [casting](#cast) to integer types.
The `expression` parameter can represent an expression for these data types:

* `INT64`
* `FLOAT64`
* `NUMERIC`
* `BIGNUMERIC`
* `BOOL`
* `STRING`

**Conversion rules**

| From | To | Rule(s) when casting `x` |
| --- | --- | --- |
| FLOAT64 | INT64 | Returns the closest integer value.  Halfway cases such as 1.5 or -0.5 round away from zero. |
| `BOOL` | INT64 | Returns `1` if `x` is `TRUE`, `0` otherwise. |
| `STRING` | INT64 |  |