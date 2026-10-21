* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The CREATE MODEL statement for Wide-and-Deep models

This document describes the `CREATE MODEL` statement for creating
[wide-and-deep](https://dl.acm.org/doi/10.1145/2988450.2988454)
models in BigQuery by using SQL. Alternatively, you can use the
Google Cloud console user interface to
[create a model by using a UI](/bigquery/docs/create-machine-learning-model-console)
([Preview](https://cloud.google.com/products#product-launch-stages)) instead of constructing the SQL
statement yourself.

You can use wide-and-deep regressor models with the
[`ML.PREDICT` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict)
to perform [regression](/bigquery/docs/regression-overview), and you can use
wide-and-deep classifier models with the `ML.PREDICT` function to
perform [classification](/bigquery/docs/classification-overview). You can use
both types of wide-and-deep models with the
`ML.PREDICT` function
to perform [anomaly detection](/bigquery/docs/anomaly-detection-overview).

For more information about supported SQL statements and functions for this
model, see
[End-to-end user journeys for ML models](/bigquery/docs/e2e-journey).

## `CREATE MODEL` syntax

```
{CREATE MODEL | CREATE MODEL IF NOT EXISTS | CREATE OR REPLACE MODEL} model_name
OPTIONS(model_option_list)
AS query_statement

model_option_list:
MODEL_TYPE = { 'DNN_LINEAR_COMBINED_CLASSIFIER' | 'DNN_LINEAR_COMBINED_REGRESSOR' }
    [, LEARN_RATE = float64_value | struct_array ]
    [, OPTIMIZER = string_value | struct_array ]
    [, L1_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, L2_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, ACTIVATION_FN = { { 'RELU' | 'RELU6' | 'CRELU' | 'ELU' | 'SELU' | 'SIGMOID' | 'TANH' } | HPARAM_CANDIDATES([candidates]) } ]
    [, BATCH_SIZE = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, DROPOUT = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, HIDDEN_UNITS = { int_array | HPARAM_CANDIDATES([candidates]) } ]
    [, AUTO_CLASS_WEIGHTS = { TRUE | FALSE } ]
    [, CLASS_WEIGHTS = struct_array ]
    [, EARLY_STOP = { TRUE | FALSE } ]
    [, MIN_REL_PROGRESS = float64_value ]
    [, INPUT_LABEL_COLS = string_array ]
    [, MAX_ITERATIONS = int64_value ]
    [, WARM_START = { TRUE | FALSE } ]
    [, DATA_SPLIT_METHOD = { 'AUTO_SPLIT' | 'RANDOM' | 'CUSTOM' | 'SEQ' | 'NO_SPLIT' } ]
    [, DATA_SPLIT_EVAL_FRACTION = float64_value ]
    [, DATA_SPLIT_TEST_FRACTION = float64_value ]
    [, DATA_SPLIT_COL = string_value ]
    [, NUM_TRIALS = int64_value ]
    [, MAX_PARALLEL_TRIALS = int64_value ]
    [, HPARAM_TUNING_ALGORITHM = { 'VIZIER_DEFAULT' | 'RANDOM_SEARCH' | 'GRID_SEARCH' } ]
    [, HPARAM_TUNING_OBJECTIVES = { 'ROC_AUC' | 'R2_SCORE' | ... } ]
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

```
MODEL_TYPE = { 'DNN_LINEAR_COMBINED_CLASSIFIER' | 'DNN_LINEAR_COMBINED_REGRESSOR' }
```

**Description**

Specifies the model type. This option is required.

### `LEARN_RATE`

**Syntax**

`LEARN_RATE = float64_value | struct_array`

**Description**

The initial learn rate for training.

**Arguments**

To specify an initial learn rate for both the linear and DNN parts of the model,
provide a `FLOAT64` value. For example:

```
LEARN_RATE = 0.01
```

To specify different initial learn rates for the linear and DNN parts of the
model, provide an array of `STRUCT` values that each contain one `STRING` and
one `FLOAT64` value. The string identifies the part of the model, and the float
specifies the initial learn rate to use for that part of the model.
For example:

```
LEARN_RATE = [STRUCT('dnn', 0.001), STRUCT('linear', 0.01)]
```

The default value is `0.001` for both the linear and DNN parts of the model.

### `OPTIMIZER`

**Syntax**

`OPTIMIZER = string_value | struct_array`

**Description**

Specifies the optimizer for training the model.

**Arguments**

To specify an optimizer for both the linear and DNN parts of the model,
provide a `STRING` value. For example:

```
OPTIMIZER = 'ADAGRAD'
```

To specify different optimizers for the linear and DNN parts of the
model, provide an array of `STRUCT` values that each contain two `STRING`
values. The first string identifies the part of the model, and the second string
specifies the optimizer to use for that part of the model. For example:

```
OPTIMIZER = [STRUCT('dnn', 'ADAGRAD'), STRUCT('linear', 'SGD')]
```

Use one of the following values for the optimizer string:

* `ADAGRAD` — [Implements the Adagrad algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/AdagradOptimizer)
* `ADAM` — [Implements the Adam algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/AdamOptimizer)
* `FTRL` — [Implements the FTRL algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/FtrlOptimizer)
* `RMSPROP` — [Implements the RMSProp algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/RMSPropOptimizer)
* `SGD` — [Implements the gradient descent algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/GradientDescentOptimizer)

The default value of `OPTIMIZER` is
`[STRUCT('dnn', 'ADAM'), STRUCT('linear', 'FTRL')]`.

### `L1_REG`

**Syntax**

`L1_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The L1 regularization strength of the `OPTIMIZER`. You can only use
this option when `OPTIMIZER` is set to one of the following values:

* `ADAGRAD` — [Implements the ProximalAdagradOptimizer algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/ProximalAdagradOptimizer)
* `FTRL` — [Implements the FtrlOptimizer algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/FtrlOptimizer)
* `SGD` — [Implements the ProximalGradientDescentOptimizer algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/ProximalGradientDescentOptimizer)

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

The L2 regularization strength of the `OPTIMIZER`. You can only
use this option when `OPTIMIZER` is set to one of the following values:

* `ADAGRAD` — [Implements the ProximalAdagradOptimizer algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/ProximalAdagradOptimizer)
* `FTRL` — [Implements the FtrlOptimizer algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/FtrlOptimizer)
* `SGD` — [Implements the ProximalGradientDescentOptimizer algorithm](https://www.tensorflow.org/api_docs/python/tf/compat/v1/train/ProximalGradientDescentOptimizer)

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

### `ACTIVATION_FN`

**Syntax**

`ACTIVATION_FN = { { 'RELU' | 'RELU6' | 'CRELU' | 'ELU' | 'SELU' | 'SIGMOID' | 'TANH' } | HPARAM_CANDIDATES([candidates]) }`

**Description**

The activation function of the neural network.

**Arguments**

This option accepts the following values:

* `RELU` — [Rectified linear](https://www.tensorflow.org/api_docs/python/tf/nn/relu). This is the default.
* `RELU6` — [Rectified linear 6](https://www.tensorflow.org/api_docs/python/tf/nn/relu6)
* `CRELU` — [Concatenated ReLU](https://www.tensorflow.org/api_docs/python/tf/nn/crelu)
* `ELU` — [Exponential linear](https://www.tensorflow.org/api_docs/python/tf/nn/elu)
* `SELU` — [Scaled exponential linear](https://www.tensorflow.org/api_docs/python/tf/nn/selu)
* `SIGMOID` — [Sigmoid activation](https://www.tensorflow.org/api_docs/python/tf/math/sigmoid)
* `TANH` — [Tanh activation](https://www.tensorflow.org/api_docs/python/tf/math/tanh)

If you are running hyperparameter training, then you can provide more than one
value for this option by using `HPARAM_CANDIDATES` and specifying an array.
For example, `ACTIVATION_FN = HPARAM_CANDIDATES(['RELU', 'RELU6', 'TANH'])`.

### `BATCH_SIZE`

**Syntax**

`BATCH_SIZE = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The mini batch size of samples that are fed to the neural network.

**Arguments**

If you aren't running hyperparameter tuning, specify an `INT64` value that
is positive and is less than or equal to `8192`. The default value is `32`
or the number of samples, whichever is smaller.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range to use for the hyperparameter. For example,
  `BATCH_SIZE = HPARAM_RANGE(16, 64)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `BATCH_SIZE = HPARAM_CANDIDATES([32, 64, 256, 1024])`.

When running hyperparameter tuning, the valid range is `(0, ∞)`,
the default range is `[16, 1024]`, and the scale type is `LOG`.

### `DROPOUT`

**Syntax**

`DROPOUT = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The dropout rate of units in the neural network.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a `FLOAT64`
value that is positive and is less than or equal to `1.0`. The default value is
`0`.

If you are running hyperparameter tuning, then you must use one of the
following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range to use for the hyperparameter. For example,
  `DROPOUT = HPARAM_RANGE(0, 0.6)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `DROPOUT = HPARAM_CANDIDATES([0.1, 0.3, 0.6])`.

When running hyperparameter tuning, the valid range is `[0, 1.0)`, the
default range is `[0, 0.8]`, and the scale type is `LINEAR`.

### `HIDDEN_UNITS`

**Syntax**

`HIDDEN_UNITS = { int_array | HPARAM_CANDIDATES([candidates]) }`

**Description**

The hidden layers of the neural network.

**Arguments**

An array of integers that represents the architecture of the hidden layers. If
not specified, BigQuery ML applies a single hidden layer that
contains no more than 128 units. The number of units is calculated as `[min(128,
num_samples / (10 * (num_input_units + num_output_units)))]`. The upper bound of
the rule ensures that the model isn't overfitting.

The number in the middle of the array defines the shape of the latent space. For
example, `hidden_units=[128, 64, 4, 64, 128]` defines a four-dimensional latent
space.

The number of layers in `hidden_units` must be odd, and we recommend that the
sequence be symmetrical.

The following example defines a model architecture that uses three hidden layers
with 256, 128, and 64 nodes, respectively.

```
HIDDEN_UNITS = [256, 128, 64]
```

If you are running hyperparameter tuning, then you must use the
`HPARAM_CANDIDATES` keyword and specify an array in the form
`ARRAY<STRUCT<ARRAY<INT64>>>` to provide discrete values to use for the
hyperparameter. Each struct value in the outer array represents a candidate
neural architecture. The array of `INT64` values in each struct represents a
hidden layer.

The following example represents a neural architecture search with three
candidates, which include a single layer of 8 neurons, two layers of neurons
with 8 and 16 in sequence, and three layers of neurons with 16, 32 and 64 in
sequence, respectively.

```
hidden_units=hparam_candidates([struct([8]), struct([8, 16]), struct([16, 32, 64])])
```

The valid range for the `INT64` arrays is `[1, ∞)`.

### `AUTO_CLASS_WEIGHTS`

**Syntax**

```
AUTO_CLASS_WEIGHTS = { TRUE | FALSE }
```

**Description**

Determines whether to balance class labels by using weights for each class in
inverse proportion to the frequency of that class.

Only use this option with classifier models.

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