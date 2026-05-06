* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.PRINCIPAL\_COMPONENTS function

This document describes the `ML.PRINCIPAL_COMPONENTS` function, which lets you
see the principal components of a principal component analysis (PCA) model.
Principal components and
[eigenvectors](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors)
are the same concepts in PCA models.

## Syntax

```
ML.PRINCIPAL_COMPONENTS(
  MODEL `PROJECT_ID.DATASET.MODEL`
)
```

### Arguments

`ML.PRINCIPAL_COMPONENTS` takes the following arguments:

* `PROJECT_ID`: your project ID.
* `DATASET`: the BigQuery dataset that contains
  the model.
* `MODEL`: the name of the model.

## Output

`ML.PRINCIPAL_COMPONENTS` returns the following columns:

* `principal_component_id`: an `INT64` that contains the principal
  component ID.
* `feature`: a `STRING` value that contains the feature column name.
* `numerical_value`: a `FLOAT64` value that contains the feature value for the
  principal component that `principal_component_id` identifies if the column
  identified by the `feature` value is numeric. Otherwise,
  `numerical_value` is `NULL`.
* `categorical_value`: an `ARRAY<STRUCT>` value that contains information
  about categorical features. Each struct contains the following fields:

  + `categorical_value.category`: a `STRING` value that contains the name of
    each category.
  + `categorical_value.value`: a `FLOAT64` value that contains the value of
    `categorical_value.category` for the principal component that
    `principal_component_id` identifies.

The output is in descending order by the eigenvalues of the principal
components, which you can get by using the
[`ML.PRINCIPAL_COMPONENT_INFO` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-principal-component-info).

## Example

The following example retrieves the principal components from the model
`mydataset.mymodel` in your default project:

```
SELECT
  *
FROM
  ML.PRINCIPAL_COMPONENTS(MODEL `mydataset.mymodel`)
```

## What's next

* For more information about model weights support in BigQuery ML, see
  [BigQuery ML model weights overview](/bigquery/docs/weights-overview).
* For more information about supported SQL statements and functions for ML
  models, see
  [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-05 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-05 UTC."],[],[]]