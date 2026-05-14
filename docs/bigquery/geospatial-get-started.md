Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見

# 開始使用地理空間分析 透過集合功能整理內容 你可以依據偏好儲存及分類內容。

本教學課程將介紹地理空間分析。地理空間分析功能可讓您在 BigQuery 中分析地理空間資料，並以圖表呈現。

## 目標

在本教學課程中，您將執行下列作業：

* 使用地理空間分析函式，將經緯度資料欄轉換為地理點
* 執行查詢作業，搜尋有超過 30 輛可供出租自行車的 Citi Bike 站點。
* 在 BigQuery 中以視覺化的方式呈現結果
* 在 [BigQuery Geo Viz](https://docs.cloud.google.com/bigquery/docs/geospatial-visualize?hl=zh-tw) 中以視覺化的方式呈現結果

## 費用

本教學課程使用 Google Cloud的計費元件，包括 BigQuery。

您需要支付以下費用：

* 在 BigQuery 的公開資料集裡[查詢資料](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models)。
  + 每個月前 1TB 免費
  + 如果您使用[以運算量為準的計價方式](https://cloud.google.com/bigquery/pricing?hl=zh-tw#capacity_compute_analysis_pricing)，查詢費用會包含在以運算量為準的價格中。

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

## 匯出樣本資料

本教學課程使用[Google Cloud 公開資料集方案](https://cloud.google.com/datasets?hl=zh-tw)提供的資料集。公開資料集是儲存在 BigQuery 中且可供一般大眾使用的任何資料集。公共資料集是 BigQuery 託管的資料集，讓您能夠存取與整合到您的應用程式中。這些資料集的儲存空間費用由 Google 支付，Google 也透過[專案](https://docs.cloud.google.com/bigquery/docs/projects?hl=zh-tw)將這些資料集提供給大眾存取。您只需要支付資料查詢費用 (每月前 1 TB 免費，相關規定請參閱[查詢費率詳情](https://cloud.google.com/bigquery/pricing?hl=zh-tw#analysis_pricing_models))。

### 紐約市 Citi Bike 行程資料集

[NYC Citi Bike Trips](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=new_york_citibike&%3Bpage=dataset&hl=zh-tw)

Citi Bike 是美國最大的自行車共享計劃，在曼哈頓、布魯克林、皇后區和澤西市設有 10,000 輛自行車及 600 個站點。這個資料集包含 Citi Bike 自 2013 年 9 月推出以來所記錄的所有行程，並且每日更新。資料已由 Citi Bike 處理過，移除了工作人員為了維修檢驗系統而騎乘的行程，以及時間長度在 60 秒內的任何行程，因為這些都視為誤始行程。

您可以在 BigQuery 主控台中查看 `citibike_stations` 資料表的詳細資料，開始探索這份資料：

[前往 citibik\_stations 結構定義](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=new_york_citibike&%3Bt=citibike_stations&%3Bpage=table&hl=zh-tw)

在此資料表中，以下有三個資料欄與本教學課程有關:

* `bike_stations.longitude`：車站的經度。這個值是十進位制格式的有效 WGS 84 經度。
* `bike_stations.latitude`：車站的緯度。這個值是十進位制格式的有效 WGS 84 緯度。
* `num_bikes_available`：可供出租的自行車數量。

## 查詢可供出租超過 30 輛自行車的站點

在本教學課程的這一節中，您將執行 GoogleSQL 查詢，找出紐約市所有可供出租超過 30 輛自行車的 Citi Bike 站點。

### 查詢詳細資料

下列 GoogleSQL 查詢用於尋找超過 30 輛自行車的 Citi Bike 站點。

```
SELECT
  ST_GeogPoint(longitude, latitude)  AS WKT,
  num_bikes_available
FROM
  `bigquery-public-data.new_york.citibike_stations`
WHERE num_bikes_available > 30
```

查詢子句會執行下列動作：

* `SELECT ST_GeogPoint(longitude, latitude) AS WKT, num_bikes_available`
  :   `SELECT` 子句會選取 `num_bikes_available` 資料欄，並使用 `ST_GeogPoint` 函式，將 `latitude` 和 `longitude` 資料欄中的值轉換為 `GEOGRAPHY` 類型 (資料點)。
* `` FROM `bigquery-public-data.new_york.citibike_stations` ``
  :   `FROM` 子句指定要查詢的資料表：`citibike_stations`。
* `WHERE num_bikes_available > 30`
  :   `WHERE` 子句篩選 `num_bikes_available` 資料欄中的值，只選出有 30 輛自行車以上的站點。

### 執行查詢

如要使用 Google Cloud 控制台執行查詢，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery 頁面](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Query editor」(查詢編輯器) 文字區域中，輸入下列 GoogleSQL 查詢。

   ```
   -- Finds Citi Bike stations with > 30 bikes
   SELECT
     ST_GeogPoint(longitude, latitude)  AS WKT,
     num_bikes_available
   FROM
     `bigquery-public-data.new_york.citibike_stations`
   WHERE num_bikes_available > 30
   ```
3. 按一下「執行」。

   查詢需要一些時間才會完成。查詢執行完畢之後，您的結果會呈現於「Query results」(查詢結果) 窗格中。

## 在 BigQuery 中以視覺化的方式呈現結果

如要以互動式地圖呈現結果，請按照下列步驟操作：

1. 在「查詢結果」窗格中，按一下「圖表」。

   地圖上的點代表各個自行車站的位置。
2. 您可以對地圖套用統一或資料導向樣式。
   如要以視覺化方式呈現各個車站的可用自行車數量，請在「資料欄」中選取 `num_bikes_available`。
3. 如要提升可視性，請調整「不透明度」、「顏色」或「點大小」。如果資料包含離群值，可以調整「最小值」和「最大值」。地圖上仍會顯示超出這個範圍的值，但不會套用任何顏色。
4. 如要查看地理位置的屬性，請按一下該地理位置。
5. 如要以衛星模式查看地圖，請按一下「衛星」。

## 在 Geo Viz 中將查詢結果視覺化

您也可以使用 BigQuery Geo Viz 將查詢結果視覺化。BigQuery Geo Viz 是一個網頁工具，使用 Google Maps API 在 BigQuery 中顯示地理空間資料。

### 啟用 Geo Viz 並進行身分驗證

在您使用 Geo Viz 之前，您必須在 BigQuery 中對資料進行身分驗證並授予存取權。

如何設定 Geo Viz：

1. 開啟 Geo Viz 網頁版工具。

   [開啟 Geo Viz 網頁版工具](https://bigquerygeoviz.appspot.com/?hl=zh-tw)

   您可能需要啟用 Cookie，才能授權及使用這項工具。
2. 在第一步「Query」(查詢) 中按一下「Authorize」(授權)。
3. 在「Choose an account」(選擇帳戶) 對話方塊中，按一下您的 Google 帳戶。
4. 在存取對話方塊中，按一下 [Allow] (允許) 以取得您 BigQuery 資料的 Geo Viz 存取權。

### 對地理空間資料執行 GoogleSQL 查詢

在您進行身分驗證並授予權限後，下一步是在 Geo Viz 中執行查詢。

執行查詢：

1. 在第一步「Select data」(選取資料) 中，於「Project ID」(專案 ID) 欄位中輸入您的專案 ID。
2. 在查詢視窗中，輸入下列 GoogleSQL 查詢。

   ```
   -- Finds Citi Bike stations with > 30 bikes
   SELECT
     ST_GeogPoint(longitude, latitude)  AS WKT,
     num_bikes_available
   FROM
     `bigquery-public-data.new_york.citibike_stations`
   WHERE num_bikes_available > 30
   ```
3. 按一下「執行」。
4. 查詢完成後，按一下「顯示結果」。您也可以按一下第二步的 [Define columns] (定義資料欄)。
5. 您會進入步驟二。在步驟二的「Geometry column」(Geometry 資料欄) 中，選擇 [WKT]。這會在您的地圖上標註相對應的自行車站點位置。

### 設定您的視覺化格式

「Style」(樣式) 區段會提供視覺化樣式清單以供您自訂。某些屬性僅適用於某些類型的資料。例如，`circleRadius` 僅會影響資料點。

系統支援的樣式屬性包含：

* **fillColor**。多邊形或點的填滿顏色。例如，可以使用「linear」或「interval」函式以數值來對應顏色漸層。
* **fillOpacity**。多邊形或點的填充透明度。值必須介於 0 到 1 之間，其中 `0` = 透明，且 `1` = 不透明。
* **strokeColor**。多邊形或線條的筆觸或外框顏色。
* **strokeOpacity**。多邊形或線條的筆觸或外框的透明度。值必須介於 0 到 1 之間，其中 `0` = 透明，且 `1` = 不透明。
* **strokeWeight**。多邊形或線條的筆觸或外框寬度 (以像素為單位)。
* **circleRadius**。資料點的圓半徑 (以像素為單位)。例如，「linear」函式能夠以數值對應資料點的大小，以建立散佈圖的樣式。

每種樣式可能得到全域值 (應用於每個結果) 或是資料導向值 (根據每個結果資料列的資料採取不同的應用方式)。針對資料導向值，以下的項目皆會影響其結果：

* **function**。用於從欄位值計算樣式值的函式。
* **身分**。每個欄位的資料值都做為樣式值使用。
* **類別**。將領域中列出的每個欄位的資料值以一對一的方式對應至範圍中的相應樣式。
* **間隔**。每個欄位的資料值會無條件捨去至領域中最接近的值，並依據範圍中對應的樣式進行樣式設定。
* **線性**。每個欄位的資料值會線性內插於領域的值之間，並混合採用範圍中對應的樣式。
* **欄位**。將資料中的指定欄位當成樣式函式的輸入使用。
* **網域**。來自欄位的範例輸入值的已排序清單。範例輸入 (領域) 會根據指定的函式與範例輸出 (範圍) 配對，並用於推測所有輸入 (包括未列於領域中的輸入) 的樣式值。領域中的值必須要有相同的類型 (文字或數字等)，做為您要進行視覺化之欄位的值。
* **範圍**。樣式規則的範例輸出值清單。範圍中的值必須要有相同的類型 (顏色或數字)，做為您要控制的樣式屬性。例如，`fillColor` 屬性的範圍應該僅包含顏色。

如要將您的地圖進行格式化，請進行以下操作：

1. 按一下第二步中的 [Add styles]，或按一下第三步的 [Style]。
2. 更換資料點的顏色。按一下 [fillColor]。
3. 在「Value」(值) 欄位中，輸入 **`#0000FF`** (藍色的 HTML 顏色代碼)。
4. 按一下「套用樣式」。
5. 查看您的地圖。按一下其中一個資料點，即會顯示該值。
6. 按一下 [fillOpacity]。
7. 在「Value」(值) 欄位中輸入 **`0.5`**，然後按一下「Apply Style」(套用樣式)。
8. 查看您的地圖。資料點的填充顏色目前為半透明。
9. 依據可用自行車的數量改變資料點的大小。按一下 [circleRadius]。
10. 在「circleRadius」面板中：

    1. 按一下「Data driven」。
    2. 在「Function」(函式) 部分選擇 [linear]。
    3. 在「Field」(欄位) 部分，選擇 **`num_bikes_available`**。
    4. 在「Domain」(領域) 部分，分別在第一個和第二個方塊中輸入 **`30`** 和 **`60`**。
    5. 在「Range」(範圍) 部分，分別在第一個和第二個方塊中輸入 **`5`** 和 **`20`**。
11. 查看您的地圖。現在每個圓的半徑會根據該位置可用的自行車數量進行調整。
12. 關閉 Geo Viz。

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
* 如要進一步瞭解如何使用地理空間分析資料，請參閱「[使用地理空間資料](https://docs.cloud.google.com/bigquery/docs/geospatial-data?hl=zh-tw)」。
* 如需使用地理空間分析的教學課程，請參閱[使用地理空間分析繪製颶風路徑](https://docs.cloud.google.com/bigquery/docs/geospatial-tutorial-hurricane?hl=zh-tw)。
* 如要查看地理空間分析的 GoogleSQL 函式說明文件，請參閱[GoogleSQL 中的地理函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-14 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-14 (世界標準時間)。"],[],[]]