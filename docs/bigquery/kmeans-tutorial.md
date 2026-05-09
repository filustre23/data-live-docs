Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 建立 k-means 模型，將倫敦自行車租用資料集分群 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程將說明如何使用 BigQuery ML 中的 [k-means 模型](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create-kmeans?hl=zh-tw)，找出資料集中的叢集。

將資料分組到叢集的 [k-means](https://en.wikipedia.org/wiki/K-means_clustering) 演算法，是一種非監督式機器學習。監督式機器學習是關於預測性分析，而非監督式機器學習著重在敘述性分析。非監督式機器學習可協助您瞭解資料，進而做出資料導向的決策。

本教學課程中的查詢使用地理空間分析服務提供的[地理位置函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)，詳情請參閱「[地理空間分析簡介](https://docs.cloud.google.com/bigquery/docs/gis-intro?hl=zh-tw)」。

本教學課程使用[倫敦自行車租用公開資料集](https://console.cloud.google.com/marketplace/details/greater-london-authority/london-bicycles?filter=solution-type%3Adataset&%3Bid=95374cac-2834-4fa2-a71f-fc033ccb5ce4&hl=zh-tw)。資料包括租用開始和結束的時間戳記、車站名稱，以及騎乘時間。

## 目標

本教學課程會逐步引導您完成下列工作：

* 檢查用於訓練模型的資料。
* 建立 k-means 分群模型。
* 使用 BigQuery ML 的叢集視覺化功能，解讀產生的資料叢集。
* 在 k-means 模型上執行 [`ML.PREDICT` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-predict?hl=zh-tw)，預測一組自行車租借站可能屬於哪個叢集。

## 費用

本教學課程使用 Google Cloud的計費元件，包括：

* BigQuery
* BigQuery ML

如要瞭解 BigQuery 費用，請參閱 [BigQuery 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw)頁面。

如要瞭解 BigQuery ML 費用，請參閱 [BigQuery ML 定價](https://cloud.google.com/bigquery/pricing?hl=zh-tw#bqml)。

## 事前準備

- 登入 Google Cloud 帳戶。如果您是 Google Cloud新手，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自評估產品在實際工作環境中的成效。新客戶還能獲得價值 $300 美元的免費抵免額，可用於執行、測試及部署工作負載。
- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).

- In the Google Cloud console, on the project selector page,
  select or create a Google Cloud project.

  **Roles required to select or create a project**

  * **Select a project**: Selecting a project doesn't require a specific
    IAM role—you can select any project that you've been
    granted a role on.
  * **Create a project**: To create a project, you need the Project Creator role
    (`roles/resourcemanager.projectCreator`), which contains the
    `resourcemanager.projects.create` permission. [Learn how to grant
    roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).
  **Note**: If you don't plan to keep the
  resources that you create in this procedure, create a project instead of
  selecting an existing project. After you finish these steps, you can
  delete the project, removing all resources associated with the project.

  [Go to project selector](https://console.cloud.google.com/projectselector2/home/dashboard?hl=zh-tw)
- [Verify that billing is enabled for your Google Cloud project](https://docs.cloud.google.com/billing/docs/how-to/verify-billing-enabled?hl=zh-tw#confirm_billing_is_enabled_on_a_project).

1. 新專案會自動啟用 BigQuery。如要在現有專案中啟用 BigQuery，請前往

   啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery&hl=zh-tw)

## 所需權限

* 如要建立資料集，您需要 `bigquery.datasets.create` IAM 權限。
* 如要建立模型，您需要下列權限：

  + `bigquery.jobs.create`
  + `bigquery.models.create`
  + `bigquery.models.getData`
  + `bigquery.models.updateData`
* 如要執行推論，您需要下列權限：

  + `bigquery.models.getData`
  + `bigquery.jobs.create`

如要進一步瞭解 BigQuery 中的 IAM 角色和權限，請參閱「[IAM 簡介](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

## 建立資料集

建立 BigQuery 資料集來儲存 k-means 模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中，按一下專案名稱。
4. 依序點按 more\_vert「View actions」(查看動作) >「Create dataset」(建立資料集)。
5. 在「建立資料集」頁面中，執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `bqml_tutorial`。
   * 針對「Location type」(位置類型) 選取「Multi-region」(多區域)，然後選取「EU (multiple regions in European Union)」(歐盟 (多個歐盟區域))。

     倫敦自行車租用公開資料集存放在 `EU`
     [多地區](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)。資料集必須位於相同位置。
   * 其餘設定請保留預設狀態，然後按一下「建立資料集」。

## 檢查訓練資料

檢查要用來訓練 k-means 模型的資料。在本教學課程中，您將根據下列屬性來將自行車站分群：

* 租用時間
* 每日租用次數
* 距市中心的距離

### SQL

這項查詢會擷取自行車的租用資料，包括 `start_station_name` 和 `duration` 資料欄，並將這項資料與車站資訊結合。包括建立計算結果欄，其中包含車站與市中心的距離。然後，查詢會計算 `stationstats` 資料欄中的車站屬性 (包括平均騎乘時間和租用次數)，以及計算出的 `distance_from_city_center` 資料欄。

請按照下列步驟檢查訓練資料：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   WITH
   hs AS (
     SELECT
       h.start_station_name AS station_name,
       IF(
         EXTRACT(DAYOFWEEK FROM h.start_date) = 1
           OR EXTRACT(DAYOFWEEK FROM h.start_date) = 7,
         'weekend',
         'weekday') AS isweekday,
       h.duration,
       ST_DISTANCE(ST_GEOGPOINT(s.longitude, s.latitude), ST_GEOGPOINT(-0.1, 51.5)) / 1000
         AS distance_from_city_center
     FROM
       `bigquery-public-data.london_bicycles.cycle_hire` AS h
     JOIN
       `bigquery-public-data.london_bicycles.cycle_stations` AS s
       ON
         h.start_station_id = s.id
     WHERE
       h.start_date
       BETWEEN CAST('2015-01-01 00:00:00' AS TIMESTAMP)
       AND CAST('2016-01-01 00:00:00' AS TIMESTAMP)
   ),
   stationstats AS (
     SELECT
       station_name,
       isweekday,
       AVG(duration) AS duration,
       COUNT(duration) AS num_trips,
       MAX(distance_from_city_center) AS distance_from_city_center
     FROM
       hs
     GROUP BY
       station_name, isweekday
   )
   SELECT *
   FROM
   stationstats
   ORDER BY
   distance_from_city_center ASC;
   ```

結果應如下所示：

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import datetime
import typing

import pandas as pd
from shapely.geometry import Point

import bigframes
import bigframes.bigquery as bbq
import bigframes.geopandas
import bigframes.pandas as bpd

bigframes.options.bigquery.project = your_gcp_project_id
# Compute in the EU multi-region to query the London bicycles dataset.
bigframes.options.bigquery.location = "EU"

# Extract the information you'll need to train the k-means model in this
# tutorial. Use the read_gbq function to represent cycle hires
# data as a DataFrame.
h = bpd.read_gbq(
    "bigquery-public-data.london_bicycles.cycle_hire",
    col_order=["start_station_name", "start_station_id", "start_date", "duration"],
).rename(
    columns={
        "start_station_name": "station_name",
        "start_station_id": "station_id",
    }
)

# Use GeoSeries.from_xy and BigQuery.st_distance to analyze geographical
# data. These functions determine spatial relationships between
# geographical features.
cycle_stations = bpd.read_gbq("bigquery-public-data.london_bicycles.cycle_stations")
s = bpd.DataFrame(
    {
        "id": cycle_stations["id"],
        "xy": bigframes.geopandas.GeoSeries.from_xy(
            cycle_stations["longitude"], cycle_stations["latitude"]
        ),
    }
)
s_distance = bbq.st_distance(s["xy"], Point(-0.1, 51.5), use_spheroid=False) / 1000
s = bpd.DataFrame({"id": s["id"], "distance_from_city_center": s_distance})

# Define Python datetime objects in the UTC timezone for range comparison,
# because BigQuery stores timestamp data in the UTC timezone.
sample_time = datetime.datetime(2015, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)
sample_time2 = datetime.datetime(2016, 1, 1, 0, 0, 0, tzinfo=datetime.timezone.utc)

h = h.loc[(h["start_date"] >= sample_time) & (h["start_date"] <= sample_time2)]

# Replace each day-of-the-week number with the corresponding "weekday" or
# "weekend" label by using the Series.map method.
h = h.assign(
    isweekday=h.start_date.dt.dayofweek.map(
        {
            0: "weekday",
            1: "weekday",
            2: "weekday",
            3: "weekday",
            4: "weekday",
            5: "weekend",
            6: "weekend",
        }
    )
)

# Supplement each trip in "h" with the station distance information from
# "s" by merging the two DataFrames by station ID.
merged_df = h.merge(
    right=s,
    how="inner",
    left_on="station_id",
    right_on="id",
)

# Engineer features to cluster the stations. For each station, find the
# average trip duration, number of trips, and distance from city center.
stationstats = typing.cast(
    bpd.DataFrame,
    merged_df.groupby(["station_name", "isweekday"]).agg(
        {"duration": ["mean", "count"], "distance_from_city_center": "max"}
    ),
)
stationstats.columns = pd.Index(
    ["duration", "num_trips", "distance_from_city_center"]
)
stationstats = stationstats.sort_values(
    by="distance_from_city_center", ascending=True
).reset_index()

# Expected output results: >>> stationstats.head(3)
# station_name	isweekday duration  num_trips	distance_from_city_center
# Borough Road...	weekday	    1110	    5749	    0.12624
# Borough Road...	weekend	    2125	    1774	    0.12624
# Webber Street...	weekday	    795	        6517	    0.164021
#   3 rows × 5 columns
```

## 建立 k-means 模型

使用倫敦自行車租用訓練資料建立 k-means 模型。

### SQL

在下列查詢中，`CREATE MODEL` 陳述式會指定要使用的叢集數量 (四個)。在 `SELECT` 陳述式中，`EXCEPT` 子句會排除 `station_name` 資料欄，因為這個資料欄不含特徵。該查詢會為每個 station\_name 建立專屬的資料列，至於 `SELECT` 陳述式中則僅會納入特徵。

請按照下列步驟建立 k-means 模型：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   CREATE OR REPLACE MODEL `bqml_tutorial.london_station_clusters`
   OPTIONS (
     model_type = 'kmeans',
     num_clusters = 4)
   AS
   WITH
   hs AS (
     SELECT
       h.start_station_name AS station_name,
       IF(
         EXTRACT(DAYOFWEEK FROM h.start_date) = 1
           OR EXTRACT(DAYOFWEEK FROM h.start_date) = 7,
         'weekend',
         'weekday') AS isweekday,
       h.duration,
       ST_DISTANCE(ST_GEOGPOINT(s.longitude, s.latitude), ST_GEOGPOINT(-0.1, 51.5)) / 1000
         AS distance_from_city_center
     FROM
       `bigquery-public-data.london_bicycles.cycle_hire` AS h
     JOIN
       `bigquery-public-data.london_bicycles.cycle_stations` AS s
       ON
         h.start_station_id = s.id
     WHERE
       h.start_date
       BETWEEN CAST('2015-01-01 00:00:00' AS TIMESTAMP)
       AND CAST('2016-01-01 00:00:00' AS TIMESTAMP)
   ),
   stationstats AS (
     SELECT
       station_name,
       isweekday,
       AVG(duration) AS duration,
       COUNT(duration) AS num_trips,
       MAX(distance_from_city_center) AS distance_from_city_center
     FROM
       hs
     GROUP BY
       station_name, isweekday
   )
   SELECT *
   EXCEPT (station_name, isweekday)
   FROM
   stationstats;
   ```

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
from bigframes.ml.cluster import KMeans

# To determine an optimal number of clusters, construct and fit several
# K-Means objects with different values of num_clusters, find the error
# measure, and pick the point at which the error measure is at its minimum
# value.
cluster_model = KMeans(n_clusters=4)
cluster_model.fit(stationstats)
cluster_model.to_gbq(
    your_model_id,  # For example: "bqml_tutorial.london_station_clusters"
    replace=True,
)
```

## 解讀資料叢集

模型「評估」分頁中的資訊有助於解讀模型產生的叢集。

如要查看模型的評估資訊，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Datasets」(資料集)。
4. 按一下「`bqml_tutorial`」資料集，然後前往「模型」分頁。
5. 選取「`london_station_clusters`」模型。
6. 選取「評估」分頁標籤。這個分頁會顯示 k-means 模型識別出的叢集。在「數值特徵」部分，長條圖會顯示每個群集中心最重要的數值特徵值。每個群集中心代表一組資料叢集。您可以從下拉式選單中選取要顯示的特徵。

   這個模型會建立下列質心：

   * 重心 1 顯示較不繁忙的市區車站，租借時間較短。
   * 重心 2 顯示第二個城市車站，這個車站較不繁忙，且租用時間較長。
   * 群集中心 3 顯示靠近市中心的繁忙城市車站。
   * 重心 4 顯示郊區車站，騎乘時間較長。

   如果您經營自行車租賃業務，就可以根據這項資訊制定業務決策。例如：

   * 假設您需要實驗某個新的鎖，您應該要選擇哪個車站叢集來做為實驗對象呢？重心 1、重心 2 或重心 4 中的車站似乎是合乎邏輯的選擇，因為這些車站並非最繁忙的車站。
   * 假設您想要在某些車站擺放競速自行車，您應該要選擇哪些車站呢？質心 4 是距市中心最遠的車站群組，且騎乘距離最長。因此這些可以成為擺放競速自行車的候選車站。

## 使用 `ML.PREDICT` 函式預測車站的叢集

使用 `ML.PREDICT` SQL 函式或 [`predict` BigQuery DataFrames 函式](https://dataframes.bigquery.dev/reference/api/bigframes.ml.cluster.KMeans.html#bigframes.ml.cluster.KMeans.predict)，找出特定車站所屬的叢集。

### SQL

下列查詢會使用 [`REGEXP_CONTAINS`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/string_functions?hl=zh-tw#regexp_contains) 函式，找出 `station_name` 資料欄中包含字串 `Kennington` 的所有項目。`ML.PREDICT` 函式會使用這些值，來預測哪些叢集可能包含這些車站。

如要預測每個名稱有「`Kennington`」字串的車站所屬的叢集，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在查詢編輯器中貼入下列查詢，然後點選「執行」：

   ```
   WITH
   hs AS (
     SELECT
       h.start_station_name AS station_name,
       IF(
         EXTRACT(DAYOFWEEK FROM h.start_date) = 1
           OR EXTRACT(DAYOFWEEK FROM h.start_date) = 7,
         'weekend',
         'weekday') AS isweekday,
       h.duration,
       ST_DISTANCE(ST_GEOGPOINT(s.longitude, s.latitude), ST_GEOGPOINT(-0.1, 51.5)) / 1000
         AS distance_from_city_center
     FROM
       `bigquery-public-data.london_bicycles.cycle_hire` AS h
     JOIN
       `bigquery-public-data.london_bicycles.cycle_stations` AS s
       ON
         h.start_station_id = s.id
     WHERE
       h.start_date
       BETWEEN CAST('2015-01-01 00:00:00' AS TIMESTAMP)
       AND CAST('2016-01-01 00:00:00' AS TIMESTAMP)
   ),
   stationstats AS (
     SELECT
       station_name,
       isweekday,
       AVG(duration) AS duration,
       COUNT(duration) AS num_trips,
       MAX(distance_from_city_center) AS distance_from_city_center
     FROM
       hs
     GROUP BY
       station_name, isweekday
   )
   SELECT *
   EXCEPT (nearest_centroids_distance)
   FROM
   ML.PREDICT(
     MODEL `bqml_tutorial.london_station_clusters`,
     (
       SELECT *
       FROM
         stationstats
       WHERE
         REGEXP_CONTAINS(station_name, 'Kennington')
     ));
   ```

結果應如下所示。

### BigQuery DataFrames

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
# Select model you'll use for predictions. `read_gbq_model` loads model
# data from BigQuery, but you could also use the `cluster_model` object
# from previous steps.
cluster_model = bpd.read_gbq_model(
    your_model_id,
    # For example: "bqml_tutorial.london_station_clusters",
)

# Use 'contains' function to filter by stations containing the string
# "Kennington".
stationstats = stationstats.loc[
    stationstats["station_name"].str.contains("Kennington")
]

result = cluster_model.predict(stationstats)

# Expected output results:   >>>results.peek(3)
# CENTROID...	NEAREST...	station_name  isweekday	 duration num_trips dist...
# 	1	[{'CENTROID_ID'...	Borough...	  weekday	  1110	    5749	0.13
# 	2	[{'CENTROID_ID'...	Borough...	  weekend	  2125      1774	0.13
# 	1	[{'CENTROID_ID'...	Webber...	  weekday	  795	    6517	0.16
#   3 rows × 7 columns
```

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者您可以保留專案並刪除資料集。

### 刪除資料集

刪除專案將移除專案中所有的資料集與資料表。若您希望重新使用專案，您可以刪除本教學課程中所建立的資料集。

1. 如有必要，請在Google Cloud 控制台中開啟 BigQuery 頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在導覽窗格中，按一下您建立的 **bqml\_tutorial** 資料集。
3. 按一下視窗右側的「刪除資料集」。
   這個動作會刪除資料集和模型。
4. 在「Delete dataset」(刪除資料集) 對話方塊中，輸入資料集的名稱 (`bqml_tutorial`)，然後按一下「Delete」(刪除) 來確認刪除指令。

### 刪除專案

如要刪除專案，請進行以下操作：

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

## 後續步驟

* 如需 BigQuery ML 的總覽，請參閱 [BigQuery ML 簡介](https://docs.cloud.google.com/bigquery/docs/bqml-introduction?hl=zh-tw)。
* 如要瞭解如何建立模型，請參閱 [`CREATE MODEL`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/bigqueryml-syntax-create?hl=zh-tw) 語法頁面。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-08 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-08 (世界標準時間)。"],[],[]]