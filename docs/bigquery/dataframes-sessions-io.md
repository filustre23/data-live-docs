Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 管理 BigQuery DataFrames 工作階段和 I/O

本文說明如何在使用 BigQuery DataFrame 時管理工作階段，以及執行輸入/輸出 (I/O) 作業。您將瞭解如何建立及使用工作階段、處理記憶體內資料，以及從檔案和 BigQuery 資料表讀取及寫入資料。

## BigQuery 工作階段

BigQuery DataFrames 會在內部使用本機工作階段物件管理中繼資料。每個 `DataFrame` 和 `Series` 物件都會連線至工作階段，每個工作階段都會連線至[位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)，且工作階段中的每項查詢都會在您建立工作階段的位置執行。使用下列程式碼範例手動建立工作階段，並用於載入資料：

```
import bigframes
import bigframes.pandas as bpd

# Create session object
context = bigframes.BigQueryOptions(
    project=YOUR_PROJECT_ID,
    location=YOUR_LOCATION,
)
session = bigframes.Session(context)

# Load a BigQuery table into a dataframe
df1 = session.read_gbq("bigquery-public-data.ml_datasets.penguins")

# Create a dataframe with local data:
df2 = bpd.DataFrame({"my_col": [1, 2, 3]}, session=session)
```

您無法合併多個工作階段例項的資料，即使您使用相同設定初始化這些例項也一樣。下列程式碼範例顯示，嘗試合併不同工作階段例項的資料會導致錯誤：

```
import bigframes
import bigframes.pandas as bpd

context = bigframes.BigQueryOptions(location=YOUR_LOCATION, project=YOUR_PROJECT_ID)

session1 = bigframes.Session(context)
session2 = bigframes.Session(context)

series1 = bpd.Series([1, 2, 3, 4, 5], session=session1)
series2 = bpd.Series([1, 2, 3, 4, 5], session=session2)

try:
    series1 + series2
except ValueError as e:
    print(e)  # Error message: Cannot use combine sources from multiple sessions
```

### 全域工作階段

BigQuery DataFrames 提供預設全域工作階段，您可以使用 `bigframes.pandas.get_global_session()` 方法存取。在 Colab 中，您必須先為 `bigframes.pandas.options.bigquery.project` 屬性提供專案 ID，才能使用該屬性。您也可以使用 `bigframes.pandas.options.bigquery.location` 屬性設定位置，預設為 `US` 多地區。

下列程式碼範例說明如何設定全域工作階段的選項：

```
import bigframes.pandas as bpd

# Set project ID for the global session
bpd.options.bigquery.project = YOUR_PROJECT_ID
# Update the global default session location
bpd.options.bigquery.location = YOUR_LOCATION
```

如要重設全域工作階段的位置或專案，請執行 `bigframes.pandas.close_session()` 方法來關閉目前的工作階段。

許多 BigQuery DataFrames 內建函式預設會使用全域工作階段。以下程式碼範例說明內建函式如何使用全域工作階段：

```
# The following two statements are essentially the same
df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
df = bpd.get_global_session().read_gbq("bigquery-public-data.ml_datasets.penguins")
```

## 記憶體內建資料

您可以使用內建的 Python 或 NumPy 資料結構建立 `DataFrames` 和 `Series` 物件，與使用 pandas 建立物件的方式類似。使用下列程式碼範例建立物件：

```
import numpy as np

import bigframes.pandas as bpd

s = bpd.Series([1, 2, 3])

# Create a dataframe with Python dict
df = bpd.DataFrame(
    {
        "col_1": [1, 2, 3],
        "col_2": [4, 5, 6],
    }
)

# Create a series with Numpy
s = bpd.Series(np.arange(10))
```

如要使用 `read_pandas()` 方法或建構函式，將 `pandas` 物件轉換為 `DataFrames` 物件，請使用下列程式碼範例：

