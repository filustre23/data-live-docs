* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery DataFrames 簡介

BigQuery DataFrames 是一組開放原始碼 Python 程式庫，可讓您使用熟悉的 Python API，充分運用 BigQuery 資料處理功能。BigQuery DataFrames 提供由 BigQuery 引擎驅動的 Pythonic DataFrame，並透過 SQL 轉換將處理作業下推至 BigQuery，實作 pandas 和 scikit-learn API。因此您可以使用 BigQuery 探索及處理 TB 級資料，並訓練機器學習 (ML) 模型，所有作業都可透過 Python API 完成。

如果您熟悉 pandas，可以使用 BigQuery DataFrame 處理 BigQuery 資料，且程式碼變更幅度極小。舉例來說，您可以使用熟悉的 pandas 方法分析 BigQuery 資料表中的資料：

```
import bigframes.pandas as bpd

# Load data from BigQuery
query_or_table = "bigquery-public-data.ml_datasets.penguins"
bq_df = bpd.read_gbq(query_or_table)

# Inspect one of the columns (or series) of the DataFrame:
bq_df["body_mass_g"]

# Compute the mean of this series:
average_body_mass = bq_df["body_mass_g"].mean()
print(f"average_body_mass: {average_body_mass}")

# Find the heaviest species using the groupby operation to calculate the
# mean body_mass_g:
(
    bq_df["body_mass_g"]
    .groupby(by=bq_df["species"])
    .mean()
    .sort_values(ascending=False)
    .head(10)
)
```

**注意：** BigQuery DataFrames 2.0 版中的部分預設參數有破壞性變更。如要瞭解這些變更，以及如何遷移至 2.0 版，請參閱「[遷移至 BigQuery DataFrames 2.0](https://docs.cloud.google.com/bigquery/docs/migrate-dataframes?hl=zh-tw)」一文。

## BigQuery DataFrames 的優點

BigQuery DataFrames 的功能如下：

* 透過透明的 SQL 轉換，實作超過 750 個 pandas 和 scikit-learn API，並轉換為 BigQuery 和 BigQuery ML API。
* 延後執行查詢，以提升效能。
* 使用使用者定義的 Python 函式擴充資料轉換作業，以便在 Google Cloud中處理資料。這些函式會自動部署為 BigQuery [遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)。
* 整合 Vertex AI，可使用 Gemini 模型生成文字。

## 授權

BigQuery DataFrames 採用 [Apache-2.0 授權](https://github.com/googleapis/python-bigquery-dataframes/blob/main/LICENSE)發布。

BigQuery DataFrames 也包含衍生自下列第三方套件的程式碼：

* [Ibis](https://ibis-project.org/)
* [pandas](https://pandas.pydata.org/)
* [Python](https://www.python.org/)
* [scikit-learn](https://scikit-learn.org/)
* [XGBoost](https://xgboost.readthedocs.io/en/stable/)

詳情請參閱 BigQuery DataFrames GitHub 存放區中的 [`third_party/bigframes_vendored`](https://github.com/googleapis/python-bigquery-dataframes/tree/main/third_party/bigframes_vendored) 目錄。

## 配額與限制

* [BigQuery 配額](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)適用於 BigQuery DataFrames，包括硬體、軟體和網路元件。
* 支援部分 pandas 和 scikit-learn API。詳情請參閱「[支援的 pandas API](https://dataframes.bigquery.dev/supported_pandas_apis.html)」。
* 您必須明確清除自動建立的 Cloud Run 函式，這是工作階段清理作業的一部分。詳情請參閱「[支援的 pandas API](https://dataframes.bigquery.dev/supported_pandas_apis.html)」。

## 定價

* BigQuery DataFrames 是一組開放原始碼 Python 程式庫，可免費下載。
* BigQuery DataFrames 會使用 BigQuery、Cloud Run functions、Vertex AI 和其他Google Cloud 服務，這些服務會產生各自的費用。
* 在一般使用期間，BigQuery DataFrames 會將中繼結果等臨時資料儲存在 BigQuery 資料表中。根據預設，這些資料表會保留七天，且系統會向您收取儲存在其中的資料費用。資料表會在您於 [`bf.options.bigquery.project` 選項](https://dataframes.bigquery.dev/reference/api/bigframes._config.BigQueryOptions.html)中指定的 Google Cloud 專案中，於 `_anonymous_` 資料集內建立。

## 後續步驟

* 試用 [BigQuery DataFrames 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)。
* [安裝 BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/install-dataframes?hl=zh-tw)。
* 瞭解如何[使用 BigQuery DataFrame 繪製圖表](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw)。
* 瞭解如何[使用 `dbt-bigquery` 轉接頭](https://docs.cloud.google.com/bigquery/docs/dataframes-dbt?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]