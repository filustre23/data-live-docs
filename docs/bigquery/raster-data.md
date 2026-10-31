Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 BigQuery 中使用 Earth Engine 處理光柵資料

使用 `ST_REGIONSTATS` 函式結合光柵和向量資料，即可計算特定地理區域的分區統計資料，例如平均空氣品質或火災風險。您可以直接在 BigQuery 中使用 Google Earth Engine，分析衛星圖像和天氣預報，以及現有的向量邊界。

## 總覽

「光柵」是二維像素網格，每個像素都會指派一或多個稱為「波段」的值。舉例來說，每個像素可能對應到地球表面上特定的一平方公里，並有平均溫度和平均降雨量的波段。光柵資料包括衛星圖像和其他連續的網格資料，例如天氣預報和土地覆蓋。許多常見的圖片格式 (例如 PNG 或 JPEG 檔案) 都是光柵資料。

光柵資料通常與「向量」資料相對，後者是以線條或曲線 (而非固定的矩形網格) 描述資料。舉例來說，您可以在 BigQuery 中使用 `GEOGRAPHY` 資料類型，描述國家/地區、城市或其他區域的邊界。

地理空間光柵和向量資料通常會使用*分區統計*作業合併，這項作業會計算指定向量區域內所有光柵值的匯總。例如，您可能想計算下列項目：

* 一組城市的平均空氣品質。
* 一組建築物多邊形的太陽能發電潛力。
* 林區輸電線走廊沿線的火災風險摘要。

BigQuery 擅長處理向量資料，Google Earth Engine 則擅長處理光柵資料。您可以使用 [`ST_REGIONSTATS` 地理函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_regionstats)，透過 Earth Engine 結合光柵資料與儲存在 BigQuery 的向量資料。

## 事前準備

