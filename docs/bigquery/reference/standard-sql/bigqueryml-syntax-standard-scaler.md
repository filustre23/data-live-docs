* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.STANDARD\_SCALER function

This document describes the `ML.STANDARD_SCALER` function, which lets you scale
a numerical expression by using
[z-score](https://developers.google.com/machine-learning/data-prep/transform/normalization#z-score).

When used in the
[`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform),
the [standard deviation](https://en.wikipedia.org/wiki/Standard_deviation) and
[mean](https://en.wikipedia.org/wiki/Mean) values calculated to standardize the
expression are automatically used in prediction.

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.STANDARD_SCALER(numerical_expression) OVER()
```

### Arguments

`ML.STANDARD_SCALER` takes the following argument:

* `numerical_expression`: the
  [numerical](/bigquery/docs/reference/standard-sql/data-types#numeric_types)
  expression to scale.

## Output

`ML.STANDARD_SCALER` returns a `FLOAT64` value that represents the scaled
numerical expression.

## Example

The following example scales a set of numerical expressions to have a
mean of `0` and standard deviation of `1`:

```
SELECT
  f, ML.STANDARD_SCALER(f) OVER() AS output
FROM
  UNNEST([1,2,3,4,5]) AS f;
```

The output looks similar to the following:

```
+---+---------------------+
| f |       output        |
+---+---------------------+
| 1 | -1.2649110640673518 |
| 5 |  1.2649110640673518 |
| 2 | -0.6324555320336759 |
| 4 |  0.6324555320336759 |
| 3 |                 0.0 |
+---+---------------------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-29 UTC."],[],[]]