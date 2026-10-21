* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The CREATE MODEL statement for matrix factorization models

**Note:** Matrix factorization models are only available to
customers with reservations. For more information, see [Pricing](#pricing).

This document describes the `CREATE MODEL` statement for creating
[matrix factorization](https://en.wikipedia.org/wiki/Matrix_factorization_(recommender_systems))
models in BigQuery by using SQL. Alternatively, you can use the
Google Cloud console user interface to
[create a model by using a UI](/bigquery/docs/create-machine-learning-model-console)
([Preview](https://cloud.google.com/products#product-launch-stages)) instead of constructing the SQL
statement yourself.

Matrix factorization models use
[collaborative filtering](https://developers.google.com/machine-learning/recommendation/collaborative/basics)
to identify similar items. Use matrix factorization models with the
[`ML.RECOMMEND` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-recommend)
to generate [recommendations](/bigquery/docs/recommendation-overview).

For more information about supported SQL statements and functions for this
model, see
[End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).

## `CREATE MODEL` syntax

```
{CREATE MODEL | CREATE MODEL IF NOT EXISTS | CREATE OR REPLACE MODEL} model_name
OPTIONS(model_option_list)
AS query_statement

model_option_list:
MODEL_TYPE = 'MATRIX_FACTORIZATION'
    [, FEEDBACK_TYPE = {'EXPLICIT' | 'IMPLICIT'} ]
    [, NUM_FACTORS = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, USER_COL = string_value ]
    [, ITEM_COL = string_value ]
    [, RATING_COL = string_value ]
    [, WALS_ALPHA = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, L2_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, MAX_ITERATIONS = int64_value ]
    [, EARLY_STOP = { TRUE | FALSE } ]
    [, MIN_REL_PROGRESS = float64_value ]
    [, DATA_SPLIT_METHOD = { 'AUTO_SPLIT' | 'RANDOM' | 'CUSTOM' | 'SEQ' | 'NO_SPLIT' } ]
    [, DATA_SPLIT_EVAL_FRACTION = float64_value ]
    [, DATA_SPLIT_TEST_FRACTION = float64_value ]
    [, DATA_SPLIT_COL = string_value ]
    [, NUM_TRIALS = int64_value ]
    [, MAX_PARALLEL_TRIALS = int64_value ]
    [, HPARAM_TUNING_ALGORITHM = { 'VIZIER_DEFAULT' | 'RANDOM_SEARCH' | 'GRID_SEARCH' } ]
    [, HPARAM_TUNING_OBJECTIVES = { 'MEAN_SQUARED_ERROR' | 'MEAN_AVERAGE_PRECISION' | ... } ]
    [, MODEL_REGISTRY = { 'VERTEX_AI' } ]
    [, VERTEX_AI_MODEL_ID = string_value ]
    [, VERTEX_AI_MODEL_VERSION_ALIASES = string_array ]
    [, KMS_KEY_NAME = string_value ]
```

### `CREATE MODEL`

Creates and trains a new model in the specified dataset. If the model name
exists, `CREATE MODEL` returns an error.

### `CREATE MODEL IF NOT EXISTS`

Creates and trains a new model only if the model doesn't exist in the
specified dataset.

### `CREATE OR REPLACE MODEL`

Creates and trains a model and replaces an existing model with the same name in
the specified dataset.

### `model_name`

The name of the model you're creating or replacing. The model
name must be unique in the dataset: no other model or table can have the same
name. The model name must follow the same naming rules as a
BigQuery table. A model name can:

* Contain up to 1,024 characters
* Contain letters (upper or lower case), numbers, and underscores

`model_name` is case-sensitive.

If you don't have a default project configured, then you must prepend the
project ID to the model name in the following format, including backticks:

`[PROJECT\_ID].[DATASET].[MODEL]`

For example, `myproject.mydataset.mymodel`.

### `MODEL_TYPE`

**Syntax**

```
MODEL_TYPE = 'MATRIX_FACTORIZATION'
```

**Description**

Specifies the model type. To create a matrix factorization model, specify `MATRIX_FACTORIZATION`.

### `FEEDBACK_TYPE`

**Syntax**

```
FEEDBACK_TYPE = { 'EXPLICIT' | 'IMPLICIT' }
```

**Description**

Specifies the feedback type for the model. The feedback type determines the
algorithm that is used during training.

**Arguments**

There are two types of ratings (user feedback): `EXPLICIT` and `IMPLICIT`.
Use the one that best fits your use case.

* If the user has explicitly provided a rating, for example 1-5, to an item
  such as movie recommendations, then specify `EXPLICIT`. This trains the
  model using the
  [Alternating Least Squares](https://en.wikipedia.org/wiki/Matrix_completion#Alternating_least_squares_minimization)
  algorithm. This is the default value.
* If you don't have explicit user feedback, the rating value must be
  artificially constructed based on the user's interaction with the item,
  for example, by looking at their clicks, pageviews, and purchases.
  In this situation, specify `IMPLICIT`. This trains the model using the
  [Weighted-Alternating Least Squares](http://yifanhu.net/PUB/cf.pdf) algorithm.

For more information about the differences between the two feedback types and
when to use which type, see
[Feedback types](#feedback-info).

### `NUM_FACTORS`

**Syntax**

`NUM_FACTORS = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

Specifies the number of latent factors to use.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify an `INT64`
value between `2` and `200`. The default value is
`log2(n)`, where `n` is the number of training examples.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `INT64` values that define
  the range of the hyperparameter. For example,
  `NUM_FACTORS = HPARAM_RANGE(5, 20)`.
* The `HPARAM_CANDIDATES` keyword and an array of `INT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `NUM_FACTORS = HPARAM_CANDIDATES([5, 10, 20, 40])`.

When running hyperparameter tuning, the valid range is `[2, 200]`,the
default range is `[2, 20]`, and the scale type is `LINEAR`.

### `USER_COL`

**Syntax**

`USER_COL = string_value`

**Description**

The user column name.

**Arguments**

A `STRING` value. The default value is `user`.

### `ITEM_COL`

**Syntax**

`ITEM_COL = string_value`

**Description**

The item column name.

**Arguments**

A `STRING` value. The default value is `item`.

### `RATING_COL`

**Syntax**

`RATING_COL = string_value`

**Description**

The rating column name.

**Arguments**

A `STRING` value. The default value is `rating`.

#### `WALS_ALPHA`

**Syntax**

`WALS_ALPHA = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

Adjusts the user feedback's impact on recommendation confidence, balancing
positive and negative input in the loss function.

You can only use this hyperparameter with `IMPLICIT` matrix factorization models.

For more information, see
[Feedback types](#feedback-info).

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a `FLOAT64`
value. The default value is `40.0`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range of the hyperparameter. For example,
  `WALS_ALPHA = HPARAM_RANGE(0, 5.0)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `WALS_ALPHA = HPARAM_CANDIDATES([0, 1.0, 3.0, 5.0])`.

When running hyperparameter tuning, the valid range is `(0, ∞]`,
the default range is `[0, 100.0]`, and the scale type is `LINEAR`.

### `L2_REG`

**Syntax**

`L2_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The amount of
[L2 regularization](https://developers.google.com/machine-learning/glossary/#L2_regularization)
applied.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a
`FLOAT64` value. The default value is `1.0`.

If you are running hyperparameter tuning, then you can use one of the
following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range to use for the hyperparameter. For example,
  `L2_REG = HPARAM_RANGE(1.5, 5.0)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `L2_REG = HPARAM_CANDIDATES([0, 1.0, 3.0, 5.0])`.

When running hyperparameter tuning, the valid range is `(0, ∞)`, the
default range is `(0, 10.0]`, and the scale type is `LOG`.

### `MAX_ITERATIONS`

**Syntax**

`MAX_ITERATIONS = int64_value`

**Description**

The maximum number of training iterations, where one iteration represents
a single pass of the entire training data.

**Arguments**

An `INT64` value. The default value is `20`.

### `EARLY_STOP`

**Syntax**

```
EARLY_STOP = { TRUE | FALSE }
```

**Description**

Determines whether training should stop after the first iteration in which the
relative loss improvement is less than the value specified for
[`MIN_REL_PROGRESS`](#min_rel_progress).

**Arguments**

A `BOOL` value. The default value is `TRUE`.

### `MIN_REL_PROGRESS`

**Syntax**

`MIN_REL_PROGRESS = float64_value`

**Description**

The minimum relative loss improvement that is necessary to continue training
when [`EARLY_STOP`](#early_stop) is set to `TRUE`. For example, a value of
`0.01` specifies that each iteration must reduce the loss by 1% for training
to continue.

**Arguments**

A `FLOAT64` value. The default value is `0.01`.

### `DATA_SPLIT_METHOD`

**Syntax**

```
DATA_SPLIT_METHOD = { 'AUTO_SPLIT' | 'RANDOM' | 'CUSTOM' | 'SEQ' | 'NO_SPLIT' }
```

**Description**

The method used to split input data into training, evaluation, and, if you are
running hyperparameter tuning, test data sets. Training data is used to train
the model. Evaluation data is used to avoid
[overfitting](https://developers.google.com/machine-learning/glossary/#overfitting)
by using early stopping. Test data is used to test the hyperparameter tuning
trial and record its metrics in the model.

The percentage sizes of the data sets produced by the various arguments for
this option are approximate. Larger input data sets come closer to the
percentages described than smaller input data sets do.

You can see the model's data split information in the following ways:

* The data split method and percentage are shown in the **Training Options**
  section of the model's **Details** page on the BigQuery
  page of the Google Cloud console.
* Links to temporary tables that contain the split data are available in the
  **Model Details** section of the model's **Details** page on the
  BigQuery of the Google Cloud console. You can also return
  this information from the
  [`DataSplitResult` field](/bigquery/docs/reference/rest/v2/models#datasplitresult)
  in the BigQuery API. These tables are saved for 48 hours. If you
  need this information for more than 48 hours, then you should export
  this data or copy it to permanent tables.

**Arguments**

This option accepts the following values:

* `AUTO_SPLIT`: This option splits the data as follows:

  + If there are fewer than 500 rows in the input data, then all rows are used
    as training data.
  + If you aren't running hyperparameter tuning, then data is randomized and
    split as follows:

    - If there are between 500 and 50,000 rows in the input data, then 20% of
      the data is used as evaluation data and 80% is used as training data.
    - If there are more than 50,000 rows, then 10,000 rows are used as
      evaluation data and the remaining rows are used as training data.
  + If you are running hyperparameter tuning and there are more than 500 rows in
    the input data, then the data is randomized and split as follows:

    - 10% of the data is used as evaluation data
    - 10% is used as test data
    - 80% is used as training data

    For more information, see
    [Data split](/bigquery/docs/hp-tuning-overview#data_split).
* `RANDOM`: Data is randomized before being split into sets. You can use this
  option with the [`DATA_SPLIT_EVAL_FRACTION`](#data_split_eval_fraction) and
  [`DATA_SPLIT_TEST_FRACTION`](#data_split_test_fraction)
  options to customize the data split. If you don't specify either of those
  options, data is split in the same way as for the `AUTO_SPLIT` option.

  A random split is deterministic: different training runs produce the same
  split results if the same underlying training data is used.

  **Note:** A random split is based on the
  [FARM\_FINGERPRINT](/bigquery/docs/reference/standard-sql/hash_functions#farm_fingerprint)
  of the data (including the column name and schema), so
  tables with the same content but different column names and schemas may get
  different splitting and different evaluation metrics.
* `CUSTOM`: Split data using the value in a specified column:

  + If you aren't running hyperparameter tuning, then you must provide the
    name of a column of type `BOOL`. Rows with a value of `TRUE` or `NULL` are
    used as evaluation data, rows with a value of `FALSE` are used as
    training data.
  + If you are running hyperparameter tuning, then you must provide the name
    of a column of type `STRING`. Rows with a value of `TRAIN` are used as
    training data, rows with a value of `EVAL` are used as evaluation data,
    and rows with a value of `TEST` are used as test data.

  Use the [`DATA_SPLIT_COL` option](#data_split_col) to identify the column
  that contains the data split information.
* `SEQ`: Split data sequentially by using the value in a specified column of one
  of the following types:

  + `NUMERIC`
  + `BIGNUMERIC`
  + `STRING`
  + `TIMESTAMP`

  The data is sorted smallest to largest based on the specified column.

  When you aren't running hyperparameter tuning, the last n rows
  are used as evaluation data, where n is the value specified for
  `DATA_SPLIT_EVAL_FRACTION`. The remaining rows are used as training data.

  When you are running hyperparameter tuning, the last m rows
  are used as test data, where m is the value specified for
  `DATA_SPLIT_TEST_FRACTION`. The second last n rows are used as
  evaluation data, where n is the value specified for
  `DATA_SPLIT_EVAL_FRACTION`. The remaining rows are used as training data.

  All rows with split values smaller than the threshold, including `NULL`s,
  are used as training data. The remaining rows are used as evaluation data.

  Use the `DATA_SPLIT_COL` option to identify the column that contains the
  data split information.
* `NO_SPLIT`: This is the default. No data split; all input data is used as
  training data.

  While the other methods are supported, use them with caution. Due to the
  nature of the matrix factorization algorithm, if a split eliminates all
  of the ratings for a user or item, a factor weight vector is not
  generated for the user or item.

  However, use this option with caution when tuning the `NUM_FACTORS`
  hyperparameter. Although `NO_SPLIT` allows better performance when using
  larger values for `NUM_FACTORS`, the validity of the results might be
  degraded.

### `DATA_SPLIT_EVAL_FRACTION`

**Syntax**

`DATA_SPLIT_EVAL_FRACTION = float64_value`

**Description**

The fraction of the data to use as evaluation data. Use when you are
specifying `RANDOM` or `SEQ` as the value for the
[`DATA_SPLIT_METHOD` option](#data_split_method).

If you are running hyperparameter tuning and you specify a value for this
option, you must also specify a value for
[`DATA_SPLIT_TEST_FRACTION`](#data_split_test_fraction). In this
case, the training dataset is
`1 - eval_fraction - test_fraction`. For
example, if you specify `20.00` for `DATA_SPLIT_EVAL_FRACTION` and `8.0` for
`DATA_SPLIT_TEST_FRACTION`, your training dataset is 72% of the input data.

**Arguments**

A `FLOAT64` value. The default is `0.2`. The service maintains the accuracy of
the input value to two decimal places.

### `DATA_SPLIT_TEST_FRACTION`

**Syntax**

`DATA_SPLIT_TEST_FRACTION = float64_value`

**Description**

The fraction of the data to use as test data. Use this option when you are
running hyperparameter tuning and specifying either `RANDOM` or `SEQ` as
value for the [`DATA_SPLIT_METHOD` option](#data_split_method).

If you specify a value for this option, you must also specify a value for
[`DATA_SPLIT_EVAL_FRACTION`](#data_split_eval_fraction). In this case,
the training dataset is
`1 - eval_fraction - test_fraction`.
For example, if you specify `20.00` for `DATA_SPLIT_EVAL_FRACTION` and `8.0` for
`DATA_SPLIT_TEST_FRACTION`, your training dataset is 72% of the input data.

**Arguments**

A `FLOAT64` value. The default is `0`. The service maintains the accuracy of
the input value to two decimal places.

### `DATA_SPLIT_COL`

**Syntax**

`DATA_SPLIT_COL = string_value`

**Description**

The name of the column to use to sort input data into the training,
evaluation, or test set. Use when you are specifying `CUSTOM` or `SEQ` as the
value for the [`DATA_SPLIT_METHOD` option](#data_split_method):

* If you aren't running hyperparameter tuning and you are specifying `SEQ` as
  the value for `DATA_SPLIT_METHOD`, then the data is first sorted smallest to
  largest based on the specified column. The last n rows are used
  as evaluation data, where n is the value specified for
  [`DATA_SPLIT_EVAL_FRACTION`](#data_split_eval_fraction). The remaining rows
  are used as training data.
* If you aren't running hyperparameter tuning and you are specifying `CUSTOM`
  as the value for `DATA_SPLIT_METHOD`, then you must provide the name
  of a column of type `BOOL`. Rows with a value of `TRUE` or `NULL` are used as
  evaluation data, rows with a value of `FALSE` are used as training
  data.
* If you are running hyperparameter tuning and you are specifying `SEQ` as the
  value for `DATA_SPLIT_METHOD`, then the data is first sorted smallest to
  largest based on the specified column. The last m rows are used
  as test data, where m is the value specified for
  [`DATA_SPLIT_TEST_FRACTION`](#data_split_test_fraction). The second last
  n rows are used as evaluation data, where n is the value
  specified for [`DATA_SPLIT_EVAL_FRACTION`](#data_split_eval_fraction).
  The remaining rows are used as training data.
* If you are running hyperparameter tuning and you are specifying `CUSTOM` as
  the value for `DATA_SPLIT_METHOD`, then you must provide the name of a column
  of type `STRING`. Rows with a value of `TRAIN` are used as training data, rows
  with a value of `EVAL` are used as evaluation data, and rows with a value of
  `TEST` are used as test data.

The column you specify for `DATA_SPLIT_COL` can't be used as a feature or
label, and is excluded from features automatically.

**Arguments**

A `STRING` value.

### `NUM_TRIALS`

**Syntax**

`NUM_TRIALS = int64_value`

**Description**

The maximum number of submodels to train. The tuning stops when `NUM_TRIALS`
submodels are trained, or when the hyperparameter search space is exhausted.
You must specify this option in order to use hyperparameter tuning.
For matrix factorization models, increasing `NUM_TRIALS` is the
recommended way to reduce model output variance.

**Arguments**

An `INT64` value between `1` and `100`, inclusive.

**Note:** We recommend using at least
`(number_of_hyperparameters * 10)` trials to tune a model.

### `MAX_PARALLEL_TRIALS`

**Syntax**

`MAX_PARALLEL_TRIALS = int64_value`

**Description**

The maximum number of trials to run at the same time. If you specify a value
for this option, you must also specify a value for
[`NUM_TRIALS`](#num_trials).

**Arguments**

An `INT64` value between `1` and `5`, inclusive. The default value is `1`.

**Note:** Although specifying larger `MAX_PARALLEL_TRIALS` values can accelerate the
hyperparameter tuning process, acceleration can undermine the final model
quality when you specify `VIZIER_DEFAULT` as the
[`HPARAM_TUNING_ALGORITHM`](#hparam_tuning_algorithm)
value. This is because the parallel trials can't benefit from concurrent
training results.

### `HPARAM_TUNING_ALGORITHM`

**Syntax**

```
HPARAM_TUNING_ALGORITHM = { 'VIZIER_DEFAULT' | 'RANDOM_SEARCH
```