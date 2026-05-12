* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The ML.GENERATE\_EMBEDDING function

This document describes the `ML.GENERATE_EMBEDDING` function, which
lets you create [embeddings](#embeddings) that describe an entity—for example,
a piece of text or an image.

The
[`AI.GENERATE_EMBEDDING` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding)
offers the same functionality with simplified column names in the output. For
new queries, we recommend that you use `AI.GENERATE_EMBEDDING` instead.

You can create embeddings for the following types of data:

* Text data from standard tables.
* Visual data that is returned as [`ObjectRefRuntime`](/bigquery/docs/reference/standard-sql/objectref_functions#objectrefruntime)
  values by the
  [`OBJ.GET_ACCESS_URL` function](/bigquery/docs/reference/standard-sql/objectref_functions#objget_access_url).
  You can use
  [`ObjectRef`](/bigquery/docs/work-with-objectref)
  values from standard tables as input to the `OBJ.GET_ACCESS_URL` function.
* Visual data in [object tables](/bigquery/docs/object-table-introduction).
* Combinations of unstructured data, including text, images, audio, video, and
  PDFs, represented by a `STRUCT` that contains
  `STRING`, `ARRAY<STRING>`, `ObjectRef`, and `ARRAY<ObjectRef>` values.
* Output data from
  [PCA](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-pca),
  [autoencoder](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-autoencoder),
  or
  [matrix factorization](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization)
  models.

## Embeddings

Embeddings are high-dimensional numerical vectors that represent a given entity.
Machine learning (ML) models use embeddings to encode semantics about entities
to make it easier to reason about and compare them. If two entities are
semantically similar, then their respective embeddings are located near each
other in the embedding vector space.

Embeddings help you perform the following tasks:

* **Semantic search**: search entities ranked by semantic similarity.
* **Recommendation**: return entities with attributes similar to a given
  entity.
* **Classification**: return the class of entities whose attributes are
  similar to the given entity.
* **Clustering**: cluster entities whose attributes are similar to a given
  entity.
* **Outlier detection**: return entities whose attributes are least related to
  the given entity.
* **Matrix factorization**: return entities that
  represent the underlying weights that a model uses during prediction.
* **Principal component analysis (PCA)**: return entities
  (principal components) that represent the input data
  in such a way that it is easier to identify patterns, clusters, and outliers.
* **Autoencoding**: return
  the latent space representations of the input data.

## Function processing

Depending on the task, the `ML.GENERATE_EMBEDDING` function works in one of the
following ways:

* To generate embeddings from text or visual content,
  `ML.GENERATE_EMBEDDING` sends the request to a BigQuery ML
  [remote model](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model)
  that represents a
  [Vertex AI embedding model](/vertex-ai/generative-ai/docs/models#embeddings-models)
  or a
  [supported open model](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-remote-model-open#supported_open_models),
  and then returns the model's response.

  The `ML.GENERATE_EMBEDDING` function works with the Vertex AI
  model to perform embedding tasks supported by that model. For more information
  on the types of tasks these models can perform, see the following documentation:

  + [Text embedding model use cases](/vertex-ai/generative-ai/docs/embeddings#text-use-cases)
  + [Multimodal embedding model use cases](/vertex-ai/generative-ai/docs/embeddings#multimodal-use-cases)

  Typically, you want to use text embedding models for text-only use cases, and
  use multimodal models for cross-modal search use cases, where embeddings for
  text and visual content are generated in the same semantic space.
* For PCA and autoencoding, `ML.GENERATE_EMBEDDING` processes the request using
  a BigQuery ML PCA or autoencoder model
  [`ML.PREDICT` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict).
  `ML.GENERATE_EMBEDDING` gathers the `ML.PREDICT` output for the model into
  an array and outputs it as the `ml_generate_embedding_result` column.
  Having all of the embeddings in a single column lets you directly use the
  [`VECTOR_SEARCH` function](/bigquery/docs/reference/standard-sql/search_functions#vector_search)
  on the`ML.GENERATE_EMBEDDING` output.
* For matrix factorization, `ML.GENERATE_EMBEDDING` processes the request using
  a BigQuery ML matrix factorization model and the
  [`ML.WEIGHTS` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-weights).
  `ML.GENERATE_EMBEDDING` gathers the `factor_weights.weight` and `intercept`
  values from the `ML.WEIGHTS` output for the model into
  an array and outputs it as the `ml_generate_embedding_result` column.
  Having all of the embeddings in a single column lets you directly use the
  [`VECTOR_SEARCH` function](/bigquery/docs/reference/standard-sql/search_functions#vector_search)
  on the`ML.GENERATE_EMBEDDING` output.

## Syntax

`ML.GENERATE_EMBEDDING` syntax differs depending on the
BigQuery ML model you choose. If you use a remote model, it also
differs depending on the Vertex AI model that your remote models
targets. Choose the option appropriate for your use case.

### `gemini-embedding-001`

```
ML.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  { TABLE `PROJECT_ID.DATASET.TABLE_NAME` | (QUERY_STATEMENT) },
  STRUCT(
    [FLATTEN_JSON_OUTPUT AS flatten_json_output]
    [, TASK_TYPE AS task_type]
    [, OUTPUT_DIMENSIONALITY AS output_dimensionality])
)
```

### Arguments

`ML.GENERATE_EMBEDDING` takes the following arguments:

* `PROJECT_ID`: the project that contains the
  resource.
* `DATASET`: the BigQuery dataset that
  contains the resource.
* `MODEL_NAME`: the name of
  a remote model over a supported open model.

  You can confirm what LLM is used by the remote model by opening the
  Google Cloud console and looking at the **Remote endpoint** field in
  the model details page.

- `QUERY_STATEMENT`: a query whose result contains a
  `STRING` column that's named `content`. For information about the
  supported SQL syntax of the `QUERY_STATEMENT` clause, see
  [GoogleSQL query
  syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).
- `FLATTEN_JSON_OUTPUT`: a `BOOL` value that
  determines whether the `JSON` content returned by the function is parsed
  into separate columns. The default is `TRUE`.
- `TASK_TYPE`: a `STRING` literal that specifies the
  intended downstream application to help the model produce better quality
  embeddings. The `TASK_TYPE` argument accepts the following values:

  * `RETRIEVAL_QUERY`: specifies that the given text is a query in a
    search or retrieval setting.
  * `RETRIEVAL_DOCUMENT`: specifies that the given text is a document in a
    search or retrieval setting.

    When using this task type, it is helpful to include the document title
    in the query statement in order to improve embedding quality.
    The document title must be in a column either named `title` or
    aliased as `title`, for example:

    ```
    SELECT *
    FROM
    ML.GENERATE_EMBEDDING(
      MODEL `mydataset.embedding_model`,
      (SELECT abstract as content, header as title, publication_number
      FROM `mydataset.publications`),
      STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_DOCUMENT' as task_type)
    );
    ```

    Specifying the title column in the input query populates the
    [`title` field](/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api#request_body)
    of the request body sent to the model.
    If you specify a `title` value when using any other task type, that
    input is ignored and has no effect on the embedding results.
  * `SEMANTIC_SIMILARITY`: specifies that the given text will be used for
    Semantic Textual Similarity (STS).
  * `CLASSIFICATION`: specifies that the embeddings will be used for
    classification.
  * `CLUSTERING`: specifies that the embeddings will be used for
    clustering.
  * `QUESTION_ANSWERING`: specifies that the embeddings will be used for question answering.
  * `FACT_VERIFICATION`: specifies that the embeddings will be used for fact verification.
  * `CODE_RETRIEVAL_QUERY`: specifies that the embeddings will be used for code retrieval.
- `OUTPUT_DIMENSIONALITY`: an `INT64` value in the range
  `[1, 3072]`
  that specifies the number of dimensions to use when generating
  embeddings. For example, if you specify `256 AS output_dimensionality`,
  then the `ml_generate_embedding_result` output column contains 256
  embeddings for each input value.
  The default value is `3072`.

### Details

The model and input table must be in the same region.

### `text-embedding`

```
ML.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  { TABLE `PROJECT_ID.DATASET.TABLE_NAME` | (QUERY_STATEMENT) },
  STRUCT(
    [FLATTEN_JSON_OUTPUT AS flatten_json_output]
    [, TASK_TYPE AS task_type]
    [, OUTPUT_DIMENSIONALITY AS output_dimensionality])
)
```

### Arguments

`ML.GENERATE_EMBEDDING` takes the following arguments:

* `PROJECT_ID`: the project that contains the
  resource.
* `DATASET`: the BigQuery dataset that
  contains the resource.
* `MODEL_NAME`: the name of
  a remote model over a Vertex AI
  text embedding model.

  You can confirm what LLM is used by the remote model by opening the
  Google Cloud console and looking at the **Remote endpoint** field in
  the model details page.
* `TABLE_NAME`: the name of the
  BigQuery table that contains a `STRING` column to embed.
  The text in the column that's named `content` is sent to the model. If
  your table doesn't have a `content` column, use a `SELECT` statement for
  this argument to provide an alias for an existing table column. An error
  occurs if no `content` column exists.

- `QUERY_STATEMENT`: a query whose result contains a
  `STRING` column that's named `content`. For information about the
  supported SQL syntax of the `QUERY_STATEMENT` clause, see
  [GoogleSQL query
  syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).
- `FLATTEN_JSON_OUTPUT`: a `BOOL` value that
  determines whether the `JSON` content returned by the function is parsed
  into separate columns. The default is `TRUE`.
- `TASK_TYPE`: a `STRING` literal that specifies the
  intended downstream application to help the model produce better quality
  embeddings. The `TASK_TYPE` argument accepts the following values:

  * `RETRIEVAL_QUERY`: specifies that the given text is a query in a
    search or retrieval setting.
  * `RETRIEVAL_DOCUMENT`: specifies that the given text is a document in a
    search or retrieval setting.

    When using this task type, it is helpful to include the document title
    in the query statement in order to improve embedding quality.
    The document title must be in a column either named `title` or
    aliased as `title`, for example:

    ```
    SELECT *
    FROM
    ML.GENERATE_EMBEDDING(
      MODEL `mydataset.embedding_model`,
      (SELECT abstract as content, header as title, publication_number
      FROM `mydataset.publications`),
      STRUCT(TRUE AS flatten_json_output, 'RETRIEVAL_DOCUMENT' as task_type)
    );
    ```

    Specifying the title column in the input query populates the
    [`title` field](/vertex-ai/generative-ai/docs/model-reference/text-embeddings-api#request_body)
    of the request body sent to the model.
    If you specify a `title` value when using any other task type, that
    input is ignored and has no effect on the embedding results.
  * `SEMANTIC_SIMILARITY`: specifies that the given text will be used for
    Semantic Textual Similarity (STS).
  * `CLASSIFICATION`: specifies that the embeddings will be used for
    classification.
  * `CLUSTERING`: specifies that the embeddings will be used for
    clustering.
  * `QUESTION_ANSWERING`: specifies that the embeddings will be used for question answering.
  * `FACT_VERIFICATION`: specifies that the embeddings will be used for fact verification.
  * `CODE_RETRIEVAL_QUERY`: specifies that the embeddings will be used for code retrieval.
- `OUTPUT_DIMENSIONALITY`: an `INT64` value in the range
  `[1, 768]`
  that specifies the number of dimensions to use when generating
  embeddings. For example, if you specify `256 AS output_dimensionality`,
  then the `ml_generate_embedding_result` output column contains 256
  embeddings for each input value.
  The default value is `768`.

### Details

The model and input table must be in the same region.

### Open models

```
ML.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  { TABLE `PROJECT_ID.DATASET.TABLE_NAME` | (QUERY_STATEMENT) },
  STRUCT([FLATTEN_JSON_OUTPUT AS flatten_json_output])
)
```

### Arguments

`ML.GENERATE_EMBEDDING` takes the following arguments:

* `PROJECT_ID`: the project that contains the
  resource.
* `DATASET`: the BigQuery dataset that
  contains the resource.
* `MODEL_NAME`: the name of
  a remote model over a supported open model.

  You can confirm the type of model by opening the Google Cloud console
  and looking at the **Model type** field in the model details page.
* `TABLE_NAME`: the name of the
  BigQuery table that contains a `STRING` column to embed.
  The text in the column that's named `content` is sent to the model. If
  your table doesn't have a `content` column, use a `SELECT` statement for
  this argument to provide an alias for an existing table column. An error
  occurs if no `content` column exists.

- `QUERY_STATEMENT`: a query whose result contains a
  `STRING` column that's named `content`. For information about the
  supported SQL syntax of the `QUERY_STATEMENT` clause, see
  [GoogleSQL query
  syntax](/bigquery/docs/reference/standard-sql/query-syntax#sql_syntax).
- `FLATTEN_JSON_OUTPUT`: a `BOOL` value that
  determines whether the `JSON` content returned by the function is parsed
  into separate columns. The default is `TRUE`.

### Details

The model and input table must be in the same region.

### Multimodal embedding

```
# Syntax for standard tables
ML.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  { TABLE `PROJECT_ID.DATASET.TABLE_NAME` | (QUERY_STATEMENT) },
  STRUCT(
    [FLATTEN_JSON_OUTPUT AS flatten_json_output]
    [, OUTPUT_DIMENSIONALITY AS output_dimensionality])
)
```

```
# Syntax for object tables
ML.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  { TABLE `PROJECT_ID.DATASET.TABLE_NAME` | (QUERY_STATEMENT) },
  STRUCT(
    [FLATTEN_JSON_OUTPUT AS flatten_json_output]
    [, START_SECOND AS start_second]
    [, END_SECOND AS end_second]
    [, INTERVAL_SECONDS AS interval_seconds]
    [, OUTPUT_DIMENSIONALITY AS output_dimensionality])
)
```

### Arguments

`ML.GENERATE_EMBEDDING` takes the following arguments:

* `PROJECT_ID`: the project that contains the
  resource.
* `DATASET`: the BigQuery dataset that
  contains the resource.
* `MODEL_NAME`: the name of
  a remote model over a Vertex AI model.
  Supported models include `multimodalembedding@001` and
  `gemini-embedding-2-preview`
  ([Preview](https://cloud.google.com/products#product-launch-stages)).

  You can confirm what LLM is used by the remote model by opening the
  Google Cloud console and looking at the **Remote endpoint** field in
  the model details page.
* `TABLE_NAME`: one of the following:

  + If you are creating embeddings for text in
    a standard table, the name of the BigQuery table
    that contains the content. The content must be in a `STRING`
    column named `content`. If your table does not have a
    `content` column, use the `QUERY_STATEMENT` argument instead and
    provide a `SELECT` statement that includes an alias for an existing
    table column. An error occurs if no `content` column is available.
  + If you are creating embeddings for visual content using data from an
    object table, the name of a BigQuery
    [object table](/bigquery/docs/object-table-introduction) that
    contains the visual content.
  + If you use the `gemini-embedding-2-preview` model
    ([Preview](https://cloud.google.com/products#product-launch-stages)),
    you can also specify a `STRUCT` column that contains a
    combination of `STRING`, `ARRAY<STRING>`, `ObjectRef`,
    and `ARRAY<ObjectRef>` values.
* `QUERY_STATEMENT`: the GoogleSQL query
  that generates the input data for the function.

  + If you are creating embeddings from a standard table, the query must
    produce a column named `content`, which you can generate as follows:

    - For text embeddings, you can pull the value from a `STRING`
      column, or you can specify a string literal in the query.
    - For visual content embeddings, you can provide an
      [`ObjectRefRuntime`](/bigquery/docs/reference/standard-sql/objectref_functions#objectrefruntime)
      value for the `content` column. You can generate
      `ObjectRefRuntime` values by using the
      [`OBJ.GET_ACCESS_URL` function](/bigquery/docs/reference/standard-sql/objectref_functions#objget_access_url).
      The `OBJ.GET_ACCESS_URL` function takes an
      [`ObjectRef`](/bigquery/docs/analyze-multimodal-data#objectref_values)
      value as input, which you can provide by either specifying
      the name of a column that contains `ObjectRef` values, or by
      constructing an `ObjectRef` value.

      `ObjectRefRuntime` values must have the `access_url.read_url` and
      `details.gcs_metadata.content_type` elements of the JSON value
      populated.
  + If you are creating embeddings from an object table, the query doesn't
    have to return a `content` column. You can only specify `WHERE`,
    `ORDER BY`, and `LIMIT` clauses in the query.
* `FLATTEN_JSON_OUTPUT`: a `BOOL` value that
  determines whether the `JSON` content returned by the function is parsed
  into separate columns. The default is `TRUE`.
* `START_SECOND`: a `FLOAT64` value that specifies the
  second in the video
  at which to start the embedding. The default value is `0`.
  If you specify this argument, you must
  also specify the `END_SECOND` argument. This value must be positive and
  less than the `END_SECOND` value. This argument only applies to video
  content.
* `END_SECOND`: a `FLOAT64` value that specifies the
  second in the video at which to end the embedding. The `END_SECOND` value
  can't be higher than `120`. The default value is `120`. If you specify
  this argument, you must also specify the `START_SECOND` argument. This
  value must be positive and greater than the `START_SECOND` value. This
  argument only applies to video content.
* `INTERVAL_SECONDS`: a `FLOAT64` value that specifies
  the interval to use when creating embeddings. For example, if you set
  `START_SECOND` = `0`, `END_SECOND` = `120`, and `INTERVAL_SECONDS` = `10`,
  then the video is split into twelve 10 second segments (`[0, 10), [10,
  20), [20, 30)...`) and embeddings are generated for each segment. This
  value must be greater than
  or equal to `4` and less than `120`. The default value is `16`.
  This argument only applies to video content.
* `OUTPUT_DIMENSIONALITY`: an `INT64` value that
  specifies the number of dimensions to use when generating embeddings.
  For more information, see how to
  [specify lower-dimensional embeddings](/vertex-ai/generative-ai/docs/embeddings/get-multimodal-embeddings#low-dimension).

  You can only use this argument when creating text or image embeddings.
  If you use this argument when creating video embeddings, the function
  returns an error.

### Details

The model and input table must be in the same region.

### PCA

```
ML.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  { TABLE `PROJECT_ID.DATASET.TABLE_NAME` | (QUERY_STATEMENT) }
)
```

### Arguments

`ML.GENERATE_EMBEDDING` takes the following arguments:

* `PROJECT_ID`: the project that contains the
  resource.
* `DATASET`: the BigQuery dataset that
  contains the resource.
* `MODEL_NAME`: the name of
  a PCA model.

  You can confirm the type of model by opening the Google Cloud console
  and looking at the **Model type** field in the model details page.
* `TABLE_NAME`: the name of the
  BigQuery table that contains the input data for the PCA
  model.

- `QUERY_STATEMENT`: a query whose result contains the
  input data for the PCA model.

### Details

The model and input table must be in the same region.

### Autoencoder

```
ML.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  { TABLE `PROJECT_ID.DATASET.TABLE_NAME` | (QUERY_STATEMENT) },
  STRUCT([TRIAL_ID AS trial_id])
)
```

### Arguments

`ML.GENERATE_EMBEDDING` takes the following arguments:

* `PROJECT_ID`: the project that contains the
  resource.
* `DATASET`: the BigQuery dataset that
  contains the resource.
* `MODEL_NAME`: the name of
  an autoencoder model.

  You can confirm the type of model by opening the Google Cloud console
  and looking at the **Model type** field in the model details page.
* `TABLE_NAME`: the name of the
  BigQuery table that contains the input data for the
  autoencoder model.

- `QUERY_STATEMENT`: a query whose result contains the
  input data for the autoencoder model.
- `TRIAL_ID`: an `INT64` value that identifies the
  hyperparameter tuning trial that you want the function to evaluate. The
  function uses the optimal trial by default. Only specify this argument if
  you ran hyperparameter tuning when creating the model.

### Details

The model and input table must be in the same region.

### Matrix factorization

```
ML.GENERATE_EMBEDDING(
  MODEL `PROJECT_ID.DATASET.MODEL_NAME`,
  STRUCT([TRIAL_ID AS trial_id])
)
```

### Arguments

`ML.GENERATE_EMBEDDING` takes the following arguments:

* `PROJECT_ID`: the project that contains the
  resource.
* `DATASET`: the BigQuery dataset that
  contains the resource.
* `MODEL_NAME`: the name of
  a matrix factorization model.

  You can confirm the type of model by opening the Google Cloud console
  and looking at the **Model type** field in the model details page.

- `TRIAL_ID`: an `INT64` value that identifies the
  hyperparameter tuning trial that you want the function to evaluate. The
  function uses the optimal trial by default. Only specify this argument if
  you ran hyperparameter tuning when creating the model.

## Output

### `gemini-embedding-001`

`ML.GENERATE_EMBEDDING` returns the input table and the following columns:

* `ml_generate_embedding_result`:

  + If `flatten_json_output` is `FALSE`, this is the
    [JSON response](/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints/predict#response-body)
    from the [`projects.locations.endpoints.predict`](/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints/predict) call to the model. The
    generated embeddings are in the `values` element.
  + If `flatten_json_output` is `TRUE`, this is an `ARRAY<FLOAT64>`
    value that contains the generated embeddings.
* `ml_generate_embedding_statistics`: a `JSON` value that contains a
  `token_count` field with the number of tokens in the content, and a
  `truncated` field that indicates whether the content was truncated. This
  column is returned when `flatten_json_output` is `TRUE`.
* `ml_generate_embedding_status`: a `STRING` value that contains the API
  response status for the corresponding row. This value is empty if the
  operation was successful.

### `text-embedding`

`ML.GENERATE_EMBEDDING` returns the input table and the following columns:

* `ml_generate_embedding_result`:

  + If `flatten_json_output` is `FALSE`, this is the
    [JSON response](/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints/predict#response-body)
    from the [`projects.locations.endpoints.predict`](/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints/predict) call to the model. The
    generated embeddings are in the `values` element.
  + If `flatten_json_output` is `TRUE`, this is an `ARRAY<FLOAT64>`
    value that contains the generated embeddings.
* `ml_generate_embedding_statistics`: a `JSON` value that contains a
  `token_count` field with the number of tokens in the content, and a
  `truncated` field that indicates whether the content was truncated. This
  column is returned when `flatten_json_output` is `TRUE`.
* `ml_generate_embedding_status`: a `STRING` value that contains the API
  response status for the corresponding row. This value is empty if the
  operation was successful.

### Open models

`ML.GENERATE_EMBEDDING` returns the input table and the following columns:

* `ml_generate_embedding_result`:

  + If `flatten_json_output` is `FALSE`, this is the
    [JSON response](/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints/predict#response-body)
    from the [`projects.locations.endpoints.predict`](/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints/predict) call to the model. The
    generated embeddings are in the first element of the `predictions`
    array.
  + If `flatten_json_output` is `TRUE`, this is an `ARRAY<FLOAT64>`
    value that contains the generated embeddings.
* `ml_generate_embedding_status`: a `STRING` value that contains the API
  response status for the corresponding row. This value is empty if the
  operation was successful.

### Multimodal embedding

`ML.GENERATE_EMBEDDING` returns the input table and the following columns:

* `ml_generate_embedding_result`:

  + If `flatten_json_output` is `FALSE`, this is the
    [JSON response](/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints/predict#response-body)
    from the [`projects.locations.endpoints.predict`](/vertex-ai/docs/reference/rest/v1/projects.locations.endpoints/predict) call to the model. The
    generated embeddings are in the `textEmbedding`, `imageEmbedding`, or `videoEmbeddings`
    element, depending on the type of input data you
    used.
  + If `flatten_json_output` is `TRUE`, this is an `ARRAY<FLOAT64>`
    value that contains the generated embeddings.
* `ml_generate_embedding_status`: a `STRING` value that contains the API
  response status for the corresponding row. This value is empty if the
  operation was successful.
* Additional output fields depend on which embedding model you use:

  + The `gemini-embedding-2-preview` model also outputs the following
    field:

    - `ml_generate_embedding_statistics`: a `JSON` value that contains
      information about the token count for each modality of input that
      you provide.
  + The `multimodalembedding@001` model also outputs the following fields:

    - `ml_generate_embedding_start_sec`: for video content, an `INT64` value
      that contains the starting second of the portion of the video that the
      embedding represents. For image content, the value is `NULL`.
      This column isn't returned for text content.
    - `ml_generate_embedding_end_sec`: for video content, an `INT64` value
      that contains the ending second of the portion of the video that the
      embedding represents. For image content, the value is `NULL`.
      This column isn't returned for text content.

### PCA

`ML.GENERATE_EMBEDDING` returns the input table and the following column:

* `ml_generate_embedding_result`: this is an `ARRAY<FLOAT>` value that
  contains the principal components for the input data. The number of array
  dimensions is equal to the P