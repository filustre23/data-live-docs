* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.MULTI\_HOT\_ENCODER function

This document describes the `ML.MULTI_HOT_ENCODER` function, which lets you
encode a string array expression by using a
[multi-hot](/bigquery/docs/auto-preprocessing#feature-transform)
encoding scheme.

The encoding vocabulary is sorted alphabetically. `NULL` values and categories
that aren't in the vocabulary are encoded with an `index` value of `0`.

When used in the
[`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform),
the vocabulary calculated during training, along with the top *k* and frequency
threshold values that you specified, are automatically used in prediction.

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.MULTI_HOT_ENCODER(array_expression [, top_k] [, frequency_threshold]) OVER()
```

### Arguments

`ML.MULTI_HOT_ENCODER` takes the following arguments:

* `array_expression`: the `ARRAY<STRING>` expression to encode.
* `top_k`: an `INT64` value that specifies the number of categories
  included in the encoding vocabulary. The function selects the `top_k`
  most frequent categories in the data and uses those; categories below this
  threshold are encoded to `0`. This value must be less than `1,000,000`
  to avoid problems due to high dimensionality. The default value is `32,000`.
* `frequency_threshold`: an `INT64` value that limits the categories
  included in the encoding vocabulary based on category frequency. The
  function uses categories whose frequency is greater than or equal to
  `frequency_threshold`; categories below this threshold are encoded to `0`.
  The default value is `5`.

## Output

`ML.MULTI_HOT_ENCODER` returns an array of struct values in the form `ARRAY<STRUCT<INT64, FLOAT64>>`. The first element in the struct provides the
index of the encoded string expression, and the second element provides the
value of the encoded string expression.

## Example

The following example performs multi-hot encoding on a set of string array
expressions. It limits the encoding vocabulary to the three categories that
occur the most frequently in the data and that also occur one or more times.

```
SELECT f[OFFSET(0)] AS f0, ML.MULTI_HOT_ENCODER(f, 3, 1) OVER () AS output
FROM
  (
    SELECT ['a', 'b', 'b', 'c', NULL] AS f
    UNION ALL
    SELECT ['c', 'c', 'd', 'd', NULL] AS f
  )
ORDER BY f[OFFSET(0)];
```

The output looks similar to the following:

```
+------+-----------------------------+
|  f0  | output.index | output.value |
+------+--------------+--------------+
|  a   |  1           |  1.0         |
|      |  2           |  1.0         |
|      |  3           |  1.0         |
|      |  0           |  1.0         |
|  c   |  3           |  1.0         |
|      |  0           |  1.0         |
+------+-----------------------------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-13 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-13 UTC."],[],[]]