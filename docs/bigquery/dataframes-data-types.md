* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BigQuery DataFrames 資料類型系統

BigQuery DataFrames 資料型別系統是以 BigQuery 資料型別為基礎建構而成。這項設計可確保與Google Cloud 資料倉儲順暢整合及保持一致，反映 BigQuery 中用於資料儲存的內建型別。

## 類型對應

下表列出 BigQuery、BigQuery DataFrames 和其他 Python 程式庫的對等資料類型，以及支援程度：

| 資料類型 | BigQuery | BigQuery DataFrames | Python 內建函式 | PyArrow |
| --- | --- | --- | --- | --- |
| 布林值 | `BOOL` | `pandas.BooleanDtype()` | `bool` | `bool_()` |
| 整數 | `INT64` | `pandas.Int64Dtype()` | `int` | `int64()` |
| 浮點值 | `FLOAT64` | `pandas.Float64Dtype()` | `float` | `float64()` |
| 字串 | `STRING` | `pandas.StringDtype(storage="pyarrow")` | `str` | `string()` |
| 位元組 | `BYTES` | `pandas.ArrowDtype(pyarrow.binary())` | `bytes` | `binary()` |
| 日期 | `DATE` | `pandas.ArrowDtype(pyarrow.date32())` | `datetime.date` | `date32()` |
| 時間 | `TIME` | `pandas.ArrowDtype(pyarrow.time64("us"))` | `datetime.time` | `time64("us")` |
| 日期時間 | `DATETIME` | `pandas.ArrowDtype(pyarrow.timestamp("us"))` | `datetime.datetime` | `timestamp("us")` |
| 時間戳記 | `TIMESTAMP` | `pandas.ArrowDtype(pyarrow.timestamp("us", tz="UTC"))` | `Datetime.datetime` (含時區) | `timestamp("us", tz="UTC")` |
| 數字 | `NUMERIC` | `pandas.ArrowDtype(pyarrow.decimal128(38, 9))` | `decimal.Decimal` | `decimal128(38, 9)` |
| 大數字 | `BIGNUMERIC` | `pandas.ArrowDtype(pyarrow.decimal256(76, 38))` | `decimal.Decimal` | `decimal256(76, 38)` |
| List<T> | `ARRAY``<T>` | `pandas.ArrowDtype(pyarrow.list_(T))` | `list[T]` | `list_(T)` |
| 結構 | `STRUCT` | `pandas.ArrowDtype(pyarrow.struct())` | `dict` | `struct()` |
| JSON | `JSON` | `pandas.ArrowDtype(pyarrow.json_(pa.string())` (適用於 pandas 3.0 以上版本和 PyArrow 19.0 以上版本)。否則，JSON 欄會顯示為 `pandas.ArrowDtype(db_dtypes.JSONArrowType())`。這項功能為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。 | 不支援 | `json_()` ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| 地理位置 | `GEOGRAPHY` | `Geopandas.array.GeometryDtype()`  僅支援 `to_pandas()`。 | 不支援 | 不支援 |
| Timedelta | 不支援 | `pandas.ArrowDtype(pyarrow.duration("us"))` | `datetime.timedelta` | `duration("us")` |

**注意：** BigQuery DataFrames 不支援下列 BigQuery 資料類型：`INTERVAL` 和 `RANGE`。所有其他 BigQuery 資料類型都會顯示為物件類型。

### 類型轉換

