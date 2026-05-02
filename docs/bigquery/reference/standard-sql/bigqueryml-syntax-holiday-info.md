* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.HOLIDAY\_INFO function

This document describes the `ML.HOLIDAY_INFO` function, which you can use to
return the list of holidays being modeled by an
[`ARIMA_PLUS`](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series)
or
[`ARIMA_PLUS_XREG`](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series)
time series forecasting model.

## Syntax

```
ML.HOLIDAY_INFO(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`
)
```

### Arguments

`ML.HOLIDAY_INFO` takes the following arguments:

* `PROJECT_ID`: your project ID.
* `DATASET`: the BigQuery dataset that contains
  the model.
* `MODEL_NAME`: the name of the model.

## Output

`ML.HOLIDAY_INFO` returns the following columns:

* `region`: a `STRING` value that identifies the holiday region.
* `holiday_name`: a `STRING` value that identifies the holiday.
* `primary_date`: a `DATE` value that identifies the date the holiday
  falls on.
* `preholiday_days`: an `INT64` value that identifies the start of the
  holiday window around the holiday that was taken into account when
  modeling.
* `postholiday_days`: an `INT64` value that identifies the end of the
  holiday window around the holiday that was taken into account when
  modeling.

## Example

The following example returns the results for a model that uses a
[custom holiday](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series#custom_holidays):

```
SELECT * FROM
ML.HOLIDAY_INFO(MODEL `mydataset.arima_model`);
```

The output looks similar to the following:

```
+-----------------------+--------------+-----------------+------------------+
| region | holiday_name | primary_date | preholiday_days | postholiday_days |
+--------------------------------------------------------+------------------+
| US     | Members day  | 2001-10-21   | 3               | 1                |
+-----------------------+--------------+-----------------+------------------+
| US     | Members day  | 2002-10-22   | 3               | 1                |
+-----------------------+--------------+-----------------+------------------+
| US     | Members day  | 2003-10-21   | 3               | 1                |
+-----------------------+--------------+-----------------+------------------+
| US     | Members day  | 2004-10-23   | 3               | 1                |
+-----------------------+--------------+-----------------+------------------+
```

## Limitation

* Results returned by `ML.HOLIDAY_INFO` only indicate the holiday information
  used during model fitting. They don't necessarily indicate the detection of a
  holiday effect. Use [`ML.EXPLAIN_FORECAST`](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast)
  instead for actual holiday effect results.

## What's next

* For more information about model evaluation, see
  [BigQuery ML model evaluation overview](/bigquery/docs/evaluate-overview).
* For more information about supported SQL statements and functions for time
  series forecasting models, see
  [End-to-end user journeys for time series forecasting models](/bigquery/docs/e2e-journey-forecast).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-01 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-01 UTC."],[],[]]