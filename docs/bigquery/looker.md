Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 使用 BI Engine 和 Looker 分析資料

Looker 是集結商業智慧、資料應用程式與嵌入式數據分析服務的企業平台。您可以運用 Looker 探索、分享公司資料，並以圖表呈現，進而制定更明智的業務決策。

## Looker 的運作方式

Looker 可讓各組織的資料專家使用 LookML 這種輕量模型語言描述資料。LookML 會指示 Looker 如何查詢資料，因此組織中的每個人都能建立容易閱讀的報表和資訊主頁，探索資料模式。Looker 則提供額外功能，可用於建立自訂資料應用程式和體驗。

Looker 平台可與 Oracle 和 MySQL 等交易資料庫，以及 BigQuery、Snowflake、Redshift 等分析資料儲存庫搭配使用。Looker 可讓您快速準確地以所有資料為基礎建立一致的資料模型。Looker 提供整合式介面，可存取組織的所有資料。

## Looker 與 BigQuery 整合

Looker 支援在 Google Cloud託管。Looker 獨立於平台，可連結 BigQuery 和其他公有雲中的資料。

您不一定要使用 Looker 才能使用 BigQuery。不過，如果您的 BigQuery 用途包括商業智慧、資料應用程式或嵌入式數據分析，建議您考慮使用 Looker 做為這些服務的供應商。

