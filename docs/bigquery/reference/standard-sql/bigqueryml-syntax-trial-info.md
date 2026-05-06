* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.TRIAL\_INFO function

This document describes the `ML.TRIAL_INFO` function, which lets you display
information about trials from a model that uses
[hyperparameter tuning](/bigquery/docs/hp-tuning-overview).

You can use this function with models that support
[hyperparameter tuning](/bigquery/docs/hp-tuning-overview). For more
information, see
[End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).

## Syntax

```
ML.TRIAL_INFO(MODEL `PROJECT_ID.DATASET.MODEL_NAME`)
```

### Arguments

`ML.TRIAL_INFO` takes the following arguments:

* `PROJECT_ID`: your project ID.
* `DATASET`: the BigQuery dataset that
  contains the model.
* `MODEL_NAME`: The name of the model.

## Output

`ML.TRIAL_INFO` returns one row per trial with the following columns:

* `trial_id`: an `INT64` value that contains the ID assigned to each trial in
  the approximate order of trial execution. `trial_id` values start from `1`.
* `hyperparameters`: a `STRUCT` value that contains the hyperparameters used in
  the trial.
* `hparam_tuning_evaluation_metrics`: a `STRUCT` value that contains the
  evaluation metrics appropriate to the hyperparameter tuning objective
  specified by the
  [`hparam_tuning_objectives` argument](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#hparam_tuning_objectives)
  in the `CREATE MODEL` statement. Metrics are calculated from the evaluation
  data. For more information about the datasets used in hyperparameter tuning,
  see [Data split](/bigquery/docs/hp-tuning-overview#data_split).
* `training_loss`: a `FLOAT64` value that contains the loss of the trial during
  the last iteration, calculated using the training data.
* `eval_loss`: a `FLOAT64` value that contains the loss of the trial during the
  last iteration, calculated using the evaluation data.
* `status`: a `STRING` value that contains the final status of the trial.
  Possible values include the following:

  + `SUCCEEDED`: the trial succeeded.
  + `FAILED`: the trial failed.
  + `INFEASIBLE`: the trial was not run due to an invalid combination of
    hyperparameters.
* `error_message`: a `STRING` value that contains the error message that is
  returned if the trial didn't succeed. For more information, see
  [Error handling](/bigquery/docs/hp-tuning-overview#error_handling).
* `is_optimal`: a `BOOL` value that indicates whether the trial had the best
  objective value. If multiple trials are marked as optimal, then the trial
  with the smallest `trial_id` value is used as the default trial during model
  serving.

## Example

The following query retrieves information of all trials for the model
`mydataset.mymodel` in your default project:

```
SELECT
  *
FROM
  ML.TRIAL_INFO(MODEL `mydataset.mymodel`)
```

## What's next

* For information about hyperparameter tuning, see
  [Hyperparameter tuning overview](/bigquery/docs/hp-tuning-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-05 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-05 UTC."],[],[]]