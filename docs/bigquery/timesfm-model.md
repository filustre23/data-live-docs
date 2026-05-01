* [Home](https://docs.cloud.google.com/?hl=zh-cn)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-cn)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-cn)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-cn)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-cn)

发送反馈



使用集合让一切井井有条

根据您的偏好保存内容并对其进行分类。

# TimesFM 模型

本文档介绍了 BigQuery ML 内置的 TimesFM 时序预测模型。

内置 TimesFM 单变量模型是 Google Research 的开源 [TimesFM 模型](https://github.com/google-research/timesfm)的实现。Google 研究 TimesFM 模型是一种时序预测的基础模型，已通过许多真实世界数据集中的数十亿个时间点进行预训练，因此您可以将其应用于许多领域的新预测数据集。所有 BigQuery 支持的区域都提供 TimesFM 模型。

将 BigQuery ML 的内置 TimesFM 模型与 [`AI.FORECAST` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-forecast?hl=zh-cn)搭配使用，您可以执行预测，而无需创建和训练自己的模型，从而避免了模型管理的需求。
TimesFM 模型的预测结果可与 ARIMA 等传统统计方法相媲美。如果您想要比 TimesFM 模型提供的更多模型调优选项，可以创建 [`ARIMA_PLUS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-cn) 或 [`ARIMA_PLUS_XREG`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-cn) 模型，并将其与 [`ML.FORECAST` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-forecast?hl=zh-cn)搭配使用。

如需尝试将 TimesFM 模型与 `AI.FORECAST` 函数搭配使用，请参阅[使用 TimesFM 单变量模型预测多个时序](https://docs.cloud.google.com/bigquery/docs/timesfm-time-series-forecasting-tutorial?hl=zh-cn)。

如需使用 TimesFM 模型检测时序数据中的异常值，请使用 [`AI.DETECT_ANOMALIES` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-detect-anomalies?hl=zh-cn)（[预览版](https://cloud.google.com/products?hl=zh-cn#product-launch-stages)）。

如需根据实际值评估 TimesFM 模型的预测值，请使用 [`AI.EVALUATE` 函数](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-evaluate?hl=zh-cn)。

如需详细了解 Google 研究 TimesFM 模型，请参阅以下资源：

* [Google 研究博客](https://research.google/blog/a-decoder-only-foundation-model-for-time-series-forecasting/?hl=zh-cn)
* [GitHub 代码库](https://github.com/google-research/timesfm)
* [Hugging Face 页面](https://huggingface.co/collections/google/timesfm-release-66e4be5fdb56e960c1e482a6)




发送反馈

如未另行说明，那么本页面中的内容已根据[知识共享署名 4.0 许可](https://creativecommons.org/licenses/by/4.0/)获得了许可，并且代码示例已根据 [Apache 2.0 许可](https://www.apache.org/licenses/LICENSE-2.0)获得了许可。有关详情，请参阅 [Google 开发者网站政策](https://developers.google.com/site-policies?hl=zh-cn)。Java 是 Oracle 和/或其关联公司的注册商标。

最后更新时间 (UTC)：2026-03-28。




需要向我们提供更多信息？

[[["易于理解","easyToUnderstand","thumb-up"],["解决了我的问题","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["很难理解","hardToUnderstand","thumb-down"],["信息或示例代码不正确","incorrectInformationOrSampleCode","thumb-down"],["没有我需要的信息/示例","missingTheInformationSamplesINeed","thumb-down"],["翻译问题","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["最后更新时间 (UTC)：2026-03-28。"],[],[]]