Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BigQuery DataFrames 建立圖表

您可以使用 BigQuery DataFrames 視覺化程式庫繪製各種圖表，以視覺化方式探索及瞭解資料。[`bigframes.pandas` API](https://dataframes.bigquery.dev/reference/api/bigframes.pandas.html) 可讓您將進階統計運算與熟悉的 Python 繪圖工具完美結合，包括大型資料集的內建取樣功能。

## 直方圖

以下範例會從 `bigquery-public-data.ml_datasets.penguins` 資料表讀取資料，繪製企鵝嘴峰深度的分布直方圖：

```
import bigframes.pandas as bpd

penguins = bpd.read_gbq("bigquery-public-data.ml_datasets.penguins")
penguins["culmen_depth_mm"].plot.hist(bins=40)
```

## 折線圖

以下範例使用 `bigquery-public-data.noaa_gsod.gsod2021` 資料表中的資料，繪製全年溫度中位數變化的折線圖：

```
import bigframes.pandas as bpd

noaa_surface = bpd.read_gbq("bigquery-public-data.noaa_gsod.gsod2021")

# Calculate median temperature for each day
noaa_surface_median_temps = noaa_surface[["date", "temp"]].groupby("date").median()

noaa_surface_median_temps.plot.line()
```

## 面積圖

以下範例使用 `bigquery-public-data.usa_names.usa_1910_2013` 資料表追蹤美國歷史上的姓名熱門程度，並著重於 `Mary`、`Emily` 和 `Lisa` 這三個姓名：

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

下列範例使用 `bigquery-public-data.ml_datasets.penguins` 資料表，以視覺化方式呈現企鵝性別分布：

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

以下範例使用 `bigquery-public-data.new_york_taxi_trips.tlc_yellow_trips_2021` 資料表，探索計程車車資金額與行程距離之間的關係：

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

## 以圖表呈現大型資料集

BigQuery DataFrames 會將資料下載到本機電腦，以便進行視覺化。根據預設，可下載的資料點數量上限為 1,000。如果資料點數量超過上限，BigQuery DataFrames 會隨機取樣，數量等於上限。

如要覆寫這項上限，請在繪製圖表時設定 `sampling_n` 參數，如以下範例所示：

```
import bigframes.pandas as bpd

noaa_surface = bpd.read_gbq("bigquery-public-data.noaa_gsod.gsod2021")

# Calculate median temperature for each day
noaa_surface_median_temps = noaa_surface[["date", "temp"]].groupby("date").median()

noaa_surface_median_temps.plot.line(sampling_n=40)
```

**注意：** `sampling_n` 參數對直方圖沒有影響，因為 BigQuery DataFrames 會在伺服器端為直方圖建立資料 bucket。

## 使用 pandas 和 Matplotlib 參數進行進階繪圖

您可以傳入更多參數，像使用 pandas 一樣微調圖表，因為 BigQuery DataFrames 的繪圖程式庫是由 pandas 和 Matplotlib 提供。以下各節將說明範例。

### 名字熱門程度趨勢 (含子圖表)

以下範例使用[面積圖範例](#area-chart)中的名稱歷來資料，在 `plot.area()` 函式呼叫中設定 `subplots=True`，為每個名稱建立個別圖表：

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

### 計程車行程散布圖 (含多個維度)

以下範例使用[散布圖範例](#scatter-plot)中的資料，重新命名 x 軸和 y 軸的標籤、使用 `passenger_count` 參數設定點大小、使用 `tip_amount` 參數設定顏色點，並調整圖表大小：

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
* 探索 [BigQuery DataFrames API 參考資料](https://dataframes.bigquery.dev/reference/index.html)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-29 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-29 (世界標準時間)。"],[],[]]