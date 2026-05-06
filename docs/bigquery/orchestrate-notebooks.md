Google uses AI technology to translate content into your preferred language. AI translations can contain errors.

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排定筆記本

本文說明如何[在 BigQuery 中排定 Colab Enterprise 筆記本的執行時間](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)，以及檢查排定的筆記本執行作業。

筆記本是由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 支援的程式碼資產。
不過，筆記本不會顯示在 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 中。

您可以排定筆記本的自動執行時間和頻率，例如訓練機器學習模型、呼叫外部 API 或執行 BigQuery DataFrames 程式碼。

系統會自動儲存您對筆記本所做的變更，但只有您和[有權存取筆記本](https://docs.cloud.google.com/bigquery/docs/manage-notebooks?hl=zh-tw#grant_access_to_notebooks)的使用者可以查看。如要使用新版筆記本更新排程，請[部署筆記本](#deploy)。部署筆記本時，系統會使用目前版本的筆記本更新排程。排程會執行最新部署的筆記本版本。

系統會使用 Google 帳戶使用者憑證或您在設定排程時選取的[自訂服務帳戶](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#about-service-accounts)，執行每個筆記本排程。

Dataform 會將排定執行的筆記本輸出內容，寫入排程建立期間選取的 [Cloud Storage 值區](https://docs.cloud.google.com/storage/docs/buckets?hl=zh-tw)。

筆記本排程使用[標準 E2 執行階段](https://docs.cloud.google.com/colab/docs/runtimes?hl=zh-tw)。
系統會收取 Colab Enterprise 執行階段費用。系統會根據 E2 機型，收取執行階段處理費用。如要瞭解標準 E2 執行階段的定價，請參閱 [Colab Enterprise 定價](https://cloud.google.com/colab/pricing?hl=zh-tw)。

## 事前準備

開始之前，請先[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。

### 啟用筆記本排程

如要安排筆記本的執行時間，請務必將下列角色授予您打算用於筆記本排程的自訂服務帳戶：

[筆記本執行程式使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.notebookExecutorUser) (`roles/aiplatform.notebookExecutorUser`)
:   按照「[授予專案的單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)」一文的說明，在所選專案中，將 Notebook Executor User 角色授予服務帳戶。

[儲存空間管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin) (`roles/storage.admin`)
:   按照「[在 Cloud Storage bucket 層級政策中新增主體](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add)」一文的說明，將服務帳戶新增為 Cloud Storage bucket 的主體，並授予該主體 Storage 管理員角色。您打算使用這個 Cloud Storage bucket 儲存排定執行的筆記本輸出內容。

[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)
:   按照「[為服務帳戶授予單一角色](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw#grant-single-role)」一文中的步驟，將服務帳戶新增為自己的主體。換句話說，請將服務帳戶新增為相同服務帳戶的主體。然後將服務帳戶使用者角色授予這個主體。

此外，您必須將下列角色授予預設的 Dataform 服務代理：

[服務帳戶權杖建立者](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#token-creator-role) (`roles/iam.serviceAccountTokenCreator`)
:   按照「[授予自訂 Dataform 服務帳戶權杖建立存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-token-creation-access)」一文的說明，將預設 Dataform 服務代理程式新增為服務帳戶的主體，並將「服務帳戶權杖建立者」角色授予這個主體。

[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)
:   按照[使用 Google Cloud 控制台授予或撤銷多個 IAM 角色](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw#multiple-roles-console)的步驟，在自訂服務帳戶中，將服務帳戶使用者角色授予預設的 Dataform 服務代理程式。

如要進一步瞭解 Dataform 中的服務帳戶，請參閱「[關於 Dataform 中的服務帳戶](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#about-service-accounts)」。

### 必要的角色

如要建立筆記本排程，您需要下列角色：

* [Dataform 管理員](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.admin) (`roles/dataform.admin`)
* [BigQuery 讀取工作階段使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.readSessionUser) (`roles/bigquery.readSessionUser`)
  或
  [BigQuery Studio 使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.studioUser) (`roles/bigquery.studioUser`)
* [筆記本執行階段使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.notebookRuntimeUser) (`roles/aiplatform.notebookRuntimeUser`)
* 自訂服務帳戶的[服務帳戶使用者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)

如要在排定筆記本執行時間時使用筆記本執行階段範本，您需要具備「筆記本執行階段使用者」([`roles/aiplatform.notebookRuntimeUser`](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.notebookRuntimeUser)) 角色。

如要編輯及刪除筆記本排程，您必須具備[Dataform 編輯者 (`roles/dataform.editor`)](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.editor) 角色。

如要查看筆記本排程，您需要「Dataform 檢視者」([`roles/dataform.viewer`](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#dataform.viewer)) 角色。

如要提升排程安全性，請參閱「[實作進階排程權限](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#enhanced-scheduling-permissions)」。

如要進一步瞭解 BigQuery IAM，請參閱「[BigQuery IAM 角色和權限](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw)」。

如要進一步瞭解 Dataform IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw)」。

## 建立排程

**提示：** 您也可以使用「管道和連線」頁面，透過[簡化且專為 BigQuery 設計的工作流程](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw)，建立筆記本排程。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要建立筆記本排程，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下要排程的筆記本名稱。你可以使用搜尋功能或篩選器尋找筆記本。
5. 在「Notebook」(筆記本) 工具列中，按一下「Schedule」(排程)。

   或者，按一下 calendar\_month「時間表」，然後按一下「建立時間表」。
6. 在「排程筆記本」窗格的「排程名稱」欄位中，輸入排程名稱。
7. 在「驗證」部分，使用 Google 帳戶使用者憑證或服務帳戶授權筆記本。

   * 如要使用 Google 帳戶使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。
8. 在「筆記本選項」區段的「執行階段範本」欄位中，選取 Colab 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。

   **注意：**筆記本執行階段範本必須與筆記本位於同一個區域。**注意：**如果沒有使用筆記本執行階段範本的[必要角色](#required_permissions)，您仍可使用預設執行階段規格執行及排定筆記本。
9. 在「Cloud Storage bucket」欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket。

   所選服務帳戶必須獲得所選值區的「Storage 管理員 (`roles/storage.admin`)」IAM 角色。詳情請參閱「[啟用筆記本排程](#enable-scheduling)」。
10. 在「排程頻率」部分，執行下列操作：

    1. 在「重複」選單中，選取排定筆記本執行的頻率。
    2. 在「At time」(時間) 欄位中，輸入排定筆記本執行的時間。
    3. 在「時區」選單中，選取時間表的時區。
11. 按一下「建立時間表」。如果選取「使用我的使用者憑證執行」做為驗證方法，您必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

建立排程時，系統會自動部署目前版本的筆記本。如要使用新版筆記本更新時間表，請[部署筆記本](#deploy)。

筆記本的最新部署版本會按照所選時間和頻率執行。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下「建立」，然後從選單中選取「筆記本時間表」。
3. 在「排定筆記本時間」窗格的「筆記本」欄位中，選取要排程的筆記本。
4. 在「排程名稱」欄位中，輸入排程名稱。
5. 在「驗證」部分，使用 Google 帳戶使用者憑證或服務帳戶授權筆記本。

   * 如要使用 Google 帳戶使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。
6. 在「筆記本選項」部分，於「執行階段範本」欄位中，選取 Colab 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。

   **注意：**筆記本執行階段範本必須與筆記本位於同一個區域。**注意：**如果沒有使用筆記本執行階段範本的[必要角色](#required_permissions)，您仍可使用預設執行階段規格執行及排定筆記本。
7. 在「Cloud Storage bucket」欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket。

   所選服務帳戶必須獲得所選值區的「Storage 管理員 (`roles/storage.admin`)」IAM 角色。詳情請參閱「[啟用筆記本排程](#enable-scheduling)」。
8. 在「排程頻率」部分，執行下列操作：

   1. 在「重複」選單中，選取排定筆記本執行的頻率。
   2. 在「At time」(時間) 欄位中，輸入排定筆記本執行的時間。
   3. 在「時區」選單中，選取時間表的時區。
9. 按一下「建立時間表」。如果選取「使用我的使用者憑證執行」做為驗證方法，您必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

建立排程時，系統會自動部署目前版本的筆記本。如要使用新版筆記本更新時間表，請[部署筆記本](#deploy)。

筆記本的最新部署版本會按照所選時間和頻率執行。

### 授權給您的 Google 帳戶

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

如果新的 Google 帳戶擁有者從未建立過時間表，更新憑證以變更筆記本時間表擁有者時，也需要手動核准。

## 部署筆記本

部署筆記本時，系統會使用目前版本的筆記本更新排程。排程會執行最新部署的筆記本版本。

如果這個筆記本有排程，當您編輯筆記本時，BigQuery 會提示您部署變更，以更新排程。

如要部署筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下所選筆記本的名稱。
5. 點選「Deploy」(部署)。

系統會使用目前版本的筆記本更新對應的排程。系統會在排定的時間執行最新部署的筆記本版本。

## 手動執行已部署的筆記本

如果您手動執行已部署的筆記本，BigQuery 會執行一次，與排程無關。

如要手動執行已部署的筆記本，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選筆記本排程的名稱。
3. 在「排程詳細資料」頁面中，按一下「執行」。

## 查看所有時間表

如要查看專案中的所有筆記本排程，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 選用：如要顯示其他資料欄的筆記本時間表詳細資料，請按一下「資料欄顯示選項」view\_column，然後選取資料欄並按一下「確定」。

## 查看排程詳細資料

您可以在「Explorer」窗格或「Scheduling」頁面中，查看所選排程的詳細資料。

如要查看所選筆記本的排程詳細資料，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」**BigQuery**頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下所選筆記本的名稱。
5. 在「Notebook」(筆記本) 工具列中，按一下「Schedule」(排程)。

   或者，按一下「時間表」calendar\_month：

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選筆記本排程的名稱。

## 查看過往執行作業

您可以在「Explorer」(探索) 窗格或「Scheduling」(排程) 頁面中，查看所選筆記本排程的過往執行作業。

如要查看所選筆記本排程的過往執行作業，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下所選筆記本的名稱。
5. 按一下「排程」，然後按一下「查看過去的執行作業」。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選筆記本排程的名稱。
3. 在「排程詳細資料」頁面的「過去的執行作業」部分，檢查過去的執行作業。
4. 選用：如要重新整理過往執行作業的清單，請按一下「重新整理」。

## 停用時間表

如要暫停所選筆記本的排定執行作業，但不想刪除排程，可以停用排程。

如要停用所選筆記本的排程，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下所選筆記本的名稱。
5. 在「Notebook」(筆記本) 工具列中，按一下「Schedule」(排程)。

   或者，按一下「時間表」calendar\_month：
6. 在排程詳細資料表格的「排程狀態」列中，按一下「已啟用排程」切換鈕。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選筆記本的名稱。
3. 在「排程詳細資料」頁面中，按一下「停用」。

## 啟用時間表

如要恢復已停用筆記本排程的排定執行作業，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下所選筆記本的名稱。
5. 在「Notebook」(筆記本) 工具列中，按一下「Schedule」(排程)。

   或者，按一下 calendar\_month「時間表」。
6. 在排程詳細資料表格的「排程狀態」列中，按一下「排程已停用」切換鈕。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選筆記本的名稱。
3. 在「時間表詳細資料」頁面中，按一下「啟用」。

## 編輯時間表

您可以在「Explorer」窗格或「Scheduling」頁面中編輯排程。

如要編輯時間表，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，然後按一下「Notebooks」。
4. 按一下所選筆記本的名稱。
5. 按一下「排程」，然後按一下「編輯」。
6. 在「排程詳細資料」對話方塊中編輯排程，然後按一下「更新排程」。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選筆記本排程的名稱。
3. 在「排程詳細資料」頁面中，按一下「編輯」。
4. 按一下「查看時間表」，然後按一下「編輯」。
5. 在「排定筆記本時間」對話方塊中編輯時間表，然後按一下「更新時間表」。

## 刪除時間表

如要永久刪除所選筆記本的排程，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 執行下列其中一項操作：

   * 按一下所選時間表的名稱，然後在「時間表詳細資料」頁面中，按一下「刪除」。
   * 在包含所選時間表的資料列中，按一下「動作」欄中的「查看動作」more\_vert，然後按一下「刪除」。
3. 在隨即顯示的對話方塊中，按一下「刪除」。

## 後續步驟

* 進一步瞭解 [BigQuery 中的 Colab Enterprise 筆記本](https://docs.cloud.google.com/bigquery/docs/notebooks-introduction?hl=zh-tw)。
* 瞭解如何[建立筆記本](https://docs.cloud.google.com/bigquery/docs/create-notebooks?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-04 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-04 (世界標準時間)。"],[],[]]