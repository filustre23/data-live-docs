Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BigQuery DataFrames 資料類型系統

BigQuery DataFrames 資料類型系統可讓您使用與內建 BigQuery 儲存空間類型一致的資料結構。根據這些資料類型建立分析，可確保資料倉儲中的資料類型完美整合且可靠對應。

## 類型對應

下表列出 BigQuery、BigQuery DataFrames 和其他 Python 程式庫中的對等資料類型，以及支援程度：

| 資料類型 | BigQuery | BigQuery DataFrames | Python 內建 | PyArrow |
| --- | --- | --- | --- | --- |
| 布林值 | `BOOL` | `pandas.BooleanDtype()` | `bool` | `bool_()` |
| 整數 | `INT64` | `pandas.Int64Dtype()` | `int` | `int64()` |
| 浮點值 | `FLOAT64` | `pandas.Float64Dtype()` | `float` | `float64()` |
| 字串 | `STRING` | `pandas.StringDtype(storage="pyarrow")` | `str` | `string()` |
| 位元組數 | `BYTES` | `pandas.ArrowDtype(pyarrow.binary())` | `bytes` | `binary()` |
| 日期 | `DATE` | `pandas.ArrowDtype(pyarrow.date32())` | `datetime.date` | `date32()` |
| 時間 | `TIME` | `pandas.ArrowDtype(pyarrow.time64("us"))` | `datetime.time` | `time64("us")` |
| 日期時間 | `DATETIME` | `pandas.ArrowDtype(pyarrow.timestamp("us"))` | `datetime.datetime` | `timestamp("us")` |
| 時間戳記 | `TIMESTAMP` | `pandas.ArrowDtype(pyarrow.timestamp("us", tz="UTC"))` | `Datetime.datetime` (含時區) | `timestamp("us", tz="UTC")` |
| 數字 | `NUMERIC` | `pandas.ArrowDtype(pyarrow.decimal128(38, 9))` | `decimal.Decimal` | `decimal128(38, 9)` |
| Big numeric | `BIGNUMERIC` | `pandas.ArrowDtype(pyarrow.decimal256(76, 38))` | `decimal.Decimal` | `decimal256(76, 38)` |
| List<T> | `ARRAY``<T>` | `pandas.ArrowDtype(pyarrow.list_(T))` | `list[T]` | `list_(T)` |
| 結構 | `STRUCT` | `pandas.ArrowDtype(pyarrow.struct())` | `dict` | `struct()` |
| JSON | `JSON` | `pandas.ArrowDtype(pyarrow.json_(pa.string())`；否則 JSON 資料欄會公開為 `pandas.ArrowDtype(db_dtypes.JSONArrowType())`。這項功能為[預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)。 | 不支援 | `json_()` ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) |
| 地理位置 | `GEOGRAPHY` | `Geopandas.array.GeometryDtype()`  僅支援 `to_pandas()`。 | 不支援 | 不支援 |
| Timedelta | 不支援 | `pandas.ArrowDtype(pyarrow.duration("us"))` | `datetime.timedelta` | `duration("us")` |

**注意：** BigQuery DataFrames 不支援下列 BigQuery 資料類型：`INTERVAL` 和 `RANGE`。所有其他 BigQuery 資料類型都會顯示為物件類型。

### 類型轉換

