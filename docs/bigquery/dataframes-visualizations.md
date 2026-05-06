Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BigQuery DataFrames 繪製圖表

本文將示範如何使用 BigQuery DataFrames 視覺化程式庫，繪製各種圖表。

[`bigframes.pandas` API](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.html) 提供完整的 Python 工具生態系統。這項 API 支援進階統計作業，您可以將 BigQuery DataFrame 產生的匯總資料以視覺化方式呈現。您也可以從 BigQuery DataFrame 切換至 `pandas` DataFrame，並使用內建的取樣作業。

## 直方圖

下列範例會從 `bigquery-public-data.ml_datasets.penguins` 資料表讀取資料，繪製企鵝鳥喙深度的分布直方圖：

```
import bigframes.pandas as bpd

penguins = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
penguins["culmen_depth_mm"].plot.hist(bins=40)
```

## 折線圖

以下範例使用 `bigquery-public-data.noaa_gsod.gsod2021` 表格中的資料，繪製一年內中位數溫度變化的折線圖：

```
import bigframes.pandas as bpd

noaa_surface = bpd.read_gbq("bigquery-public-data.noaa_gsod.gsod2021")

# Calculate median temperature for each day
noaa_surface_median_temps = noaa_surface[["date", "temp"]].groupby("date").median()

noaa_surface_median_temps.plot.line()
```

## 面積圖

以下範例使用 `bigquery-public-data.usa_names.usa_1910_2013` 資料表追蹤美國歷史上名字的熱門程度，並著重於 `Mary`、`Emily` 和 `Lisa` 這幾個名字：

```
import bigframes.pandas as bpd

usa_names = bpd.read_gbq("bigquery-public-data.usa_names.usa_1910_2013")

# Count the occurences of the target names each year. The result is a dataframe with a multi-index.
name_counts = (
    usa_names[usa_names["name"].isin(("Mary", "Emily", "Lisa"))]
    .groupby(("year", "name"))["number"]
    .sum()
)

# Flatten the index of the dataframe so that the counts for each name has their own columns.
name_counts = name_counts.unstack(level=1).fillna(0)

name_counts.plot.area(stacked=False, alpha=0.5)
```

## 長條圖

以下範例使用 `bigquery-public-data.ml_datasets.penguins` 資料表，以視覺化方式呈現企鵝性別分布：

```
import bigframes.pandas as bpd

penguins = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")

penguin_count_by_sex = (
    penguins[penguins["sex"].isin(("MALE", "FEMALE"))]
    .groupby("sex")["species"]
    .count()
)
penguin_count_by_sex.plot.bar()
```

## 散布圖

以下範例使用 `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2021` 表格，探索計程車車資金額與行程距離之間的關係：

```
import bigframes.pandas as bpd

taxi_trips = bpd.read_gbq(
    "bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2021"
).dropna()

# Data Cleaning
taxi_trips = taxi_trips[
    taxi_trips["trip_distance"].between(0, 10, inclusive="right")
]
taxi_trips = taxi_trips[taxi_trips["fare_amount"].between(0, 50, inclusive="right")]

# If you are using partial ordering mode, you will also need to assign an order to your dataset.
# Otherwise, the next line can be skipped.
taxi_trips = taxi_trips.sort_values("pickup_datetime")

taxi_trips.plot.scatter(x="trip_distance", y="fare_amount", alpha=0.5)
```

## 將大型資料集視覺化

BigQuery DataFrames 會將資料下載至本機，以供視覺化。預設情況下，可下載的資料點數量上限為 1,000 個。如果資料點數量超過上限，BigQuery DataFrame 會隨機取樣，資料點數量等於上限。

如要覆寫這項上限，請在繪製圖表時設定 `sampling_n` 參數，如下列範例所示：

```
import bigframes.pandas as bpd

noaa_surface = bpd.read_gbq("bigquery-public-data.noaa_gsod.gsod2021")

# Calculate median temperature for each day
noaa_surface_median_temps = noaa_surface[["date", "temp"]].groupby("date").median()

noaa_surface_median_temps.plot.line(sampling_n=40)
```

**注意：** `sampling_n` 參數不會影響直方圖，因為 BigQuery DataFrames 會在伺服器端將資料分組，以產生直方圖。

## 使用 pandas 和 Matplotlib 參數繪製進階圖表

由於 BigQuery DataFrames 的繪圖程式庫是由 pandas 和 Matplotlib 提供支援，因此您可以傳入更多參數來微調圖表，就像使用 pandas 一樣。以下各節說明相關範例。

### 附有子圖的姓名熱門趨勢

使用[面積圖範例](#area-chart)中的名稱記錄資料，下列範例會在 `plot.area()` 函式呼叫中設定 `subplots=True`，為每個名稱建立個別圖表：

```
import bigframes.pandas as bpd

usa_names = bpd.read_gbq("bigquery-public-data.usa_names.usa_1910_2013")

# Count the occurences of the target names each year. The result is a dataframe with a multi-index.
name_counts = (
    usa_names[usa_names["name"].isin(("Mary", "Emily", "Lisa"))]
    .groupby(("year", "name"))["number"]
    .sum()
)

# Flatten the index of the dataframe so that the counts for each name has their own columns.
name_counts = name_counts.unstack(level=1).fillna(0)

name_counts.plot.area(subplots=True, alpha=0.5)
```

### 計程車行程的散佈圖，包含多個維度

使用[散布圖範例](#scatter-plot)中的資料，以下範例會重新命名 X 軸和 Y 軸的標籤、使用 `passenger_count` 參數設定點大小、使用 `tip_amount` 參數設定點顏色，以及調整圖表大小：

```
import bigframes.pandas as bpd

taxi_trips = bpd.read_gbq(
    "bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2021"
).dropna()

# Data Cleaning
taxi_trips = taxi_trips[
    taxi_trips["trip_distance"].between(0, 10, inclusive="right")
]
taxi_trips = taxi_trips[taxi_trips["fare_amount"].between(0, 50, inclusive="right")]

# If you are using partial ordering mode, you also need to assign an order to your dataset.
# Otherwise, the next line can be skipped.
taxi_trips = taxi_trips.sort_values("pickup_datetime")

taxi_trips["passenger_count_scaled"] = taxi_trips["passenger_count"] * 30

taxi_trips.plot.scatter(
    x="trip_distance",
    xlabel="trip distance (miles)",
    y="fare_amount",
    ylabel="fare amount (usd)",
    alpha=0.5,
    s="passenger_count_scaled",
    label="passenger_count",
    c="tip_amount",
    cmap="jet",
    colorbar=True,
    legend=True,
    figsize=(15, 7),
    sampling_n=1000,
)
```

## 後續步驟

* 瞭解 [BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/bigquery-dataframes-introduction?hl=zh-tw)。
* 瞭解如何[在 dbt 中使用 BigQuery DataFrames](https://docs.cloud.google.com/bigquery/docs/dataframes-dbt?hl=zh-tw)。
* 請參閱 [BigQuery DataFrames API 參考資料](https://dataframes.bigquery.dev/reference/index.html)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]