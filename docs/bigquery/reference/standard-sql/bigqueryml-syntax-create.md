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
    [, INTEGRATED_GRADIENTS_NUM_STEPS = int64_value ]
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
    [, XGBOOST_VERSION = { '0.9' | '1.1' } ]
    [, TF_VERSION = { '1.15' | '2.8.0' | '2.17.0' } ]
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
field names of the Vertex AI endpoint request and response. See examples in [remote model `INPUT` and `OUTPUT` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https#in-out-clause).

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
to interact with your Vertex AI endpoint. You need to grant [Vertex AI User role](/vertex-ai/docs/general/access-control#aiplatform.user) to connection's service account on your Vertex AI endpoint project.

See examples in [remote model `CONNECTION` statement](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model#connection).

To use a [default connection](/bigquery/docs/default-connections), specify
specify `DEFAULT` instead of the connection name.

### `model_option_list`

`CREATE MODEL` supports the following options:

#### `MODEL_TYPE`

**Syntax**

```
MODEL_TYPE = { 'LINEAR_REG' | 'LOGISTIC_REG' | 'KMEANS' | 'PCA' |
'MATRIX_FACTORIZATION' | 'AUTOENCODER' | 'AUTOML_REGRESSOR' |
'AUTOML_CLASSIFIER' | 'BOOSTED_TREE_CLASSIFIER' | 'BOOSTED_TREE_REGRESSOR' |
'RANDOM_FOREST_CLASSIFIER' | 'RANDOM_FOREST_REGRESSOR' |
'DNN_CLASSIFIER' | 'DNN_REGRESSOR' | 'DNN_LINEAR_COMBINED_CLASSIFIER' |
'DNN_LINEAR_COMBINED_REGRESSOR' | 'ARIMA_PLUS' | 'ARIMA_PLUS_XREG' |
'TENSORFLOW' | 'TENSORFLOW_LITE' | 'ONNX' | 'XGBOOST' | 'CONTRIBUTION_ANALYSIS'}
```

**Description**

Specify the model type. This argument is required.

**Arguments**

The argument is in the model type column.

| Model category | Model type | Description | Model specific CREATE MODEL statement |
| --- | --- | --- | --- |
| Regression | `'LINEAR_REG'` | Linear regression for real-valued label prediction; for example, the sales of an item on a given day. | [CREATE MODEL statement for generalized linear models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm) |
| `'BOOSTED_TREE_REGRESSOR'` | Create a boosted tree regressor model using the XGBoost library. | [CREATE MODEL statement for boosted tree models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree) |
| `'RANDOM_FOREST_REGRESSOR'` | Create a random forest regressor model using the XGBoost library. | [CREATE MODEL statement for random forest models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest) |
| `'DNN_REGRESSOR'` | Create a Deep Neural Network Regressor model. | [CREATE MODEL statement for DNN models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models) |
| `'DNN_LINEAR_COMBINED_REGRESSOR'` | Create a Wide-and-Deep Regressor model. | [CREATE MODEL statement for Wide-and-Deep models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models) |
| `'AUTOML_REGRESSOR'` | Create a regression model using AutoML. | [CREATE MODEL statement for AutoML models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl) |
| Classification | `'LOGISTIC_REG'` | Logistic regression for binary-class or multi-class classification; for example, determining whether a customer will make a purchase. | [CREATE MODEL statement for generalized linear models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm) |
| `'BOOSTED_TREE_CLASSIFIER'` | Create a boosted tree classifier model using the XGBoost library. | [CREATE MODEL statement for boosted tree models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree) |
| `'RANDOM_FOREST_CLASSIFIER'` | Create a random forest classifier model using the XGBoost library. | [CREATE MODEL statement for random forest models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest) |
| `'DNN_CLASSIFIER'` | Create a Deep Neural Network Classifier model. | [CREATE MODEL statement for DNN models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models) |
| `'DNN_LINEAR_COMBINED_CLASSIFIER'` | Create a Wide-and-Deep Classifier model. | [CREATE MODEL statement for Wide-and-Deep models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models) |
| `'AUTOML_CLASSIFIER'` | Create a classification model using AutoML. | [CREATE MODEL statement for AutoML models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl) |
| Clustering | `'KMEANS'` | K-means clustering for data segmentation; for example, identifying customer segments. | [CREATE MODEL statement for K-means models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans) |
| Collaborative Filtering | `'MATRIX_FACTORIZATION'` | Matrix factorization for recommendation systems. For example, given a set of users, items, and some ratings for a subset of the items, creates a model to predict a user's rating for items they have not rated. | [CREATE MODEL statement for matrix factorization models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization) |
| Dimensionality Reduction | `'PCA'` | Principal component analysis for dimensionality reduction. | [CREATE MODEL statement for PCA models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca) |
| `'AUTOENCODER'` | Create an Autoencoder model for anomaly detection, dimensionality reduction, and embedding purposes. | [CREATE MODEL statement for Autoencoder model](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder) |
| Time series forecasting | `'ARIMA_PLUS'` (previously `'ARIMA'`) | Univariate time-series forecasting with many modeling components under the hood such as ARIMA model for the trend, STL and ETS for seasonality, and holiday effects. | [CREATE MODEL statement for time series models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series) |
| `'ARIMA_PLUS_XREG'` | Multivariate time-series forecasting using linear regression and ARIMA\_PLUS as the underlying techniques. | [CREATE MODEL statement for time series models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series) |
| Augmented analytics | `'CONTRIBUTION_ANALYSIS'` | Create a contribution analysis model to find key drivers of a change. | [CREATE MODEL statement for Contribution Analysis](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-contribution-analysis) |
| Importing models | `'TENSORFLOW'` | Create a model by importing a TensorFlow model into BigQuery. | [CREATE MODEL statement for TensorFlow models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow) |
| `'TENSORFLOW_LITE'` | Create a model by importing a TensorFlow Lite model into BigQuery. | [CREATE MODEL statement for TensorFlow Lite models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tflite) |
| `'ONNX'` | Create a model by importing an ONNX model into BigQuery. | [CREATE MODEL statement for ONNX models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-onnx) |
| `'XGBOOST'` | Create a model by importing a XGBoost model into BigQuery. | [CREATE MODEL statement for XGBoost models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-xgboost) |
| Remote models | N/A | Create a model by specifying a Cloud AI service, or the endpoint for a Vertex AI model. | [CREATE MODEL statement for remote models over Google models in Vertex AI](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model)   [CREATE MODEL statement for remote models over hosted models in Vertex AI](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-https)   [CREATE MODEL statement for remote models over Cloud AI services](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service) |

**Note:** We are deprecating `ARIMA` as the model type. While the model training
pipelines of `ARIMA` and `ARIMA_PLUS` are the same, `ARIMA_PLUS` supports more
capabilities, including support for a new training option,
[`DECOMPOSE_TIME_SERIES`](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#decompose_time_series),
and table-valued functions including [`ML.ARIMA_EVALUATE`](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-arima-evaluate)
and [`ML.EXPLAIN_FORECAST`](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-explain-forecast).

#### Other model options

The following table provides a comprehensive list of model options, with a brief
descriptions and their applicable model types. You can find detailed description
in the model specific `CREATE MODEL` statement by clicking the model type in the
"Applied model types" column.

When the applied model types are supervised learning models, unless "regressor"
or "classifier" is explicitly listed, it means that model options apply to both
the regressor and the classifier. For example, the "boosted tree" means that
model option applies to both boosted tree regressor and boosted tree classifier,
while the "boosted tree classifier" only applies to the classifier.

| Name | Description | Applied model types |
| --- | --- | --- |
| MODEL\_REGISTRY | The MODEL\_REGISTRY option specifies the Model Registry destination. | All model types are supported. |
| VERTEX\_AI\_MODEL\_ID | The Vertex AI model ID to register the model with. | All model types are supported. |
| VERTEX\_AI\_MODEL\_VERSION\_ALIASES | The Vertex AI model alias to register the model with. | All model types are supported. |
| INPUT\_LABEL\_COLS | The label column names in the training data. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#input_label_cols),  [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#input_label_cols),  [Random forest](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#input_label_cols),  [DNN](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#input_label_cols),  [Wide & Deep](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#input_label_cols),  [AutoML](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-automl#input_label_cols) |
| MAX\_ITERATIONS | The maximum number of training iterations or steps. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#max_iterations),  [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#max_iterations),  [DNN](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#max_iterations),  [Wide & Deep](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#max_iterations),  [Kmeans](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans#max_iterations),  [Matrix factorization](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization#max_iterations),  [Autoencoder](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder#max_iterations) |
| EARLY\_STOP | Whether training should stop after the first iteration in which the relative loss improvement is less than the value specified for `MIN\_REL\_PROGRESS`. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#early_stop),  [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#early_stop),  [Random forest](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#early_stop),  [DNN](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#early_stop),  [Wide & Deep](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#early_stop),  [Kmeans](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans#early_stop),  [Matrix factorization](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization#early_stop),  [Autoencoder](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder#early_stop) |
| MIN\_REL\_PROGRESS | The minimum relative loss improvement that is necessary to continue training when `EARLY\_STOP` is set to true. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#min_rel_progress),  [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#min_rel_progress),  [Random forest](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#min_rel_progress),  [DNN](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#min_rel_progress),  [Wide & Deep](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#min_rel_progress),  [Kmeans](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans#min_rel_progress),  [Matrix factorization](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization#min_rel_progress),  [Autoencoder](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder#min_rel_progress) |
| DATA\_SPLIT\_METHOD | The method to split input data into training and evaluation sets when not running hyperparameter tuning, or into training, evaluation, and test sets when running hyperparameter tuning. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#data_split_method),  [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#data_split_method),  [Random forest](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#data_split_method),  [DNN](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#data_split_method),  [Wide & Deep](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#data_split_method)  [Matrix factorization](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization#data_split_method) |
| DATA\_SPLIT\_EVAL\_FRACTION | Specifies the fraction of the data used for evaluation. Accurate to two decimal places. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#data_split_eval_fraction),  [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#data_split_eval_fraction),  [Random forest](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#data_split_eval_fraction),  [DNN](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#data_split_eval_fraction),  [Wide & Deep](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#data_split_eval_fraction)  [Matrix factorization](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization#data_split_eval_fraction) |
| DATA\_SPLIT\_TEST\_FRACTION | Specifies the fraction of the data used for testing when you are running hyperparameter tuning. Accurate to two decimal places. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#data_split_test_fraction),  [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#data_split_test_fraction),  [Random forest](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#data_split_test_fraction),  [DNN](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#data_split_test_fraction),  [Wide & Deep](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#data_split_test_fraction)  [Matrix factorization](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization#data_split_test_fraction) |
| DATA\_SPLIT\_COL | Identifies the column used to split the data. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#data_split_col),  [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#data_split_col),  [Random forest](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#data_split_col),  [DNN](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#data_split_col),  [Wide & Deep](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#data_split_col)  [Matrix factorization](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization#data_split_col) |
| OPTIMIZE\_STRATEGY | The strategy to train linear regression models. | [Linear regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#optimize_strategy) |
| L1\_REG | The amount of [L1 regularization](https://developers.google.com/machine-learning/glossary/#L1_regularization) applied. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#l1_reg),  [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#l1_reg)  [Random forest](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#l1_reg) |
| L2\_REG | The amount of [L2 regularization](https://developers.google.com/machine-learning/glossary/#L2_regularization) applied. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#l2_reg),  [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#l2_reg),  [Random forest](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#l2_reg),  [Matrix factorization](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization#l2_reg),  [ARIMA\_PLUS\_XREG](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series#l2_reg) |
| LEARN\_RATE\_STRATEGY | The strategy for specifying the [learning rate](https://developers.google.com/machine-learning/glossary/#learning_rate) during training. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#learn_rate_strategy) |
| LEARN\_RATE | The learn rate for [gradient descent](https://developers.google.com/machine-learning/glossary/#gradient_descent) when LEARN\_RATE\_STRATEGY is set to CONSTANT. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#learn_rate) |
| LS\_INIT\_LEARN\_RATE | Sets the initial learning rate that LEARN\_RATE\_STRATEGY=LINE\_SEARCH uses. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#ls_init_learn_rate) |
| WARM\_START | Retrain a model with new training data, new model options, or both. | [Linear & logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#warm_start),  [DNN](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#warm_start),  [Wide & Deep](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#warm_start),  [Kmeans](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans#warm_start),  [Autoencoder](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder#warm_start) |
| AUTO\_CLASS\_WEIGHTS | Whether to balance class labels using weights for each class in inverse proportion to the frequency of that class. | [Logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#auto_class_weights),  [Boosted tree classifier](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#auto_class_weights),  [Random forest classifier](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#auto_class_weights),  [DNN classifier](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#auto_class_weights),  [Wide & Deep classifier](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#auto_class_weights) |
| CLASS\_WEIGHTS | The weights to use for each class label. This option cannot be specified if AUTO\_CLASS\_WEIGHTS is specified.   It takes an ARRAY of STRUCTs; each STRUCT is a (STRING, FLOAT64) pair representing a class label and the corresponding weight.   A weight must be present for every class label. The weights are not required to add up to one. For example: CLASS\_WEIGHTS = [STRUCT('example\_label', .2)]. | [Logistic regression](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-glm#class_weights),  [Boosted tree classifier](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#class_weights),  [Random forest classifier](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#class_weights),  [DNN classifier](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-dnn-models#class_weights),  [Wide & Deep classifier](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-wnd-models#class_weights) |
| INSTANCE\_WEIGHT\_COL | Identifies the column used to specify the weights for each data point in the training dataset. | [Boosted trees](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-boosted-tree#instance_weight_col),  [Random forest](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-random-forest#instance_weight_col) |
| NUM\_CLUSTERS | The number of clusters to identify in the input data. | [Kmeans](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans#num_clusters) |
| KMEANS\_INIT\_METHOD | The method of initializing the clusters. | [Kmeans](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans#kmeans_init_method) |
| KMEANS\_INIT\_COL | Identifies the column used to initialize the centroids. | [Kmeans](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans#kmeans_init_col) |
| DISTANCE\_TYPE | The type of metric to compute the distance between two points. |  |