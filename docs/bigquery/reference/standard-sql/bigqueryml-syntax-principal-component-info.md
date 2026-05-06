* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.PRINCIPAL\_COMPONENT\_INFO function

This document describes the `ML.PRINCIPAL_COMPONENT_INFO` function, which lets
you see the statistics of the principal components in a principal component
analysis (PCA) model, such as
[eigenvalue](https://en.wikipedia.org/wiki/Eigenvalues_and_eigenvectors)
and explained variance ratio.

## Syntax

```
ML.PRINCIPAL_COMPONENT_INFO(
  MODEL `PROJECT_ID.DATASET.MODEL`
)
```

### Arguments

`ML.PRINCIPAL_COMPONENT_INFO` takes the following arguments:

* `PROJECT_ID`: your project ID.
* `DATASET`: the BigQuery dataset that contains
  the model.
* `MODEL`: the name of the model.

## Output

`ML.PRINCIPAL_COMPONENT_INFO` returns the following columns:

* `principal_component_id`: an `INT64` that contains the principal
  component. The table is ordered in descending order of the `eigenvalue`
  value.
* `eigenvalue`: a `FLOAT64` value that contains the factor by which the
  eigenvector is scaled. Eigenvalue and explained variance are the same
  concepts in PCA.
* `explained_variance_ratio`: a `FLOAT64` value that contains the explained
  variance ratio, which is the ratio between the variance, also known as
  eigenvalue, of that principal component and the total variance. The total
  variance is the sum of the variances from all of the individual principal
  components.
* `cumulative_explained_variance_ratio`: a `FLOAT64` value that contains
  the cumulative explained variance ratio of the k-th principal component,
  which is the sum of the explained variance ratios of all
  the previous principal components, including the k-th principal component.

## Example

The following example retrieves the eigenvalue-related information of each
principal component in the model `mydataset.mymodel` in your default project.

```
SELECT
  *
FROM
  ML.PRINCIPAL_COMPONENT_INFO(MODEL `mydataset.mymodel`)
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