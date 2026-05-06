Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 寫入目的地資料表 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

對出生率公開資料集執行查詢，然後將結果寫入目的地資料表。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [使用 Managed Service for Apache Spark、BigQuery 和 Apache Spark ML 進行機器學習](https://docs.cloud.google.com/dataproc/docs/tutorials/bigquery-sparkml?hl=zh-tw)

## 程式碼範例

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
"""Create a Google BigQuery linear regression input table.

In the code below, the following actions are taken:
* A new dataset is created "natality_regression."
* A query is run against the public dataset,
    bigquery-public-data.samples.natality, selecting only the data of
    interest to the regression, the output of which is stored in a new
    "regression_input" table.
* The output table is moved over the wire to the user's default project via
    the built-in BigQuery Connector for Spark that bridges BigQuery and
    Cloud Dataproc.
"""

from google.cloud import bigquery

# Create a new Google BigQuery client using Google Cloud Platform project
# defaults.
client = bigquery.Client()

# Prepare a reference to a new dataset for storing the query results.
dataset_id = "natality_regression"
dataset_id_full = f"{client.project}.{dataset_id}"

dataset = bigquery.Dataset(dataset_id_full)

# Create the new BigQuery dataset.
dataset = client.create_dataset(dataset)

# Configure the query job.
job_config = bigquery.QueryJobConfig()

# Set the destination table to where you want to store query results.
# As of google-cloud-bigquery 1.11.0, a fully qualified table ID can be
# used in place of a TableReference.
job_config.destination = f"{dataset_id_full}.regression_input"

# Set up a query in Standard SQL, which is the default for the BigQuery
# Python client library.
# The query selects the fields of interest.
query = """
    SELECT
        weight_pounds, mother_age, father_age, gestation_weeks,
        weight_gain_pounds, apgar_5min
    FROM
        `bigquery-public-data.samples.natality`
    WHERE
        weight_pounds IS NOT NULL
        AND mother_age IS NOT NULL
        AND father_age IS NOT NULL
        AND gestation_weeks IS NOT NULL
        AND weight_gain_pounds IS NOT NULL
        AND apgar_5min IS NOT NULL
"""

# Run the query.
client.query_and_wait(query, job_config=job_config)  # Waits for the query to finish
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]