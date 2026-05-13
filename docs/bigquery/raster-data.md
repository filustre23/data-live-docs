Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 BigQuery 中使用 Earth Engine 處理光柵資料

本文說明如何使用 [`ST_REGIONSTATS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_regionstats)合併光柵和向量資料，該函式會使用 Google Earth Engine 存取 BigQuery 中的圖片和光柵資料。

## 總覽

*點陣*是像素的二維格線，每個像素都會指派一或多個稱為「波段」的值。舉例來說，每個像素可能對應到地表上特定的一平方公里，並包含平均溫度和平均降雨量的頻帶。點陣資料包括衛星圖像和其他連續的格線資料，例如天氣預報和土地覆蓋。許多常見的圖片格式 (例如 PNG 或 JPEG 檔案) 都是光柵資料格式。

點陣資料通常與*向量*資料形成對比，後者是以線條或曲線描述資料，而非固定矩形格線。舉例來說，您可以在 BigQuery 中使用 `GEOGRAPHY` 資料型別，描述國家/地區、城市或其他區域的邊界。

地理空間光柵和向量資料通常會使用「區域統計」作業合併，這項作業會計算指定向量區域內所有光柵值的匯總。舉例來說，您可能想計算下列項目：

* 一系列城市中的平均空氣品質。
* 一組建築物多邊形的太陽能發電潛能。
* 森林地區輸電線路走廊的火災風險摘要。

BigQuery 擅長處理向量資料，Google Earth Engine 則擅長處理光柵資料。您可以使用 [`ST_REGIONSTATS` 地理函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_regionstats)，將 Earth Engine 的點陣資料與儲存在 BigQuery 中的向量資料合併。

## 事前準備

1. 如要在查詢中使用 `ST_REGIONSTATS` 函式，請啟用 Earth Engine API。

   [啟用 API](https://console.cloud.google.com/apis/library/earthengine.googleapis.com?hl=zh-tw)
2. 選用：如要使用 `ST_REGIONSTATS` 函式訂閱及使用發布至 BigQuery sharing (舊稱 Analytics Hub) 的資料，請啟用 Analytics Hub API。

   [啟用 API](https://console.cloud.google.com/apis/library/analyticshub.googleapis.com?hl=zh-tw)

### 所需權限

如要取得呼叫 `ST_REGIONSTATS` 函式所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* [Earth Engine 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/earthengine?hl=zh-tw#earthengine.viewer)  (`roles/earthengine.viewer`)
* [服務使用情形消費者](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer)  (`roles/serviceusage.serviceUsageConsumer`)
* 訂閱 BigQuery sharing 資料集：
  [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備呼叫 `ST_REGIONSTATS` 函式所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要呼叫 `ST_REGIONSTATS` 函式，必須具備下列權限：

* `earthengine.computations.create`
* `serviceusage.services.use`
* `bigquery.datasets.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 尋找光柵資料

`ST_REGIONSTATS` 函式中的 `raster_id` 參數是字串，用於指定點陣資料的來源。以下各節說明如何尋找及設定點陣 ID 格式。

### BigQuery 圖片資料表

您可以使用 BigQuery sharing (舊稱 Analytics Hub) 探索及存取 BigQuery 中的點陣資料集。如要使用 BigQuery sharing，請[啟用 Analytics Hub API](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw#before_you_begin)，並確認您具備[查看及訂閱項目和資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw)的必要權限。

Google Earth Engine 會發布公開資料集，其中包含 `US` 和 `EU` 多區域的光柵資料。如要[訂閱](https://docs.cloud.google.com/bigquery/docs/analytics-hub-view-subscribe-listings?hl=zh-tw#subscribe-listings)含有點陣資料的 Earth Engine 資料集，請按照下列步驟操作：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「搜尋房源」search。
3. 在「Search for listings」(搜尋房源) 欄位中輸入 `"Google Earth Engine"`。
4. 按一下要訂閱的資料集。
5. 按一下「訂閱」。
6. 選用：更新「專案」或「連結的資料集名稱」欄位。
7. 按一下 [儲存]。連結的資料集會新增至專案。

資料集包含*圖片資料表*，其中儲存一系列點陣圖像的中繼資料，並遵循 [STAC](https://stacspec.org/) 項目規格。影像表格類似於 Earth Engine 影像集合 ([`ImageCollection`](https://developers.google.com/earth-engine/guides/ic_creating?hl=zh-tw))。

表格中的每一列都對應單一點陣圖像，欄位則包含圖像屬性和中繼資料。每張圖片的點陣 ID 會儲存在 `assets.image.href` 欄中。在查詢中使用這個 ID 做為 `raster_id` 參數值，即可參照圖片。

使用屬性欄篩選表格，選取符合條件的特定圖片或圖片子集。如要進一步瞭解可用波段、像素大小和屬性定義，請開啟表格並按一下「圖片詳細資料」分頁標籤。

每個圖片資料表都包含對應的 `*_metadata` 資料表，提供圖片資料表的輔助資訊。

舉例來說，ERA5-Land 資料集提供每日氣候變數統計資料，且開放大眾使用。`climate`
表格含有多個點陣 ID。下列查詢會使用 `start_datetime` 欄篩選圖片資料表，取得 2025 年 1 月 1 日對應圖片的光柵 ID，並使用 `temperature_2m` 頻帶計算每個國家/地區的平均溫度：

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

在嘗試這個範例之前，請按照[使用 BigQuery DataFrames 的 BigQuery 快速入門導覽課程](https://docs.cloud.google.com/bigquery/docs/dataframes-quickstart?hl=zh-tw)中的 BigQuery DataFrames 設定說明操作。
詳情請參閱 [BigQuery DataFrames 參考文件](https://docs.cloud.google.com/python/docs/reference/bigframes/latest?hl=zh-tw)。

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

GeoTIFF 是儲存地理空間點陣資料的常見檔案格式。`ST_REGIONSTATS` 函式支援以[雲端最佳化 GeoTIFF](https://developers.google.com/earth-engine/Earth_Engine_asset_from_cloud_geotiff?hl=zh-tw) (COG) 格式儲存在 Cloud Storage 值區中的點陣資料，這些值區位於下列區域：

* `US` 多地區
* `us-central1`
* `EU` 多地區
* `europe-west1`

將 Cloud Storage URI 做為點陣 ID 提供，例如 `gs://bucket/folder/raster.tif`。

### Earth Engine 圖片資產

`ST_REGIONSTATS` 函式支援傳遞 Earth Engine 圖片素材資源路徑做為 `raster_id` 引數。Earth Engine 點陣資料可做為個別圖片或圖片集合使用。這些資料位於 `US` 區域，且僅與在 `US` 區域執行的查詢相容。如要找出圖片的點陣 ID，請按照下列步驟操作：

1. 在 [Earth Engine 資料目錄](https://developers.google.com/earth-engine/datasets?hl=zh-tw)中搜尋您感興趣的資料集。
2. 如要開啟該項目的說明頁面，請按一下資料集名稱。
   **Earth Engine 片段**會說明單一圖片或圖片集合。

   如果 Earth Engine 片段的格式為 `ee.Image('IMAGE_PATH')`，則點陣 ID 為 `'ee://IMAGE_PATH'`。

   如果 Earth Engine 片段採用 `ee.ImageCollection('IMAGE_COLLECTION_PATH')` 形式，您可以使用 [Earth Engine 程式碼編輯器](https://developers.google.com/earth-engine/guides/quickstart_javascript?hl=zh-tw)，將 [ImageCollection 篩選為單一圖片](https://developers.google.com/earth-engine/guides/ic_filtering?hl=zh-tw)。使用 `ee.Image.get('system:id')` 方法將該圖片的 `IMAGE_PATH` 值列印到控制台。點陣 ID 為 `'ee://IMAGE_PATH'`。

## 像素權重

您可以為 `ST_REGIONSTATS` 函式中的 `include` 參數指定*權重* (有時稱為*遮罩值*)，決定計算時每個像素的權重。權重值必須介於 0 到 1 之間。
如果權重超出這個範圍，系統會將權重設為最接近的限制值 (0 或 1)。

如果像素的權重大於 0，系統就會將其視為*有效*。權重為 0 表示像素*無效*。
無效像素通常代表資料遺漏或不可靠，例如雲層遮蔽的區域、感應器異常、處理錯誤，或是位於定義邊界外的地點。

如未指定權重，系統會根據像素落入幾何圖形內的比例，自動為每個像素加權，以便按比例納入區域統計資料。如果幾何體小於像素大小的 1/256，像素的權重為 0。在這些情況下，除了 `count` 和 `area` 以外，所有統計資料都會傳回 `null`，這兩項資料則會傳回 0。

如果部分相交的像素具有 `include` 引數的權重 (適用於 `ST_REGIONSTATS`)，則 BigQuery 會使用該權重和與區域相交的像素分數中的最小值。

權重值的精確度與 `FLOAT64` 值不同。在實務上，這些值的實際值與計算中使用的值最多可能相差 1/256 (約 0.4%)。

您可以在 `include` 引數中，使用 Earth Engine [影像運算式語法](https://developers.google.com/earth-engine/guides/image_math?hl=zh-tw#expressions)提供運算式，根據點陣帶中的特定條件，動態加權像素。舉例來說，下列運算式會將計算限制在 `probability` 波段超過 70% 的像素：

```
include => 'probability > 0.7'
```

如果資料集包含權重因數頻帶，您可以使用下列語法：

```
include => 'weight_factor_band_name'
```

## 像素大小和分析規模

地理空間點陣圖像是由像素格線組成，對應地球表面的某個位置。點陣的像素大小 (有時稱為「比例」) 是格線座標參考系統中，像素一側的名義大小。舉例來說，解析度為 10 公尺的點陣圖，像素大小為 10 公尺 x 10 公尺。原始回報的像素大小在資料集之間可能差異極大，從不到 1 公尺到超過 20 公里都有可能。

使用 `ST_REGIONSTATS` 函式計算區域統計資料時，請務必考量光柵資料的像素大小。舉例來說，在某個國家/地區的區域內匯總高解析度點陣資料，可能需要大量運算資源，而且過於精細。反之，如果匯總區域 (例如城市地塊) 的低解析度資料，可能無法提供足夠的詳細資料。

如要從分析中取得有意義且有效率的結果，建議您選擇適合多邊形大小和分析目標的像素大小。您可以在 BigQuery sharing 圖片資料表說明部分，找到每個光柵資料集的像素大小。

變更像素大小會改變與特定地理區域相交的像素數量，進而影響結果和解讀方式。我們不建議變更用於正式版分析的像素大小。不過，如果您要製作查詢原型，增加像素大小可以縮短查詢執行時間並降低費用，特別是高解析度資料。

如要變更像素大小，請在 `ST_REGIONSTATS` 函式的 `options` 引數中設定 `scale`。舉例來說，如要計算 1,000 公尺像素的統計資料，請使用 `options => JSON '{"scale":1000}'`，這會指示 Earth Engine 以要求的比例重新取樣圖片。如要進一步瞭解 Earth Engine 如何處理重新調整比例，請參閱 Google Earth Engine 說明文件中的「[比例](https://developers.google.com/earth-engine/guides/scale?hl=zh-tw)」一節。

如果多邊形遠小於點陣圖的像素，計算出的統計資料可能會不準確或為空值。在這種情況下，其中一種替代做法是使用 [`ST_CENTROID`](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_centroid) 將多邊形替換為其質心點。

## 帳單

執行查詢時，系統會針對 `ST_REGIONSTATS` 函式的使用量另外計費，因為 Earth Engine 會計算函式呼叫的結果。無論您採用以量計價或預留方案，系統都會根據 BigQuery 服務 SKU，以運算單元時數計算這類用量的費用。如要查看 Earth Engine 的 BigQuery 呼叫費用，請[查看帳單報表](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw#overview)，並使用[標籤](https://docs.cloud.google.com/billing/docs/how-to/reports?hl=zh-tw#filter-by-labels)依標籤鍵 `goog-bq-feature-type` 篩選，值為 `EARTH_ENGINE`。如果 `ST_REGIONSTATS` 函式失敗，您就不必支付任何使用的 Earth Engine 運算費用。

您可以在 BigQuery API 中使用 [`jobs.get` 方法](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/jobs/get?hl=zh-tw)，查看每項查詢的下列資訊：

* [`slotMs` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#externalservicecost)，顯示 `externalService` 欄位為 `EARTH_ENGINE` 且 `billingMethod` 欄位為 `SERVICES_SKU` 時，Earth Engine 消耗的運算單元時間 (毫秒)。
* [`totalServicesSkuSlotMs` 欄位](https://docs.cloud.google.com/bigquery/docs/reference/rest/v2/Job?hl=zh-tw#jobstatistics2)，顯示所有 BigQuery 外部服務使用的運算單元毫秒總數，這些服務會透過 BigQuery 服務 SKU 收費。

您也可以查詢[`INFORMATION_SCHEMA.JOBS` 檢視中的 `total_services_sku_slot_ms` 欄位](https://docs.cloud.google.com/bigquery/docs/information-schema-jobs?hl=zh-tw)，找出以 BigQuery 服務 SKU 計費的外部服務所耗用的運算單元毫秒總數。

### 費用因素

執行 `ST_REGIONSTATS` 函式時，下列因素會影響運算用量：

* 輸入資料列數。
* 您使用的光柵圖像。部分點陣是從 Earth Engine 資料目錄中的來源圖像集合建立的複合資料，產生複合結果所需的運算資源各不相同。
* 圖片解析度。
* 輸入地理位置的大小和複雜度、與地理位置相交的像素數，以及 Earth Engine 讀取的圖像圖塊和位元組數。
* 地球上輸入地理位置相對於來源圖片的位置，以及圖片的投影和解析度。

  + 影像投影可能會扭曲像素，尤其是在高緯度或遠離影像預期涵蓋範圍的像素。
  + 如果是複合點陣圖，與輸入地理位置相交的來源圖片數量可能會因地區和時間而異。舉例來說，部分衛星可能會根據軌道和資料收集參數，在低緯度或高緯度地區產生更多圖片，也可能會根據不斷變化的天氣狀況省略圖片。
* `include` 或 `band_name` 引數中使用的公式，以及這些公式涉及的頻帶數量。
* 快取先前的結果。

### 控管費用

如要控管與 `ST_REGIONSTATS` 函式相關的費用，可以調整配額，控管函式可消耗的時段時間量。預設值為每天 350 個時段小時。
[查看配額](https://docs.cloud.google.com/docs/quotas/view-manage?hl=zh-tw)時，請篩選「指標」清單，`earthengine.googleapis.com/bigquery_slot_usage_time` 即可查看與 BigQuery 呼叫相關聯的 Earth Engine 配額。詳情請參閱 Google Earth Engine 說明文件中的
[BigQuery 點陣函式配額](https://developers.google.com/earth-engine/guides/usage?hl=zh-tw#bigquery_slot-time_per_day)。

**注意：** 與 BigQuery 中的自訂查詢配額類似，這項配額為約略值。這項功能可預防費用超額，但無法嚴格限制時段。因此在某些情況下，BigQuery 可能會執行超過配額限制的查詢作業，而您可能在配額用盡後，不會收到整筆用量的帳單。

## 支援的地區

呼叫 `ST_REGIONSTATS` 函式的查詢必須在下列其中一個區域中執行：

* `US` 多地區
* `us-central1`
* `us-central2`
* `EU` 多地區
* `europe-west1`

## 後續步驟

* 請參閱[這個教學課程](https://docs.cloud.google.com/bigquery/docs/raster-tutorial-weather?hl=zh-tw)，瞭解如何使用點陣資料分析溫度。
* 進一步瞭解 [BigQuery 中的地理函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)。
* 進一步瞭解[如何處理地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-12 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-12 (世界標準時間)。"],[],[]]