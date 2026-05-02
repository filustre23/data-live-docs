* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排定管道

本文說明如何排定 [BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)的執行時間，包括如何排定管道執行時間，以及檢查排定的管道執行作業。

管道是由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 支援。
每個管道排程都會使用您的 Google 帳戶使用者憑證或[自訂服務帳戶](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#about-service-accounts)執行，您可以在設定排程時選取。

您對管道所做的變更會自動儲存，但只有您和專案中獲派 Dataform 管理員角色的使用者可以存取。如要使用新版管道更新排程，請[部署管道](#deploy)。
部署後，排程就會更新為使用目前版本的管道。排程一律會執行最新部署的版本。

含有筆記本的管道排程會使用[預設執行階段規格](https://docs.cloud.google.com/colab/docs/runtimes?hl=zh-tw#default_runtime_specifications)。在排定執行的管道中，如果包含筆記本，BigQuery 會將筆記本輸出內容寫入排程建立期間選取的 [Cloud Storage 值區](https://docs.cloud.google.com/storage/docs/buckets?hl=zh-tw)。

## 事前準備

請先[建立管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。

### 啟用管道排程

如要排定管道執行時間，請將下列角色授予您打算用於管道排程的自訂服務帳戶：

[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)
:   按照「[為服務帳戶授予單一角色](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw#grant-single-role)」一文中的步驟，將服務帳戶新增為自身的主體。換句話說，請將服務帳戶新增為相同服務帳戶的主體。然後將「服務帳戶使用者」角色授予這個主體。

如果管道包含 SQL 查詢，您必須將下列角色授予預計用於管道排程的服務帳戶：

[BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
:   按照「[在專案中授予單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)」一文的說明，在管道讀取資料的專案中，將 BigQuery 工作使用者角色授予服務帳戶。

[BigQuery 資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer) (`roles/bigquery.dataViewer`)
:   按照「[在專案中授予單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)」一文的說明，在管道讀取資料的專案中，將 BigQuery 資料檢視者角色授予服務帳戶。

[BigQuery 資料編輯者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor) (`roles/bigquery.dataEditor`)
:   按照「[在專案中授予單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)」一文的說明，在管道寫入資料的專案中，將 BigQuery 資料編輯者角色授予服務帳戶。

如果管道包含筆記本，您必須將下列角色授予計畫用於管道排程的服務帳戶：

[筆記本執行程式使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.notebookExecutorUser) (`roles/aiplatform.notebookExecutorUser`)
:   按照「[授予專案的單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)」一文的說明，在所選專案中，將 Notebook Executor User 角色授予服務帳戶。

[儲存空間管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin) (`roles/storage.admin`)
:   按照「[將主體新增至 bucket 層級政策](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add)」一文的說明，將服務帳戶新增為 Cloud Storage bucket 的主體，並授予該主體「Storage Admin」角色。您打算使用這個 bucket 儲存在排定時間執行的管線中，筆記本的輸出內容。

此外，您必須將下列角色授予預設的 Dataform 服務代理：

[服務帳戶憑證建立者](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#token-creator-role) (`roles/iam.serviceAccountTokenCreator`)
:   請按照「[授予服務帳戶憑證建立存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-token-creation-access)」一文的說明，將預設 Dataform 服務代理程式新增為服務帳戶的主體，並將「服務帳戶憑證建立者」角色授予這個主體。

[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)
:   按照[使用 Google Cloud 控制台授予或撤銷多個 IAM 角色](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw#multiple-roles-console)的步驟，將服務帳戶使用者角色授予自訂服務帳戶的預設 Dataform 服務代理程式。

如要進一步瞭解 Dataform 中的服務帳戶，請參閱「[關於 Dataform 中的服務帳戶](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#about-service-accounts)」。

### 必要的角色

如要取得管理管道所需的權限，請要求管理員授予您下列 IAM 角色：

* 刪除管道：
  [Dataform 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Admin)  (`roles/dataform.Admin`)
  在管道上
* 建立、編輯、執行及刪除管道排程：
  + [Dataform 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Admin)  (`roles/dataform.Admin`)
    管道
  + [服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser)  (`roles/iam.serviceAccountUser`)
    自訂服務帳戶
* 查看及執行管道：
  專案的 [Dataform 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Viewer)  (`roles/dataform.Viewer`)
* 查看管道排程：專案的 [Dataform 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.Editor)  (`roles/dataform.Editor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如要提升排程安全性，請參閱「[實作進階排程權限](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#enhanced-scheduling-permissions)」。

如要進一步瞭解 Dataform IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw)」。

如要在排定管道時使用 Colab 筆記本執行階段範本，您需要[筆記本執行階段使用者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.notebookRuntimeUser) (`roles/aiplatform.notebookRuntimeUser`)。

## 建立管道排程

**提示：** 您也可以使用「管道和連線」頁面，透過[簡化、BigQuery 專屬的工作流程](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw)，排定 Dataform 管道。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

如要建立管道排程，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下「展開左側窗格」圖示 last\_page 開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「Schedule」(排程)。
5. 在「排定管道」窗格的「排程名稱」欄位中，輸入排程名稱。
6. 在「Authentication」(驗證) 區段中，使用 Google 帳戶使用者憑證或服務帳戶授權管道。

   * 如要使用 Google 帳戶使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。
7. 如果管道包含筆記本，請在「筆記本選項」部分的「執行階段範本」欄位中，選取 Colaboratory 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。

   **注意：**筆記本執行階段範本必須與管道位於相同區域。**注意：**如果您沒有使用 Colab 筆記本執行階段範本的[必要角色](#required_roles)，仍可使用預設執行階段規格執行及排定管道。
8. 如果管道包含筆記本，請在「Notebook options」(筆記本選項) 部分的「Cloud Storage bucket」(Cloud Storage 值區) 欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage 值區，用於儲存管道中筆記本的輸出內容。

   您選取的服務帳戶必須獲得所選 bucket 的 Storage 管理員 IAM 角色。詳情請參閱「[啟用管道排程](#enable-scheduling)」。
9. 在「排程頻率」部分，執行下列操作：

   1. 在「Repeats」(重複時間間隔) 選單中，選取排定管道執行的頻率。
   2. 在「At time」(時間) 欄位中，輸入排定管道執行的時間。
   3. 在「時區」選單中，選取時間表的時區。
10. 使用「以高優先順序執行互動式工作 (預設)」選項，設定 BigQuery 查詢工作優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果清除這個選項，查詢會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行，優先順序較低。
11. 按一下「建立時間表」。如果選取「使用我的使用者憑證執行」做為驗證方法，您必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

建立時間表時，系統會自動部署管道的目前版本。如要使用新版管道更新排程，請[部署管道](#deploy)。

管道的最新部署版本會在所選時間和頻率執行。

**注意：** 如果預定管道執行作業未在下一次預定執行作業開始前完成，系統會略過下一次預定執行作業，並標示為錯誤。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下「建立」，然後從選單中選取「管線時間表」。
3. 在「Schedule pipeline」(排程管道) 窗格中，選取要排程的管道。
4. 在「排程名稱」欄位中，輸入排程名稱。
5. 在「Authentication」(驗證) 區段中，使用 Google 帳戶使用者憑證或服務帳戶授權管道。

   * 如要使用 Google 帳戶使用者憑證 ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「以我的使用者憑證執行」。
   * 如要使用服務帳戶，請選取「以所選服務帳戶執行」，然後選取服務帳戶。
6. 如果管道包含筆記本，請在「筆記本選項」部分，選取「執行階段範本」欄位中的 Colab 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」一文。

   **注意：**筆記本執行階段範本必須與管道位於相同區域。**注意：**如果您沒有使用 Colab 筆記本執行階段範本的[必要角色](#required_roles)，仍可使用預設執行階段規格執行及排定管道。
7. 如果管道包含筆記本，請在「Cloud Storage bucket」(Cloud Storage bucket) 欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket，用來儲存管道中筆記本的輸出內容。

   您選取的服務帳戶必須獲得所選 bucket 的 Storage 管理員 IAM 角色。詳情請參閱「[啟用管道排程](#enable-scheduling)」。
8. 在「排程頻率」部分，執行下列操作：

   1. 在「Repeats」(重複時間間隔) 選單中，選取排定管道執行的頻率。
   2. 在「At time」(時間) 欄位中，輸入排定管道執行的時間。
   3. 在「時區」選單中，選取時間表的時區。
9. 使用「以高優先順序執行互動式工作 (預設)」選項，設定 BigQuery 查詢工作優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果清除這個選項，查詢會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行，優先順序較低。
10. 按一下「建立時間表」。如果選取「使用我的使用者憑證執行」做為驗證方法，您必須[授權 Google 帳戶](#authorize-google-account) ([預覽](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

**注意：** 如果預定管道執行作業未在下一次預定執行作業開始前完成，系統會略過下一次預定執行作業，並標示為錯誤。

### 授權給您的 Google 帳戶

**預覽**

這項產品或功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前的產品和功能是按照「原樣」提供，支援範圍可能有限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要尋求支援或針對這項功能提供意見回饋，請傳送電子郵件至 [dataform-preview-support@google.com](mailto:dataform-preview-support@google.com)。

如要使用[Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)使用者憑證驗證資源，您必須手動授予 BigQuery 管道權限，讓管道取得 Google 帳戶的存取權杖，並代表您存取來源資料。您可以使用 OAuth 對話方塊介面手動授予核准。

您只需要授予 BigQuery 管道一次權限。

如要撤銷授予的權限，請按照下列步驟操作：

1. 前往 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)。
2. 按一下「BigQuery Pipelines」。
3. 按一下 [移除存取權]。

**警告：** 撤銷存取權後，這個 Google 帳戶在所有區域擁有的管道日後都無法執行。

如果新的 Google 帳戶擁有者從未建立過時間表，更新憑證以變更管道時間表擁有者時，也需要手動核准。

如果管道包含筆記本，您也必須手動授予 Colab Enterprise 權限，才能取得 Google 帳戶的存取權權杖，並以您的名義存取來源資料。你只需要授予一次權限。您可以在 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)撤銷這項權限。

## 部署管道

部署管道時，系統會使用管道的目前版本更新排程。排程會執行最新部署的 pipeline 版本。

如要部署管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 點選「Deploy」(部署)。

系統會使用管道的目前版本更新對應的排程。
系統會在排定的時間執行最新部署的管道版本。

## 停用時間表

如要暫停所選管道的排定執行作業，但不想刪除排程，可以停用排程。

如要停用所選管道的排程，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「查看時間表」。
5. 在「時間表詳細資料」表格的「時間表狀態」列中，按一下「時間表已啟用」切換鈕。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「排程詳細資料」頁面中，按一下「停用」。

## 啟用時間表

如要恢復已停用管道排程的排定執行作業，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「查看時間表」。
5. 在「時間表詳細資料」表格的「時間表狀態」列中，按一下「時間表已停用」切換鈕。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「時間表詳細資料」頁面上，按一下「啟用」。

## 手動執行已部署的管道

手動執行已部署的管道時，BigQuery 會執行一次管道，與排定的時間表無關。

如要手動執行已部署的管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道排程的名稱。
3. 在「排程詳細資料」頁面中，按一下「執行」。

## 查看所有管道排程

如要查看專案中的所有管道時間表，請按照下列步驟操作： Google Cloud

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 選用：如要顯示含有管道時間表詳細資料的其他資料欄，請按一下「資料欄顯示選項」view\_column，然後選取資料欄並按一下「確定」。

## 查看管道排程詳細資料

如要查看所選管道排程的詳細資料，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「查看時間表」。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道排程的名稱。

## 查看過去的排程執行作業

如要查看所選管道排程的過往執行記錄，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「執行」。
5. 選用：如要重新整理過往執行記錄清單，請按一下「重新整理」。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「排程詳細資料」頁面的「過去的執行作業」部分，檢查過去的執行作業。
4. 選用：如要重新整理過往執行記錄清單，請按一下「重新整理」。

## 編輯管道排程

如要編輯管道排程，請按照下列步驟操作：

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」，然後選取管道。
4. 按一下「查看時間表」，然後按一下「編輯」。
5. 在「排定管道」對話方塊中編輯排程，然後按一下「更新排程」。

### 「排定時間」頁面

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「排程詳細資料」頁面上，按一下「編輯」。
4. 按一下「查看時間表」，然後按一下「編輯」。
5. 在「排定管道」對話方塊中編輯排程，然後按一下「更新排程」。

## 刪除管道排程

如要永久刪除管道排程，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」頁面。

   [前往「排程」](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 執行下列其中一項操作：

   * 按一下所選管道排程的名稱，然後在「排程詳細資料」頁面中，按一下「刪除」。
   * 在包含所選管道排程的資料列中，按一下「Actions」(動作) 欄中的「View actions」(查看動作) more\_vert，然後按一下「Delete」(刪除)。
3. 在隨即顯示的對話方塊中，按一下「刪除」。

## 後續步驟

* 進一步瞭解 [BigQuery 中的管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)。
* 瞭解如何[建立管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-05-02 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-05-02 (世界標準時間)。"],[],[]]