* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Mathematical functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports mathematical functions.
All mathematical functions have the following behaviors:

* They return `NULL` if any of the input parameters is `NULL`.
* They return `NaN` if any of the arguments is `NaN`.

## Categories

| Category | Functions |
| --- | --- |
| Trigonometric | [`ACOS`](#acos)   [`ACOSH`](#acosh)   [`ASIN`](#asin)   [`ASINH`](#asinh)   [`ATAN`](#atan)   [`ATAN2`](#atan2)   [`ATANH`](#atanh)   [`COS`](#cos)   [`COSH`](#cosh)   [`COT`](#cot)   [`COTH`](#coth)   [`CSC`](#csc)   [`CSCH`](#csch)   [`SEC`](#sec)   [`SECH`](#sech)   [`SIN`](#sin)   [`SINH`](#sinh)   [`TAN`](#tan)   [`TANH`](#tanh) |
| Exponential and  logarithmic | [`EXP`](#exp)   [`LN`](#ln)   [`LOG`](#log)   [`LOG10`](#log10) |
| Rounding and  truncation | [`CEIL`](#ceil)   [`CEILING`](#ceiling)   [`FLOOR`](#floor)   [`ROUND`](#round)   [`TRUNC`](#trunc) |
| Power and  root | [`CBRT`](#cbrt)   [`POW`](#pow)   [`POWER`](#power)   [`SQRT`](#sqrt) |
| Sign | [`ABS`](#abs)   [`SIGN`](#sign) |
| Distance | [`COSINE_DISTANCE`](#cosine_distance)   [`EUCLIDEAN_DISTANCE`](#euclidean_distance) |
| Comparison | [`GREATEST`](#greatest)   [`LEAST`](#least) |
| Random number generator | [`RAND`](#rand) |
| Arithmetic and error handling | [`DIV`](#div)   [`IEEE_DIVIDE`](#ieee_divide)   [`IS_INF`](#is_inf)   [`IS_NAN`](#is_nan)   [`MOD`](#mod)   [`SAFE_ADD`](#safe_add)   [`SAFE_DIVIDE`](#safe_divide)   [`SAFE_MULTIPLY`](#safe_multiply)   [`SAFE_NEGATE`](#safe_negate)   [`SAFE_SUBTRACT`](#safe_subtract) |
| Bucket | [`RANGE_BUCKET`](#range_bucket) |

## Function list

| Name | Summary |
| --- | --- |
| [`ABS`](/bigquery/docs/reference/standard-sql/mathematical_functions#abs) | Computes the absolute value of `X`. |
| [`ACOS`](/bigquery/docs/reference/standard-sql/mathematical_functions#acos) | Computes the inverse cosine of `X`. |
| [`ACOSH`](/bigquery/docs/reference/standard-sql/mathematical_functions#acosh) | Computes the inverse hyperbolic cosine of `X`. |
| [`ASIN`](/bigquery/docs/reference/standard-sql/mathematical_functions#asin) | Computes the inverse sine of `X`. |
| [`ASINH`](/bigquery/docs/reference/standard-sql/mathematical_functions#asinh) | Computes the inverse hyperbolic sine of `X`. |
| [`ATAN`](/bigquery/docs/reference/standard-sql/mathematical_functions#atan) | Computes the inverse tangent of `X`. |
| [`ATAN2`](/bigquery/docs/reference/standard-sql/mathematical_functions#atan2) | Computes the inverse tangent of `X/Y`, using the signs of `X` and `Y` to determine the quadrant. |
| [`ATANH`](/bigquery/docs/reference/standard-sql/mathematical_functions#atanh) | Computes the inverse hyperbolic tangent of `X`. |
| [`AVG`](/bigquery/docs/reference/standard-sql/aggregate_functions#avg) | Gets the average of non-`NULL` values.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |
| [`AVG` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_avg) | `DIFFERENTIAL_PRIVACY`-supported `AVG`. |
| [`CBRT`](/bigquery/docs/reference/standard-sql/mathematical_functions#cbrt) | Computes the cube root of `X`. |
| [`CEIL`](/bigquery/docs/reference/standard-sql/mathematical_functions#ceil) | Gets the smallest integral value that isn't less than `X`. |
| [`CEILING`](/bigquery/docs/reference/standard-sql/mathematical_functions#ceiling) | Synonym of `CEIL`. |
| [`COS`](/bigquery/docs/reference/standard-sql/mathematical_functions#cos) | Computes the cosine of `X`. |
| [`COSH`](/bigquery/docs/reference/standard-sql/mathematical_functions#cosh) | Computes the hyperbolic cosine of `X`. |
| [`COSINE_DISTANCE`](/bigquery/docs/reference/standard-sql/mathematical_functions#cosine_distance) | Computes the cosine distance between two vectors. |
| [`COT`](/bigquery/docs/reference/standard-sql/mathematical_functions#cot) | Computes the cotangent of `X`. |
| [`COTH`](/bigquery/docs/reference/standard-sql/mathematical_functions#coth) | Computes the hyperbolic cotangent of `X`. |
| [`CSC`](/bigquery/docs/reference/standard-sql/mathematical_functions#csc) | Computes the cosecant of `X`. |
| [`CSCH`](/bigquery/docs/reference/standard-sql/mathematical_functions#csch) | Computes the hyperbolic cosecant of `X`. |
| [`DIV`](/bigquery/docs/reference/standard-sql/mathematical_functions#div) | Divides integer `X` by integer `Y`. |
| [`EXP`](/bigquery/docs/reference/standard-sql/mathematical_functions#exp) | Computes `e` to the power of `X`. |
| [`EUCLIDEAN_DISTANCE`](/bigquery/docs/reference/standard-sql/mathematical_functions#euclidean_distance) | Computes the Euclidean distance between two vectors. |
| [`FLOOR`](/bigquery/docs/reference/standard-sql/mathematical_functions#floor) | Gets the largest integral value that isn't greater than `X`. |
| [`GREATEST`](/bigquery/docs/reference/standard-sql/mathematical_functions#greatest) | Gets the greatest value among `X1,...,XN`. |
| [`IEEE_DIVIDE`](/bigquery/docs/reference/standard-sql/mathematical_functions#ieee_divide) | Divides `X` by `Y`, but doesn't generate errors for division by zero or overflow. |
| [`IS_INF`](/bigquery/docs/reference/standard-sql/mathematical_functions#is_inf) | Checks if `X` is positive or negative infinity. |
| [`IS_NAN`](/bigquery/docs/reference/standard-sql/mathematical_functions#is_nan) | Checks if `X` is a `NaN` value. |
| [`LEAST`](/bigquery/docs/reference/standard-sql/mathematical_functions#least) | Gets the least value among `X1,...,XN`. |
| [`LN`](/bigquery/docs/reference/standard-sql/mathematical_functions#ln) | Computes the natural logarithm of `X`. |
| [`LOG`](/bigquery/docs/reference/standard-sql/mathematical_functions#log) | Computes the natural logarithm of `X` or the logarithm of `X` to base `Y`. |
| [`LOG10`](/bigquery/docs/reference/standard-sql/mathematical_functions#log10) | Computes the natural logarithm of `X` to base 10. |
| [`MAX`](/bigquery/docs/reference/standard-sql/aggregate_functions#max) | Gets the maximum non-`NULL` value.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |
| [`MAX_BY`](/bigquery/docs/reference/standard-sql/aggregate_functions#max_by) | Synonym for `ANY_VALUE(x HAVING MAX y)`.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |
| [`MIN_BY`](/bigquery/docs/reference/standard-sql/aggregate_functions#min_by) | Synonym for `ANY_VALUE(x HAVING MIN y)`.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |
| [`MOD`](/bigquery/docs/reference/standard-sql/mathematical_functions#mod) | Gets the remainder of the division of `X` by `Y`. |
| [`POW`](/bigquery/docs/reference/standard-sql/mathematical_functions#pow) | Produces the value of `X` raised to the power of `Y`. |
| [`POWER`](/bigquery/docs/reference/standard-sql/mathematical_functions#power) | Synonym of `POW`. |
| [`RAND`](/bigquery/docs/reference/standard-sql/mathematical_functions#rand) | Generates a pseudo-random value of type `FLOAT64` in the range of `[0, 1)`. |
| [`RANGE_BUCKET`](/bigquery/docs/reference/standard-sql/mathematical_functions#range_bucket) | Scans through a sorted array and returns the 0-based position of a point's upper bound. |
| [`ROUND`](/bigquery/docs/reference/standard-sql/mathematical_functions#round) | Rounds `X` to the nearest integer or rounds `X` to `N` decimal places after the decimal point. |
| [`SAFE_ADD`](/bigquery/docs/reference/standard-sql/mathematical_functions#safe_add) | Equivalent to the addition operator (`X + Y`), but returns `NULL` if overflow occurs. |
| [`SAFE_DIVIDE`](/bigquery/docs/reference/standard-sql/mathematical_functions#safe_divide) | Equivalent to the division operator (`X / Y`), but returns `NULL` if an error occurs. |
| [`SAFE_MULTIPLY`](/bigquery/docs/reference/standard-sql/mathematical_functions#safe_multiply) | Equivalent to the multiplication operator (`X * Y`), but returns `NULL` if overflow occurs. |
| [`SAFE_NEGATE`](/bigquery/docs/reference/standard-sql/mathematical_functions#safe_negate) | Equivalent to the unary minus operator (`-X`), but returns `NULL` if overflow occurs. |
| [`SAFE_SUBTRACT`](/bigquery/docs/reference/standard-sql/mathematical_functions#safe_subtract) | Equivalent to the subtraction operator (`X - Y`), but returns `NULL` if overflow occurs. |
| [`SEC`](/bigquery/docs/reference/standard-sql/mathematical_functions#sec) | Computes the secant of `X`. |
| [`SECH`](/bigquery/docs/reference/standard-sql/mathematical_functions#sech) | Computes the hyperbolic secant of `X`. |
| [`SIGN`](/bigquery/docs/reference/standard-sql/mathematical_functions#sign) | Produces -1 , 0, or +1 for negative, zero, and positive arguments respectively. |
| [`SIN`](/bigquery/docs/reference/standard-sql/mathematical_functions#sin) | Computes the sine of `X`. |
| [`SINH`](/bigquery/docs/reference/standard-sql/mathematical_functions#sinh) | Computes the hyperbolic sine of `X`. |
| [`SQRT`](/bigquery/docs/reference/standard-sql/mathematical_functions#sqrt) | Computes the square root of `X`. |
| [`SUM`](/bigquery/docs/reference/standard-sql/aggregate_functions#sum) | Gets the sum of non-`NULL` values.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |
| [`SUM` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_sum) | `DIFFERENTIAL_PRIVACY`-supported `SUM`.   Gets the differentially-private sum of non-`NULL`, non-`NaN` values in a query with a `DIFFERENTIAL_PRIVACY` clause. |
| [`TAN`](/bigquery/docs/reference/standard-sql/mathematical_functions#tan) | Computes the tangent of `X`. |
| [`TANH`](/bigquery/docs/reference/standard-sql/mathematical_functions#tanh) | Computes the hyperbolic tangent of `X`. |
| [`TRUNC`](/bigquery/docs/reference/standard-sql/mathematical_functions#trunc) | Rounds a number like `ROUND(X)` or `ROUND(X, N)`, but always rounds towards zero and never overflows. |

## `ABS`

```
ABS(X)
```

**Description**

Computes absolute value. Returns an error if the argument is an integer and the
output value can't be represented as the same type; this happens only for the
largest negative input value, which has no positive representation.

| X | ABS(X) |
| --- | --- |
| 25 | 25 |
| -25 | 25 |
| `+inf` | `+inf` |
| `-inf` | `+inf` |

**Return Data Type**

| INPUT | `INT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| --- | --- | --- | --- | --- |
| OUTPUT | `INT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |

## `ACOS`

```
ACOS(X)
```

**Description**

Computes the principal value of the inverse cosine of X. The return value is in
the range [0,π]. Generates an error if X is a value outside of the
range [-1, 1].

| X | ACOS(X) |
| --- | --- |
| `+inf` | `NaN` |
| `-inf` | `NaN` |
| `NaN` | `NaN` |
| X < -1 | Error |
| X > 1 | Error |

## `ACOSH`

```
ACOSH(X)
```

**Description**

Computes the inverse hyperbolic cosine of X. Generates an error if X is a value
less than 1.

| X | ACOSH(X) |
| --- | --- |
| `+inf` | `+inf` |
| `-inf` | `NaN` |
| `NaN` | `NaN` |
| X < 1 | Error |

## `ASIN`

```
ASIN(X)
```

**Description**

Computes the principal value of the inverse sine of X. The return value is in
the range [-π/2,π/2]. Generates an error if X is outside of
the range [-1, 1].

| X | ASIN(X) |
| --- | --- |
| `+inf` | `NaN` |
| `-inf` | `NaN` |
| `NaN` | `NaN` |
| X < -1 | Error |
| X > 1 | Error |

## `ASINH`

```
ASINH(X)
```

**Description**

Computes the inverse hyperbolic sine of X. Doesn't fail.

| X | ASINH(X) |
| --- | --- |
| `+inf` | `+inf` |
| `-inf` | `-inf` |
| `NaN` | `NaN` |

## `ATAN`

```
ATAN(X)
```

**Description**

Computes the principal value of the inverse tangent of X. The return value is
in the range [-π/2,π/2]. Doesn't fail.

| X | ATAN(X) |
| --- | --- |
| `+inf` | π/2 |
| `-inf` | -π/2 |
| `NaN` | `NaN` |

## `ATAN2`

```
ATAN2(X, Y)
```

**Description**

Calculates the principal value of the inverse tangent of X/Y using the signs of
the two arguments to determine the quadrant. The return value is in the range
[-π,π].

| X | Y | ATAN2(X, Y) |
| --- | --- | --- |
| `NaN` | Any value | `NaN` |
| Any value | `NaN` | `NaN` |
| 0.0 | 0.0 | 0.0 |
| Positive Finite value | `-inf` | π |
| Negative Finite value | `-inf` | -π |
| Finite value | `+inf` | 0.0 |
| `+inf` | Finite value | π/2 |
| `-inf` | Finite value | -π/2 |
| `+inf` | `-inf` | ¾π |
| `-inf` | `-inf` | -¾π |
| `+inf` | `+inf` | π/4 |
| `-inf` | `+inf` | -π/4 |

## `ATANH`

```
ATANH(X)
```

**Description**

Computes the inverse hyperbolic tangent of X. Generates an error if X is outside
of the range (-1, 1).

| X | ATANH(X) |
| --- | --- |
| `+inf` | `NaN` |
| `-inf` | `NaN` |
| `NaN` | `NaN` |
| X < -1 | Error |
| X > 1 | Error |

## `CBRT`

```
CBRT(X)
```

**Description**

Computes the cube root of `X`. `X` can be any data type
that [coerces to `FLOAT64`](/bigquery/docs/reference/standard-sql/conversion_rules).
Supports the `SAFE.` prefix.

| X | CBRT(X) |
| --- | --- |
| `+inf` | `inf` |
| `-inf` | `-inf` |
| `NaN` | `NaN` |
| `0` | `0` |
| `NULL` | `NULL` |

**Return Data Type**

`FLOAT64`

**Example**

```
SELECT CBRT(27) AS cube_root;

/*--------------------+
 | cube_root          |
 +--------------------+
 | 3.0000000000000004 |
 +--------------------*/
```

## `CEIL`

```
CEIL(X)
```

**Description**

Returns the smallest integral value that isn't less than X.

| X | CEIL(X) |
| --- | --- |
| 2.0 | 2.0 |
| 2.3 | 3.0 |
| 2.8 | 3.0 |
| 2.5 | 3.0 |
| -2.3 | -2.0 |
| -2.8 | -2.0 |
| -2.5 | -2.0 |
| 0 | 0 |
| `+inf` | `+inf` |
| `-inf` | `-inf` |
| `NaN` | `NaN` |

**Return Data Type**

| INPUT | `INT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |
| --- | --- | --- | --- | --- |
| OUTPUT | `FLOAT64` | `NUMERIC` | `BIGNUMERIC` | `FLOAT64` |

## `CEILING`

```
CEILING(X)
```

**Description**

Synonym of CEIL(X)

## `COS`

```
COS(X)
```

**Description**

Computes the cosine of X where X is specified in radians. Never fails.

| X | COS(X) |
| --- | --- |
| `+inf` | `NaN` |
| `-inf` | `NaN` |
| `NaN` | `NaN` |

## `COSH`

```
COSH(X)
```

**Description**

Computes the hyperbolic cosine of X where X is specified in radians.
Generates an error if overflow occurs.

| X | COSH(X) |
| --- | --- |
| `+inf` | `+inf` |
| `-inf` | `+inf` |
| `NaN` | `NaN` |

## `COSINE_DISTANCE`

```
COSINE_DISTANCE(vector1, vector2)
```

**Description**

Computes the [cosine distance](https://en.wikipedia.org/wiki/Cosine_similarity#Cosine_distance) between two vectors.

**Definitions**

* `vector1`: A vector that's represented by an
  `ARRAY<T>` value or a sparse vector that is
  represented by an `ARRAY<STRUCT<dimension,magnitude>>` value.
* `vector2`: A vector that's represented by an
  `ARRAY<T>` value or a sparse vector that is
  represented by an `ARRAY<STRUCT<dimension,magnitude>>` value.

**Details**

* `ARRAY<T>` can be used to represent a vector. Each zero-based index in this
  array represents a dimension. The value for each element in this array
  represents a magnitude.

  `T` can represent the following and must be the same for both
  vectors:

  + `FLOAT64`

  In the following example vector, there are four dimensions. The magnitude
  is `10.0` for dimension `0`, `55.0` for dimension `1`, `40.0` for
  dimension `2`, and `34.0` for dimension `3`:

  ```
  [10.0, 55.0, 40.0, 34.0]
  ```
* `ARRAY<STRUCT<dimension,magnitude>>` can be used to represent a
  sparse vector. With a sparse vector, you only need to include
  dimension-magnitude pairs for non-zero magnitudes. If a magnitude isn't
  present in the sparse vector, the magnitude is implicitly understood to be
  zero.

  For example, if you have a vector with 10,000 dimensions, but only 10
  dimensions have non-zero magnitudes, then the vector is a sparse vector.
  As a result, it's more efficient to describe a sparse vector by only
  mentioning its non-zero magnitudes.

  In `ARRAY<STRUCT<dimension,magnitude>>`, `STRUCT<dimension,magnitude>`
  represents a dimension-magnitude pair for each non-zero magnitude in a
  sparse vector. These parts need to be included for each dimension-magnitude
  pair:

  + `dimension`: A `STRING` or `INT64` value that represents a
    dimension in a vector.
  + `magnitude`: A `FLOAT64` value that represents a
    non-zero magnitude for a specific dimension in a vector.

  You don't need to include empty dimension-magnitude pairs in a
  sparse vector. For example, the following sparse vector and
  non-sparse vector are equivalent:

  ```
  -- sparse vector ARRAY<STRUCT<INT64, FLOAT64>>
  [(1, 10.0), (2, 30.0), (5, 40.0)]
  ```

  ```
  -- vector ARRAY<FLOAT64>
  [0.0, 10.0, 30.0, 0.0, 0.0, 40.0]
  ```

  In a sparse vector, dimension-magnitude pairs don't need to be in any
  particular order. The following sparse vectors are equivalent:

  ```
  [('a', 10.0), ('b', 30.0), ('d', 40.0)]
  ```

  ```
  [('d', 40.0), ('a', 10.0), ('b', 30.0)]
  ```
* Both non-sparse vectors
  in this function must share the same dimensions, and if they don't, an error
  is produced.
* A vector can't be a zero vector. A vector is a zero vector if it has
  no dimensions or all dimensions have a magnitude of `0`, such as `[]` or
  `[0.0, 0.0]`. If a zero vector is encountered, an error is produced.
* An error is produced if a magnitude in a vector is `NULL`.
* If a vector is `NULL`, `NULL` is returned.

**Return type**

`FLOAT64`

**Examples**

In the following example, non-sparsevectors
are used to compute the cosine distance:

```
SELECT COSINE_DISTANCE([1.0, 2.0], [3.0, 4.0]) AS results;

/*----------+
 | results  |
 +----------+
 | 0.016130 |
 +----------*/
```

In the following example, sparse vectors are used to compute the
cosine distance:

```
SELECT COSINE_DISTANCE(
 [(1, 1.0), (2, 2.0)],
 [(2, 4.0), (1, 3.0)]) AS results;

 /*----------+
  | results  |
  +----------+
  | 0.016130 |
  +----------*/
```

The ordering of numeric values in a vector doesn't impact the results
produced by this function. For example these queries produce the same results
even though the numeric values in each vector is in a different order:

```
SELECT COSINE_DISTANCE([1.0, 2.0], [3.0, 4.0]) AS results;
```

```
SELECT COSINE_DISTANCE([2.0, 1.0], [4.0, 3.0]) AS results;
```

```
SELECT COSINE_DISTANCE([(1, 1.0), (2, 2.0)], [(1, 3.0), (2, 4.0)]) AS results;
```

```
 /*----------+
  | results  |
  +----------+
  | 0.016130 |
  +----------*/
```

In the following example, the function can't compute cosine distance against
the first vector, which is a zero vector:

```
-- ERROR
SELECT COSINE_DISTANCE([0.0, 0.0], [3.0, 4.0]) AS results;
```

```
-- ERROR
SELECT COSINE_DISTANCE([(1, 0.0), (2, 0.0)], [(1, 3.0), (2, 4.0)]) AS results;
```

Both non-sparse vectors must have the same
dimensions. If not, an error is produced. In the following example, the
first vector has two dimensions and the second vector has three:

```
-- ERROR
SELECT COSINE_DISTANCE([9.0, 7.0], [8.0, 4.0, 5.0]) AS results;
```

If you use sparse vectors and you repeat a dimension, an error is
produced:

```
-- ERROR
SELECT COSINE_DISTANCE(
  [(1, 9.0), (2, 7.0), (2, 8.0)], [(1, 8.0), (2, 4.0), (3, 5.0)]) AS results;
```

## `COT`

```
COT
```