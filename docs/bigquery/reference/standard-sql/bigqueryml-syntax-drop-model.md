* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The DROP MODEL statement

To delete a model in BigQuery ML, use the `DROP MODEL` or the `DROP
MODEL IF EXISTS` DDL statement.

The `DROP MODEL` DDL statement deletes a model in the specified dataset. If
the model name does not exist in the dataset, the following error is returned:

`Error: Not found: Model myproject:mydataset.mymodel`

The `DROP MODEL IF EXISTS` DDL statement deletes a model in the specified
dataset only if the model exists. If the model name does not exist in the
dataset, no error is returned, and no action is taken.

If you are deleting a model in another project, you must specify the project,
dataset, and model in the following format: `[PROJECT].[DATASET].[MODEL]`
(including the backticks); for example, `myproject.mydataset.mymodel`.

For more information about supported SQL statements and functions for different
model types, see the following documents:

* [End-to-end user journeys for generative AI models](/bigquery/docs/e2e-journey-genai)
* [End-to-end user journeys for time series forecasting models](/bigquery/docs/e2e-journey-forecast)
* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [End-to-end user journeys for imported models](/bigquery/docs/e2e-journey-import)

## Syntax

```
{DROP MODEL | DROP MODEL IF EXISTS}
model_name
```

Where:

**`{DROP MODEL | DROP MODEL IF EXISTS}`** is one of the following statements:

* `DROP MODEL` — deletes a model in the specified dataset
* `DROP MODEL IF EXISTS` — deletes a model only if the model exists in the
  specified dataset

**`model_name`** is the name of the model you're deleting.




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-15 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-15 UTC."],[],[]]