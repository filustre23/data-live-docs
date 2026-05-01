* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Data types Stay organized with collections Save and categorize content based on your preferences.

This page provides an overview of all GoogleSQL for BigQuery
data types, including information about their value
domains. For
information on data type literals and constructors, see
[Lexical Structure and Syntax](/bigquery/docs/reference/standard-sql/lexical#literals).

## Data type list

| Name | Summary |
| --- | --- |
| [Array type](#array_type) | An ordered list of zero or more elements of non-array values.  SQL type name: `ARRAY` |
| [Boolean type](#boolean_type) | A value that can be either `TRUE` or `FALSE`.  SQL type name: `BOOL`  SQL aliases: `BOOLEAN` |
| [Bytes type](#bytes_type) | Variable-length binary data.  SQL type name: `BYTES` |
| [Date type](#date_type) | A Gregorian calendar date, independent of time zone.  SQL type name: `DATE` |
| [Datetime type](#datetime_type) | A Gregorian date and a time, as they might be displayed on a watch, independent of time zone.  SQL type name: `DATETIME` |
| [Geography type](#geography_type) | A collection of points, linestrings, and polygons, which is represented as a point set, or a subset of the surface of the Earth.  SQL type name: `GEOGRAPHY` |
| [Graph element type](#graph_element_type) | An element in a property graph. Can be a `GRAPH_NODE` or `GRAPH_EDGE`.  SQL type name: `GRAPH_ELEMENT` |
| [Graph path type](#graph_path_type) | A path in a property graph.  SQL type name: `GRAPH_PATH` |
| [Interval type](#interval_type) | A duration of time, without referring to any specific point in time.  SQL type name: `INTERVAL` |
| [JSON type](#json_type) | Represents JSON, a lightweight data-interchange format.  SQL type name: `JSON` |
| [Measure type](#measure_type) | An aggregate calculation that doesn’t overcount.  SQL type name: `MEASURE` |
| [Numeric types](#numeric_types) | A numeric value. Several types are supported.  A 64-bit integer.  SQL type name: `INT64`   SQL aliases: `INT`, `SMALLINT`, `INTEGER`, `BIGINT`, `TINYINT`, `BYTEINT`  A decimal value with precision of 38 digits.  SQL type name: `NUMERIC`   SQL aliases: `DECIMAL`  A decimal value with precision of approximately 76.8 digits (the 77th digit is partial).  SQL type name: `BIGNUMERIC`   SQL aliases: `BIGDECIMAL`  An approximate double precision numeric value.  SQL type name: `FLOAT64` |
| [Range type](#range_type) | Contiguous range between two dates, datetimes, or timestamps.  SQL type name: `RANGE` |
| [String type](#string_type) | Variable-length character data.  SQL type name: `STRING` |
| [Struct type](#struct_type) | Container of ordered fields.  SQL type name: `STRUCT` |
| [Time type](#time_type) | A time of day, as might be displayed on a clock, independent of a specific date and time zone.  SQL type name: `TIME` |
| [Timestamp type](#timestamp_type) | A timestamp value represents an absolute point in time, independent of any time zone or convention such as daylight saving time (DST).  SQL type name: `TIMESTAMP` |

## Data type properties

When storing and querying data, it's helpful to keep the following data type
properties in mind:

### Nullable data types

For nullable data types, `NULL` is a valid value. Currently, all existing
data types are nullable. Conditions apply for
[arrays](#array_nulls).

### Orderable data types

Expressions of orderable data types can be used in an `ORDER BY` clause.
Applies to all data types except for:

* `ARRAY`
* `STRUCT`
* `GEOGRAPHY`
* `JSON`
* `GRAPH_ELEMENT`
* `GRAPH_PATH`

#### Ordering `NULL`s

In the context of the `ORDER BY` clause, `NULL`s are the minimum
possible value; that is, `NULL`s appear first in `ASC` sorts and last in
`DESC` sorts.

`NULL` values can be specified as the first or last values for a column
irrespective of `ASC` or `DESC` by using the `NULLS FIRST` or `NULLS LAST`
modifiers respectively.

To learn more about using `ASC`, `DESC`, `NULLS FIRST` and `NULLS LAST`, see
the [`ORDER BY` clause](/bigquery/docs/reference/standard-sql/query-syntax#order_by_clause).

#### Ordering floating points

Floating point values are sorted in this order, from least to greatest:

1. `NULL`
2. `NaN` — All `NaN` values are considered equal when sorting.
3. `-inf`
4. Negative numbers
5. 0 or -0 — All zero values are considered equal when sorting.
6. Positive numbers
7. `+inf`

### Groupable data types

Groupable data types can generally appear in an expression following `GROUP BY`,
`DISTINCT`, and `PARTITION BY`. All data types are supported except for:

* `GEOGRAPHY`
* `JSON`
* `GRAPH_PATH`

#### Grouping with floating point types

Groupable floating point types can appear in an expression following `GROUP BY`
and `DISTINCT`. `PARTITION BY` expressions can't
include [floating point types](#floating_point_types).

Special floating point values are grouped in the following way, including
both grouping done by a `GROUP BY` clause and grouping done by the
`DISTINCT` keyword:

* `NULL`
* `NaN` — All `NaN` values are considered equal when grouping.
* `-inf`
* 0 or -0 — All zero values are considered equal when grouping.
* `+inf`

#### Grouping with arrays

An `ARRAY` type is groupable if its element type is
groupable. An `ARRAY` type
is only groupable in a `GROUP BY` clause or in a
`SELECT DISTINCT` clause.

Two arrays are in the same group if and only if one of the following statements
is true:

* The two arrays are both `NULL`.
* The two arrays have the same number of elements and all corresponding
  elements are in the same groups.

#### Grouping with structs

A `STRUCT` type is groupable if its field types are
groupable. A `STRUCT` type
is only groupable in a `GROUP BY` clause or in a
`SELECT DISTINCT` clause.

Two structs are in the same group if and only if one of the following statements
is true:

* The two structs are both `NULL`.
* All corresponding field values between the structs are in the same groups.

### Comparable data types

Values of the same comparable data type can be compared to each other.
All data types are supported except for:

* `GEOGRAPHY`
* `JSON`
* `ARRAY`

Notes:

* Equality comparisons for structs are supported field by field, in
  field order. Field names are ignored. Less than and greater than comparisons
  aren't supported.
* To compare geography values, use [ST\_Equals](/bigquery/docs/reference/standard-sql/geography_functions#st_equals).
* When comparing ranges, the lower bounds are compared. If the lower bounds are
  equal, the upper bounds are compared, instead.
* When comparing ranges, `NULL` values are handled as follows:
  + `NULL` lower bounds are sorted before non-`NULL` lower bounds.
  + `NULL` upper bounds are sorted after non-`NULL` upper bounds.
  + If two bounds that are being compared are `NULL`, the comparison is `TRUE`.
  + An `UNBOUNDED` bound is treated as a `NULL` bound.
* All types that support comparisons can be used in a `JOIN` condition.
  See [JOIN Types](/bigquery/docs/reference/standard-sql/query-syntax#join_types) for an explanation of join conditions.

### Collatable data types

Collatable data types support collation, which determines how to sort and
compare strings. These data types support collation:

* String
* String fields in a struct
* String elements in an array

## Data type sizes

Use the following table to see the size in logical bytes for each supported data
type.

| Data type | Size |
| --- | --- |
| `ARRAY` | The sum of the size of its elements. For example, an array defined as (`ARRAY<INT64>`) that contains 4 entries is calculated as 32 logical bytes (4 entries x 8 logical bytes). |
| `BIGNUMERIC` | 32 logical bytes |
| `BOOL` | 1 logical byte |
| `BYTES` | 2 logical bytes + the number of logical bytes in the value |
| `DATE` | 8 logical bytes |
| `DATETIME` | 8 logical bytes |
| `FLOAT64` | 8 logical bytes |
| `GEOGRAPHY` | 16 logical bytes + 24 logical bytes \* the number of vertices in the geography type. To verify the number of vertices, use the [`ST_NumPoints`](/bigquery/docs/reference/standard-sql/geography_functions#st_numpoints) function. |
| `INT64` | 8 logical bytes |
| `INTERVAL` | 16 logical bytes |
| `JSON` | The number of logical bytes in UTF-8 encoding of the JSON-formatted string equivalent after canonicalization. |
| `NUMERIC` | 16 logical bytes |
| `RANGE` | 16 logical bytes |
| `STRING` | 2 logical bytes + the UTF-8 encoded string size |
| `STRUCT` | 0 logical bytes + the size of the contained fields |
| `TIME` | 8 logical bytes |
| `TIMESTAMP` | 8 logical bytes |

A `NULL` value for any data type is calculated as 0 logical bytes.

A repeated column is stored as an array, and the size is calculated based on the
column data type and the number of values. For example, an integer column
(`INT64`) that's repeated (`ARRAY<INT64>`) and contains 4 entries is calculated
as 32 logical bytes (4 entries x 8 logical bytes). The total size of all values
in a table row can't exceed the
[maximum row size](/bigquery/quotas#max_row_size).

## Parameterized data types

Syntax:

```
DATA_TYPE(param[, ...])
```

You can use parameters to specify constraints for the following data types:

* `STRING`
* `BYTES`
* `NUMERIC`
* `BIGNUMERIC`

A data type that's declared with parameters is called a parameterized data
type. You can only use parameterized data types with columns and script
variables. A column with a parameterized data type is a *parameterized column*
and a script variable with a parameterized data type is a *parameterized script
variable*. Parameterized type constraints are enforced when writing a value to a
parameterized column or when assigning a value to a parameterized script
variable.

A data type's parameters aren't propagated in an expression, only the data type
is.

**Examples**

```
-- Declare a variable with type parameters.
DECLARE x STRING(10);

-- This is a valid assignment to x.
SET x = "hello";

-- This assignment to x violates the type parameter constraint and results in an OUT_OF_RANGE error.
SET x = "this string is too long"
```

```
-- Declare variables with type parameters.
DECLARE x NUMERIC(10) DEFAULT 12345;
DECLARE y NUMERIC(5, 2) DEFAULT 123.45;

-- The variable x is treated as a NUMERIC value when read, so the result of this query
-- is a NUMERIC without type parameters.
SELECT x;

-- Type parameters aren't propagated within expressions, so variables x and y are treated
-- as NUMERIC values when read and the result of this query is a NUMERIC without type parameters.
SELECT x + y;
```

## Array type

| Name | Description |
| --- | --- |
| `ARRAY` | Ordered list of zero or more elements of any non-array type. |

An array is an ordered list of zero or more elements of non-array values.
Elements in an array must share the same type.

Arrays of arrays aren't allowed. Queries that would produce an array of
arrays return an error. Instead, a struct must be inserted between the
arrays using the `SELECT AS STRUCT` construct.

To learn more about the literal representation of an array type,
see [Array literals](/bigquery/docs/reference/standard-sql/lexical#array_literals).

To learn more about using arrays in GoogleSQL, see [Work with
arrays](/bigquery/docs/arrays#constructing_arrays).

### `NULL`s and the array type

Currently, GoogleSQL for BigQuery has the following rules with respect to `NULL`s and
arrays:

* An array can be `NULL`.

  For example:

  ```
  SELECT CAST(NULL AS ARRAY<INT64>) IS NULL AS array_is_null;

  /*---------------+
   | array_is_null |
   +---------------+
   | TRUE          |
   +---------------*/
  ```
* GoogleSQL for BigQuery translates a `NULL` array into an empty array in the query
  result, although inside the query, `NULL` and empty arrays are two distinct
  values.

  For example:

  ```
  WITH Items AS (
    SELECT [] AS numbers, "Empty array in query" AS description UNION ALL
    SELECT CAST(NULL AS ARRAY<INT64>), "NULL array in query")
  SELECT numbers, description, numbers IS NULL AS numbers_null
  FROM Items;

  /*---------+----------------------+--------------+
   | numbers | description          | numbers_null |
   +---------+----------------------+--------------+
   | []      | Empty array in query | false        |
   | []      | NULL array in query  | true         |
   +---------+----------------------+--------------*/
  ```

  When you write a `NULL` array to a table, it's converted to an
  empty array. If you write `Items` to a table from the previous query,
  then each array is written as an empty array:

  ```
  SELECT numbers, description, numbers IS NULL AS numbers_null
  FROM Items;

  /*---------+----------------------+--------------+
   | numbers | description          | numbers_null |
   +---------+----------------------+--------------+
   | []      | Empty array in query | false        |
   | []      | NULL array in query  | false        |
   +---------+----------------------+--------------*/
  ```
* GoogleSQL for BigQuery raises an error if the query result has an array which
  contains `NULL` elements, although such an array can be used inside the query.

  For example, this works:

  ```
  SELECT FORMAT("%T", [1, NULL, 3]) as numbers;

  /*--------------+
   | numbers      |
   +--------------+
   | [1, NULL, 3] |
   +--------------*/
  ```

  But this raises an error:

  ```
  -- error
  SELECT [1, NULL, 3] as numbers;
  ```

### Declaring an array type

```
ARRAY<T>
```

Array types are declared using the angle brackets (`<` and `>`). The type
of the elements of an array can be arbitrarily complex with the exception that
an array can't directly contain another array.

**Examples**

| Type Declaration | Meaning |
| --- | --- |
| `ARRAY<INT64>` | Simple array of 64-bit integers. |
| `ARRAY<BYTES(5)>` | Simple array of parameterized bytes. |
| `ARRAY<STRUCT<INT64, INT64>>` | An array of structs, each of which contains two 64-bit integers. |
| `ARRAY<ARRAY<INT64>>`  (not supported) | This is an **invalid** type declaration which is included here just in case you came looking for how to create a multi-level array. Arrays can't contain arrays directly. Instead see the next example. |
| `ARRAY<STRUCT<ARRAY<INT64>>>` | An array of arrays of 64-bit integers. Notice that there is a struct between the two arrays because arrays can't hold other arrays directly. |

### Constructing an array

You can construct an array using array literals or array functions.

#### Using array literals

You can build an array literal in GoogleSQL using brackets (`[` and
`]`). Each element in an array is separated by a comma.

```
SELECT [1, 2, 3] AS numbers;

SELECT ["apple", "pear", "orange"] AS fruit;

SELECT [true, false, true] AS booleans;
```

You can also create arrays from any expressions that have compatible types. For
example:

```
SELECT [a, b, c]
FROM
  (SELECT 5 AS a,
          37 AS b,
          406 AS c);

SELECT [a, b, c]
FROM
  (SELECT CAST(5 AS INT64) AS a,
          CAST(37 AS FLOAT64) AS b,
          406 AS c);
```

Notice that the second example contains three expressions: one that returns an
`INT64`, one that returns a `FLOAT64`, and one that
declares a literal. This expression works because all three expressions share
`FLOAT64` as a supertype.

To declare a specific data type for an array, use angle
brackets (`<` and `>`). For example:

```
SELECT ARRAY<FLOAT64>[1, 2, 3] AS floats;
```

Arrays of most data types, such as `INT64` or `STRING`, don't require
that you declare them first.

```
SELECT [1, 2, 3] AS numbers;
```

You can write an empty array of a specific type using `ARRAY<type>[]`. You can
also write an untyped empty array using `[]`, in which case GoogleSQL
attempts to infer the array type from the surrounding context. If
GoogleSQL can't infer a type, the default type `ARRAY<INT64>` is used.

#### Using generated values

You can also construct an `ARRAY` with generated values.

##### Generating arrays of integers

[`GENERATE_ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#generate_array)
generates an array of values from a starting and ending value and a step value.
For example, the following query generates an array that contains all of the odd
integers from 11 to 33, inclusive:

```
SELECT GENERATE_ARRAY(11, 33, 2) AS odds;

/*--------------------------------------------------+
 | odds                                             |
 +--------------------------------------------------+
 | [11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31, 33] |
 +--------------------------------------------------*/
```

You can also generate an array of values in descending order by giving a
negative step value:

```
SELECT GENERATE_ARRAY(21, 14, -1) AS countdown;

/*----------------------------------+
 | countdown                        |
 +----------------------------------+
 | [21, 20, 19, 18, 17, 16, 15, 14] |
 +----------------------------------*/
```

##### Generating arrays of dates

[`GENERATE_DATE_ARRAY`](/bigquery/docs/reference/standard-sql/array_functions#generate_date_array)
generates an array of `DATE`s from a starting and ending `DATE` and a step
`INTERVAL`.

You can generate a set of `DATE` values using `GENERATE_DATE_ARRAY`. For
example, this query returns the current `DATE` and the following
`DATE`s at 1 `WEEK` intervals up to and including a later `DATE`:

```
SELECT
  GENERATE_DATE_ARRAY('2017-11-21', '2017-12-31', INTERVAL 1 WEEK)
    AS date_array;

/*--------------------------------------------------------------------------+
 | date_array                                                               |
 +--------------------------------------------------------------------------+
 | [2017-11-21, 2017-11-28, 2017-12-05, 2017-12-12, 2017-12-19, 2017-12-26] |
 +--------------------------------------------------------------------------*/
```

## Boolean type

| Name | Description |
| --- | --- |
| `BOOL`  `BOOLEAN` | Boolean values are represented by the keywords `TRUE` and `FALSE` (case-insensitive). |

`BOOLEAN` is an alias for `BOOL`.

Boolean values are sorted in this order, from least to greatest:

1. `NULL`
2. `FALSE`
3. `TRUE`

## Bytes type

| Name | Description |
| --- | --- |
| `BYTES` | Variable-length binary data. |

String and bytes are separate types that can't be used interchangeably.
Most functions on strings are also defined on bytes. The bytes version
operates on raw bytes rather than Unicode characters. Casts between string and
bytes enforce that the bytes are encoded using UTF-8.

You can convert a base64-encoded `STRING` expression into the `BYTES` format
using the
[`FROM_BASE64` function](/bigquery/docs/reference/standard-sql/string_functions#from_base64).
You can also convert a sequence of `BYTES` into a base64-encoded `STRING`
expression using the
[`TO_BASE64` function](/bigquery/docs/reference/standard-sql/string_functions#to_base64).

To learn more about the literal representation of a bytes type,
see [Bytes literals](/bigquery/docs/reference/standard-sql/lexical#string_and_bytes_literals).

### Parameterized bytes type

| Parameterized Type | Description |
| --- | --- |
| `BYTES(L)` | Sequence of bytes with a maximum of L bytes allowed in the binary string, where L is a positive `INT64` value. If a sequence of bytes has more than L bytes, throws an `OUT_OF_RANGE` error. |

See [Parameterized Data Types](#parameterized_data_types) for more information on
parameterized types and where they can be used.

## Date type

| Name | Range |
| --- | --- |
| `DATE` | 0001-01-01 to 9999-12-31. |

The date type represents a Gregorian calendar date, independent of time zone. A
date value doesn't represent a specific 24-hour time period. Rather, a given
date value represents a different 24-hour period when interpreted in different
time zones, and may represent a shorter or longer day during daylight saving
time (DST) transitions.
To represent an absolute point in time,
use a [timestamp](#timestamp_type).

##### Canonical format

```
YYYY-[M]M-[D]D
```

* `YYYY`: Four-digit year.
* `[M]M`: One or two digit month.
* `[D]D`: One or two digit day.

To learn more about the literal representation of a date type,
see [Date literals](/bigquery/docs/reference/standard-sql/lexical#date_literals).

## Datetime type

| Name | Range |
| --- | --- |
| `DATETIME` | 0001-01-01 00:00:00 to 9999-12-31 23:59:59.999999 |

A datetime value represents a Gregorian date and a time,
as they might be displayed on a watch, independent of time zone.
It includes the year, month, day, hour, minute, second,
and subsecond.
To represent an absolute point in time,
use a [timestamp](#timestamp_type).

##### Canonical format

```
civil_date_part[time_part]

civil_date_part:
    YYYY-[M]M-[D]D

time_part:
    { |T|t}[H]H:[M]M:[S]S[.F]
```

* `YYYY`: Four-digit year.
* `[M]M`: One or two digit month.
* `[D]D`: One or two digit day.
* `{ |T|t}`: A space or a `T` or `t` separator. The `T` and `t`
  separators are flags for time.
* `[H]H`: One or two digit hour (valid values from 00 to 23).
* `[M]M`: One or two digit minutes (valid values from 00 to 59).
* `[S]S`: One or two digit seconds (valid values from 00 to 60).
* `[.F]`: Up to six fractional digits (microsecond
  precision).

To learn more about the literal representation of a datetime type,
see [Datetime literals](/bigquery/docs/reference/standard-sql/lexical#datetime_literals).

## Geography type

| Name | Description |
| --- | --- |
| `GEOGRAPHY` | A collection of points, linestrings, and polygons, which is represented as a point set, or a subset of the surface of the Earth. |

The geography type is based on the [OGC Simple
Features specification (SFS)](http://www.opengeospatial.org/standards/sfs#downloads),
and can contain the following objects:

| Geography object | Description |
| --- | --- |
| `Point` | A single location in coordinate space known as a point. A point has an x-coordinate value and a y-coordinate value, where the x-coordinate is longitude and the y-coordinate is latitude of the point on the [WGS84 reference ellipsoid](https://en.wikipedia.org/wiki/World_Geodetic_System).  Syntax:    ``` POINT(x_coordinate y_coordinate) ```  Examples:    ``` POINT(32 210) ```      ``` POINT EMPTY ``` |
| `LineString` | Represents a linestring, which is a one-dimensional geometric object, with a sequence of points and geodesic edges between them.  Syntax:    ``` LINESTRING(point[, ...]) ```  Examples:    ``` LINESTRING(1 1, 2 1, 3.1 2.88, 3 -3) ```      ``` LINESTRING EMPTY ``` |
| `Polygon` | A polygon, which is represented as a planar surface defined by 1 exterior boundary and 0 or more interior boundaries. Each interior boundary defines a hole in the polygon. The boundary loops of polygons are oriented so that if you traverse the boundary vertices in order, the interior of the polygon is on the left.  Syntax:    ``` POLYGON(interior_ring[, ...])  interior_ring:   (point[, ...]) ```  Examples:    ``` POLYGON((0 0, 2 2, 2 0, 0 0), (2 2, 3 4, 2 4, 2 2)) ```      ``` POLYGON EMPTY ``` |
| `MultiPoint` | A collection of points.  Syntax:    ``` MULTIPOINT(point[, ...]) ```  Examples:    ``` MULTIPOINT(0 32, 123 9, 48 67) ```      ``` MULTIPOINT EMPTY ``` |
| `MultiLineString` | Represents a multilinestring, which is a collection of linestrings.  Syntax:    ``` MULTILINESTRING((linestring)[, ...]) ```  Examples: |