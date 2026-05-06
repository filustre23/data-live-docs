Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [範例](https://docs.cloud.google.com/bigquery/docs/samples?hl=zh-tw)

# 插入 GeoJSON 資料 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

使用 GeoJSON 資料串流插入 GEOGRAPHY 欄。

## 深入探索

如需包含這個程式碼範例的詳細說明文件，請參閱下列文章：

* [使用地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw)

## 程式碼範例

### Python

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Python 設定說明操作。詳情請參閱 [BigQuery Python API 參考說明文件](https://docs.cloud.google.com/python/docs/reference/bigquery/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
import geojson
from google.cloud import bigquery

bigquery_client = bigquery.Client()

# This example uses a table containing a column named "geo" with the
# GEOGRAPHY data type.
table_id = "my-project.my_dataset.my_table"

# Use the python-geojson library to generate GeoJSON of a line from LAX to
# JFK airports. Alternatively, you may define GeoJSON data directly, but it
# must be converted to a string before loading it into BigQuery.
my_geography = geojson.LineString([(-118.4085, 33.9416), (-73.7781, 40.6413)])
rows = [
    # Convert GeoJSON data into a string.
    {"geo": geojson.dumps(my_geography)}
]

#  table already exists and has a column
# named "geo" with data type GEOGRAPHY.
errors = bigquery_client.insert_rows_json(table_id, rows)
if errors:
    raise RuntimeError(f"row insert failed: {errors}")
else:
    print(f"wrote 1 row to {table_id}")
```

### Ruby

在試用這個範例之前，請先按照「[使用用戶端程式庫的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/quickstarts/quickstart-client-libraries?hl=zh-tw)」中的 Ruby 設定說明操作。詳情請參閱 [BigQuery Ruby API 參考說明文件](https://googleapis.dev/ruby/google-cloud-bigquery/latest/Google/Cloud/Bigquery.html)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。詳情請參閱「[設定用戶端程式庫的驗證作業](https://docs.cloud.google.com/bigquery/docs/authentication?hl=zh-tw#client-libs)」。

```
require "google/cloud/bigquery"
require "rgeo"
require "rgeo/geo_json"

def insert_geojson dataset_id = "your_dataset_id", table_id = "your_table_id"
  bigquery = Google::Cloud::Bigquery.new
  dataset  = bigquery.dataset dataset_id
  table    = dataset.table table_id

  # Use the RGeo library to generate GeoJSON of a line from LAX to
  # JFK airports. Alternatively, you may define GeoJSON data directly, but it
  # must be converted to a string before loading it into BigQuery.
  factory = RGeo::Geographic.spherical_factory
  my_line = factory.line_string([factory.point(-118.4085, 33.9416), factory.point(-73.7781, 40.6413)])
  row_data = [
    # Convert GeoJSON data into a string.
    { geo: RGeo::GeoJSON.encode(my_line).to_json }
  ]

  # Table already exists and has a column named "geo" with data type GEOGRAPHY.
  response = table.insert row_data

  if response.success?
    puts "Inserted GeoJSON row successfully"
  else
    puts "GeoJSON row insert failed: #{response.error_rows.first&.errors}"
  end
end
```

## 後續步驟

如要搜尋及篩選其他 Google Cloud 產品的程式碼範例，請參閱[Google Cloud 範例瀏覽工具](https://docs.cloud.google.com/docs/samples?product=bigquery&hl=zh-tw)。

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。




[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],[],[],[]]