1. 如要在查詢中使用 `ST_REGIONSTATS` 函式，請啟用 Earth Engine API。

   [啟用 API](https://console.cloud.google.com/apis/library/earthengine.googleapis.com?hl=zh-tw)
2. 選用：如要訂閱並使用透過 `ST_REGIONSTATS` 函式發布至 BigQuery sharing (舊稱 Analytics Hub) 的資料，請啟用 Analytics Hub API。

   [啟用 API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### 所需權限

如要取得呼叫 `ST_REGIONSTATS` 函式所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* [Earth Engine 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/earthengine?hl=zh-tw#earthengine.viewer)  (`roles/earthengine.viewer`)
* [服務使用情形消費者](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer)  (`roles/serviceusage.serviceUsageConsumer`)
* 訂閱 BigQuery sharing 資料集：[BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備呼叫 `ST_REGIONSTATS` 函式所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

必須具備下列權限，才能呼叫 `ST_REGIONSTATS` 函式：

* `earthengine.computations.create`
* `serviceusage.services.use`
* `bigquery.datasets.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 尋找光柵資料

`ST_REGIONSTATS` 函式中的 `raster_id` 參數是字串，用於指定光柵資料的來源。以下各節說明如何找出光柵 ID 並設定格式。

### BigQuery 圖片資料表

您可以使用 BigQuery sharing (舊稱 Analytics Hub)，在 BigQuery 中探索及存取光柵資料集。如要使用 BigQuery 共用功能，您必須[啟用 Analytics Hub API](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#before_you_begin)，並確認您具備[查看及訂閱項目和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)的必要權限。

Google Earth Engine 會發布公開資料集，其中包含 `US` 和 `EU` 多區域的光柵資料。如要[訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)含有光柵資料的 Earth Engine 資料集，請按照下列步驟操作：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「Sharing (Analytics Hub)」](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「search 搜尋產品資訊」。
3. 在「Search for listings」(搜尋產品) 欄位中輸入 `"Google Earth Engine"`。
4. 按一下要訂閱的資料集。
5. 點選「訂閱」。
6. 選用：更新「專案」或「連結的資料集名稱」欄位。
7. 按一下「儲存」。連結的資料集會新增至專案。

資料集包含*圖片資料表*，可根據 [STAC](https://stacspec.org/) 項目規格，儲存光柵圖片集合的中繼資料。圖片資料表類似於 Earth Engine 圖片集合 ([`ImageCollection`](https://developers.google.com/earth-engine/guides/ic_creating?hl=zh-tw))。

表格中的每一列都對應一張光柵圖片，資料欄則包含圖片屬性和中繼資料。每張圖片的光柵 ID 會儲存在 `assets.image.href` 欄中。在查詢中參照圖片時，請將這個 ID 做為 `raster_id` 參數值。

使用屬性欄篩選表格，選取符合條件的特定映像檔或映像檔子集。如要進一步瞭解可用的波段、像素大小和屬性定義，請開啟表格，然後按一下「Image details」(圖片詳細資料) 分頁標籤。

每個圖片資料表都包含對應的 `*_metadata` 資料表，提供圖片資料表的輔助資訊。

舉例來說，ERA5-Land 資料集提供每日氣候變數統計資料，並公開提供。`climate` 資料表包含多個光柵 ID。下列查詢會使用 `start_datetime` 欄篩選圖片資料表，取得 2025 年 1 月 1 日對應圖片的光柵 ID，並使用 `temperature_2m` 波段計算各國的平均溫度：

### SQL

```
WITH SimplifiedCountries AS (
  SELECT
    ST_SIMPLIFY(geometry, 10000) AS simplified_geometry,
    names.primary AS name
  FROM
    `bigquery-public-data.overture_maps.division_area`
  WHERE
    subtype = 'country'
)
SELECT
  sc.simplified_geometry AS geometry,
  sc.name,
  ST_REGIONSTATS(
    sc.simplified_geometry,
    (SELECT assets.image.href
    FROM `LINKED_DATASET_NAME.climate`
    WHERE start_datetime = '2025-01-01 00:00:00'),
    'temperature_2m'
  ).mean - 273.15 AS mean_temperature
FROM
  SimplifiedCountries AS sc
ORDER BY
  mean_temperature DESC;
```

### BigQuery DataFrames

在試用這個範例之前，請先按照「[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)」中的 BigQuery DataFrames 設定操作說明進行操作。詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

如要向 BigQuery 進行驗證，請設定應用程式預設憑證。
詳情請參閱「[為本機開發環境設定 ADC](https://docs.cloud.google.com/docs/authentication/set-up-adc-local-dev-environment?hl=zh-tw)」。

```
import datetime
from typing import cast

import bigframes.bigquery as bbq
import bigframes.pandas as bpd

# TODO: Set the project_id to your Google Cloud project ID.
# project_id = "your-project-id"
bpd.options.bigquery.project = project_id

# TODO: Set the dataset_id to the ID of the dataset that contains the
# `climate` table. This is likely a linked dataset to Earth Engine.
# See: https://cloud.google.com/bigquery/docs/link-earth-engine
linked_dataset = "era5_land_daily_aggregated"

# For the best efficiency, use partial ordering mode.
bpd.options.bigquery.ordering_mode = "partial"

# Load the table of country boundaries.
countries = bpd.read_gbq("bigquery-public-data.overture_maps.division_area")

# Filter to just the countries.
countries = countries[countries["subtype"] == "country"].copy()
countries["name"] = countries["names"].struct.field("primary")
countries["simplified_geometry"] = bbq.st_simplify(
    countries["geometry"],
    tolerance_meters=10_000,
)

# Get the reference to the temperature data from a linked dataset.
# Note: This sample assumes you have a linked dataset to Earth Engine.
image_href = (
    bpd.read_gbq(f"{project_id}.{linked_dataset}.climate")
    .set_index("start_datetime")
    .loc[[datetime.datetime(2025, 1, 1, tzinfo=datetime.timezone.utc)], :]
)
raster_id = image_href["assets"].struct.field("image").struct.field("href")
raster_id = raster_id.item()
stats = bbq.st_regionstats(
    countries["simplified_geometry"],
    raster_id=cast(str, raster_id),
    band="temperature_2m",
)

# Extract the mean and convert from Kelvin to Celsius.
countries["mean_temperature"] = stats.struct.field("mean") - 273.15

# Sort by the mean temperature to find the warmest countries.
result = countries[["name", "mean_temperature"]].sort_values(
    "mean_temperature", ascending=False
)
print(result.head(10))
```

### Cloud Storage GeoTIFF

GeoTIFF 是儲存地理空間光柵資料的常見檔案格式。`ST_REGIONSTATS` 函式支援以 [Cloud Optimized GeoTIFF](https://developers.google.com/earth-engine/Earth_Engine_asset_from_cloud_geotiff?hl=zh-tw) (COG) 格式儲存的點陣資料，這些資料位於下列區域的 Cloud Storage bucket：

* `US` 多地區
* `us-central1`
* `EU` 多地區
* `europe-west1`

提供 Cloud Storage URI 做為光柵 ID，例如 `gs://bucket/folder/raster.tif`。

### Earth Engine 圖片素材資源

`ST_REGIONSTATS` 函式支援傳遞 Earth Engine 圖片素材資源路徑做為 `raster_id` 引數。Earth Engine 光柵資料可以個別圖片或圖片集合的形式提供。這些資料位於 `US` 區域，且僅與在 `US` 區域執行的查詢相容。如要找出圖片的光柵 ID，請按照下列步驟操作：

1. 在 [Earth Engine 資料目錄](https://developers.google.com/earth-engine/datasets?hl=zh-tw)中搜尋感興趣的資料集。
2. 如要開啟該項目的說明頁面，請按一下資料集名稱。**Earth Engine 程式碼片段**會描述單一圖片或圖片集合。

   如果 Earth Engine 程式碼片段的格式為 `ee.Image('IMAGE_PATH')`，則光柵 ID 為 `'ee://IMAGE_PATH'`。

   如果 Earth Engine 程式碼片段的形式為 `ee.ImageCollection('IMAGE_COLLECTION_PATH')`，您可以使用 [Earth Engine 程式碼編輯器](https://developers.google.com/earth-engine/guides/quickstart_javascript?hl=zh-tw)，[將 ImageCollection 篩選](https://developers.google.com/earth-engine/guides/ic_filtering?hl=zh-tw)為單一圖片。使用 `ee.Image.get('system:id')` 方法，將該圖片的 `IMAGE_PATH` 值輸出至控制台。光柵 ID 為 `'ee://IMAGE_PATH'`。

## 像素權重

您可以為 `ST_REGIONSTATS` 函式中的 `include` 參數指定*權重* (有時稱為*遮罩值*)，決定計算時每個像素的權重。權重值必須介於 0 到 1 之間。
如果權重超出這個範圍，系統會將其設為最接近的限制值 (0 或 1)。

如果像素的權重大於 0，則視為*有效*。權重為 0 表示像素*無效*。無效像素通常代表資料遺失或不可靠，例如雲層遮蔽的區域、感應器異常、處理錯誤，或定義邊界以外的位置。

如未指定權重，系統會根據像素落在幾何圖形內的比例，自動為每個像素加權，以便按比例納入分區統計資料。如果幾何圖形小於像素大小的 1/256，像素的權重為 0。在這些情況下，除了 `count` 和 `area` 為 0 以外，所有統計資料都會傳回 `null`。

如果部分相交像素的權重介於 `include` 引數和 `ST_REGIONSTATS` 之間，BigQuery 會使用該權重和與區域相交的像素分數中的最小值。

權重值的精確度與 `FLOAT64` 值不同。在實際情況下，其真實值與計算中使用的值可能會有高達 1/256 (約 0.4%) 的差異。

您可以在 `include` 引數中使用 Earth Engine [圖片運算式語法](https://developers.google.com/earth-engine/guides/image_math?hl=zh-tw#expressions)提供運算式，根據光柵波段內的特定條件，動態調整像素權重。舉例來說，下列運算式會將計算範圍限制在 `probability` 波段超過 70% 的像素：

```
include => 'probability > 0.7'
```

如果資料集包含權重係數波段，您可以使用下列語法：

```
include => 'weight_factor_band_name'
```

## 像素大小和分析比例

地理空間光柵圖片是由像素組成的網格，對應地球表面的某個位置。光柵的像素大小 (有時稱為「比例」) 是指格線座標參照系統中，像素單邊的標稱大小。舉例來說，解析度為 10 公尺的光柵，像素大小為 10 公尺 x 10 公尺。各資料集原始回報的像素大小可能差異極大，從不到 1 公尺到超過 20 公里都有。

使用 `ST_REGIONSTATS` 函式計算分區統計資料時，光柵資料的像素大小是重要考量。舉例來說，匯總某個國家/地區的高解析度光柵資料，可能會耗用大量運算資源，且精細程度過高。相反地，匯總區域內的低解析度資料 (例如城市地塊)，可能無法提供足夠的詳細資料。

為取得有意義且有效率的分析結果，建議您根據多邊形大小和分析目標，選擇適當的像素大小。在 BigQuery sharing 功能的圖片資料表說明部分，可以找到每個光柵資料集的像素大小。

變更像素大小會改變與特定地理區域交集的像素數量，進而影響結果和解讀方式。不建議變更正式版分析的像素大小。不過，如果您正在設計查詢原型，增加像素大小可以縮短查詢執行時間並降低成本，尤其是高解析度資料。

如要變更像素大小，請將 `ST_REGIONSTATS` 函式的 `options` 引數設為 `scale`。舉例來說，如要計算 1,000 公尺像素的統計資料，請使用 `options => JSON '{"scale":1000}'`，指示 Earth Engine 按照要求的比例重新取樣圖片。如要進一步瞭解 Earth Engine 如何處理重新縮放，請參閱 Google Earth Engine 說明文件中的「[縮放](https://developers.google.com/earth-engine/guides/scale?hl=zh-tw)」一節。

如果多邊形明顯小於光柵像素，計算統計資料可能會產生不準確或空值結果。在這種情況下，其中一個替代方案是使用 [`ST_CENTROID`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_centroid) 將多邊形替換為其群集中心點。

## 帳單

執行查詢時，`ST_REGIONSTATS` 函式的使用費用會與查詢的其他部分分開計算，因為 Earth Engine 會計算函式呼叫的結果。無論您是採用隨選計費模式或預留項目，這類用量都會以 BigQuery 服務 SKU 的運算單元時數計費。如要查看 BigQuery 呼叫 Earth Engine 的計費金額，請[查看帳單報表](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw#overview)，並使用[標籤](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw#filter-by-labels)依標籤鍵 `goog-bq-feature-type` (值為 `EARTH_ENGINE`) 篩選。如果 `ST_REGIONSTATS` 函式失敗，系統不會向您收取任何 Earth Engine 運算費用。

針對每項查詢，您可以使用 BigQuery API 中的 [`jobs.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)查看下列資訊：

* [`slotMs` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#externalservicecost)：當 `externalService` 欄位為 `EARTH_ENGINE`，且 `billingMethod` 欄位為 `SERVICES_SKU` 時，顯示 Earth Engine 耗用的運算單元時間 (毫秒)。
* [`totalServicesSkuSlotMs` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2)：顯示所有 BigQuery 外部服務使用的運算單元毫秒總數，這些服務會依 BigQuery 服務 SKU 計費。

您也可以查詢 [`INFORMATION_SCHEMA.JOBS` 檢視表](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)中的 `total_services_sku_slot_ms` 欄位，找出外部服務耗用的總運算單元毫秒數，並依 BigQuery 服務 SKU 計費。

### 費用因素

執行 `ST_REGIONSTATS` 函式時，下列因素會影響運算用量：

* 輸入資料列數。
* 您使用的光柵圖片。部分光柵是由 Earth Engine Data Catalog 中的來源圖片集合建立的複合資料，而產生複合結果所需的運算資源不盡相同。
* 圖片解析度。
* 輸入地理區的大小和複雜程度、與地理區交集的像素數量，以及 Earth Engine 讀取的圖片圖塊和位元組數量。
* 輸入地理位置在地球上相對於來源圖片的位置，以及圖片的投影和解析度。

  + 圖片投影可能會扭曲像素，尤其是高緯度或遠超出圖片預期涵蓋範圍的像素。
  + 如果是複合光柵，與輸入地理區域交集的來源圖片數量，可能會因區域和時間而異。舉例來說，部分衛星會根據軌道和資料收集參數，在低緯度或高緯度地區產生更多圖片，或根據不斷變化的大氣條件省略圖片。
* 在 `include` 或 `band_name` 引數中使用公式，以及公式涉及的波段數量。
* 快取先前的結果。

### 控管費用

如要控管與 `ST_REGIONSTATS` 函式相關的費用，您可以調整配額，控管函式可使用的運算單元時間。預設為每天 350 個運算單元小時。[查看配額](https://docs.cloud.google.com/docs/quotas/view-manage?hl=zh-tw)時，請將「Metric」(指標) 清單篩選為 `earthengine.googleapis.com/bigquery_slot_usage_time`，查看與 BigQuery 呼叫相關的 Earth Engine 配額。詳情請參閱 Google Earth Engine 說明文件中的 [BigQuery 光柵函式配額](https://developers.google.com/earth-engine/guides/usage?hl=zh-tw#bigquery_slot-time_per_day)。

**注意：** 與 BigQuery 中的自訂查詢配額一樣，這項配額也是約略值。這項功能可防止支出過多，但並非用於嚴格限制運算單元時間。BigQuery 有時可能會執行超出配額限制的查詢，您可能會用盡配額，但不會依據全部用量付費。

## 支援的地區

呼叫 `ST_REGIONSTATS` 函式的查詢必須在下列其中一個區域執行：

* `US` 多地區
* `us-central1`
* `us-central2`
* `EU` 多地區
* `europe-west1`

## 後續步驟

* 試試這個教學課程，瞭解如何[使用光柵資料分析溫度](https://docs.cloud.google.com/bigquery/docs/raster-tutorial-weather?hl=zh-tw)。
* 進一步瞭解 [BigQuery 的地理函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)。
* 進一步瞭解如何[使用地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-30 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-30 (世界標準時間)。"],[],[]]