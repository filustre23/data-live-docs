* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.IMPUTER function

This document describes the `ML.IMPUTER` function, which lets you replace
`NULL` values in a string or numerical expression. You can replace `NULL` values
with the most frequently used value for string expressions, or the
[mean](https://en.wikipedia.org/wiki/Mean) or
[median](https://en.wikipedia.org/wiki/Median) value for numerical expressions.

When used in the
[`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform),
the values calculated during training for mean, median, and most frequently
used value are automatically used in prediction.

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.IMPUTER(expression, strategy) OVER()
```

## Arguments

`ML.IMPUTER` takes the following arguments:

* `expression`: the
  [numerical](/bigquery/docs/reference/standard-sql/data-types#numeric_types)
  or `STRING` expression to impute.
* `strategy`: a `STRING` value that specifies how to replace `NULL` values.
  Valid values are as follows:
  + `mean`: the mean of `expression`. You can only use this value with
    numerical expressions.
  + `median`: the median of `expression`. You can only use this value with
    numerical expressions.
  + `most_frequent`: the most frequent value in `expression`.

## Output

`ML.IMPUTER` returns a `FLOAT64` (for numerical expressions) or `STRING`
(for string expressions) value that contains the replacement for the
`NULL` value.

## Examples

**Example 1**

The following example imputes numerical expressions:

```
SELECT f, ML.IMPUTER(f, 'mean') OVER () AS output
FROM
  UNNEST([NULL, -3, -3, -3, 1, 2, 3, 4, 5]) AS f
ORDER BY f;
```

The output looks similar to the following:

```
+------+--------+
|  f   | output |
+------+--------+
| NULL |   0.75 |
|   -3 |   -3.0 |
|   -3 |   -3.0 |
|   -3 |   -3.0 |
|    1 |    1.0 |
|    2 |    2.0 |
|    3 |    3.0 |
|    4 |    4.0 |
|    5 |    5.0 |
+------+--------+
```

**Example 2**

The following example imputes string expressions:

```
SELECT f, ML.IMPUTER(f, 'most_frequent') OVER () AS output
FROM
  UNNEST([NULL, NULL, NULL, NULL, 'a', 'a', 'b', 'b', 'c', 'c', 'c']) AS f
ORDER BY f;
```

The output looks similar to the following:

```
+------+--------+
|  f   | output |
+------+--------+
| NULL | c      |
| NULL | c      |
| NULL | c      |
| NULL | c      |
| a    | a      |
| a    | a      |
| b    | b      |
| b    | b      |
| c    | c      |
| c    | c      |
| c    | c      |
+------+--------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-13 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-13 UTC."],[],[]]