* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.MAX\_ABS\_SCALER function

This document describes the `ML.MAX_ABS_SCALER` function, which lets you
scale a numerical expression to the range
`[-1, 1]` by dividing with the maximum absolute value. It doesn't
shift or center the data, and so doesn't destroy any sparsity.

When used in the
[`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform),
the maximum absolute value calculated during training is automatically
used in prediction.

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.MAX_ABS_SCALER(numerical_expression) OVER()
```

### Arguments

`ML.MAX_ABS_SCALER` takes the following argument:

* `numerical_expression`: the
  [numerical](/bigquery/docs/reference/standard-sql/data-types#numeric_types)
  expression to scale.

## Output

`ML.MAX_ABS_SCALER` returns a `FLOAT64` value that represents the scaled
numerical expression.

## Example

The following example scales a set of numerical expressions to have values
between `-1` and `1`:

```
SELECT f, ML.MAX_ABS_SCALER(f) OVER () AS output
FROM
  UNNEST([NULL, -3, 1, 2, 3, 4, 5]) AS f
ORDER BY f;
```

The output looks similar to the following:

```
+------+--------+
|  f   | output |
+------+--------+
| NULL |   NULL |
|   -3 |   -0.6 |
|    1 |    0.2 |
|    2 |    0.4 |
|    3 |    0.6 |
|    4 |    0.8 |
|    5 |    1.0 |
+------+--------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-08 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-08 UTC."],[],[]]