與店面資料搭配使用時，BigQuery DataFrames 會在[定義類型對應](#type-mappings)的位置，將資料類型轉換為對應的 BigQuery DataFrames 等效類型，如下例所示：

```
import pandas as pd

import bigframes.pandas as bpd

s = pd.Series([pd.Timestamp("20250101")])
assert s.dtype == "datetime64[ns]"
assert bpd.read_pandas(s).dtype == "timestamp[us][pyarrow]"
```

如果等效資料類型之間有差異，PyArrow 會決定行為。在極少數情況下，Python 內建類型的運作方式與 PyArrow 對應類型不同，BigQuery DataFrames 通常會優先採用 PyArrow 行為，以確保一致性。

下列程式碼範例使用 `datetime.date + timedelta` 作業，顯示 BigQuery DataFrames 遵循 PyArrow 行為，傳回時間戳記例項，而非像 Python datetime 程式庫一樣傳回日期例項：

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

以下各節說明 BigQuery DataFrames 使用的特殊資料類型。

### JSON

在 BigQuery DataFrames 中，使用 BigQuery [JSON 格式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/data-types?hl=zh-tw#json_type) (輕量標準) 的資料欄會以 `pandas.ArrowDtype` 表示。確切的基礎 Arrow 類型取決於程式庫版本。舊版環境通常會使用 `db_dtypes.JSONArrowType()` 以確保相容性，這是一種 Arrow 擴充功能類型，可做為 `pa.string()` 的輕量包裝函式。相較之下，較新的設定 (pandas 3.0 以上版本和 PyArrow 19.0 以上版本) 則使用較新的 `pa.json_(pa.string())` 表示法。

### `timedelta`

BigQuery 內建類型系統中沒有與 `timedelta` 類型直接對應的類型。為管理時間長度資料，BigQuery DataFrames 會使用 `INT64` 類型，做為 BigQuery 資料表的基礎儲存格式。運算結果應與使用 pandas 程式庫執行等效運算時預期的行為一致。

您可以直接將 `timedelta` 值載入 BigQuery DataFrames 和 `Series` 物件，如以下範例所示：

```
import pandas as pd

import bigframes.pandas as bpd

s = pd.Series([pd.Timedelta("1s"), pd.Timedelta("2m")])
bpd.read_pandas(s)
# 0    0 days 00:00:01
# 1    0 days 00:02:00
# dtype: duration[us][pyarrow]
```

與 pandas 不同，BigQuery DataFrames 僅支援微秒精確度的 `timedelta` 值。如果資料包含奈秒，請務必四捨五入，以免發生潛在例外狀況，如以下範例所示：

```
import pandas as pd

s = pd.Series([pd.Timedelta("999ns")])
bpd.read_pandas(s.dt.round("us"))
# 0    0 days 00:00:00.000001
# dtype: duration[us][pyarrow]
```

您可以使用 `bigframes.pandas.to_timedelta` 函式，將 BigQuery DataFrames `Series` 物件轉換為 `timedelta` 類型，如下例所示：

```
import bigframes.pandas as bpd

bpd.to_timedelta([1, 2, 3], unit="s")
# 0    0 days 00:00:01
# 1    0 days 00:00:02
# 2    0 days 00:00:03
# dtype: duration[us][pyarrow]
```

將含有 `timedelta` 值的資料載入 BigQuery 資料表時，系統會將這些值轉換為微秒，並儲存在 `INT64` 資料欄中。為保留類型資訊，BigQuery DataFrames 會將 `#microseconds` 字串附加至這些資料欄的說明。部分作業 (例如執行 SQL 查詢和叫用 UDF) 不會保留資料欄說明，且在這些作業完成後，`timedelta` 類型資訊會遺失。

## 複合類型的工具

針對特定複合類型，BigQuery DataFrames 提供工具，可讓您存取及處理這些類型中的元素值。

### 清單存取子

`ListAccessor` 物件可協助您使用 `Series` 物件的清單屬性，對每個清單元素執行作業，如以下範例所示：

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

### struct 存取子

`StructAccessor` 物件可以存取及處理一系列 struct 中的欄位。API 存取子物件為 `series.struct`，如以下範例所示：

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

如果您要存取的 `struct` 欄位與其他 `Series` 屬性明確區分，則可以略過呼叫 `struct`，如以下範例所示：

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

不過，最佳做法是使用 `struct` 存取欄位，因為這樣可以讓程式碼更容易理解，也比較不容易出錯。

### 字串存取子

您可以透過 `Series` 物件的 `str` 屬性存取 `StringAccessor` 物件，如以下範例所示：

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

BigQuery DataFrames 提供 `GeographyAccessor` 物件，其 API 與 GeoPandas 程式庫提供的 GeoSeries 結構類似。您可以使用 `Series` 物件上的 `geo` 屬性叫用 `GeographyAccessor` 物件，如以下範例所示：

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
* 瞭解如何[使用 BigQuery DataFrames 建立圖表](https://docs.cloud.google.com/bigquery/docs/dataframes-visualizations?hl=zh-tw)。
* 探索 [BigQuery DataFrames API 參考資料](https://dataframes.bigquery.dev/reference/index.html)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-24 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-24 (世界標準時間)。"],[],[]]