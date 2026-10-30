* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The AI.FORECAST function

This document describes the `AI.FORECAST` function, which lets you forecast time
series by using the [TimesFM model](/bigquery/docs/timesfm-model) that's built
into BigQuery ML. You can use this function to perform univariate or
multivariate forecasting:

* **Univariate forecasting**: predicts future values of a single time series
  based only on its own past values.
* **Multivariate forecasting**: predicts future values based on the time series'
  past values and additional variables (covariates) that might influence the
  forecast.

For example, imagine you have a table containing sales data for a
product. You could run a query similar to the following to forecast
sales for the next 30 data points:

```
SELECT *
FROM AI.FORECAST(
  TABLE `mydataset.input_table`,
  data_col => 'units_sold',
  timestamp_col => 'sales_date',
  horizon => 30);
```

## Syntax

The syntax for `AI.FORECAST` depends on if you're performing univariate or
multivariate forecasting.

### Univariate

```
SELECT
  *
FROM
  AI.FORECAST(
    { TABLE TABLE | (QUERY_STATEMENT) },
    data_col => 'DATA_COL',
    timestamp_col => 'TIMESTAMP_COL'
    [, model => 'MODEL']
    [, id_cols => ID_COLS]
    [, horizon => HORIZON]
    [, forecast_end_timestamp => FORECAST_END_TIMESTAMP]
    [, confidence_level => CONFIDENCE_LEVEL]
    [, output_historical_time_series => OUTPUT_HISTORICAL_TIME_SERIES]
    [, context_window => CONTEXT_WINDOW]
  )
```

#### Arguments

`AI.FORECAST` takes the following arguments for univariate forecasting:

* `TABLE`: the name of the table that contains the
  data that you want to forecast. For example, `` `mydataset.mytable` ``.

  If the table is in a different project, then you must prepend the
  project ID to the table name in the following format, including backticks:

  `` `PROJECT_ID.DATASET.TABLE` ``

  For example, `` `myproject.mydataset.mytable` ``.

  To prevent query errors, we recommend providing the fully qualified table
  name, including backticks. This is especially important if the project name
  contains characters other than letters, numbers, and underscores.
* `QUERY_STATEMENT`: the GoogleSQL query that
  generates the data that you want to forecast. See the
  [GoogleSQL query syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax)
  page for the supported SQL syntax of the `QUERY_STATEMENT` clause.
* `DATA_COL`: a `STRING` value that specifies the name of
  the data column. The data column contains the data to forecast. The data
  column must use one of the following data types:

  + `INT64`
  + `NUMERIC`
  + `BIGNUMERIC`
  + `FLOAT64`
* `TIMESTAMP_COL`: a `STRING` value that specifies the
  name of the timestamp column. The timestamp
  column must use one of the following data types:

  + `TIMESTAMP`
  + `DATE`
  + `DATETIME`
