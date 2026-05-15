* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Operators Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports operators.
Operators are represented by special characters or keywords; they don't use
function call syntax. An operator manipulates any number of data inputs, also
called operands, and returns a result.

Common conventions:

* Unless otherwise specified, all operators return `NULL` when one of the
  operands is `NULL`.
* All operators will throw an error if the computation result overflows.
* For all floating point operations, `+/-inf` and `NaN` may only be returned
  if one of the operands is `+/-inf` or `NaN`. In other cases, an error is
  returned.

### Operator precedence

The following table lists all GoogleSQL operators from highest to
lowest precedence, i.e., the order in which they will be evaluated within a
statement.

| Order of Precedence | Operator | Input Data Types | Name | Operator Arity |
| --- | --- | --- | --- | --- |
| 1 | Field access operator | `STRUCT` `JSON` | Field access operator | Binary |
|  | Array subscript operator | `ARRAY` | Array position. Must be used with `OFFSET` or `ORDINAL`—see [Array Functions](/bigquery/docs/reference/standard-sql/array_functions) . | Binary |
|  | JSON subscript operator | `JSON` | Field name or array position in JSON. | Binary |
| 2 | `+` | All numeric types | Unary plus | Unary |
|  | `-` | All numeric types | Unary minus | Unary |
|  | `~` | Integer or `BYTES` | Bitwise not | Unary |
| 3 | `*` | All numeric types | Multiplication | Binary |
|  | `/` | All numeric types | Division | Binary |
|  | `||` | `STRING`, `BYTES`, or `ARRAY<T>` | Concatenation operator | Binary |
| 4 | `+` | All numeric types, `DATE` with `INT64` , `INTERVAL` | Addition | Binary |
|  | `-` | All numeric types, `DATE` with `INT64` , `INTERVAL` | Subtraction | Binary |
| 5 | `<<` | Integer or `BYTES` | Bitwise left-shift | Binary |
|  | `>>` | Integer or `BYTES` | Bitwise right-shift | Binary |
| 6 | `&` | Integer or `BYTES` | Bitwise and | Binary |
| 7 | `^` | Integer or `BYTES` | Bitwise xor | Binary |
| 8 | `|` | Integer or `BYTES` | Bitwise or | Binary |
| 9 (Comparison Operators) | `=` | Any comparable type. See [Data Types](/bigquery/docs/reference/standard-sql/data-types) for a complete list. | Equal | Binary |
|  | `<` | Any comparable type. See [Data Types](/bigquery/docs/reference/standard-sql/data-types) for a complete list. | Less than | Binary |
|  | `>` | Any comparable type. See [Data Types](/bigquery/docs/reference/standard-sql/data-types) for a complete list. | Greater than | Binary |
|  | `<=` | Any comparable type. See [Data Types](/bigquery/docs/reference/standard-sql/data-types) for a complete list. | Less than or equal to | Binary |
|  | `>=` | Any comparable type. See [Data Types](/bigquery/docs/reference/standard-sql/data-types) for a complete list. | Greater than or equal to | Binary |
|  | `!=`, `<>` | Any comparable type. See [Data Types](/bigquery/docs/reference/standard-sql/data-types) for a complete list. | Not equal | Binary |
|  | `[NOT] LIKE` | `STRING` and `BYTES` | Value does [not] match the pattern specified | Binary |
|  | Quantified LIKE | `STRING` and `BYTES` | Checks a search value for matches against several patterns. | Binary |
|  | `[NOT] BETWEEN` | Any comparable types. See [Data Types](/bigquery/docs/reference/standard-sql/data-types) for a complete list. | Value is [not] within the range specified | Binary |
|  | `[NOT] IN` | Any comparable types. See [Data Types](/bigquery/docs/reference/standard-sql/data-types) for a complete list. | Value is [not] in the set of values specified | Binary |
|  | `IS [NOT] DISTINCT FROM` | All | Value is [not] `DISTINCT FROM` | Binary |
|  | `IS [NOT] NULL` | All | Value is [not] `NULL` | Unary |
|  | `IS [NOT] TRUE` | `BOOL` | Value is [not] `TRUE`. | Unary |
|  | `IS [NOT] FALSE` | `BOOL` | Value is [not] `FALSE`. | Unary |
| 10 | `NOT` | `BOOL` | Logical `NOT` | Unary |
| 11 | `AND` | `BOOL` | Logical `AND` | Binary |
| 12 | `OR` | `BOOL` | Logical `OR` | Binary |

