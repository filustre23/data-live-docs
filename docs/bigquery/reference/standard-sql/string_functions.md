* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# String functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports string functions.
These string functions work on two different values:
`STRING` and `BYTES` data types. `STRING` values must be well-formed UTF-8.

Functions that return position values, such as [STRPOS](#strpos),
encode those positions as `INT64`. The value `1`
refers to the first character (or byte), `2` refers to the second, and so on.
The value `0` indicates an invalid position. When working on `STRING` types, the
returned positions refer to character positions.

All string comparisons are done byte-by-byte, without regard to Unicode
canonical equivalence.

## Function list

| Name | Summary |
| --- | --- |
| [`ARRAY_TO_STRING`](/bigquery/docs/reference/standard-sql/array_functions#array_to_string) | Produces a concatenation of the elements in an array as a `STRING` value.  For more information, see [Array functions](/bigquery/docs/reference/standard-sql/array_functions). |
| [`ASCII`](/bigquery/docs/reference/standard-sql/string_functions#ascii) | Gets the ASCII code for the first character or byte in a `STRING` or `BYTES` value. |
| [`BYTE_LENGTH`](/bigquery/docs/reference/standard-sql/string_functions#byte_length) | Gets the number of `BYTES` in a `STRING` or `BYTES` value. |
| [`CHAR_LENGTH`](/bigquery/docs/reference/standard-sql/string_functions#char_length) | Gets the number of characters in a `STRING` value. |
| [`CHARACTER_LENGTH`](/bigquery/docs/reference/standard-sql/string_functions#character_length) | Synonym for `CHAR_LENGTH`. |
| [`CHR`](/bigquery/docs/reference/standard-sql/string_functions#chr) | Converts a Unicode code point to a character. |
| [`CODE_POINTS_TO_BYTES`](/bigquery/docs/reference/standard-sql/string_functions#code_points_to_bytes) | Converts an array of extended ASCII code points to a `BYTES` value. |
| [`CODE_POINTS_TO_STRING`](/bigquery/docs/reference/standard-sql/string_functions#code_points_to_string) | Converts an array of extended ASCII code points to a `STRING` value. |
| [`COLLATE`](/bigquery/docs/reference/standard-sql/string_functions#collate) | Combines a `STRING` value and a collation specification into a collation specification-supported `STRING` value. |
| [`CONCAT`](/bigquery/docs/reference/standard-sql/string_functions#concat) | Concatenates one or more `STRING` or `BYTES` values into a single result. |
| [`CONTAINS_SUBSTR`](/bigquery/docs/reference/standard-sql/string_functions#contains_substr) | Performs a normalized, case-insensitive search to see if a value exists as a substring in an expression. |
| [`EDIT_DISTANCE`](/bigquery/docs/reference/standard-sql/string_functions#edit_distance) | Computes the Levenshtein distance between two `STRING` or `BYTES` values. |
| [`ENDS_WITH`](/bigquery/docs/reference/standard-sql/string_functions#ends_with) | Checks if a `STRING` or `BYTES` value is the suffix of another value. |
| [`FORMAT`](/bigquery/docs/reference/standard-sql/string_functions#format_string) | Formats data and produces the results as a `STRING` value. |
| [`FROM_BASE32`](/bigquery/docs/reference/standard-sql/string_functions#from_base32) | Converts a base32-encoded `STRING` value into a `BYTES` value. |
| [`FROM_BASE64`](/bigquery/docs/reference/standard-sql/string_functions#from_base64) | Converts a base64-encoded `STRING` value into a `BYTES` value. |
| [`FROM_HEX`](/bigquery/docs/reference/standard-sql/string_functions#from_hex) | Converts a hexadecimal-encoded `STRING` value into a `BYTES` value. |
| [`INITCAP`](/bigquery/docs/reference/standard-sql/string_functions#initcap) | Formats a `STRING` as proper case, which means that the first character in each word is uppercase and all other characters are lowercase. |
| [`INSTR`](/bigquery/docs/reference/standard-sql/string_functions#instr) | Finds the position of a subvalue inside another value, optionally starting the search at a given offset or occurrence. |
| [`LAX_STRING`](/bigquery/docs/reference/standard-sql/json_functions#lax_string) | Attempts to convert a JSON value to a SQL `STRING` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`LEFT`](/bigquery/docs/reference/standard-sql/string_functions#left) | Gets the specified leftmost portion from a `STRING` or `BYTES` value. |
| [`LENGTH`](/bigquery/docs/reference/standard-sql/string_functions#length) | Gets the length of a `STRING` or `BYTES` value. |
| [`LOWER`](/bigquery/docs/reference/standard-sql/string_functions#lower) | Formats alphabetic characters in a `STRING` value as lowercase.    Formats ASCII characters in a `BYTES` value as lowercase. |
| [`LPAD`](/bigquery/docs/reference/standard-sql/string_functions#lpad) | Prepends a `STRING` or `BYTES` value with a pattern. |
| [`LTRIM`](/bigquery/docs/reference/standard-sql/string_functions#ltrim) | Identical to the `TRIM` function, but only removes leading characters. |
| [`NORMALIZE`](/bigquery/docs/reference/standard-sql/string_functions#normalize) | Case-sensitively normalizes the characters in a `STRING` value. |
| [`NORMALIZE_AND_CASEFOLD`](/bigquery/docs/reference/standard-sql/string_functions#normalize_and_casefold) | Case-insensitively normalizes the characters in a `STRING` value. |
| [`OCTET_LENGTH`](/bigquery/docs/reference/standard-sql/string_functions#octet_length) | Alias for `BYTE_LENGTH`. |
| [`REGEXP_CONTAINS`](/bigquery/docs/reference/standard-sql/string_functions#regexp_contains) | Checks if a value is a partial match for a regular expression. |
| [`REGEXP_EXTRACT`](/bigquery/docs/reference/standard-sql/string_functions#regexp_extract) | Produces a substring that matches a regular expression. |
| [`REGEXP_EXTRACT_ALL`](/bigquery/docs/reference/standard-sql/string_functions#regexp_extract_all) | Produces an array of all substrings that match a regular expression. |
| [`REGEXP_INSTR`](/bigquery/docs/reference/standard-sql/string_functions#regexp_instr) | Finds the position of a regular expression match in a value, optionally starting the search at a given offset or occurrence. |
| [`REGEXP_REPLACE`](/bigquery/docs/reference/standard-sql/string_functions#regexp_replace) | Produces a `STRING` value where all substrings that match a regular expression are replaced with a specified value. |
| [`REGEXP_SUBSTR`](/bigquery/docs/reference/standard-sql/string_functions#regexp_substr) | Synonym for `REGEXP_EXTRACT`. |
| [`REPEAT`](/bigquery/docs/reference/standard-sql/string_functions#repeat) | Produces a `STRING` or `BYTES` value that consists of an original value, repeated. |
| [`REPLACE`](/bigquery/docs/reference/standard-sql/string_functions#replace) | Replaces all occurrences of a pattern with another pattern in a `STRING` or `BYTES` value. |
| [`REVERSE`](/bigquery/docs/reference/standard-sql/string_functions#reverse) | Reverses a `STRING` or `BYTES` value. |
| [`RIGHT`](/bigquery/docs/reference/standard-sql/string_functions#right) | Gets the specified rightmost portion from a `STRING` or `BYTES` value. |
| [`RPAD`](/bigquery/docs/reference/standard-sql/string_functions#rpad) | Appends a `STRING` or `BYTES` value with a pattern. |
| [`RTRIM`](/bigquery/docs/reference/standard-sql/string_functions#rtrim) | Identical to the `TRIM` function, but only removes trailing characters. |
| [`SAFE_CONVERT_BYTES_TO_STRING`](/bigquery/docs/reference/standard-sql/string_functions#safe_convert_bytes_to_string) | Converts a `BYTES` value to a `STRING` value and replace any invalid UTF-8 characters with the Unicode replacement character, `U+FFFD`. |
| [`SOUNDEX`](/bigquery/docs/reference/standard-sql/string_functions#soundex) | Gets the Soundex codes for words in a `STRING` value. |
| [`SPLIT`](/bigquery/docs/reference/standard-sql/string_functions#split) | Splits a `STRING` or `BYTES` value, using a delimiter. |
| [`STARTS_WITH`](/bigquery/docs/reference/standard-sql/string_functions#starts_with) | Checks if a `STRING` or `BYTES` value is a prefix of another value. |
| [`STRING` (JSON)](/bigquery/docs/reference/standard-sql/json_functions#string_for_json) | Converts a JSON string to a SQL `STRING` value.  For more information, see [JSON functions](/bigquery/docs/reference/standard-sql/json_functions). |
| [`STRING` (Timestamp)](/bigquery/docs/reference/standard-sql/timestamp_functions#string) | Converts a `TIMESTAMP` value to a `STRING` value.  For more information, see [Timestamp functions](/bigquery/docs/reference/standard-sql/timestamp_functions). |
| [`STRING_AGG`](/bigquery/docs/reference/standard-sql/aggregate_functions#string_agg) | Concatenates non-`NULL` `STRING` or `BYTES` values.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |
| [`STRPOS`](/bigquery/docs/reference/standard-sql/string_functions#strpos) | Finds the position of the first occurrence of a subvalue inside another value. |
| [`SUBSTR`](/bigquery/docs/reference/standard-sql/string_functions#substr) | Gets a portion of a `STRING` or `BYTES` value. |
| [`SUBSTRING`](/bigquery/docs/reference/standard-sql/string_functions#substring) | Alias for `SUBSTR` |
| [`TO_BASE32`](/bigquery/docs/reference/standard-sql/string_functions#to_base32) | Converts a `BYTES` value to a base32-encoded `STRING` value. |
| [`TO_BASE64`](/bigquery/docs/reference/standard-sql/string_functions#to_base64) | Converts a `BYTES` value to a base64-encoded `STRING` value. |
| [`TO_CODE_POINTS`](/bigquery/docs/reference/standard-sql/string_functions#to_code_points) | Converts a `STRING` or `BYTES` value into an array of extended ASCII code points. |
| [`TO_HEX`](/bigquery/docs/reference/standard-sql/string_functions#to_hex) | Converts a `BYTES` value to a hexadecimal `STRING` value. |
| [`TRANSLATE`](/bigquery/docs/reference/standard-sql/string_functions#translate) | Within a value, replaces each source character with the corresponding target character. |
| [`TRIM`](/bigquery/docs/reference/standard-sql/string_functions#trim) | Removes the specified leading and trailing Unicode code points or bytes from a `STRING` or `BYTES` value. |
| [`UNICODE`](/bigquery/docs/reference/standard-sql/string_functions#unicode) | Gets the Unicode code point for the first character in a value. |
| [`UPPER`](/bigquery/docs/reference/standard-sql/string_functions#upper) | Formats alphabetic characters in a `STRING` value as uppercase.    Formats ASCII characters in a `BYTES` value as uppercase. |

## `ASCII`

```
ASCII(value)
```

**Description**

Returns the ASCII code for the first character or byte in `value`. Returns
`0` if `value` is empty or the ASCII code is `0` for the first character
or byte.

**Return type**

`INT64`

**Examples**

```
SELECT ASCII('abcd') as A, ASCII('a') as B, ASCII('') as C, ASCII(NULL) as D;

/*-------+-------+-------+-------+
 | A     | B     | C     | D     |
 +-------+-------+-------+-------+
 | 97    | 97    | 0     | NULL  |
 +-------+-------+-------+-------*/
```

## `BYTE_LENGTH`

```
BYTE_LENGTH(value)
```

**Description**

Gets the number of `BYTES` in a `STRING` or `BYTES` value,
regardless of whether the value is a `STRING` or `BYTES` type.

**Return type**

`INT64`

**Examples**

```
SELECT BYTE_LENGTH('абвгд') AS string_example;

/*----------------+
 | string_example |
 +----------------+
 | 10             |
 +----------------*/
```

```
SELECT BYTE_LENGTH(b'абвгд') AS bytes_example;

/*----------------+
 | bytes_example  |
 +----------------+
 | 10             |
 +----------------*/
```

## `CHAR_LENGTH`

```
CHAR_LENGTH(value)
```

**Description**

Gets the number of characters in a `STRING` value.

**Return type**

`INT64`

**Examples**

```
SELECT CHAR_LENGTH('абвгд') AS char_length;

/*-------------+
 | char_length |
 +-------------+
 | 5           |
 +------------ */
```

## `CHARACTER_LENGTH`

```
CHARACTER_LENGTH(value)
```

**Description**

Synonym for [CHAR\_LENGTH](#char_length).

**Return type**

`INT64`

**Examples**

```
SELECT
  'абвгд' AS characters,
  CHARACTER_LENGTH('абвгд') AS char_length_example

/*------------+---------------------+
 | characters | char_length_example |
 +------------+---------------------+
 | абвгд      |                   5 |
 +------------+---------------------*/
```

## `CHR`

```
CHR(value)
```

**Description**

Takes a Unicode [code point](https://en.wikipedia.org/wiki/Code_point) and returns
the character that matches the code point. Each valid code point should fall
within the range of [0, 0xD7FF] and [0xE000, 0x10FFFF]. Returns an empty string
if the code point is `0`. If an invalid Unicode code point is specified, an
error is returned.

To work with an array of Unicode code points, see
[`CODE_POINTS_TO_STRING`](#code_points_to_string)

**Return type**

`STRING`

**Examples**

```
SELECT CHR(65) AS A, CHR(255) AS B, CHR(513) AS C, CHR(1024)  AS D;

/*-------+-------+-------+-------+
 | A     | B     | C     | D     |
 +-------+-------+-------+-------+
 | A     | ÿ     | ȁ     | Ѐ     |
 +-------+-------+-------+-------*/
```

```
SELECT CHR(97) AS A, CHR(0xF9B5) AS B, CHR(0) AS C, CHR(NULL) AS D;

/*-------+-------+-------+-------+
 | A     | B     | C     | D     |
 +-------+-------+-------+-------+
 | a     | 例    |       | NULL  |
 +-------+-------+-------+-------*/
```

## `CODE_POINTS_TO_BYTES`

```
CODE_POINTS_TO_BYTES(ascii_code_points)
```

**Description**

Takes an array of extended ASCII
[code points](https://en.wikipedia.org/wiki/Code_point)
as `ARRAY<INT64>` and returns `BYTES`.

To convert from `BYTES` to an array of code points, see
[TO\_CODE\_POINTS](#to_code_points).

**Return type**

`BYTES`

**Examples**

The following is a basic example using `CODE_POINTS_TO_BYTES`.

```
SELECT CODE_POINTS_TO_BYTES([65, 98, 67, 100]) AS bytes;

-- Note that the result of CODE_POINTS_TO_BYTES is of type BYTES, displayed as a base64-encoded string.
-- In BYTES format, b'AbCd' is the result.
/*----------+
 | bytes    |
 +----------+
 | QWJDZA== |
 +----------*/
```

The following example uses a rotate-by-13 places (ROT13) algorithm to encode a
string.

```
SELECT CODE_POINTS_TO_BYTES(ARRAY_AGG(
  (SELECT
      CASE
        WHEN chr BETWEEN b'a' and b'z'
          THEN TO_CODE_POINTS(b'a')[offset(0)] +
            MOD(code+13-TO_CODE_POINTS(b'a')[offset(0)],26)
        WHEN chr BETWEEN b'A' and b'Z'
          THEN TO_CODE_POINTS(b'A')[offset(0)] +
            MOD(code+13-TO_CODE_POINTS(b'A')[offset(0)],26)
        ELSE code
      END
   FROM
     (SELECT code, CODE_POINTS_TO_BYTES([code]) chr)
  ) ORDER BY OFFSET)) AS encoded_string
FROM UNNEST(TO_CODE_POINTS(b'Test String!')) code WITH OFFSET;

-- Note that the result of CODE_POINTS_TO_BYTES is of type BYTES, displayed as a base64-encoded string.
-- In BYTES format, b'Grfg Fgevat!' is the result.
/*------------------+
 | encoded_string   |
 +------------------+
 | R3JmZyBGZ2V2YXQh |
 +------------------*/
```

## `CODE_POINTS_TO_STRING`

```
CODE_POINTS_TO_STRING(unicode_code_points)
```

**Description**

Takes an array of Unicode [code points](https://en.wikipedia.org/wiki/Code_point)
as `ARRAY<INT64>` and returns a `STRING`.

To convert from a string to an array of code points, see
[TO\_CODE\_POINTS](#to_code_points).

**Return type**

`STRING`

**Examples**

The following are basic examples using `CODE_POINTS_TO_STRING`.

```
SELECT CODE_POINTS_TO_STRING([65, 255, 513, 1024]) AS string;

/*--------+
 | string |
 +--------+
 | AÿȁЀ   |
 +--------*/
```

```
SELECT CODE_POINTS_TO_STRING([97, 0, 0xF9B5]) AS string;

/*--------+
 | string |
 +--------+
 | a例    |
 +--------*/
```

```
SELECT CODE_POINTS_TO_STRING([65, 255, NULL, 1024]) AS string;

/*--------+
 | string |
 +--------+
 | NULL   |
 +--------*/
```

The following example computes the frequency of letters in a set of words.

```
WITH Words AS (
  SELECT word
  FROM UNNEST(['foo', 'bar', 'baz', 'giraffe', 'llama']) AS word
)
SELECT
  CODE_POINTS_TO_STRING([code_point]) AS letter,
  COUNT(*) AS letter_count
FROM Words,
  UNNEST(TO_CODE_POINTS(word)) AS code_point
GROUP BY 1
ORDER BY 2 DESC;

/*--------+--------------+
 | letter | letter_count |
 +--------+--------------+
 | a      | 5            |
 | f      | 3            |
 | r      | 2            |
 | b      | 2            |
 | l      | 2            |
 | o      | 2            |
 | g      | 1            |
 | z      | 1            |
 | e      | 1            |
 | m      | 1            |
 | i      | 1            |
 +--------+--------------*/
```

## `COLLATE`

```
COLLATE(value, collate_specification)
```

Takes a `STRING` and a [collation specification](/bigquery/docs/reference/standard-sql/collation-concepts#collate_spec_details). Returns
a `STRING` with a collation specification. If `collate_specification` is empty,
returns a value with collation removed from the `STRING`.

The collation specification defines how the resulting `STRING` can be compared
and sorted. To learn more, see
[Collation](/bigquery/docs/reference/standard-sql/collation-concepts).

* `collation_specification` must be a string literal, otherwise an error is
  thrown.
* Returns `NULL` if `value` is `NULL`.

**Return type**

`STRING`

**Examples**

In this example, the weight of `a` is less than the weight of `Z`. This
is because the collate specification, `und:ci` assigns more weight to `Z`.

```
WITH Words AS (
  SELECT
    COLLATE('a', 'und:ci') AS char1,
    COLLATE('Z', 'und:ci') AS char2
)
SELECT ( Words.char1 < Words.char2 ) AS a_less_than_Z
FROM Words;

/*----------------+
 | a_less_than_Z  |
 +----------------+
 | TRUE           |
 +----------------*/
```

In this example, the weight of `a` is greater than the weight of `Z`. This
is because the default collate specification assigns more weight to `a`.

```
WITH Words AS (
  SELECT
    'a' AS char1,
    'Z' AS char2
)
SELECT ( Words.char1 < Words.char2 ) AS a_less_than_Z
FROM Words;

/*----------------+
 | a_less_than_Z  |
 +----------------+
 | FALSE          |
 +----------------*/
```

## `CONCAT`

```
CONCAT(value1[, ...])
```

**Description**

Concatenates one or more values into a single result. All values must be
`BYTES` or data types that can be cast to `STRING`.

The function returns `NULL` if any input argument is `NULL`.

**Note:** You can also use the
[|| concatenation operator](/bigquery/docs/reference/standard-sql/operators) to concatenate
values into a string.

**Return type**

`STRING` or `BYTES`

**Examples**

```
SELECT CONCAT('T.P.', ' ', 'Bar') as author;

/*---------------------+
 | author              |
 +---------------------+
 | T.P. Bar            |
 +---------------------*/
```

```
SELECT CONCAT('Summer', ' ', 1923) as release_date;

/*---------------------+
 | release_date        |
 +---------------------+
 | Summer 1923         |
 +---------------------*/
```

```
With Employees AS
  (SELECT
    'John' AS first_name,
    'Doe' AS last_name
  UNION ALL
  SELECT
    'Jane' AS first_name,
    'Smith' AS last_name
  UNION ALL
  SELECT
    'Joe' AS first_name,
    'Jackson' AS last_name)

SELECT
  CONCAT(first_name, ' ',
```