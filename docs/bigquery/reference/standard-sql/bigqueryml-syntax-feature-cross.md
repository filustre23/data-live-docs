* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.FEATURE\_CROSS function

This document describes the `ML.FEATURE_CROSS` function, which lets you create
[feature crosses](https://developers.google.com/machine-learning/crash-course/feature-crosses/video-lecture).

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.FEATURE_CROSS(struct_categorical_features [, degree])
```

### Arguments

`ML.FEATURE_CROSS` takes the following arguments:

* `struct_categorical_features`: a `STRUCT<STRING>` value that specifies
  the categorical features to cross. The maximum number of input features is 10.
  Don't specify unnamed features or duplicate features in
  `struct_numerical_features`.
* `degree`: an `INT64` value that specifies the highest degree of all
  combinations of features in the range of `[2, 4]`. The default value is `2`.

## Output

`ML.FEATURE_CROSS` returns a `STRUCT<STRING>` value that identifies all
combinations of the crossed categorical features with a degree no larger than
the `degree` value, except for 1-degree items (the original features) and
self-crossing items. The field names in the output struct are concatenations
of the original feature names.

## Example

The following example crosses three features:

```
SELECT
  ML.FEATURE_CROSS(STRUCT('a' AS f1, 'b' AS f2, 'c' AS f3)) AS output;
```

The output looks similar to the following:

```
+---------------------------------------------+
|                   output                    |
+---------------------------------------------+
| {"f1_f2":"a_b","f1_f3":"a_c","f2_f3":"b_c"} |
+---------------------------------------------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-08 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-08 UTC."],[],[]]