* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 為行銷分析資料建構 ELT 管道

本教學課程說明如何設定 ELT 工作流程，在 BigQuery 中擷取、載入及轉換行銷分析資料。

典型的 ELT 工作流程會定期從資料來源擷取新的客戶資料，並載入至 BigQuery。接著，系統會將非結構化資料處理為有意義的指標。在本教學課程中，您將使用 BigQuery 資料移轉服務設定行銷分析資料移轉作業，藉此建立 ELT 工作流程。接著，您會排定 Dataform 的執行時間，定期轉換資料。

在本教學課程中，您會使用 Google Ads 做為資料來源，但您也可以使用[BigQuery 資料移轉服務支援的任何資料來源](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw#supported_data_sources)。

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

### 必要的角色

如要取得完成本教學課程所需的權限，請要求管理員在專案中授予您下列 IAM 角色：

* [BigQuery 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.admin)  (`roles/bigquery.admin`)
* [Dataform 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.admin)  (`roles/dataform.admin`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

## 排定週期性資料移轉作業

如要讓 BigQuery 隨時掌握資料來源的最新行銷資料，請使用 BigQuery 資料移轉服務設定週期性資料移轉，以便按照排程擷取及載入資料。

在本教學課程中，您會使用 Google Ads 做為範例資料來源。
如需 BigQuery 資料移轉服務支援的資料來源完整清單，請參閱[支援的資料來源](https://docs.cloud.google.com/bigquery/docs/dts-introduction?hl=zh-tw#supported_data_sources)。

1. 前往 Google Cloud 控制台的「資料移轉」頁面。

   [前往「資料轉移」頁面](https://console.cloud.google.com/bigquery/transfers?hl=zh-tw)
2. 按一下 add「建立轉移作業」。
3. 在「Source type」(來源類型) 區段中，針對「Source」(來源)，選擇 [Google Ads]。
4. 在「Data source details」(資料來源詳細資料) 區段：

   1. 在「Customer ID」(客戶 ID) 中，輸入您的 Google Ads 客戶 ID。
   2. 在「報表類型」選取「標準」。標準報表包含一組標準報表和欄位，詳情請參閱 [Google Ads 報表轉換](https://docs.cloud.google.com/bigquery/docs/google-ads-transformation?hl=zh-tw)。
      * 在「Refresh window」(重新整理時間範圍) 中輸入 `5`。
5. 在「Destination settings」(目的地設定) 部分，「Dataset」(資料集) 請選取您為了儲存資料而建立的資料集。
6. 在「Transfer config name」(轉移設定名稱) 部分，針對「Display name」(顯示名稱) 輸入 `Marketing tutorial`。
7. 在「Schedule options」(排程選項) 專區：

   * 在「重複頻率」部分選取「天」。
   * 在「At」(在) 中輸入 `08:00`。
8. 按一下 [儲存]。

儲存設定後，BigQuery 資料移轉服務就會開始移轉資料。根據轉移設定中的設定，資料轉移作業每天會在世界標準時間上午 8 點執行一次，並從 Google Ads 擷取過去五天的資料。

您可以[監控進行中的移轉作業](https://docs.cloud.google.com/bigquery/docs/dts-monitor?hl=zh-tw)，查看每項資料移轉的狀態。

## 查詢資料表資料

資料移轉至 BigQuery 時，系統會將資料寫入擷取時間分區資料表。詳情請參閱[分區資料表簡介](https://docs.cloud.google.com/bigquery/docs/partitioned-tables?hl=zh-tw)一文。

如果您要直接查詢資料表，而不要使用自動產生的檢視表，您必須在查詢中使用 `_PARTITIONTIME` 虛擬資料欄。詳情請參閱[查詢分區資料表](https://docs.cloud.google.com/bigquery/docs/querying-partitioned-tables?hl=zh-tw)一文。

以下各節顯示可用來檢查已移轉資料的查詢範例。

### 廣告活動成效

下列查詢範例分析了最近 30 天的 Google Ads 廣告活動成效。

### 控制台

```
SELECT
  c.customer_id,
  c.campaign_name,
  c.campaign_status,
  SUM(cs.metrics_impressions) AS Impressions,
  SUM(cs.metrics_interactions) AS Interactions,
  (SUM(cs.metrics_cost_micros) / 1000000) AS Cost
FROM
  `DATASET.ads_Campaign_CUSTOMER_ID` c
LEFT JOIN
  `DATASET.ads_CampaignBasicStats_CUSTOMER_ID` cs
ON
  (c.campaign_id = cs.campaign_id
  AND cs._DATA_DATE BETWEEN
  DATE_ADD(CURRENT_DATE(), INTERVAL -31 DAY) AND DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY))
WHERE
  c._DATA_DATE = c._LATEST_DATE
GROUP BY
  1, 2, 3
ORDER BY
  Impressions DESC
```

### bq

```
  bq query --use_legacy_sql=false '
  SELECT
    c.customer_id,
    c.campaign_name,
    c.campaign_status,
    SUM(cs.metrics_impressions) AS Impressions,
    SUM(cs.metrics_interactions) AS Interactions,
    (SUM(cs.metrics_cost_micros) / 1000000) AS Cost
  FROM
    `DATASET.ads_Campaign_CUSTOMER_ID` c
  LEFT JOIN
    `DATASET.ads_CampaignBasicStats_CUSTOMER_ID` cs
  ON
    (c.campaign_id = cs.campaign_id
    AND cs._DATA_DATE BETWEEN
    DATE_ADD(CURRENT_DATE(), INTERVAL -31 DAY) AND DATE_ADD(CURRENT_DATE(), INTERVAL -1 DAY))
  WHERE
    c._DATA_DATE = c._LATEST_DATE
  GROUP BY
    1, 2, 3
  ORDER BY
    Impressions DESC'
```

更改下列內容：

* `DATASET`：您建立的資料集名稱，用於儲存轉移的資料表
* `CUSTOMER_ID`：您的 Google Ads 客戶 ID。

### 關鍵字數量

下列查詢範例分析了關鍵字 (依廣告活動、廣告群組和關鍵字狀態)。這項查詢使用 `KeywordMatchType` 函式。關鍵字比對類型可用來控制能帶出廣告的搜尋查詢。如要進一步瞭解關鍵字比對選項，請參閱「[關於關鍵字比對選項](https://support.google.com/google-ads/answer/2497836?hl=zh-tw)」一文。

### 控制台

```
  SELECT
    c.campaign_status AS CampaignStatus,
    a.ad_group_status AS AdGroupStatus,
    k.ad_group_criterion_status AS KeywordStatus,
    k.ad_group_criterion_keyword_match_type AS KeywordMatchType,
    COUNT(*) AS count
  FROM
    `DATASET.ads_Keyword_CUSTOMER_ID` k
    JOIN
    `DATASET.ads_Campaign_CUSTOMER_ID` c
  ON
    (k.campaign_id = c.campaign_id AND k._DATA_DATE = c._DATA_DATE)
  JOIN
    `DATASET.ads_AdGroup_CUSTOMER_ID` a
  ON
    (k.ad_group_id = a.ad_group_id AND k._DATA_DATE = a._DATA_DATE)
  WHERE
    k._DATA_DATE = k._LATEST_DATE
  GROUP BY
    1, 2, 3, 4
```

### bq

```
  bq query --use_legacy_sql=false '
  SELECT
    c.campaign_status AS CampaignStatus,
    a.ad_group_status AS AdGroupStatus,
    k.ad_group_criterion_status AS KeywordStatus,
    k.ad_group_criterion_keyword_match_type AS KeywordMatchType,
    COUNT(*) AS count
  FROM
    `DATASET.ads_Keyword_CUSTOMER_ID` k
  JOIN
    `DATASET.ads_Campaign_CUSTOMER_ID` c
  ON
    (k.campaign_id = c.campaign_id AND k._DATA_DATE = c._DATA_DATE)
  JOIN
    `DATASET.ads_AdGroup_CUSTOMER_ID` a
  ON
    (k.ad_group_id = a.ad_group_id AND k._DATA_DATE = a._DATA_DATE)
  WHERE
    k._DATA_DATE = k._LATEST_DATE
  GROUP BY
    1, 2, 3, 4'
```

更改下列內容：

* `DATASET`：您建立的資料集名稱，用於儲存轉移的資料表
* `CUSTOMER_ID`：您的 Google Ads 客戶 ID。

## 建立 Dataform 存放區

建立資料移轉設定，從 Google Ads 移轉最新資料後，請設定 Dataform 定期轉換行銷分析資料。您可以使用 Dataform 安排定期資料轉換作業，並與其他資料分析師協作，使用 SQL 定義這些轉換作業。

建立 Dataform 存放區，以便儲存構成轉換程式碼的 [SQLX 查詢](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw#dataform-core)。

1. 前往 Google Cloud 控制台的「Dataform」頁面。

   [前往 Dataform](https://console.cloud.google.com/bigquery/dataform?hl=zh-tw)
2. 按一下 add「建立存放區」。
3. 在「建立存放區」頁面中執行下列操作：

   1. 在「Repository ID」(存放區 ID) 欄位中輸入 `marketing-tutorial-repository`。
   2. 在「Region」(區域) 清單中選取區域。
   3. 點選「建立」。

`marketing-tutorial-repository` 存放區現在會顯示在 Dataform 存放區清單中。

如要進一步瞭解 Dataform 存放區，請參閱「[關於 Dataform 存放區](https://docs.cloud.google.com/dataform/docs/create-repository?hl=zh-tw#about-repositories)」。

## 建立並初始化 Dataform 開發工作區

建立 Dataform 開發工作區，以便在存放區中處理轉換程式碼，然後再將變更提交並推送至存放區。

1. 前往 Google Cloud 控制台的「Dataform」頁面。

   [前往 Dataform](https://console.cloud.google.com/bigquery/dataform?hl=zh-tw)
2. 按一下「`marketing-tutorial-repository`」。
3. 按一下「建立開發工作區」add。
4. 在「建立開發工作區」視窗中執行下列操作：

   1. 在「Workspace ID」(工作區 ID) 欄位中輸入 `marketing-tutorial-workspace`。
   2. 點選「建立」。

   系統隨即會顯示開發工作區頁面。
5. 按一下「Initialize workspace」(初始化工作區)。

`marketing-tutorial-workspace`開發工作區現在會顯示在 `marketing-tutorial-repository` 存放區的「開發工作區」分頁中，以及 `definitions` 目錄中的兩個範例檔案，分別名為 `*first_view.sqlx` 和 `*second_view.sqlx`。

如要進一步瞭解 Dataform 開發工作區，請參閱[開發工作區總覽](https://docs.cloud.google.com/dataform/docs/create-workspace?hl=zh-tw#overview-workspaces)。

## 將 Google Ads 表格宣告為表格來源

按照下列步驟，將新轉移的 Google Ads 資料表宣告為資料來源，並連結至 Dataform：

### 建立 SQLX 檔案以用於資料來源宣告

在 Dataform 中，您可以在 `definitions/` 目錄中建立 SQLX 檔案，宣告資料來源目的地：

1. 前往 Google Cloud 控制台的「Dataform」頁面。

   [前往「Dataform」頁面](https://console.cloud.google.com/bigquery/dataform?hl=zh-tw)
2. 選取「`marketing-tutorial-repository`」。
3. 選取「`marketing-tutorial-workspace`」。
4. 在「Files」(檔案) 窗格中，點按 `definitions/` 旁的「更多」選單。
5. 點選「建立檔案」。
6. 在「建立新檔案」窗格中，執行下列步驟：

   1. 在「Add a file path」(新增檔案路徑) 欄位中，輸入 `definitions/` 後，輸入名稱 `definitions/googleads-declaration.sqlx`。
   2. 點選「建立檔案」。

### 宣告資料來源

編輯 `definitions/googleads-declaration.sqlx`，將已轉移的 Google Ads 資料表宣告為資料來源。這個範例會將 `ads_Campaign` 資料表宣告為資料來源：

1. 在開發工作區的「Files」(檔案) 窗格中，按一下 SQLX 檔案，宣告資料來源。
2. 在檔案中輸入下列程式碼片段：

   ```
       config {
           type: "declaration",
           database: "PROJECT_ID",
           schema: "DATASET",
           name: "ads_Campaign_CUSTOMER_ID",
       }
   ```

## 定義轉換

在 `definitions/` 目錄中建立 SQLX 檔案，定義資料轉換。在本教學課程中，您將建立每日轉換，使用名為 `daily_performance.sqlx` 的檔案匯總點擊次數、曝光次數、費用和轉換次數等指標。

### 建立轉換 SQLX 檔案

1. 在「檔案」窗格中，點按 `definitions/` 旁的 more\_vert「更多」選單，然後選取「建立檔案」。
2. 在「Add a file path」(新增檔案路徑) 欄位中，輸入 `definitions/daily_performance.sqlx`。
3. 點選「建立檔案」。

### 定義轉換 SQLX 檔案

1. 在「檔案」窗格中，展開 `definitions/` 目錄。
2. 選取 `daily_performance.sqlx`，然後輸入下列查詢：

   ```
       config {
           type: "table",
           schema: "reporting",
           tags: ["daily", "google_ads"]
       }
       SELECT
           date,
           campaign_id,
           campaign_name,
       SUM(clicks) AS total_clicks
       FROM
           `ads_Campaign_CUSTOMER_ID`
       GROUP BY
           date,
           campaign_id,
           campaign_name
           ORDER BY
           date DESC
   ```

## 修訂並推送變更

在開發工作區中完成變更後，請按照下列步驟將變更提交並推送至存放區：

1. 在 `marketing-tutorial-workspace` 工作區中，按一下「提交 1 項變更」。
2. 在「New commit」(新增提交) 窗格中，於「Add a commit message」(新增提交訊息) 欄位輸入提交說明。
3. 按一下「Commit all changes」(提交所有變更)。
4. 在 `marketing-tutorial-workspace` 工作區中，按一下「Push to default branch」(推送至預設分支)。

變更成功推送至存放區後，系統會顯示「工作區已是最新版本」訊息。

## 排定資料轉換時間

定義資料轉換檔案後，請排定資料轉換時間。

### 建立正式版

在 Dataform 中發布正式版，可確保環境持續更新資料轉換結果。下列步驟說明如何指定 `marketing-tutorial-repository` 存放區的 `main` 分支，以儲存資料轉換：

1. 前往 Google Cloud 控制台的「Dataform」頁面。

   [前往「Dataform」頁面](https://console.cloud.google.com/bigquery/dataform?hl=zh-tw)
2. 選取「`marketing-tutorial-repository`」。
3. 按一下「發布與排程」分頁標籤。
4. 按一下「建立正式版」。
5. 在「Create release configuration」(建立版本設定) 窗格中，進行下列設定：

   1. 在「Release ID」(發布版本 ID) 欄位中輸入 `transformations`。
   2. 保留「Git commitish」(Git 修訂版本) 欄位的預設值 `main`。
   3. 在「排程頻率」部分，選取「隨選」。
6. 點選「建立」。

### 建立工作流程設定

建立正式版後，您就可以建立工作流程設定，在存放區中依指定時間表執行資料轉換。下列步驟說明如何從 `transformations` 檔案排定每日轉換作業：

1. 前往 Google Cloud 控制台的「Dataform」頁面。

   [前往「Dataform」頁面](https://console.cloud.google.com/bigquery/dataform?hl=zh-tw)
2. 選取「`marketing-tutorial-repository`」。
3. 按一下「發布與排程」分頁標籤。
4. 在「工作流程設定」部分，按一下「建立」。
5. 在「Create workflow configuration」(建立工作流程設定) 窗格的「Configuration ID」(設定 ID) 欄位中輸入 `transformations`。
6. 在「Release configuration」(版本設定) 選單中，選取 `transformations`。
7. 在「驗證」下方，選取「以使用者憑證執行」
8. 在「排程頻率」部分，執行下列操作：

   ```
   1. Select **Repeat**.
   1. For **Repeats**, select `Daily`.
   1. For **At time**, enter `10:00 AM`.
   1. For **Timezone**, select `Coordinated Universal Time (UTC)`.
   ```
9. 按一下「選取代碼」。
10. 在「選取要執行的標記」欄位中，選取「每日」。
11. 點選「建立」。

您建立的工作流程設定會執行 `transformations` 版本設定建立的所有最新編譯結果。

## 清除所用資源

為避免系統向您的 Google Cloud 帳戶收取本頁面所用資源的費用，請按照下列步驟操作。

### 刪除在 BigQuery 中建立的資料集

如要避免系統依 BigQuery 資產收取費用，請刪除名為 `dataform` 的資料集。

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在「Explorer」面板中展開專案，然後選取 `dataform`。
3. 按一下 more\_vert「Actions」(動作) 選單，然後選取「Delete」(刪除)。
4. 在「Delete dataset」(刪除資料集) 對話方塊中，在欄位輸入 `delete`，然後按一下「Delete」(刪除)。

### 刪除 Dataform 開發工作區和設定

建立 Dataform 開發工作區不會產生任何費用，但如要刪除開發工作區，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Dataform」頁面。

   [前往 Dataform](https://console.cloud.google.com/bigquery/dataform?hl=zh-tw)
2. 按一下「`quickstart-repository`」。
3. 按一下「發布與排程」分頁標籤。
4. 在「發布設定」部分下方，點選設定旁邊的「更多」more\_vert`production`選單，然後點選「刪除」。
5. 在「Workflow configurations」(工作流程設定) 區段下方，按一下 `transformations` 設定旁的 more\_vert「More」(更多) 選單，然後按一下「Delete」(刪除)。
6. 在「Development workspaces」(開發工作區) 分頁，按一下 `quickstart-workspace` 旁的 more\_vert「More」(更多) 選單，然後選取「Delete」(刪除)。
7. 按一下「Delete」(刪除) 確認操作。

### 刪除 Dataform 存放區

建立 Dataform 存放區不會產生任何費用，但如要刪除存放區，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Dataform」頁面。

   [前往 Dataform](https://console.cloud.google.com/bigquery/dataform?hl=zh-tw)
2. 在 `quickstart-repository` 旁邊，按一下 more\_vert「More」(更多) 選單，然後選取「Delete」(刪除)。
3. 在「Delete repository」(刪除存放區) 視窗中，輸入存放區名稱來確認刪除。
4. 按一下「Delete」(刪除) 確認操作。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]