* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.TFDV\_DESCRIBE function

This document describes the `ML.TFDV_DESCRIBE` function, which you can use
to generate fine-grained statistics for the columns in a table. For example, you
might want to know statistics for a table of training or serving data
statistics that you plan to use with a machine learning (ML) model. Calling
this function provides the same behavior as calling the TensorFlow
[TensorFlow `tfdv.generate_statistics_from_csv` API](https://www.tensorflow.org/tfx/data_validation/api_docs/python/tfdv/generate_statistics_from_csv).
You can use the data output by this function for such purposes as
[feature preprocessing](/bigquery/docs/manual-preprocessing) or
[model monitoring](/bigquery/docs/model-monitoring-overview).

## Syntax

```
ML.TFDV_DESCRIBE(
  { TABLE `PROJECT_ID.DATASET.TABLE_NAME` | (QUERY_STATEMENT) },
  STRUCT(
    [NUM_HISTOGRAM_BUCKETS AS num_histogram_buckets]
    [, NUM_QUANTILES_HISTOGRAM_BUCKETS AS num_quantiles_histogram_buckets]
    [, NUM_VALUES_HISTOGRAM_BUCKETS AS num_values_histogram_buckets]
    [, NUM_RANK_HISTOGRAM_BUCKETS AS num_rank_histogram_buckets])
)
```

### Arguments

`ML.TFDV_DESCRIBE` takes the following arguments:

* `PROJECT_ID`: your project ID.
* `DATASET`: the BigQuery dataset that contains
  the table.
* `TABLE_NAME`: the name of the input table that contains
  the training or serving data to calculate statistics for.
* `QUERY_STATEMENT`: a query that generates the training
  or serving data to calculate statistics for. For the supported SQL syntax of
  the `QUERY_STATEMENT` clause, see [GoogleSQL query
  syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).
* `NUM_HISTOGRAM_BUCKETS`: an `INT64` value that specifies
  the number of buckets to use for a histogram with equal-width buckets. Only
  applies to numerical, `ARRAY<numerical>`, and `ARRAY<STRUCT<INT64,
  numerical>>` columns. The `num_histogram_buckets` value must be in the range
  `[1, 1,000]`. The default value is `10`.
* `NUM_QUANTILES_HISTOGRAM_BUCKETS`: an `INT64` value that
  specifies the number of buckets to use for a
  [quantiles](https://en.wikipedia.org/wiki/Quantile) histogram. Only applies to
  numerical, `ARRAY<numerical>`, and `ARRAY<STRUCT<INT64, numerical>>` columns.
  The `num_quantiles_histogram_buckets` value must be in the range `[1, 1,000]`.
  The default value is `10`.
* `NUM_VALUES_HISTOGRAM_BUCKETS`: an `INT64` value that
  specifies the number of buckets to use for a quantiles histogram. Only applies
  to `ARRAY` columns. The `num_values_histogram_buckets` value must be in the
  range `[1, 1,000]`. The default value is `10`.
* `NUM_RANK_HISTOGRAM_BUCKETS`: an `INT64` value that
  specifies the number of buckets to use for a
  [rank](https://en.wikipedia.org/wiki/Ranking_(statistics)) histogram. Only
  applies to categorical and `ARRAY<categorical>` columns. The
  `num_rank_histogram_buckets` value must be in the range `[1, 10,000]`. The
  default value is `50`.

## Output

`ML.TFDV_DESCRIBE` returns a column named `dataset_feature_statistics_list`
that contains a TensorFlow
[`DatasetFeatureStatisticsList` protocol buffer](https://www.tensorflow.org/tfx/tf_metadata/api_docs/python/tfmd/proto/statistics_pb2/DatasetFeatureStatisticsList)
in JSON format.

## Example

The following example returns statistics for the `penguins` public dataset and
uses 20 buckets for rank histograms for string values:

```
SELECT * FROM ML.TFDV_DESCRIBE(
  TABLE `bigquery-public-data.ml_datasets.penguins`,
  STRUCT(20 AS num_rank_histogram_buckets)
);
```

## Limitations

Input data for the `ML.TFDV_DESCRIBE` function can only contain columns of the
following data types:

* [Numeric](/bigquery/docs/reference/standard-sql/data-types#numeric_types)
  types
* `STRING`
* `BOOL`
* `BYTE`
* `DATE`
* `DATETIME`
* `TIME`
* `TIMESTAMP`
* `ARRAY<STRUCT<INT64, FLOAT64>>` (a sparse tensor)
* `STRUCT` columns that contain any of the following types:
  + Numeric types
  + `STRING`
  + `BOOL`
  + `BYTE`
  + `DATE`
  + `DATETIME`
  + `TIME`
  + `TIMESTAMP`
* `ARRAY` columns that contain any of the following types:
  + Numeric types
  + `STRING`
  + `BOOL`
  + `BYTE`
  + `DATE`
  + `DATETIME`
  + `TIME`
  + `TIMESTAMP`

## Pricing

The `ML.TFDV_DESCRIBE` function uses
[BigQuery on-demand compute pricing](https://cloud.google.com/bigquery/pricing#on-demand-compute-pricing).

## What's next

* For more information about model monitoring in BigQuery ML, see
  [Model monitoring overview](/bigquery/docs/model-monitoring-overview).
* For more information about supported SQL statements and functions for ML
  models, see
  [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-13 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-13 UTC."],[],[]]