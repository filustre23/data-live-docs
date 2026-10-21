Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 使用 pandas-gbq 將 DataFrame 載入 BigQuery 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用 pandas-gbq 套件將 DataFrame 載入 BigQuery。

## 程式碼範例

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import bigframes.pandas as bpd
import pandas as pd
import pandas_gbq

# Set partial ordering mode for BigQuery DataFrames.
bpd.options.bigquery.ordering_mode = "partial"


def pandas_to_gbq_simple_pandas_gbq(
    destination_table: str = "your-project.your_dataset.your_table_name",
) -> None:
    """Uploads a pandas DataFrame to BigQuery using pandas-gbq directly."""
    df = pd.DataFrame(
        {
            "my_string": ["a", "b", "c"],
            "my_int64": [1, 2, 3],
            "my_float64": [4.0, 5.0, 6.0],
            "my_bool1": [True, False, True],
            "my_bool2": [False, True, False],
            "my_dates": pd.date_range("now", periods=3),
        }
    )
    pandas_gbq.to_gbq(df, destination_table, if_exists="replace")
    print(f"Uploaded DataFrame to {destination_table} using pandas-gbq.")


def pandas_to_gbq_simple_bigframes(
    destination_table: str = "your-project.your_dataset.your_table_name",
) -> None:
    """Uploads a pandas DataFrame to BigQuery using BigQuery DataFrames."""
    df = pd.DataFrame(
        {
            "my_string": ["a", "b", "c"],
            "my_int64": [1, 2, 3],
            "my_float64": [4.0, 5.0, 6.0],
            "my_bool1": [True, False, True],
            "my_bool2": [False, True, False],
            "my_dates": pd.date_range("now", periods=3),
        }
    )
    bq_df = bpd.read_pandas(df)
    bq_df.to_gbq(destination_table, if_exists="replace")
    print(f"Uploaded DataFrame to {destination_table} using BigQuery DataFrames.")


# [Preferred] Run using pandas-gbq:
# pandas_to_gbq_simple_pandas_gbq("your-project.your_dataset.your_table_name")

# Alternatively, run using BigQuery DataFrames:
# pandas_to_gbq_simple_bigframes("your-project.your_dataset.your_table_name")
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]