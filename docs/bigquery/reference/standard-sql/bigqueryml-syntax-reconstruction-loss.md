* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.RECONSTRUCTION\_LOSS function

This document describes the `ML.RECONSTRUCTION_LOSS` function, which you can use
to compute the reconstruction losses between the input and output data of an
[autoencoder model](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder).

## Syntax

```
ML.RECONSTRUCTION_LOSS(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  { TABLE `PROJECT_ID.DATASET.TABLE` | (QUERY_STATEMENT) }
)
```

### Arguments

`ML.RECONSTRUCTION_LOSS` takes the following arguments:

* `PROJECT_ID`: the project that contains the
  resource.
* `DATASET`: the dataset that contains the
  resource.
* `MODEL`: the name of the model.
* `TABLE`: the name of the input data table.

  If you specify `TABLE`, the input column names in the table must match
  the column names in the model, and their types must be compatible according to
  BigQuery [implicit coercion rules](/bigquery/docs/reference/standard-sql/conversion_rules#coercion).
* `QUERY_STATEMENT`: the GoogleSQL
  query to use for input data to generate the reconstruction losses. For
  the supported SQL syntax of the `QUERY_STATEMENT` clause in
  GoogleSQL, see
  [Query syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).

  If you specify `QUERY_STATEMENT`, the input column names from the query must
  match the column names in the model, and their types must be compatible
  according to BigQuery [implicit coercion rules](/bigquery/docs/reference/standard-sql/conversion_rules#coercion).

  If you used the
  [`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform)
  in the `CREATE MODEL` statement that created the model,
  then you can only use the input columns present in the `TRANSFORM` clause
  in the `QUERY_STATEMENT`.

## Output

`ML.RECONSTRUCTION_LOSS` returns the following columns:

* `mean_absolute_error`: a `FLOAT64` value that contains the
  [mean absolute error](https://en.wikipedia.org/wiki/Mean_absolute_error) for
  the model.
* `mean_squared_error`: a `FLOAT64` value that contains the
  [mean squared error](https://en.wikipedia.org/wiki/Mean_squared_error) for
  the model.
* `mean_squared_log_error`: a `FLOAT64` value that contains the mean squared
  log error for the model.

## Limitations

`ML.RECONSTRUCTION_LOSS` doesn't support
[imported TensorFlow models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow).

## Example

The following query computes reconstruction losses for the model
`mydataset.mymodel` in your default project:

```
SELECT *
FROM ML.RECONSTRUCTION_LOSS(
  MODEL `mydataset.mymodel`,
  (SELECT column1,
          column2,
          column3,
          column4
   FROM `mydataset.mytable`)
)
```

## What's next

* For more information about model evaluation, see
  [BigQuery ML model evaluation overview](/bigquery/docs/evaluate-overview).
* For more information about supported SQL statements and functions for ML
  models, see
  [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-13 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-13 UTC."],[],[]]