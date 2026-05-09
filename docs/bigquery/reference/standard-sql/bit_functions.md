* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback

# Bit functions Stay organized with collections Save and categorize content based on your preferences.

GoogleSQL for BigQuery supports the following bit functions.

## Function list

| Name | Summary |
| --- | --- |
| [`BIT_AND`](/bigquery/docs/reference/standard-sql/aggregate_functions#bit_and) | Performs a bitwise AND operation on an expression.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |
| [`BIT_COUNT`](/bigquery/docs/reference/standard-sql/bit_functions#bit_count) | Gets the number of bits that are set in an input expression. |
| [`BIT_OR`](/bigquery/docs/reference/standard-sql/aggregate_functions#bit_or) | Performs a bitwise OR operation on an expression.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |
| [`BIT_XOR`](/bigquery/docs/reference/standard-sql/aggregate_functions#bit_xor) | Performs a bitwise XOR operation on an expression.  For more information, see [Aggregate functions](/bigquery/docs/reference/standard-sql/aggregate_functions). |

## `BIT_COUNT`

```
BIT_COUNT(expression)
```

**Description**

The input, `expression`, must be an
integer or `BYTES`.

Returns the number of bits that are set in the input `expression`.
For signed integers, this is the number of bits in two's complement form.

**Return Data Type**

`INT64`

**Example**

```
SELECT a, BIT_COUNT(a) AS a_bits, FORMAT("%T", b) as b, BIT_COUNT(b) AS b_bits
FROM UNNEST([
  STRUCT(0 AS a, b'' AS b), (0, b'\x00'), (5, b'\x05'), (8, b'\x00\x08'),
  (0xFFFF, b'\xFF\xFF'), (-2, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFE'),
  (-1, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF'),
  (NULL, b'\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF\xFF')
]) AS x;

/*-------+--------+---------------------------------------------+--------+
 | a     | a_bits | b                                           | b_bits |
 +-------+--------+---------------------------------------------+--------+
 | 0     | 0      | b""                                         | 0      |
 | 0     | 0      | b"\x00"                                     | 0      |
 | 5     | 2      | b"\x05"                                     | 2      |
 | 8     | 1      | b"\x00\x08"                                 | 1      |
 | 65535 | 16     | b"\xff\xff"                                 | 16     |
 | -2    | 63     | b"\xff\xff\xff\xff\xff\xff\xff\xfe"         | 63     |
 | -1    | 64     | b"\xff\xff\xff\xff\xff\xff\xff\xff"         | 64     |
 | NULL  | NULL   | b"\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff" | 80     |
 +-------+--------+---------------------------------------------+--------*/
```




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-08 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-08 UTC."],[],[]]