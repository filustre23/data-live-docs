* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The CREATE MODEL statement for boosted trees models using XGBoost

This document describes the `CREATE MODEL` statement for creating
[boosted trees](https://xgboost.readthedocs.io/en/stable/tutorials/model.html)
models in BigQuery by using SQL. Alternatively, you can use the
Google Cloud console user interface to
[create a model by using a UI](/bigquery/docs/create-machine-learning-model-console)
([Preview](https://cloud.google.com/products#product-launch-stages)) instead of constructing the SQL
statement yourself. Boosted trees models are trained using the
[XGBoost library](https://xgboost.readthedocs.io/en/latest/).

You can use boosted trees regressor models with the
[`ML.PREDICT` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict)
to perform [regression](/bigquery/docs/regression-overview), and you can use
boosted trees classifier models with the `ML.PREDICT` function to
perform [classification](/bigquery/docs/classification-overview). You can use
both types of boosted trees models with the
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
MODEL_TYPE = { 'BOOSTED_TREE_CLASSIFIER' | 'BOOSTED_TREE_REGRESSOR' }
    [, APPROX_GLOBAL_FEATURE_CONTRIB = { TRUE | FALSE } ]
    [, CATEGORY_ENCODING_METHOD = { 'ONE_HOT_ENCODING` | 'TARGET_ENCODING' | 'LABEL_ENCODING' } ]
    [, BOOSTER_TYPE = { {'GBTREE' | 'DART'} | HPARAM_CANDIDATES([candidates]) } ]
    [, DART_NORMALIZE_TYPE = { {'TREE' | 'FOREST'} | HPARAM_CANDIDATES([candidates]) } ]
    [, NUM_PARALLEL_TREE = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, MAX_TREE_DEPTH = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, DROPOUT = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, L1_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, L2_REG = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
    [, LEARN_RATE = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) } ]
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
    [, MAX_ITERATIONS = int64_value ]
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

**Syntax**

```
MODEL_TYPE = { 'BOOSTED_TREE_CLASSIFIER' | 'BOOSTED_TREE_REGRESSOR' }
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
`TRUE` and `NUM_PARALLEL_TREE >= 10`, otherwise it is `FALSE`.

### `CATEGORY_ENCODING_METHOD`

**Syntax**

```
CATEGORY_ENCODING_METHOD = { 'ONE_HOT_ENCODING' | 'TARGET_ENCODING' | 'LABEL_ENCODING' }
```

**Description**

Specifies which encoding method to use on non-numeric features. For more
information about supported encoding methods, see
[BigQuery ML auto preprocessing](/bigquery/docs/auto-preprocessing).

**Arguments**

This option accepts the following values:

* `LABEL_ENCODING`. This is the default.
* `TARGET_ENCODING`
* `ONE_HOT_ENCODING`

### `BOOSTER_TYPE`

**Syntax**

`BOOSTER_TYPE = { { 'GBTREE' | 'DART'} | HPARAM_CANDIDATES([candidates]) }`

**Description**

Specifies the booster type to use.

**Arguments**

This option accepts the following values:

* `GBTREE`: [tree-booster](https://xgboost.readthedocs.io/en/latest/parameter.html#parameters-for-tree-booster). This is the default.
* `DART`: [dart-booster](https://xgboost.readthedocs.io/en/latest/tutorials/dart.html)

If you are running hyperparameter training, you can provide more than one
value for this option by using `HPARAM_CANDIDATES` and specifying an array.
For example, `BOOSTER_TYPE = HPARAM_CANDIDATES(['GBTREE', 'DART'])`.

### `DART_NORMALIZE_TYPE`

**Syntax**

`DART_NORMALIZE_TYPE = { { 'TREE' | 'FOREST'} | HPARAM_CANDIDATES([candidates]) }`

**Description**

The type of normalization algorithm to use if you are using the `DART`
booster.

**Arguments**

This option accepts the following values:

* `TREE`: New trees have the same weight of each of the dropped trees. This is
  the default value.
* `FOREST`: New trees have the same weight of the sum of the dropped
  trees (forest).

If you are running hyperparameter training, you can provide more than one
value for this option by using `HPARAM_CANDIDATES` and specifying an array.
For example, `DART_NORMALIZE_TYPE = HPARAM_CANDIDATES(['TREE', 'FOREST'])`.

### `NUM_PARALLEL_TREE`

**Syntax**

`NUM_PARALLEL_TREE = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The number of parallel trees constructed during each iteration. To train a
boosted random forest model, set this value to larger than `1`.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify an `INT64`
value. The default value is `1`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `INT64` values that define
  the range of the hyperparameter. For example,
  `NUM_PARALLEL_TREE = HPARAM_RANGE(1, 5)`.
* The `HPARAM_CANDIDATES` keyword and an array of `INT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `NUM_PARALLEL_TREE = HPARAM_CANDIDATES([0, 1, 3, 5])`.

When running hyperparameter tuning, the valid range is `(1, ∞]`, there
is no default range, and the scale type is `LINEAR`.

### `MAX_TREE_DEPTH`

**Syntax**

`MAX_TREE_DEPTH = { int64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

The maximum depth of a tree.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify an `INT64`
value. The default value is `6`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `INT64` values that define
  the range of the hyperparameter. For example,
  `MAX_TREE_DEPTH = HPARAM_RANGE(0, 4)`.
* The `HPARAM_CANDIDATES` keyword and an array of `INT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `MAX_TREE_DEPTH = HPARAM_CANDIDATES([1, 5, 10, 15])`.

When running hyperparameter tuning, the valid range is `(1, 20]`, the default
range is `(1, 10]`, and the scale type is `LINEAR`.

### `DROPOUT`

**Syntax**

`DROPOUT = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

Specifies the dropout rate, which is the fraction of previous trees to drop
during the dropout.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a `FLOAT64`
value between `0` and `1.0`. The default value is `0`.

**Note:** The `DROPOUT` parameter is only applicable when the `BOOSTER_TYPE` is
set to `'DART'`. If you are using hyperparameter tuning, ensure that `'DART'`
is included in the `HPARAM_CANDIDATES` for `BOOSTER_TYPE` if you intend to
tune `DROPOUT`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range of the hyperparameter. For example,
  `DROPOUT = HPARAM_RANGE(0, 0.6)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `DROPOUT = HPARAM_CANDIDATES([0, 0.1, 0.2, 0.6])`.

When running hyperparameter tuning, the valid range is `(0, 1.0]`, there is no
default range, and the scale type is `LINEAR`.

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

### `LEARN_RATE`

**Syntax**

`LEARN_RATE = { float64_value | HPARAM_RANGE(range) | HPARAM_CANDIDATES([candidates]) }`

**Description**

`LEARN_RATE` is the step size shrinkage used in updates to prevents overfitting.
After each boosting step, `LEARN_RATE` shrinks the feature weights to make the
boosting process more conservative.

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a `FLOAT64`
value. The default value is `0.3`.

If you are running hyperparameter tuning, use one of the following options:

* The `HPARAM_RANGE` keyword and two `FLOAT64` values that define
  the range of the hyperparameter. For example,
  `LEARN_RATE = HPARAM_RANGE(0, 0.5)`.
* The `HPARAM_CANDIDATES` keyword and an array of `FLOAT64` values
  that provide discrete values to use for the hyperparameter. For example,
  `LEARN_RATE = HPARAM_CANDIDATES([0, 0.1, 0.3, 0.5])`.

When running hyperparameter tuning, the valid range is `(0, ∞]`, the
default range is `(0, 1.0]`, and the scale type is `LINEAR`.

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

**Arguments**

If you aren't running hyperparameter tuning, then you can specify a `FLOAT64`
value between `0` and `1.0`. The default value is `1.0`.

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