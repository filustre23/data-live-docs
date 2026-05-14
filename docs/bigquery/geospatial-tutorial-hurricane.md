Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 使用地理空間數據分析繪製颶風路徑 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程將介紹地理空間分析。地理空間分析功能可讓您在 BigQuery 中輕鬆分析地理空間資料，並將資料視覺化。

## 目標

在本教學課程中，您將執行下列作業：

* 使用地理空間分析函式，將經緯度資料欄轉換為地理點
* 執行查詢以繪製颶風路徑
* 在 BigQuery 中以視覺化的方式呈現結果
* 在 [BigQuery Geo Viz](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize?hl=zh-tw) 中以視覺化的方式呈現結果

## 費用

BigQuery 為付費產品，您在這個教學課程中將會產生 BigQuery 使用費。使用者可免費使用一定限度的部分 BigQuery 資源。詳情請參閱「[BigQuery 免費作業和免費層級](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free)」一文。

## 事前準備

開始本教學課程之前，請先使用 Google Cloud 控制台建立或選取專案。

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

1. 新專案會自動啟用 BigQuery。如要在現有專案中啟用 BigQuery，請前往

   啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery&hl=zh-tw)
2. 選用：
   [啟用專案的計費功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw)。如果您不想啟用帳單或提供信用卡，仍可按照本文步驟操作。BigQuery 提供沙箱，方便您執行這些步驟。詳情請參閱「[啟用 BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw#setup)」一文。
   **注意：**如果專案有帳單帳戶，且您想使用 BigQuery 沙箱，請[停用專案的帳單功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw#disable_billing_for_a_project)。

## 匯出樣本資料

本教學課程使用[Google Cloud 公開資料集方案](https://cloud.google.com/datasets?hl=zh-tw)提供的資料集。公開資料集是儲存在 BigQuery 中且可供一般大眾使用的任何資料集。公開資料集是在 BigQuery 託管的資料集，讓您能夠存取及整合到應用程式中。Google 為這些資料集的儲存空間付費，並透過[專案](https://docs.cloud.google.com/bigquery/docs/projects?hl=zh-tw)提供資料的公開存取權。您只需要支付資料查詢費用 (每月前 1 TB 免費，相關規定請參閱[查詢費率詳情](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models))。

### 全球颶風軌跡 (IBTrACS) 資料集

[全球颶風軌跡 (IBTrACS) 資料集](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=noaa_hurricanes&%3Bpage=dataset&hl=zh-tw)

NOAA 的 International Best Track Archive for Climate Stewardship (IBTrACS) 提供全球熱帶氣旋 (TC) 軌跡上的歷史位置和強度。熱帶氣旋在北大西洋和東北太平洋海盆稱為颶風，在西北太平洋海盆稱為颱風，在南北印度洋海盆稱為旋風，而在西南太平洋海盆則稱之為熱帶氣旋。

IBTrACS 收集各地國際監測中心回報的 TC 資料。國際監測中心負責預測和回報 TC 資訊，也包含部分重要歷史資料集。IBTrACS 包含 9 個不同國家/地區的資料。歷史上，描述這些系統的資料已涵蓋了軌跡和強度的最佳預測資料 (因此有「最佳軌跡」之說)。

您可以在 Google Cloud 控制台中查看 `hurricanes` 資料表的詳細資料，開始探索這份資料：

[前往颶風結構定義](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=noaa_hurricanes&%3Bt=hurricanes&%3Bpage=table&hl=zh-tw)

## 查詢 2017 年瑪莉亞颶風的路徑

在本教學課程的這一節中，您將執行 GoogleSQL 查詢，找出 2017 年瑪麗亞颶風的路徑。如果要繪製該颶風的路徑，您可以查詢該颶風在不同時間點的位置。

### 查詢詳細資料

下列 GoogleSQL 查詢用於尋找瑪莉亞颶風的路徑。

```
SELECT
  ST_GeogPoint(longitude, latitude) AS point,
  name,
  iso_time,
  dist2land,
  usa_wind,
  usa_pressure,
  usa_sshs,
  (usa_r34_ne + usa_r34_nw + usa_r34_se + usa_r34_sw)/4 AS radius_34kt,
  (usa_r50_ne + usa_r50_nw + usa_r50_se + usa_r50_sw)/4 AS radius_50kt
FROM
  `bigquery-public-data.noaa_hurricanes.hurricanes`
WHERE
  name LIKE '%MARIA%'
  AND season = '2017'
  AND ST_DWithin(ST_GeogFromText('POLYGON((-179 26, -179 48, -10 48, -10 26, -100 -10.1, -179 26))'),
    ST_GeogPoint(longitude, latitude), 10)
ORDER BY
  iso_time ASC
```

查詢子句會執行下列動作：

* `SELECT ST_GeogPoint(longitude, latitude) AS point, name, iso_time, dist2land, usa_wind, usa_pressure, usa_sshs, (usa_r34_ne + usa_r34_nw + usa_r34_se + usa_r34_sw)/4 AS radius_34kt, (usa_r50_ne + usa_r50_nw + usa_r50_se + usa_r50_sw)/4 AS radius_50kt`
  :   `SELECT` 子句會選擇風暴的全部天氣資料，然後使用 `ST_GeogPoint` 函式，將 `latitude` 和 `longitude` 資料欄中的值轉換為 `GEOGRAPHY` 類型 (資料點)。
* `FROM bigquery-public-data.noaa_hurricanes.hurricanes`
  :   `FROM` 子句指定要查詢的資料表：`hurricanes`。
* `WHERE name LIKE '%MARIA%' AND season = '2017' AND ST_DWithin(ST_GeogFromText('POLYGON((-179 26, -179 48, -10 48, -10 26, -100 -10.1, -179 26))'), ST_GeogPoint(longitude, latitude), 10)`
  :   `WHERE` 子句只會篩選出對應至 2017 年颶風季節中瑪利亞颶風的大西洋資料點資料。
* `ORDER BY iso_time ASC`
  :   `ORDER BY` 子句對資料點進行排序，形成按時間順序排列的風暴路徑。

### 執行查詢

如要使用 Google Cloud 控制台執行查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Query editor」(查詢編輯器) 文字區域中，輸入下列 GoogleSQL 查詢。

   ```
   SELECT
     ST_GeogPoint(longitude, latitude) AS point,
     name,
     iso_time,
     dist2land,
     usa_wind,
     usa_pressure,
     usa_sshs,
     (usa_r34_ne + usa_r34_nw + usa_r34_se + usa_r34_sw)/4 AS radius_34kt,
     (usa_r50_ne + usa_r50_nw + usa_r50_se + usa_r50_sw)/4 AS radius_50kt
   FROM
     `bigquery-public-data.noaa_hurricanes.hurricanes`
   WHERE
     name LIKE '%MARIA%'
     AND season = '2017'
     AND ST_DWithin(ST_GeogFromText('POLYGON((-179 26, -179 48, -10 48, -10 26, -100 -10.1, -179 26))'),
       ST_GeogPoint(longitude, latitude), 10)
   ORDER BY
     iso_time ASC
   ```
3. 按一下「執行」。

   查詢需要一些時間才會完成。查詢執行完畢之後，您的結果會呈現於「Query results」(查詢結果) 窗格中。

## 在 BigQuery 中以視覺化方式呈現查詢結果

如要在 BigQuery 中以圖表呈現結果，請按照下列步驟操作：

1. 如要在 BigQuery 中以視覺化的方式呈現結果，請在「查詢結果」窗格中，按一下「視覺化」。
2. 在「資料欄」部分，選取 `usa_wind`。

   地圖會顯示颶風隨時間移動的路徑，並以風速的色階標示。
3. 選用：如要調整點的顯示程度，請將「最小值」設為 0，然後從「顏色」清單中選取其他顏色漸層。

## 在 Geo Viz 中將查詢結果視覺化

您也可以使用 BigQuery Geo Viz 將查詢結果視覺化。BigQuery Geo Viz 是一個網頁工具，使用 Google Maps API 在 BigQuery 中顯示地理空間資料。

### 啟用 Geo Viz 並進行身分驗證

在您使用 Geo Viz 之前，您必須在 BigQuery 中對資料進行身分驗證並授予存取權。

如何設定 Geo Viz：

1. 開啟 Geo Viz 網頁版工具。

   [開啟 Geo Viz 網頁版工具](https://bigquerygeoviz.appspot.com/?hl=zh-tw)
2. 在第一步「Select data」(選取資料) 中按一下 [Authorize] (授權)。
3. 在「Choose an account」(選擇帳戶) 對話方塊中，按一下您的 Google 帳戶。
4. 在存取對話方塊中，按一下 [Allow] (允許) 以取得您 BigQuery 資料的 Geo Viz 存取權。

### 在 Geo Viz 中執行查詢

在您進行身分驗證並授予權限後，下一步是在 Geo Viz 中執行查詢。

執行查詢：

1. 在第一步「Select data」(選取資料) 中，於「Project ID」(專案 ID) 欄位中輸入您的專案 ID。
2. 在查詢視窗中，輸入下列 GoogleSQL 查詢。

   ```
   SELECT
     ST_GeogPoint(longitude, latitude) AS point,
     name,
     iso_time,
     dist2land,
     usa_wind,
     usa_pressure,
     usa_sshs,
     (usa_r34_ne + usa_r34_nw + usa_r34_se + usa_r34_sw)/4 AS radius_34kt,
     (usa_r50_ne + usa_r50_nw + usa_r50_se + usa_r50_sw)/4 AS radius_50kt
   FROM
     `bigquery-public-data.noaa_hurricanes.hurricanes`
   WHERE
     name LIKE '%MARIA%'
     AND season = '2017'
     AND ST_DWithin(ST_GeogFromText('POLYGON((-179 26, -179 48, -10 48, -10 26, -100 -10.1, -179 26))'),
       ST_GeogPoint(longitude, latitude), 10)
   ORDER BY
     iso_time ASC
   ```
3. 按一下「執行」。
4. 查詢完成後，按一下「顯示結果」。您也可以按一下第二步的「資料」。
5. 您會進入步驟二。在步驟二的「Geometry column」中，選擇 [point]。系統即會繪製對應至瑪利亞颶風路徑的資料點。

### 在 Geo Viz 中設定視覺化格式

「樣式」部分會提供視覺化樣式清單以供您自訂。如要進一步瞭解樣式屬性和值，請參閱「[設定資料視覺化格式](https://docs.cloud.google.com/bigquery/docs/geospatial-get-started?hl=zh-tw#format_your_visualization)」。

如要將您的地圖進行格式化，請進行以下操作：

1. 按一下第二步中的 [Add styles]，或按一下第三步的 [Style]。
2. 更換資料點的顏色。按一下 [fillColor]。
3. 在「fillColor」面板中：

   1. 按一下 [Data driven]。
   2. 在「Function」(函式) 部分選擇 [linear]。
   3. 在「Field」(欄位) 部分，選擇 **`usa_wind`**。
   4. 針對「Domain」(領域)，分別在第一個和第二個方塊中輸入 **`0`** 和 **`150`**。
   5. 針對「Range」(範圍)，按一下第一個方塊，然後在「Hex」方塊中輸入 **`#0006ff`**；按一下第二個方塊，然後輸入 **`#ff0000`**。資料點的顏色就會因風速不同而改變。藍色代表風速較弱，紅色代表風速較強。
4. 查看您的地圖。將游標懸停在其中一個資料點上，即會顯示該點的天氣資料。
5. 按一下 [fillOpacity]。
6. 在「Value」(值) 欄位中，輸入 **.5**。
7. 查看您的地圖。資料點的填充顏色目前為半透明。
8. 根據颶風半徑，變更資料點的大小。按一下 [circleRadius]。
9. 在「circleRadius」面板中：

   1. 按一下「Data driven」。
   2. 在「Function」(函式) 部分選擇 [linear]。
   3. 在「Field」(欄位) 部分，選擇 **`radius_50kt`**。
   4. 在「Domain」(領域) 部分，分別在第一個和第二個方塊中輸入 **`0`** 和 **`135`**。
   5. 在「Range」(範圍) 部分，分別在第一個和第二個方塊中輸入 **`5`** 和 **`135000`**。
10. 查看您的地圖。現在每個資料點的半徑都跟颶風的半徑對應。
11. 關閉 Geo Viz。

## 清除所用資源

為避免因為本教學課程所用資源，導致系統向 Google Cloud 帳戶收取費用，請刪除含有相關資源的專案，或者保留專案但刪除個別資源。

* 您可以刪除建立的專案。
* 或者您可以保留該專案以備將來使用。

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

* 如要進一步瞭解地理空間分析的視覺化選項，請參閱「[視覺化地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize?hl=zh-tw)」。
* 如要使用地理空間資料，請參閱「[使用地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw)」。
* 如要進一步瞭解地理空間分析中可使用的地理位置函式，請參閱 [GoogleSQL 中的地理位置函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]