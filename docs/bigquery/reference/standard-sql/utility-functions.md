* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Utility functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following utility functions.

## Function list

| Name | Summary |
| --- | --- |
| [`GENERATE_UUID`](/bigquery/docs/reference/standard-sql/utility-functions#generate_uuid) | Produces a random universally unique identifier (UUID) as a `STRING` value. |
| [`TYPEOF`](/bigquery/docs/reference/standard-sql/utility-functions#typeof) | Gets the name of the data type for an expression. |

## `GENERATE_UUID`

```
GENERATE_UUID()
```

**Description**

Returns a random universally unique identifier (UUID) as a `STRING`.
The returned `STRING` consists of 32 hexadecimal
digits in five groups separated by hyphens in the form 8-4-4-4-12. The
hexadecimal digits represent 122 random bits and 6 fixed bits, in compliance
with [RFC 4122 section 4.4](https://tools.ietf.org/html/rfc4122#section-4.4).
The returned `STRING` is lowercase.

**Return Data Type**

STRING

**Example**

The following query generates a random UUID.

```
SELECT GENERATE_UUID() AS uuid;

/*--------------------------------------+
 | uuid                                 |
 +--------------------------------------+
 | 4192bff0-e1e0-43ce-a4db-912808c32493 |
 +--------------------------------------*/
```

## `TYPEOF`

```
TYPEOF(expression)
```

**Description**

Takes an expression and gets the name of the data type for that
expression.

**Return type**

`STRING`

**Examples**

The following example produces the name of the data type for the expression
passed into the `TYPEOF` function. When `NULL` is passed in, the
[supertype](/bigquery/docs/reference/standard-sql/conversion_rules#supertypes), `INT64`, is produced.

```
SELECT
  TYPEOF(NULL) AS A,
  TYPEOF('hello') AS B,
  TYPEOF(12+1) AS C,
  TYPEOF(4.7) AS D

/*-------+--------+-------+--------+
 | A     | B      | C     | D      |
 +-------+--------+-------+--------+
 | INT64 | STRING | INT64 | FLOAT64 |
 +-------+--------+-------+--------*/
```

The following example produces the name of the data type for field `y` in a
struct.

```
SELECT
  TYPEOF(STRUCT<x INT64, y STRING>(25, 'apples')) AS struct_type,
  TYPEOF(STRUCT<x INT64, y STRING>(25, 'apples').y) AS field_type;

/*---------------------------+------------+
 | struct_type               | field_type |
 +---------------------------+------------+
 | STRUCT<x INT64, y STRING> | STRING     |
 +---------------------------+------------*/
```

The following example produces the name of the data type for elements in an
array.

```
SELECT
  TYPEOF(ARRAY<INT64>[25, 32]) AS array_type,
  TYPEOF(ARRAY<INT64>[25, 32][0]) AS element_type;

/*--------------+--------------+
 | array_type   | element_type |
 +--------------+--------------+
 | ARRAY<INT64> | INT64        |
 +--------------+--------------*/
```




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-08 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-08 UTC."],[],[]]