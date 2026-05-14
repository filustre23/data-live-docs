* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# JSON functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following functions, which can retrieve and
transform JSON data.

## Categories

The JSON functions are grouped into the following categories based on their
behavior:

| Category | Functions | Description |
| --- | --- | --- |
| Standard extractors | [`JSON_QUERY`](#json_query)  [`JSON_VALUE`](#json_value)  [`JSON_QUERY_ARRAY`](#json_query_array)  [`JSON_VALUE_ARRAY`](#json_value_array) | Functions that extract JSON data. |
| Legacy extractors | [`JSON_EXTRACT`](#json_extract)  [`JSON_EXTRACT_SCALAR`](#json_extract_scalar)  [`JSON_EXTRACT_ARRAY`](#json_extract_array)  [`JSON_EXTRACT_STRING_ARRAY`](#json_extract_string_array) | Functions that extract JSON data.  While these functions are supported by GoogleSQL, we recommend using the [standard extractor functions](#extractors). |
| Lax converters | [`LAX_BOOL`](#lax_bool)  [`LAX_FLOAT64`](#lax_double)  [`LAX_INT64`](#lax_int64)  [`LAX_STRING`](#lax_string) | Functions that flexibly convert a JSON value to a SQL value without returning errors. |
| Converters | [`BOOL`](#bool_for_json)  [`FLOAT64`](#double_for_json)  [`INT64`](#int64_for_json)  [`STRING`](#string_for_json) | Functions that convert a JSON value to a SQL value. |
| Other converters | [`PARSE_JSON`](#parse_json)  [`TO_JSON`](#to_json)  [`TO_JSON_STRING`](#to_json_string) | Other conversion functions from or to JSON. |
| Constructors | [`JSON_ARRAY`](#json_array)  [`JSON_OBJECT`](#json_object) | Functions that create JSON. |
| Mutators | [`JSON_ARRAY_APPEND`](#json_array_append)  [`JSON_ARRAY_INSERT`](#json_array_insert)  [`JSON_REMOVE`](#json_remove)  [`JSON_SET`](#json_set)  [`JSON_STRIP_NULLS`](#json_strip_nulls) | Functions that mutate existing JSON. |
| Accessors | [`JSON_KEYS`](#json_keys)  [`JSON_TYPE`](#json_type) | Functions that provide access to JSON properties. |
| Transformers | [`JSON_FLATTEN`](#json_flatten) | Functions that apply a transformation to a JSON value. |

## Function list

| Name | Summary |
| --- | --- |
| [`BOOL`](/bigquery/docs/reference/standard-sql/json_functions#bool_for_json) | Converts a JSON boolean to a SQL `BOOL` value. |
| [`FLOAT64`](/bigquery/docs/reference/standard-sql/json_functions#double_for_json) | Converts a JSON number to a SQL `FLOAT64` value. |
| [`INT64`](/bigquery/docs/reference/standard-sql/json_functions#int64_for_json) | Converts a JSON number to a SQL `INT64` value. |
| [`JSON_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_array) | Creates a JSON array. |
| [`JSON_ARRAY_APPEND`](/bigquery/docs/reference/standard-sql/json_functions#json_array_append) | Appends JSON data to the end of a JSON array. |
| [`JSON_ARRAY_INSERT`](/bigquery/docs/reference/standard-sql/json_functions#json_array_insert) | Inserts JSON data into a JSON array. |
| [`JSON_EXTRACT`](/bigquery/docs/reference/standard-sql/json_functions#json_extract) | (Deprecated) Extracts a JSON value and converts it to a SQL JSON-formatted `STRING` or `JSON` value. |
| [`JSON_EXTRACT_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_extract_array) | (Deprecated) Extracts a JSON array and converts it to a SQL `ARRAY<JSON-formatted STRING>` or `ARRAY<JSON>` value. |
| [`JSON_EXTRACT_SCALAR`](/bigquery/docs/reference/standard-sql/json_functions#json_extract_scalar) | (Deprecated) Extracts a JSON scalar value and converts it to a SQL `STRING` value. |
| [`JSON_EXTRACT_STRING_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_extract_string_array) | (Deprecated) Extracts a JSON array of scalar values and converts it to a SQL `ARRAY<STRING>` value. |
| [`JSON_FLATTEN`](/bigquery/docs/reference/standard-sql/json_functions#json_flatten) | Produces a new SQL `ARRAY<JSON>` value containing all non-array values that are either directly in the input JSON value or children of one or more consecutively nested arrays in the input JSON value. |
| [`JSON_KEYS`](/bigquery/docs/reference/standard-sql/json_functions#json_keys) | Extracts unique JSON keys from a JSON expression. |
| [`JSON_OBJECT`](/bigquery/docs/reference/standard-sql/json_functions#json_object) | Creates a JSON object. |
| [`JSON_QUERY`](/bigquery/docs/reference/standard-sql/json_functions#json_query) | Extracts a JSON value and converts it to a SQL JSON-formatted `STRING` or `JSON` value. |
| [`JSON_QUERY_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_query_array) | Extracts a JSON array and converts it to a SQL `ARRAY<JSON-formatted STRING>` or `ARRAY<JSON>` value. |
| [`JSON_REMOVE`](/bigquery/docs/reference/standard-sql/json_functions#json_remove) | Produces JSON with the specified JSON data removed. |
| [`JSON_SET`](/bigquery/docs/reference/standard-sql/json_functions#json_set) | Inserts or replaces JSON data. |
| [`JSON_STRIP_NULLS`](/bigquery/docs/reference/standard-sql/json_functions#json_strip_nulls) | Removes JSON nulls from JSON objects and JSON arrays. |
| [`JSON_TYPE`](/bigquery/docs/reference/standard-sql/json_functions#json_type) | Gets the JSON type of the outermost JSON value and converts the name of this type to a SQL `STRING` value. |
| [`JSON_VALUE`](/bigquery/docs/reference/standard-sql/json_functions#json_value) | Extracts a JSON scalar value and converts it to a SQL `STRING` value. |
| [`JSON_VALUE_ARRAY`](/bigquery/docs/reference/standard-sql/json_functions#json_value_array) | Extracts a JSON array of scalar values and converts it to a SQL `ARRAY<STRING>` value. |
| [`LAX_BOOL`](/bigquery/docs/reference/standard-sql/json_functions#lax_bool) | Attempts to convert a JSON value to a SQL `BOOL` value. |
| [`LAX_FLOAT64`](/bigquery/docs/reference/standard-sql/json_functions#lax_double) | Attempts to convert a JSON value to a SQL `FLOAT64` value. |
| [`LAX_INT64`](/bigquery/docs/reference/standard-sql/json_functions#lax_int64) | Attempts to convert a JSON value to a SQL `INT64` value. |
| [`LAX_STRING`](/bigquery/docs/reference/standard-sql/json_functions#lax_string) | Attempts to convert a JSON value to a SQL `STRING` value. |
| [`PARSE_JSON`](/bigquery/docs/reference/standard-sql/json_functions#parse_json) | Converts a JSON-formatted `STRING` value to a `JSON` value. |
| [`STRING` (JSON)](/bigquery/docs/reference/standard-sql/json_functions#string_for_json) | Converts a JSON string to a SQL `STRING` value. |
| [`TO_JSON`](/bigquery/docs/reference/standard-sql/json_functions#to_json) | Converts a SQL value to a JSON value. |
| [`TO_JSON_STRING`](/bigquery/docs/reference/standard-sql/json_functions#to_json_string) | Converts a SQL value to a JSON-formatted `STRING` value. |

## `BOOL`

```
BOOL(json_expr)
```

**Description**

Converts a JSON boolean to a SQL `BOOL` value.

Arguments:

* `json_expr`: JSON. For example:

  ```
  JSON 'true'
  ```

  If the JSON value isn't a boolean, an error is produced. If the expression
  is SQL `NULL`, the function returns SQL `NULL`.

**Return type**

`BOOL`

**Examples**

```
SELECT BOOL(JSON 'true') AS vacancy;

/*---------+
 | vacancy |
 +---------+
 | true    |
 +---------*/
```

```
SELECT BOOL(JSON_QUERY(JSON '{"hotel class": "5-star", "vacancy": true}', "$.vacancy")) AS vacancy;

/*---------+
 | vacancy |
 +---------+
 | true    |
 +---------*/
```

The following examples show how invalid requests are handled:

```
-- An error is thrown if JSON isn't of type bool.
SELECT BOOL(JSON '123') AS result; -- Throws an error
SELECT BOOL(JSON 'null') AS result; -- Throws an error
SELECT SAFE.BOOL(JSON '123') AS result; -- Returns a SQL NULL
```

## `FLOAT64`

```
FLOAT64(
  json_expr
  [, wide_number_mode => { 'exact' | 'round' } ]
)
```

**Description**

Converts a JSON number to a SQL `FLOAT64` value.

Arguments:

* `json_expr`: JSON. For example:

  ```
  JSON '9.8'
  ```

  If the JSON value isn't a number, an error is produced. If the expression
  is a SQL `NULL`, the function returns SQL `NULL`.
* `wide_number_mode`: A named argument with a `STRING` value.
  Defines what happens with a number that can't be
  represented as a `FLOAT64` without loss of
  precision. This argument accepts one of the two case-sensitive values:

  + `exact`: The function fails if the result can't be represented as a
    `FLOAT64` without loss of precision.
  + `round` (default): The numeric value stored in JSON will be rounded to
    `FLOAT64`. If such rounding isn't possible,
    the function fails.

**Return type**

`FLOAT64`

**Examples**

```
SELECT FLOAT64(JSON '9.8') AS velocity;

/*----------+
 | velocity |
 +----------+
 | 9.8      |
 +----------*/
```

```
SELECT FLOAT64(JSON_QUERY(JSON '{"vo2_max": 39.1, "age": 18}', "$.vo2_max")) AS vo2_max;

/*---------+
 | vo2_max |
 +---------+
 | 39.1    |
 +---------*/
```

```
SELECT FLOAT64(JSON '18446744073709551615', wide_number_mode=>'round') as result;

/*------------------------+
 | result                 |
 +------------------------+
 | 1.8446744073709552e+19 |
 +------------------------*/
```

```
SELECT FLOAT64(JSON '18446744073709551615') as result;

/*------------------------+
 | result                 |
 +------------------------+
 | 1.8446744073709552e+19 |
 +------------------------*/
```

The following examples show how invalid requests are handled:

```
-- An error is thrown if JSON isn't of type FLOAT64.
SELECT FLOAT64(JSON '"strawberry"') AS result;
SELECT FLOAT64(JSON 'null') AS result;

-- An error is thrown because `wide_number_mode` is case-sensitive and not "exact" or "round".
SELECT FLOAT64(JSON '123.4', wide_number_mode=>'EXACT') as result;
SELECT FLOAT64(JSON '123.4', wide_number_mode=>'exac') as result;

-- An error is thrown because the number can't be converted to DOUBLE without loss of precision
SELECT FLOAT64(JSON '18446744073709551615', wide_number_mode=>'exact') as result;

-- Returns a SQL NULL
SELECT SAFE.FLOAT64(JSON '"strawberry"') AS result;
```

## `INT64`

```
INT64(json_expr)
```

**Description**

Converts a JSON number to a SQL `INT64` value.

Arguments:

* `json_expr`: JSON. For example:

  ```
  JSON '999'
  ```

  If the JSON value isn't a number, or the JSON number isn't in the SQL
  `INT64` domain, an error is produced. If the expression is SQL `NULL`, the
  function returns SQL `NULL`.

**Return type**

`INT64`

**Examples**

```
SELECT INT64(JSON '2005') AS flight_number;

/*---------------+
 | flight_number |
 +---------------+
 | 2005          |
 +---------------*/
```

```
SELECT INT64(JSON_QUERY(JSON '{"gate": "A4", "flight_number": 2005}', "$.flight_number")) AS flight_number;

/*---------------+
 | flight_number |
 +---------------+
 | 2005          |
 +---------------*/
```

```
SELECT INT64(JSON '10.0') AS score;

/*-------+
 | score |
 +-------+
 | 10    |
 +-------*/
```

The following examples show how invalid requests are handled:

```
-- An error is thrown if JSON isn't a number or can't be converted to a 64-bit integer.
SELECT INT64(JSON '10.1') AS result;  -- Throws an error
SELECT INT64(JSON '"strawberry"') AS result; -- Throws an error
SELECT INT64(JSON 'null') AS result; -- Throws an error
SELECT SAFE.INT64(JSON '"strawberry"') AS result;  -- Returns a SQL NULL
```

## `JSON_ARRAY`

```
JSON_ARRAY([value][, ...])
```

**Description**

Creates a JSON array from zero or more SQL values.

Arguments:

* `value`: A [JSON encoding-supported](#json_encodings) value to add
  to a JSON array.

**Return type**

`JSON`

**Examples**

The following query creates a JSON array with one value in it:

```
SELECT JSON_ARRAY(10) AS json_data

/*-----------+
 | json_data |
 +-----------+
 | [10]      |
 +-----------*/
```

You can create a JSON array with an empty JSON array in it. For example:

```
SELECT JSON_ARRAY([]) AS json_data

/*-----------+
 | json_data |
 +-----------+
 | [[]]      |
 +-----------*/
```

```
SELECT JSON_ARRAY(10, 'foo', NULL) AS json_data

/*-----------------+
 | json_data       |
 +-----------------+
 | [10,"foo",null] |
 +-----------------*/
```

```
SELECT JSON_ARRAY(STRUCT(10 AS a, 'foo' AS b)) AS json_data

/*----------------------+
 | json_data            |
 +----------------------+
 | [{"a":10,"b":"foo"}] |
 +----------------------*/
```

```
SELECT JSON_ARRAY(10, ['foo', 'bar'], [20, 30]) AS json_data

/*----------------------------+
 | json_data                  |
 +----------------------------+
 | [10,["foo","bar"],[20,30]] |
 +----------------------------*/
```

```
SELECT JSON_ARRAY(10, [JSON '20', JSON '"foo"']) AS json_data

/*-----------------+
 | json_data       |
 +-----------------+
 | [10,[20,"foo"]] |
 +-----------------*/
```

You can create an empty JSON array. For example:

```
SELECT JSON_ARRAY() AS json_data

/*-----------+
 | json_data |
 +-----------+
 | []        |
 +-----------*/
```

## `JSON_ARRAY_APPEND`

```
JSON_ARRAY_APPEND(
  json_expr,
  json_path_value_pair[, ...]
  [, append_each_element => { TRUE | FALSE } ]
)

json_path_value_pair:
  json_path, value
```

Appends JSON data to the end of a JSON array.

Arguments:

* `json_expr`: JSON. For example:

  ```
  JSON '["a", "b", "c"]'
  ```
* `json_path_value_pair`: A value and the [JSONPath](#JSONPath_format) for
  that value. This includes:

  + `json_path`: Append `value` at this [JSONPath](#JSONPath_format)
    in `json_expr`.
  + `value`: A [JSON encoding-supported](#json_encodings) value to
    append.
* `append_each_element`: A named argument with a `BOOL` value.

  + If `TRUE` (default), and `value` is a SQL array,
    appends each element individually.
  + If `FALSE,` and `value` is a SQL array, appends
    the array as one element.

Details:

* Path value pairs are evaluated left to right. The JSON produced by
  evaluating one pair becomes the JSON against which the next pair
  is evaluated.
* The operation is ignored if the path points to a JSON non-array value that
  isn't a JSON null.
* If `json_path` points to a JSON null, the JSON null is replaced by a
  JSON array that contains `value`.
* If the path exists but has an incompatible type at any given path token,
  the path value pair operation is ignored.
* The function applies all path value pair append operations even if an
  individual path value pair operation is invalid. For invalid operations,
  the operation is ignored and the function continues to process the rest of
  the path value pairs.
* If any `json_path` is an invalid [JSONPath](#JSONPath_format), an error is
  produced.
* If `json_expr` is SQL `NULL`, the function returns SQL `NULL`.
* If `append_each_element` is SQL `NULL`, the function returns `json_expr`.
* If `json_path` is SQL `NULL`, the `json_path_value_pair` operation is
  ignored.

**Return type**

`JSON`

**Examples**

In the following example, path `$` is matched and appends `1`.

```
SELECT JSON_ARRAY_APPEND(JSON '["a", "b", "c"]', '$', 1) AS json_data

/*-----------------+
 | json_data       |
 +-----------------+
 | ["a","b","c",1] |
 +-----------------*/
```

In the following example, `append_each_element` defaults to `TRUE`, so
`[1, 2]` is appended as individual elements.

```
SELECT JSON_ARRAY_APPEND(JSON '["a", "b", "c"]', '$', [1, 2]) AS json_data

/*-------------------+
 | json_data         |
 +-------------------+
 | ["a","b","c",1,2] |
 +-------------------*/
```

In the following example, `append_each_element` is `FALSE`, so
`[1, 2]` is appended as one element.

```
SELECT JSON_ARRAY_APPEND(
  JSON '["a", "b", "c"]',
  '$', [1, 2],
  append_each_element=>FALSE) AS json_data

/*---------------------+
 | json_data           |
 +---------------------+
 | ["a","b","c",[1,2]] |
 +---------------------*/
```

In the following example, `append_each_element` is `FALSE`, so
`[1, 2]` and `[3, 4]` are each appended as one element.

```
SELECT JSON_ARRAY_APPEND(
  JSON '["a", ["b"], "c"]',
  '$[1]', [1, 2],
  '$[1][1]', [3, 4],
  append_each_element=>FALSE) AS json_data

/*-----------------------------+
 | json_data                   |
 +-----------------------------+
 | ["a",["b",[1,2,[3,4]]],"c"] |
 +-----------------------------*/
```

In the following example, the first path `$[1]` appends `[1, 2]` as single
elements, and then the second path `$[1][1]` isn't a valid path to an array,
so the second operation is ignored.

```
SELECT JSON_ARRAY_APPEND(
  JSON '["a", ["b"], "c"]',
  '$[1]', [1, 2],
  '$[1][1]', [3, 4]) AS json_data

/*---------------------+
 | json_data           |
 +---------------------+
 | ["a",["b",1,2],"c"] |
 +---------------------*/
```

In the following example, path `$.a` is matched and appends `2`.

```
SELECT JSON_ARRAY_APPEND(JSON '{"a": [1]}', '$.a', 2) AS json_data

/*-------------+
 | json_data   |
 +-------------+
 | {"a":[1,2]} |
 +-------------*/
```

In the following example, a value is appended into a JSON null.

```
SELECT JSON_ARRAY_APPEND(JSON '{"a": null}', '$.a', 10)

/*------------+
 | json_data  |
 +------------+
 | {"a":[10]} |
 +------------*/
```

In the following example, path `$.a` isn't an array, so the operation is
ignored.

```
SELECT JSON_ARRAY_APPEND(JSON '{"a": 1}', '$.a', 2) AS json_data

/*-----------+
 | json_data |
 +-----------+
 | {"a":1}   |
 +----------
```