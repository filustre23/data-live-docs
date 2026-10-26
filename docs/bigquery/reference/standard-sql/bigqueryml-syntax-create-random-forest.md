* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The CREATE MODEL statement for random forest models

This document describes the `CREATE MODEL` statement for creating
[random forest](https://en.wikipedia.org/wiki/Random_forest)
models in BigQuery by using SQL. Alternatively, you can use the
Google Cloud console user interface to
[create a model by using a UI](/bigquery/docs/create-machine-learning-model-console)
([Preview](https://cloud.google.com/products#product-launch-stages)) instead of constructing the SQL
statement yourself. Random forest models are trained using the
[XGBoost library](https://xgboost.readthedocs.io/en/latest/).

You can use random forest regressor models with the
[`ML.PREDICT` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict)
to perform [regression](/bigquery/docs/regression-overview), and you can use
random forest classifier models with the `ML.PREDICT` function to
perform [classification](/bigquery/docs/classification-overview). You can use
both types of random forest models with the
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
MODEL_TYPE = { 'RANDOM_FOREST_CLASSIFIER' | 'RANDOM_FOREST_REGRESSOR' } ]
    [, APPROX_GLOBAL_FEATURE_CONTRIB = { TRUE | FALSE } ]
    [, NUM_PARALLEL_TREE = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, MAX_TREE_DEPTH = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, L1_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, L2_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, TREE_METHOD = { {'AUTO' | 'EXACT' | 'APPROX' | 'HIST'} | HPARAM_CANDIDATES([candidates]) } ]
    [, MIN_TREE_CHILD_WEIGHT = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, COLSAMPLE_BYTREE = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, COLSAMPLE_BYLEVEL = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, COLSAMPLE_BYNODE = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, MIN_SPLIT_LOSS = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, SUBSAMPLE = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, INSTANCE_WEIGHT_COL = string_value ]
    [, AUTO_CLASS_WEIGHTS = { TRUE | FALSE } ]
    [, CLASS_WEIGHTS = struct_array ]
    [, ENABLE_GLOBAL_EXPLAIN = { TRUE | FALSE } ]
    [, EARLY_STOP = { TRUE | FALSE } ]
    [, MIN_REL_PROGRESS = float64_value ]
    [, INPUT_LABEL_COLS = string_array ]
    [, DATA_SPLIT_METHOD = { 'AUTO_SPLIT' | 'RANDOM' | 'CUSTOM' | 'SEQ' | 'NO_SPLIT' } ]
    [, DATA_SPLIT_EVAL_FRACTION = float64_value ]
    [, DATA_SPLIT_TEST_FRACTION = float64_value ]
    [, DATA_SPLIT_COL = string_value ]
    [, NUM_TRIALS = int64_value ]
    [, MAX_PARALLEL_TRIALS = int64_value ]
    [, HPARAM_TUNING_ALGORITHM = { 'VIZIER_DEFAULT' | 'RANDOM_SEARCH' | 'GRID_SEARCH' } ]
    [, HPARAM_TUNING_OBJECTIVES = { 'ROC_AUC' | 'R2_SCORE' | ... } ]
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
MODEL_TYPE = { 'RANDOM_FOREST_CLASSIFIER' | 'RANDOM_FOREST_REGRESSOR' }
```

**Description**

Specifies the model type. This option is required.

### `APPROX_GLOBAL_FEATURE_CONTRIB`

**Syntax**

```
APPROX_GLOBAL_FEATURE_CONTRIB = { TRUE | FALSE }
```

**Description**

Enables fast approximation for feature contributions. This capability is
provided by the XGBoost library; BigQuery ML only passes this
option through to it. For more information, see
[Package 'xgboost'](https://cran.r-project.org/web/packages/xgboost/xgboost.pdf)
and search for `approxcontrib`.

In order to use the fast approximation for feature contribution
computations, you need to set both `ENABLE_GLOBAL_EXPLAIN` and
`APPROX_GLOBAL_FEATURE_CONTRIB` to `TRUE`.

**Arguments**

A `BOOL` value. The default value is `TRUE` when `ENABLE_GLOBAL_EXPLAIN` is
`TRUE` and `NUM_PARALLEL_TREE >= 50`, otherwise it is `FALSE`.

### `NUM_PARALLEL_TREE`

**Syntax**

`NUM_PARALLEL_TREE = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The number of parallel trees constructed during each iteration. To train a
boosted random forest model, set this value to larger than `1`.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify an `INT64`
value greater than or equal to `2`. The default value is `100`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `INT64` values that define
  the range of the hyperparameter. For example,
  `NUM_PARALLEL_TREE = HPARAM_RANGE(50, 100)`.
* The `HPARAM_CANDIDATES` keyword and an array of `INT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `NUM_PARALLEL_TREE = HPARAM_CANDIDATES([5, 10, 50, 150])`.

When running hyperparameter tuning, the valid range is `(2, ∞]`,
the default range is `(2, 200]`, and the scale type is `LINEAR`.

### `MAX_TREE_DEPTH`

**Syntax**

`MAX_TREE_DEPTH = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The maximum depth of a tree.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify an `INT64`
value greater than or equal to `1`. The default value is `15`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `INT64` values that define
  the range of the hyperparameter. For example,
  `MAX_TREE_DEPTH = HPARAM_RANGE(1, 4)`.
* The `HPARAM_CANDIDATES` keyword and an array of `INT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `MAX_TREE_DEPTH = HPARAM_CANDIDATES([5, 10, 15, 20])`.

When running hyperparameter tuning, the valid range is `(1, 20]`, the default
range is `(1, 20]`, and the scale type is `LINEAR`.

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

### `TREE_METHOD`

**Syntax**

`TREE_METHOD = { { 'AUTO' | 'EXACT' | 'APPROX' | 'HIST'} | HPARAM_CANDIDATES([candidates]) }`

**Description**

The type of tree construction algorithm.

`HIST` is recommended for large datasets in order to increase training
speed and reduce resource consumption. For more information, see
[tree booster](https://xgboost.readthedocs.io/en/latest/parameter.html#parameters-for-tree-booster).

**Arguments**

This option accepts the following values:

* `AUTO`: Faster histogram optimized approximate greedy algorithm.
  This is the default.
* `EXACT`: Exact greedy algorithm. Enumerates all split candidates.
* `APPROX`: Approximate greedy algorithm using quantile sketch and gradient
  histogram.
* `HIST`: Same as the `AUTO` tree method.

If you are running hyperparameter training, you can provide more than one
value for this option by using `HPARAM_CANDIDATES` and specifying an array.
For example, `TREE_METHOD = HPARAM_CANDIDATES(['APPROX', 'HIST'])`.

### `MIN_TREE_CHILD_WEIGHT`

**Syntax**

`MIN_TREE_CHILD_WEIGHT = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The minimum sum of instance weight needed in a child for further partitioning.
If the tree partition step results in a leaf node whose sum of instance
weight is less than `MIN_TREE_CHILD_WEIGHT`, then the building process stops
partitioning. The larger the `MIN_TREE_CHILD_WEIGHT` value is,
the more conservative the algorithm is.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify an `INT64`
value greater than or equal to `0`. The default value is `1`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `INT64` values that define
  the range of the hyperparameter. For example,
  `MIN_TREE_CHILD_WEIGHT = HPARAM_RANGE(0, 5)`.
* The `HPARAM_CANDIDATES` keyword and an array of `INT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `MIN_TREE_CHILD_WEIGHT = HPARAM_CANDIDATES([0, 1, 3, 5])`.

When running hyperparameter tuning, the valid range is `[0, ∞)`,
there is no default range, and the scale type is `LINEAR`.

### `COLSAMPLE_BYTREE`

**Syntax**

`COLSAMPLE_BYTREE = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The subsample ratio of columns when constructing each tree. Subsampling occurs
once for every tree constructed.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a `FLOAT64`
value between `0` and `1.0`. The default value is `1.0`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range of the hyperparameter. For example,
  `COLSAMPLE_BYTREE = HPARAM_RANGE(0, 0.3)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `COLSAMPLE_BYTREE = HPARAM_CANDIDATES([0, 0.1, 0.3, 0.5])`.

When running hyperparameter tuning, the valid range is `[0, 1.0]`, there is
no default range, and the scale type is `LINEAR`.

### `COLSAMPLE_BYLEVEL`

**Syntax**

`COLSAMPLE_BYLEVEL = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The subsample ratio of columns for each level. Subsampling occurs once for every
new depth level reached in a tree. Columns are subsampled from the set of
columns chosen for the current tree.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a `FLOAT64`
value between `0` and `1.0`. The default value is `1.0`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range of the hyperparameter. For example,
  `COLSAMPLE_BYLEVEL = HPARAM_RANGE(0, 0.3)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `COLSAMPLE_BYLEVEL = HPARAM_CANDIDATES([0, 0.1, 0.3, 0.5])`.

When running hyperparameter tuning, the valid range is `[0, 1.0]`, there is
no default range, and the scale type is `LINEAR`.

### `COLSAMPLE_BYNODE`

**Syntax**

`COLSAMPLE_BYNODE = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The subsample ratio of columns for each node (split). Subsampling occurs once
for every time a new split is evaluated. Columns are subsampled from the set of
columns chosen for the current level.

At least one of the `COLSAMPLE_BY*` parameters must be set to a value less than
`1.0` to enable the random selection of columns. Normally, `COLSAMPLE_BYNODE`
is a value less than `1.0` to randomly sample the columns at each tree split.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a `FLOAT64`
value between `0` and `1.0`. The default value is `0.8`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range of the hyperparameter. For example,
  `COLSAMPLE_BYNODE = HPARAM_RANGE(0, 0.3)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `COLSAMPLE_BYNODE = HPARAM_CANDIDATES([0, 0.1, 0.3, 0.5])`.

When running hyperparameter tuning, the valid range is `[0, 1.0]`, there is
no default range, and the scale type is `LINEAR`.

### `MIN_SPLIT_LOSS`

**Syntax**

`MIN_SPLIT_LOSS = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The minimum loss reduction required to make a further partition on a leaf node of
the tree. The larger the `MIN_SPLIT_LOSS` value is, the more conservative the
algorithm is.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a `FLOAT64`
value. The default value is `0`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range of the hyperparameter. For example,
  `MIN_SPLIT_LOSS = HPARAM_RANGE(0, 5.5)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `MIN_SPLIT_LOSS = HPARAM_CANDIDATES([0, 0.5, 1.5, 2.5])`.

When running hyperparameter tuning, the valid range is `[0, ∞)`, there
is no default range, and the scale type is `LINEAR`.

### `SUBSAMPLE`

**Syntax**

`SUBSAMPLE = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The subsample ratio of the training instances during construction of each tree.
Setting this value to `0.5` means that training randomly samples half of the
training data prior to growing trees, which prevents overfitting. This is
independent of the training-test data split used in the training options. The
test data is not used in any iteration irrespective of the `SUBSAMPLE` value;
subsampling is only applied to the training data.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a `FLOAT64`
value greater than `0` and less than `1.0`. The default value is `0.8`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range of the hyperparameter. For example,
  `SUBSAMPLE = HPARAM_RANGE(0, 0.6)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `SUBSAMPLE = HPARAM_CANDIDATES([0, 0.1, 0.2, 0.6])`.

When running hyperparameter tuning, the valid range is `(0, 1.0]`, the default
range is `(0, 1.0]`, and the scale type is `LINEAR`.

### `INSTANCE_WEIGHT_COL`

**Syntax**

`INSTANCE_WEIGHT_COL = string_value`

**Description**

The column used to specify the weights for each data point in the
training dataset. The column you specify must be a numerical column. You can't
use this column as a feature or label, and it is excluded from features
automatically. You can't specify this option if `AUTO_CLASS_WEIGHTS` is `TRUE`
or if `CLASS_WEIGHTS` is set.

The `INSTANCE_WEIGHT_COL` option is only supported for non-array
features.

**Arguments**

A `STRING` value.

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

### `ENABLE_GLOBAL_EXPLAIN`

**Syntax**

```
ENABLE_GLOBAL_EXPLAIN =
```