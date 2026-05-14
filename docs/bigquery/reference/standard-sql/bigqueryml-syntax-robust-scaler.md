* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.ROBUST\_SCALER function

This document describes the `ML.ROBUST_SCALER` function, which lets you scale a
numerical expression by using statistics that are robust to outliers. The
function performs the scaling by removing the
[median](https://en.wikipedia.org/wiki/Median) and scaling
the data according to the [quantile](https://en.wikipedia.org/wiki/Quantile)
range.

When used in the
[`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform),
the median and quantile range calculated during training are automatically
used in prediction.

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.ROBUST_SCALER(numerical_expression [, quantile_range] [, with_median] [, with_quantile_range]) OVER()
```

### Arguments

`ML.ROBUST_SCALER` takes the following arguments:

* `numerical_expression`: the
  [numerical](/bigquery/docs/reference/standard-sql/data-types#numeric_types)
  expression to scale.
* `quantile_range`: an array of two `INT64` elements that specifies
  the quantile range. The first element provides the lower boundary of the
  range. It must be greater than `0`. The second element provides the upper
  boundary of the range. It must be greater than the first element but less
  than `100`. The default value is `[25, 75]`.
* `with_median`: a `BOOL` value that specifies whether the data
  is centered. If `TRUE`, the function centers the data by removing the
  median before scaling. The default value is `TRUE`.
* `with_quantile_range`: a `BOOL` value that specifies whether the
  data is scaled to the quantile range. If `TRUE`, the data is scaled. The
  default value is `TRUE`.

## Output

`ML.ROBUST_SCALER` returns a `FLOAT64` value that represents the scaled
numerical expression.

## Example

The following example centers a set of numerical expressions and then
scales it to the range `[25, 75]`:

```
SELECT f, ML.ROBUST_SCALER(f) OVER () AS output
FROM
  UNNEST([NULL, -3, 1, 2, 3, 4, 5]) AS f
ORDER BY f;
```

The output looks similar to the following:

```
+------+---------------------+
|  f   |       output        |
+------+---------------------+
| NULL |                NULL |
|   -3 | -1.6666666666666667 |
|    1 | -0.3333333333333333 |
|    2 |                 0.0 |
|    3 |  0.3333333333333333 |
|    4 |  0.6666666666666666 |
|    5 |                 1.0 |
+------+---------------------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-13 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-13 UTC."],[],[]]