* `MODEL`: a `STRING` value that specifies the name of the
  model to use. Supported models include `TimesFM 2.5` and
  `TimesFM 3.0` ([Preview](https://cloud.google.com/products#product-launch-stages)).
  The default value is `TimesFM 2.5`.
* `ID_COLS`: an `ARRAY<STRING>` value that specifies the
  names of one or more ID columns. Each unique combination of IDs identifies a
  unique time series to forecast. Specify one or more values for this argument
  in order to forecast multiple time series using a single query. The columns
  that you specify must use one of the following data types:

  + `STRING`
  + `INT64`
  + `ARRAY<STRING>`
  + `ARRAY<INT64>`
* `HORIZON`: an `INT64` value that specifies the number of
  time series data points to forecast. The default value is `10`. The valid
  input range for the `TimesFM 2.5` model is `[1, 10,000]`.
  The valid input range for the `TimesFM 3.0` model is `[1, 1024]`. This argument
  can't be used with the
  `forecast_end_timestamp` argument.
* `FORECAST_END_TIMESTAMP`: a timestamp literal value that
  specifies the end timestamp for the forecasted values. The horizon is
  calculated based on the end timestamp and the frequency provided from the
  input table for each time series. If the calculated horizon is out of the
  valid range `[1, 10,000]`, the query returns an error. You can then adjust the
  `forecast_end_timestamp` value so that the calculated horizon is within the
  valid range. This argument can't be used with the `horizon` argument.
* `CONFIDENCE_LEVEL`: a `FLOAT64` value that specifies the
  percentage of the future values that fall in the prediction interval. The
  default value is `0.95`. The valid input range is `[0, 1)`.
* `OUTPUT_HISTORICAL_TIME_SERIES`: a `BOOL` value that
  determines whether the input data is returned along with the forecasted
  data. Set this argument to `TRUE` to return input data. The default value
  is `FALSE`.

  Returning the input data along with the forecasted data lets you compare the
  historical value of the data column with the forecasted value of the data
  column, or chart the change in the data column values over time.
* `CONTEXT_WINDOW`: an `INT64` value that specifies the
  context window length used by BigQuery ML's built-in TimesFM model.
  The context window length determines how many of the most recent data points
  from the input time series are used by the model. For example, if your time
  series date range is March 1 to April 15, data points are selected starting
  at April 15 and working backwards. Valid values for models are as follows:

  | **Model name** | **Supported context window length** |
  | --- | --- |
  | `TimesFM 2.5` | 64, 128, 256, 512, 1024, 2048, 4096, 8192, 15360 |
  | `TimesFM 3.0` | `n * 32` where `n` is an integer in the range `[2, 64]` |

  If you don't specify a `CONTEXT_WINDOW` value when you use the
  `TimesFM 2.5` model, the `AI.FORECAST` function
  automatically chooses the smallest possible context window length to use that
  is still large enough to cover the number of time series data points in your
  input data. If you don't specify a `CONTEXT_WINDOW` value when you use the
  `TimesFM 3.0` model, the `AI.FORECAST` function defaults to the maximum
  supported size, `2048`. The following table shows the relationships between
  the number of time series data points in the input data, the selected context
  window length and the corresponding supported TimesFM model name:

  | **Number of time series data points** | **Context window length** | **Supported model names** |
  | --- | --- | --- |
  | `(1, 64]` | 64 | `TimesFM 2.5`, `TimesFM 3.0` |
  | `(65, 128]` | 128 | `TimesFM 2.5`, `TimesFM 3.0` |
  | `(129, 256]` | 256 | `TimesFM 2.5`, `TimesFM 3.0` |
  | `(257, 512]` | 512 | `TimesFM 2.5`, `TimesFM 3.0` |
  | `(513, 1024]` | 1,024 | `TimesFM 2.5`, `TimesFM 3.0` |
  | `(1025, 2048]` | 2,048 | `TimesFM 2.5`, `TimesFM 3.0` |
  | `(2049, 4096]` | 4,096 | `TimesFM 2.5` |
  | `(4097, 8192]` | 8,192 | `TimesFM 2.5` |
  | `(8193, 15360]` | 15,360 | `TimesFM 2.5` |
  | `15360` | 15,360 | `TimesFM 2.5` |

  For the `TimesFM 3.0` model, 2,048 is the maximum
  number of time series data
  points that are passed to the model. For the `TimesFM 2.5`
  model, 15,360 is the maximum number of time series data points that are
  passed to the model. Any additional time series data points in the input data
  are ignored.

### Multivariate

**Preview**

This product or feature is
subject to the "Pre-GA Offerings Terms" in the General Service Terms section
of the [Service Specific
Terms](/terms/service-terms#1).
Pre-GA products and features are available "as is" and might have limited support.
For more information, see the
[launch stage descriptions](https://cloud.google.com/products/#product-launch-stages).

```
SELECT *
FROM AI.FORECAST(
  { TABLE TABLE | (QUERY_STATEMENT) },
  target_cols => [TARGET_COLS],
  timestamp_col => 'TIMESTAMP_COL',
  model => 'MODEL'
  [, id_cols => [ID_COLS]]
  [, horizon => HORIZON]
  [, confidence_level => CONFIDENCE_LEVEL]
  [, context_window => CONTEXT_WINDOW]
  [, past_covariate_cols => [PAST_COVARIATE_COLS]]
  [, future_covariate_cols => [FUTURE_COVARIATE_COLS]]
  [, output_historical_time_series => OUTPUT_HISTORICAL_TIME_SERIES]
);
```

#### Arguments

`AI.FORECAST` takes the following arguments for multivariate forecasting:

* `TABLE`: the name of the table that contains the
  data that you want to forecast. For example, `` `mydataset.mytable` ``.

  If the table is in a different project, then you must prepend the
  project ID to the table name in the following format, including backticks:

  `` `PROJECT_ID.DATASET.TABLE` ``

  For example, `` `myproject.mydataset.mytable` ``.

  To prevent query errors, we recommend providing the fully qualified table
  name, including backticks. This is especially important if the project name
  contains characters other than letters, numbers, and underscores.
* `QUERY_STATEMENT`: the GoogleSQL query that
  generates the data that you want to forecast. See the
  [GoogleSQL query syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax)
  page for the supported SQL syntax of the `QUERY_STATEMENT` clause.
* `TARGET_COLS`: an `ARRAY<STRING>` value that specifies the names of
  the data columns. The data columns contain the data to forecast. The data
  columns must use one of the following data types:

  + `INT64`
  + `NUMERIC`
  + `BIGNUMERIC`
  + `FLOAT64`
* `TIMESTAMP_COL`: a `STRING` value that specifies the
  name of the timestamp column. The timestamp
  column must use one of the following data types:

  + `TIMESTAMP`
  + `DATE`
  + `DATETIME`
* `MODEL`: a `STRING` value that specifies the name of the
  model to use. You must use the `TimesFM 3.0` model
  ([Preview](https://cloud.google.com/products#product-launch-stages))
  for multivariate forecasting.
* PAST\_COVARIATE\_COLS: an `ARRAY<STRING>` value that specifies the
  names of columns that could influence the target columns and that are only
  known historically. For
  example, if you're forecasting daily sales at a store's location,
  then a past covariate column could be the number of customers who visited
  the store each day. Customer counts are known historically and can
  influence sales, but they aren't known for the future. The columns
  that you specify must use one of the following data types:

  + `INT64`
  + `FLOAT64`
  + `NUMERIC`
  + `BIGNUMERIC`
* FUTURE\_COVARIATE\_COLS: an `ARRAY<STRING>` value that specifies
  the names of columns that could influence the target
  columns and are known for both the past and
  the future. For example, if you're forecasting daily sales at a store's
  location, then a future covariate column could be whether or not the day
  is a weekend. This data is known in advance for both the past and the
  future. The columns that you specify must use one of the following data
  types:

  + `INT64`
  + `FLOAT64`
  + `NUMERIC`
  + `BIGNUMERIC`**Note:** When you use `FUTURE_COVARIATE_COLS`, *all* input columns must have
  data spanning the entire `CONTEXT_WINDOW` + `HORIZON` length.
* `HORIZON`: an `INT64` value that specifies the number of
  time series data points to forecast. The default value is `10`. The valid
  input range for the `TimesFM 3.0` model is `[1, 1024]`. This argument can't be used with the
  `forecast_end_timestamp` argument.
* `ID_COLS`: an `ARRAY<STRING>` value that specifies the
  names of one or more ID columns. Each unique combination of IDs identifies a
  unique time series to forecast. Specify one or more values for this argument
  in order to forecast multiple time series using a single query. The columns
  that you specify must use one of the following data types:

  + `STRING`
  + `INT64`
  + `ARRAY<STRING>`
  + `ARRAY<INT64>`
* `CONFIDENCE_LEVEL`: a `FLOAT64` value that specifies the
  percentage of the future values that fall in the prediction interval. The
  default value is `0.95`. The valid input range is `[0, 1)`.
* `CONTEXT_WINDOW`: an `INT64` value that specifies the
  context window length used by the TimesFM model.
  The context window length determines how many of the most recent data points
  from the input time series are used by the model. For example, if your time
  series date range is March 1 to April 15, data points are selected starting
  at April 15 and working backwards. Valid values for the `TimesFM 3.0` model are
  as follows:

  | **Model name** | **Supported context window length** |
  | --- | --- |
  | `TimesFM 3.0` | `n * 32` where `n` is an integer in the range `[2, 64]` |

  If you don't specify a `CONTEXT_WINDOW` value when you use the `TimesFM 3.0`
  model, the `AI.FORECAST` function defaults to the maximum supported size,
  `2048`.

  For the `TimesFM 3.0` model, 2,048 is the maximum number of time series
  data points that are passed to the model. Any additional time series data
  points in the input data are ignored.
* `OUTPUT_HISTORICAL_TIME_SERIES`: a `BOOL` value that
  determines whether the input data is returned along with the forecasted
  data. Set this argument to `TRUE` to return input data. The default value
  is `FALSE`.

  Returning the input data along with the forecasted data lets you compare the
  historical value of the data column with the forecasted value of the data
  column, or chart the change in the data column values over time.

## Output

The output schema of `AI.FORECAST` depends on if you're performing univariate or
multivariate forecasting.

### Univariate

The output schema of `AI.FORECAST` depends on the value of the
`output_historical_time_series` argument. The following columns are always part
of the output:

* `id_cols`: one or more values that contain the identifiers of a time
  series. `id_cols` can be an `INT64`, `STRING`, `ARRAY<INT64>`, or
  `ARRAY<STRING>` value. The column names and types are inherited from the
  `ID_COLS` argument value specified in the function input.
* `confidence_level`: a `FLOAT64` value that contains the
  `confidence_level` value that you specified in the function input, or
  `0.95` if you didn't specify a `confidence_level` value. This value is the
  same across all rows.
* `prediction_interval_lower_bound`: a `FLOAT64` value that contains the
  lower bound of the prediction interval for each forecasted point. For
  historical points, the value is `NULL`.
* `prediction_interval_upper_bound`: a `FLOAT64` value that contains the
  upper bound of the prediction interval for each forecasted point. For
  historical points, the value is `NULL`.
* `ai_forecast_status`: a `STRING` value that contains the forecast status.
  This value is empty if the operation was successful. If the operation wasn't
  successful, the value is the error string. A common error is
  `The time series data is too short.` This error indicates that there wasn't
  enough historical data in the time series to generate a forecast.
  A minimum of 3 data points is required.

If you set `output_historical_time_series` to `FALSE`, then the output rows
only include forecasted data and the output columns are the following:

* `forecast_timestamp`: a `TIMESTAMP` value that contains the timestamps
  of the time series.
* `forecast_value`: a `FLOAT64` value that contains the 50% quantile value for
  the forecasting output from the model. The 50% quantile value represents
  the median value of the forecasted data.

If you set `output_historical_time_series` to `TRUE`, then the output rows
include all data, and the output columns are the following:

* `time_series_type`: a `STRING` value that contains a value of either
  `history` or `forecast`. Rows that have a value of `history` contain data
  from the input table or query. Rows that have a value of `forecast` contain
  forecasted data.
* `time_series_timestamp`: a `TIMESTAMP` value that contains the
  timestamps of the time series.
* `time_series_data`: a `FLOAT64` value that represents the historical input
  if the `time_series_type` is `history`. Otherwise, if the `time_series_type` is
  `forecast` this number represents the 50% quantile of the forecast.

### Multivariate

**Preview**

This product or feature is
subject to the "Pre-GA Offerings Terms" in the General Service Terms section
of the [Service Specific
Terms](/terms/service-terms#1).
Pre-GA products and features are available "as is" and might have limited support.
For more information, see the
[launch stage descriptions](https://cloud.google.com/products/#product-launch-stages).

If you perform a multivariate forecast, the output schema is restructured to
support multiple targets:

* `id_cols`: one or more values that contain the identifiers of a time
  series. `id_cols` can be an `INT64`, `STRING`, `ARRAY<INT64>`, or
  `ARRAY<STRING>` value. The column names and types are inherited from the
  `ID_COLS` argument value specified in the function input.
* `timestamp_col`: a `TIMESTAMP` value that contains the timestamp of the data
  point. Unlike univariate, this column preserves the name of the timestamp
  column from your input table—for example, `date`.
* `target_cols`: for each target column specified in
  `TARGET_COLS` input argument, the output contains a `STRUCT` type with the
  following fields:

  + `value`: a `FLOAT64` value that contains the 50% quantile value for
    the forecasting output from the model. The 50% quantile value represents
    the median value of the forecasted data.
  + `prediction_interval_lower_bound`: a `FLOAT64` value that contains the
    lower bound of the prediction interval for each forecasted point. For
    historical points, the value is `NULL`.
  + `prediction_interval_upper_bound`: a `FLOAT64` value that contains the
    upper bound of the prediction interval for each forecasted point. For
    historical points, the value is `NULL`.
* `time_series_type`: a
  `STRING` value that contains a value of either `history` or `forecast`. Rows
  that have a value of `history` contain data from the input table or query.
  Rows that have a value of `forecast` contain forecasted data.
* `confidence_level`: a `FLOAT64` value that contains the
  `confidence_level` value that you specified in the function input, or
  `0.95` if you didn't specify a `confidence_level` value. This value is the
  same across all rows.
* `ai_forecast_status`: a `STRING` value that contains the forecast status.
  This value is empty if the operation was successful. If the operation failed,
  the value is the error string. A common error is
  `The time series data is too short.` This error indicates that there wasn't
  enough historical data in the time series to generate a forecast.
  A minimum of 3 data points is required.

## Examples

The following examples show how to perform univariate and multivariate
forecasting.

### Univariate forecasting

The following example performs univariate forecasting to predict the daily
number of bike trips for each different user type for the next 30 days:

```
WITH
  citibike_trips AS (
    SELECT EXTRACT(DATE FROM starttime) AS date, usertype, COUNT(*) AS num_trips
    FROM `bigquery-public-data.new_york.citibike_trips`
    GROUP BY date, usertype
  )
SELECT *
FROM
  AI.FORECAST(
    TABLE
```