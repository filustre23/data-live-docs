Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# BigQuery DataFrames 簡介

您可以使用開放原始碼 BigQuery DataFrames 程式庫，透過熟悉的 Python API 處理數 TB 的資料，並訓練 AI 和機器學習 (ML) 模型。您可以使用 pandas 和 scikit-learn API 建構資料管道，並直接在 BigQuery 中分析大量資料集，不必將資料移至用戶端機器。

**注意：** BigQuery DataFrames 2.0 版對部分預設參數進行了破壞性變更。如要瞭解這些異動，以及如何遷移至 2.0 版，請參閱「[遷移至 BigQuery DataFrames 2.0](https://docs.cloud.google.com/bigquery/docs/migrate-dataframes?hl=zh-tw)」。

## BigQuery DataFrames 的優點

BigQuery DataFrames 會執行下列操作：

* 提供超過 750 個 pandas 和 scikit-learn API，透過 SQL 轉換為 BigQuery 和 BigQuery ML API 實作。
* 延遲執行查詢，提升效能。
* 使用使用者定義的 Python 函式擴充資料轉換功能，以便在 Google Cloud中處理資料。這些函式會自動部署為 BigQuery [遠端函式](https://docs.cloud.google.com/bigquery/docs/remote-functions?hl=zh-tw)。
* 與 Gemini Enterprise Agent Platform 整合，可讓您使用 Gemini 模型生成文字。

## 授權

BigQuery DataFrames 採用 [Apache-2.0 授權](https://github.com/googleapis/python-bigquery-dataframes/blob/main/LICENSE)。

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
* 您必須在清除工作階段時，明確清除所有自動建立的 Cloud Run 函式。詳情請參閱「[支援的 pandas API](https://dataframes.bigquery.dev/supported_pandas_apis.html)」。

## 定價

* BigQuery DataFrames 是一組開放原始碼 Python 程式庫，可不需額外付費下載。
* BigQuery DataFrames 會使用 BigQuery、Cloud Run functions、Agent Platform 和其他Google Cloud 服務，這些服務會產生各自的費用。
* 在一般使用情況下，BigQuery DataFrames 會將臨時資料 (例如中繼結果) 儲存在 BigQuery 資料表中。根據預設，這些資料表會保留七天，系統會向您收取儲存資料的費用。系統會在您透過 [`bf.options.bigquery.project` 選項](https://dataframes.bigquery.dev/reference/api/bigframes._config.BigQueryOptions.html)指定的 Google Cloud 專案中，建立`_anonymous_`資料集內的資料表。

## 用途

如果您熟悉 pandas，可以使用 BigQuery DataFrames 處理 BigQuery 資料，只需稍微修改程式碼即可。例如，您可以使用熟悉的 pandas 方法，分析 BigQuery 資料表中的資料：

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

BigQuery DataFrames 可用於下列數據分析和機器學習用途：

* [機器學習與 AI](https://docs.cloud.google.com/bigquery/docs/dataframes-ml-ai?hl=zh-tw)
* [自訂 Python 函式](https://docs.cloud.google.com/bigquery/docs/dataframes-custom-python-functions?hl=zh-tw)
* [使用 BigQuery DataFrames 以圖表呈現圖形](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw)
* [在 dbt 中使用 BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/dataframes-dbt?hl=zh-tw)
* [使用 BigQuery JupyterLab 外掛程式](https://docs.cloud.google.com/bigquery/docs/jupyterlab-plugin?hl=zh-tw)

## 程式碼範例和參考文件

探索 BigQuery DataFrames 的程式碼範例、筆記本和參考文件：

* [GitHub 中的 BigQuery DataFrames 筆記本範例](https://github.com/google/bigframes/tree/main/notebooks)
* [BigQuery DataFrames API 參考資料](https://dataframes.bigquery.dev/reference/index.html) (包括 [`bigframes.pandas`](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.html) 和 [`bigframes.bigquery.ai`](https://dataframes.bigquery.dev/reference/api/bigframes.bigquery.ai.html))
* [BigQuery DataFrames Cloud 用戶端程式庫參考資料](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)
* [BigQuery Python 程式庫總覽](https://docs.cloud.google.com/bigquery/docs/python-libraries?hl=zh-tw)
* [GitHub 上的 BigQuery DataFrames 原始碼存放區](https://github.com/google/bigframes)和 [PyPI 上的套件](https://pypi.org/project/bigframes/)

## 後續步驟

* 試用 [BigQuery DataFrames 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)。
* [安裝及設定 BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/install-dataframes?hl=zh-tw)。
* 瞭解如何[操控資料](https://docs.cloud.google.com/bigquery/docs/dataframes-data-manipulation?hl=zh-tw)及[使用資料類型系統](https://docs.cloud.google.com/bigquery/docs/dataframes-data-types?hl=zh-tw)。
* 瞭解如何[管理工作階段和 I/O](https://docs.cloud.google.com/bigquery/docs/dataframes-sessions-io?hl=zh-tw)。
* 瞭解如何[提升效能](https://docs.cloud.google.com/bigquery/docs/dataframes-performance?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]