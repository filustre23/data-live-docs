Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 支援的輸入特徵類型

BigQuery ML 支援不同模型類型的輸入特徵類型。下表列出支援的輸入特徵類型：

| 模型類別 | [模型類型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw#model_option_list) | [數值型別](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_types) ([INT64](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types)、[NUMERIC](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#decimal_types)、[BIGNUMERIC](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#decimal_types)、[FLOAT64](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#floating_point_types)) | 類別類型 ([BOOL](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#boolean_type)、[STRING](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#string_type)、[BYTES](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#bytes_type)、[DATE](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#date_type)、[DATETIME](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#datetime_type)) | [TIMESTAMP](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#timestamp_type) | [STRUCT](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type) | [GEOGRAPHY](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#geography_type) | [ARRAY](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type)<[數值型別](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_types)> | [ARRAY](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type)<Categorical types> | [ARRAY](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#array_type)<[STRUCT](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#struct_type)<[INT64](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#integer_types), [Numeric types](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_types)>> |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 監督式學習 | 線性與邏輯迴歸 | ✔ | ✔ | ✔ | ✔ |  | ✔ | ✔ | ✔ |
| 深層類神經網路 | ✔ | ✔ |  | ✔ |  | ✔ | ✔ | ✔ |
| 廣度和深度 | ✔ | ✔ |  | ✔ |  | ✔ | ✔ | ✔ |
| 強化型樹狀結構 | ✔ | ✔ |  | ✔ |  | ✔ | ✔ | ✔ |
| AutoML Tables | ✔ | ✔ | ✔ | ✔ |  | ✔ | ✔ |  |
| 非監督式學習 | K-means | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ | ✔ |  |
| PCA | ✔ | ✔ | ✔ | ✔ |  | ✔ | ✔ |  |
| 自動編碼器 | ✔ | ✔ | ✔ | ✔ |  | ✔ | ✔ | ✔ |
| 時間序列模型 | ARIMA\_PLUS\_XREG | ✔ | ✔ | ✔ | ✔ |  |  | ✔ | ✔ |

**注意：** [矩陣分解](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-matrix-factorization?hl=zh-tw#inputs)和 [ARIMA\_PLUS](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-time-series?hl=zh-tw#time_series_data_col) 模型有特殊的輸入特徵類型。[ARIMA\_PLUS\_XREG](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-multivariate-time-series?hl=zh-tw#time_series_data_col) 列出的輸入類型僅適用於外部迴歸因子。

## 稠密型向量輸入

BigQuery ML 支援在模型訓練期間，將 `ARRAY<numeric>` 做為密集向量輸入。嵌入功能是特殊的密集向量類型。詳情請參閱 [`AI.GENERATE_EMBEDDING` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-ai-generate-embedding?hl=zh-tw)。

## 稀疏輸入

BigQuery ML 支援在模型訓練期間，將 `ARRAY<STRUCT>` 做為稀疏輸入。每個結構體都包含代表以零為準索引的 `INT64` 值，以及代表對應值的[數值型別](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#numeric_types)。

以下是整數陣列 `[0,1,0,0,0,0,1]` 的稀疏張量輸入範例：

```
ARRAY<STRUCT<k INT64, v INT64>>[(1, 1), (6, 1)] AS f1
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]