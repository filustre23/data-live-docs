* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.POLYNOMIAL\_EXPAND function

This document describes the `ML.POLYNOMIAL_EXPAND` function, which lets you
calculate all polynomial combinations of the input features.

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.POLYNOMIAL_EXPAND(struct_numerical_features [, degree])
```

### Arguments

`ML.POLYNOMIAL_EXPAND` takes the following arguments:

* `struct_numerical_features`: a `STRUCT` value that contains the
  [numerical](/bigquery/docs/reference/standard-sql/data-types#numeric_types)
  input features to expand. You can specify less than or equal to `10`
  input features. Don't specify unnamed features or duplicate features.
* `degree`: an `INT64` value that specifies the highest degree of
  all combinations in the range of `[1, 4]`. The default value is `2`.

## Output

`ML.POLYNOMIAL_EXPAND` returns a `STRUCT<STRING>` value that contain all
polynomial combinations of the numerical input features with a degree no larger
than the passed-in degree, including the original features. The field names of
the output struct are concatenations of the original feature names.

## Example

The following example calculates the polynomial expansion of two
numerical features:

```
SELECT
  ML.POLYNOMIAL_EXPAND(STRUCT(2 AS f1, 3 AS f2)) AS output;
```

The output looks similar to the following:

```
+-------------------------------------------------------------------+
|                              output                               |
+-------------------------------------------------------------------+
| {"f1":"2.0","f1_f1":"4.0","f1_f2":"6.0","f2":"3.0","f2_f2":"9.0"} |
+-------------------------------------------------------------------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-04-29 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-04-29 UTC."],[],[]]