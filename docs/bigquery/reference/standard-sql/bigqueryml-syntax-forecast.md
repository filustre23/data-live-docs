* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.FORECAST function

This document describes the `ML.FORECAST` function, which you can use to
forecast a time series based on a trained `ARIMA_PLUS` or `ARIMA_PLUS_XREG`
model.

If you don't want to manage your own times series forecasting model, you can
use the
[`AI.FORECAST` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast)
with BigQuery ML's built-in
[TimesFM time series model](/bigquery/docs/timesfm-model)
to perform forecasting.

## Syntax

```
# ARIMA_PLUS models:
ML.FORECAST(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
    STRUCT(
      [, HORIZON AS horizon]
      [, CONFIDENCE_LEVEL AS confidence_level])
)

# ARIMA_PLUS_XREG model:
ML.FORECAST(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
    [{ TABLE `PROJECT_ID.DATASET.TABLE` | (QUERY_STATEMENT) } ,]
    STRUCT(
      HORIZON AS horizon,
      CONFIDENCE_LEVEL AS confidence_level)
)
```

### Arguments

`ML.FORECAST` takes the following arguments:

* `PROJECT_ID`: the project that contains the
  resource.
* `DATASET`: the dataset that contains the
  resource.
* `MODEL`: The name of the model.
* `HORIZON`: an `INT64` value that specifies the number of
  time points to forecast. The default value is `3`, and the maximum value is
  the value
  of the `HORIZON` option specified in the
  [`CREATE MODEL`](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series)
  statement for time-series models, or `1000` if that option isn't specified.
  When forecasting multiple time series at the same time, this parameter
  applies to each time series.

  **Note:** Forecasting takes place when the
  [`CREATE MODEL` statement](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series)
  runs. `ML.FORECAST` just retrieves the forecasting values and computes the
  prediction intervals. Therefore, this argument exists mainly for filtering
  results when forecasting multiple time series. To save query time, you
  should specify a value for the `HORIZON` option in the `CREATE MODEL`
  statement.
* `CONFIDENCE_LEVEL`: a `FLOAT64` value that specifies
  percentage of the future values that fall in the prediction interval. The
  default value is `0.95`. The valid input range is `[0, 1)`.
* `TABLE`: The name of the input table that contains the
  features.

  If `TABLE` is specified, the input column names in the table must match the
  column names in the model, and their types should be compatible according to
  BigQuery [implicit coercion rules](/bigquery/docs/reference/standard-sql/conversion_rules#coercion).

  If there are unused columns from the table, they are ignored.
* `QUERY_STATEMENT`: The GoogleSQL query that is
  used to generate the features. See the
  [GoogleSQL query syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax)
  page for the supported SQL syntax of the `QUERY_STATEMENT` clause.

  If `QUERY_STATEMENT` is specified, the input column names from the query
  must match the column names in the model, and their types should be
  compatible according to BigQuery
  [implicit coercion rules](/bigquery/docs/reference/standard-sql/conversion_rules#coercion).

  If there are unused columns from the query, they are ignored.

## Output

`ML.FORECAST` returns the following columns:

* `time_series_id_col` or `time_series_id_cols`: a value that contains
  the identifiers of a time series. `time_series_id_col` can be an `INT64` or
  `STRING` value. `time_series_id_cols` can be an `ARRAY<INT64>` or
  `ARRAY<STRING>` value. Only present when forecasting multiple time series at
  once. The column names and types are inherited from the
  `TIME_SERIES_ID_COL` option as specified in the `CREATE MODEL` statement.
* `forecast_timestamp`: a `TIMESTAMP` value that contains the timestamps of a
  time series.
* `forecast_value`: a `FLOAT64` value that contains the average of the
  `prediction_interval_lower_bound` and `prediction_interval_upper_bound` values.
* `standard_error`: a `FLOAT64` value that contains the amount of variability
  in the estimated results.
* `confidence_level`: a `FLOAT64` value that contains the `confidence_level`
  value you specified in the function input, or `0.95` if you didn't
  specify a `confidence_level` value. It is the same across all rows.
* `prediction_interval_lower_bound`: a `FLOAT64` value that contains the lower
  bound of the prediction interval for each forecasted point.
* `prediction_interval_upper_bound`: a `FLOAT64` value that contains the upper
  bound of the prediction interval for each forecasted point.
* `confidence_interval_lower_bound`: a `FLOAT64` value that contains the
  lower bound of the confidence interval for each forecasted point.
* `confidence_interval_upper_bound`: a `FLOAT64` value that contains the upper
  bound of the confidence interval for each forecasted point.

The output of `ML.FORECAST` has the following properties:

* For each time series, the output rows are sorted in the chronological order of
  `forecast_timestamp`.
* `forecast_timestamp` always has a type of `TIMESTAMP`, regardless of the type
  of the column specified in the
  [`TIME_SERIES_TIMESTAMP_COL` option](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series#time_series_timestamp_col) of the `CREATE MODEL`
  statement.

## `ARIMA_PLUS` example

The following example forecasts 30 time points with a
confidence level of `0.8`:

```
SELECT
  *
FROM
  ML.FORECAST(MODEL `mydataset.mymodel`,
    STRUCT(30 AS horizon, 0.8 AS confidence_level))
```

## `ARIMA_PLUS_XREG` example

The following example forecasts 30 time points with a
confidence level of `0.8` with future features:

```
SELECT
  *
FROM
  ML.FORECAST(MODEL `mydataset.mymodel`,
    STRUCT(30 AS horizon, 0.8 AS confidence_level),
    (SELECT * FROM `mydataset.mytable`))
```

## Limitation

Applying any additional computation on top of `ML.FORECAST`'s result
columns might lead to an out of memory error if the model size is too large. If this happens, you might see errors like
`Resources exceeded during query execution: The query could not be executed in the allotted memory`.
Examples of operations that might cause this issue are calculating minimum or maximum values, or adding to or subtracting
from a particular column. If you are trying to filter on the forecasted value,
we recommend that you use the [forecast with limit](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series#forecast_limit_lower_bound) option instead, because the algorithm it uses is less likely to cause an issue. If you keep getting out of memory errors, you can try working around this issue by
creating a new table for the `ML.FORECAST` result, and then applying other computations in a different query that uses data from the new table.

## What's next

* For information about model inference, see
  [Model inference overview](/bigquery/docs/inference-overview).
* For more information about supported SQL statements and functions for time
  series forecasting models, see
  [End-to-end user journeys for time series forecasting models](/bigquery/docs/e2e-journey-forecast).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-01 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-01 UTC."],[],[]]