```
import numpy as np
import pandas as pd

import bigframes.pandas as bpd

pd_df = pd.DataFrame(np.random.randn(4, 2))

# Convert Pandas dataframe to BigQuery DataFrame with read_pandas()
df_1 = bpd.read_pandas(pd_df)
# Convert Pandas dataframe to BigQuery DataFrame with the dataframe constructor
df_2 = bpd.DataFrame(pd_df)
```

如要使用 `to_pandas()` 方法將 BigQuery DataFrames 資料載入記憶體，請使用下列程式碼範例：

```
import bigframes.pandas as bpd

bf_df = bpd.DataFrame({"my_col": [1, 2, 3]})
# Returns a Pandas Dataframe
bf_df.to_pandas()

bf_s = bpd.Series([1, 2, 3])
# Returns a Pandas Series
bf_s.to_pandas()
```

### 使用 `dry_run` 參數估算費用

載入大量資料可能需要耗費大量時間和資源。如要查看處理的資料量，請在 `to_pandas()` 呼叫中使用 `dry_run=True` 參數。使用下列程式碼範例執行模擬測試：

```
import bigframes.pandas as bpd

df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

# Returns a Pandas series with dry run stats
df.to_pandas(dry_run=True)
```

## 讀取及寫入檔案

您可以將相容檔案中的資料讀取至 BigQuery DataFrames。這些檔案可以位於本機或 Cloud Storage 中。使用下列程式碼範例，從 CSV 檔案讀取資料：

```
import bigframes.pandas as bpd

# Read a CSV file from GCS
df = bpd.read_csv("gs://cloud-samples-data/bigquery/us-states/us-states.csv")
```

如要使用 `to_csv` 方法將 BigQuery DataFrame 儲存至本機檔案或 Cloud Storage 檔案，請使用下列程式碼範例：

```
import bigframes.pandas as bpd

df = bpd.DataFrame({"my_col": [1, 2, 3]})
# Write a dataframe to a CSV file in GCS
df.to_csv(f"gs://{YOUR_BUCKET}/myfile*.csv")
```

## 讀取及寫入 BigQuery 資料表

如要使用 BigQuery 資料表參照和 `bigframes.pandas.read_gbq` 函式建立 BigQuery DataFrames，請使用下列程式碼範例：

```
import bigframes.pandas as bpd

df = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
```

如要使用 `read_gbq()` 函式搭配 SQL 字串，將資料讀取至 BigQuery DataFrames，請使用下列程式碼範例：

```
import bigframes.pandas as bpd

sql = """
SELECT species, island, body_mass_g
FROM bigquery-public-data.ml_datasets.penguins
WHERE sex = 'MALE'
"""

df = bpd.read_gbq(sql)
```

**注意：** 如果您在呼叫 `read_gbq()`、`read_gbq_table()` 或 `read_gbq_query()` 函式時指定資料表，且未在函式呼叫前設定 `bigframes.pandas.options.bigquery.location` 屬性，BigQuery DataFrames 會自動將 `bigframes.pandas.options.bigquery.location` 屬性設為資料表的位置。如要瞭解如何手動指定位置，請參閱「[全域工作階段](#global-session)」一文。

如要將 `DataFrame` 物件儲存至 BigQuery 資料表，請使用 `DataFrame` 物件的 `to_gbq()` 方法。以下程式碼範例說明如何執行這項操作：

```
import bigframes.pandas as bpd

df = bpd.DataFrame({"my_col": [1, 2, 3]})

df.to_gbq(f"{YOUR_PROJECT_ID}.{YOUR_DATASET_ID}.{YOUR_TABLE_NAME}")
```

## 後續步驟

* 瞭解 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)。
* 瞭解如何[使用 BigQuery DataFrames 中的資料類型](https://docs.cloud.google.com/bigquery/docs/dataframes-data-types?hl=zh-tw)。
* 瞭解如何[使用 BigQuery DataFrame 顯示圖表](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw)。
* 請參閱 [BigQuery DataFrames API 參考資料](https://dataframes.bigquery.dev/reference/index.html)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]