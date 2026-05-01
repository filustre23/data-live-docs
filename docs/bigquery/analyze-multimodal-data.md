* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# 在 BigQuery 中分析多模态数据

**预览版**

此功能 受[服务专用条款](https://docs.cloud.google.com/terms/service-terms?hl=zh-cn#1)的约束。 非正式版功能“按原样”提供，且可能仅提供有限支持。
如需了解详情，请参阅[发布阶段说明](https://cloud.google.com/products/?hl=zh-cn#product-launch-stages)。

**注意**：如需就此功能提供反馈或请求支持，请发送邮件至 [bq-objectref-feedback@google.com](mailto:bq-objectref-feedback@google.com)。

本文档介绍了可用于分析多模态数据的 BigQuery 功能。有些功能可在Google Cloud 控制台和 bq 命令行工具中使用，而另一些功能则可通过在 Python 中使用 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-cn) 来使用。您可以将其中许多功能结合使用，以便更轻松地进行多模态数据分析和转换工作流。

借助 BigQuery 的多模态数据功能，您可以执行以下任务：

* 使用 [`ObjectRef`](#objectref_values) 值将非结构化数据集成到标准表中。
* 通过使用 [`ObjectRefRuntime`](#objectrefruntime_values) 值，在分析和转换工作流中使用非结构化数据。
* 通过将 BigQuery ML [生成式 AI 函数](#generative_ai_functions)与 Gemini 模型搭配使用，从多模态数据生成文本、嵌入和标量值。
* 在 BigQuery DataFrames 中[创建多模态 DataFrame](#multimodal_dataframes)。
* 使用 BigQuery DataFrames `Series.BlobAccessor` 方法[转换图片和对 PDF 文件进行分块](#object_transformation_methods)。
* 使用 BigQuery DataFrames [生成式 AI 方法](#generative_ai_methods)根据多模态数据生成文本和嵌入。

如需查看使用 Google Cloud 控制台的分步教程，请参阅[使用 SQL 分析多模态数据](https://docs.cloud.google.com/bigquery/docs/multimodal-data-sql-tutorial?hl=zh-cn)。如需查看有关如何在 Python 中使用 BigQuery DataFrames 的分步教程，请参阅[使用 BigQuery DataFrames 在 Python 中分析多模态数据](https://docs.cloud.google.com/bigquery/docs/multimodal-data-dataframes-tutorial?hl=zh-cn)。

## 优势

BigQuery 的多模态数据功能具有以下优势：

* **可组合性**：您可以使用 `ObjectRef` 值在同一标准表行中存储和管理结构化数据和非结构化数据。例如，您可以将商品的图片与其余商品信息存储在同一行中。您可以使用标准 SQL 函数来创建和更新包含 `ObjectRef` 值的列，还可以创建 `ObjectRef` 值作为对象转换操作的输出。
* **在生成式 AI 提示中使用对象数据**：使用 `ObjectRefRuntime` 值作为生成式 AI 函数的输入。例如，您可以对同一表中的图片和文本数据生成嵌入。对于文本和标量值生成，您还可以在发送给模型的提示中引用多个对象。例如，您可以创建一个提示，让模型比较两张动物图片，然后返回文本，指明这两张图片是否显示了同一种动物。
* **保留块顺序**：您可以对对象进行分块，然后将这些块作为 `ObjectRef` 值的数组存储在标准表列中，以便保留它们的顺序。例如，您可以解析视频中的图片，然后将这些图片存储为 `ObjectRef` 值数组，这样图片就会保持与原始视频中相同的显示顺序。

## `ObjectRef` 个值

`ObjectRef` 值是使用 [`ObjectRef` 格式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-cn#objectref)的 `STRUCT` 值。您可以创建一个使用此格式的 `STRUCT` 或 `ARRAY<STRUCT>` 列，从而在 [BigQuery 标准表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-cn#standard-tables)中存储 Cloud Storage 对象元数据和关联的授权方。授权方值用于标识 BigQuery 用来访问 Cloud Storage 对象的 [Cloud 资源连接](https://docs.cloud.google.com/bigquery/docs/create-cloud-resource-connection?hl=zh-cn)。

当您需要将非结构化数据集成到标准表中时，使用 `ObjectRef` 值。例如，在商品表中，您可以通过添加包含 `ObjectRef` 值的列，将商品图片与其余商品信息存储在同一行中。

使用以下 GoogleSQL 函数创建和更新 `ObjectRef` 值：

* [`OBJ.MAKE_REF`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-cn#objmake_ref)：创建包含 Cloud Storage 对象元数据的 `ObjectRef` 值。
* [`OBJ.FETCH_METADATA`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-cn#objfetch_metadata)：针对部分填充了 `uri` 和 `authorizer` 值的 `ObjectRef` 值提取 Cloud Storage 元数据。

如需了解详情，请参阅[在表架构中指定 `ObjectRef` 列](https://docs.cloud.google.com/bigquery/docs/objectref-columns?hl=zh-cn)。

## `ObjectRefRuntime` 个值

`ObjectRefRuntime` 值是使用 [`ObjectRefRuntime` 架构](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-cn#objectrefruntime)的 `JSON` 值。`ObjectRefRuntime` 值包含用于创建它的 `ObjectRef` 值中的 Cloud Storage 对象元数据、关联的授权方和访问网址。您可以使用访问网址来读取或修改 Cloud Storage 中的对象。

使用 `ObjectRefRuntime` 值可在分析和转换工作流中处理对象数据。`ObjectRefRuntime` 值中的访问网址最多在 6 小时后过期，不过您可以配置更短的过期时间。如果您将 `ObjectRefRuntime` 值作为工作流的一部分持久保存在任何地方，则应定期刷新此数据。如需持久保存对象元数据，请改为存储 `ObjectRef` 值，然后在需要时使用这些值生成 `ObjectRefRuntime` 值。除非 Cloud Storage 中的底层对象已修改，否则无需刷新 `ObjectRef` 值。

使用 [`OBJ.GET_ACCESS_URL` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/objectref_functions?hl=zh-cn#objget_access_url)创建 `ObjectRefRuntime` 值。

## 生成式 AI 函数

将以下生成式 AI 函数与 Gemini 模型搭配使用，根据 `ObjectRefRuntime` 输入生成文本、嵌入和标量值：

* [`AI.GENERATE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate?hl=zh-cn)
* [`AI.GENERATE_TEXT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-text?hl=zh-cn)
* [`AI.GENERATE_TABLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-generate-table?hl=zh-cn)
* [`AI.GENERATE_BOOL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-bool?hl=zh-cn)
* [`AI.GENERATE_DOUBLE`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-double?hl=zh-cn)
* [`AI.GENERATE_INT`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-int?hl=zh-cn)
* [`AI.GENERATE_EMBEDDING`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-cn)
* [`AI.EMBED`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-embed?hl=zh-cn)
* [`AI.SIMILARITY`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-similarity?hl=zh-cn)

## 在 Python 中处理多模态数据

您可以使用 BigQuery DataFrames 类和方法在 Python 中分析多模态数据。

### 多模态 DataFrame

使用以下 [`Session`](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.session.Session?hl=zh-cn) 方法创建一个将结构化数据和非结构化数据集成在一起的多模态 DataFrame：

* [`from_glob_path` 方法](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.session.Session?hl=zh-cn#bigframes_session_Session_from_glob_path)：从 Cloud Storage 存储桶创建多模态 DataFrame。
* [`read_gbq_object_table` 方法](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.session.Session?hl=zh-cn#bigframes_session_Session_read_gbq_object_table)：根据对象表创建多模态 DataFrame。

### 对象转换方法

使用以下 [`Series.BlobAccessor`](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.operations.blob.BlobAccessor?hl=zh-cn) 方法转换对象数据：

* [`pdf_chunk` 方法](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.operations.blob.BlobAccessor?hl=zh-cn#bigframes_operations_blob_BlobAccessor_pdf_chunk)：从多模态 DataFrame 中对 PDF 对象进行分块。
* 以下方法可用于转换多模态 DataFrame 中的图片对象：

  + [`image_blur`](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.operations.blob.BlobAccessor?hl=zh-cn#bigframes_operations_blob_BlobAccessor_image_blur)
  + [`image_normalize`](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.operations.blob.BlobAccessor?hl=zh-cn#bigframes_operations_blob_BlobAccessor_image_normalize)
  + [`image_resize`](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.operations.blob.BlobAccessor?hl=zh-cn#bigframes_operations_blob_BlobAccessor_image_resize)

### 生成式 AI 方法

使用以下方法可对多模态数据执行生成式 AI 任务：

* [`GeminiTextGenerator` 类](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.GeminiTextGenerator?hl=zh-cn)的 [`predict` 方法](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.GeminiTextGenerator?hl=zh-cn#bigframes_ml_llm_GeminiTextGenerator_predict)：根据多模态数据生成文本。
* [`MultimodalEmbeddingGenerator` 类](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.MultimodalEmbeddingGenerator?hl=zh-cn)的 [`predict` 方法](https://docs.cloud.google.com/python/docs/reference/bigframes/latest/bigframes.ml.llm.MultimodalEmbeddingGenerator?hl=zh-cn#bigframes_ml_llm_MultimodalEmbeddingGenerator_predict)：根据多模态数据生成嵌入。

## 对象表

如果您在多模数据预览的许可名单中，那么您创建的任何新[对象表](https://docs.cloud.google.com/bigquery/docs/object-table-introduction?hl=zh-cn)都会包含一个 `ref` 列，其中包含给定对象的 `ObjectRef` 值。用于创建对象表的连接用于填充 `ref` 列中的 `authorizer` 值。您可以使用 `ref` 列在标准表中填充和刷新 `ObjectRef` 值。

## 限制

以下限制适用于 BigQuery 多模态数据功能：

* 您必须在包含 `ObjectRef` 值的表的同一项目中运行引用 `ObjectRef` 值的任何查询。
* 在运行引用 `ObjectRef` 或 `ObjectRefRuntime` 值的查询的项目和区域中，连接数不得超过 20 个。例如，如果您在 `myproject` 中运行 `asia-east1` 中的查询，那么您在 `myproject` 中不能有超过 20 个 `asia-east1` 连接。

## 费用

使用多模态数据时，会产生以下费用：

* 在标准表中将对象元数据存储为 `ObjectRef` 值会增加相应表的 BigQuery 存储费用。
* 对 `ObjectRef` 值运行的查询会产生 BigQuery 计算费用。
* 通过对象转换创建的新对象会产生 Cloud Storage 费用。
* 您在 BigQuery 中创建并保留的新数据会产生 BigQuery 存储费用。
* 使用生成式 AI 函数会产生 Vertex AI 费用。
* 使用 BigQuery Python UDF 以及 BigQuery DataFrames 中的多模态 DataFrame 和对象转换方法会产生 Python UDF 费用。

如需了解详情，请参阅以下价格页面：

* [BigQuery 价格](https://cloud.google.com/bigquery/pricing?hl=zh-cn)
* [BigQuery Python UDF 价格](https://docs.cloud.google.com/bigquery/docs/user-defined-functions-python?hl=zh-cn#pricing)
* [Vertex AI 价格](https://docs.cloud.google.com/vertex-ai/generative-ai/pricing?hl=zh-cn)
* [Cloud Storage 价格](https://cloud.google.com/storage/pricing?hl=zh-cn)

## 后续步骤

* [在表架构中指定 `ObjectRef` 列](https://docs.cloud.google.com/bigquery/docs/objectref-columns?hl=zh-cn)。
* [使用 SQL 分析多模态数据](https://docs.cloud.google.com/bigquery/docs/multimodal-data-sql-tutorial?hl=zh-cn)。
* [使用 BigQuery DataFrames 在 Python 中分析多模态数据](https://docs.cloud.google.com/bigquery/docs/multimodal-data-dataframes-tutorial?hl=zh-cn)
* 详细了解 [BigQuery ML 中的生成式 AI](https://docs.cloud.google.com/bigquery/docs/generative-ai-overview?hl=zh-cn)。
* 详细了解 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-cn)。




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-17。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-17。"],[],[]]