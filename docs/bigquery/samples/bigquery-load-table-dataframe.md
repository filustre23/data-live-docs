* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 從 DataFrame 載入資料 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

將 pandas DataFrame 的內容載入資料表。

## 程式碼範例

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import datetime

from google.cloud import bigquery
import pandas
import pytz

# Construct a BigQuery client object.
client = bigquery.Client()

# TODO(developer): Set table_id to the ID of the table to create.
# table_id = "your-project.your_dataset.your_table_name"

records = [
    {
        "title": "The Meaning of Life",
        "release_year": 1983,
        "length_minutes": 112.5,
        "release_date": pytz.timezone("Europe/Paris")
        .localize(datetime.datetime(1983, 5, 9, 13, 0, 0))
        .astimezone(pytz.utc),
        # Assume UTC timezone when a datetime object contains no timezone.
        "dvd_release": datetime.datetime(2002, 1, 22, 7, 0, 0),
    },
    {
        "title": "Monty Python and the Holy Grail",
        "release_year": 1975,
        "length_minutes": 91.5,
        "release_date": pytz.timezone("Europe/London")
        .localize(datetime.datetime(1975, 4, 9, 23, 59, 2))
        .astimezone(pytz.utc),
        "dvd_release": datetime.datetime(2002, 7, 16, 9, 0, 0),
    },
    {
        "title": "Life of Brian",
        "release_year": 1979,
        "length_minutes": 94.25,
        "release_date": pytz.timezone("America/New_York")
        .localize(datetime.datetime(1979, 8, 17, 23, 59, 5))
        .astimezone(pytz.utc),
        "dvd_release": datetime.datetime(2008, 1, 14, 8, 0, 0),
    },
    {
        "title": "And Now for Something Completely Different",
        "release_year": 1971,
        "length_minutes": 88.0,
        "release_date": pytz.timezone("Europe/London")
        .localize(datetime.datetime(1971, 9, 28, 23, 59, 7))
        .astimezone(pytz.utc),
        "dvd_release": datetime.datetime(2003, 10, 22, 10, 0, 0),
    },
]
dataframe = pandas.DataFrame(
    records,
    # In the loaded table, the column order reflects the order of the
    # columns in the DataFrame.
    columns=[
        "title",
        "release_year",
        "length_minutes",
        "release_date",
        "dvd_release",
    ],
    # Optionally, set a named index, which can also be written to the
    # BigQuery table.
    index=pandas.Index(
        ["Q24980", "Q25043", "Q24953", "Q16403"], name="wikidata_id"
    ),
)
job_config = bigquery.LoadJobConfig(
    # Specify a (partial) schema. All columns are always written to the
    # table. The schema is used to assist in data type definitions.
    schema=[
        # Specify the type of columns whose type cannot be auto-detected. For
        # example the "title" column uses pandas dtype "object", so its
        # data type is ambiguous.
        bigquery.SchemaField("title", bigquery.enums.SqlTypeNames.STRING),
        # Indexes are written if included in the schema by name.
        bigquery.SchemaField("wikidata_id", bigquery.enums.SqlTypeNames.STRING),
    ],
    # Optionally, set the write disposition. BigQuery appends loaded rows
    # to an existing table by default, but with WRITE_TRUNCATE write
    # disposition it replaces the table with the loaded data.
    write_disposition="WRITE_TRUNCATE",
)

job = client.load_table_from_dataframe(
    dataframe, table_id, job_config=job_config
)  # Make an API request.
job.result()  # Wait for the job to complete.

table = client.get_table(table_id)  # Make an API request.
print(
    "Loaded {} rows and {} columns to {}".format(
        table.num_rows, len(table.schema), table_id
    )
)
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 瀏覽器範例](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]