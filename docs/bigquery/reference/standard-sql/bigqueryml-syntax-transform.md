* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.TRANSFORM function

This document describes the `ML.TRANSFORM` function, which you can use
to preprocess feature data. This function processes input data by
applying the data transformations captured in the
[`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform)
of an existing model. The statistics that were calculated for data
transformation during model training are applied to the input data of the function.

For more information about which models support this function, see
[End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).

## Syntax

```
ML.TRANSFORM(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  { TABLE `PROJECT_ID.DATASET.TABLE_NAME` | (QUERY_STATEMENT) }
)
```

### Arguments

`ML.TRANSFORM` takes the following arguments:

* `PROJECT_ID`: the project that contains the
  resource.
* `DATASET`: the BigQuery dataset that
  contains the resource.
* `MODEL_NAME`: the name of a model. The model
  must have been created by using a `CREATE MODEL` statement that includes a
  [`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform)
  to manually preprocess feature data. You can check to see if a model uses a
  `TRANSFORM` clause by using the
  [`bq show` command](/bigquery/docs/reference/bq-cli-reference#bq_show)
  to look at the
  [model's metadata](/bigquery/docs/getting-model-metadata#get_model_metadata).
  If the model was trained using a `TRANSFORM` clause, the model metadata
  contains a section about the transform columns. The function returns an error
  if you specify a model that was trained without a `TRANSFORM` clause.
* `TABLE_NAME`: the name of the input table that
  contains the feature data to preprocess.

  If you specify a value for the `TABLE_NAME` argument, the input column names
  in the table must match the input column names in the model's `TRANSFORM`
  clause, and their types should be compatible according to
  BigQuery [implicit coercion rules](/bigquery/docs/reference/standard-sql/conversion_rules#coercion).
  You can get the input column names and data types from the
  [model's metadata](/bigquery/docs/getting-model-metadata#get_model_metadata),
  in the section about the feature columns.
* `QUERY_STATEMENT`: A query that generates the feature
  data to preprocess. For the supported SQL syntax of the `QUERY_STATEMENT`
  clause, see
  [GoogleSQL query syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).

  If you specify a value for the `QUERY_STATEMENT` argument, the input column
  names from the query must match the input column names in the model's
  `TRANSFORM` clause, and their types should be compatible according to
  BigQuery [implicit coercion rules](/bigquery/docs/reference/standard-sql/conversion_rules#coercion).
  You can get the input column names and data types from the
  [model's metadata](/bigquery/docs/getting-model-metadata#get_model_metadata),
  in the section about the feature columns.

## Output

`ML.TRANSFORM` returns the columns specified in the model's `TRANSFORM` clause.

## Example

The following example returns feature data that has been preprocessed by
using the `TRANSFORM` clause included in the model named `mydataset.mymodel`
in your default project.

Create the model that contains the `TRANSFORM` clause:

```
CREATE OR REPLACE MODEL `mydataset.mymodel`
  TRANSFORM(
    species,
    island,
    ML.MAX_ABS_SCALER(culmen_length_mm) OVER () AS culmen_length_mm,
    ML.MAX_ABS_SCALER(flipper_length_mm) OVER () AS flipper_length_mm,
    sex,
    body_mass_g)
  OPTIONS (
    model_type = 'linear_reg',
    input_label_cols = ['body_mass_g'])
AS (
  SELECT *
  FROM `bigquery-public-data.ml_datasets.penguins`
  WHERE body_mass_g IS NOT NULL
);
```

Return feature data preprocessed by the model's `TRANSFORM` clause:

```
SELECT
  *
FROM
  ML.TRANSFORM(
    MODEL `mydataset.mymodel`,
    TABLE `bigquery-public-data.ml_datasets.penguins`);
```

The result is similar to the following:

```
+-------------------------------------+--------+---------------------+---------------------+--------+-----------------+-------------+
| species                             | island | culmen_length_mm    | flipper_length_mm   | sex    | culmen_depth_mm | body_mass_g |
--------------------------------------+--------+ ------------------- +---------------------+--------+-----------------+-------------+
| Adelie Penguin (Pygoscelis adeliae) | Dream  | 0.61409395973154368 | 0.79653679653679654 | Female | 18.4            | 3475.0      |
| Adelie Penguin (Pygoscelis adeliae) | Dream  | 0.66778523489932884 | 0.79653679653679654 | Male   | 19.1            | 4650.0      |
+-------------------------------------+--------+---------------------+---------------------+--------+-----------------+-------------+
```

## What's next

* For information about feature preprocessing, see
  [Feature preprocessing overview](/bigquery/docs/preprocess-overview).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-05 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-05 UTC."],[],[]]