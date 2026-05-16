* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.GLOBAL\_EXPLAIN function

This document describes the `ML.GLOBAL_EXPLAIN` function, which lets you provide
explanations for the entire model by aggregating the local explanations of the evaluation data. You can only use `ML.GLOBAL_EXPLAIN` with models that are trained with the
[`ENABLE_GLOBAL_EXPLAIN` option](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#enable_global_explain)
set to `TRUE`.

## Syntax

```
ML.GLOBAL_EXPLAIN(
  MODEL `PROJECT_ID.DATASET.MODEL`,
  STRUCT(
    [CLASS_LEVEL_EXPLAIN AS class_level_explain]))
```

### Arguments

`ML.GLOBAL_EXPLAIN` takes the following arguments:

* `PROJECT_ID`: your project ID.
* `DATASET`: the BigQuery dataset that contains
  the model.
* `MODEL`: the name of the model.
* `CLASS_LEVEL_EXPLAIN`: a `BOOL` value that specifies
  whether global feature importances are returned for each class. Applies only
  to non-AutoML Tables classification models. When set to `FALSE`, the global
  feature importance of the entire model is returned rather than that of each
  class. The default value is `FALSE`.

  Regression models and AutoML Tables classification models only have
  model-level global feature importance.

## Output

The output of `ML.GLOBAL_EXPLAIN` has two formats:

* For classification models with `class_level_explain` set
  to `FALSE`, and for regression models, the following columns are returned:

  + `feature`: a `STRING` value that contains the feature name.
  + `attribution`: a `FLOAT64` value that contains the feature importance to
    the model overall.
* For classification models with `class_level_explain` set to `TRUE`,
  the following columns are returned:

  + `<class_name>`: a `STRING` value that contains the name of the class in the
    label column.
  + `feature`: a `STRING` value that contains the feature name.
  + `attribution`: a `FLOAT64` value that contains the feature importance to
    this class.

  For each class, only the top 10 most important features are returned.

## Examples

The following examples assume your model is in your default project.

### Regression model

This example gets global feature importance for the boosted tree regression
model `mymodel` in `mydataset`. The dataset is in your default project.

```
SELECT
  *
FROM
  ML.GLOBAL_EXPLAIN(MODEL `mydataset.mymodel`)
```

### Classifier model

This example gets global feature importance for the boosted tree classifier
model `mymodel` in `mydataset`. The dataset is in your default project.

```
SELECT
  *
FROM
  ML.GLOBAL_EXPLAIN(MODEL `mydataset.mymodel`, STRUCT(TRUE AS class_level_explain))
```

## What's next

* For information about Explainable AI, see
  [BigQuery Explainable AI overview](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-xai-overview).
* For more information about supported SQL statements and functions for ML
  models, see
  [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-15 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-15 UTC."],[],[]]