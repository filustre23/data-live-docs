* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.TFDV\_VALIDATE function

This document describes the `ML.TFDV_VALIDATE` function, which you can use to
compare the statistics for training and serving data, or two sets of
serving data, in order to identify anomalous differences between the two data
sets. Calling this function provides the same behavior as calling the
TensorFlow
[`validate_statistics` API](https://www.tensorflow.org/tfx/data_validation/api_docs/python/tfdv/validate_statistics).
You can use the data output by this function for
[model monitoring](/bigquery/docs/model-monitoring-overview).

## Syntax

```
ML.TFDV_VALIDATE(
  base_statistics,
  study_statistics
  [, detection_type]
  [, categorical_default_threshold]
  [, categorical_metric_type]
  [, numerical_default_threshold]
  [, numerical_metric_type]
  [, thresholds]
)
```

### Arguments

`ML.TFDV_VALIDATE` takes the following arguments:

* `base_statistics`: the statistics of the training or serving data
  that you want to use as the baseline for comparison. This must be
  a TensorFlow
  [`DatasetFeatureStatisticsList` protocol buffer](https://www.tensorflow.org/tfx/tf_metadata/api_docs/python/tfmd/proto/statistics_pb2/DatasetFeatureStatisticsList)
  in JSON format. You can generate a protocol buffer in the correct
  format by running the
  [`ML.TFDV_DESCRIBE` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-tfdv-describe),
  or you can load it from outside of BigQuery.
* `study_statistics`: the statistics of the training or serving data
  that you want to compare to the baseline. This must be
  a TensorFlow `DatasetFeatureStatisticsList` protocol buffer
  in JSON format. You can generate a protocol buffer in the correct format by
  running the `ML.TFDV_DESCRIBE` function, or you can load it from outside of
  BigQuery.
* `detection_type`: a `STRING` value that specifies the type of comparison that
  you want to make. Valid values are as follows:
  + `SKEW`: returns the data skew, which represents the statistical variation
    between training and serving data.
  + `DRIFT`: returns the data drift, which represents the statistical
    variation between two different sets of serving data.
* `categorical_default_threshold`: a `FLOAT64` value that specifies the custom
  threshold to use for anomaly detection for categorical and
  `ARRAY<categorical>` features. The value
  must be in the range `[0, 1)`. The default value is `0.3`.
* `categorical_metric_type`: a `STRING` value that specifies the metric used
  to compare statistics for categorical and `ARRAY<categorical>`features.
  Valid values are as follows:
  + `L_INFTY`: use
    [L-infinity distance](https://en.wikipedia.org/wiki/Chebyshev_distance).
    This value is the default.
  + `JENSEN_SHANNON_DIVERGENCE`: use
    [Jensen–Shannon divergence](https://en.wikipedia.org/wiki/Jensen%E2%80%93Shannon_divergence).
* `numerical_default_threshold`: a `FLOAT64` value that specifies the custom
  threshold to use for anomaly detection for numerical,
  `ARRAY<numerical>`, and `ARRAY<STRUCT<INT64, numerical>>` features. The value
  must be in the range `[0, 1)`. The default value is `0.3`.
* `numerical_metric_type`: a `STRING` value that specifies the metric used
  to compare statistics for numerical, `ARRAY<numerical>`, and
  `ARRAY<STRUCT<INT64, numerical>>` features. The only valid value is
  `JENSEN_SHANNON_DIVERGENCE`.
* `thresholds`: an `ARRAY<STRUCT<STRING, FLOAT64>>` value
  that specifies the anomaly detection thresholds for one or more columns
  for which you don't want to use the default threshold. The `STRING` value in
  the struct specifies the column name, and the `FLOAT64` value specifies the
  threshold. The `FLOAT64` value must be in the range `[0, 1)`. For example,
  `[('col_a', 0.1), ('col_b', 0.8)]`.

`ML.TFDV_VALIDATE` uses positional arguments, so if you specify an
optional argument, you must also specify all arguments prior to that argument.
For more information on argument types, see
[Named arguments](/bigquery/docs/reference/standard-sql/functions-reference#named_arguments).

## Output

`ML.TFDV_VALIDATE` returns a TensorFlow
[`Anomalies` protocol buffer](https://www.tensorflow.org/tfx/tf_metadata/api_docs/python/tfmd/proto/anomalies_pb2/Anomalies)
in JSON format.

## Examples

The following example returns the skew between training and serving data
and also sets custom anomaly detection thresholds for two of the feature
columns:

```
DECLARE stats1 JSON;
DECLARE stats2 JSON;

SET stats1 = (SELECT * FROM ML.TFDV_DESCRIBE(TABLE `myproject.mydataset.training`));

SET stats2 = (SELECT * FROM ML.TFDV_DESCRIBE(TABLE `myproject.mydataset.serving`));

SELECT ML.TFDV_VALIDATE(
  stats1, stats2, 'SKEW', .3, 'L_INFTY', .3, 'JENSEN_SHANNON_DIVERGENCE', [('feature1', 0.2), ('feature2', 0.5)]
);

INSERT `myproject.mydataset.serve_stats`
  (t, dataset_feature_statistics_list)
SELECT CURRENT_TIMESTAMP() AS t, stats1;
```

The following example returns the drift between two sets of serving data:

```
SELECT ML.TFDV_VALIDATE(
  (SELECT dataset_feature_statistics_list FROM `myproject.mydataset.servingJan24`),
  (SELECT * FROM ML.TFDV_DESCRIBE(TABLE `myproject.mydataset.serving`)),
  'DRIFT'
);
```

## Limitations

The `ML.TFDV_VALIDATE` function doesn't conduct schema validation.

`ML.TFDV_VALIDATE` handles type mismatch as follows:

* If you specify `JENSEN_SHANNON_DIVERGENCE` for the
  `categorical_default_threshold` or `numerical_default_threshold`
  argument, the feature isn't included in the final anomaly report.
* If you specify `L_INFTY` for the `categorical_default_threshold`
  argument, the function outputs the computed feature distance as expected.

## Pricing

The `ML.TFDV_VALIDATE` function uses
[BigQuery on-demand compute pricing](https://cloud.google.com/bigquery/pricing#on-demand-compute-pricing).

## What's next

* For more information about model monitoring in BigQuery ML, see
  [Model monitoring overview](/bigquery/docs/model-monitoring-overview).
* For more information about supported SQL statements and functions for ML
  models, see
  [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-01 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-01 UTC."],[],[]]