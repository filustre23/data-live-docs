Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 Google Cloud 控制台探索 BigQuery

BigQuery Google Cloud 控制台提供圖形介面，方便您建立及管理 BigQuery 資源。您也可以使用控制台完成執行 SQL 查詢和建立管道等工作。

在本逐步導覽中，您將探索 BigQueryGoogle Cloud 控制台的元件。

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

1. 啟用 BigQuery API。

   **啟用 API 時所需的角色**

   如要啟用 API，您需要服務使用情形管理員 IAM 角色 (`roles/serviceusage.serviceUsageAdmin`)，其中包含 `serviceusage.services.enable` 權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/flows/enableapi?apiid=bigquery&hl=zh-tw)

   新專案會自動啟用 BigQuery API。
2. 選用：
   [啟用專案的計費功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw)。如果您不想啟用帳單或提供信用卡，仍可按照本文步驟操作。BigQuery 提供沙箱，方便您執行這些步驟。詳情請參閱「[啟用 BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw#setup)」一文。
   **注意：**如果專案有帳單帳戶，且您想使用 BigQuery 沙箱，請[停用專案的帳單功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw#disable_billing_for_a_project)。

## 開啟 Google Cloud 控制台

1. 前往 Google Cloud 控制台。

   [前往控制台](https://console.cloud.google.com/?hl=zh-tw)
2. 在 Google Cloud 控制台工具列中，按一下 menu「導覽選單」。
3. 依序點選「解決方案」**> 所有產品**。
4. 在「數據分析」部分，點選「BigQuery」。

   BigQuery [**Studio**](#open-ui) 頁面隨即開啟。
5. 如要展開或收合選單，請按一下 last\_page 或 first\_page「切換 BigQuery 導覽選單」。

您可以使用導覽選單開啟下列頁面：

* [**總覽**](#open-overview) ([搶先體驗版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：
  可讓您探索教學課程、功能和資源。
* [**Studio**](#open-ui)：可顯示 BigQuery 資源並執行常見工作。
* [**搜尋**](#search-page) ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：
  可讓您使用自然語言查詢，搜尋 BigQuery 的 Google Cloud 資源。
* [**代理程式**](#agents-page) ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：
  可讓您建立資料代理程式並與之對話，這些代理程式專門回答
  有關 BigQuery 資源的問題。

您也可以使用導覽選單，在下列選單區段中執行特定工作：

* **管道和整合**：可建立及設定[資料移轉](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)、建立及列出 [Dataform](https://docs.cloud.google.com/bigquery/docs/orchestrate-workloads?hl=zh-tw#dataform) 存放區，以及建立及列出[排程資源](https://docs.cloud.google.com/bigquery/docs/orchestrate-workloads?hl=zh-tw)，例如[排程查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)。
* **治理**：顯示共用的[資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)和[淨室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)、查看[政策標記](https://docs.cloud.google.com/bigquery/docs/column-level-security?hl=zh-tw)，以及[管理中繼資料](https://docs.cloud.google.com/bigquery/docs/automatic-discovery?hl=zh-tw)。
* **管理**：可執行管理工作，例如[監控](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)、查看[工作](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)相關資訊、[管理容量](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)、查看[災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)相關資訊，以及顯示[建議](https://docs.cloud.google.com/bigquery/docs/recommendations-intro?hl=zh-tw)。
* **遷移**：可供您查看及設定[將資料倉儲遷移至 BigQuery](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw) 的選項。
* **合作夥伴中心**：提供[合作夥伴](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-overview?hl=zh-tw#partner_center)的工具和服務，加快工作流程。
* **設定** ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：
  可自訂 BigQuery 預設值或使用者介面[設定](https://docs.cloud.google.com/bigquery/docs/default-configuration?hl=zh-tw#configuration-settings)。
* **版本資訊**：包含 BigQuery 的最新[產品更新和公告](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)。

## BigQuery Studio 頁面

BigQuery [**Studio**](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 頁面會顯示 BigQuery 資源，並讓您執行常見工作。Studio 頁面包含下列元件：

1. *左側窗格的「探索」分頁*：使用「探索」分頁處理資料表、檢視區塊、常式和其他 BigQuery 資源，並查看[工作記錄](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#list_jobs_in_a_project)。

   左側窗格也提供將資料新增至 BigQuery 的選項。按一下「新增資料」add後，即可使用搜尋和篩選功能，找出要使用的資料來源。選取資料來源後，您可以根據資料來源提供的功能執行下列操作：

   * **透過外部資料設定 BigQuery 資料表 (*聯盟*)**：可讓 BigQuery 存取外部資料，不必將資料匯入 BigQuery。您可以[建立資料表來存取外部資料](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw)，或[建立與外部來源的連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)。
   * **將資料載入 BigQuery**：設定[資料移轉](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)或使用[合作夥伴功能](https://docs.cloud.google.com/bigquery/docs/load-data-third-party?hl=zh-tw)，將資料載入 BigQuery。建議您將資料載入 BigQuery，以最佳方式大規模處理資料。
   * **將變更資料擷取至 BigQuery**：擷取並套用變更，將資料從資料來源複製到 BigQuery。您可以透過 [datastream](https://docs.cloud.google.com/datastream/docs/overview?hl=zh-tw) 或[合作夥伴解決方案](https://docs.cloud.google.com/bigquery/docs/load-data-third-party?hl=zh-tw)等應用程式，從資料來源擷取資料。
   * **將資料串流至 BigQuery**：以低延遲的方式將資料擷取至 BigQuery。您可以使用 [Dataflow](https://docs.cloud.google.com/dataflow/docs/guides/write-to-bigquery?hl=zh-tw)、[Pub/Sub](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw) 或[合作夥伴解決方案](https://docs.cloud.google.com/bigquery/docs/load-data-third-party?hl=zh-tw)等應用程式，從資料來源擷取資料。

   如要進一步瞭解如何將資料載入 BigQuery，請參閱「[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」。
2. *左窗格的「傳統 Explorer」分頁*：使用舊版「Explorer」窗格查看 BigQuery 資源。
3. *左側窗格的「檔案」分頁* ([預覽](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))：
   使用「檔案」分頁，透過資料夾整理程式碼資產，例如儲存的查詢和筆記本。詳情請參閱「[使用資料夾整理程式碼資產](https://docs.cloud.google.com/bigquery/docs/code-asset-folders?hl=zh-tw)」。
4. *左窗格的「存放區」分頁* ([預覽版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))：
   使用「存放區」分頁儲存程式碼、編輯檔案，以及透過存放區或以 Git 為基礎的遠端存放區，使用版本管控功能追蹤變更。詳情請參閱「[存放區簡介](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw)」。
5. ***首頁**分頁*：使用「首頁」分頁查看下列資源：

   * 「查看 Studio 的新功能」部分會列出 BigQuery Studio 的新功能。按一下「試用」即可查看功能。如果沒有看到這個部分，請按一下「What's new in Studio」(Studio 的新功能) 展開這個部分。
   * 「建立新項目」部分，提供建立新 SQL 查詢、筆記本、Apache Spark 筆記本、資料畫布、資料準備檔案、管道或資料表的選項。
   * 「最近」部分：可查看最近存取的 10 項資源。這些資源包括資料表、已儲存的查詢、模型和常式。
   * 「使用範本試試看」部分，可讓您使用範本開始查詢資料及處理筆記本。
   * 「新增自己的資料」部分，可協助您開始將資料載入 BigQuery。
6. *查詢編輯器*：使用查詢編輯器建立及[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)。您也可以在執行查詢後開啟的「Query results」(查詢結果) 窗格中查看結果。

### 探索「Studio」頁面

BigQuery 的「Studio」頁面是查看 BigQuery 資源的中心位置，您可以在這裡執行常見工作，例如建立資料集，以及建立及執行筆記本。

**注意：** 如要瞭解如何在 Studio 中使用鍵盤快速鍵，請在 BigQuery Studio 工具列中點選「BigQuery Studio 快速鍵」圖示 keyboard：

如要瀏覽 **Studio** 頁面，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的 BigQuery **Studio** 頁面。

   [前往 Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)

   你也可以在瀏覽器中輸入下列網址：

   ```
   https://console.cloud.google.com/bigquery
   ```

   「Studio」(工作室) 頁面隨即開啟，顯示您最近存取過的專案。
2. 點選左側窗格中的 explore「Explorer」。

   「Explorer」窗格會列出不同的程式碼資產和資料資源，並可供您搜尋 BigQuery 資源。

   **注意：** 按一下「收合左窗格」first\_page 或「展開左窗格」last\_page，即可展開及收合左窗格。
3. 前往 `bigquery-public-data` 專案，按一下 arrow\_right「Toggle node」(切換節點) 展開專案，然後按一下「Datasets」(資料集)。詳細資料窗格會開啟新分頁，顯示專案中的所有資料集清單。

   BigQuery [公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)儲存在 BigQuery 中，透過 Google Cloud 公開資料集計畫提供給一般大眾使用。
4. 在清單中，點選「`austin_crime`」資料集。
5. 在「總覽」分頁中，查看資料集中儲存的資源，例如資料表、模型和常式。
6. 按一下「詳細資料」分頁標籤。這個分頁會顯示資料集的所有詳細資料，包括中繼資料資訊。
7. 如要瀏覽不同分頁和資源，請使用如以下範例所示的麵包屑路徑：
8. 在「Explorer」窗格中，按一下「Job history」。系統會在新的分頁中開啟工作記錄清單：

   每次載入、匯出、查詢或複製資料時，BigQuery 都會自動建立、排定及執行工作，追蹤工作進度。

   1. 如要查看自己工作的詳細資料，請按一下「個人記錄」。
   2. 如要查看專案中近期工作的詳細資料，請按一下「專案記錄」。

      **注意：** 如要查看工作詳細資料，或從查詢工作開啟查詢，請在工作或查詢的「動作」欄中，依序點選 more\_vert「動作」>「顯示工作詳細資料」或「在編輯器中查看工作」。
9. 在左側窗格中，按一下「資料夾」folder\_data「存放區」分頁標籤 (「預覽」)。

   您可以使用存放區，對 BigQuery 中使用的檔案執行版本管控。BigQuery 會使用 Git 記錄變更，並管理檔案版本。

   您可以在存放區中使用工作區，編輯存放區中儲存的程式碼。在「Git repository」窗格中按一下[工作區](https://docs.cloud.google.com/bigquery/docs/workspaces?hl=zh-tw)，詳細資料窗格就會開啟該工作區的分頁。
10. 在左側窗格中，按一下「檔案」(「預覽」)。folder

    您可以在「檔案」分頁中建立使用者和團隊資料夾，儲存及整理程式碼資產。
11. 按一下「首頁」home分頁標籤。

    「首頁」分頁提供連結和範本，方便您開始使用 BigQuery。

    如果關閉「首頁」分頁，請點選「Explorer」分頁中的 home「首頁」開啟。
12. 按一下查詢編輯器。這個分頁標籤標示為「search\_insights」search\_insights「未命名的查詢」。

    您可以使用查詢編輯器建立及執行 SQL 查詢，並查看結果。

    如果關閉查詢編輯器，可以點選「首頁」分頁標籤，然後在「建立新項目」部分，點選 add\_box「SQL 查詢」，開啟查詢編輯器。

### 在 Studio 中使用分頁

每當您選取資源或在詳細資料窗格中點按「add\_box SQL 查詢」，系統就會開啟新分頁。如果開啟多個分頁，可以將分頁分成兩個窗格並並排顯示。

#### 防止分頁遭到取代

為減少分頁數量，點選資源時，系統會在同一個分頁中開啟資源。
如要在另一個分頁中開啟資源，請按照下列步驟操作：

1. 按住 `Ctrl` 鍵 (或 macOS 的 `Command` 鍵)，然後點按資源。
2. 你也可以按兩下分頁名稱，名稱會從斜體字改為一般字型。
3. 如果不小心取代了目前頁面，可以按一下詳細資料窗格中的「最近的分頁」tab\_recent，找到該頁面。

#### 分割及取消分割分頁

如要將分頁分割成兩個窗格，請按照下列步驟操作：

1. 按一下分頁名稱旁邊的「開啟選單」。arrow\_drop\_down
2. 選取下列選項之一：

   * 如要將選取的分頁放在左側窗格，請選取「將分頁分割到左側」。
   * 如要將所選分頁放在右側窗格中，請選取「將分頁分割到右側」。**注意：** 如果只開啟一個分頁，這些選單選項將無法使用。
3. 如要取消分割分頁，請在其中一個開啟的分頁上選取「開啟選單」arrow\_drop\_down，然後選取「將分頁移至左側窗格」或「將分頁移至右側窗格」。

#### 使用分割分頁查詢資料

如要在查詢資料表時分割分頁，請按照下列步驟操作：

1. 在「Explorer」選單中，點選要查詢的資料表。
2. 依序點按「查詢」和「在新分頁中開啟」或「在分割分頁中開啟」：
3. 按一下要查詢的欄位名稱：

下圖顯示詳細資料窗格，其中開啟了兩個分頁。一個分頁包含 SQL 查詢，另一個分頁則顯示資料表的詳細資料。

#### 在窗格之間移動分頁

如要將分頁從一個窗格移至另一個窗格，請按照下列步驟操作：

1. 按一下分頁名稱旁邊的「開啟選單」。arrow\_drop\_down
2. 選取「將分頁移至右側窗格」或「將分頁移至左側窗格」 (視可用選項而定)。

#### 關閉所有其他分頁

如要關閉所有分頁，只保留一個，請按照下列步驟操作：

1. 按一下分頁名稱旁邊的「開啟選單」。arrow\_drop\_down
2. 選取
   cancel
   「關閉其他分頁」。

## 「總覽」頁面

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要對「總覽」頁面提供意見，請依序點選「說明」**>「提供意見」**。

BigQuery **總覽**頁面是中心樞紐，您可以在這裡找到教學課程、功能和資源，充分運用 BigQuery。無論您是執行第一個查詢，還是探索進階 AI/機器學習功能，都能透過這項服務的引導式路徑，提升各方面的技能。

您可以在「總覽」頁面中，依據角色或興趣 (例如資料分析或資料科學) 尋找資源。這些資源可協助您找到最相關的內容，快速上手。

### 探索「總覽」頁面

1. 前往控制台的「總覽」頁面。

   [前往總覽頁面](https://console.cloud.google.com/bigquery/overview?hl=zh-tw)

   您也可以在瀏覽器中輸入下列網址，開啟 BigQuery **總覽**頁面：

   ```
   https://console.cloud.google.com/bigquery/overview
   ```
2. 查看「總覽」頁面的下列部分：

   * 「簡介」部分：提供 BigQuery 功能的快速影片簡介。
   * 「開始使用」專區：專為透過實作來學習而設計。您可以在這裡啟動互動式指南，瞭解如何使用 BigQuery 功能。
   * 「瞭解詳情」部分：顯示 BigQuery 版本資訊，方便您查看最新功能公告和更新。
   * 「探索各種可能性」專區：提供特定功能的深入教學課程和學習機會。

### 自訂「總覽」頁面

您可以自訂「總覽」頁面，顯示或隱藏與工作或角色相關的資訊。

1. 前往「總覽」頁面的篩選列。
2. 點選最符合目前工作或職務的選項：

   * 資料分析
   * 數據資料學
   * 資料工程
   * 資料管理

   選取工作後，「簡介」、「開始使用」和「探索可能性」部分會動態變更內容，顯示最相關的資訊。
3. 選用：如要根據特定需求調整「總覽」頁面的內容，請隱藏個別資訊卡：

   1. 在資訊卡中，按一下「更多選項」more\_vert。
   2. 選擇「隱藏卡片」。系統會為每位使用者儲存隱藏卡片的偏好設定。
   3. 如要取消隱藏資訊卡，請按一下該部分結尾的「顯示隱藏內容」。
4. 如果整個部分都不相關，請按一下 keyboard\_arrow\_up 將其收合。系統會儲存摺疊區塊的使用者偏好設定。

## 「搜尋」頁面

在「搜尋」頁面 ([預覽版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，您可以使用自然語言查詢，搜尋 BigQuery 的資源。 Google Cloud

如要瞭解如何選擇使用「搜尋」頁面，請參閱「[搜尋資源](https://docs.cloud.google.com/bigquery/docs/search-resources?hl=zh-tw)」。

## 「服務專員」頁面

「代理程式」頁面 ([搶先版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 是集中管理位置，您可以在這裡建立資料代理程式並與之對話，這些代理程式專門用來回答有關 BigQuery 資源的問題。

資料代理程式包含資料表的中繼資料，以及用來定義最佳方式的查詢處理指令，可回答使用者對您所選資料表集提出的問題。使用者可以與資料代理進行[對話](https://docs.cloud.google.com/bigquery/docs/ca/create-conversations?hl=zh-tw)，以自然語言詢問有關 BigQuery 資料的問題。詳情請參閱「[建立資料代理程式](https://docs.cloud.google.com/bigquery/docs/create-data-agents?hl=zh-tw)」。

如要瞭解如何建立代理程式及使用對話式數據分析，請參閱「[BigQuery 中的對話式數據分析](https://docs.cloud.google.com/bigquery/docs/conversational-analytics?hl=zh-tw)」一文。

## 限制

BigQuery Google Cloud 控制台不支援[虛擬私有雲](https://docs.cloud.google.com/vpc-service-controls/docs/supported-products?hl=zh-tw#console)或[私人服務連線](https://docs.cloud.google.com/vpc/docs/private-service-connect?hl=zh-tw)。

## 後續步驟

* 如要瞭解如何查詢公開資料集及使用 BigQuery 沙箱，請參閱「[使用沙箱試用 BigQuery](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)」。
* 如要瞭解如何在 Google Cloud 控制台中載入及查詢資料，請參閱「[載入及查詢資料](https://docs.cloud.google.com/bigquery/docs/quickstarts/load-data-console?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-06 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-06 (世界標準時間)。"],[],[]]