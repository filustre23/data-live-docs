* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.FEATURE\_INFO function

This document describes the `ML.FEATURE_INFO` function, which lets you see
information about the input features that are used to train a model.

For more information about which models support this function, see
[End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).

## Syntax

```
ML.FEATURE_INFO(MODEL `PROJECT_ID.DATASET.MODEL_NAME`)
```

### Arguments

`ML.FEATURE_INFO` takes the following arguments:

* `PROJECT_ID`: Your project ID.
* `DATASET`: The BigQuery dataset
  that contains the model.
* `MODEL_NAME`: The name of the model.

## Output

`ML.FEATURE_INFO` returns the following columns:

* `input`: a `STRING` value that contains the name of the column in the
  input training data.
* `min`: a `FLOAT64` value that contains the minimum value in the `input`
  column. `min` is `NULL` for non-numeric inputs.
* `max`: a `FLOAT64` value that contains the maximum value in the `input`
  column. `max` is `NULL` for non-numeric inputs.
* `mean`: a `FLOAT64` value that contains the average value for the `input`
  column. `mean` is `NULL` for non-numeric inputs.
* `median`: a `FLOAT64` value that contains the median value for the `input`
  column. `median` is `NULL` for non-numeric inputs.
* `stddev`: a `FLOAT64` value that contains the standard deviation value for
  the `input` column. `stddev` is `NULL` for non-numeric inputs.
* `category_count`: an `INT64` value that contains the number of categories
  in the `input` column. `category_count` is `NULL` for non-categorical columns.
* `null_count`: an `INT64` value that contains the number of `NULL` values
  in the `input` column.
* `dimension`: an `INT64` value that contains the dimension of the `input`
  column if the `input` column has a `ARRAY<STRUCT>` type. `dimension` is
  `NULL` for non-`ARRAY<STRUCT>` columns.

For [matrix factorization](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization)
models, only `category_count` is calculated for the `user` and `item`
columns.

If you used the
[`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform)
in the `CREATE MODEL` statement that created the model, `ML.FEATURE_INFO`
outputs the information of the pre-transform columns from the
`query_statement` argument.

## Permissions

You must have the `bigquery.models.create` and `bigquery.models.getData`
[Identity and Access Management (IAM) permissions](/bigquery/docs/access-control#bq-permissions)
in order to run `ML.FEATURE_INFO`.

## Limitations

`ML.FEATURE_INFO` doesn't support
[imported TensorFlow models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow).

## Example

The following example retrieves feature information from the model
`mydataset.mymodel` in your default project:

```
SELECT
  *
FROM
  ML.FEATURE_INFO(MODEL `mydataset.mymodel`)
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-01 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-01 UTC."],[],[]]