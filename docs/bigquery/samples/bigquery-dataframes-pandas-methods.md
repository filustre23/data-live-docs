Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用 BigQuery DataFrames bigframes.pandas API 執行查詢 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用 BigQuery DataFrames bigframes.pandas API，透過 BigQuery 查詢引擎執行資料分析。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [使用 BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/use-bigquery-dataframes?hl=zh-tw)

## 程式碼範例

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

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

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]