For example, the logical expression:

`x OR y AND z`

is interpreted as:

`( x OR ( y AND z ) )`

Operators with the same precedence are left associative. This means that those
operators are grouped together starting from the left and moving right. For
example, the expression:

`x AND y AND z`

is interpreted as:

`( ( x AND y ) AND z )`

The expression:

`x * y / z`

is interpreted as:

`( ( x * y ) / z )`

All comparison operators have the same priority, but comparison operators
aren't associative. Therefore, parentheses are required to resolve
ambiguity. For example:

`(x < y) IS FALSE`

### Operator list

| Name | Summary |
| --- | --- |
| [Field access operator](#field_access_operator) | Gets the value of a field. |
| [Array subscript operator](#array_subscript_operator) | Gets a value from an array at a specific position. |
| [Struct subscript operator](#struct_subscript_operator) | Gets the value of a field at a selected position in a struct. |
| [JSON subscript operator](#json_subscript_operator) | Gets a value of an array element or field in a JSON expression. |
| [Arithmetic operators](#arithmetic_operators) | Performs arithmetic operations. |
| [Date arithmetics operators](#date_arithmetics_operators) | Performs arithmetic operations on dates. |
| [Datetime subtraction](#datetime_subtraction) | Computes the difference between two datetimes as an interval. |
| [Interval arithmetic operators](#interval_arithmetic_operators) | Adds an interval to a datetime or subtracts an interval from a datetime. |
| [Bitwise operators](#bitwise_operators) | Performs bit manipulation. |
| [Logical operators](#logical_operators) | Tests for the truth of some condition and produces `TRUE`, `FALSE`, or `NULL`. |
| [Graph logical operators](#graph_logical_operators) | Tests for the truth of a condition in a graph label and produces either `TRUE` or `FALSE`. |
| [Graph predicates](#graph_predicates) | Tests for the truth of a condition for a graph element and produces `TRUE`, `FALSE`, or `NULL`. |
| [`ALL_DIFFERENT` predicate](#all_different_predicate) | In a graph, checks to see if the elements in a list are all different. |
| [`IS DESTINATION` predicate](#is_destination_predicate) | In a graph, checks to see if a node is or isn't the destination of an edge. |
| [`IS SOURCE` predicate](#is_source_predicate) | In a graph, checks to see if a node is or isn't the source of an edge. |
| [`SAME` predicate](#same_predicate) | In a graph, checks if all graph elements in a list bind to the same node or edge. |
| [Comparison operators](#comparison_operators) | Compares operands and produces the results of the comparison as a `BOOL` value. |
| [`EXISTS` operator](#exists_operator) | Checks if a subquery produces one or more rows. |
| [`IN` operator](#in_operators) | Checks for an equal value in a set of values. |
| [`IS` operators](#is_operators) | Checks for the truth of a condition and produces either `TRUE` or `FALSE`. |
| [`IS DISTINCT FROM` operator](#is_distinct) | Checks if values are considered to be distinct from each other. |
| [`LIKE` operator](#like_operator) | Checks if values are like or not like one another. |
| [Quantified `LIKE` operator](#like_operator_quantified) | Checks a search value for matches against several patterns. |
| [Concatenation operator](#concatenation_operator) | Combines multiple values into one. |
| [`WITH` expression](#with_expression) | Creates variables for re-use and produces a result expression. |

### Field access operator

```
expression.fieldname[. ...]
```

**Description**

Gets the value of a field. Alternatively known as the dot operator. Can be
used to access nested fields. For example, `expression.fieldname1.fieldname2`.

Input values:

* `STRUCT`
* `JSON`
* `GRAPH_ELEMENT`

**Note:** If the field to access is within a `STRUCT`, you can use the
[struct subscript operator](#struct_subscript_operator) to access the field by
its position within the `STRUCT` instead of by its name. Accessing by
a field by position is useful when fields are un-named or have ambiguous names.

**Return type**

* For `STRUCT`: SQL data type of `fieldname`. If a field isn't found in
  the struct, an error is thrown.
* For `JSON`: `JSON`. If a field isn't found in a JSON value, a SQL `NULL` is
  returned.
* For `GRAPH_ELEMENT`: SQL data type of `fieldname`. If a field (property)
  isn't found in the graph element, an error is returned.

**Example**

In the following example, the field access operations are `.address` and
`.country`.

```
SELECT
  STRUCT(
    STRUCT('Yonge Street' AS street, 'Canada' AS country)
      AS address).address.country

/*---------+
 | country |
 +---------+
 | Canada  |
 +---------*/
```

### Array subscript operator

**Note:** Syntax characters enclosed in double quotes (`""`) are literal and
required.

```
array_expression "[" array_subscript_specifier "]"

array_subscript_specifier:
  { index | position_keyword(index) }

position_keyword:
  { OFFSET | SAFE_OFFSET | ORDINAL | SAFE_ORDINAL }
```

**Description**

Gets a value from an array at a specific position.

Input values:

* `array_expression`: The input array.
* `position_keyword(index)`: Determines where the index for the array should
  start and how out-of-range indexes are handled. The index is an integer that
  represents a specific position in the array.
  + `OFFSET(index)`: The index starts at zero. Produces an error if the index is
    out of range. To produce `NULL` instead of an error, use
    `SAFE_OFFSET(index)`. This
    position keyword produces the same result as `index` by itself.
  + `SAFE_OFFSET(index)`: The index starts at
    zero. Returns `NULL` if the index is out of range.
  + `ORDINAL(index)`: The index starts at one.
    Produces an error if the index is out of range.
    To produce `NULL` instead of an error, use `SAFE_ORDINAL(index)`.
  + `SAFE_ORDINAL(index)`: The index starts at
    one. Returns `NULL` if the index is out of range.
* `index`: An integer that represents a specific position in the array. If used
  by itself without a position keyword, the index starts at zero and produces
  an error if the index is out of range. To produce `NULL` instead of an error,
  use the `SAFE_OFFSET(index)` or `SAFE_ORDINAL(index)` position keyword.

**Tip:** To access the first or last element in an array, use the
[`ARRAY_FIRST`](/bigquery/docs/reference/standard-sql/array_functions#array_first) or [`ARRAY_LAST`](/bigquery/docs/reference/standard-sql/array_functions#array_last)
function.

**Return type**

`T` where `array_expression` is `ARRAY<T>`.

**Examples**

In following query, the array subscript operator is used to return values at
specific position in `item_array`. This query also shows what happens when you
reference an index (`6`) in an array that's out of range. If the `SAFE` prefix
is included, `NULL` is returned, otherwise an error is produced.

```
SELECT
  ["coffee", "tea", "milk"] AS item_array,
  ["coffee", "tea", "milk"][0] AS item_index,
  ["coffee", "tea", "milk"][OFFSET(0)] AS item_offset,
  ["coffee", "tea", "milk"][ORDINAL(1)] AS item_ordinal,
  ["coffee", "tea", "milk"][SAFE_OFFSET(6)] AS item_safe_offset

/*---------------------+------------+-------------+--------------+------------------+
 | item_array          | item_index | item_offset | item_ordinal | item_safe_offset |
 +---------------------+------------+-------------+--------------+------------------+
 | [coffee, tea, milk] | coffee     | coffee      | coffee       | NULL             |
 +----------------------------------+-------------+--------------+------------------*/
```

When you reference an index that's out of range in an array, and a positional
keyword that begins with `SAFE` isn't included, an error is produced.
For example:

```
-- Error. Array index 6 is out of bounds.
SELECT ["coffee", "tea", "milk"][6] AS item_offset
```

```
-- Error. Array index 6 is out of bounds.
SELECT ["coffee", "tea", "milk"][OFFSET(6)] AS item_offset
```

### Struct subscript operator

**Note:** Syntax characters enclosed in double quotes (`""`) are literal and
required.

```
struct_expression "[" struct_subscript_specifier "]"

struct_subscript_specifier:
  { index | position_keyword(index) }

position_keyword:
  { OFFSET | ORDINAL }
```

**Description**

Gets the value of a field at a selected position in a struct.

**Input types**

* `struct_expression`: The input struct.
* `position_keyword(index)`: Determines where the index for the struct should
  start and how out-of-range indexes are handled. The index is an
  integer literal or constant that represents a specific position in the struct.
  + `OFFSET(index)`: The index starts at zero. Produces an error if the index is
    out of range. Produces the same
    result as `index` by itself.
  + `ORDINAL(index)`: The index starts at one. Produces an error if the index
    is out of range.
* `index`: An integer literal or constant that represents a specific position in
  the struct. If used by itself without a position keyword, the index starts at
  zero and produces an error if the index is out of range.

**Note:** The struct subscript operator doesn't support `SAFE` positional keywords
at this time.

**Examples**

In following query, the struct subscript operator is used to return values at
specific locations in `item_struct` using position keywords. This query also
shows what happens when you reference an index (`6`) in an struct that's out of
range.

```
SELECT
  STRUCT<INT64, STRING, BOOL>(23, "tea", FALSE)[0] AS field_index,
  STRUCT<INT64, STRING, BOOL>(23, "tea", FALSE)[OFFSET(0)] AS field_offset,
  STRUCT<INT64, STRING, BOOL>(23, "tea", FALSE)[ORDINAL(1)] AS field_ordinal

/*-------------+--------------+---------------+
 | field_index | field_offset | field_ordinal |
 +-------------+--------------+---------------+
 | 23          | 23           | 23            |
 +-------------+--------------+---------------*/
```

When you reference an index that's out of range in a struct, an error is
produced. For example:

```
-- Error: Field ordinal 6 is out of bounds in STRUCT
SELECT STRUCT<INT64, STRING, BOOL>(23, "tea", FALSE)[6] AS field_offset
```

```
-- Error: Field ordinal 6 is out of bounds in STRUCT
SELECT STRUCT<INT64, STRING, BOOL>(23, "tea", FALSE)[OFFSET(6)] AS field_offset
```

### JSON subscript operator

**Note:** Syntax characters enclosed in double quotes (`""`) are literal and
required.

```
json_expression "[" array_element_id "]"
```

```
json_expression "[" field_name "]"
```

**Description**

Gets a value of an array element or field in a JSON expression. Can be
used to access nested data.

Input values:

* `JSON expression`: The `JSON` expression that contains an array element or
  field to return.
* `[array_element_id]`: An `INT64` expression that represents a zero-based index
  in the array. If a negative value is entered, or the value is greater than
  or equal to the size of the array, or the JSON expression doesn't represent
  a JSON array, a SQL `NULL` is returned.
* `[field_name]`: A `STRING` expression that represents the name of a field in
  JSON. If the field name isn't found, or the JSON expression isn't a
  JSON object, a SQL `NULL` is returned.

**Return type**

`JSON`

**Example**

In the following example:

* `json_value` is a JSON expression.
* `.class` is a JSON field access.
* `.students` is a JSON field access.
* `[0]` is a JSON subscript expression with an element offset that
  accesses the zeroth element of an array in the JSON value.
* `['name']` is a JSON subscript expression with a field name that
  accesses a field.

```
SELECT json_value.class.students[0]['name'] AS first_student
FROM
  UNNEST(
    [
      JSON '{"class" : {"students" : [{"name" : "Jane"}]}}',
      JSON '{"class" : {"students" : []}}',
      JSON '{"class" : {"students" : [{"name" : "John"}, {"name": "Jamie"}]}}'])
    AS json_value;

/*-----------------+
 | first_student   |
 +-----------------+
 | "Jane"          |
 | NULL            |
 | "John"          |
 +-----------------*/
```

### Arithmetic operators

All arithmetic operators accept input of numeric type `T`, and the result type
has type `T` unless otherwise indicated in the description below:

| Name | Syntax |
| --- | --- |
| Addition | `X + Y` |
| Subtraction | `X - Y` |
| Multiplication | `X * Y` |
| Division | `X / Y` |
| Unary Plus | `+ X` |
| Unary Minus | `- X` |

**Note:** Divide by zero operations return an error. To return a different result,
consider the `IEEE_DIVIDE` or `SAFE_DIVIDE` functions.

Result types for Addition, Subtraction and Multiplication:

| INPUT | `INT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| --- | --- | --- | --- | --- |
| `INT64` | `INT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| `NUMERIC` | `NUMERIC` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| `BIGNUMERIC` | `BIGNUMERIC` | `BIGNUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| `FLOAT64` | `FLOAT64` | `FLOAT64` | `FLOAT64` | `FLOAT64` |

Result types for Division:

| INPUT | `INT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| --- | --- | --- | --- | --- |
| `INT64` | `FLOAT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| `NUMERIC` | `NUMERIC` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| `BIGNUMERIC` | `BIGNUMERIC` | `BIGNUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| `FLOAT64` | `FLOAT64` | `FLOAT64` | `FLOAT64` | `FLOAT64` |

Result types for Unary Plus:

| INPUT | `INT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| --- | --- | --- | --- | --- |
| OUTPUT | `INT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |

Result types for Unary Minus:

| INPUT | `INT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| --- | --- | --- | --- | --- |
| OUTPUT | `INT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |

### Date arithmetics operators

Operators '+' and '-' can be used for arithmetic operations on dates.

```
date_expression + int64_expression
int64_expression + date_expression
date_expression - int64_expression
```

**Description**

Adds or subtracts `int64_expression` days to or from `date_expression`. This is
equivalent to `DATE_ADD` or `DATE_SUB` functions, when interval is expressed in
days.

**Return Data Type**

`DATE`

**Example**

```
SELECT DATE "2020-09-22" + 1 AS day_later, DATE "2020-09-22" - 7 AS week_ago

/*------------+------------+
 | day_later  | week_ago   |
 +------------+------------+
 | 2020-09-23 | 2020-09-15 |
 +------------+------------*/
```

### Datetime subtraction

```
date_expression - date_expression
timestamp_expression - timestamp_expression
datetime_expression - datetime_expression
```

**Description**

Computes the difference between two datetime values as an interval.

**Return Data Type**

`INTERVAL`

**Example**

```
SELECT
  DATE "2021-05-20" - DATE "2020-04-19" AS date_diff,
  TIMESTAMP "2021-06-01 12:34:56.789" - TIMESTAMP "2021-05-31 00:00:00" AS time_diff

/*-------------------+------------------------+
 | date_diff         | time_diff              |
 +-------------------+------------------------+
 | 0-0 396 0:0:0     | 0-0 0 36:34:56.789     |
 +-------------------+------------------------*/
```

### Interval arithmetic operators

**Addition and subtraction**

```
date_expression + interval_expression = DATETIME
date_expression - interval_expression = DATETIME
timestamp_expression + interval_expression = TIMESTAMP
timestamp_expression - interval_expression = TIMESTAMP
datetime_expression + interval_expression = DATETIME
datetime_expression - interval_expression = DATETIME
```

**Description**

Adds an interval to a datetime value or subtracts an interval from a datetime
value.

**Example**

```
SELECT
  DATE "2021-04-20" + INTERVAL 25 HOUR AS date_plus,
  TIMESTAMP "2021-05-02 00:01:02.345+00" - INTERVAL 10 SECOND AS time_minus;

/*-------------------------+--------------------------------+
 | date_plus               | time_minus                     |
 +-------------------------+--------------------------------+
 | 2021-04-21 01:00:00     | 2021-05-02 00:00:52.345+00     |
 +-------------------------+--------------------------------*/
```

**Multiplication and division**

```
interval_expression * integer_expression = INTERVAL
interval_expression / integer_expression = INTERVAL
```

**Description**

Multiplies or divides an interval value by an integer.

**Example**

```
SELECT
  INTERVAL '1:2:3' HOUR TO SECOND * 10 AS mul1,
```