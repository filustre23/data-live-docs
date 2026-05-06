Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用光柵資料分析溫度

本教學課程說明如何對[點陣資料](https://docs.cloud.google.com/bigquery/docs/raster-data?hl=zh-tw)執行地理空間分析。

## 目標

* 在 BigQuery sharing (舊稱 Analytics Hub) 中，尋找可公開取得的 Google Earth Engine 資料。
* 使用 [`ST_REGIONSTATS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_regionstats)計算各國家/地區在特定時間點的平均溫度。
* 在 [BigQuery Geo Viz](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize?hl=zh-tw) 中以視覺化的方式呈現結果。BigQuery Geo Viz 是一個網頁工具，使用 Google Maps API 在 BigQuery 中顯示地理空間資料。

## 費用

本教學課程使用下列 Google Cloud計費元件：

* [BigQuery](https://cloud.google.com/bigquery/pricing?hl=zh-tw)
* [Google Earth Engine](https://cloud.google.com/earth-engine/pricing?hl=zh-tw)

## 事前準備

建議您為本教學課程建立 Google Cloud 專案。請確認您具備完成本教學課程的必要角色。

### 設定 Google Cloud 專案

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
- Enable the BigQuery, BigQuery sharing, and Google Earth Engine APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery%2Canalyticshub.googleapis.com%2Cearthengine.googleapis.com&hl=zh-tw)

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
- Enable the BigQuery, BigQuery sharing, and Google Earth Engine APIs.

  **Roles required to enable APIs**

  To enable APIs, you need the Service Usage Admin IAM
  role (`roles/serviceusage.serviceUsageAdmin`), which
  contains the `serviceusage.services.enable` permission. [Learn how to grant
  roles](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw).

  [Enable the APIs](https://console.cloud.google.com/flows/enableapi?apiid=bigquery%2Canalyticshub.googleapis.com%2Cearthengine.googleapis.com&hl=zh-tw)

### 必要的角色

如要取得執行本教學課程中工作所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* [Earth Engine 資源檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/earthengine?hl=zh-tw#earthengine.viewer)  (`roles/earthengine.viewer`)
* [服務使用情形消費者](https://docs.cloud.google.com/iam/docs/roles-permissions/serviceusage?hl=zh-tw#serviceusage.serviceUsageConsumer)  (`roles/serviceusage.serviceUsageConsumer`)
* [BigQuery 資料編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.dataEditor)  (`roles/bigquery.dataEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

這些預先定義的角色具備執行本教學課程中工作所需的權限。如要查看確切的必要權限，請展開「Required permissions」(必要權限) 部分：

#### 所需權限

如要執行本教學課程中的工作，必須具備下列權限：

* `earthengine.computations.create`
* `serviceusage.services.use`
* `bigquery.datasets.create`

您或許還可透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)取得這些權限。

## 訂閱資料集

如要找出本教學課程使用的資料集，請按照下列步驟操作：

1. 前往「Sharing (Analytics Hub)」頁面。

   [前往「共用」(Analytics Hub)](https://console.cloud.google.com/bigquery/analytics-hub?hl=zh-tw)
2. 按一下「搜尋房源」search。
3. 在「Search for listings」(搜尋房源) 欄位中輸入 `"ERA5-Land Daily Aggregated"`。
4. 按一下結果。詳細資料窗格隨即開啟，顯示 ERA5-Land 氣候再分析資料集的相關資訊，包括說明、波段資訊連結、可用性、像素大小和使用條款。
5. 按一下「訂閱」。
6. 選用：更新「Project」(專案)。
7. 將「連結的資料集名稱」更新為 `era5_climate_tutorial`。
8. 按一下 [儲存]。連結的資料集會新增至專案，並包含名為 `climate` 的單一資料表。

## 找出光柵 ID

`era5_climate_tutorial.climate` 表格中的每一列都包含特定日期的點陣圖像中繼資料，當中含有氣候資料。執行下列查詢，擷取 2025 年 1 月 1 日的光柵圖像光柵 ID：

```
SELECT
  assets.image.href
FROM
  `era5_climate_tutorial.climate`
WHERE
  properties.start_datetime = '2025-01-01';
```

結果為 `ee://ECMWF/ERA5_LAND/DAILY_AGGR/20250101`。在下一節中，您會將這個值做為 `ST_REGIONSTATS` 函式的 `raster_id` 引數。

## 計算平均溫度

執行下列查詢，使用 [`ST_REGIONSTATS` 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_regionstats)計算 2025 年 1 月 1 日各國的平均溫度：

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
    'ee://ECMWF/ERA5_LAND/DAILY_AGGR/20250101',
    'temperature_2m'
  ).mean - 273.15 AS mean_temperature
FROM
  SimplifiedCountries AS sc
ORDER BY
  mean_temperature DESC;
```

這項查詢會在公開的 `division_area` 表格上執行，該表格包含代表地球上各個區域 (包括國家/地區) 邊界的 `GEOGRAPHY` 值。`ST_REGIONSTATS` 函式會使用光柵圖片的 `temperature_2m` 頻帶，其中包含指定像素位置地表上方 2 公尺處的氣溫。

## 在 BigQuery 中以視覺化方式呈現查詢結果

如要在 BigQuery 中以圖表呈現結果，請按照下列步驟操作：

1. 在「查詢結果」窗格中，按一下「圖表」分頁標籤。
2. 在「資料欄」部分，選取 `mean_temperature`。

   世界地圖會顯示各國的平均溫度，並以顏色漸層標示。

## 在 Geo Viz 中將查詢結果視覺化

您也可以使用 BigQuery Geo Viz 將結果視覺化。

### 啟用 Geo Viz 並進行身分驗證

在您使用 Geo Viz 之前，您必須在 BigQuery 中對資料進行身分驗證並授予存取權。

如要設定 Geo Viz，請按照下列步驟操作：

1. 開啟 Geo Viz 網頁版工具。

   [開啟 Geo Viz](https://bigquerygeoviz.appspot.com/?hl=zh-tw)

   或者，在「查詢結果」窗格中，依序點選「開啟方式」**>「GeoViz」**。
2. 在第一步「Query」(查詢) 中，按一下「Authorize」(授權)。
3. 在「Choose an account」(選擇帳戶) 對話方塊中，按一下您的 Google 帳戶。
4. 在存取對話方塊中，按一下 [Allow] (允許) 以取得您 BigQuery 資料的 Geo Viz 存取權。

### 在 Geo Viz 中執行查詢

在您進行身分驗證並授予權限後，下一步是在 Geo Viz 中執行查詢。

如要執行查詢，請按照下列步驟操作：

1. 在第一步「Select data」(選取資料) 中，於「Project ID」(專案 ID) 欄位中輸入您的專案 ID。
2. 在查詢視窗中，輸入下列 GoogleSQL 查詢。如果您是從查詢結果開啟 Geo Viz，這個欄位會預先填入查詢內容。

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
       'ee://ECMWF/ERA5_LAND/DAILY_AGGR/20250101',
       'temperature_2m'
     ).mean - 273.15 AS mean_temperature
   FROM
     SimplifiedCountries AS sc
   ORDER BY
     mean_temperature DESC;
   ```
3. 按一下「執行」。

### 套用樣式

「樣式」區段會提供視覺化樣式清單以供您自訂。如要進一步瞭解各個樣式，請參閱「[設定資料視覺化格式](https://docs.cloud.google.com/bigquery/docs/geospatial-get-started?hl=zh-tw#format_your_visualization)」。

如要將地圖格式化，請按照下列步驟操作：

1. 如要開啟「fillColor」面板，請按一下步驟 3「Style」。
2. 將「以數據為準」切換鈕設為開啟。
3. 在「Function」中選擇 [linear]。
4. 在「Field」(欄位) 部分，選擇 **`mean_temperature`**。
5. 在「Domain」(網域) 部分，分別在第一個和第二個方塊中輸入 `-20` 和 `32`。
6. 針對「Range」(範圍)，按一下第一個方塊，然後在「Hex」方塊中輸入 `#0006ff`；按一下第二個方塊，然後輸入 `#ff0000`。這會根據各國家/地區在 2025 年 1 月 1 日的平均溫度，變更各國家/地區的顏色。藍色代表溫度較低，紅色代表溫度較高。
7. 按一下 [fillOpacity]。
8. 在「Value」(值) 欄位中，輸入 `.5`。
9. 按一下「套用樣式」。
10. 查看您的地圖。按一下國家/地區，系統會顯示該國家/地區的名稱、平均溫度和簡化幾何圖形。

## 清除所用資源

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

## 後續步驟

* 如要進一步瞭解地理空間分析的視覺化選項，請參閱「[視覺化地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize?hl=zh-tw)」。
* 如要使用光柵資料，請參閱「[使用光柵資料](https://docs.cloud.google.com/bigquery/docs/raster-data?hl=zh-tw)」。
* 如要進一步瞭解地理空間分析中可使用的地理位置函式，請參閱 [GoogleSQL 中的地理位置函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]