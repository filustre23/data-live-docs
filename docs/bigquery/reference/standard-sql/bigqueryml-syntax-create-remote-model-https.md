* [Home](https://docs.cloud.google.com/)
* [Documentation](https://docs.cloud.google.com/docs)
* [Data analytics](https://docs.cloud.google.com/docs/data)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs)
* [Reference](https://docs.cloud.google.com/bigquery/quotas)

Send feedback



Stay organized with collections

Save and categorize content based on your preferences.

# The CREATE MODEL statement for remote models over custom models

This document describes the `CREATE MODEL` statement for creating remote models
in BigQuery over custom models deployed to
[Vertex AI](/vertex-ai/docs) by using SQL.
Alternatively, you can use the Google Cloud console user interface to
[create a model by using a UI](/bigquery/docs/create-machine-learning-model-console)
([Preview](https://cloud.google.com/products#product-launch-stages)) instead of constructing the SQL
statement yourself.

After you create a remote model, you can use it with the
[`ML.PREDICT` function](/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict)
to get predictions from the custom model deployed to Vertex AI.

## `CREATE MODEL` syntax

```
{CREATE MODEL | CREATE MODEL IF NOT EXISTS | CREATE OR REPLACE MODEL}
`project_id.dataset.model_name`
[INPUT (field_name field_type)]
[OUTPUT (field_name field_type)]
REMOTE WITH CONNECTION `project_id.region.connection_id`
OPTIONS(ENDPOINT = vertex_ai_https_endpoint);
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

### `INPUT` and `OUTPUT` clauses

You must specify the `INPUT` and `OUTPUT` clauses when you create a remote
model with an HTTPS endpoint over a custom model deployed to
Vertex AI. The `INPUT` clause must contain the fields needed
for the Vertex AI endpoint request, and the `OUTPUT` clause must
contain the fields needed for the Vertex AI endpoint response.

#### Supported data types

You can use the following BigQuery data types in the `INPUT` and
`OUTPUT` clauses:

* [`BOOL`](/bigquery/docs/reference/standard-sql/data-types#boolean_type)
* [`INT64`](/bigquery/docs/reference/standard-sql/data-types#integer_types)
* [`FLOAT64`](/bigquery/docs/reference/standard-sql/data-types#floating_point_types)
* [`NUMERIC`](/bigquery/docs/reference/standard-sql/data-types#decimal_types)
* [`BIGNUMERIC`](/bigquery/docs/reference/standard-sql/data-types#decimal_types)
* [`STRING`](/bigquery/docs/reference/standard-sql/data-types#string_type)
* An [`ARRAY`](/bigquery/docs/reference/standard-sql/data-types#array_type) of
  any of the aforementioned types.

#### Field name format

The `INPUT` and `OUTPUT` field names must be identical as the field names of
the Vertex AI endpoint request and response. For a Vertex AI
endpoint with a single `OUTPUT`, there is no field name in the response, and
therefore you can specify any field name in the `OUTPUT` statement.

**Example**

If the Vertex AI request looks like the following example:

```
{
  "instances": [
    { "f1": 10, "f2": 12.3, "f3": "abc", "f4": [1, 2, 3, 4] },
    { "f1": 40, "f2": 32.5, "f3": "def", "f4": [11, 12, 13, 14] },
  ]
}
```

The `INPUT` statement must be:

```
INPUT(f1 INT64, f2 FLOAT64, f3 STRING, f4 ARRAY<INT64>)
```

If the Vertex AI response looks like the following example:

```
{
  "predictions": [
    {
      "out1": 300,
      "out2": 40
    },
    {
      "out1": 200,
      "out2": 30
    }
  ]
}
```

The `OUTPUT` statement must be:

```
OUTPUT(out1 INT64, out2 INT64)
```

### `REMOTE WITH CONNECTION`

**Syntax**

```
`[PROJECT_ID].[LOCATION].[CONNECTION_ID]`
```

BigQuery uses a
[Cloud resource connection](/bigquery/docs/create-cloud-resource-connection)
to interact with
the Vertex AI endpoint.

The connection elements are as follows:

* `PROJECT_ID`: the project ID of the project that
  contains the connection.
* `LOCATION`: the [location](/bigquery/docs/locations)
  used by the connection. The connection must be in the same location as the
  dataset that contains the model.
* `CONNECTION_ID`: the connection ID—for
  example, `myconnection`.

  To find your connection ID,
  [view the connection details](/bigquery/docs/working-with-connections#view-connections)
  in the Google Cloud console. The connection ID is the value in the last
  section of the fully qualified connection ID that is shown in
  **Connection ID**—for example
  `projects/myproject/locations/connection_location/connections/myconnection`.

  To use a [default
  connection](/bigquery/docs/default-connections), specify `DEFAULT` instead of the connection string
  containing PROJECT\_ID.LOCATION.CONNECTION\_ID.

If you are creating a remote model over a Vertex AI model that
uses supervised tuning, you need to grant the
[Vertex AI Service Agent role](/vertex-ai/docs/general/access-control#aiplatform.serviceAgent)
to the connection's service account in the project where you create the model.
Otherwise, you need to grant the
[Vertex AI User role](/vertex-ai/docs/general/access-control#aiplatform.user)
to the connection's service account in the project where you create the model.

If you are using the remote model to analyze unstructured data from an
[object table](/bigquery/docs/object-table-introduction), you must also grant the
[Vertex AI Service Agent role](/vertex-ai/docs/general/access-control#aiplatform.serviceAgent)
to the service account of the connection associated with the object table.
You can find the object table's connection in the Google Cloud console, on the
**Details** pane for the object table.

**Example**

```
`myproject.us.my_connection`
```

### `ENDPOINT`

**Syntax**

```
ENDPOINT = vertex_ai_https_endpoint
```

**Description**

For `vertex_ai_https_endpoint`, specify the
[shared public endpoint](/vertex-ai/docs/predictions/choose-endpoint-type)
of a model deployed to Vertex AI, in the format
`https://location-aiplatform.googleapis.com/v1/projects/project/locations/location/endpoints/endpoint_id`.
Dedicated public endpoints, Private Service Connect endpoints, and
private endpoints aren't supported.

To learn more about deploying a model to a shared public endpoint, see
[Create a shared public endpoint](/vertex-ai/docs/predictions/create-public-endpoint#create_a_shared_public_endpoint).

The following example shows how to create a remote model that uses a shared
public endpoint:

```
ENDPOINT = 'https://us-central1-aiplatform.googleapis.com/v1/projects/myproject/locations/us-central1/endpoints/1234'
```

## Locations

For information about supported locations, see
[Locations for remote models](/bigquery/docs/locations#locations-for-remote-models).

## Example

The following example creates a BigQuery ML remote model
over a model deployed to a Vertex AI endpoint:

```
CREATE MODEL `project_id.mydataset.mymodel`
 INPUT(f1 INT64, f2 FLOAT64, f3 STRING, f4 ARRAY)
 OUTPUT(out1 INT64, out2 INT64)
 REMOTE WITH CONNECTION `myproject.us.test_connection`
 OPTIONS(ENDPOINT = 'https://us-central1-aiplatform.googleapis.com/v1/projects/myproject/locations/us-central1/endpoints/1234')
```

## What's next

* Learn how to
  [make predictions with remote models on Vertex AI](/bigquery/docs/bigquery-ml-remote-model-tutorial#create-remote-model).
* For more information about the supported SQL statements and functions for
  remote models that use HTTPS endpoints, see
  [End-to-end user journey for each model](/bigquery/docs/e2e-journey).




Send feedback

Except as otherwise noted, the content of this page is licensed under the [Creative Commons Attribution 4.0 License](https://creativecommons.org/licenses/by/4.0/), and code samples are licensed under the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0). For details, see the [Google Developers Site Policies](https://developers.google.com/site-policies). Java is a registered trademark of Oracle and/or its affiliates.

Last updated 2026-05-05 UTC.




Need to tell us more?

[[["Easy to understand","easyToUnderstand","thumb-up"],["Solved my problem","solvedMyProblem","thumb-up"],["Other","otherUp","thumb-up"]],[["Hard to understand","hardToUnderstand","thumb-down"],["Incorrect information or sample code","incorrectInformationOrSampleCode","thumb-down"],["Missing the information/samples I need","missingTheInformationSamplesINeed","thumb-down"],["Other","otherDown","thumb-down"]],["Last updated 2026-05-05 UTC."],[],[]]