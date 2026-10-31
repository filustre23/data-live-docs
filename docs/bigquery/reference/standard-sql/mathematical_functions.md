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
| [`AVG` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_avg) | `DIFFERENTIAL_PRIVACY`-supported `AVG`.   Gets the differentially-private average of non-`NULL`, non-`NaN` values in a query with a `DIFFERENTIAL_PRIVACY` clause.   For more information, see [Differential privacy functions](/bigquery/docs/reference/standard-sql/aggregate-dp-functions). |
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
| [`SUM` (Differential Privacy)](/bigquery/docs/reference/standard-sql/aggregate-dp-functions#dp_sum) | `DIFFERENTIAL_PRIVACY`-supported `SUM`.   Gets the differentially-private sum of non-`NULL`, non-`NaN` values in a query with a `DIFFERENTIAL_PRIVACY` clause.   For more information, see [Differential privacy functions](/bigquery/docs/reference/standard-sql/aggregate-dp-functions). |
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