* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排定資料準備作業

本文說明如何排定資料準備管道的執行時間，以及如何手動執行管道。

資料準備作業由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 支援。
系統會使用 Google 帳戶使用者憑證或您在設定時間表或執行測試時選取的[自訂服務帳戶](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#about-service-accounts)，執行各項資料準備時間表。

您對資料準備步驟所做的變更不會自動儲存。您必須先儲存並部署變更，才能透過排程執行變更。排程一律會執行最新部署的資料準備作業版本，並排除您可能正在開發的任何未部署變更。

## 事前準備

開始之前，請先[建立資料準備](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw)。

### 必要的角色

如要使用服務帳戶授權資料準備作業，請[手動在開發環境中執行資料準備作業](#run-undeployed-manually)，或[排定資料準備作業的執行時間](#create-schedule)，並授予服務帳戶角色，以便執行資料準備作業。詳情請參閱「[授予 Dataform 服務帳戶存取權](https://docs.cloud.google.com/bigquery/docs/manage-data-preparations?hl=zh-tw#dataform-service-account-iam)」。

如要排定資料準備作業，請按照下列步驟操作：

* 請管理員授予您自訂服務帳戶的[服務帳戶使用者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)。
* 將[服務帳戶使用者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`) 和[服務帳戶權杖建立者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountTokenCreator) (`roles/iam.serviceAccountTokenCreator`) 授予自訂服務帳戶的預設 Dataform 服務代理。

如要提升排程安全性，請參閱「[實作進階排程權限](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#enhanced-scheduling-permissions)」。

## 開發資料準備作業

開發資料準備作業時，您可以手動執行步驟並檢查輸出內容，然後再將變更部署至實際工作環境。您可以根據[排程](#create-schedule)，在資料上測試目前開發的版本，同時讓 BigQuery 繼續執行最新部署的版本。執行作業前，請務必[設定目的地](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#add-or-change-destination)，並修正所有驗證錯誤。

### 在開發環境中手動執行資料準備作業

如要測試資料準備步驟，並驗證目的地表格中的結果，請從資料準備編輯器手動執行資料準備作業：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「資料準備」。
4. 按一下要執行的資料準備作業名稱。
5. 在資料準備編輯器工具列中，依序點選「更多」**>「設定『立即執行』體驗」**。
6. 在「驗證」部分，使用 Google 帳戶使用者憑證或服務帳戶授權資料準備作業。

   * 如要使用 Google 帳戶使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。這是預設選項。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。如果服務帳戶需要其他權限，請按一下「全部授予」，將必要角色授予該帳戶。**注意：** 如果資料準備作業使用 Google 雲端硬碟做為資料來源，您必須選取「使用所選服務帳戶執行」。這項作業不支援使用者的憑證。您也必須與服務帳戶共用 Google 雲端硬碟檔案。
7. 按一下 [儲存]。
8. 修正顯示的所有驗證錯誤。
9. 在資料準備編輯器工具列中，按一下「執行」。
10. 在「立即執行」對話方塊中，按一下「確認」，確認這項手動執行作業會將資料寫入目的地資料表，而您可能也會使用該資料表執行排程作業。

    如果選取「使用我的使用者憑證執行」做為驗證方法，您必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

    接著，執行作業會執行步驟，並將輸出內容載入目的地。
11. 選用步驟：執行完成後，您可以在「Executions」(執行作業) 窗格中查看執行詳細資料。

## 部署資料準備作業

如要為資料準備作業版本排定執行時間，請先部署該版本。時間表會執行最近部署的版本。

如要部署資料準備作業，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「資料準備」。
4. 按一下所選資料準備作業的名稱。

   資料準備編輯器隨即開啟。
5. 在資料準備編輯器工具列中，按一下「部署」。

## 建立排程

**提示：** 您也可以使用「管道和連線」頁面，透過[簡化、專為 BigQuery 設計的工作流程](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw)，排定資料準備作業。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要建立排程，執行已部署的資料準備步驟，並將準備好的資料載入目的地資料表，請先排定資料準備作業執行時間。如要排定執行時間，請[設定目的地](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw#add-or-change-destination)，並修正所有驗證錯誤。

如要建立資料準備時間表，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「資料準備」。
4. 按一下要排程的資料準備作業名稱。
5. 在資料準備編輯器工具列中，按一下「排定時間」。
6. 輸入排程名稱。
7. 在「驗證」部分，使用 Google 帳戶使用者憑證或服務帳戶授權資料準備作業。

   * 如要使用 Google 帳戶使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。**注意：** 如果資料準備作業使用 Google 雲端硬碟做為資料來源，您必須選取「使用所選服務帳戶執行」。這項作業不支援使用者的憑證。您也必須與服務帳戶共用 Google 雲端硬碟檔案。
8. 排定頻率。
9. 按一下「建立時間表」。如果選取「使用我的使用者憑證執行」做為驗證方法，您必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下「建立」，然後從選單中選取「資料準備排程」。
3. 在「Schedule data preparation」(排定資料準備作業) 窗格的「Data preparation」(資料準備) 欄位中，選取要排定的資料準備作業。
4. 在「排程名稱」欄位中，輸入排程名稱。
5. 在「驗證」部分，使用 Google 帳戶使用者憑證或服務帳戶授權資料準備作業。

   * 如要使用 Google 帳戶使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。**注意：** 如果資料準備作業使用 Google 雲端硬碟做為資料來源，您必須選取「使用所選服務帳戶執行」。這項作業不支援使用者的憑證。您也必須與服務帳戶共用 Google 雲端硬碟檔案。
6. 在「排程頻率」部分，執行下列操作：

   1. 在「重複頻率」選單中，選取資料準備作業的執行頻率。
   2. 在「At time」(時間) 欄位中，輸入排定資料準備作業執行的時間。
   3. 在「時區」選單中，選取時間表的時區。
7. 按一下「建立時間表」。如果選取「使用我的使用者憑證執行」做為驗證方法，您必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

## 授權給您的 Google 帳戶

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [dataform-preview-support@google.com](mailto:dataform-preview-support@google.com)。

如要使用[Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)使用者憑證驗證資源，您必須手動授予 BigQuery 管道權限，讓管道取得 Google 帳戶的存取權杖，並代表您存取來源資料。您可以使用 OAuth 對話方塊介面手動授予核准。

**注意：** 使用 Google 帳戶的使用者憑證執行或排定 BigQuery 管道時，系統不支援情境感知存取權 (CAA) 政策，包括以 IP 為準、以地理位置為準，以及裝置合規政策，因為權杖要求來自 Google 基礎架構。除非[豁免 Dataform OAuth 用戶端 ID 遵守政策](https://docs.cloud.google.com/dataform/docs/troubleshooting?hl=zh-tw#euc-permission-denied)，否則 CAA 政策會禁止執行這些作業。

您只需要授予 BigQuery 管道一次權限。

如要撤銷授予的權限，請按照下列步驟操作：

1. 前往 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)。
2. 按一下「BigQuery Pipelines」。
3. 按一下 [移除存取權]。

**警告：** 撤銷存取權後，這個 Google 帳戶在所有區域擁有的管道日後都無法執行。

如果新的 Google 帳戶擁有者從未建立時間表，更新憑證來變更資料準備時間表擁有者時，也需要手動核准。

## 手動執行排定的資料準備作業

在選取的排程中手動執行資料準備作業時，BigQuery 會獨立於排程執行一次資料準備作業。

如要手動執行排定的資料準備作業，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選資料準備作業排程的名稱。
3. 在「排程詳細資料」頁面中，按一下「執行」。

## 查看時間表

您可以透過資料準備編輯器或「排程」頁面查看資料準備排程。

### 資料準備編輯器

如要查看資料準備作業的排程，請按照下列步驟操作：

1. 在資料準備編輯器工具列中，依序點選「排程」「查看排程」。
2. 選用：如要查看排程記錄，請按一下「查看過去的執行作業」。

### 「排定時間」頁面

如要查看專案中的所有資料準備排程，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 選用：如要查看所選時間表的執行記錄和詳細資料，請按一下時間表的名稱。系統不會顯示手動執行的記錄。

## 編輯時間表

您可以在資料準備編輯器或「排程」頁面中編輯排程。

### 資料準備編輯器

如要編輯時間表，請按照下列步驟操作：

1. 在資料準備編輯器工具列中，依序點選「排程」「查看排程」。
2. 在「排定資料準備作業」對話方塊中，按一下「編輯」，然後更新排程。
3. 按一下「更新時間表」。

### 「排定時間」頁面

如要編輯時間表，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選資料準備作業排程的名稱。
3. 在「排程詳細資料」頁面中，按一下「編輯」。
4. 按一下「查看時間表」。
5. 在「排定資料準備作業」對話方塊中，按一下「編輯」，然後更新排程。
6. 按一下「更新時間表」。

## 刪除時間表

如要永久刪除所選資料準備作業的排程，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 在包含時間表的資料列中，依序點選 more\_vert「動作」**> 刪除**。

## 後續步驟

* 瞭解如何[建立資料準備作業](https://docs.cloud.google.com/bigquery/docs/data-prep-get-suggestions?hl=zh-tw)。
* 進一步瞭解如何[管理資料準備作業](https://docs.cloud.google.com/bigquery/docs/manage-data-preparations?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-04 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-04 (世界標準時間)。"],[],[]]