與本機資料搭配使用時，BigQuery DataFrames 會在[定義類型對應](#type-mappings)的任何位置，將資料類型轉換為對應的 BigQuery DataFrames 等效類型，如下列範例所示：

```
import pandas as pd

import bigframes.pandas as bpd

s = pd.Series([pd.Timestamp("20250101")])
assert s.dtype == "datetime64[ns]"
assert bpd.read_pandas(s).dtype == "timestamp[us][pyarrow]"
```

如果資料型別對等項目之間有差異，PyArrow 會決定行為。在極少數情況下，Python 內建型別的運作方式與 PyArrow 對應項目不同，BigQuery DataFrames 通常會偏好 PyArrow 行為，以確保一致性。

下列程式碼範例使用 `datetime.date + timedelta` 作業，說明 BigQuery DataFrames 遵循 PyArrow 行為，傳回時間戳記例項，這與仍會傳回日期例項的 Python datetime 程式庫不同：

```
import datetime

import pandas as pd

import bigframes.pandas as bpd

s = pd.Series([datetime.date(2025, 1, 1)])
s + pd.Timedelta(hours=12)
# 0	2025-01-01
# dtype: object

bpd.read_pandas(s) + pd.Timedelta(hours=12)
# 0    2025-01-01 12:00:00
# dtype: timestamp[us][pyarrow]
```

## 特殊類型

以下各節說明 BigQuery DataFrame 使用的特殊資料型別。

### JSON

在 BigQuery DataFrames 中，使用 BigQuery [JSON 格式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#json_type) (輕量級標準) 的資料欄會以 `pandas.ArrowDtype` 表示。確切的基礎 Arrow 型別取決於程式庫版本。舊版環境通常會使用 `db_dtypes.JSONArrowType()` 確保相容性，這是 Arrow 擴充功能型別，可做為 `pa.string()` 的輕量包裝函式。相較之下，較新的設定 (pandas 3.0 以上版本和 PyArrow 19.0 以上版本) 使用的是較新的 `pa.json_(pa.string())` 表示法。

### `timedelta`

BigQuery 內建型別系統中沒有 `timedelta` 型別的直接對應項目。如要管理時間長度資料，BigQuery DataFrames 會使用 `INT64` 型別做為 BigQuery 表格中的基礎儲存格式。您可以預期計算結果會與使用 pandas 程式庫執行同等作業時的行為一致。

您可以將 `timedelta` 值直接載入 BigQuery DataFrame 和 `Series` 物件，如下列範例所示：

```
import pandas as pd

import bigframes.pandas as bpd

s = pd.Series([pd.Timedelta("1s"), pd.Timedelta("2m")])
bpd.read_pandas(s)
# 0    0 days 00:00:01
# 1    0 days 00:02:00
# dtype: duration[us][pyarrow]
```

與 pandas 不同，BigQuery DataFrames 僅支援微秒精確度的 `timedelta` 值。如果資料包含奈秒，您必須將其四捨五入，以免發生例外狀況，如下列範例所示：

```
import pandas as pd

s = pd.Series([pd.Timedelta("999ns")])
bpd.read_pandas(s.dt.round("us"))
# 0    0 days 00:00:00.000001
# dtype: duration[us][pyarrow]
```

您可以使用 `bigframes.pandas.to_timedelta` 函式，將 BigQuery DataFrame `Series` 物件轉換為 `timedelta` 型別，如下列範例所示：

```
import bigframes.pandas as bpd

bpd.to_timedelta([1, 2, 3], unit="s")
# 0    0 days 00:00:01
# 1    0 days 00:00:02
# 2    0 days 00:00:03
# dtype: duration[us][pyarrow]
```

將含有 `timedelta` 值的資料載入 BigQuery 資料表時，這些值會轉換為微秒，並儲存在 `INT64` 資料欄中。為保留型別資訊，BigQuery DataFrames 會在這些資料欄的說明中附加 `#microseconds` 字串。部分作業 (例如執行 SQL 查詢和叫用 UDF) 不會保留資料欄說明，且完成這些作業後，`timedelta` 類型資訊會遺失。

## 複合類型工具

對於特定複合型別，BigQuery DataFrames 提供工具，可讓您存取及處理這些型別中的基本值。

### 清單存取子

如以下範例所示，`ListAccessor` 物件可協助您使用 `Series` 物件的清單屬性，對每個清單元素執行作業：

```
import bigframes.pandas as bpd

s = bpd.Series([[1, 2, 3], [4, 5], [6]])  # dtype: list<item: int64>[pyarrow]

# Access the first elements of each list
s.list[0]
# 0    1
# 1    4
# 2    6
# dtype: Int64

# Get the lengths of each list
s.list.len()
# 0    3
# 1    2
# 2    1
# dtype: Int64
```

### 結構存取子

`StructAccessor` 物件可以存取及處理一系列結構體中的欄位。API 存取器物件為 `series.struct`，如下列範例所示：

```
import bigframes.pandas as bpd

structs = [
    {"id": 101, "category": "A"},
    {"id": 102, "category": "B"},
    {"id": 103, "category": "C"},
]
s = bpd.Series(structs)
# Get the 'id' field of each struct
s.struct.field("id")
# 0    101
# 1    102
# 2    103
# Name: id, dtype: Int64
```

如果您要存取的 `struct` 欄位與其他 `Series` 屬性明確無關，可以略過呼叫 `struct`，如以下範例所示：

```
import bigframes.pandas as bpd

structs = [
    {"id": 101, "category": "A"},
    {"id": 102, "category": "B"},
    {"id": 103, "category": "C"},
]
s = bpd.Series(structs)

# not explicitly using the "struct" property
s.id
# 0    101
# 1    102
# 2    103
# Name: id, dtype: Int64
```

不過，最佳做法是使用 `struct` 存取欄位，因為這樣程式碼會更容易理解，也比較不會出錯。

### 字串存取子

您可以使用 `Series` 物件的 `str` 屬性存取 `StringAccessor` 物件，如以下範例所示：

```
import bigframes.pandas as bpd

s = bpd.Series(["abc", "de", "1"])  # dtype: string[pyarrow]

# Get the first character of each string
s.str[0]
# 0    a
# 1    d
# 2    1
# dtype: string

# Check whether there are only alphabetic characters in each string
s.str.isalpha()
# 0     True
# 1     True
# 2     False
# dtype: boolean

# Cast the alphabetic characters to their upper cases for each string
s.str.upper()
# 0    ABC
# 1     DE
# 2      1
# dtype: string
```

### 地理位置存取子

BigQuery DataFrames 提供 `GeographyAccessor` 物件，與 GeoPandas 程式庫提供的 GeoSeries 結構共用類似的 API。您可以使用 `Series` 物件的 `geo` 屬性叫用 `GeographyAccessor` 物件，如下列範例所示：

```
from shapely.geometry import Point

import bigframes.pandas as bpd

s = bpd.Series([Point(1, 0), Point(2, 1)])  # dtype: geometry

s.geo.y
# 0    0.0
# 1    1.0
# dtype: Float64
```

## 後續步驟

* 瞭解 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)。
* 瞭解 [BigQuery DataFrames 工作階段和 I/O](https://docs.cloud.google.com/bigquery/docs/dataframes-sessions-io?hl=zh-tw)。
* 瞭解如何[使用 BigQuery DataFrame 顯示圖表](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw)。
* 請參閱 [BigQuery DataFrames API 參考資料](https://dataframes.bigquery.dev/reference/index.html)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-04-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-04-30 (世界標準時間)。"],[],[]]