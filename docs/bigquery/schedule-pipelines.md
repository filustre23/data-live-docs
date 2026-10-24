Google 會運用 AI 技術將內容翻譯成你偏好的語言，但可能會出錯。

* [Home](https://docs.cloud.google.com/?hl=zh-tw)
* [Documentation](https://docs.cloud.google.com/docs?hl=zh-tw)
* [Data analytics](https://docs.cloud.google.com/docs/data?hl=zh-tw)
* [BigQuery](https://docs.cloud.google.com/bigquery/docs?hl=zh-tw)
* [指南](https://docs.cloud.google.com/bigquery/docs/introduction?hl=zh-tw)

提供意見



透過集合功能整理內容

你可以依據偏好儲存及分類內容。

# 排定管道執行時間

本文說明如何排定 [BigQuery 管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)，包括如何排定管道和檢查排定的管道執行作業。

管道由 [Dataform](https://docs.cloud.google.com/dataform/docs/overview?hl=zh-tw) 提供技術支援。每個管道排程都會使用您的 Google 帳戶使用者憑證，或您在設定排程時選取的[自訂服務帳戶](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#about-service-accounts)執行。

您對管道所做的變更會自動儲存，但只有您和具備專案 Dataform 管理員角色的使用者可以查看。如要使用新版管道更新排程，請[部署管道](#deploy)。部署後，排程就會更新，改用目前的管道版本。排程一律會執行最新部署的版本。

含有筆記本的管道排程會使用[預設執行階段規格](https://docs.cloud.google.com/colab/docs/runtimes?hl=zh-tw#default_runtime_specifications)。如果管道含有筆記本，BigQuery 會在排定的執行期間，將筆記本輸出內容寫入建立排程時選取的 [Cloud Storage bucket](https://docs.cloud.google.com/storage/docs/buckets?hl=zh-tw)。

## 事前準備

開始之前，請先[建立管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。

### 啟用管道排程

如要排定管道執行時間，您必須將下列角色授予要用於管道排程的自訂服務帳戶：

[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)
:   按照「[授予服務帳戶單一角色](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw#grant-single-role)」一節的說明，將服務帳戶新增為主體。換句話說，請將服務帳戶新增為同一服務帳戶的主體。接著，將「服務帳戶使用者」角色授予這個主體。

如果管道包含 SQL 查詢，您必須將下列角色授予要用於管道排程的自訂服務帳戶或 Google 帳戶：

[BigQuery 工作使用者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.jobUser) (`roles/bigquery.jobUser`)
:   請按照[授予專案單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)的步驟，將 BigQuery 工作使用者角色授予自訂服務帳戶或 Google 帳戶，用於管道讀取資料的專案。

[BigQuery 資料檢視者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataViewer) (`roles/bigquery.dataViewer`)
:   按照[授予專案單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)的步驟，將 BigQuery 資料檢視者角色授予自訂服務帳戶或 Google 帳戶，用於管道讀取資料的專案。

[BigQuery 資料編輯者](https://docs.cloud.google.com/bigquery/docs/access-control?hl=zh-tw#bigquery.dataEditor) (`roles/bigquery.dataEditor`)
:   請按照[這篇文章](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)的指示，在專案中授予單一角色，將 BigQuery 資料編輯者角色授予自訂服務帳戶，或授予管道寫入資料的專案中的 Google 帳戶。

如果 pipeline 包含 Notebook，您必須將下列角色授予要用於 pipeline 排程的自訂服務帳戶或 Google 帳戶：

[Notebook 執行工具使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.notebookExecutorUser) (`roles/aiplatform.notebookExecutorUser`)
:   按照[授予專案單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)的說明，將 Notebook 執行者使用者角色授予所選專案的自訂服務帳戶或 Google 帳戶。

[儲存空間管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/storage?hl=zh-tw#storage.admin) (`roles/storage.admin`)
:   按照「[將主體新增至 bucket 層級政策](https://docs.cloud.google.com/storage/docs/access-control/using-iam-permissions?hl=zh-tw#bucket-add)」一文的指示，將自訂服務帳戶或 Google 帳戶新增為主體，加入您要用來儲存筆記本輸出內容的 Cloud Storage bucket (筆記本輸出內容是在排定的管道執行作業中執行)，然後將 Storage 管理員角色授予這些主體。

此外，您必須將下列角色授予預設 Dataform 服務代理：

[服務帳戶權杖建立者](https://docs.cloud.google.com/iam/docs/service-account-permissions?hl=zh-tw#token-creator-role) (`roles/iam.serviceAccountTokenCreator`)
:   按照「[將權杖建立權限授予服務帳戶](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#grant-token-creation-access)」一節的說明，將預設 Dataform 服務代理新增為服務帳戶的主體，並將「服務帳戶權杖建立者」角色授予這個主體。

[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser) (`roles/iam.serviceAccountUser`)
:   按照
    [使用 Google Cloud 控制台授予或撤銷多個 IAM 角色](https://docs.cloud.google.com/iam/docs/manage-access-service-accounts?hl=zh-tw#multiple-roles-console)
    一文中的步驟，將「服務帳戶使用者」角色授予自訂服務帳戶的預設
    Dataform 服務代理。

如要在 Knowledge Catalog 啟用中繼資料擴充功能，請務必啟用 [Dataplex API](https://console.cloud.google.com/flows/enableapi?apiid=dataplex.googleapis.com&hl=zh-tw)。此外，您必須將專案或 `@bigquery` 項目群組的下列角色，授予要用於管道排程的自訂服務帳戶或 Google 帳戶：

[Dataplex Catalog 編輯者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.catalogEditor) (`roles/dataplex.catalogEditor`)
:   按照「[授予專案單一角色](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw#grant-single-role)」一節的說明，將 Dataplex Catalog 編輯者角色授予專案或 `@bigquery` 項目群組的自訂服務帳戶或 Google 帳戶。

如要進一步瞭解 Dataform 中的服務帳戶，請參閱「[關於 Dataform 中的服務帳戶](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#about-service-accounts)」。

### VPC Service Controls 需求

如果您使用 VPC Service Controls 保護管道，請注意，排定的執行作業是由 Dataform 提供。為排定執行作業設定 VPC Service Controls 時，請務必符合下列規定：

* 您必須設定 [`dataform.restrictGitRemotes` 組織政策服務](https://docs.cloud.google.com/dataform/docs/restrict-git-remotes?hl=zh-tw)。
* Dataform 和 BigQuery 必須受相同的 VPC Service Controls service perimeter 限制。
* 如要允許使用者在排定或手動觸發執行作業時，使用 Google 帳戶的使用者憑證進行驗證，您必須將他們的使用者身分新增至輸入規則。詳情請參閱「[更新 service perimeter 的輸入和輸出政策](https://docs.cloud.google.com/vpc-service-controls/docs/configuring-ingress-egress-policies?hl=zh-tw#updating)」和「[輸入規則參考資料](https://docs.cloud.google.com/vpc-service-controls/docs/ingress-egress-rules?hl=zh-tw#ingress-rules-reference)」。

如需詳細設定步驟和安全性考量，請參閱「[設定 Dataform 的 VPC Service Controls](https://docs.cloud.google.com/dataform/docs/vpc-service-controls?hl=zh-tw)」。

### 必要的角色

如要取得管理管道所需的權限，請要求管理員授予您下列 IAM 角色：

* 查看及管理時間表：
  + 管道的 [Dataform 管理員](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.admin)  (`roles/dataform.admin`)
  + 專案的 [Dataform 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.editor)  (`roles/dataform.editor`)
* 查看及執行管道：
  + 專案的 [Dataform 檢視者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.viewer)  (`roles/dataform.viewer`)
  + 專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 使用 Google 帳戶的使用者憑證執行管道排程：專案的 [BigQuery 工作使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/bigquery?hl=zh-tw#bigquery.jobUser)  (`roles/bigquery.jobUser`)
* 使用自訂服務帳戶執行 pipeline 排程：自訂服務帳戶的[服務帳戶使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/iam?hl=zh-tw#iam.serviceAccountUser)  (`roles/iam.serviceAccountUser`)
* 管理使用者資料夾中的管道排程：
  + 資料夾的[程式碼擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.codeOwner)  (`roles/dataform.codeOwner`)
  + 資料夾上的「Code Editor」(程式碼編輯器) (`roles/dataform.codeEditor`)
* 管理團隊資料夾中的管道排程：
  + 團隊資料夾的[團隊資料夾擁有者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.teamFolderOwner)  (`roles/dataform.teamFolderOwner`)
  + 團隊資料夾的[團隊資料夾協作者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataform?hl=zh-tw#dataform.teamFolderContributor)  (`roles/dataform.teamFolderContributor`)
* 管理 Git 存放區中的管道：專案的 [Developer Connect OAuth 使用者](https://docs.cloud.google.com/iam/docs/roles-permissions/developerconnect?hl=zh-tw#developerconnect.oauthUser)  (`roles/developerconnect.oauthUser`)
* 啟用中繼資料擴充功能：專案或 `@bigquery` 項目群組的 [Dataplex Catalog 編輯者](https://docs.cloud.google.com/iam/docs/roles-permissions/dataplex?hl=zh-tw#dataplex.catalogEditor)  (`roles/dataplex.catalogEditor`)

如要進一步瞭解如何授予角色，請參閱「[管理專案、資料夾和組織的存取權](https://docs.cloud.google.com/iam/docs/granting-changing-revoking-access?hl=zh-tw)」。

您或許也能透過[自訂角色](https://docs.cloud.google.com/iam/docs/creating-custom-roles?hl=zh-tw)或其他[預先定義的角色](https://docs.cloud.google.com/iam/docs/roles-overview?hl=zh-tw#predefined)，取得必要權限。

如要提高排程安全性，請參閱「[實作強化排程權限](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw#enhanced-scheduling-permissions)」。

如要進一步瞭解 Dataform IAM，請參閱「[使用 IAM 控管存取權](https://docs.cloud.google.com/dataform/docs/access-control?hl=zh-tw)」。

如要進一步瞭解資料夾的角色，請參閱「[建立及管理資料夾](https://docs.cloud.google.com/bigquery/docs/create-manage-folders?hl=zh-tw#required_roles)」。

如要進一步瞭解 Git 存放區的角色，請參閱「[使用 BigQuery Studio Git 存放區管理程式碼](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw#required_roles)」。

如要在排定 pipeline 時使用 Colab 筆記本執行階段範本，您必須具備[筆記本執行階段使用者角色](https://docs.cloud.google.com/iam/docs/roles-permissions/aiplatform?hl=zh-tw#aiplatform.notebookRuntimeUser) (`roles/aiplatform.notebookRuntimeUser`)。

## 建立管道排程

您也可以使用「Pipelines & Connections」(管道和連線) 頁面，透過[簡化的 BigQuery 專屬工作流程](https://docs.cloud.google.com/bigquery/docs/pipeline-connection-page?hl=zh-tw)排定 Dataform 管道。這項功能為[預先發布版](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如果管道儲存在 BigQuery Studio Git 資料夾中，則會透過 [Dataform 部署作業](#deploy-git-pipelines)管理排程。

如要建立管道排程，請按照下列步驟操作：

### 「Files」(檔案) 窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下 folder「Files」(檔案)，開啟檔案瀏覽器。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Files」(檔案) 窗格中，展開「User」(使用者) 資料夾或「Team folder」(團隊資料夾)，然後選取管道。
4. 在「Pipeline Viewer」工具列中，按一下「Schedule」(排程) 或「Trigger」(觸發)。
5. 在「Schedule pipeline」(排定管道) 窗格的「Schedule name」(排程名稱) 欄位中，輸入排程名稱。
6. 在「Authentication」(驗證) 區段中，使用 Google 帳戶使用者憑證或服務帳戶，為管道授權。

   * 如要使用 Google 帳戶使用者憑證 ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))，請選取「Execute with my user credentials」(以我的使用者憑證執行)。

     選用：在「Extended access options」(擴充存取權選項) 部分，選取管道所需的其他服務：

     + **Knowledge Catalog**：可更新 Google Cloud Knowledge Catalog 中繼資料。
     + **Google 雲端硬碟**：允許唯讀存取 Google 雲端硬碟檔案。
     + **Bigtable**：可讀取 Google Bigtable 資料 (唯讀)。
   * 如要使用服務帳戶，請選取「Execute with selected service account」(以所選服務帳戶執行)，然後選取服務帳戶。
7. 如果管道包含筆記本，請在「Notebook options」(筆記本選項) 區段的「Runtime template」(執行階段範本) 欄位中，選取 Colaboratory 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。

   **注意：**筆記本執行階段範本必須與管道位於相同區域。**注意：**如果您沒有使用 Colab 筆記本執行階段範本的[必要角色](#required_roles)，仍可使用預設執行階段規格執行及排定管道。
8. 如果管道包含筆記本，請在「Notebook options」(筆記本選項) 區段的「Cloud Storage bucket」欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket，用於儲存管道中筆記本的輸出內容。

   您選取的服務帳戶必須具備所選 bucket 的 Storage 管理員 IAM 角色。詳情請參閱「[啟用管道排程](#enable-scheduling)」。
9. 在「Configuration Type」(設定類型) 下方，選取「Schedule (time-based recurrence)」(排程 (依時間週期))。
10. 在「Schedule frequency」(排程頻率) 下方，執行下列操作：

    1. 在「Repeats」(重複) 選單中，選取排定管道執行的頻率。
    2. 在「At time」(時間) 欄位中，輸入排定的管道執行時間。
    3. 在「Timezone」(時區) 選單中，選取排程的時區。
11. 使用「Execute as interactive job with high priority (default)」(以高優先順序執行互動式工作 (預設)) 選項，設定 BigQuery 查詢工作的優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果取消勾選這個選項，系統會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，優先順序較低。
12. 按一下「建立排程」。如果驗證方式選取「Execute with my user credentials」(使用我的使用者憑證執行)，則必須[授權 Google 帳戶](#authorize-google-account) ([預先發布版](https://cloud.google.com/products?hl=zh-tw#product-launch-stages))。

建立排程時，系統會自動部署目前的管道版本。如要使用新版管道更新排程，請[部署管道](#deploy)。

最新部署的管道版本會按照所選時間和頻率執行。

**注意：** 如果排定的管道執行作業未在下次排定的執行作業開始前完成，系統會略過下次排定的執行作業，並標示錯誤。

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。

   如果沒有看到左側窗格，請按一下 last\_page「Expand left pane」(展開左側窗格)，開啟窗格。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下「Schedule」(排程)。
5. 在「Schedule pipeline」(排定管道) 窗格的「Schedule name」(排程名稱) 欄位中，輸入排程名稱。
6. 在「Authentication」(驗證) 區段中，使用 Google 帳戶使用者憑證或服務帳戶，為管道授權。

   * 如要使用 Google 帳戶使用者憑證，請選取「Execute with my user credentials」(以我的使用者憑證執行)。

     選用：在「Extended access options」(擴充存取權選項) 部分，選取管道所需的其他服務：

     + **Knowledge Catalog**：可更新 Google Cloud Knowledge Catalog 中繼資料。
     + **Google 雲端硬碟**：允許唯讀存取 Google 雲端硬碟檔案。
     + **Bigtable**：可讀取 Google Bigtable 資料 (唯讀)。
   * 如要使用服務帳戶，請選取「Execute with selected service account」(以所選服務帳戶執行)，然後選取服務帳戶。
7. 如果管道包含筆記本，請在「Notebook options」(筆記本選項) 區段的「Runtime template」(執行階段範本) 欄位中，選取 Colaboratory 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。

   **注意：**筆記本執行階段範本必須與管道位於相同區域。**注意：**如果您沒有使用 Colab 筆記本執行階段範本的[必要角色](#required_roles)，仍可使用預設執行階段規格執行及排定管道。
8. 如果管道包含筆記本，請在「Notebook options」(筆記本選項) 區段的「Cloud Storage bucket」欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket，用於儲存管道中筆記本的輸出內容。

   您選取的服務帳戶必須具備所選 bucket 的 Storage 管理員 IAM 角色。詳情請參閱「[啟用管道排程](#enable-scheduling)」。
9. 在「Configuration Type」(設定類型) 下方，選取「Schedule (time-based recurrence)」(排程 (依時間週期))。
10. 在「Schedule frequency」(排程頻率) 下方，執行下列操作：

    1. 在「Repeats」(重複) 選單中，選取排定管道執行的頻率。
    2. 在「At time」(時間) 欄位中，輸入排定的管道執行時間。
    3. 在「Timezone」(時區) 選單中，選取排程的時區。
11. 使用「Execute as interactive job with high priority (default)」(以高優先順序執行互動式工作 (預設)) 選項，設定 BigQuery 查詢工作優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果取消勾選這個選項，系統會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，優先順序較低。
12. 按一下「建立排程」。如果驗證方式選取「Execute with my user credentials」(使用我的使用者憑證執行)，則必須[授權 Google 帳戶](#authorize-google-account)。

建立排程時，系統會自動部署目前的管道版本。如要使用新版管道更新排程，請[部署管道](#deploy)。

管道的最新部署版本會按照所選時間和頻率執行。

**注意：** 如果排定的管道執行作業未在下次排定的執行作業開始前完成，系統會略過下次排定的執行作業，並標示錯誤。

### 「排程」頁面

1. 前往 Google Cloud 控制台的「Scheduling」(排程) 頁面。

   [前往「排程」頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下「建立」，然後從選單中選取「管道排程」。
3. 在「Schedule pipeline」(排定管道) 窗格中，選取要排定的管道。
4. 在「Schedule name」(排程名稱) 欄位中，輸入排程名稱。
5. 在「Authentication」(驗證) 區段中，使用 Google 帳戶使用者憑證或服務帳戶，為管道授權。

   * 如要使用 Google 帳戶使用者憑證，請選取「Execute with my user credentials」(以我的使用者憑證執行)。

     選用：在「Extended access options」(擴充存取權選項) 部分，選取管道所需的其他服務：

     + **Knowledge Catalog**：可更新 Google Cloud Knowledge Catalog 中繼資料。
     + **Google 雲端硬碟**：允許唯讀存取 Google 雲端硬碟檔案。
     + **Bigtable**：可讀取 Google Bigtable 資料 (唯讀)。
   * 如要使用服務帳戶，請選取「Execute with selected service account」(以所選服務帳戶執行)，然後選取服務帳戶。
6. 如果管道包含筆記本，請在「Notebook options」(筆記本選項) 區段的「Runtime template」(執行階段範本) 欄位中，選取 Colab 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。

   **注意：**筆記本執行階段範本必須與管道位於相同區域。**注意：**如果您沒有使用 Colab 筆記本執行階段範本的[必要角色](#required_roles)，仍可使用預設執行階段規格執行及排定管道。
7. 如果管道包含筆記本，請在「Cloud Storage bucket」欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket，用於儲存管道中筆記本的輸出內容。

   您選取的服務帳戶必須具備所選 bucket 的 Storage 管理員 IAM 角色。詳情請參閱「[啟用管道排程](#enable-scheduling)」。
8. 在「Configuration Type」(設定類型) 下方，選取「Schedule (time-based recurrence)」(排程 (依時間週期))。
9. 在「Schedule frequency」(排程頻率) 下方，執行下列操作：

   1. 在「Repeats」(重複) 選單中，選取排定管道執行的頻率。
   2. 在「At time」(時間) 欄位中，輸入排定的管道執行時間。
   3. 在「Timezone」(時區) 選單中，選取排程的時區。
10. 使用「Execute as interactive job with high priority (default)」(以高優先順序執行互動式工作 (預設)) 選項，設定 BigQuery 查詢工作優先順序。根據預設，BigQuery 會以[互動式查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，這類工作會盡快開始執行。如果取消勾選這個選項，系統會以[批次查詢工作](https://docs.cloud.google.com/bigquery/docs/running-queries?hl=zh-tw#interactive-batch)的形式執行查詢，優先順序較低。
11. 按一下「建立排程」。如果驗證方式選取「Execute with my user credentials」(使用我的使用者憑證執行)，則必須[授權 Google 帳戶](#authorize-google-account)。

**注意：** 如果排定的 pipeline 執行作業未在下一次排定的執行作業開始前完成，系統會略過下一次排定的執行作業，並標示錯誤。

### 授權給您的 Google 帳戶

如要使用 [Google 帳戶](https://docs.cloud.google.com/iam/docs/principals-overview?hl=zh-tw#google-account)使用者憑證驗證資源，您必須手動授予權限，讓 BigQuery 管道取得 Google 帳戶的存取權杖，並代表您存取來源資料。您可以使用 OAuth 對話方塊介面手動授予核准。如果選取任何「Extended access options」，就必須授予這些服務的存取權，例如 Google 雲端硬碟或 Knowledge Catalog。

**注意：** 使用 Google 帳戶的使用者憑證執行或排定 BigQuery 管道時，不支援情境感知存取權 (CAA) 政策，包括 IP、地理位置和裝置法規遵循政策，因為權杖要求源自 Google 基礎架構。除非 Dataform OAuth 用戶端 ID [不受政策限制](https://docs.cloud.google.com/dataform/docs/troubleshooting?hl=zh-tw#euc-permission-denied)，否則 CAA 政策會封鎖這些執行作業。

您只需要授予 BigQuery 管道權限一次。

如要撤銷已授予的權限，請按照下列步驟操作：

1. 前往 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)。
2. 按一下「BigQuery Pipelines」。
3. 按一下 [移除存取權]。

**警告：** 撤銷存取權限後，這個 Google 帳戶擁有者在所有區域擁有的管道，日後都無法執行。

如果新的 Google 帳戶擁有者從未建立過排程，則透過更新憑證變更管道排程擁有者時，也需要手動核准。

如果管道含有筆記本，您也必須手動授予權限，Colab Enterprise 才能取得 Google 帳戶的存取權杖，並代表您存取來源資料。只需授予權限一次。您可以在 [Google 帳戶頁面](https://myaccount.google.com/?hl=zh-tw)撤銷這項權限。

## 依指定條件觸發排程

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

**注意：** 如要取得支援或提供這項功能的意見回饋，請傳送電子郵件至 [bigquery-event-based-triggers@google.com](mailto:bigquery-event-based-triggers@google.com)。

您可以設定 BigQuery 管道，根據指定 BigQuery 資料表的更新，自動觸發執行作業。您可以建立以觸發條件為基礎的時間表，根據 BigQuery 資料的變更自動執行管道，而非按照固定時間表執行。

當 pipeline 偵測到指定資料表有變更時，就會觸發相關聯工作流程的新執行作業。您可以根據單一資料表、一組資料表中的所有資料表，或一組資料表中的任何資料表更新，定義條件。

您也可以調整觸發條件式排程的選用設定，控管管道觸發條件之間的最短間隔。舉例來說，您可以調整「Min Execution Duration」(最短執行時間長度) 值，確保觸發條件式排程不會過於頻繁地啟動。您也可以調整「Max Wait Duration」(最長等待時間) 值，確保即使未偵測到資料表更新，系統也會在該時間內強制啟用以觸發條件為依據的時間表。

### 限制

觸發條件式排程有下列限制：

* 觸發條件式排程不會立即生效。設定以觸發條件為依據的時間表時，管道會每隔約 3 分鐘檢查一次 BigQuery 資料表的狀態。這段時間稱為輪詢間隔，可能會導致資料表修改和觸發條件啟用之間出現延遲。
* 在每個輪詢間隔期間，每個受監控的資料表都會向 BigQuery 發出 API 呼叫。監控大量資料表可能會導致 [BigQuery API 配額用量](https://docs.cloud.google.com/bigquery/docs/troubleshoot-quotas?hl=zh-tw#ts-maximum-api-request-limit)增加。

### 建立觸發條件

如要建立觸發條件，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在管道檢視器中開啟管道，方法如下：

   * 在左側窗格中，按一下「檔案」folder，展開「使用者」資料夾或「團隊資料夾」，然後選取管道。
   * 在左側窗格中，按一下「explore Explorer」，展開專案，按一下「Pipelines」，然後選取管道。
3. 在 Pipeline Viewer 工具列中，按一下「Trigger」(觸發)。
4. 在「Trigger」(觸發條件) 欄位中，輸入觸發條件的名稱。
5. 在「Authentication」(驗證) 區段中，使用 Google 帳戶使用者憑證或服務帳戶，為管道授權。

   * 如要使用 Google 帳戶使用者憑證，請選取「Execute with my user credentials」(以我的使用者憑證執行)。

     選用：在「Extended access options」(擴充存取權選項) 部分，選取管道所需的其他服務：

     + **Knowledge Catalog**：可更新 Google Cloud Knowledge Catalog 中繼資料。
     + **Google 雲端硬碟**：允許唯讀存取 Google 雲端硬碟檔案。
     + **Bigtable**：可讀取 Google Bigtable 資料 (唯讀)。
   * 如要使用服務帳戶，請選取「Execute with selected service account」(以所選服務帳戶執行)，然後選取服務帳戶。
6. 如果管道包含筆記本，請在「Notebook options」(筆記本選項) 區段的「Runtime template」(執行階段範本) 欄位中，選取 Colaboratory 筆記本執行階段範本或預設執行階段規格。如要進一步瞭解如何建立 Colab 筆記本執行階段範本，請參閱「[建立執行階段範本](https://docs.cloud.google.com/colab/docs/create-runtime-template?hl=zh-tw)」。

   **注意：**筆記本執行階段範本必須與管道位於相同區域。**注意：**如果您沒有使用 Colab 筆記本執行階段範本的[必要角色](#required_roles)，仍可使用預設執行階段規格執行及排定管道。
7. 如果管道包含筆記本，請在「Notebook options」(筆記本選項) 區段的「Cloud Storage bucket」欄位中，按一下「Browse」(瀏覽)，然後選取或建立 Cloud Storage bucket，用於儲存管道中筆記本的輸出內容。

   您選取的服務帳戶必須具備所選 bucket 的 Storage 管理員 IAM 角色。詳情請參閱「[啟用管道排程](#enable-scheduling)」。
8. 在「Configuration Type」(設定類型) 下方，選取「Trigger (event-based execution)」(觸發條件 (事件型執行作業))。
9. 在「Search tables」(搜尋資料表) 欄位中，新增要監控觸發條件的一或多個資料表。
10. 在「觸發條件」下方，選取下列任一選項：

    * **等待「所有」資料表更新**：只有在上次檢查後，所有列出的資料表都已更新，才會觸發工作流程。
    * **「任意」資料表更新就會觸發**：如果上次檢查後，有任何列出的資料表更新，就會觸發這個工作流程。
11. (選用) 在「Max Wait Duration」(最長等待時間) 部分，輸入一段時間長度。如果在這段時間內未偵測到資料表更新，系統會強制啟用觸發條件。支援 1 秒到 7 天之間的值。如未指定，則只有在監控的資料表更新，且符合最短執行時間時，工作流程才會執行。
12. (選用) 在「Min Execution Duration」(最短執行時間長度)，選取時間長度，避免觸發條件的啟用頻率高於這個最短時間長度。支援 3 分鐘到 24 小時之間的值。如未指定，預設值為 3 分鐘。
13. 按一下「建立排程」。如果驗證方式選取「Execute with my user credentials」(使用我的使用者憑證執行)，則必須[授權 Google 帳戶](#authorize-google-account)。

### 疑難排解依觸發條件觸發的時間表問題

本節說明觸發條件式排程的常見問題，以及解決方法。

問題：觸發條件未啟動
:   **解決方法：**請嘗試下列任一步驟：

    * 確認使用者憑證或服務帳戶具備所有[必要權限](#required_roles)。
    * 確認指定的 BigQuery 資料表是否正在修改。
    * 確認觸發條件未受到[輪詢間隔](#limitations)影響。
    * 檢查最短執行時間 (即「Min Execution Duration」(最短執行時間) 值) 是否會阻礙更頻繁的執行。您可以調低這個值，提高觸發條件的啟用頻率。
    * 檢查觸發條件選項 (「全部」或「任一」) 是否會影響觸發條件啟用。
    * 檢查[稽核記錄](https://docs.cloud.google.com/bigquery/docs/introduction-audit-workloads?hl=zh-tw)，確認 Dataform 嘗試呼叫 BigQuery API 來檢查受監控資料表的狀態時，是否發生錯誤。

問題：觸發條件太常啟動
:   **解決方法：**調整執行時間下限或「Min Execution Duration」(執行時間下限) 值。您可以提高這個值，降低觸發條件的啟用頻率。

## 部署管道

部署管道時，系統會以目前版本的管道更新其排程或自動化調度管理設定。排定的執行作業一律會執行最新部署的 pipeline 版本。

### 部署儲存在資料夾中的管道

如要部署獨立管道和儲存在資料夾中的管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在**管道檢視器**中開啟管道，方法如下：

   * 在左側窗格中，按一下「檔案」圖示 folder，展開「使用者」資料夾或「團隊資料夾」，然後選取管道。
   * 在左側窗格中，按一下「explore Explorer」，展開專案，按一下「Pipelines」，然後選取管道。
3. 在「Pipeline Viewer」工具列中，按一下「Deploy」。

相應排程會更新為目前版本的管道。最新部署的管道版本會在排定時間執行。

### 部署儲存在 Git 存放區的管道

**預覽**

這項功能適用《[服務專屬條款](https://docs.cloud.google.com/terms/service-terms?hl=zh-tw#1)》中「一般服務條款」一節的《正式發布前產品條款》。正式發布前功能是依「原樣」提供，支援服務可能受限。
詳情請參閱[推出階段說明](https://cloud.google.com/products/?hl=zh-tw#product-launch-stages)。

儲存在 Git 資料夾中的管道會使用 Dataform [部署作業](https://docs.cloud.google.com/dataform/docs/deployments?hl=zh-tw)進行自動化調度管理和排程。您可以透過 Deployment 設定版本、工作流程、編譯覆寫和多環境自動調度管理。

如要部署儲存在 Git 存放區的管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder 檔案」。
3. 在檔案樹狀結構中，展開已連結的 Git 存放區資料夾，然後選取管道。如果管道位於根層級，請點選 Git 存放區資料夾。
4. 在「Pipeline Viewer」工具列中，按一下「Deploy」。
5. 在部署對話方塊中，調整版本設定、工作流程設定和執行設定。
6. 點選「Deploy」(部署)。

如要進一步瞭解如何設定部署作業、版本設定和工作流程設定，請參閱「[Dataform 部署作業](https://docs.cloud.google.com/dataform/docs/deployments?hl=zh-tw)」。

## 停用時間表

如要暫停所選 pipeline 的排定執行作業，但不刪除排程，可以停用排程。

如要停用所選管道的時間表，請按照下列步驟操作：

### 「Files」(檔案) 窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder 檔案」。
3. 在「Files」窗格中，展開「User」資料夾或「Team folder」，然後選取管道。
4. 在管道檢視器工具列中，按一下「View trigger」(查看觸發條件)。
5. 在「Schedule details」(排程詳細資料) 表格中，按一下「Schedule state」(排程狀態) 列中的「Schedule is enabled」(已啟用排程) 切換鈕。

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下「查看觸發條件」。
5. 在「Schedule details」(排程詳細資料) 表格中，按一下「Schedule state」(排程狀態) 列中的「Schedule is enabled」(已啟用排程) 切換鈕。

### 「排程」頁面

1. 前往 Google Cloud 控制台的「Scheduling」(排程) 頁面。

   [前往「排程」頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「Schedule details」(排程詳細資料) 頁面中，按一下「Disable」(停用)。

## 啟用時間表

如要恢復已停用管道排程的排定執行作業，請按照下列步驟操作：

### 「Files」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder 檔案」。
3. 在「Files」窗格中，展開「User」資料夾或「Team folder」，然後選取管道。
4. 在「Pipeline Viewer」工具列中，按一下「View trigger」。
5. 在「Schedule details」(排程詳細資料) 表格中，按一下「Schedule state」(排程狀態) 列中的「Schedule is disabled」(排程已停用) 切換鈕。

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下「查看觸發條件」。
5. 在「Schedule details」(排程詳細資料) 表格中，按一下「Schedule state」(排程狀態) 列中的「Schedule is disabled」(排程已停用) 切換鈕。

### 「排程」頁面

1. 前往 Google Cloud 控制台的「Scheduling」(排程) 頁面。

   [前往「排程」頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「Schedule details」(排程詳細資料) 頁面中，按一下「Enable」(啟用)。

## 手動執行已部署的管道

手動執行已部署至特定排程的管道時，BigQuery 會執行該管道一次，不受排程影響。

如要手動執行已部署的管道，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」(排程) 頁面。

   [前往「排程」頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道排程的名稱。
3. 在「Schedule details」(排程詳細資料) 頁面中，按一下「Run」(執行)。

## 查看所有管道排程

如要查看 Google Cloud 專案中的所有管道排程，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」(排程) 頁面。

   [前往「排程」頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 選用：如要顯示其他資料欄，查看管道排程詳細資料，請按一下 view\_column「Column display options」(資料欄顯示選項)，然後選取資料欄並點選「OK」(確定)。

## 查看管道排程詳細資料

如要查看所選管道排程的詳細資料，請按照下列步驟操作：

### 「Files」(檔案) 窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder 檔案」。
3. 在「Files」窗格中，展開「User」資料夾或「Team folder」，然後選取管道。
4. 在「Pipeline Viewer」工具列中，按一下「View trigger」(查看觸發條件) (或「View trigger」(查看觸發條件))。

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下「查看觸發條件」。

### 「排程」頁面

1. 前往 Google Cloud 控制台的「Scheduling」(排程) 頁面。

   [前往「排程」頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道排程的名稱。

## 查看過往排定的執行作業

如要查看所選管道排程的過往執行作業，請按照下列步驟操作：

### **檔案**窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder 檔案」。
3. 在「Files」窗格中，展開「User」資料夾、「Team folder」或 Git 存放區，然後選取管道。
4. 在「Pipeline Viewer」工具列中，按一下「Executions」。
5. 選用：如要重新整理過去執行作業的清單，請按一下「Refresh」(重新整理)。

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 按一下「Executions」(執行作業)。
5. 選用：如要重新整理過去執行作業的清單，請按一下「Refresh」(重新整理)。

### 「排程」頁面

1. 前往 Google Cloud 控制台的「Scheduling」(排程) 頁面。

   [前往「排程」頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「Schedule details」(排程詳細資料) 頁面的「Past executions」(過去執行作業) 區段中，檢查過去的執行作業。
4. 選用：如要重新整理過去執行作業的清單，請按一下「Refresh」(重新整理)。

## 編輯管道排程

如要編輯管道排程，請按照下列步驟操作：

### 「Files」(檔案) 窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 在左側窗格中，按一下「folder 檔案」。
3. 在「Files」窗格中，展開「User」資料夾或「Team folder」，然後選取管道。
4. 在「Pipeline Viewer」工具列中，依序點選「View trigger」(查看觸發條件) 和「Edit」(編輯)。
5. 在「Schedule pipeline」(排定管道) 對話方塊中編輯排程，然後按一下「Update schedule」(更新排程)。

### 「Explorer」窗格

1. 前往 Google Cloud 控制台的「BigQuery」頁面。

   [前往「BigQuery」](https://console.cloud.google.com/bigquery?hl=zh-tw)
2. 點選左側窗格中的 explore「Explorer」。
3. 在「Explorer」窗格中展開專案，按一下「Pipelines」(管道)，然後選取管道。
4. 依序點選「查看觸發條件」和「編輯」。
5. 在「Schedule pipeline」(排定管道) 對話方塊中編輯排程，然後按一下「Update schedule」(更新排程)。

### 「排程」頁面

1. 前往 Google Cloud 控制台的「Scheduling」(排程) 頁面。

   [前往「排程」頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 按一下所選管道的名稱。
3. 在「Schedule details」(排程詳細資料) 頁面中，按一下「Edit」(編輯)。
4. 依序點選「查看觸發條件」和「編輯」。
5. 在「Schedule pipeline」(排定管道) 對話方塊中編輯排程，然後按一下「Update schedule」(更新排程)。

## 刪除管道排程

如要永久刪除管道排程，請按照下列步驟操作：

1. 前往 Google Cloud 控制台的「Scheduling」(排程) 頁面。

   [前往「排程」頁面](https://console.cloud.google.com/bigquery/orchestration?hl=zh-tw)
2. 執行下列任一操作：

   * 按一下所選管道排程的名稱，然後在「Schedule details」(排程詳細資料) 頁面中，點選「Delete」(刪除)。
   * 在含有選定管道排程的資料列中，按一下「Actions」(動作) 欄中的 more\_vert「View actions」(查看動作)，然後按一下「Delete」(刪除)。
3. 在顯示的對話方塊中，按一下「刪除」。

## 後續步驟

* 進一步瞭解 [BigQuery 中的管道](https://docs.cloud.google.com/bigquery/docs/pipelines-introduction?hl=zh-tw)。
* 瞭解如何[建立管道](https://docs.cloud.google.com/bigquery/docs/create-pipelines?hl=zh-tw)。
* 瞭解如何[管理管道](https://docs.cloud.google.com/bigquery/docs/manage-pipelines?hl=zh-tw)。
* 瞭解如何[使用 BigQuery Studio Git 存放區管理程式碼](https://docs.cloud.google.com/bigquery/docs/git-repositories?hl=zh-tw)。
* 瞭解如何[使用資料夾整理程式碼資產](https://docs.cloud.google.com/bigquery/docs/code-asset-folders?hl=zh-tw)。
* 進一步瞭解 [Dataform 部署作業](https://docs.cloud.google.com/dataform/docs/deployments?hl=zh-tw)。




提供意見

除非另有註明，否則本頁面中的內容是採用[創用 CC 姓名標示 4.0 授權](https://creativecommons.org/licenses/by/4.0/)，程式碼範例則為[阿帕契 2.0 授權](https://www.apache.org/licenses/LICENSE-2.0)。詳情請參閱《[Google Developers 網站政策](https://developers.google.com/site-policies?hl=zh-tw)》。Java 是 Oracle 和/或其關聯企業的註冊商標。

上次更新時間：2026-10-22 (世界標準時間)。




想進一步說明嗎？

[[["容易理解","easyToUnderstand","thumb-up"],["確實解決了我的問題","solvedMyProblem","thumb-up"],["其他","otherUp","thumb-up"]],[["難以理解","hardToUnderstand","thumb-down"],["資訊或程式碼範例有誤","incorrectInformationOrSampleCode","thumb-down"],["缺少我需要的資訊/範例","missingTheInformationSamplesINeed","thumb-down"],["翻譯問題","translationIssue","thumb-down"],["其他","otherDown","thumb-down"]],["上次更新時間：2026-10-22 (世界標準時間)。"],[],[]]