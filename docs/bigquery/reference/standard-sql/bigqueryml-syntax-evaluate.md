* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.EVALUATE function

This document describes the `ML.EVALUATE` function, which lets you
evaluate model metrics.

## Supported models

You can use the `ML.EVALUATE` function with all model types except for the
following:

* [Imported TensorFlow models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-tensorflow)
* [Remote models over Cloud AI services](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-service)
* [Remote models over embedding models](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model)

## Syntax

The `ML.EVALUATE` function syntax differs depending on the type of model that
you use the function with. Choose the option appropriate for your use case.

### Times series

```
ML.EVALUATE(
  MODEL `PROJECT_ID.DATASET.MODEL`
  [, { TABLE `PROJECT_ID.DATASET.TABLE` | (QUERY_STATEMENT) }],
    STRUCT(
      [PERFORM_AGGREGATION AS perform_aggregation]
      [, HORIZON AS horizon]
      [, CONFIDENCE_LEVEL AS confidence_level])
)
```

### Arguments

`ML.EVALUATE` takes the following arguments:

* `PROJECT_ID`: the project that contains the resource.
* `DATASET`: the project that contains the resource.
* `MODEL`: the name of the model.
* `TABLE`: the name of the input table that contains the evaluation data.

  If you don't specify a table or query to provide input data, the
  evaluation metrics that are generated for the model during training are
  returned.

  If you specify a `TABLE` value, the input column names in the table must
  match the column names in the model, and their types must be compatible
  according to BigQuery
  [implicit coercion rules](/bigquery/docs/reference/standard-sql/conversion_rules#coercion).
* `QUERY_STATEMENT`: a GoogleSQL query that
  is used to generate the evaluation data. For the supported SQL syntax of
  the `QUERY_STATEMENT` clause in
  GoogleSQL, see
  [Query syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).

  If you don't specify a table or query to provide input data, the
  evaluation metrics that are generated for the model during training
  are returned.

  If you used the
  [`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform)
  in the `CREATE MODEL` statement that created the model, then you can
  only specify the input columns present in the `TRANSFORM` clause
  in the query.

* `PERFORM_AGGREGATION`: a `BOOL` value that
  indicates the level of evaluation for forecasting accuracy. If you specify
  `TRUE`, then the forecasting accuracy is on the time series level. If you
  specify `FALSE`, the forecasting accuracy is on the timestamp level.
  The default value is `TRUE`.
* `HORIZON`: an `INT64` value that specifies the
  number of forecasted time points against which the evaluation metrics are
  computed. The default value is the horizon value specified in the
  [`CREATE MODEL`](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series)
  statement for the time series model, or `1000` if unspecified. When
  evaluating multiple time series at the same time, this parameter applies
  to each time series.

  You can only use the `HORIZON` argument
  when the following conditions are met:

  + The model type is `ARIMA_PLUS`.
  + You have specified a value for either the
    `TABLE` or
    `QUERY_STATEMENT` argument.
* `CONFIDENCE_LEVEL`: a `FLOAT64` value that
  specifies the percentage of the future values that fall in the
  prediction interval. The default value is `0.95`. The valid input
  range is `[0, 1)`.

  You can only use the `CONFIDENCE_LEVEL` argument
  when the following conditions are met:

  + The model type is `ARIMA_PLUS`.
  + You have specified a value for either the
    `TABLE` or
    `QUERY_STATEMENT` argument.
  + The `PERFORM_AGGREGATION` argument value is
    `FALSE`.

    The value of the `CONFIDENCE_LEVEL` argument
    affects the `upper_bound` and `lower_bound` values in the output.

**Note:**

For `ARIMA_PLUS` and `ARIMA_PLUS_XREG` models, the output columns differ
depending on whether the input data is provided or not. If no input data
is provided, use `ML.ARIMA_EVALUATE` instead. The support of `ML.EVALUATE`
without input data is deprecated.

### Classification & regression

```
ML.EVALUATE(
  MODEL `PROJECT_ID.DATASET.MODEL`
  [, { TABLE `PROJECT_ID.DATASET.TABLE` | (QUERY_STATEMENT) }],
    STRUCT(
      [THRESHOLD AS threshold]
      [, TRIAL_ID AS trial_id])
)
```

### Arguments

`ML.EVALUATE` takes the following arguments:

* `PROJECT_ID`: the project that contains the resource.
* `DATASET`: the project that contains the resource.
* `MODEL`: the name of the model.
* `TABLE`: the name of the input table that contains the evaluation data.

  If you don't specify a table or query to provide input data, the
  evaluation metrics that are generated for the model during training are
  returned.

  If you specify a `TABLE` value, the input column names in the table must
  match the column names in the model, and their types must be compatible
  according to BigQuery
  [implicit coercion rules](/bigquery/docs/reference/standard-sql/conversion_rules#coercion).

  The table must have a
  column that matches the label column name that is provided during
  model training. You can provide this value by using the
  `input_label_cols` option during model training. If `input_label_cols`
  is unspecified, the column named `label` in the training data is used.
* `QUERY_STATEMENT`: a GoogleSQL query that
  is used to generate the evaluation data. For the supported SQL syntax of
  the `QUERY_STATEMENT` clause in
  GoogleSQL, see
  [Query syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).

  If you don't specify a table or query to provide input data, the
  evaluation metrics that are generated for the model during training
  are returned.

  If you used the
  [`TRANSFORM` clause](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create#transform)
  in the `CREATE MODEL` statement that created the model, then you can
  only specify the input columns present in the `TRANSFORM` clause
  in the query.

  The query must have a
  column that matches the label column name that is provided during
  model training. You can provide this value by using the
  `input_label_cols` option during model training. If `input_label_cols`
  is unspecified, the column named `label` in the training data is used.

* `THRESHOLD`: a `FLOAT64` value that specifies
  a custom threshold for the evaluation. You can only use the
  `THRESHOLD` argument with binary-class
  classification models. The default value is `0.5`.

  A `0` value for precision or recall means that the selected threshold
  produced no true positive labels. A `NaN` value for precision means
  that the selected threshold produced no positive labels, neither true
  positives nor false positives.

  You must specify a value for either the
  `TABLE` or
  `QUERY_STATEMENT` argument in order to specify
  a threshold.

* `TRIAL_ID`: an `INT64` value that identifies the
  hyperparameter tuning trial that you want the function to evaluate. The
  `ML.EVALUATE` function uses the optimal trial by default. Only specify
  this argument if you ran hyperparameter tuning when creating the model.

### Remote over Gemini

```
ML.EVALUATE(
  MODEL `PROJECT_ID.DATASET.MODEL`
  [, { TABLE `PROJECT_ID.DATASET.TABLE` | (QUERY_STATEMENT) }],
    STRUCT(
      [TASK_TYPE AS task_type]
      [, MAX_OUTPUT_TOKENS AS max_output_tokens]
      [, TEMPERATURE AS temperature]
      [, TOP_P AS top_k])
)
```

### Arguments

`ML.EVALUATE` takes the following arguments:

* `PROJECT_ID`: the project that contains the resource.
* `DATASET`: the project that contains the resource.
* `MODEL`: the name of the model.
* `TABLE`: the name of the input table that contains the evaluation data.

  If you don't specify a table or query to provide input data, the
  evaluation metrics that are generated for the model during training are
  returned.

  If the remote model isn't configured to use
  [supervised tuning](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned#supervised_tuning),
  the following column naming requirements apply:

  + The table must have a column named `input_text` that contains the
    prompt text to use when evaluating the model.
  + The table must have a column named `output_text` that contains the
    generated text that you would expect to be returned by the model.

  If the remote model is configured to use supervised tuning,
  the following column naming requirements apply:

  + The table must have a column whose name matches the prompt column
    name that is provided during model training. You can provide this
    value by using the `prompt_col` option during model training. If
    `prompt_col` is unspecified, the column named `prompt` in the
    training data is used. An error is returned if there is no column
    named `prompt`.
  + The table must have a column whose name matches the label column
    name that is provided during model training. You can provide this
    value by using the `input_label_cols` option during model training.
    If `input_label_cols` is unspecified, the column named `label` in
    the training data is used. An error is returned if there is no
    column named `label`.

    You can find information about the label and prompt columns by
    looking at the model schema information in the Google Cloud console.

  For more information, see
  [`AS SELECT`](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned#as_select).
* `QUERY_STATEMENT`: a GoogleSQL query that
  is used to generate the evaluation data. For the supported SQL syntax of
  the `QUERY_STATEMENT` clause in
  GoogleSQL, see
  [Query syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).

  If you don't specify a table or query to provide input data, the
  evaluation metrics that are generated for the model during training
  are returned.

  If the remote model isn't configured to use
  [supervised tuning](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned#supervised_tuning),
  the following column naming requirements apply:

  + The query must have a column named `input_text` that contains the
    prompt text to use when evaluating the model.
  + The query must have a column named `output_text` that contains the
    generated text that you would expect to be returned by the model.

  If the remote model is configured to use supervised tuning,
  the following column naming requirements apply:

  + The query must have a column whose name matches the prompt column
    name that is provided during model training. You can provide this
    value by using the `prompt_col` option during model training. If
    `prompt_col` is unspecified, the column named `prompt` in the
    training data is used. An error is returned if there is no column
    named `prompt`.
  + The query must have a column whose name matches the label column
    name that is provided during model training. You can provide this
    value by using the `input_label_cols` option during model training.
    If `input_label_cols` is unspecified, the column named `label` in
    the training data is used. An error is returned if there is no
    column named `label`.

    You can find information about the label and prompt columns by
    looking at the model schema information in the Google Cloud console.

  For more information, see
  [`AS SELECT`](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-tuned#as_select).

* `TASK_TYPE`: a `STRING` value that specifies the
  type of task for which you want to evaluate the model's performance. The
  valid options are the following:

  + `TEXT_GENERATION`
  + `CLASSIFICATION`
  + `SUMMARIZATION`
  + `QUESTION_ANSWERING`

  The default value is `TEXT_GENERATION`.

* `MAX_OUTPUT_TOKENS`: an `INT64` value that sets
  the maximum number of tokens output by the model. Specify a lower value
  for shorter responses and a higher value for longer responses.
  A token might be smaller than a word and is approximately four characters.
  100 tokens correspond to approximately 60-80 words.

  The default value is `1024`.

  The `MAX_OUTPUT_TOKENS` value must be in the range
  `[1,8192]`.

* `TEMPERATURE`: a `FLOAT64` value that is used for
  sampling during the response generation. It controls the
  degree of randomness in token selection. Lower
  `TEMPERATURE` values are good for prompts that require a more deterministic
  and less open-ended or creative response, while higher `TEMPERATURE` values
  can lead to more diverse or creative results. A `TEMPERATURE` value of `0` is
  deterministic, meaning that the highest probability response is always
  selected.

  The `TEMPERATURE` value must be in the range
  `[0.0,1.0]`.

  The default value is `1.0`.

* `TOP_P`: a `FLOAT64` value in the range `[0.0,1.0]`
  that changes how the model selects tokens for output. Tokens are selected
  from the most to least probable until the sum of their probabilities
  equals the `TOP_P` value. For example, if tokens A,
  B, and C have a probability of `0.3`, `0.2`, and `0.1` and the
  `TOP_P` value is `0.5`, then the model selects
  either A or B as the next token by using the
  `TEMPERATURE` value and doesn't consider C. Specify
  a lower value for less random responses and a higher value for more random
  responses.

  The default value is `0.95`.

### Remote over Claude

```
ML.EVALUATE(
  MODEL `PROJECT_ID.DATASET.MODEL`
  [, { TABLE `PROJECT_ID.DATASET.TABLE` | (QUERY_STATEMENT) }],
    STRUCT(
      [TASK_TYPE AS task_type]
      [, MAX_OUTPUT_TOKENS AS max_output_tokens]
      [, TOP_K AS top_k]
      [, TOP_P AS top_k])
)
```

### Arguments

`ML.EVALUATE` takes the following arguments:

* `PROJECT_ID`: the project that contains the resource.
* `DATASET`: the project that contains the resource.
* `MODEL`: the name of the model.
* `TABLE`: the name of the input table that contains the evaluation data.

  If you don't specify a table or query to provide input data, the
  evaluation metrics that are generated for the model during training are
  returned.

  The following column naming requirements apply:

  + The table must have a column named `input_text` that contains the
    prompt text to use when evaluating the model.
  + The table must have a column named `output_text` that contains the
    generated text that you would expect to be returned by the model.
* `QUERY_STATEMENT`: a GoogleSQL query that
  is used to generate the evaluation data. For the supported SQL syntax of
  the `QUERY_STATEMENT` clause in
  GoogleSQL, see
  [Query syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).

  If you don't specify a table or query to provide input data, the
  evaluation metrics that are generated for the model during training
  are returned.

  The following column naming requirements apply:

  + The query must have a column named `input_text` that contains the
    prompt text to use when evaluating the model.
  + The query must have a column named `output_text` that contains the
    generated text that you would expect to be returned by the model.

* `TASK_TYPE`: a `STRING` value that specifies the
  type of task for which you want to evaluate the model's performance. The
  valid options are the following:

  + `TEXT_GENERATION`
  + `CLASSIFICATION`
  + `SUMMARIZATION`
  + `QUESTION_ANSWERING`

  The default value is `TEXT_GENERATION`.

* `MAX_OUTPUT_TOKENS`: an `INT64` value that sets
  the maximum number of tokens output by the model. Specify a lower value
  for shorter responses and a higher value for longer responses.
  A token might be smaller than a word and is approximately four characters.
  100 tokens correspond to approximately 60-80 words.

  The default value is `1024`.

  The `MAX_OUTPUT_TOKENS` value must be in the range
  `[1,4096]`.

* `TOP_K`: an `INT64` value in the range `[1,40]`
  that changes how the model selects tokens for output. Specify a lower
  value for less random responses and a higher value for more random
  responses. The model determines an appropriate value if you don't
  specify one.

  A `TOP_K` value of `1` means the next selected token
  is the most probable among all tokens in the model's vocabulary, while a
  `TOP_K` value of `3` means that the next token is
  selected from among the three most probable tokens by using the
  `TEMPERATURE` value.

  For each token selection step, the `TOP_K` tokens
  with the highest probabilities are sampled. Then tokens are further
  filtered based on the `TOP_P` value, with the final
  token selected using temperature sampling.

* `TOP_P`: a `FLOAT64` value in the range `[0.0,1.0]`
  that changes how the model selects tokens for output. Tokens are selected
  from the most to least probable until the sum of their probabilities
  equals the `TOP_P` value. For example, if tokens A,
  B, and C have a probability of `0.3`, `0.2`, and `0.1` and the
  `TOP_P` value is `0.5`, then the model selects
  either A or B as the next token by using the
  `TEMPERATURE` value and doesn't consider C. Specify
  a lower value for less random responses and a higher value for more random
  responses.

  The model determines an appropriate value if you don't specify one.

### Remote over Llama or Mistral AI

```
ML.EVALUATE(
  MODEL `PROJECT_ID.DATASET.MODEL`
  [, { TABLE `PROJECT_ID.DATASET.TABLE` | (QUERY_STATEMENT) }],
    STRUCT(
      [TASK_TYPE AS task_type]
      [, MAX_OUTPUT_TOKENS AS max_output_tokens]
      [, TEMPERATURE AS temperature]
      [, TOP_P AS top_k])
)
```

### Arguments

`ML.EVALUATE` takes the following arguments:

* `PROJECT_ID`: the project that contains the resource.
* `DATASET`: the project that contains the resource.
* `MODEL`: the name of the model.
* `TABLE`: the name of the input table that contains the evaluation data.

  If you don't specify a table or query to provide input data, the
  evaluation metrics that are generated for the model during training are
  returned.

  The following column naming requirements apply:

  + The table must have a column named `input_text` that contains the
    prompt text to use when evaluating the model.
  + The table must have a column named `output_text` that contains the
    generated text that you would expect to be returned by the model.
* `QUERY_STATEMENT`: a GoogleSQL query that
  is used to generate the evaluation data. For the supported SQL syntax of
  the `QUERY_STATEMENT` clause in
  GoogleSQL, see
  [Query syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).

  If you don't specify a table or query to provide input data, the
  evaluation metrics that are generated for the model during training
  are returned.

  The following column naming requirements apply:

  + The query must have a column named `input_text` that contains the
    prompt text to use when evaluating the model.
  + The query must have a column named `output_text` that contains the
    generated text that you would expect to be returned by the model.

* `TASK_TYPE`: a `STRING` value that specifies the
  type of task for which you want to evaluate the model's performance. The
  valid options are the following:

  + `TEXT_GENERATION`
  + `CLASSIFICATION`
  + `SUMMARIZATION`
  + `QUESTION_ANSWERING`

  The default value is `TEXT_GENERATION`.

* `MAX_OUTPUT_TOKENS`: an `INT64` value that sets
  the maximum number of tokens output by the model. Specify a lower value
  for shorter responses and a higher value for longer responses.
  A token might be smaller than a word and is approximately four characters.
  100 tokens correspond to approximately 60-80 words.

  The default value is `1024`.

  The `MAX_OUTPUT_TOKENS` value must be in the range
  `[1,4096]`.

* `TEMPERATURE`: a `FLOAT64` value that is used for
  sampling during the response generation. It controls the
  degree of randomness in token selection. Lower
  `TEMPERATURE` values are good for prompts that require a more deterministic
  and less open-ended or creative response, while higher `TEMPERATURE` values
  can lead to more diverse or creative results. A `TEMPERATURE` value of `0` is
  deterministic, meaning that the highest probability response is always
  selected.

  The `TEMPERATURE` value must be in the range