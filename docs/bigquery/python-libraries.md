* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用開放原始碼 Python 程式庫

您可以依據用途，選取 BigQuery 中的 Python 程式庫 (共有三個)。

|  | 用途 | 維護者 | 說明 |
| --- | --- | --- | --- |
| BigQuery DataFrames | 以 Python 為基礎的資料處理和機器學習作業，並透過伺服器端處理 (例如使用 slot) | Google | 透過伺服器端下推功能實作的 Pandas 和 scikit-learn API。詳情請參閱 [BigQuery DataFrames 簡介](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)。 |
| pandas-gbq | 使用用戶端資料副本，以 Python 為基礎處理資料 | 開放原始碼程式庫是由 PyData 和自願貢獻者來維護 | 可讓您在用戶端將資料移入及移出 Python DataFrame。詳情請參閱[說明文件](https://googleapis.dev/python/pandas-gbq/latest/index.html)和[原始碼](https://github.com/googleapis/python-bigquery-pandas)。 |
| google-cloud-bigquery | BigQuery 部署、管理及以 SQL 為基礎的查詢 | 開放原始碼程式庫是由 Google 維護 | 這個 Python 套件會包裝所有 BigQuery API。詳情請參閱[說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)和[原始碼](https://github.com/googleapis/python-bigquery)。 |

## 使用 pandas-gbq 和 google-cloud-bigquery

`pandas-gbq` 程式庫提供簡單的介面，可執行查詢，並將 pandas DataFrame 上傳至 BigQuery。這是 [BigQuery 用戶端程式庫](https://docs.cloud.google.com/bigquery/docs/reference/libraries?hl=zh-tw) (`google-cloud-bigquery`) 的精簡包裝函式。這兩個程式庫的重點都是協助您使用 SQL 執行資料分析。

### 安裝程式庫

如要使用本指南中的程式碼範例，請安裝 `pandas-gbq` 套件和 BigQuery Python 用戶端程式庫。

安裝 [`pandas-gbq`](https://pypi.org/project/pandas-gbq/) 和 [`google-cloud-bigquery`](https://pypi.org/project/google-cloud-bigquery/) 套件。

```
pip install --upgrade pandas-gbq 'google-cloud-bigquery[bqstorage,pandas]'
```

### 執行中的查詢數

兩種程式庫均支援查詢儲存在 BigQuery 中的資料，主要差異包括：

|  | pandas-gbq | google-cloud-bigquery |
| --- | --- | --- |
| 預設 SQL 語法 | GoogleSQL (可使用 `pandas_gbq.context.dialect` 設定) | GoogleSQL |
| 查詢設定 | 以字典形式傳送 (需符合[查詢要求](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw#QueryRequest)的格式)。 | 使用 [`QueryJobConfig`](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJobConfig?hl=zh-tw) 類別，其中包含各種 API 設定選項的屬性。 |

#### 使用 GoogleSQL 語法查詢資料

以下範例顯示如何在明確/未明確指定專案的情況下，執行 GoogleSQL 查詢。兩種程式庫在未指定專案時，均會根據[預設憑證](https://googleapis.dev/python/google-auth/latest/reference/google.auth.html#google.auth.default)來判定專案。

**注意：** `pandas.read_gbq` 方法預設使用舊版 SQL。如要使用標準 SQL，請務必如圖所示，將 `dialect` 參數明確設為 `'standard'`。

**`pandas-gbq`：**

```
import pandas

sql = """
    SELECT name
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    LIMIT 100
"""

# Run a Standard SQL query using the environment's default project
df = pandas.read_gbq(sql, dialect="standard")

# Run a Standard SQL query with the project set explicitly
project_id = "your-project-id"
df = pandas.read_gbq(sql, project_id=project_id, dialect="standard")
```

**`google-cloud-bigquery`：**

```
from google.cloud import bigquery

client = bigquery.Client()
sql = """
    SELECT name
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = 'TX'
    LIMIT 100
"""

# Run a Standard SQL query using the environment's default project
df = client.query(sql).to_dataframe()

# Run a Standard SQL query with the project set explicitly
project_id = "your-project-id"
df = client.query(sql, project=project_id).to_dataframe()
```

#### 使用舊版 SQL 語法查詢資料

以下範例顯示如何使用舊版 SQL 語法執行查詢。如需將查詢更新成 GoogleSQL 的相關說明，請參閱 [GoogleSQL 遷移指南](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/migrating-from-legacy-sql?hl=zh-tw)。

**`pandas-gbq`：**

```
import pandas

sql = """
    SELECT name
    FROM [bigquery-public-data:usa_names.usa_1910_current]
    WHERE state = 'TX'
    LIMIT 100
"""

df = pandas.read_gbq(sql, dialect="legacy")
```

**`google-cloud-bigquery`：**

```
from google.cloud import bigquery

client = bigquery.Client()
sql = """
    SELECT name
    FROM [bigquery-public-data:usa_names.usa_1910_current]
    WHERE state = 'TX'
    LIMIT 100
"""
query_config = bigquery.QueryJobConfig(use_legacy_sql=True)

df = client.query(sql, job_config=query_config).to_dataframe()
```

#### 使用 BigQuery Storage API 下載大量結果

使用 [BigQuery Storage API](https://docs.cloud.google.com/bigquery/docs/reference/storage?hl=zh-tw) 將[大量結果的下載速度提高 15 到 31 倍](https://friendliness.dev/2019/07/29/bigquery-arrow/)。

**`pandas-gbq`：**

```
import pandas

sql = "SELECT * FROM `bigquery-public-data.irs_990.irs_990_2012`"

# Use the BigQuery Storage API to download results more quickly.
df = pandas.read_gbq(sql, dialect="standard", use_bqstorage_api=True)
```

**`google-cloud-bigquery`：**

```
from google.cloud import bigquery

client = bigquery.Client()
sql = "SELECT * FROM `bigquery-public-data.irs_990.irs_990_2012`"

# The client library uses the BigQuery Storage API to download results to a
# pandas dataframe if the API is enabled on the project, the
# `google-cloud-bigquery-storage` package is installed, and the `pyarrow`
# package is installed.
df = client.query(sql).to_dataframe()
```

#### 使用設定執行查詢

您必須透過 BigQuery API 要求傳送設定，才能執行某些複雜作業，例如執行參數化查詢，或是指定要儲存查詢結果的目標資料表。在 `pandas-gbq` 程式庫中，設定必須以字典形式傳送 (需符合[查詢要求](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/query?hl=zh-tw#QueryRequest)的格式)。在 `google-cloud-bigquery` 程式庫中則會提供工作設定類別，例如 [`QueryJobConfig`](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.QueryJobConfig?hl=zh-tw) (其中包含設定複雜工作時的必要屬性)。

以下範例顯示如何使用具名參數執行查詢。

**`pandas-gbq`：**

```
import pandas

sql = """
    SELECT name
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = @state
    LIMIT @limit
"""
query_config = {
    "query": {
        "parameterMode": "NAMED",
        "queryParameters": [
            {
                "name": "state",
                "parameterType": {"type": "STRING"},
                "parameterValue": {"value": "TX"},
            },
            {
                "name": "limit",
                "parameterType": {"type": "INTEGER"},
                "parameterValue": {"value": 100},
            },
        ],
    }
}

df = pandas.read_gbq(sql, configuration=query_config)
```

**`google-cloud-bigquery`：**

```
from google.cloud import bigquery

client = bigquery.Client()
sql = """
    SELECT name
    FROM `bigquery-public-data.usa_names.usa_1910_current`
    WHERE state = @state
    LIMIT @limit
"""
query_config = bigquery.QueryJobConfig(
    query_parameters=[
        bigquery.ScalarQueryParameter("state", "STRING", "TX"),
        bigquery.ScalarQueryParameter("limit", "INTEGER", 100),
    ]
)

df = client.query(sql, job_config=query_config).to_dataframe()
```

### 將 pandas DataFrame 載入 BigQuery 表格

兩種程式庫均支援將 pandas DataFrame 資料上傳至新的 BigQuery 資料表。主要差異如下：

|  | pandas-gbq | google-cloud-bigquery |
| --- | --- | --- |
| 支援類型 | 由於 API 不支援巢狀結構值或陣列值，因此會將 DataFrame 轉換為 CSV 格式後才傳送至 API。 | 由於 API 支援巢狀結構值或陣列值，因此會將 DataFrame 轉換為 Parquet 或 CSV 格式後才傳送至 API。如果需要彈性序列化日期和時間，請選擇 CSV；如果需要結構體和陣列值，請選擇 Parquet。系統預設會選擇 Parquet。請注意，您必須安裝 `pyarrow` (即用來將 DataFrame 資料傳送至 BigQuery API 的 Parquet Engine)，才能將 DataFrame 載入至資料表。 |
| 載入設定 | 您可以選擇指定[資料表結構定義](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/tables?hl=zh-tw#TableSchema)。 | 使用 [`LoadJobConfig`](https://docs.cloud.google.com/python/docs/reference/bigquery/latest/google.cloud.bigquery.job.LoadJobConfig?hl=zh-tw) 類別，其中包含各種 API 設定選項的屬性。 |

**`pandas-gbq`：**

```
import pandas

df = pandas.DataFrame(
    {
        "my_string": ["a", "b", "c"],
        "my_int64": [1, 2, 3],
        "my_float64": [4.0, 5.0, 6.0],
        "my_timestamp": [
            pandas.Timestamp("1998-09-04T16:03:14"),
            pandas.Timestamp("2010-09-13T12:03:45"),
            pandas.Timestamp("2015-10-02T16:00:00"),
        ],
    }
)
table_id = "my_dataset.new_table"

df.to_gbq(table_id)
```

**`google-cloud-bigquery`：**

`google-cloud-bigquery` 套件需要 `pyarrow` 程式庫，才能將 pandas DataFrame 序列化到 Parquet 檔案。

安裝 `pyarrow` 套件：

```
 pip install pyarrow
```

```
from google.cloud import bigquery
import pandas

df = pandas.DataFrame(
    {
        "my_string": ["a", "b", "c"],
        "my_int64": [1, 2, 3],
        "my_float64": [4.0, 5.0, 6.0],
        "my_timestamp": [
            pandas.Timestamp("1998-09-04T16:03:14"),
            pandas.Timestamp("2010-09-13T12:03:45"),
            pandas.Timestamp("2015-10-02T16:00:00"),
        ],
    }
)
client = bigquery.Client()
table_id = "my_dataset.new_table"
# Since string columns use the "object" dtype, pass in a (partial) schema
# to ensure the correct BigQuery data type.
job_config = bigquery.LoadJobConfig(
    schema=[
        bigquery.SchemaField("my_string", "STRING"),
    ]
)

job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

# Wait for the load job to complete.
job.result()
```

### pandas-gbq 不支援的功能

`pandas-gbq` 程式庫提供的實用介面可讓您查詢資料並將資料寫入資料表，但不支援部分 BigQuery API 功能，包括 (但不限於) 以下功能：

* [管理資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)，包括[建立新資料集](https://docs.cloud.google.com/bigquery/docs/datasets?hl=zh-tw)、[更新資料集屬性](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw)以及[刪除資料集](https://docs.cloud.google.com/bigquery/docs/managing-datasets?hl=zh-tw#delete-datasets)
* 將 pandas DataFrames 以外格式的資料載入至 BigQuery，或從含有 JSON 欄的 pandas DataFrames 載入資料
* [管理資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw)，包括[列出資料集中的資料表](https://docs.cloud.google.com/bigquery/docs/tables?hl=zh-tw#list_tables_in_a_dataset)、[複製資料表的資料](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#copying_a_single_source_table)以及[刪除資料表](https://docs.cloud.google.com/bigquery/docs/managing-tables?hl=zh-tw#deleting_a_table)
* 直接[將 BigQuery 資料匯出](https://docs.cloud.google.com/bigquery/docs/exporting-data?hl=zh-tw)至 Cloud Storage

## 排解連線集區錯誤

錯誤字串：`Connection pool is full, discarding connection: bigquery.googleapis.com.
Connection pool size: 10`

如果您在 Python 中使用預設的 BigQuery 用戶端物件，則最多只能有 10 個執行緒，因為 [Python HTTPAdapter](https://docs.python-requests.org/en/latest/api/#requests.adapters.HTTPAdapter) 的預設集區大小為 10。如要使用超過 10 個連線，請建立自訂 `requests.adapters.HTTPAdapter` 物件。例如：

```
client = bigquery.Client()
adapter = requests.adapters.HTTPAdapter(pool_connections=128,
pool_maxsize=128,max_retries=3)
client._http.mount("https://",adapter)
client._http._auth_request.session.mount("https://",adapter)
query_job = client.query(QUERY)
```




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]