如果您已有執行中的 Looker 執行個體，請參閱[將 Looker 連結至 BigQuery 的操作說明](https://docs.cloud.google.com/looker/docs/db-config-google-bigquery?hl=zh-tw)。

## 開始使用 Looker 和 BigQuery

BI Engine 可與任何商業智慧 (BI) 工具完美整合，包括 Looker。詳情請參閱「[BI Engine 總覽](https://docs.cloud.google.com/bigquery/docs/bi-engine-intro?hl=zh-tw)」。

## 建立 BigQuery 資料集

首先，請建立 BigQuery 資料集，用於儲存 BI Engine 代管資料表。如要建立資料集，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中，點選專案。
4. 在詳細資料窗格中，依序點選「View actions」(查看動作) more\_vert 和「Create dataset」(建立資料集)。
5. 在「Create dataset」(建立資料集) 頁面執行下列操作：

   * 在「Dataset ID」(資料集 ID) 中輸入 `biengine_tutorial`。
   * 在「Data location」(資料位置) 中選擇「us (multiple regions in United States)」(us (多個美國區域))，也就是儲存公開資料集的[多區域位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw#multi-regions)。
   * 在本教學課程中，您可以選取「Enable table expiration」(啟用資料表到期時間)，然後指定資料表到期前的天數。
6. 讓其他設定維持在預設狀態，然後按一下 [Create dataset] (建立資料集)。

## 複製公開資料集的資料來建立資料表

本教學課程使用 [Google Cloud Public Dataset Program](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw) 提供的資料集。公開資料集是 BigQuery 代管的資料集，可供您存取並整合至應用程式。

在本節中，您將複製[舊金山 311 服務要求](https://console.cloud.google.com/marketplace/details/san-francisco-public-data/sf-311?filter=solution-type%3Adataset&hl=zh-tw)資料集中的資料，建立資料表。您可以使用[Google Cloud 控制台](https://console.cloud.google.com/bigquery?p=bigquery-public-data&%3Bd=san_francisco_311&%3Bpage=dataset&hl=zh-tw)探索資料集。

### 建立資料表

如要建立資料表，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格，搜尋 `san_francisco_311` 資料集。
4. 依序點選資料集和**「總覽」 > 「資料表」**。
5. 點選「`311_service_requests`」資料表。
6. 按一下工具列中的「複製」。
7. 在「Copy table」(複製資料表) 對話方塊的「Destination」(目的地) 部分，執行下列操作：

   * 在「Project」(專案) 部分，點選「Browse」(瀏覽)，然後選取專案。
   * 在「資料集」部分，選取「biengine\_tutorial」。
   * 在「Table」(資料表) 中輸入 `311_service_requests_copy`。
8. 點選「複製」。
9. 選用步驟：複製工作完成後，請依序展開「`PROJECT_NAME`」>「biengine\_tutorial」，然後依序點選「311\_service\_requests\_copy」>「預覽」，驗證資料表內容。將 **`PROJECT_NAME`** 替換為本教學課程的 Google Cloud 專案名稱。

## 建立 BI Engine 預留項目

1. 在 Google Cloud 控制台的「Administration」(管理) 下方，前往「BI Engine」頁面。

   [前往「BI Engine」頁面](https://console.cloud.google.com/bigquery/admin/bi-engine?hl=zh-tw)

   **注意：** 如果系統提示您啟用 **BigQuery Reservation API**，請點選「啟用」。
2. 按一下 add「Create reservation」(建立預留項目)。
3. 在「Create Reservation」(建立預留項目) 頁面中，設定 BI Engine 預留項目：

   * 在「Project」(專案) 清單中，確認您的 Google Cloud 專案。
   * 在「Location」(位置) 清單中選取位置。位置應與您查詢的[資料集位置](https://docs.cloud.google.com/bigquery/docs/locations?hl=zh-tw)相符。
   * 將「GiB of Capacity」(容量 (GiB)) 滑桿調整至要預留的記憶體容量。以下範例將容量設為 2 GiB。上限為 250 GiB。
4. 點選「下一步」。
5. 在「Preferred Tables」(偏好資料表) 部分，您可以視需要指定要透過 BI Engine 加速的資料表。如要找出資料表名稱，請按照下列步驟操作：

   1. 在「Table Id」(資料表 ID) 欄位中，輸入要由 BI Engine 加速的資料表名稱部分，例如 `311`。
   2. 從建議名稱清單中選取資料表名稱。

      只有指定的資料表才能加速。如未指定偏好資料表，所有專案查詢都能加速。
6. 點選「下一步」。
7. 在「確認並提交」部分，詳閱協議內容。
8. 如果您接受協議條款，請按一下「建立」。

確認預留項目後，詳細資料會顯示在「Reservations」(預留項目) 頁面。

## 使用 Looker 連線

**捷徑：**如果您已有 Looker 模型，且該模型在已啟用 BI Engine 的專案中，使用具備服務帳戶的 BigQuery 資料集，則不需進行額外設定。

下列操作說明將引導您設定 Looker 與 BigQuery。

1. 以管理員身分登入 Looker。
2. 在 Looker 的 BigQuery 說明文件中，完成下列部分：

   1. [建立服務帳戶](https://docs.cloud.google.com/looker/docs/db-config-google-bigquery?hl=zh-tw#creating_a_service_account_and_downloading_the_json_credentials_certificate)。
   2. [在 Looker 中為 BigQuery 連線設定 OAuth](https://docs.cloud.google.com/looker/docs/db-config-google-bigquery?hl=zh-tw#configuring_oauth_for_a_bigquery_connection)。**注意：** 請確認您建立的服務帳戶使用的帳單專案，與您啟用 BI Engine 預留項目的專案相同。
3. 按一下「開發」分頁標籤，然後選取「開發模式」。
4. 為資料集生成 LookML 模型和專案。詳情請參閱[將 Looker 連線至資料庫的操作說明](https://docs.cloud.google.com/looker/docs/connecting-to-your-db?hl=zh-tw)。
5. 使用「探索」選單，前往與新模型檔案名稱「Explore 311\_service\_requests\_copy」 (或您命名的探索名稱) 相關聯的探索。

您已成功將 Looker 連結至 BigQuery。您可以使用 Looker 的「系統活動」功能產生 Looker 使用情形報表，並根據 BigQuery 專屬成效指標分析查詢成效。如要瞭解各種 BigQuery BI Engine 查詢成效指標，請參閱「[BigQuery BI Engine 指標](https://docs.cloud.google.com/looker/docs/query-performance-metrics?hl=zh-tw#bigquery_bi_engine_metrics)」。

## 清除所用資源

如要避免系統向您的 Google Cloud 帳戶收取本快速入門導覽課程所用資源的費用，您可以刪除專案、刪除 BI Engine 預留項目，或同時刪除兩者。

### 刪除專案

如要避免付費，最簡單的方法就是刪除您為了本教學課程而建立的專案。

如要刪除專案，請進行以下操作：

**警告：** 刪除專案會出現以下結果：

* **專案中的所有內容都會遭到刪除。**如果使用現有專案來進行本教學課程，刪除專案將一併移除當中已完成的其他工作。
* **自訂專案 ID 會消失。**您建立這個專案時，可能已建立日後使用的自訂專案 ID。如要保留使用該專案 ID 的網址 (例如 **appspot.com** 網址)，請刪除在該專案中選取的資源，而不是刪除整個專案。如果打算進行多個教學課程及快速入門導覽課程，重複使用專案有助於避免超出專案配額限制。

1. 前往 Google Cloud 控制台的「Manage resources」(管理資源) 頁面。

   [前往「BI Engine」頁面](https://console.cloud.google.com/cloud-resource-manager?hl=zh-tw)
2. 在專案清單中選取要刪除的專案，然後點選「Delete」(刪除)。
3. 在對話方塊中輸入專案 ID，然後按一下「Shut down」(關閉)，即可刪除專案。

### 刪除保留項目

或者，如果您打算保留專案，可以刪除預留運算資源，避免產生額外的 BI Engine 費用。

如要刪除預留項目，請按照下列步驟操作：

1. 在 Google Cloud 控制台的「Administration」(管理) 下方，前往「BI Engine」頁面。

   [前往「BI Engine」頁面](https://console.cloud.google.com/bigquery/admin/bi-engine?hl=zh-tw)

   **注意：** 如果系統提示您啟用 **BigQuery Reservation API**，請點選「啟用」。
2. 在「Reservations」(預留項目) 部分，找出預留項目。
3. 在「Actions」(動作) 欄中，按一下預留項目右側的 more\_vert 圖示，然後選擇「Delete」(刪除)。
4. 在「Delete reservation?」(要刪除預留項目嗎？) 對話方塊中，輸入「Delete」，然後按一下「DELETE」(刪除)。

## 後續步驟

還有許多其他選項，可用於管理 Looker、自訂資料模型，以及向使用者公開資料。詳情請參閱下列資源：

* [Looker 說明文件](https://docs.cloud.google.com/looker/docs?hl=zh-tw)
* [Looker 最佳做法](https://docs.cloud.google.com/looker/docs/best-practices/home?hl=zh-tw)
* [Looker 訓練](https://www.cloudskillsboost.google/journeys/28?hl=zh-tw)




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-16 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-16 (世界標準時間)。"],[],[]]