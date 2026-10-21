* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The CREATE MODEL statement for ARIMA\_PLUS\_XREG models

This document describes the `CREATE MODEL` statement for creating multivariate
time series models in BigQuery by using SQL. Alternatively, you can use the
Google Cloud console user interface to
[create a model by using a UI](/bigquery/docs/create-machine-learning-model-console)
([Preview](https://cloud.google.com/products#product-launch-stages)) instead of constructing the SQL
statement yourself. You can use a multivariate
time series model to [forecast](/bigquery/docs/forecasting-overview)
the future value for a given column based on the analysis of multiple
variables. You can also use multivariate time series models to detect anomalies
in time series data.

You can use multivariate time series models with the following functions:

* Use the
  [`ML.FORECAST` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast)
  to retrieve the forecasted values that were generated when you created the
  model.
* Use the
  [`ML.EXPLAIN_FORECAST` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast)
  function to retrieve the forecasted values that were generated when you
  created the model, and compute the prediction intervals.
* Use the
  [`ML.DETECT_ANOMALIES` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-detect-anomalies)
  to perform [anomaly detection](/bigquery/docs/anomaly-detection-overview).

**Note:** If you don't want to create and manage your own model, you can use
BigQuery ML's built-in
[TimesFM time series model](/bigquery/docs/timesfm-model)
with the
[`AI.FORECAST` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast)
([Preview](https://cloud.google.com/products#product-launch-stages)) to perform forecasting.

For more information about supported SQL statements and functions for this
model, see
[End-to-end user journey for time series forecasting models](/bigquery/docs/e2e-journey-forecast).

## Time series modeling pipeline

The multivariate `ARIMA_PLUS_XREG` time series model is an
[`ARIMA_PLUS` model](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series)
with linear external regressors. For more information, see [ARIMA\_PLUS: Large-scale, Accurate, Automatic and Interpretable In-Database Time Series Forecasting and Anomaly Detection in Google BigQuery](https://arxiv.org/abs/2510.24452). The following diagram shows the model pipeline:

For a diagram that shows the details of the **ARIMA\_PLUS Pipeline** section
in the preceding diagram, see
[Time series modeling pipeline](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series#modeling-pipeline).

The modeling pipeline for the `ARIMA_PLUS` time series models performs the
following functions:

* Infer the data frequency of the time series.
* Handle irregular time intervals.
* Handle duplicated timestamps by taking the mean value.
* Interpolate missing data using local linear interpolation.
* Detect and clean spike and dip outliers.
* Detect and adjust abrupt step (level) changes.
* Detect and adjust holiday effect.
* Detect multiple seasonal patterns within a single time series by using
  [Seasonal and Trend decomposition using Loess (STL)](https://otexts.com/fpp2/stl.html),
  and extrapolate seasonality by using
  [double exponential smoothing (ETS)](https://en.wikipedia.org/wiki/Exponential_smoothing#Double_exponential_smoothing).
* Detect and model the trend using the ARIMA model and the
  [auto.ARIMA](https://otexts.com/fpp2/arima-r.html)
  algorithm for automatic hyperparameter tuning. In auto.ARIMA, dozens of
  candidate models are trained and evaluated in parallel. The model with the
  lowest
  [Akaike information criterion (AIC)](https://en.wikipedia.org/wiki/Akaike_information_criterion)
  is selected as the best model.

## Large-scale time series

You can forecast up to 100,000,000 time series simultaneously with a single query
by using the [`TIME_SERIES_ID_COL`](#time_series_id_col)
option. With this option, different modeling pipelines run in parallel, as long
as enough [slots](/bigquery/docs/slots) are available. The following diagram
shows this process:

## Large-scale time series forecasting best practices

Forecasting many time series simultaneously can lead to long-running
queries, because query processing isn't completely parallel due to limited
slot capacity. The following best practices can help you avoid long-running
queries when forecasting many time series simultaneously:

* When you have a large number (for example, 100,000) of time series to
  forecast, first forecast a small number of time series (for example, 1,000)
  to see how long the query takes. You can then estimate how long your entire
  time series forecast will take.
* You can use the `AUTO_ARIMA_MAX_ORDER` option to balance between query
  run time and forecast accuracy. Increasing `AUTO_ARIMA_MAX_ORDER`
  expands the hyperparameter search space to try more complex ARIMA models, that
  is, ARIMA models with higher non-seasonal p and q. This increases forecast
  accuracy but also increases query run time. Decreasing the value of
  `AUTO_ARIMA_MAX_ORDER` decreases forecast accuracy but also decreases query
  run time. For example, if you specify a value of `1` instead of using the
  `2` for this option, the query run time is reduced
  by more than 50%. The forecast accuracy might drop slightly for some of the
  time series. If a shorter training time is important to your use case, use a
  smaller value for `AUTO_ARIMA_MAX_ORDER`.
* The model training time for each time series has a linear relationship to its
  length, which is based on the number of data points. The longer the
  time series, the longer the training takes. However, not all data points
  contribute equally to the model fitting process. Instead, the more
  recent the data point is, the more it contributes to the process. Therefore,
  if you have a long time series, for example ten years of daily data, you
  don't need to train a time series model using all of the data points. The
  most recent two or three years of data points are enough.
* You can use the `TIME_SERIES_LENGTH_FRACTION`, `MIN_TIME_SERIES_LENGTH` and
  `MAX_TIME_SERIES_LENGTH` training options to enable fast model training
  with little to no loss of forecasting accuracy. The idea behind these options
  is that while periodic modeling, such as seasonality, requires a certain
  number of time points, trend modeling doesn't need many time points. However,
  trend modeling is much more computationally expensive than other time series
  components. By using the aforementioned training options, you can efficiently
  model the trend component with a subset of the time series, while the other
  time series components use the entire time series.
* To avoid a single long-running query, use BigQuery
  [multi-statement queries](/bigquery/docs/multi-statement-queries).
* In some cases, your input table might be missing values in the feature columns.
  For example, in a multivariate time series with features A and B, most of the
  rows contain valid values for both A and B, while some might have `NULL`
  values for one or the other of the features. BigQuery ML fills
  in the missing values by using the mean value of the entire data column, which
  might include values from different time series. This causes discrepancies in
  the results when compared to single time series training, because the input
  values are affected by other time series. The best practice is to analyze the
  data and impute the missing feature values before running `CREATE MODEL`.
  For example, using the mean value of that feature within each time series, or
  assigning a value of zero.

## `CREATE MODEL` syntax

```
{CREATE MODEL | CREATE MODEL IF NOT EXISTS | CREATE OR REPLACE MODEL}
model_name
OPTIONS(model_option_list)
AS { query_statement |
  (
    training_data AS (query_statement),
    custom_holiday AS (holiday_statement)
  )
}

model_option_list:
MODEL_TYPE = 'ARIMA_PLUS_XREG'
    [, TIME_SERIES_TIMESTAMP_COL = string_value ]
    [, TIME_SERIES_DATA_COL = string_value ]
    [, TIME_SERIES_ID_COL = { string_value | string_array } ]
    [, HORIZON = int64_value ]
    [, AUTO_ARIMA = { TRUE | FALSE } ]
    [, AUTO_ARIMA_MAX_ORDER = int64_value ]
    [, AUTO_ARIMA_MIN_ORDER = int64_value ]
    [, NON_SEASONAL_ORDER = (int64_value, int64_value, int64_value) ]
    [, DATA_FREQUENCY = { 'AUTO_FREQUENCY' | 'PER_MINUTE' | 'HOURLY' | 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'QUARTERLY' | 'YEARLY' } ]
    [, INCLUDE_DRIFT = { TRUE | FALSE } ]
    [, HOLIDAY_REGION = string_value | string_array ]
    [, CLEAN_SPIKES_AND_DIPS = { TRUE | FALSE } ]
    [, ADJUST_STEP_CHANGES = { TRUE | FALSE } ]
    [, TIME_SERIES_LENGTH_FRACTION = float64_value ]
    [, MIN_TIME_SERIES_LENGTH = int64_value ]
    [, MAX_TIME_SERIES_LENGTH = int64_value ]
    [, TREND_SMOOTHING_WINDOW_SIZE = int64_value ]
    [, L2_REG = float64_value ]
    [, MODEL_REGISTRY = { 'VERTEX_AI' } ]
    [, VERTEX_AI_MODEL_ID = string_value ]
    [, VERTEX_AI_MODEL_VERSION_ALIASES = string_array ]
    [, KMS_KEY_NAME = string_value ]
```

### `CREATE MODEL`

Creates and trains a new model in the specified dataset. If the model name
exists, `CREATE MODEL` returns an error.

### `CREATE MODEL IF NOT EXISTS`

Creates and trains a new model only if the model doesn't exist in the
specified dataset.

### `CREATE OR REPLACE MODEL`

Creates and trains a model and replaces an existing model with the same name in
the specified dataset.

### `model_name`

The name of the model you're creating or replacing. The model
name must be unique in the dataset: no other model or table can have the same
name. The model name must follow the same naming rules as a
BigQuery table. A model name can:

* Contain up to 1,024 characters
* Contain letters (upper or lower case), numbers, and underscores

`model_name` is case-sensitive.

If you don't have a default project configured, then you must prepend the
project ID to the model name in the following format, including backticks:

`[PROJECT\_ID].[DATASET].[MODEL]`

For example, `myproject.mydataset.mymodel`.

### `MODEL_TYPE`

**Syntax**

```
MODEL_TYPE = 'ARIMA_PLUS_XREG'
```

**Description**

Specifies the model type. This option is required.

### `TIME_SERIES_TIMESTAMP_COL`

**Syntax**

`TIME_SERIES_TIMESTAMP_COL = string_value`

**Description**

The name of the column that provides the time points used in
training the model. The column must be of one of the following data types:

* `TIMESTAMP`
* `DATE`
* `DATETIME`

**Arguments**

A `STRING` value.

### `TIME_SERIES_DATA_COL`

**Syntax**

`TIME_SERIES_DATA_COL = string_value`

**Description**

The name of the column that contains the data to forecast. The column must be
of one of the following data types:

* `INT64`
* `NUMERIC`
* `BIGNUMERIC`
* `FLOAT64`

**Arguments**

A `STRING` value.

### `TIME_SERIES_ID_COL`

**Syntax**

`TIME_SERIES_ID_COL = { string_value | string_array }`

**Description**

The names of the ID columns. Specify one or more values for this option when
you want to fit and forecast multiple time series using a single query.
Each ID identifies a unique time series. The columns must be
of one of the following data types:

* `STRING`
* `INT64`
* `ARRAY<STRING>`
* `ARRAY<INT64>`

**Arguments**

A `STRING` or `ARRAY<STRING>` value.

### `HORIZON`

**Syntax**

`HORIZON = int64_value`

**Description**

The number of time points to forecast.

**Arguments**

An `INT64` value. The default value is `1,000`. The maximum value is `10,000`.

### `AUTO_ARIMA`

**Syntax**

```
AUTO_ARIMA = { TRUE | FALSE }
```

**Description**

Determines whether the training process uses auto.ARIMA or not. If `TRUE`,
training automatically finds the best non-seasonal order (that is, the p, d,
q tuple) and decides whether or not to include a linear drift term when d is 1.
If `FALSE`, you must specify the `NON_SEASONAL_ORDER` option.

**Arguments**

A `BOOL` value. The default value is `TRUE`.

### `AUTO_ARIMA_MAX_ORDER`

**Syntax**

`AUTO_ARIMA_MAX_ORDER = int64_value`

**Description**

The maximum value for the sum of non-seasonal p and q. This value determines
the parameter search space in the auto.ARIMA algorithm, in combination with the
`AUTO_ARIMA_MIN_ORDER` value. This option is disabled when the `AUTO_ARIMA`
value is `FALSE`.

**Arguments**

An `INT64` value between `1` and `5`, inclusive. The default value is `2`.

If non-seasonal d is determined to be 0 or 2, the number of candidate models
evaluated for each supported value is as follows:

* `1`: 3 candidate models
* `2`: 6 candidate models
* `3`: 10 candidate models
* `4`: 15 candidate models
* `5`: 21 candidate models

If non-seasonal d is determined to be 1, the number of candidate models to
evaluate is doubled, because there's an additional drift term to consider for
all of the existing candidate models.

**Note:** the number of bytes processed by the input `SELECT` statement is
multiplied by the number of candidate models, which is controlled by
the `AUTO_ARIMA_MAX_ORDER` and `AUTO_ARIMA_MIN_ORDER` options.
This affects the pricing. See [BigQuery ML pricing](https://cloud.google.com/bigquery/pricing#bqml)
for details.

### `AUTO_ARIMA_MIN_ORDER`

**Syntax**

`AUTO_ARIMA_MIN_ORDER = int64_value`

**Description**

The minimum value for the sum of non-seasonal p and q. This value determines
the parameter search space in the auto.ARIMA algorithm, in combination with the
`AUTO_ARIMA_MAX_ORDER` value. Setting this option to `1` or greater lets the
model exclude some flat forecasting results. This option is disabled when
`AUTO_ARIMA` is `FALSE`.

**Arguments**

The value is a `INT64`. The default value is `0`.

**Note:** If `AUTO_ARIMA_MAX_ORDER` is set, the `AUTO_ARIMA_MIN_ORDER` value must
be less than the `AUTO_ARIMA_MAX_ORDER` value.

### `NON_SEASONAL_ORDER`

**Syntax**

`NON_SEASONAL_ORDER = (p_value, d_value, q_value)`

**Description**

The tuple of non-seasonal p, d, q for the `ARIMA_PLUS` model. There are no
default values, and you must specify all three values. p and q must be a value
between `0` and `5`, inclusive. d must be a value between `0` and `2`,
inclusive.

The `AUTO_ARIMA` value must be `FALSE` to use this option.

**Arguments**

A tuple of three `INT64` values. For example, `(1, 2, 1)`.

### `DATA_FREQUENCY`

**Syntax**

```
DATA_FREQUENCY = { 'AUTO_FREQUENCY' | 'PER_MINUTE' | 'HOURLY' | 'DAILY' | 'WEEKLY' | 'MONTHLY' | 'QUARTERLY' | 'YEARLY' }
```

**Description**

The data frequency of the input time series. The finest supported granularity is
`PER_MINUTE`.

**Arguments**

This option accepts the following values:

* `AUTO_FREQUENCY`: This is the default. The training process automatically
  infers the data frequency, which can be any of the other supported values for
  this option.
* `PER_MINUTE`
* `HOURLY`
* `DAILY`
* `WEEKLY`
* `MONTHLY`
* `QUARTERLY`
* `YEARLY`

### `INCLUDE_DRIFT`

**Syntax**

```
INCLUDE_DRIFT = { TRUE | FALSE }
```

**Description**

Determines whether the `ARIMA_PLUS` model should include a linear drift term or
not. The drift term is applicable when non-seasonal d is 1.

* When the `AUTO_ARIMA` value is `FALSE`, this argument defaults to `FALSE`.
  You can set it to `TRUE` only when non-seasonal d is 1. Otherwise the
  `CREATE MODEL` statement returns an invalid query error.
* When the `AUTO_ARIMA` value is `TRUE`, BigQuery ML
  automatically determines whether or not to include a linear drift term, so
  you can't use this option.

**Arguments**

A `BOOL` value. The default value is `FALSE`.

### `HOLIDAY_REGION`

**Syntax**

`HOLIDAY_REGION = string_value | string_array`

**Description**

The geographical region based on which the holiday effect is applied in
modeling. By default, holiday effect modeling isn't used. To use it,
specify one or more holiday regions using this option. If you include more than
one region string, the union of the holidays in all the provided regions are
taken into account when modeling.

Holiday effect modeling is only applicable when the time series is daily
or weekly, and longer than a year. If the input time series doesn't meet these
requirements, holiday effect modeling isn't used even if you specify
this option.

For more information about the holidays included in each region, see
[Holiday data](#holiday_data).

**Arguments**

A `STRING` or `ARRAY<STRING>` value.

Use a single string value to identify one region. For example:

```
HOLIDAY_REGION = 'GLOBAL'
```

Use an array of string values to identify multiple regions. For example:

```
HOLIDAY_REGION = ['US', 'GB']
```

This option accepts the following values:

**Global**

* `GLOBAL`

**Continental regions**

* `NA`: North America
* `JAPAC`: Japan and Asia Pacific
* `EMEA`: Europe, the Middle East and Africa
* `LAC`: Latin America and the Caribbean

**Countries**

* `AE`: United Arab Emirates
* `AR`: Argentina
* `AT`: Austria
* `AU`: Australia
* `BE`: Belgium
* `BR`: Brazil
* `CA`: Canada
* `CH`: Switzerland
* `CL`: Chile
* `CN`: China
* `CO`: Colombia
* `CZ`: Czechia
* `DE`: Germany
* `DK`: Denmark
* `DZ`: Algeria
* `EC`: Ecuador
* `EE`: Estonia
* `EG`: Egypt
* `ES`: Spain
* `FI`: Finland
* `FR`: France
* `GB`: United Kingdom
* `GR`: Greece
* `HK`: Hong Kong
* `HU`: Hungary
* `ID`: Indonesia
* `IE`: Ireland
* `IL`: Israel
* `IN`: India
* `IR`: Iran
* `IT`: Italy
* `JP`: Japan
* `KR`: South Korea
* `LV`: Latvia
* `MA`: Morocco
* `MX`: Mexico
* `MY`: Malaysia
* `NG`: Nigeria
* `NL`: Netherlands
* `NO`: Norway
* `NZ`: New Zealand
* `PE`: Peru
* `PH`: Philippines
* `PK`: Pakistan
* `PL`: Poland
* `PT`: Portugal
* `RO`: Romania
* `RS`: Serbia
* `RU`: Russia
* `SA`: Saudi Arabia
* `SE`: Sweden
* `SG`: Singapore
* `SI`: Slovenia
* `SK`: Slovakia
* `TH`: Thailand
* `TR`: Turkey
* `TW`: Taiwan
* `UA`: Ukraine
* `US`: United States
* `VE`: Venezuela
* `VN`: Vietnam
* `ZA`: South Africa

### `CLEAN_SPIKES_AND_DIPS`

**Syntax**

```
CLEAN_SPIKES_AND_DIPS = { TRUE | FALSE }
```

**Description**

Determines whether or not to perform automatic spikes and dips detection and
cleanup in the `ARIMA_PLUS` model training pipeline. The spikes and dips are
replaced with local linear interpolated values when they're detected.

**Arguments**

A `BOOL` value. The default value is `TRUE`.

### `ADJUST_STEP_CHANGES`

**Syntax**