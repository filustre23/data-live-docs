* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The CREATE MODEL statement

To create a model in BigQuery, use the BigQuery ML `CREATE
MODEL` statement. This statement is similar to the
[`CREATE TABLE`](/bigquery/docs/data-definition-language#create_table_statement)
DDL statement. When you run a query that contains a `CREATE MODEL` statement, a
[query job](/bigquery/docs/managing-jobs) is generated for you that processes
the query. You can also use the Google Cloud console user interface to
[create a model by using a UI](/bigquery/docs/create-machine-learning-model-console)
([Preview](https://cloud.google.com/products#product-launch-stages)).

For more information about supported SQL statements and functions for each
model type, see the following documents:

* [End-to-end user journeys for generative AI models](/bigquery/docs/e2e-journey-genai)
* [End-to-end user journeys for time series forecasting models](/bigquery/docs/e2e-journey-forecast)
* [End-to-end user journeys for ML models](/bigquery/docs/e2e-journey)
* [End-to-end user journeys for imported models](/bigquery/docs/e2e-journey-import)
* [Contribution analysis user journey](/bigquery/docs/contribution-analysis#contribution_analysis_user_journey)

## Required permissions

* To create a dataset to store the model, you need the
  `bigquery.datasets.create` IAM permission.
* To create a model, you need the following permissions:

  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
  + `bigquery.connections.delegate` (for remote models)

The following [predefined IAM roles](/bigquery/docs/access-control#bigquery)
grant these permissions:

* [BigQuery Studio Admin](/bigquery/docs/access-control#bigquery.studioAdmin)
* [BigQuery Admin](/bigquery/docs/access-control#bigquery.admin)

For more information about IAM roles and permissions in
BigQuery, see
[Introduction to IAM](/bigquery/docs/access-control).

## `CREATE MODEL` syntax

**Note:** This syntax statement provides a comprehensive list of model types with
their model options. When you create a model, use that model specific `CREATE
MODEL` statement for convenience. You can view specific `CREATE MODEL`
statements by clicking the `MODEL_TYPE` name in the following list,
in the table of contents in the left panel, or in the *create model* link in the
[End-to-end user journey for each model](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-e2e-journey).

```
{CREATE MODEL | CREATE MODEL IF NOT EXISTS | CREATE OR REPLACE MODEL}
model_name
[TRANSFORM (select_list)]
[INPUT (field_name field_type)
 OUTPUT (field_name field_type)]
[REMOTE WITH CONNECTION {`connection_name` | DEFAULT}]
[OPTIONS(model_option_list)]
[AS {query_statement |
  (
    training_data AS (query_statement),
    custom_holiday AS (holiday_statement)
  )}]

model_option_list:
    MODEL_TYPE = { 'LINEAR_REG' |
      'LOGISTIC_REG' |
      'KMEANS' |
      'MATRIX_FACTORIZATION' |
      'PCA' |
      'AUTOENCODER' |
      'AUTOML_CLASSIFIER' |
      'AUTOML_REGRESSOR' |
      'BOOSTED_TREE_CLASSIFIER' |
      'BOOSTED_TREE_REGRESSOR' |
      'RANDOM_FOREST_CLASSIFIER' |
      'RANDOM_FOREST_REGRESSOR' |
      'DNN_CLASSIFIER' |
      'DNN_REGRESSOR' |
      'DNN_LINEAR_COMBINED_CLASSIFIER' |
      'DNN_LINEAR_COMBINED_REGRESSOR' |
      'ARIMA_PLUS' |
      'ARIMA_PLUS_XREG' |
      'TENSORFLOW' |
      'TENSORFLOW_LITE' |
      'ONNX' |
      'XGBOOST' |
      'CONTRIBUTION_ANALYSIS'}
    [, MODEL_REGISTRY = { 'VERTEX_AI' } ]
    [, VERTEX_AI_MODEL_ID = string_value ]
    [, VERTEX_AI_MODEL_VERSION_ALIASES = string_array ]
    [, INPUT_LABEL_COLS = string_array ]
    [, MAX_ITERATIONS = int64_value ]
    [, EARLY_STOP = { TRUE | FALSE } ]
    [, MIN_REL_PROGRESS = float64_value ]
    [, DATA_SPLIT_METHOD = { 'AUTO_SPLIT' | 'RANDOM' | 'CUSTOM' | 'SEQ' | 'NO_SPLIT' } ]
    [, DATA_SPLIT_EVAL_FRACTION = float64_value ]
    [, DATA_SPLIT_TEST_FRACTION = float64_value ]
    [, DATA_SPLIT_COL = string_value ]
    [, OPTIMIZE_STRATEGY = { 'AUTO_STRATEGY' | 'BATCH_GRADIENT_DESCENT' | 'NORMAL_EQUATION' } ]
    [, L1_REG = float64_value ]
    [, L2_REG = float64_value ]
    [, LEARN_RATE_STRATEGY = { 'LINE_SEARCH' | 'CONSTANT' } ]
    [, LEARN_RATE = float64_value ]
    [, LS_INIT_LEARN_RATE = float64_value ]
    [, WARM_START = { TRUE | FALSE } ]
    [, AUTO_CLASS_WEIGHTS = { TRUE | FALSE } ]
    [, CLASS_WEIGHTS = struct_array ]
    [, INSTANCE_WEIGHT_COL = string_value ]
    [, NUM_CLUSTERS = int64_value ]
    [, KMEANS_INIT_METHOD = { 'RANDOM' | 'KMEANS++' | 'CUSTOM' } ]
    [, KMEANS_INIT_COL = string_value ]
    [, DISTANCE_TYPE = { 'EUCLIDEAN' | 'COSINE' } ]
    [, STANDARDIZE_FEATURES = { TRUE | FALSE } ]
    [, MODEL_PATH = string_value ]
    [, BUDGET_HOURS = float64_value ]
    [, OPTIMIZATION_OBJECTIVE = { string_value | struct_value } ]
    [, FEEDBACK_TYPE = {'EXPLICIT' | 'IMPLICIT'} ]
    [, NUM_FACTORS = int64_value ]
    [, USER_COL = string_value ]
    [, ITEM_COL = string_value ]
    [, RATING_COL = string_value ]
    [, WALS_ALPHA = float64_value ]
    [, BOOSTER_TYPE = { 'gbtree' | 'dart'} ]
    [, NUM_PARALLEL_TREE = int64_value ]
    [, DART_NORMALIZE_TYPE = { 'tree' | 'forest'} ]
    [, TREE_METHOD = { 'auto' | 'exact' | 'approx' | 'hist'} ]
    [, MIN_TREE_CHILD_WEIGHT = float64_value ]
    [, COLSAMPLE_BYTREE = float64_value ]
    [, COLSAMPLE_BYLEVEL = float64_value ]
    [, COLSAMPLE_BYNODE = float64_value ]
    [, MIN_SPLIT_LOSS = float64_value ]
    [, MAX_TREE_DEPTH = int64_value ]
    [, SUBSAMPLE = float64_value ]
    [, ACTIVATION_FN = { 'RELU' | 'RELU6' | 'CRELU' | 'ELU' | 'SELU' | 'SIGMOID' | 'TANH' } ]
    [, BATCH_SIZE = int64_value ]
    [, DROPOUT = float64_value ]
    [, HIDDEN_UNITS = int_array ]
    [, OPTIMIZER = { 'ADAGRAD' | 'ADAM' | 'FTRL' | 'RMSPROP' | 'SGD' } ]
    [, TIME_SERIES_TIMESTAMP_COL = string_value ]
    [, TIME_SERIES_DATA_COL = string_value ]
    [, TIME_SERIES_ID_COL = { string_value | string_array } ]
    [, HORIZON = int64_value ]
    [, AUTO_ARIMA = { TRUE | FALSE } ]
    [, AUTO_ARIMA_MAX_ORDER = int64_value ]
    [, AUTO_ARIMA_MIN_ORDER = int64_value ]
    [, NON_SEASONAL_ORDER = (int64_value, int64_value, int64_value) ]
    [, DATA_FREQUENCY = { 'AUTO_FREQUENCY' | 'PER_MINUTE' | 'HOURLY' | 'DAILY' | 'WEEKLY' | ... } ]
    [, FORECAST_LIMIT_LOWER_BOUND = float64_value  ]
    [, FORECAST_LIMIT_UPPER_BOUND = float64_value  ]
    [, INCLUDE_DRIFT = { TRUE | FALSE } ]
    [, HOLIDAY_REGION = { 'GLOBAL' | 'NA' | 'JAPAC' | 'EMEA' | 'LAC' | 'AE' | ... } ]
    [, CLEAN_SPIKES_AND_DIPS = { TRUE | FALSE } ]
    [, ADJUST_STEP_CHANGES = { TRUE | FALSE } ]
    [, DECOMPOSE_TIME_SERIES = { TRUE | FALSE } ]
    [, HIERARCHICAL_TIME_SERIES_COLS = { string_array } ]
    [, ENABLE_GLOBAL_EXPLAIN = { TRUE | FALSE } ]
    [, APPROX_GLOBAL_FEATURE_CONTRIB = { TRUE | FALSE }]
    [, CALCULATE_P_VALUES = { TRUE | FALSE } ]
    [, FIT_INTERCEPT = { TRUE | FALSE } ]
    [, CATEGORY_ENCODING_METHOD = { 'ONE_HOT_ENCODING' | 'DUMMY_ENCODING' |
      'LABEL_ENCODING' | 'TARGET_ENCODING' } ]
    [, { ENDPOINT = string_value |
      HUGGING_FACE_MODEL_ID = string_value |
      MODEL_GARDEN_MODEL_NAME = string_value} ]
    [, HUGGING_FACE_TOKEN = string_value ]
    [, MACHINE_TYPE = string_value ]
    [, MIN_REPLICA_COUNT = int64_value ]
    [, MAX_REPLICA_COUNT = int64_value ]
    [, RESERVATION_AFFINITY_TYPE = { 'NO_RESERVATION' | 'ANY_RESERVATION' | 'SPECIFIC_RESERVATION' } ]
    [, RESERVATION_AFFINITY_KEY = string_value ]
    [, RESERVATION_AFFINITY_VALUES = string_array ]
    [, ENDPOINT_IDLE_TTL = interval_value ]
    [, REMOTE_SERVICE_TYPE = { 'CLOUD_AI_VISION_V1' | 'CLOUD_AI_NATURAL_LANGUAGE_V1' |
      'CLOUD_AI_TRANSLATE_V3' } ]
    [, NUM_TRIALS = int64_value, ]
    [, MAX_PARALLEL_TRIALS = int64_value ]
    [, HPARAM_TUNING_ALGORITHM = { 'VIZIER_DEFAULT' | 'RANDOM_SEARCH' | 'GRID_SEARCH' } ]
    [, HPARAM_TUNING_OBJECTIVES = { 'R2_SCORE' | 'ROC_AUC' | ... } ]
    [, NUM_PRINCIPAL_COMPONENTS = int64_value ]
    [, PCA_EXPLAINED_VARIANCE_RATIO = float64_value ]
    [, SCALE_FEATURES = { TRUE | FALSE } ]
    [, PCA_SOLVER = { 'FULL' | 'RANDOMIZED' | 'AUTO' } ]
    [, TIME_SERIES_LENGTH_FRACTION = float64_value ]
    [, MIN_TIME_SERIES_LENGTH = int64_value ]
    [, MAX_TIME_SERIES_LENGTH = int64_value ]
    [, TREND_SMOOTHING_WINDOW_SIZE = int64_value ]
    [, SEASONALITIES = string_array ]
    [, PROMPT_COL = string_value ]
    [, LEARNING_RATE_MULTIPLIER = float64_value ]
    [, ACCELERATOR_TYPE = { 'GPU' | 'TPU' } ]
    [, EVALUATION_TASK = { 'TEXT_GENERATION' | 'CLASSIFICATION' | 'SUMMARIZATION' |
      'QUESTION_ANSWERING' | 'UNSPECIFIED' } ]
    [, DOCUMENT_PROCESSOR = string_value ]
    [, SPEECH_RECOGNIZER = string_value ]
    [, KMS_KEY_NAME = string_value ]
    [, CONTRIBUTION_METRIC = string_value ]
    [, DIMENSION_ID_COLS = string_array ]
    [, IS_TEST_COL = string_value ]
    [, MIN_APRIORI_SUPPORT = float64_value ]
    [, PRUNING_METHOD = {'NO_PRUNING', 'PRUNE_REDUNDANT_INSIGHTS'}  ]
    [, TOP_K_INSIGHTS_BY_APRIORI_SUPPORT = int64_value ]
```

### `CREATE MODEL`

Creates and trains a new model in the specified dataset. If the model name
exists, `CREATE MODEL` returns an error.

### `CREATE MODEL IF NOT EXISTS`

Creates and trains a new model only if the model does not exist in the
specified dataset.

### `CREATE OR REPLACE MODEL`

Creates and trains a model and replaces an existing model with the same name in
the specified dataset.

### `model_name`

`model_name` is the name of the model you're creating or replacing. The model
name must be unique per dataset: no other model or table can have the same name.
The model name must follow the same naming rules as a BigQuery table. A
model name can:

* Contain up to 1,024 characters
* Contain letters (upper or lower case), numbers, and underscores

`model_name` is case-sensitive.

If you don't have a default project configured, prepend the project ID to the
model name in following format, including backticks:
`` `[PROJECT_ID].[DATASET].[MODEL]` ``; for example,
`` `myproject.mydataset.mymodel` ``.

### `TRANSFORM`

TRANSFORM lets you specify all preprocessing during model creation and
have it automatically applied during prediction and evaluation.

For example, you can create the following model:

```
CREATE OR REPLACE MODEL `myproject.mydataset.mymodel`
  TRANSFORM(ML.FEATURE_CROSS(STRUCT(f1, f2)) as cross_f,
            ML.QUANTILE_BUCKETIZE(f3) OVER() as buckets,
            label_col)
  OPTIONS(model_type='linear_reg', input_label_cols=['label_col'])
AS SELECT * FROM t
```

During prediction, you don't need to preprocess the input again, and the same
transformations are automatically restored:

```
SELECT * FROM ML.PREDICT(MODEL `myproject.mydataset.mymodel`, (SELECT f1, f2, f3 FROM table))
```

When the `TRANSFORM` clause is present, only output columns from the
`TRANSFORM` clause are used in training. Any results from
`query_statement` that don't appear in the `TRANSFORM` clause are ignored.

The input columns of the `TRANSFORM` clause are the result of `query_statement`.
So, the final input used in training is the set of columns generated by the
following query:

```
SELECT (select_list) FROM (query_statement);
```

Input columns of the `TRANSFORM` clause can be of any SIMPLE type or ARRAY of
SIMPLE type. SIMPLE types are non-STRUCT and non-ARRAY data types.

In prediction (`ML.PREDICT`), users only need to pass in the original
columns from the `query_statement` that are used inside the `TRANSFORM` clause.
The columns dropped in `TRANSFORM` don't need to be provided during prediction.
`TRANSFORM` is automatically applied to the input data during prediction,
including the statistics used in ML analytic functions (for example,
`ML.QUANTILE_BUCKETIZE`).

To learn more about feature preprocessing, see
[Feature preprocessing overview](/bigquery/docs/preprocess-overview), or try the
[Feature Engineering Functions](https://github.com/GoogleCloudPlatform/bigquery-ml-utils/blob/master/notebooks/bqml-preprocessing-functions.ipynb) notebook.

To try using the `TRANSFORM` clause, try the
[Use the BigQuery ML `TRANSFORM` clause for feature engineering](/bigquery/docs/bigqueryml-transform) tutorial or the
[Create Model With Inline Transpose](https://github.com/GoogleCloudPlatform/bigquery-ml-utils/blob/master/notebooks/bqml-feature-engineering.ipynb) notebook.

### `select_list`

You can pass columns from `query_statement` through to model training without
transformation by either using `*`, `* EXCEPT()`, or by listing
the column names directly.

Not all columns from `query_statement` are required to appear in the `TRANSFORM`
clause, so you can drop columns appearing in `query_statement` by omitting
them from the `TRANSFORM` clause.

You can transform inputs from `query_statement` by using expressions in
`select_list`. `select_list` is similar to a normal `SELECT` statement.
`select_list` supports the following syntax:

* `*`
* `* EXCEPT()`
* `* REPLACE()`
* `expression`
* `expression.*`

The following cannot appear inside `select_list`:

* Aggregation functions.
* Non-BigQuery ML analytic functions. For more information about
  supported functions, see
  [Manual feature preprocessing](/bigquery/docs/manual-preprocessing).
* UDFs.
* Subqueries.
* Anonymous columns. For example, `a + b as c` is allowed, while `a + b` isn't.

The output columns of `select_list` can be of any BigQuery
supported data type.

If present, the following columns must appear in `select_list` without
transformation:

* `label`
* `data_split_col`
* `kmeans_init_col`
* `instance_weight_col`

If these columns are returned by `query_statement`, you must reference them in
`select_list` by column name outside of any expression, or by using `*`. You
can't use aliases with these columns.

### `INPUT` and `OUTPUT`

`INPUT` and `OUTPUT` clauses are used to specify input and output format for [remote models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model) or [XGBoost models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-xgboost).

#### `field_name`

For remote models, `INPUT` and `OUTPUT` field names must be identical as the
field names of the Gemini Enterprise Agent Platform endpoint request and response. See examples in [remote model `INPUT` and `OUTPUT` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https#in-out-clause).

For XGBoost models, `INPUT` field names must be identical to the names in the `feature_names` field if `feature_names` field is populated in the XGBoost model file. See [XGBoost INPUT OUTPUT clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-xgboost#input_output_clause) for more details.

#### `field_type`

[Remote models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https) support the
following BigQuery data types for `INPUT` and `OUTPUT` clauses:

* Simple type: [BOOL](/bigquery/docs/reference/standard-sql/data-types#boolean_type), [INT64](/bigquery/docs/reference/standard-sql/data-types#integer_types), [FLOAT64](/bigquery/docs/reference/standard-sql/data-types#floating_point_types), [NUMERIC](/bigquery/docs/reference/standard-sql/data-types#decimal_types), [BIGNUMERIC](/bigquery/docs/reference/standard-sql/data-types#decimal_types), [STRING](/bigquery/docs/reference/standard-sql/data-types#string_type)
* [ARRAY](/bigquery/docs/reference/standard-sql/data-types#array_type)<Simple type>

[XGBoost models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-xgboost) only support
[numeric types](/bigquery/docs/reference/standard-sql/data-types#numeric_types)
for the `INPUT` field type and
[`FLOAT64`](/bigquery/docs/reference/standard-sql/data-types#floating_point_types)
for the `OUTPUT` field type.

### `connection_name`

BigQuery uses a `CLOUD_RESOURCE` [connection](/bigquery/docs/create-cloud-resource-connection)
to interact with your Gemini Enterprise Agent Platform endpoint. You need to grant [Vertex AI User role](/vertex-ai/docs/general/access-control#aiplatform.user) to connection's service account on your Gemini Enterprise Agent Platform endpoint project.

See examples in [remote model `CONNECTION` statement](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model#connection).

To use a [default connection](/bigquery/docs/default-connections), specify
`DEFAULT` instead of the connection name.

### `model_option_list`

`CREATE MODEL` supports the following options:

#### `MODEL_TYPE`

**Syntax**

```
MODEL_TYPE = { 'LINEAR_REG' | 'LOGISTIC_REG' | 'KMEANS'
```