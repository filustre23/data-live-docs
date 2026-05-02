* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.ARIMA\_EVALUATE function

This document describes the `ML.ARIMA_EVALUATE` function, which you can use
to evaluate the model metrics of `ARIMA_PLUS` or `ARIMA_PLUS_XREG` time series
models.

## Syntax

```
ML.ARIMA_EVALUATE(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  [, STRUCT(SHOW_ALL_CANDIDATE_MODELS AS show_all_candidate_models)])
```

**Note:** No input data is required.

### Arguments

`ML.ARIMA_EVALUATE` takes the following arguments:

* `PROJECT_ID`: Your project ID.
* `DATASET`: The BigQuery dataset that contains
  the model.
* `MODEL_NAME`: The name of the model.
* `SHOW_ALL_CANDIDATE_MODELS`: a `BOOL` value that
  indicates whether to show evaluation metrics or an error message for either
  all candidate models or for only the best model with the lowest
  [Akaike information criterion (AIC)](https://en.wikipedia.org/wiki/Akaike_information_criterion).

  When the `SHOW_ALL_CANDIDATE_MODELS` argument value is `FALSE`, the
  `ML.ARIMA_EVALUATE` function returns evaluation metrics for only the best
  model. When the `SHOW_ALL_CANDIDATE_MODELS` argument value is `TRUE`,
  metrics are returned for all candidate models, along with a possible fitting
  error on a setting of `non_seasonal_p`, `non_seasonal_d`, `non_seasonal_q`,
  and `drift`; this applies to both single time series training with
  `auto.ARIMA` and large-scale time series training cases.

  For large-scale time series forecasting training, regardless of the value of
  the `SHOW_ALL_CANDIDATE_MODELS` argument, a single row is returned for a
  time series for which there is no a valid model. The error message explains
  the reason, and the values of all other columns are `NULL`.

  For single time series `ARIMA_PLUS` or `ARIMA_PLUS_XREG` models, the default
  value is `TRUE`. For large-scale time series `ARIMA_PLUS` models, the
  default value is `FALSE`.

## Output

`ML.ARIMA_EVALUATE` returns the following columns:

* `time_series_id_col` or `time_series_id_cols`: the identifiers of a time
  series. Only present when forecasting multiple time series at once. The column
  names and types are inherited from the `TIME_SERIES_ID_COL` option
  as specified in the model creation query.
* `non_seasonal_p`: an `INT64` value that contains the order of the
  autoregressive part in a non-seasonal ARIMA model.
* `non_seasonal_d`: an `INT64` value that contains the degree of first
  differencing involved in a non-seasonal ARIMA model.
* `non_seasonal_q`: an `INT64` value that contains the order of the moving
  average part in a non-seasonal ARIMA model.
* `has_drift`: a `BOOL` value that indicates whether the model has drift.
* `log_likelihood`: a `FLOAT64` value that contains the
  [log-likelihood](https://en.wikipedia.org/wiki/Likelihood_function#Log-likelihood)
  of the model.
* `AIC`: the AIC of the model.
* `variance`: a `FLOAT64` value that contains the variance of the model.
* `seasonal_periods`: an `ARRAY<STRING>` value that contains one or more of
  the following values:

  + `DAILY`
  + `WEEKLY`
  + `MONTHLY`
  + `QUARTERLY`
  + `YEARLY`
  + `NO_SEASONALITY`
* `has_holiday_effect`: a `BOOL` value that indicates whether the history data
  has a holiday effect.
* `has_spikes_and_dips`: a `BOOL` value that indicates whether the history data
  has spikes and dips.
* `has_step_changes`: a `BOOL` value that indicates whether the model has
  step changes.
* `error_message`: a `STRING` value that contains the error message raised if
  any time series fail in the model.

The `has_holiday_effect`, `has_spikes_and_dips`, and `has_step_changes` columns
are only populated for `ARIMA_PLUS` models that have `decompose_time_series`
enabled.

All of the columns are specific to the fitted `ARIMA` models except for the
following columns:

* `time_series_id_col`
* `time_series_id_cols`
* `seasonal_periods`
* `has_holiday_effect`
* `has_spikes_and_dips`
* `has_step_changes`

When the `non_seasonal_d` value is not `1`, `has_drift` is set to `FALSE` by
default, because `has_drift` doesn't apply in those cases.

## Example

The following example retrieves the evaluation metrics of the best model from
the model `mydataset.mymodel` in your default project:

```
SELECT
  *
FROM
  ML.ARIMA_EVALUATE(MODEL `mydataset.mymodel`, STRUCT(FALSE AS show_all_candidate_models))
```

## What's next

* For information about model evaluation, see
  [BigQuery ML model evaluation overview](/bigquery/docs/evaluate-overview).
* For more information about supported SQL statements and functions for time
  series forecasting models, see
  [End-to-end user journeys for time series forecasting models](/bigquery/docs/e2e-journey-forecast).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-01 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-01 UTC."],[],[]]