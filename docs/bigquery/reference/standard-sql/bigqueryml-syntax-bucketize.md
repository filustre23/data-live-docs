* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.BUCKETIZE function

This document describes the `ML.BUCKETIZE` function, which lets you split
a numerical expression into buckets.

You can use this function with models that support
[manual feature preprocessing](/bigquery/docs/manual-preprocessing). For more
information, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Syntax

```
ML.BUCKETIZE(numerical_expression, array_split_points [, exclude_boundaries] [, output_format])
```

### Arguments

`ML.BUCKETIZE` takes the following arguments:

* `numerical_expression`: the
  [numerical](/bigquery/docs/reference/standard-sql/data-types#numeric_types)
  expression to bucketize.
* `array_split_points`: an array of numerical values that provide the
  points at which to split the `numerical_expression` value. The
  numerical values in the array must be finite, so not `-inf`, `inf`, or `NaN`.
  Provide the numerical values in order, lowest to highest. The range of
  possible buckets is determined by the upper and lower boundaries of the array.
  For example, if the `array_split_points` value is `[1, 2, 3, 4]`, then there
  are five potential buckets that the `numerical_expression` value can be
  bucketized into.
* `exclude_boundaries`: a `BOOL` value that determines whether
  the upper and lower boundaries from `array_split_points` are used.
  If `TRUE`, then the boundary values aren't used to create buckets. For
  example, if the `array_split_points` value is `[1, 2, 3, 4]` and
  `exclude_boundaries` is `TRUE`, then there are three potential buckets
  that the `numerical_expression` value can be bucketized into.
  The default value is `FALSE`.
* `output_format`: a `STRING` value that specifies the output format of the bucket. Valid output formats are as follows:
  + `bucket_names`: returns a `STRING` value in the format `bin_<bucket_index>`. For example, `bin_3`. The `bucket_index` value starts at 1. This is the default bucket format.
  + `bucket_ranges`: returns a `STRING` value in the format `[lower_bound, upper_bound)` in [interval notation](https://en.wikipedia.org/wiki/Interval_(mathematics)). For example, `(-inf, 2.5)`, `[2.5, 4.6)`, `[4.6, +inf)`.
  + `bucket_ranges_json`: returns a JSON-formatted `STRING` value in the format `{"start": "lower_bound", "end": "upper_bound"}`. For example, `{"start": "-Infinity", "end": "2.5"}`, `{"start": "2.5", "end": "4.6"}`, `{"start": "4.6", "end": "Infinity"}`. The inclusivity and exclusivity of the lower and upper bound follow the same pattern as the `bucket_ranges` option.

## Output

`ML.BUCKETIZE` returns a `STRING` value that contains the name of the bucket, in the format specified by the `output_format` argument.

## Example

The following example bucketizes a numerical expression both with and without
boundaries:

```
SELECT
  ML.BUCKETIZE(2.5, [1, 2, 3]) AS bucket,
  ML.BUCKETIZE(2.5, [1, 2, 3], TRUE) AS bucket_without_boundaries,
  ML.BUCKETIZE(2.5, [1, 2, 3], FALSE, "bucket_ranges") AS bucket_ranges,
  ML.BUCKETIZE(2.5, [1, 2, 3], FALSE, "bucket_ranges_json") AS bucket_ranges_json;
```

The output looks similar to the following:

```
+--------+---------------------------+---------------+----------------------------+
| bucket | bucket_without_boundaries | bucket_ranges | bucket_ranges_json         |
|--------|---------------------------|---------------|----------------------------|
| bin_3  | bin_2                     | [2, 3)        | {"start": "2", "end": "3"} |
+--------+---------------------------+---------------+----------------------------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-08 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-08 UTC."],[],[]]