* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.QUANTILE\_BUCKETIZE function

This document describes the `ML.QUANTILE_BUCKETIZE` function, which lets you
break a continuous numerical feature into buckets based on quantiles.

When used in the
[`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform),
the same quantiles are automatically used in prediction.

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.QUANTILE_BUCKETIZE(numerical_expression, num_buckets [, output_format]) OVER()
```

### Arguments

`ML.QUANTILE_BUCKETIZE` takes the following arguments:

* `numerical_expression`: the
  [numerical](/bigquery/docs/reference/standard-sql/data-types#numeric_types)
  expression to bucketize.
* `num_buckets`: an `INT64` value that specifies the number of buckets to split
  `numerical_expression` into.
* `output_format`: a `STRING` value that specifies the output format of the bucket. Valid output formats are as follows:
  + `bucket_names`: returns a `STRING` value in the format `bin_<bucket_index>`. For example, `bin_3`. The `bucket_index` value starts at 1. This is the default bucket format.
  + `bucket_ranges`: returns a `STRING` value in the format `[lower_bound, upper_bound)` in [interval notation](https://en.wikipedia.org/wiki/Interval_(mathematics)). For example, `(-inf, 2.5)`, `[2.5, 4.6)`, `[4.6, +inf)`.
  + `bucket_ranges_json`: returns a JSON-formatted `STRING` value in the format `{"start": "lower_bound", "end": "upper_bound"}`. For example, `{"start": "-Infinity", "end": "2.5"}`, `{"start": "2.5", "end": "4.6"}`, `{"start": "4.6", "end": "Infinity"}`. The inclusivity and exclusivity of the lower and upper bound follow the same pattern as the `bucket_ranges` option.

## Output

`ML.QUANTILE_BUCKETIZE` returns a `STRING` value that contains the name of the bucket, in the format specified by the `output_format` argument.

## Example

The following example breaks a numerical expression of five elements into
three buckets:

```
SELECT
  f,
  ML.QUANTILE_BUCKETIZE(f, 3) OVER() AS bucket,
  ML.QUANTILE_BUCKETIZE(f, 3, "bucket_ranges") OVER() AS bucket_ranges,
  ML.QUANTILE_BUCKETIZE(f, 3, "bucket_ranges_json") OVER() AS bucket_ranges_json
FROM
  UNNEST([1,2,3,4,5]) AS f
ORDER BY f;
```

The output looks similar to the following:

```
+---+--------+---------------+------------------------------------+
| f | bucket | bucket_ranges | bucket_ranges_json                 |
|---|--------|---------------|------------------------------------|
| 1 | bin_1  | (-inf, 2)     | {"start": "-Infinity", "end": "2"} |
| 2 | bin_2  | [2, 4)        | {"start": "2", "end": "4"}         |
| 3 | bin_2  | [2, 4)        | {"start": "2", "end": "4"}         |
| 4 | bin_3  | [4, +inf)     | {"start": "4", "end": "Infinity"}  |
| 5 | bin_3  | [4, +inf)     | {"start": "4", "end": "Infinity"}  |
+---+--------+---------------+------------------------------------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-13 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-13 UTC."],[],[]]