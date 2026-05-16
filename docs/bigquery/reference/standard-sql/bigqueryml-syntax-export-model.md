* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The EXPORT MODEL statement

To export an existing model from BigQuery ML to
[Cloud Storage](/storage/docs), use the `EXPORT MODEL`
statement.

For more information about supported model types, formats, and limitations, see
[Export models](/bigquery/docs/exporting-models).

For more information about supported SQL statements and functions for exportable
models, see the following documents:

* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [End-to-end user journeys for imported models](/bigquery/docs/e2e-journey-import)

## Syntax

The following is the syntax of `EXPORT MODEL` for a regular model that is not generated from BigQuery ML hyperparameter tuning.

```
EXPORT MODEL MODEL_NAME [OPTIONS(URI = STRING_VALUE)]
```

* `MODEL_NAME` is the name of the BigQuery ML
  model you're exporting. If you are exporting a model in another project,
  you must specify the project, dataset, and model in the following format,
  including backticks:

  ```
  `PROJECT.DATASET.MODEL`
  ```

  For example, `` `myproject.mydataset.mymodel` ``.

  If the model name does not exist in the dataset, the following error is
  returned:

  `Error: Not found: Model myproject:mydataset.mymodel`
* `STRING_VALUE` is the [URI of a Cloud Storage](/bigquery/docs/loading-data-cloud-storage#gcs-uri) bucket where the model
  is exported. This option is required for the `EXPORT MODEL` statement. For
  example:

  ```
  URI = 'gs://bucket/path/to/saved_model/'
  ```

For a model that is generated from BigQuery ML hyperparameter tuning,
`EXPORT MODEL` can also export an individual trial to a destination URI. For example:

```
EXPORT MODEL MODEL_NAME [OPTIONS(URI = STRING_VALUE [, TRIAL_ID = INT_VALUE])]
```

* `INT_VALUE` is the numeric ID of the exporting trial.
  For example:

  ```
  ```sql
  TRIAL_ID = 12
  ```
  ```
* If `TRIAL_ID` is not specified, then the optimal trial is exported by default.




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-15 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-15 UTC."],[],[]]