* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The CREATE MODEL statement for generalized linear models

This document describes the `CREATE MODEL` statement for creating
[linear regression](https://developers.google.com/machine-learning/crash-course/linear-regression)
or
[logistic regression](https://developers.google.com/machine-learning/crash-course/logistic-regression)
models in BigQuery by using SQL. Alternatively, you can use the
Google Cloud console user interface to
[create a model by using a UI](/bigquery/docs/create-machine-learning-model-console)
([Preview](https://cloud.google.com/products#product-launch-stages)) instead of constructing the SQL
statement yourself.

You can use linear regression models with the
[`ML.PREDICT` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict)
to perform [regression](/bigquery/docs/regression-overview), and you can use
logistic regression models with the `ML.PREDICT` function to
perform [classification](/bigquery/docs/classification-overview). You can use
both linear and logistic regression models with the
`ML.PREDICT` function to perform
[anomaly detection](/bigquery/docs/anomaly-detection-overview).

For more information about supported SQL statements and functions for this
model, see
[End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).

## `CREATE MODEL` syntax

```
{CREATE MODEL | CREATE MODEL IF NOT EXISTS | CREATE OR REPLACE MODEL} model_name
OPTIONS(model_option_list)
AS query_statement

model_option_list:
MODEL_TYPE = { 'LINEAR_REG' | 'LOGISTIC_REG' }
    [, OPTIMIZE_STRATEGY = { 'AUTO_STRATEGY' | 'BATCH_GRADIENT_DESCENT' | 'NORMAL_EQUATION' } ]
    [, LEARN_RATE_STRATEGY = { 'LINE_SEARCH' | 'CONSTANT' } ]
    [, LEARN_RATE = float64_value ]
    [, LS_INIT_LEARN_RATE = float64_value ]
    [, CALCULATE_P_VALUES = { TRUE | FALSE } ]
    [, FIT_INTERCEPT = { TRUE | FALSE } ]
    [, CATEGORY_ENCODING_METHOD = { 'ONE_HOT_ENCODING` | 'DUMMY_ENCODING' } ]
    [, AUTO_CLASS_WEIGHTS = { TRUE | FALSE } ]
    [, CLASS_WEIGHTS = struct_array ]
    [, ENABLE_GLOBAL_EXPLAIN = { TRUE | FALSE } ]
    [, INPUT_LABEL_COLS = string_array ]
    [, L1_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, L2_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, MAX_ITERATIONS = int64_value ]
    [, WARM_START = { TRUE | FALSE } ]
    [, EARLY_STOP = { TRUE | FALSE } ]
    [, MIN_REL_PROGRESS = float64_value ]
    [, DATA_SPLIT_METHOD = { 'AUTO_SPLIT' | 'RANDOM' | 'CUSTOM' | 'SEQ' | 'NO_SPLIT' } ]
    [, DATA_SPLIT_EVAL_FRACTION = float64_value ]
    [, DATA_SPLIT_TEST_FRACTION = float64_value ]
    [, DATA_SPLIT_COL = string_value ]
    [, NUM_TRIALS = int64_value ]
    [, MAX_PARALLEL_TRIALS = int64_value ]
    [, HPARAM_TUNING_ALGORITHM = { 'VIZIER_DEFAULT' | 'RANDOM_SEARCH' | 'GRID_SEARCH' } ]
    [, HPARAM_TUNING_OBJECTIVES = { 'R2_SCORE' | 'ROC_AUC' | ... } ]
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
MODEL_TYPE = { 'LINEAR_REG' | 'LOGISTIC_REG'}
```

**Description**

Specify the model type. This option is required.

**Arguments**

This option accepts the following values:

* `LINEAR_REG`: The model performs linear regression for forecasting; for
  example, the sales of an item on a given day. Labels are real-valued. They
  can't be +/- infinity or `NaN`.
* `LOGISTIC_REG`: The model performs logistic regression for classification;
  for example, determining whether a customer will make a purchase.

  Logistic models can be one of two types:

  + Binary logistic regression for classification; for example, determining
    whether a customer will make a purchase. Labels must only have two possible
    values, one for the [positive class](https://developers.google.com/machine-learning/glossary/?&_ga=2.199267948.315885954.1628494155-266466322.1625885991#positive-class) and another
    for the
    [negative class](https://developers.google.com/machine-learning/glossary/?&_ga=2.199267948.315885954.1628494155-266466322.1625885991#negative-class).
    BigQuery ML treats the higher label value as the positive
    class, and lower label value as the negative class. This holds for both
    numeric and string label values.
  + Multiclass logistic regression for classification; for example,
    predicting multiple possible values such as whether an input is
    `low-value`, `medium-value`, or `high-value`. Labels can have up to 50
    unique values. In BigQuery ML, multiclass logistic
    regression training uses a
    [multinomial classifier](https://en.wikipedia.org/wiki/Multinomial_logistic_regression)
    with a
    [cross entropy loss function](https://developers.google.com/machine-learning/glossary/#cross-entropy).

### `OPTIMIZE_STRATEGY`

**Syntax**

```
OPTIMIZE_STRATEGY = { 'AUTO_STRATEGY' | 'BATCH_GRADIENT_DESCENT' | 'NORMAL_EQUATION' }
```

**Description**

The strategy to train linear regression models.

**Arguments**

This option accepts the following values:

* `AUTO_STRATEGY`: This is the default. Determines the training strategy
  as follows:

  + If you specified a value for `L1_REG` or set `WARM_START` to `TRUE`,
    the `BATCH_GRADIENT_DESCENT` strategy is used.
  + If the total cardinality of training features is more than 10,000,
    the `BATCH_GRADIENT_DESCENT` strategy is used.
  + If there is an over-fitting issue, where the number of training examples
    is less than 10*x* and *x* is the total cardinality, the
    `BATCH_GRADIENT_DESCENT` strategy is used.
  + The `NORMAL_EQUATION` strategy is used for all other cases.
* `BATCH_GRADIENT_DESCENT`: Train the model using the
  [batch gradient descent](https://en.wikipedia.org/wiki/Gradient_descent)
  method, which optimizes the loss function using the gradient function.
* `NORMAL_EQUATION`: Directly compute the
  [least square solution](http://mathworld.wolfram.com/NormalEquation.html)
  of the linear regression problem with the analytical formula. You can't use
  `NORMAL_EQUATION` in the following cases:

  + You specified a value for `L1_REG`.
  + You set `WARM_START` to `TRUE`.
  + The total cardinality of training features is greater than 10,000.

### `LEARN_RATE_STRATEGY`

**Syntax**

```
LEARN_RATE_STRATEGY = { 'LINE_SEARCH' | 'CONSTANT' }
```

**Description**

The strategy for specifying the
[learning rate](https://developers.google.com/machine-learning/glossary/#learning_rate) during training.

**Arguments**

This option accepts the following values:

* `LINE_SEARCH`: This is the default. Use the
  [line search](https://en.wikipedia.org/wiki/Line_search) method to calculate
  the learning rate. You specify the line search initial learn rate in
  [`LS_INIT_LEARN_RATE`](#ls_init_learn_rate).

  Line search slows down training and increases the number of bytes
  processed, but it generally converges even with a larger initial specified
  learning rate.
* `CONSTANT`: Set the learning rate to the value you specify in
  [`LEARN_RATE`](#learn_rate).

### `LEARN_RATE`

**Syntax**

`LEARN_RATE = float64_value`

**Description**

The learn rate for
[gradient descent](https://developers.google.com/machine-learning/glossary/#gradient_descent)
when [`LEARN_RATE_STRATEGY`](#learn_rate_strategy) is set to `CONSTANT`. If
`LEARN_RATE_STRATEGY` is set to `LINE_SEARCH`, an error is returned.

**Arguments**

A `FLOAT64` value. The default value is `0.1`.

### `LS_INIT_LEARN_RATE`

**Syntax**

`LS_INIT_LEARN_RATE = float64_value`

**Description**

Sets the initial learning rate when you specify `LINE_SEARCH` for
[`LEARN_RATE_STRATEGY`](#learn_rate_strategy).

If the model learning rate appears to be doubling every
iteration as indicated by the
[`ML.TRAINING_INFO` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-train),
then try setting `LS_INIT_LEARN_RATE` to the last doubled learning rate. The
optimal initial learning rate is different for every model. A good initial
learning rate for one model might not be a good initial learning rate for
another.

**Arguments**

A `FLOAT64` value. The default value is `0.1`.

### `CALCULATE_P_VALUES`

**Syntax**

`CALCULATE_P_VALUES = { TRUE | FALSE }`

**Description**

Determines whether to compute p-values and standard errors during training.

P-values and standard errors are computed when you create the model.
This option must be `TRUE` if you want to use the
[`ML.ADVANCED_WEIGHTS` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-advanced-weights)
to retrieve the p-values and standard errors after the model finishes training.
For more information on the usage requirements for `ML.ADVANCED_WEIGHTS`,
see [Usage requirements](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-advanced-weights#usage_requirements).

**Arguments**

A `BOOL` value. The default value is `FALSE`.

### `FIT_INTERCEPT`

**Syntax**

```
FIT_INTERCEPT = { TRUE | FALSE }
```

**Description**

Determines whether to fit an intercept to the model during training.

**Arguments**

A `BOOL` value. The default value is `TRUE`.

### `CATEGORY_ENCODING_METHOD`

**Syntax**

```
CATEGORY_ENCODING_METHOD = { 'ONE_HOT_ENCODING' | 'DUMMY_ENCODING' }
```

**Description**

Specifies which encoding method to use on non-numeric features. For more
information about supported encoding methods, see
[Automatic feature preprocessing](/bigquery/docs/auto-preprocessing).

**Arguments**

This option accepts the following values:

* `ONE_HOT_ENCODING`. This is the default.
* `DUMMY_ENCODING`

### `AUTO_CLASS_WEIGHTS`

**Syntax**

```
AUTO_CLASS_WEIGHTS = { TRUE | FALSE }
```

**Description**

Determines whether to balance class labels by using weights for each class in
inverse proportion to the frequency of that class.

Only use this option with logistic regression models.

By default, the training data used to create the model
is unweighted. If the labels in the training data are imbalanced, the model
might learn to predict the most popular class of labels more heavily, which
you might not want.

To balance every class, set this option to `TRUE`. Balance is
accomplished using the following formula:

```
total_input_rows / (input_rows_for_class_n * number_of_unique_classes)
```

**Arguments**

A `BOOL` value. The default value is `FALSE`.

### `CLASS_WEIGHTS`

**Syntax**

`CLASS_WEIGHTS = struct_array`

**Description**

The weights to use for each class label. You can't specify this option if
[`AUTO_CLASS_WEIGHTS`](#auto_class_weights) is `TRUE`.

**Arguments**

An `ARRAY` of `STRUCT` values. Each `STRUCT` contains a
`STRING` value that specifies the class label and a `FLOAT64` value that
specifies the weight for that class label. A weight must be present for every
class label. The weights are not required to add up to 1.

A `CLASS_WEIGHTS` value might look like the following example:

```
CLASS_WEIGHTS = [STRUCT('example_label', .2)]
```

### `ENABLE_GLOBAL_EXPLAIN`

**Syntax**

```
ENABLE_GLOBAL_EXPLAIN = { TRUE | FALSE }
```

**Description**

Determines whether to compute global explanations by using
[explainable AI](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-xai-overview)
to evaluate the importance of global features to the model.

Global explanations are computed when you create the model. This option
must be `TRUE` if you want to use the
[`ML.GLOBAL_EXPLAIN` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-global-explain)
to retrieve the global explanations after the model is created.

**Arguments**

A `BOOL` value. The default value is `FALSE`.

### `INPUT_LABEL_COLS`

**Syntax**

`INPUT_LABEL_COLS = string_array`

**Description**

The name of the label column in the training data. The label column contains the
expected machine learning result for the given record. For example, in a spam
detection dataset, the label column value would probably be either `spam` or
`not spam`. In a rainfall dataset, the label column value might be the amount
of rain that fell during a certain period.

**Arguments**

A one-element `ARRAY` of string values. Defaults to `label`.

### `L1_REG`

**Syntax**

`L1_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The amount of
[L1 regularization](https://developers.google.com/machine-learning/glossary/#L1_regularization)
applied.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a
`FLOAT64` value. The default value is `0`.

If you are running hyperparameter tuning, then you can use one of the
following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range to use for the hyperparameter. For example,
  `L1_REG = HPARAM_RANGE(0, 5.0)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `L1_REG = HPARAM_CANDIDATES([0, 1.0, 3.0, 5.0])`.

When running hyperparameter tuning, the valid range is
`(0, ∞)`, the default range is `(0, 10.0]`, and the scale
type is `LOG`.

### `L2_REG`

**Syntax**

`L2_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The amount of
[L2 regularization](https://developers.google.com/machine-learning/glossary/#L2_regularization)
applied.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a
`FLOAT64` value. The default value is `0`.

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

### `WARM_START`

**Syntax**

```
WARM_START = { TRUE | FALSE }
```

**Description**

Determines whether to train a model with new training data, new model options,
or both. Unless you explicitly override them, the initial options used to train
the model are used for the warm start run.

In a warm start run, the iteration numbers are reset to start from zero. Use
the training run or iteration information returned by the
[`ML.TRAINING_INFO` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-train)
to distinguish the warm start run from the original run.

The values of the `MODEL_TYPE` and `LABELS` options and the training data schema
must remain constant in a warm start.

**Arguments**

A `BOOL` value. The default value is `FALSE`.

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