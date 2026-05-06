* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.ARIMA\_COEFFICIENTS function

This document describes the `ML.ARIMA_COEFFICIENTS` function, which lets you
see the ARIMA coefficients and the weights of the external regressors for
`ARIMA_PLUS` and `ARIMA_PLUS_XREG` time series models.

## Syntax

```
ML.ARIMA_COEFFICIENTS(
  MODEL `PROJECT_ID.DATASET.MODEL`
)
```

### Arguments

`ML.ARIMA_COEFFICIENTS` takes the following arguments:

* `PROJECT_ID`: your project ID.
* `DATASET`: the BigQuery dataset that contains
  the model.
* `MODEL`: the name of the model.

## Output

`ML.ARIMA_COEFFICIENTS` returns the following columns:

* `time_series_id_col` or `time_series_id_cols`: a value that contains the
  identifiers of a time series. `time_series_id_col` can be an `INT64` or
  `STRING` value. `time_series_id_cols` can be an `ARRAY<INT64>` or
  `ARRAY<STRING>` value. Only present when forecasting multiple time series
  simultaneously. The column names and types are inherited from the
  `TIME_SERIES_ID_COL` option as specified in the model creation query.
* `ar_coefficients`: an `ARRAY<FLOAT64>` value that contains the autoregressive
  coefficients, which corresponds to non-seasonal p.
* `ma_coefficients`: an `ARRAY<FLOAT64>` value that contains the moving-average
  coefficients, which corresponds to non-seasonal q.
* `intercept_or_drift`: a `FLOAT64` value that contains the constant term of
  the ARIMA model. By definition, the constant term is called `intercept` when
  non-seasonal d is `0`, and `drift` when non-seasonal d is `1`.
  `intercept_or_drift` is always `0` when non-seasonal d is `2`.
* `processed_input`: a `STRING` value that contains the name of the model
  feature input column. The value of this column matches the name of the
  feature column provided in the
  [`query_statement` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#query_statement)
  that was used when the model was trained.
* `weight`: when the `processed_input` value is numerical, `weight` contains a
  `FLOAT64` value and the `category_weights` column contains `NULL` values.
  When the `processed_input` value is non-numerical and has been converted to
  dummy encoding, the `weight` column is `NULL` and the `category_weights`
  column contains the category names and weights for each category.
* `category_weights.category`: a `STRING` value that contains the category
  name if the `processed_input` value is non-numeric.
* `category_weights.weight`: a `FLOAT64` that contains the category's weight
  if the `processed_input` value is non-numeric.

**Note:** For trained `ARIMA_PLUS` models, this function returns the ARIMA
coefficients for all time series, in ascending order of the
`time_series_id_col` or `time_series_id_cols` value.

## Example

The following example retrieves the model coefficients information from
the model `mydataset.mymodel` in your default project:

```
SELECT
  *
FROM
  ML.ARIMA_COEFFICIENTS(MODEL `mydataset.mymodel`)
```

## What's next

* For information about model weights support in BigQuery ML, see
  [BigQuery ML model weights overview](/bigquery/docs/weights-overview).
* For more information about supported SQL statements and functions for time
  series forecasting models, see
  [End-to-end user journeys for time series forecasting models](/bigquery/docs/e2e-journey-forecast).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-05 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-05 UTC."],[],[]]