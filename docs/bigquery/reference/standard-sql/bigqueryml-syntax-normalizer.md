* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.NORMALIZER function

This document describes the `ML.NORMALIZER` function, which lets you normalize
an array of numerical expressions using a given
[p-norm](https://ncatlab.org/nlab/show/p-norm).

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.NORMALIZER(array_expression [, p])
```

### Arguments

`ML.NORMALIZER` takes the following arguments:

* `array_expression`: an array of
  [numerical](/bigquery/docs/reference/standard-sql/data-types#numeric_types)
  expressions to normalize.
* `p`: a `FLOAT64` value that specifies the degree of p-norm. This
  can be `0.0`, any value greater than or equal to `1.0`, or
  `CAST('+INF' AS FLOAT64)`. The default value is `2`.

## Output

`ML.NORMALIZER` returns an array of `FLOAT64` values that represent the
normalized numerical expressions.

## Example

The following example normalizes a set of numerical expressions using a p-norm
of `2`:

```
SELECT ML.NORMALIZER([4.0, 1.0, 2.0, 2.0, 0.0]) AS output;
```

The output looks similar to the following:

```
+--------+
| output |
+--------+
| 0.8    |
| 0.2    |
| 0.4    |
| 0.4    |
| 0.0    |
+--------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-13 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-13 UTC."],[],[]]