Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 在 Google Cloud 控制台探索 BigQuery

Google Cloud 控制台中的 BigQuery 是圖形介面，可讓您建立及管理 BigQuery 資源。您可以使用 Google Cloud 控制台查看資料表和資料集、建立及執行 SQL 查詢、建構管道，以及執行其他工作，協助您管理 BigQuery 工作流程。

## 事前準備

- 登入 Google Cloud 帳戶。如果您未曾使用過 Google Cloud，歡迎[建立帳戶](https://console.cloud.google.com/freetrial?hl=zh-tw)，親自體驗實際使用我們產品的成效。新客戶還能獲得價值 $300 美元的免費抵免額，用於執行、測試及部署工作負載。
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

1. 啟用 BigQuery API (如果尚未啟用)。

   **啟用 API 所需的角色**

   您必須具備 `serviceusage.services.enable` 權限，才能啟用 API。如果您建立了專案，可能已透過擁有者角色 (`roles/owner`) 取得這項權限。否則，您可以透過 Service Usage 管理員角色 (`roles/serviceusage.serviceUsageAdmin`) 取得這項權限。[瞭解如何授予角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)。

   [啟用 API](https://console.cloud.google.com/apis/enableflow?apiid=bigquery&hl=zh-tw)

   如果是新專案，系統會自動啟用 BigQuery API。
2. 選用：為專案[啟用計費功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw)。如果您不想啟用計費功能或提供信用卡，仍可按照本文中的步驟操作。BigQuery 提供沙箱，方便您執行步驟。詳情請參閱「[啟用 BigQuery 沙箱](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw#setup)」。
   **注意：**如果專案有帳單帳戶，而您想使用 BigQuery 沙箱，請[停用專案的計費功能](https://docs.cloud.google.com/billing/docs/how-to/modify-project?hl=zh-tw#disable_billing_for_a_project)。

## 開啟 Google Cloud 控制台

1. 前往 Google Cloud 控制台。

   [前往控制台](https://console.cloud.google.com/?hl=zh-tw)
2. 在 Google Cloud 控制台工具列中，按一下menu「Navigation menu」(導覽選單)。
3. 依序點選**「解決方案」>「所有產品」**。
4. 在「數據分析」部分，點選「BigQuery」。

   BigQuery「[**Studio**](#open-ui)」頁面隨即開啟。
5. 如要控制 BigQuery 導覽選單，請執行下列任一操作：

   * 如要展開導覽選單，請將游標懸停在 圖示上，然後按一下「left\_panel\_open」left\_panel\_open「切換 BigQuery 導覽選單」。
   * 如要收合導覽選單，請按一下 left\_panel\_close「Toggle BigQuery navigation menu」(切換 BigQuery 導覽選單)。

您可以使用導覽選單開啟下列頁面：

* [**總覽**](#open-overview)：探索教學課程、功能和資源。
* [**Studio**](#open-ui)：可顯示 BigQuery 資源並執行常見工作。
* [**搜尋**](#search-page) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：可讓您使用自然語言查詢，搜尋 BigQuery 中的 Google Cloud 資源。
* [**代理**](#agents-page) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))：可建立資料代理並與其對話，回答 BigQuery 資源相關問題。

您也可以使用導覽選單，在下列選單區段中執行特定工作：

* **管道和整合**：可建立及設定[資料移轉](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)、建立及列出 [Dataform](https://docs.cloud.google.com/bigquery/docs/orchestrate-workloads?hl=zh-tw#dataform) 存放區，以及建立及列出[排定的資源](https://docs.cloud.google.com/bigquery/docs/orchestrate-workloads?hl=zh-tw)，例如[排定的查詢](https://docs.cloud.google.com/bigquery/docs/scheduling-queries?hl=zh-tw)。
* **治理**：可顯示共用的[資料交換](https://docs.cloud.google.com/bigquery/docs/analytics-hub-manage-exchanges?hl=zh-tw)和[資料無塵室](https://docs.cloud.google.com/bigquery/docs/data-clean-rooms?hl=zh-tw)，並在「[安全中心](https://docs.cloud.google.com/bigquery/docs/security-center-overview?hl=zh-tw)」頁面管理安全性和存取權政策。
* **管理**：可讓您執行管理工作，例如[監控](https://docs.cloud.google.com/bigquery/docs/admin-resource-charts?hl=zh-tw)、查看[工作](https://docs.cloud.google.com/bigquery/docs/admin-jobs-explorer?hl=zh-tw)相關資訊、[管理容量](https://docs.cloud.google.com/bigquery/docs/reservations-intro?hl=zh-tw)、查看[災難復原](https://docs.cloud.google.com/bigquery/docs/managed-disaster-recovery?hl=zh-tw)相關資訊，以及顯示[建議](https://docs.cloud.google.com/bigquery/docs/recommendations-intro?hl=zh-tw)。
* **遷移**：可查看及設定將[資料倉儲遷移](https://docs.cloud.google.com/bigquery/docs/migration/migration-overview?hl=zh-tw)至 BigQuery 的選項。
* **合作夥伴中心**：提供[合作夥伴](https://docs.cloud.google.com/bigquery/docs/bigquery-ready-overview?hl=zh-tw#partner_center)的工具和服務，加快工作流程。
* **設定**：可自訂 BigQuery 使用者和管理員設定。
* **版本資訊**：包含 BigQuery 的最新[產品更新和公告](https://docs.cloud.google.com/bigquery/docs/release-notes?hl=zh-tw)。

## BigQuery Studio 頁面

BigQuery [**Studio**](https://docs.cloud.google.com/bigquery/docs/query-overview?hl=zh-tw#bigquery-studio) 頁面會顯示 BigQuery 資源，並可讓您執行常見工作。Studio 頁面包含下列元件：

1. *左側窗格的「Explorer」分頁*：使用「Explorer」分頁處理資料集、連線、程式碼資產和其他 BigQuery 資源，以及查看[工作記錄](https://docs.cloud.google.com/bigquery/docs/managing-jobs?hl=zh-tw#list_jobs_in_a_project)。
2. *左側窗格的「Data」(資料) 分頁*：使用「Data」(資料) 分頁，瀏覽及檢查已釘選專案的資料階層，包括資料集、資料表、檢視表、模型、常式、屬性圖和連線。程式碼資產不會列在「Data」(資料) 窗格中，但您可以在單一區域的「Files」(檔案) 分頁，或所有區域的「Explorer」(探索工具) 分頁中存取程式碼資產。

   「Data」(資料) 窗格也包含將資料新增至 BigQuery 的選項。按一下 add「Add data」(新增資料)，即可使用搜尋和篩選功能，找出要使用的資料來源。選取資料來源後，您可以根據資料來源提供的功能，執行下列操作：

   * **透過外部資料設定 BigQuery 資料表 (*聯盟*)**：可讓 BigQuery 存取外部資料，不必將資料擷取至 BigQuery。您可以[建立資料表來存取外部資料](https://docs.cloud.google.com/bigquery/docs/external-data-sources?hl=zh-tw)，或[建立與外部來源的連線](https://docs.cloud.google.com/bigquery/docs/connections-api-intro?hl=zh-tw)。
   * **將資料載入 BigQuery**：設定[資料移轉](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw)或使用[合作夥伴功能](https://docs.cloud.google.com/bigquery/docs/load-data-third-party?hl=zh-tw)，將資料載入 BigQuery。建議您將資料載入 BigQuery，以最佳方式大規模處理資料。
   * **將變更資料擷取至 BigQuery**：擷取並套用變更，將資料從資料來源複製到 BigQuery。您可以使用 [datastream](https://docs.cloud.google.com/datastream/docs/overview?hl=zh-tw) 等應用程式或[合作夥伴解決方案](https://docs.cloud.google.com/bigquery/docs/load-data-third-party?hl=zh-tw)，從資料來源擷取資料。
   * **將資料串流至 BigQuery**：以低延遲的方式將資料擷取至 BigQuery。您可以使用 [Dataflow](https://docs.cloud.google.com/dataflow/docs/guides/write-to-bigquery?hl=zh-tw)、[Pub/Sub](https://docs.cloud.google.com/pubsub/docs/overview?hl=zh-tw) 或[合作夥伴解決方案](https://docs.cloud.google.com/bigquery/docs/load-data-third-party?hl=zh-tw)等應用程式，從資料來源擷取資料。

   如要進一步瞭解如何將資料載入 BigQuery，請參閱「[載入資料簡介](https://docs.cloud.google.com/bigquery/docs/loading-data?hl=zh-tw)」。
3. *左側窗格的「Files」(檔案) 分頁*：使用「Files」(檔案) 分頁，透過資料夾整理程式碼資產，例如已儲存的查詢和筆記本。詳情請參閱「[使用資料夾整理程式碼資產](https://docs.cloud.google.com/bigquery/docs/code-asset-folders?hl=zh-tw)」。
4. *左側窗格的「Source control」(原始碼控制) 分頁* ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))：使用「Source control」(原始碼控制) 分頁，透過存放區或以 Git 為基礎的遠端存放區，儲存程式碼、編輯檔案，以及使用版本管控功能追蹤變更。詳情請參閱「[存放區簡介](https://docs.cloud.google.com/bigquery/docs/repository-intro?hl=zh-tw)」。
5. *「首頁」分頁*：使用「首頁」分頁查看下列資源：

   * 「Check out what's new in Studio」(查看 Studio 的新功能) 專區，列出 BigQuery Studio 的新功能。按一下「試用」即可查看功能。如果沒有看到該部分，請按一下「What's new in Studio」展開。
   * 「Create new」(新建) 專區，提供建立新 SQL 查詢、筆記本、Apache Spark 筆記本、資料畫布、資料準備檔案、管道或資料表的選項。
   * 「Recent」(近期) 專區：可查看最近存取的 10 項資源。這些資源包括資料表、已儲存的查詢、模型和常式。
   * 「Try with templates」(試用範本) 專區：您可以使用範本開始查詢資料及使用筆記本。
   * 「Add your own data」(新增自己的資料) 專區，協助您開始將資料載入 BigQuery。
6. ***查詢編輯器***：使用查詢編輯器建立及[執行互動式查詢](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#queries)。您也可以在執行查詢後開啟的「Query results」(查詢結果) 窗格中查看結果。在查詢結果中，您可以透過工作階段專屬的「Recent」(近期) 窗格查看近期結果。

### 探索「Studio」頁面

BigQuery 的「Studio」頁面是查看 BigQuery 資源及執行常見工作 (例如建立資料集、建立及執行 Notebook) 的中心。

**注意：**如要瞭解如何在 Studio 使用鍵盤快速鍵，請按一下 BigQuery Studio 工具列中的 keyboard「BigQuery Studio 快速鍵」：

如要探索「Studio」頁面，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery Studio」頁面。

   [前往 Studio](https://console.cloud.google.com/bigquery?hl=zh-tw)

   或者，您也可以在瀏覽器中輸入下列網址：

   ```
   https://console.cloud.google.com/bigquery
   ```

   「Studio」頁面會開啟您最近存取的專案。
2. 點選左側窗格中的「Explorer」分頁標籤。

   「Explorer」窗格會列出不同的程式碼資產和資料資源，並可讓您搜尋 BigQuery 資源。

   **注意：**您可以按一下 first\_page「Collapse left pane」(收合左側窗格) 或 last\_page「Expand left pane」(展開左側窗格)，展開或收合左側窗格。
3. 前往 `bigquery-public-data` 專案，按一下 arrow\_right「Toggle node」(切換節點) 展開專案，然後點選「Datasets」(資料集)。「Details」(詳細資料) 窗格中會開啟新分頁，顯示專案中所有資料集的清單。

   BigQuery [公開資料集](https://docs.cloud.google.com/bigquery/public-data?hl=zh-tw)儲存在 BigQuery 中，並透過 Google Cloud 公開資料集計畫提供給一般大眾使用。
4. 在清單中，點選「`america_health_rankings`」資料集。
5. 在「Overview」(總覽) 分頁中，查看資料集中儲存的資源，例如資料表、模型和常式。
6. 按一下「Details」(詳細資料) 分頁標籤。這個分頁會顯示資料集的所有詳細資料
   包括中繼資料資訊
7. 如要瀏覽不同的分頁和資源，請使用導覽標記，如以下範例所示：
8. 在「Explorer」窗格中，點選「工作記錄」。這會在新分頁中開啟工作記錄清單：

   每當您載入、匯出、查詢或複製資料時，BigQuery 都會自動建立、排定及執行工作，追蹤工作進度。

   1. 如要查看自己的工作詳細資料，請按一下「個人記錄」。
   2. 如要查看專案中近期工作的詳細資料，請按一下「Project history」(專案記錄)。

      **注意：**如要查看工作詳細資料，或從查詢工作開啟查詢，請在工作或查詢的「Actions」(動作) 欄中，依序點選 more\_vert「Actions」(動作) >「Show job details」(顯示工作詳細資料) 或「View job in editor」(在編輯器中查看工作)。
9. 在左側窗格中，按一下 fork\_right「Source control」(原始碼控管) 分頁標籤 ([預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages))。

   您可以使用存放區，對 BigQuery 中使用的檔案執行版本管控。BigQuery 使用 Git 記錄變更及管理檔案版本。

   您可以使用存放區中的工作區，編輯儲存在存放區中的程式碼。在「Source control」(原始碼控制) 窗格中點選「workspace」(工作區)，即可在詳細資料窗格的分頁中開啟。
10. 在左側窗格中，按一下「folder Files」(檔案)。

    您可以在「檔案」分頁建立使用者和團隊資料夾，用於儲存及管理程式碼資產。
11. 按一下「home 首頁」分頁標籤。

    「Home」(首頁) 分頁提供連結和範本，方便您開始使用 BigQuery。

    如果關閉「Home」分頁，只要在「Explorer」分頁中點選 home「Home」，即可開啟該分頁。
12. 按一下查詢編輯器。這個分頁標籤會顯示 search\_insights「未命名的查詢」。

    您可以使用查詢編輯器建立 SQL 查詢、執行 SQL 查詢及查看結果。

    如果關閉查詢編輯器，可以按一下「Home」(首頁) 分頁標籤，然後在「Create new」(新建) 區段中，按一下 add\_box「SQL query」(SQL 查詢)，即可開啟查詢編輯器。

### 在 Studio 中使用分頁

每當您選取資源或在詳細資料窗格中點選 add\_box「SQL query」(SQL 查詢) 時，系統就會開啟新分頁。如果開啟多個分頁，可以將分頁分割成兩個窗格，並排查看。

#### 防止分頁遭到取代

為避免分頁過多，點選資源時，系統會在同一個分頁中開啟。如要在另一個分頁中開啟資源，請按照下列步驟操作：

1. 按住 `Ctrl` 鍵 (或 macOS 的 `Command` 鍵)，然後點選資源。
2. 或按兩下分頁名稱。名稱會從斜體變更為一般字型。
3. 如果不小心取代了目前頁面，只要在詳細資料窗格中按一下 tab\_recent「Recent tabs」(最近使用的分頁)，即可找到該頁面。

#### 分割及取消分割分頁

如要將分頁分割成兩個窗格，請按照下列步驟操作：

1. 按一下分頁名稱旁的「開啟選單」圖示 arrow\_drop\_down。
2. 選取下列選項之一：

   * 如要將所選分頁放在左側窗格，請選取「Split tab to left」(將分頁分割至左側)。
   * 如要將所選分頁移至右側窗格，請選取「Split tab to right」(將分頁分割至右側)。**注意：**如果只開啟一個分頁，就無法使用這些選單選項。
3. 如要取消分割分頁，請在其中一個開啟的分頁上選取「arrow\_drop\_down 開啟選單」，然後選取「將分頁移至左側窗格」或「將分頁移至右側窗格」。

#### 使用分割分頁查詢資料

如要在查詢資料表時分割分頁，請按照下列步驟操作：

1. 在「Explorer」選單中，點選要查詢的資料表。
2. 依序點選「查詢」和「在新分頁中開啟」或「在分割分頁中開啟」：
3. 按一下要查詢的欄位名稱：

下圖顯示詳細資料窗格，其中有兩個開啟的分頁。一個分頁顯示 SQL 查詢，另一個分頁顯示資料表詳細資料。

#### 在窗格之間移動分頁

如要將分頁從一個窗格移至另一個窗格，請按照下列步驟操作：

1. 按一下分頁名稱旁的「開啟選單」圖示 arrow\_drop\_down。
2. 選取「將分頁移至右側窗格」或「將分頁移至左側窗格」(視可用的選項而定)。

#### 關閉所有其他分頁

如要關閉所有分頁 (保留一個)，請按照下列步驟操作：

1. 按一下分頁名稱旁的「開啟選單」圖示 arrow\_drop\_down。
2. 選取 cancel「關閉其他分頁」。

## 「總覽」頁面

BigQuery 的「Overview」(總覽) 頁面是探索教學課程、功能和資源的中心，可協助您充分運用 BigQuery。無論是初次執行查詢，還是探索進階 AI/機器學習功能，各種技能等級的使用者都能獲得指引。

您可以使用「Overview」(總覽) 頁面，依角色或興趣 (例如資料分析或資料科學) 尋找資源。這些資源可協助您找到最相關的內容，快速上手。

### 探索「總覽」頁面

1. 前往控制台的「Overview」(總覽) 頁面。

   [前往總覽頁面](https://console.cloud.google.com/bigquery/overview?hl=zh-tw)

   您也可以在瀏覽器中輸入下列網址，開啟 BigQuery「Overview」(總覽) 頁面：

   ```
   https://console.cloud.google.com/bigquery/overview
   ```
2. 查看「Overview」(總覽) 頁面的下列部分：

   * **簡介**部分：透過簡短影片概略介紹 BigQuery 的功能。
   * 「開始使用」部分：旨在透過實作學習。您可以在這裡啟動互動式指南，瞭解如何使用 BigQuery 功能。
   * 「Find out more」(瞭解詳情) 專區：顯示 BigQuery 版本資訊，方便您查看最新功能公告和更新。
   * 「Explore possibilities」(探索各種可能) 專區：提供特定功能的深入教學課程和學習機會。

### 自訂「總覽」頁面

您可以自訂「Overview」(總覽) 頁面，顯示或隱藏與工作或角色相關的資訊。

1. 前往「總覽」頁面的篩選列。
2. 請點選最符合您目前工作或角色的選項：

   * 資料分析
   * 資料科學
   * 資料工程
   * 資料管理

   選取工作後，「Introduction」(簡介)、「Get started」(開始使用) 和「Explore Possibilities」(探索各種可能) 區段中的內容會動態變更，顯示最相關的內容。
3. 選用：如要根據特定需求調整「Overview」(總覽) 頁面上的內容，請隱藏個別資訊卡：

   1. 在資訊卡中，按一下「more\_vert 更多選項」。
   2. 選擇「隱藏卡片」。系統會儲存每位使用者對隱藏資訊卡的偏好設定。
   3. 如要取消隱藏資訊卡，請按一下該部分結尾的「Show hidden content」(顯示隱藏內容)。
4. 如果整個部分都不相關，請按一下 keyboard\_arrow\_up 摺疊該部分。系統會儲存您對收合區段的使用者偏好設定。

## 「搜尋」頁面

在「[**Search**](https://docs.cloud.google.com/bigquery/docs/search-resources?hl=zh-tw)」(搜尋) 頁面 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，您可以使用自然語言查詢，搜尋 BigQuery 中的 Google Cloud 資源。

如要瞭解如何選擇使用「Search」(搜尋) 頁面，請參閱「[搜尋資源](https://docs.cloud.google.com/bigquery/docs/search-resources?hl=zh-tw)」。

## 「代理」頁面

「Agents」(代理) 頁面 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages)) 是建立資料代理並與其對話的中心位置，這些代理專門回答有關 BigQuery 資源的問題。

資料代理包含資料表的中繼資料，以及特定用途的查詢處理指示，可定義最佳方式，回答使用者對所選資料表的問題。使用者可以與資料代理[對話](https://docs.cloud.google.com/bigquery/docs/create-conversations?hl=zh-tw)，以自然語言詢問 BigQuery 資料相關問題。詳情請參閱「[建立資料代理](https://docs.cloud.google.com/bigquery/docs/create-data-agents?hl=zh-tw)」。

如要瞭解如何建立代理及使用對話式數據分析，請參閱「[BigQuery 對話式數據分析](https://docs.cloud.google.com/bigquery/docs/conversational-analytics?hl=zh-tw)」。

## 限制

BigQuery Google Cloud 控制台不支援[虛擬私有雲](https://docs.cloud.google.com/vpc-service-controls/docs/supported-products?hl=zh-tw#console)或 [Private Service Connect](https://docs.cloud.google.com/vpc/docs/private-service-connect?hl=zh-tw)。

## 排解 BigQuery Google Cloud 控制台問題

使用 BigQuery 時，如果 Google Cloud 控制台發生問題，例如網頁無法載入、回應速度緩慢或缺少功能，請嘗試下列疑難排解步驟。

### 常見的瀏覽器修正方式

許多 Google Cloud 控制台問題都是由本機瀏覽器設定或快取資料造成。

* **瀏覽器疑難排解：**如需一般瀏覽器疑難排解步驟，例如使用無痕模式、清除快取和 Cookie，或關閉瀏覽器擴充功能，請參閱「[排解 Google Cloud 控制台載入網頁問題](https://docs.cloud.google.com/support/docs/troubleshoot-console-page-loading?hl=zh-tw)」。
* **確認服務健康狀態：**查看 [Google Cloud **Service Health** 資訊主頁](https://status.cloud.google.com/?hl=zh-tw)，瞭解 BigQuery 服務是否中斷。

### 連線能力和防火牆需求

如果您在公司 VPN 或 Proxy 後方工作，可能會封鎖控制台所需的 API 呼叫。請確認網路管理員已將下列網域加入許可清單：

* `https://cloudconsole-pa.clients6.google.com`
* `https://clients6.google.com`
* `https://cloudusersettings-pa.clients6.google.com`

API 端點遭到封鎖的常見症狀包括：自動完成建議的進度指標持續旋轉，或即使具備正確的 IAM 角色，仍出現權限錯誤。

### 提升大型專案的效能

如果專案包含大量資料集或資料表，「Explorer」分頁的載入速度可能會變慢。

* **使用最小載入參數：**在網址中附加 `?minimal=true`，即可防止資源樹狀結構預先載入。例如：

  `https://console.cloud.google.com/bigquery?minimal=true&project=PROJECT_ID`
* **取消固定未使用的專案：**移除未主動使用的固定專案，減輕「Explorer」分頁的負載。
* **強制重新整理中繼資料：**如果您透過 API/CLI 修改資料表，但控制台未顯示變更，請強制重新整理 (Ctrl+Shift+R 或 Cmd+Shift+R)。請使用 `INFORMATION_SCHEMA` 查詢做為可靠資料來源。

### 排解地圖和圖表問題

* **地理空間 (TinyMap)：**只有在查詢結果包含 `GEOGRAPHY` 欄時，才會顯示地理空間圖表分頁。地圖圖表最多只能顯示 20,000 個地圖項目或 100 萬個頂點。
* **圖表：**結果必須包含至少一個數值欄，才能生成圖表。如果出現「沒有可顯示的資料」警告，請檢查所選 X 軸維度中是否有空值。

### 排解資料歷程和剖析問題

* **歷程延遲：**資料歷程資訊並非即時。歷程資料最多需要 30 分鐘才能同步。
* **必要 API：**確認專案已啟用 Dataplex API (`dataplex.googleapis.com`) 和 Data Catalog API (`datacatalog.googleapis.com`)。

### 排解 BigQuery Studio 和已儲存查詢的問題

* **已儲存的查詢遷移限制：**如果已儲存的查詢超過 2,500 項，自動遷移工具就無法處理。請與 [Cloud Customer Care](https://cloud.google.com/support?hl=zh-tw) 聯絡，要求手動遷移。
* **必要 API：**如要在 BigQuery Studio 中儲存指令碼和筆記本，專案必須啟用 Dataform API (`dataform.googleapis.com`)。

### 聯絡支援團隊

如果問題仍未解決，請先收集下列資訊，再建立支援單：

1. **HAR 檔案：**重現問題時，記錄網路要求記錄 (使用瀏覽器開發人員工具的「Network」分頁，並勾選「Preserve Log」)。
2. **控制台記錄：**擷取瀏覽器開發人員控制台中顯示的 JavaScript 錯誤 (Ctrl+Shift+I > 控制台)。
3. **專案 ID：**您目前使用的專案 ID。
4. **追蹤號碼：**錯誤橫幅中顯示的追蹤 ID。

## 後續步驟

* 如要瞭解如何查詢公開資料集及使用 BigQuery 沙箱，請參閱「[使用沙箱試用 BigQuery](https://docs.cloud.google.com/bigquery/docs/sandbox?hl=zh-tw)」。
* 如要瞭解如何在 Google Cloud 控制台中載入及查詢資料，請參閱「[載入及查詢資料](https://docs.cloud.google.com/bigquery/docs/quickstarts/load-data-console?hl=zh-tw)」。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-11-05 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-11-05 (世界標準時間)。"],[],[]]