Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用沙箱試用 BigQuery

有了 BigQuery 沙箱，你就能免付費探索部分 BigQuery 功能，確認 BigQuery 是否符合需求。您不需要提供信用卡資料或為專案建立帳單帳戶，就能透過 BigQuery 沙箱體驗 BigQuery。如果已建立帳單帳戶，仍然可以使用免付費層級的 BigQuery 服務，無須支付費用。

您可透過沙箱免付費使用部分 BigQuery 功能，藉此熟悉 BigQuery。您可以使用 BigQuery 沙箱查看及查詢公開資料集，評估 BigQuery。

Google Cloud 提供儲存在 BigQuery 中的公開資料集，並透過 [Google Cloud 公開資料集計畫](https://cloud.google.com/datasets?hl=zh-tw)提供給一般大眾使用。如要進一步瞭解如何使用公開資料集，請參閱「[BigQuery 公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)」。

---

如要直接在 Google Cloud 控制台中，按照這項工作的逐步指南操作，請按一下「Guide me」(逐步引導)：

[「Guide me」(逐步引導)](https://console.cloud.google.com/freetrial?redirectPath=%2F%3Fwalkthrough_id%3Dbigquery--bigquery-quickstart-query-public-dataset&hl=zh-tw)

---

## 事前準備

### 啟用 BigQuery 沙箱

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往 BigQuery](https://console.cloud.google.com/bigquery?hl=zh-tw)

   您也可以在瀏覽器中輸入下列網址，在 Google Cloud 控制台開啟 BigQuery：

   ```
   https://console.cloud.google.com/bigquery
   ```

   Google Cloud 控制台是圖形化介面，可用於建立及管理 BigQuery 資源，以及執行 SQL 查詢。
2. 使用 Google 帳戶驗證身分，或建立新帳戶。
3. 在歡迎頁面中，執行下列操作：

   1. 在「Country」(國家/地區)，選取你的國家/地區。
   2. 如要同意《**服務條款**》，請勾選核取方塊。
   3. 選用：如果系統詢問是否要接收電子郵件通知，請勾選核取方塊，以便接收電子郵件通知。
   4. 點按「同意並繼續」。
4. 按一下 [Create Project]。
5. 在「New Project」(新增專案) 頁面中，執行下列操作：

   1. 在「專案名稱」部分，輸入專案名稱。
   2. 如為「機構」，請選取機構，如果沒有所屬機構，請選取「無機構」。受管理帳戶 (例如與學術機構相關聯的帳戶) 必須選取機構。
   3. 如果系統要求選取「位置」，請按一下「瀏覽」，然後選取專案位置。
   4. 點按「Create」(建立)。系統會將您重新導向至 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

您已成功啟用 BigQuery 沙箱。「BigQuery」**BigQuery**頁面現在會顯示 BigQuery 沙箱通知：

## 限制

BigQuery 沙箱有下列限制：

* 適用 BigQuery 的所有[配額與限制](https://docs.cloud.google.com/bigquery/quotas?hl=zh-tw)。
* 您的免費用量限制與 BigQuery [免費方案](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)相同，也就是每個月都能使用 10 GB 的儲存空間，並可處理 1 TB 的查詢資料。
* 所有 BigQuery [資料集](https://docs.cloud.google.com/bigquery/docs/datasets-intro?hl=zh-tw)都有[預設資料表到期時間](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#table-expiration)，而所有[資料表](https://docs.cloud.google.com/bigquery/docs/tables-intro?hl=zh-tw)、[檢視區塊](https://docs.cloud.google.com/bigquery/docs/views-intro?hl=zh-tw)和[分區](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)都會在 60 天後自動到期。
* BigQuery 沙箱不支援多項 BigQuery 功能，包括：

  + [以串流方式傳輸資料](https://docs.cloud.google.com/bigquery/docs/write-api?hl=zh-tw)
  + [資料操縱語言 (DML) 陳述式](https://docs.cloud.google.com/bigquery/docs/data-manipulation-language?hl=zh-tw)
  + [BigQuery 資料移轉服務](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)

## 查看公開資料集

根據預設，BigQuery 公開資料集會直接出現在名為 `bigquery-public-data` 的 BigQuery Studio 專案中。在本教學課程中，您將查詢紐約市 Citi Bike 行程資料集。Citi Bike 是大型自行車共享計畫，在曼哈頓、布魯克林、皇后區和澤西市設有 10,000 輛自行車及 600 個站點。這個資料集包含 Citi Bike 自 2013 年 9 月推出以來的行程。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中，點選「新增資料」**add**。
4. 在「新增資料」對話方塊中，按一下 「公開資料集」。
5. 在「Marketplace」頁面的「Search Marketplace」欄位中輸入 `NYC
   Citi Bike Trips`，縮小搜尋範圍。
6. 在搜尋結果中，按一下「NYC Citi Bike Trips」。
7. 在「產品詳細資料」頁面中，按一下「查看資料集」。您可以在「詳細資料」分頁中查看資料集相關資訊。

## 查詢公開資料集

在下列步驟中，您會查詢 `citibike_trips` 資料表，找出 NYC Citi Bike 行程公開資料集中最熱門的 100 個 Citi Bike 車站。這項查詢會擷取車站名稱和位置，以及從該車站出發的行程數量。

這項查詢會使用 [ST\_GEOGPOINT 函式](https://docs.cloud.google.com/bigquery/docs/reference/standard-sql/geography_functions?hl=zh-tw#st_geogpoint)，根據每個車站的經緯度參數建立點，並在 `GEOGRAPHY` 資料欄中傳回該點。`GEOGRAPHY` 欄用於在整合式地理資料檢視器中產生熱視圖。

1. 在 Google Cloud 控制台開啟「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 按一下 add\_box「SQL query」(SQL 查詢)。
3. 在
   查詢編輯器中輸入下列查詢：

   ```
   SELECT
     start_station_name,
     start_station_latitude,
     start_station_longitude,
     ST_GEOGPOINT(start_station_longitude, start_station_latitude) AS geo_location,
     COUNT(*) AS num_trips
   FROM
     `bigquery-public-data.new_york.citibike_trips`
   GROUP BY
     1,
     2,
     3
   ORDER BY
     num_trips DESC
   LIMIT
     100;
   ```

   如果查詢有效，系統就會顯示勾號和查詢處理的資料量。如果查詢無效，則會顯示驚嘆號和錯誤訊息。
4. 點選「Run」(執行)，「Query results」(查詢結果) 部分會列出最熱門的電台。
5. 選用步驟：如要查看工作持續時間和查詢工作處理的資料量，請點選「Query results」(查詢結果) 專區中的「Job information」(工作資訊) 分頁標籤。
6. 切換至「Visualization」分頁。這個分頁會生成地圖，方便您快速查看結果。
7. 在「視覺化設定」面板中：

   1. 確認「圖表類型」已設為「地圖」。
   2. 確認「Geography column」(地理位置資料欄) 已設為 **`geo_location`**。
   3. 在「資料欄」部分，選擇 **`num_trips`**。
   4. 使用「add 放大」選項，顯示曼哈頓地圖。

## 從 BigQuery 沙箱升級

有了 BigQuery 沙箱，你就能免付費探索[部分 BigQuery 功能](#limitations)，想增加儲存空間和查詢功能時，請從 BigQuery 沙箱升級。

如要升級，請按照下列步驟操作：

1. [啟用專案的計費功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw#enable_billing_for_a_project)。
2. 探索 [BigQuery 版本](https://docs.cloud.google.com/bigquery/docs/editions-intro?hl=zh-tw)，並決定適合您的定價模式。

從 BigQuery 沙箱升級後，請[更新 BigQuery 資源 (例如資料表、檢視區塊和分區) 的預設到期時間](https://docs.cloud.google.com/bigquery/docs/updating-datasets?hl=zh-tw#table-expiration)。

## 清除所用資源

為了避免系統向您的 Google Cloud 帳戶收取本頁面所用資源的費用，請按照下列步驟操作。

### 刪除專案

如果您使用 [BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)查詢公開資料集，專案就不會啟用帳單功能，因此您不需要刪除專案。

如要避免付費，最簡單的方法就是刪除您為了本教學課程所建立的專案。

刪除專案的方法如下：

**注意**：刪除專案會造成以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本文中的任務，刪除專案將一併移除當中已完成的其他任務'。
* **自訂專案 ID 會消失。**當您之前建立這個專案時，可能建立了想要在日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 `appspot.com` 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。

如果打算探索多種架構、教學課程或快速入門導覽課程，重複使用專案可避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「Manage resources」(管理資源)](https://console.cloud.google.com/iam-admin/projects?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下 [Shut down] (關閉) 以刪除專案。

## 後續步驟

* 如要進一步瞭解如何透過免費用量級別使用 BigQuery，請參閱「[免費用量級別](https://cloud.google.com/bigquery/pricing?hl=zh-tw#free-tier)」。
* 瞭解如何[在 BigQuery 中建立資料集、載入資料及查詢資料表](https://docs.cloud.google.com/bigquery/docs/quickstarts/load-data-console?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-09 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-09 (世界標準時間)。"],[],[]]