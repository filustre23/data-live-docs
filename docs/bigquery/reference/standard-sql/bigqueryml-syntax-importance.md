* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.FEATURE\_IMPORTANCE function

This document describes the `ML.FEATURE_IMPORTANCE` function, which lets you
see the feature importance score. This score indicates how useful or valuable
each feature was in the construction of a boosted tree or a random forest model
during training. For more information, see the
[`feature_importances` property](https://xgboost.readthedocs.io/en/latest/python/python_api.html#xgboost.XGBRegressor.feature_importances_)
in the XGBoost library.

## Syntax

```
ML.FEATURE_IMPORTANCE(
  MODEL `PROJECT_ID.DATASET.MODEL`
)
```

### Arguments

`ML.FEATURE_IMPORTANCE` takes the following arguments:

* `PROJECT_ID`: your project ID.
* `DATASET`: the BigQuery dataset that contains
  the model.
* `MODEL`: the name of the model.

## Output

`ML.FEATURE_IMPORTANCE` returns the following columns:

* `feature`: a `STRING` value that contains the name of the feature column
  in the input training data.
* `importance_weight`: a `FLOAT64` value that contains the number of times a
  feature is used to split the data across all trees.
* `importance_gain`: a `FLOAT64` value that contains the average gain across all
  splits the feature is used in.
* `importance_cover`: a `FLOAT64` value that contains the average coverage
  across all splits the feature is used in.

If the [`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform)
was used in the `CREATE MODEL` statement that created the model,
`ML.FEATURE_IMPORTANCE` returns the information of the pre-transform columns
from the `query_statement` clause of the `CREATE MODEL` statement.

## Permissions

You must have the `bigquery.models.create` and `bigquery.models.getData`
[Identity and Access Management (IAM) permissions](/bigquery/docs/access-control#bq-permissions)
in order to run `ML.FEATURE_IMPORTANCE`.

## Limitations

`ML.FEATURE_IMPORTANCE` is only supported with
[boosted tree models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree)
and
[random forest models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest).

## Example

This example retrieves feature importance from `mymodel` in
`mydataset`. The dataset is in your default project.

```
SELECT
  *
FROM
  ML.FEATURE_IMPORTANCE(MODEL `mydataset.mymodel`)
```

## What's next

* For more information about Explainable AI, see
  [BigQuery Explainable AI overview](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-xai-overview).
* For more information about supported SQL statements and functions for ML
  models, see
  [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-15 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-15 UTC."],[],[]]